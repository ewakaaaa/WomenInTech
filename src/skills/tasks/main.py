"""Skill: generate_tasks.

Plan the analysis steps needed to reach the goal. Each step names the few
documents it needs (by file name) — that selective sourcing is what keeps later
steps from drowning in the whole case file.
"""

from __future__ import annotations

from src.llm import call_llm
from src.skills.file_description.schemas import DescribedFile
from src.skills.tasks.prompts import SYSTEM_PROMPT, USER_PROMPT
from src.skills.tasks.schemas import Tasks


def _format_sources(files: list[DescribedFile]) -> str:
    return "\n".join(f"- {f.name}: {f.title} — {f.description}" for f in files)


def generate_tasks(
    goal: str, described_files: list[DescribedFile], model: str | None = None
) -> Tasks:
    """Produce the analysis plan from the goal and the described documents."""
    return call_llm(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    general_goal=goal, list_of_sources=_format_sources(described_files)
                ),
            },
        ],
        response_model=Tasks,
        model=model,
        max_tokens=16000,
    )
