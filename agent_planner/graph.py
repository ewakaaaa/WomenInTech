"""LangGraph wiring for the planner agent (non-linear, with human-in-the-loop).

Unlike the linear/`agent_langgraph` pipelines, here the **planner** is the hub:
everything returns to it and it decides the next move (analyze more / ask the human /
write / no grounds). That makes the graph cyclic — exactly what LangGraph is good at.
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send, interrupt

from agent_planner.state import DescribeFileIn, PlannerState, RunTaskIn
from src.descriptions import descriptions_cached, load_descriptions, save_descriptions
from src.loader import load_all
from src.skills.document.main import generate_document
from src.skills.file_description.main import generate_file_description
from src.skills.make_task.main import make_task
from src.skills.planner.main import plan_next
from src.skills.strategy.schemas import Strategy
from src.sources import prepare_input_texts

MAX_ROUNDS = 4  # bezpiecznik na nieskończoną pętlę planera


# --- nodes ---


def load_node(state: PlannerState) -> dict:
    # Podłącz opisy z cache, jeśli istnieją (inaczej policzy je fan-out poniżej).
    cached = load_descriptions() if descriptions_cached() else []
    return {"documents": load_all(), "files_out": cached}


def file_description_node(payload: DescribeFileIn) -> dict:
    described = generate_file_description(payload["document"], payload["goal"])
    return {"files_out": [described]}


def planner_node(state: PlannerState) -> dict:
    # Pierwszy raz po policzeniu opisów (cache pusty) — zapisz je do ponownego użycia.
    if state.get("files_out") and not descriptions_cached():
        save_descriptions(state["files_out"])
    decision = plan_next(
        state["goal"],
        state["files_out"],
        state.get("task_outputs", []),
        state.get("human_feedback"),
    )
    return {"decision": decision, "rounds": state.get("rounds", 0) + 1}


def make_task_node(payload: RunTaskIn) -> dict:
    output = make_task(payload["goal"], payload["task"], payload["sources_text"])
    return {"task_outputs": [output]}


def human_node(state: PlannerState) -> dict:
    # Pauza grafu — czeka na decyzję człowieka (radcy). Wymaga checkpointera.
    feedback = interrupt(state["decision"].summary_for_human)
    return {"human_feedback": feedback}


def document_node(state: PlannerState) -> dict:
    decision = state["decision"]
    strategy = Strategy(
        definition_of_success=state["goal"],
        strategies=decision.reasoning,
        best_strategy=decision.conclusion or decision.reasoning,
    )
    document = generate_document(state["goal"], strategy, state.get("task_outputs", []))
    return {"document": document.tekst}


def conclude_node(state: PlannerState) -> dict:
    return {"document": "BRAK PODSTAW DO APELACJI\n\n" + state["decision"].conclusion}


# --- routing ---


def fan_out_files(state: PlannerState):
    # Cache trafiony — opisy już w files_out, pomijamy fan-out i od razu do planera.
    if state.get("files_out"):
        return "planner"
    return [
        Send("file_description", DescribeFileIn(goal=state["goal"], document=doc))
        for doc in state["documents"]
    ]


def route_after_planner(state: PlannerState):
    decision = state["decision"]
    if state.get("rounds", 0) > MAX_ROUNDS:
        return "document"  # bezpiecznik: piszemy, zamiast się zapętlić
    if decision.action == "analyze" and decision.new_tasks:
        return [
            Send(
                "make_task",
                RunTaskIn(
                    goal=state["goal"],
                    task=task,
                    sources_text=prepare_input_texts(state["documents"], task.input),
                ),
            )
            for task in decision.new_tasks
        ]
    if decision.action == "ask_human":
        return "human"
    if decision.action == "no_grounds":
        return "conclude"
    return "document"


def build_graph(checkpointer=None):
    graph = StateGraph(PlannerState)

    graph.add_node("load", load_node)
    graph.add_node("file_description", file_description_node)
    graph.add_node("planner", planner_node)
    graph.add_node("make_task", make_task_node)
    graph.add_node("human", human_node)
    graph.add_node("document", document_node)
    graph.add_node("conclude", conclude_node)

    graph.add_edge(START, "load")
    graph.add_conditional_edges("load", fan_out_files, ["file_description", "planner"])
    graph.add_edge("file_description", "planner")
    graph.add_conditional_edges(
        "planner", route_after_planner, ["make_task", "human", "document", "conclude"]
    )
    graph.add_edge("make_task", "planner")
    graph.add_edge("human", "planner")
    graph.add_edge("document", END)
    graph.add_edge("conclude", END)

    return graph.compile(checkpointer=checkpointer)


graph = build_graph()
