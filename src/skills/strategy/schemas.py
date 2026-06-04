"""Schemas for the strategy skill."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Strategy(BaseModel):
    """The chosen approach for reaching the goal."""

    definition_of_success: str = Field(
        ..., description="Jak należy rozumieć sukces w kontekście głównego zadania."
    )
    strategies: str = Field(
        ...,
        description="Rozumowanie na temat kilku możliwych strategii/podejść realizacji celu i osiągnięcia sukcesu",
    )
    best_strategy: str = Field(..., description="Opis najlepszej strategii")
