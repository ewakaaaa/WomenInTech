"""Schemas for the make_task skill."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TaskAnalysis(BaseModel):
    """LLM output — the result of carrying out one analysis step."""

    output: str = Field(..., description="Wynik wykonania kroku analizy")


class TaskOutput(TaskAnalysis):
    """The analysis result together with the action it answers."""

    action: str = Field(..., description="Akcja, której dotyczy wynik")
