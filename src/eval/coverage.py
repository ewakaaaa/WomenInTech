"""Coverage evaluation against ``data/eval.json``.

For each required issue in the key, the LLM judge decides whether the appeal
actually addresses it. The shared yardstick across all approaches: how many of
the required issues did the generated appeal cover.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from src.llm import call_llm

# Evaluation key resolved from the repo root so evaluation works regardless of
# the current directory (e.g. from a notebook in notebooks/).
_DEFAULT_EVAL_PATH = Path(__file__).resolve().parents[2] / "data" / "eval.json"

JUDGE_SYSTEM_PROMPT = (
    "Jesteś egzaminatorem na egzaminie radcowskim. Oceniasz, czy przygotowana "
    "apelacja porusza konkretne zagadnienie wymagane w kluczu odpowiedzi. Bądź "
    "rygorystyczny: zagadnienie uznaj za poruszone tylko wtedy, gdy apelacja "
    "faktycznie podnosi dany zarzut lub wniosek wraz z istotą argumentacji, a nie "
    "jedynie wspomina temat."
)


class IssueVerdict(BaseModel):
    """LLM judge verdict for a single issue (reasoning first, then the verdict)."""

    reasoning: str = Field(..., description="Krótkie uzasadnienie oceny")
    covered: bool = Field(..., description="Czy apelacja porusza to zagadnienie")


class CoverageResult(BaseModel):
    """Aggregated coverage result for one appeal."""

    total: int = Field(..., description="Liczba zagadnień w kluczu")
    covered: int = Field(..., description="Liczba poruszonych zagadnień")
    score: float = Field(..., description="covered / total (0.0–1.0)")
    results: list[IssueVerdict] = Field(
        ..., description="Werdykt per zagadnienie (w kolejności klucza)"
    )


def load_eval(path: str | Path = _DEFAULT_EVAL_PATH) -> list[str]:
    """Load the list of required issues from the evaluation key."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _judge_issue(
    appeal_text: str, issue: str, model: str | None = None
) -> IssueVerdict:
    """Ask the LLM whether the appeal covers a single required issue."""
    messages = [
        {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"ZAGADNIENIE (klucz odpowiedzi):\n{issue}\n\n"
                f"APELACJA DO OCENY:\n{appeal_text}"
            ),
        },
    ]
    return call_llm(messages, response_model=IssueVerdict, model=model)


def evaluate(
    appeal_text: str,
    eval_path: str | Path = _DEFAULT_EVAL_PATH,
    model: str | None = None,
    print_results: bool = False,
) -> CoverageResult:
    """Evaluate an appeal against every issue in the evaluation key.

    When ``print_results=True`` (handy in a notebook / during a demo) it prints
    the verdict for each issue **as it goes**, as the judge evaluates them.
    """
    issues = load_eval(eval_path)
    results: list[IssueVerdict] = []
    for i, issue in enumerate(issues, 1):
        verdict = _judge_issue(appeal_text, issue, model=model)
        results.append(verdict)
        if print_results:
            mark = "✅" if verdict.covered else "❌"
            print(f"[{i}/{len(issues)}] {mark} {issue}")
            print(f"     → {verdict.reasoning}\n", flush=True)

    covered = sum(r.covered for r in results)
    total = len(results)
    score = covered / total if total else 0.0
    if print_results:
        print(f"Pokrycie: {covered}/{total} = {score:.0%}")
    return CoverageResult(total=total, covered=covered, score=score, results=results)


def evaluate_file(
    path: str | Path,
    eval_path: str | Path = _DEFAULT_EVAL_PATH,
    model: str | None = None,
) -> CoverageResult:
    """Evaluate an appeal stored in a text file."""
    return evaluate(
        Path(path).read_text(encoding="utf-8"), eval_path=eval_path, model=model
    )
