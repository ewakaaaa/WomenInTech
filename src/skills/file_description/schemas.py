"""Schemas for the file_description skill."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FileDescription(BaseModel):
    """LLM output — a description of a single document."""

    title: str = Field(..., description="Tytuł dokumentu")
    description: str = Field(
        ...,
        description="Kilka zdań podsumowania, które wskażą, jak ważny jest dokument dla realizacji celu.",
    )


class DescribedFile(FileDescription):
    """A described document together with its source file name."""

    name: str = Field(..., description="Nazwa pliku źródłowego")
