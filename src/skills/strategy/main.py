"""Skill: generate_strategy.

From the gathered analysis, decide how to approach the goal: define success,
weigh possible strategies, and pick the best one.
"""

from __future__ import annotations

from src.llm import call_llm
from src.skills.make_task.schemas import TaskOutput
from src.skills.strategy.prompts import SYSTEM_PROMPT, USER_PROMPT
from src.skills.strategy.schemas import Strategy


def _format_outputs(task_outputs: list[TaskOutput]) -> str:
    return "\n\n".join(f"### {t.action}\n{t.output}" for t in task_outputs)


def generate_strategy(
    goal: str, task_outputs: list[TaskOutput], model: str | None = None
) -> Strategy:
    """Choose the best strategy based on the analysis results."""
    return call_llm(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(general_goal=goal)},
            {
                "role": "user",
                "content": USER_PROMPT.format(action_outputs=_format_outputs(task_outputs)),
            },
        ],
        response_model=Strategy,
        model=model,
        max_tokens=16000,
    )
