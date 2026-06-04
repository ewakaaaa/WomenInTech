"""Schemas for the planner skill."""

from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field

from src.skills.tasks.schemas import Task


class PlannerDecision(BaseModel):
    """The planner's decision on what to do next."""

    reasoning: str = Field(..., description="Tok myślowy: co już wiemy i czego brakuje")
    action: Literal["analyze", "ask_human", "write", "no_grounds"] = Field(
        ...,
        description=(
            "Następny krok: 'analyze' = dorzuć zadania do analizy; "
            "'ask_human' = poproś człowieka o potwierdzenie kierunku; "
            "'write' = mamy dość, napisz apelację; "
            "'no_grounds' = brak podstaw do apelacji"
        ),
    )
    new_tasks: List[Task] = Field(
        default_factory=list,
        description="Nowe zadania do analizy (gdy action == 'analyze')",
    )
    summary_for_human: str = Field(
        default="",
        description="Podsumowanie i pytanie do człowieka (gdy action == 'ask_human')",
    )
    conclusion: str = Field(
        default="",
        description="Uzasadnienie decyzji o pisaniu lub braku podstaw (gdy 'write'/'no_grounds')",
    )
