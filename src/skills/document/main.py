"""Skill: generate_document.

Write the final legal document in one shot, based on the chosen strategy and the
gathered analysis.
"""

from __future__ import annotations

from src.llm import call_llm
from src.skills.document.prompts import SYSTEM_PROMPT, USER_PROMPT
from src.skills.document.schemas import GeneratedDocument
from src.skills.make_task.schemas import TaskOutput
from src.skills.strategy.schemas import Strategy


def _format_analysis(task_outputs: list[TaskOutput]) -> str:
    return "\n\n".join(f"### {t.action}\n{t.output}" for t in task_outputs)


def generate_document(
    goal: str,
    strategy: Strategy,
    task_outputs: list[TaskOutput],
    model: str | None = None,
) -> GeneratedDocument:
    """Produce the final document from strategy and analysis."""
    return call_llm(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    general_goal=goal,
                    strategy=strategy.best_strategy,
                    analysis=_format_analysis(task_outputs),
                ),
            },
        ],
        response_model=GeneratedDocument,
        model=model,
    )
