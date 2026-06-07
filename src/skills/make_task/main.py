"""Skill: make_task.

Carry out a single analysis step using only the source texts selected for it.
The caller is responsible for gathering ``sources_text`` (the few documents the
task asked for) — this keeps the skill pure.
"""

from __future__ import annotations

from src.llm import call_llm
from src.skills.make_task.prompts import SYSTEM_PROMPT, USER_PROMPT
from src.skills.make_task.schemas import TaskAnalysis, TaskOutput
from src.skills.tasks.schemas import Task


def make_task(
    goal: str,
    task: Task,
    sources_text: str,
    model: str | None = None,
    temperature: float = 0.0,
) -> TaskOutput:
    """Execute one analysis step over its selected sources."""
    result = call_llm(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(general_goal=goal)},
            {
                "role": "user",
                "content": USER_PROMPT.format(
                    action_step=task.action,
                    context=task.reasoning,
                    sources=sources_text,
                ),
            },
        ],
        response_model=TaskAnalysis,
        model=model,
        temperature=temperature,
        max_tokens=16000,
    )
    return TaskOutput(action=task.action, output=result.output)
