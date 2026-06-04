"""Schemas for the tasks skill."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, conlist


class Task(BaseModel):
    """A single planned analysis step."""

    reasoning: str = Field(..., description="Tok myślowy asystenta")
    input: Optional[conlist(str, min_length=1, max_length=10)] = Field(
        ...,
        description="Lista dokumentów (nazwy plików), z których chce skorzystać przy realizacji tego kroku",
    )
    action: str = Field(
        ...,
        description="Podsumowanie przemyśleń asystenta - Akcja która należy wykonać",
    )


class Tasks(BaseModel):
    """The full analysis plan — a list of steps."""

    thoughts: List[Task] = Field(
        ...,
        description="Lista kroków myślowych i działań zaplanowanych przez asystenta.",
    )
