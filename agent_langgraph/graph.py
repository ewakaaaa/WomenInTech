"""LangGraph wiring.

The nodes are thin wrappers around the existing skills (``src/skills/*``) — the
skill logic is unchanged. Fan-out (one branch per file, one per task) is done
with the ``Send`` API; results are merged back via the ``operator.add`` reducers
on ``files_out`` / ``tasks_out``.
"""

from __future__ import annotations

from langgraph.constants import END, START, Send
from langgraph.graph import StateGraph

from agent_langgraph.state import DescribeFileIn, OverallState, RunTaskIn
from src.descriptions import descriptions_cached, load_descriptions, save_descriptions
from src.skills.document.main import generate_document
from src.skills.file_description.main import generate_file_description
from src.skills.make_task.main import make_task
from src.skills.strategy.main import generate_strategy
from src.skills.tasks.main import generate_tasks
from src.loader import load_all
from src.sources import prepare_input_texts


# --- nodes (wrap the skills, return state updates) ---


def load_node(state: OverallState) -> dict:
    """Entry node: load the case files; attach cached descriptions if they exist."""
    cached = load_descriptions() if descriptions_cached() else []
    return {"documents": load_all(), "files_out": cached}


def file_description_node(payload: DescribeFileIn) -> dict:
    described = generate_file_description(payload["document"], payload["goal"])
    return {"files_out": [described]}


def tasks_node(state: OverallState) -> dict:
    # First run (empty cache) — save the computed descriptions for reuse.
    if not descriptions_cached():
        save_descriptions(state["files_out"])
    tasks = generate_tasks(state["goal"], state["files_out"])
    return {"tasks": tasks.thoughts}


def make_task_node(payload: RunTaskIn) -> dict:
    output = make_task(payload["goal"], payload["task"], payload["sources_text"])
    return {"tasks_out": [output]}


def strategy_node(state: OverallState) -> dict:
    return {"strategy": generate_strategy(state["goal"], state["tasks_out"])}


def document_node(state: OverallState) -> dict:
    document = generate_document(state["goal"], state["strategy"], state["tasks_out"])
    return {"document": document.tekst}


# --- routing (fan-out with Send) ---


def fan_out_files(state: OverallState):
    # Cache hit — descriptions already in files_out, skip the fan-out and recomputation.
    if state.get("files_out"):
        return "generate_tasks"
    return [
        Send("generate_file_description", DescribeFileIn(goal=state["goal"], document=doc))
        for doc in state["documents"]
    ]


def fan_out_tasks(state: OverallState) -> list[Send]:
    return [
        Send(
            "make_task",
            RunTaskIn(
                goal=state["goal"],
                task=task,
                sources_text=prepare_input_texts(state["documents"], task.input),
            ),
        )
        for task in state["tasks"]
    ]


def build_graph():
    graph = StateGraph(OverallState)

    graph.add_node("load", load_node)
    graph.add_node("generate_file_description", file_description_node)
    graph.add_node("generate_tasks", tasks_node)
    graph.add_node("make_task", make_task_node)
    graph.add_node("generate_strategy", strategy_node)
    graph.add_node("generate_document", document_node)

    graph.add_edge(START, "load")
    graph.add_conditional_edges(
        "load", fan_out_files, ["generate_file_description", "generate_tasks"]
    )
    graph.add_edge("generate_file_description", "generate_tasks")
    graph.add_conditional_edges("generate_tasks", fan_out_tasks, ["make_task"])
    graph.add_edge("make_task", "generate_strategy")
    graph.add_edge("generate_strategy", "generate_document")
    graph.add_edge("generate_document", END)

    return graph.compile()


graph = build_graph()
