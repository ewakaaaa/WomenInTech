"""Schemas for the document skill."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GeneratedDocument(BaseModel):
    """The final legal document."""

    tekst: str = Field(..., description="Pełna treść dokumentu prawniczego")
