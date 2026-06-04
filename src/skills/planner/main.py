"""Skill: plan_next (the planner — "brain of the operation").

Given the goal, what documents exist (their descriptions) and the analysis done so
far, decide the next step: analyze more, ask the human, write the document, or
conclude there are no grounds.
"""

from __future__ import annotations

from src.llm import call_llm
from src.skills.file_description.schemas import DescribedFile
from src.skills.make_task.schemas import TaskOutput
from src.skills.planner.prompts import SYSTEM_PROMPT, USER_PROMPT
from src.skills.planner.schemas import PlannerDecision


def _format_files(files: list[DescribedFile]) -> str:
    return "\n".join(f"- {f.name}: {f.title} — {f.description}" for f in files)


def _format_outputs(task_outputs: list[TaskOutput]) -> str:
    if not task_outputs:
        return "(jeszcze brak — nie wykonano żadnej analizy)"
    return "\n\n".join(f"### {t.action}\n{t.output}" for t in task_outputs)


def plan_next(
    goal: str,
    described_files: list[DescribedFile],
    task_outputs: list[TaskOutput],
    human_feedback: str | None = None,
    model: str | None = None,
) -> PlannerDecision:
    """Decide the next step in the analysis."""
    feedback = (
        f"Decyzja/uwaga od człowieka (radcy): {human_feedback}\n" if human_feedback else ""
    )
    return call_llm(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(general_goal=goal)},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    file_descriptions=_format_files(described_files),
                    task_outputs=_format_outputs(task_outputs),
                    human_feedback=feedback,
                ),
            },
        ],
        response_model=PlannerDecision,
        model=model,
        max_tokens=16000,
    )
