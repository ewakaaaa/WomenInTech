"""Run the LangGraph agent.

    uv run python -m langgraph_agent.main
"""

from pathlib import Path

from langgraph_agent.graph import graph
from src.loader import load_all

GOAL = "Wygeneruj apelację z perspektywy obrony"
OUTPUT_PATH = "langgraph_agent/apelacja.txt"

if __name__ == "__main__":
    result = graph.invoke({"goal": GOAL, "documents": load_all()})

    output = Path(OUTPUT_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result["document"], encoding="utf-8")
    print(f"Saved to {OUTPUT_PATH} ({len(result['document']):,} chars)")
