"""Walidacja apelacji z linii poleceń (zamiast notebooka).

Dla danej apelacji liczy i wypisuje **pokrycie** (`coverage` — czy porusza
wymagane zagadnienia) oraz **jakość/formę** (`quality` — ocena egzaminatora),
każde z kosztem i czasem. Używane w blokach `__main__` podejść (np.
`agent_linear.main`), żeby iterować nad jakością bez klikania notebooka.
"""

from __future__ import annotations

import os

from src.cost import cost_summary
from src.eval.coverage import CoverageResult, evaluate
from src.eval.quality import QUALITY_JUDGE_MODEL, QualityVerdict, evaluate_quality
from src.llm import track_usage


def evaluate_appeal(
    appeal_text: str, model: str | None = None
) -> tuple[CoverageResult, QualityVerdict]:
    """Oceń apelację: pokrycie + jakość, wypisz wyniki wraz z kosztem i czasem."""
    model_name = model or os.environ.get("LLM_MODEL", "?")

    # Uwaga: poniższe koszty/czasy dotyczą EWALUACJI i są podane osobno —
    # nie wliczają się do kosztu metody (sama generacja apelacji liczona wyżej).
    print("\n--- EWALUACJA (koszt osobno, NIE wlicza się do kosztu metody) ---")
    print("\n=== POKRYCIE (czy porusza wymagane zagadnienia) ===")
    with track_usage() as cov_usage:
        cov = evaluate(appeal_text, model=model, print_results=True)
    print(f"POKRYCIE: {cov.covered}/{cov.total} = {cov.score:.0%}")
    print(f"  koszt: {cost_summary(cov_usage, model_name)}")
    print(f"  czas:  {cov_usage.seconds:.1f}s (≈{cov_usage.seconds_per_call:.1f}s/wyw.)")

    # Jakość oceniamy MOCNYM sędzią (gpt-5.4) — niezależnie od modelu generacji.
    print("\n=== JAKOŚĆ / FORMA (ocena egzaminatora, skala 2–6) ===")
    with track_usage() as q_usage:
        q = evaluate_quality(appeal_text)
    print(q.reasoning)
    print(f"  wymogi formalne:            {q.wymogi_formalne}/6")
    print(f"  zastosowanie/interpretacja: {q.zastosowanie_i_interpretacja}/6")
    print(f"  poprawność rozwiązania:     {q.poprawnosc_rozwiazania}/6")
    print(f"  -- średnia:                 {q.srednia:.2f}/6")
    print(f"  koszt: {cost_summary(q_usage, QUALITY_JUDGE_MODEL)}")
    print(f"  czas:  {q_usage.seconds:.1f}s (≈{q_usage.seconds_per_call:.1f}s/wyw.)")

    return cov, q


if __name__ == "__main__":
    # Sama ewaluacja (bez generacji) na ostatniej zapisanej apelacji danego podejścia.
    # Log trafia do <podejście>/output/run_<znacznik>.log.
    #   uv run python -m src.eval.report baseline
    #   uv run python -m src.eval.report agent_linear
    import sys

    from src.output import load_latest_appeal, tee_output

    approach = sys.argv[1] if len(sys.argv) > 1 else "baseline"
    with tee_output(approach) as log_path:
        appeal = load_latest_appeal(approach)
        print(f"=== EWALUACJA (sama ocena, bez generacji): {approach} ===")
        print(f"Apelacja: {len(appeal):,} znaków")
        evaluate_appeal(appeal)
    print(f"\nLog z ewaluacji zapisany: {log_path}")
