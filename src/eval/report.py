"""Appeal validation from the command line (instead of a notebook).

For a given appeal it computes and prints **coverage** (`coverage` — whether it
addresses the required issues) and **quality/form** (`quality` — the examiner's
grade), each with its cost and time. Used in the `__main__` blocks of the
approaches (e.g. `agent_linear.main`) to iterate on quality without clicking
through a notebook.
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
    """Evaluate an appeal: coverage + quality, printing results with cost and time."""
    model_name = model or os.environ.get("LLM_MODEL", "?")

    # Note: the costs/times below pertain to EVALUATION and are reported
    # separately — they don't count toward the method's cost (appeal generation
    # itself is measured above).
    print("\n--- EWALUACJA (koszt osobno, NIE wlicza się do kosztu metody) ---")
    print("\n=== POKRYCIE (czy porusza wymagane zagadnienia) ===")
    with track_usage() as cov_usage:
        cov = evaluate(appeal_text, model=model, print_results=True)
    print(f"POKRYCIE: {cov.covered}/{cov.total} = {cov.score:.0%}")
    print(f"  koszt: {cost_summary(cov_usage, model_name)}")
    print(
        f"  czas:  {cov_usage.seconds:.1f}s (≈{cov_usage.seconds_per_call:.1f}s/wyw.)"
    )

    # Quality is judged by a STRONG judge (gpt-5.4) — independent of the generation model.
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
    # Evaluation only (no generation) on the latest saved appeal for the given approach.
    # The log goes to <approach>/output/run_<timestamp>.log.
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
