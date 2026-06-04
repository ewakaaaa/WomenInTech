"""Run the planner agent (non-linear, with human-in-the-loop).

The planner loops until it decides to write (or that there are no grounds). When it
asks the human, the graph pauses (``interrupt``) and waits for your decision in the
terminal — you play the radca confirming the direction.

    uv run python -m agent_planner.main
"""

from pathlib import Path

from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from agent_planner.graph import build_graph

GOAL = (
    "Oceń, czy w sprawie zasadna jest apelacja od wyroku sądu pierwszej instancji, "
    "a jeśli tak — sporządź apelację z perspektywy obrony."
)
OUTPUT_PATH = "agent_planner/apelacja.txt"

if __name__ == "__main__":
    graph = build_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "warsztat"}}

    state = graph.invoke({"goal": GOAL}, config=config)

    # Human-in-the-loop: wznawiaj, dopóki planer pauzuje na pytanie.
    while "__interrupt__" in state:
        question = state["__interrupt__"][0].value
        print("\n=== PLANER PYTA ===")
        print(question)
        answer = input("\nTwoja decyzja (radca): ")
        state = graph.invoke(Command(resume=answer), config=config)

    document = state.get("document", "")
    output = Path(OUTPUT_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(f"\nZapisano do {OUTPUT_PATH} ({len(document):,} znaków)")
