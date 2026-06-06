"""LangGraph agent — runner (te same skille co agent liniowy, ale kroki równolegle).

Logika jest w grafie (``agent_langgraph/graph.py``): te same umiejętności
(``src/skills/*``) co w ``agent_linear``, tylko zamiast pętli ``for`` opis plików
i wykonanie kroków są rozgłaszane przez ``Send`` i biegną **współbieżnie**
(każde ``call_llm`` jest I/O-bound, więc wątki dają realny zysk czasu).

    uv run python -m agent_langgraph.main
"""

from __future__ import annotations

from agent_langgraph.graph import graph

GOAL = "Wygeneruj apelację z perspektywy obrony"


def run(goal: str = GOAL) -> str:
    """Uruchom graf i zwróć treść apelacji (akta wczytuje sam graf w węźle ``load``)."""
    result = graph.invoke({"goal": goal})
    return result["document"]


if __name__ == "__main__":
    # Sama generacja z CLI (model z .env, np. gpt-5.4) — BEZ ewaluacji.
    # Pokrycie i jakość są jak u agent_linear (ta sama logika), więc tu interesuje
    # nas tylko CZAS: wall-clock przy równoległym fan-oucie vs sekwencyjny liner.
    #   uv run python -m agent_langgraph.main
    import os
    import time

    from src.cost import cost_summary
    from src.llm import track_usage
    from src.output import save_appeal, tee_output

    # tee_output: wszystkie printy generacji lecą też do pliku logu.
    with tee_output("agent_langgraph") as log_path:
        print("=== GENERACJA (agent LangGraph, kroki równolegle) ===")
        with track_usage() as gen_usage:
            wall_t0 = time.perf_counter()
            appeal = run()
            wall_seconds = time.perf_counter() - wall_t0

        saved = save_appeal(appeal, "agent_langgraph")
        print(f"\nZapisano apelację: {saved} ({len(appeal):,} znaków)")
        print(f"KOSZT METODY (sama generacja): {cost_summary(gen_usage, os.environ.get('LLM_MODEL', '?'))}")
        # Przy równoległości realny czas (wall-clock) jest krótszy niż suma czasów
        # wywołań LLM — to właśnie zysk z fan-outu przez Send (vs pętla w agent_linear).
        print(f"Czas metody (wall-clock, równolegle): {wall_seconds:.1f}s")
        print(f"  suma czasów wywołań LLM: {gen_usage.seconds:.1f}s ({gen_usage.calls} wyw., ≈{gen_usage.seconds_per_call:.1f}s/wyw.)")
        if wall_seconds > 0:
            print(f"  przyspieszenie z równoległości: ≈{gen_usage.seconds / wall_seconds:.1f}×")

    print(f"\nLog z przebiegu zapisany: {log_path}")
