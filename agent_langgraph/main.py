"""LangGraph agent — runner (same skills as the linear agent, but steps run in parallel).

The logic lives in the graph (``agent_langgraph/graph.py``): the same skills
(``src/skills/*``) as in ``agent_linear``, except that instead of ``for`` loops the
file descriptions and step executions are broadcast via ``Send`` and run **concurrently**
(each ``call_llm`` is I/O-bound, so threads yield a real time saving).

    uv run python -m agent_langgraph.main
"""

from __future__ import annotations

from agent_langgraph.graph import graph

GOAL = "Wygeneruj apelację z perspektywy obrony"


def run(goal: str = GOAL) -> str:
    """Run the graph and return the appeal text (the graph loads the case files in the ``load`` node)."""
    result = graph.invoke({"goal": goal})
    return result["document"]


if __name__ == "__main__":
    # Generation only from the CLI (model from .env, e.g. gpt-5.4) — WITHOUT evaluation.
    # Coverage and quality match agent_linear (same logic), so here we only care
    # about TIME: wall-clock with parallel fan-out vs the sequential linear agent.
    #   uv run python -m agent_langgraph.main
    import os
    import time

    from src.cost import cost_summary
    from src.llm import track_usage
    from src.output import save_appeal, tee_output

    # tee_output: all generation prints also go to the log file.
    with tee_output("agent_langgraph") as log_path:
        print("=== GENERACJA (agent LangGraph, kroki równolegle) ===")
        with track_usage() as gen_usage:
            wall_t0 = time.perf_counter()
            appeal = run()
            wall_seconds = time.perf_counter() - wall_t0

        saved = save_appeal(appeal, "agent_langgraph")
        print(f"\nZapisano apelację: {saved} ({len(appeal):,} znaków)")
        print(
            f"KOSZT METODY (sama generacja): {cost_summary(gen_usage, os.environ.get('LLM_MODEL', '?'))}"
        )
        # With parallelism the real (wall-clock) time is shorter than the sum of LLM
        # call times — that is the gain from the Send fan-out (vs the loop in agent_linear).
        print(f"Czas metody (wall-clock, równolegle): {wall_seconds:.1f}s")
        print(
            f"  suma czasów wywołań LLM: {gen_usage.seconds:.1f}s ({gen_usage.calls} wyw., ≈{gen_usage.seconds_per_call:.1f}s/wyw.)"
        )
        if wall_seconds > 0:
            print(
                f"  przyspieszenie z równoległości: ≈{gen_usage.seconds / wall_seconds:.1f}×"
            )

    print(f"\nLog z przebiegu zapisany: {log_path}")
