"""Walidacja apelacji z linii poleceń (zamiast notebooka).

Dla danej apelacji liczy i wypisuje **pokrycie** (`coverage` — czy porusza
wymagane zagadnienia) wraz z kosztem. Używane w blokach `__main__` podejść
(np. `agent_linear.pipeline`), żeby iterować nad jakością bez klikania notebooka.
"""

from __future__ import annotations

import os

from src.cost import cost_summary
from src.eval.coverage import CoverageResult, evaluate
from src.llm import track_usage


def evaluate_appeal(appeal_text: str, model: str | None = None) -> CoverageResult:
    """Oceń pokrycie apelacji (na bieżąco) i wypisz wynik + koszt."""
    model_name = model or os.environ.get("LLM_MODEL", "?")

    print("\n=== POKRYCIE (czy porusza wymagane zagadnienia) ===")
    with track_usage() as usage:
        cov = evaluate(appeal_text, model=model, print_results=True)
    print(f"POKRYCIE: {cov.covered}/{cov.total} = {cov.score:.0%}")
    print(f"  koszt: {cost_summary(usage, model_name)}")
    return cov
