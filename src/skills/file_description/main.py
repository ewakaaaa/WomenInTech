"""Skill: generate_file_description.

For a single document, produce a short, goal-oriented description of what it
contains. Pure function (input -> output) — easy to test and easy to wrap as a
graph node later.
"""

from __future__ import annotations

from src.llm import call_llm
from src.loader import Document
from src.skills.file_description.prompts import SYSTEM_PROMPT, USER_PROMPT
from src.skills.file_description.schemas import DescribedFile, FileDescription


def generate_file_description(
    document: Document, goal: str, model: str | None = None
) -> DescribedFile:
    """Describe one document in the context of the overall goal."""
    result = call_llm(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT.format(general_goal=goal)},
            {"role": "user", "content": USER_PROMPT.format(text=document.text)},
        ],
        response_model=FileDescription,
        model=model,
        max_tokens=2000,
    )
    return DescribedFile(name=document.filename, **result.model_dump())
