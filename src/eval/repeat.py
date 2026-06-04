"""Powtarzalność wyniku — wygeneruj apelację N razy tym samym sposobem, oceń
każdą i policz statystyki pokrycia.

Pojedynczy przebieg LLM to za mało, żeby ocenić podejście: ten sam prompt przy
każdym uruchomieniu daje nieco inną apelację, więc i pokrycie się waha. Dopiero
średnia (i rozrzut) z kilku przebiegów mówi coś wiarygodnego.

    uv run python -m src.eval.repeat                              # baseline, 5 przebiegów
    uv run python -m src.eval.repeat --approach agent_linear --runs 3
    uv run python -m src.eval.repeat --runs 10 --model qwen2.5:14b
"""

from __future__ import annotations

import argparse
import itertools
import statistics
from functools import lru_cache

from src.eval.coverage import CoverageResult, evaluate

# Auto-odpowiedź dla planera (człowiek w pętli) przy automatycznych przebiegach.
PLANNER_AUTO_ANSWER = (
    "Tak, kierunek obrony jest słuszny — sporządź apelację z perspektywy obrońcy."
)
_run_counter = itertools.count(1)


@lru_cache(maxsize=1)
def _docs():
    """Wczytaj akta raz i trzymaj w cache — te same dla wszystkich przebiegów."""
    from src.loader import load_all

    return load_all()


def _gen_baseline(model: str | None) -> str:
    from baseline.main import generate_appeal

    return generate_appeal(_docs(), model=model).tekst


def _gen_linear(model: str | None) -> str:
    from agent_linear.pipeline import run

    return run(model=model).tekst


def _gen_planner(model: str | None) -> str:
    # Planner ma człowieka w pętli (interrupt) — przy automatycznych przebiegach
    # auto-odpowiadamy potwierdzeniem, aż graf dojdzie do napisania pisma.
    # Uwaga: planer korzysta z modelu z .env (LLM_MODEL) — flaga --model go nie zmienia.
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.types import Command

    from agent_planner.graph import build_graph
    from agent_planner.main import GOAL

    graph = build_graph(checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": f"repeat-{next(_run_counter)}"}}

    state = graph.invoke({"goal": GOAL}, config=config)
    while "__interrupt__" in state:
        state = graph.invoke(Command(resume=PLANNER_AUTO_ANSWER), config=config)
    return state.get("document", "")


GENERATORS = {
    "baseline": _gen_baseline,
    "agent_linear": _gen_linear,
    "agent_planner": _gen_planner,
}


def repeat(
    approach: str = "baseline",
    runs: int = 5,
    model: str | None = None,
    eval_path: str = "data/eval.json",
) -> list[CoverageResult]:
    """Wygeneruj `runs` apelacji sposobem `approach`, oceń każdą i podsumuj."""
    if approach not in GENERATORS:
        raise ValueError(
            f"nieznany sposób: {approach!r}; dostępne: {', '.join(GENERATORS)}"
        )
    generate = GENERATORS[approach]

    reports: list[CoverageResult] = []
    for i in range(1, runs + 1):
        print(f"\n[{approach}] przebieg {i}/{runs} — generuję apelację...")
        appeal_text = generate(model)
        cov = evaluate(appeal_text, eval_path=eval_path, model=model)
        reports.append(cov)
        print(f"  pokrycie: {cov.covered}/{cov.total} = {cov.score:.0%}")

    _summary(approach, reports)
    return reports


def _summary(approach: str, reports: list[CoverageResult]) -> None:
    """Wypisz tabelę przebiegów i statystyki zbiorcze."""
    scores = [r.score for r in reports]

    print(f"\n=== {approach}: {len(reports)} przebiegów ===")
    print(f"{'przebieg':>8} {'pokryte':>10} {'score':>7}")
    print("-" * 28)
    for i, r in enumerate(reports, 1):
        print(f"{i:>8} {f'{r.covered}/{r.total}':>10} {r.score:>6.0%}")

    print("-" * 28)
    print(f"{'średnia':>8} {'':>10} {statistics.mean(scores):>6.0%}")
    print(f"{'min':>8} {'':>10} {min(scores):>6.0%}")
    print(f"{'max':>8} {'':>10} {max(scores):>6.0%}")
    if len(scores) > 1:
        # odchylenie standardowe próbki — miara rozrzutu między przebiegami
        print(f"{'odch.std':>8} {'':>10} {statistics.stdev(scores):>6.1%}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--approach",
        default="baseline",
        choices=list(GENERATORS),
        help="sposób generowania apelacji (domyślnie: baseline)",
    )
    parser.add_argument(
        "--runs", type=int, default=5, help="liczba przebiegów (domyślnie: 5)"
    )
    parser.add_argument(
        "--model", default=None, help="nazwa modelu; domyślnie z .env (LLM_MODEL)"
    )
    args = parser.parse_args()
    repeat(approach=args.approach, runs=args.runs, model=args.model)


if __name__ == "__main__":
    main()
