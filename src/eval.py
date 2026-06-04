"""Evaluation against ``data/eval.json`` — the list of issues an appeal must cover.

Used by every approach (baseline and the agent) so results are comparable on the
same yardstick: how many of the required issues did the generated appeal actually
address. Uses the LLM as a judge — each issue is graded independently.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from src.llm import call_llm

JUDGE_SYSTEM_PROMPT = (
    "Jesteś egzaminatorem na egzaminie radcowskim. Oceniasz, czy przygotowana "
    "apelacja porusza konkretne zagadnienie wymagane w kluczu odpowiedzi. Bądź "
    "rygorystyczny: zagadnienie uznaj za poruszone tylko wtedy, gdy apelacja "
    "faktycznie podnosi dany zarzut lub wniosek wraz z istotą argumentacji, a nie "
    "jedynie wspomina temat."
)


class IssueVerdict(BaseModel):
    """LLM judge verdict for a single issue."""

    covered: bool = Field(..., description="Czy apelacja porusza to zagadnienie")
    reasoning: str = Field(..., description="Krótkie uzasadnienie oceny")


class IssueResult(IssueVerdict):
    """Verdict together with the issue it refers to."""

    issue: str = Field(..., description="Treść zagadnienia z klucza")


class EvalResult(BaseModel):
    """Aggregated evaluation result for one appeal."""

    total: int = Field(..., description="Liczba zagadnień w kluczu")
    covered: int = Field(..., description="Liczba poruszonych zagadnień")
    score: float = Field(..., description="covered / total (0.0–1.0)")
    results: list[IssueResult] = Field(..., description="Wynik per zagadnienie")


def load_eval(path: str | Path = "data/eval.json") -> list[str]:
    """Load the list of required issues from the evaluation key."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _judge_issue(appeal_text: str, issue: str, model: str | None = None) -> IssueVerdict:
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
    eval_path: str | Path = "data/eval.json",
    model: str | None = None,
) -> EvalResult:
    """Evaluate an appeal against every issue in the evaluation key."""
    issues = load_eval(eval_path)
    results = [
        IssueResult(issue=issue, **_judge_issue(appeal_text, issue, model=model).model_dump())
        for issue in issues
    ]
    covered = sum(r.covered for r in results)
    total = len(results)
    return EvalResult(
        total=total,
        covered=covered,
        score=covered / total if total else 0.0,
        results=results,
    )
