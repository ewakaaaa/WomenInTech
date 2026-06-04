"""Loading case files from PDF into text."""

from __future__ import annotations

from pathlib import Path

import pdfplumber
from pydantic import BaseModel, Field


class Document(BaseModel):
    """A single document from the case files."""
    filename: str = Field(..., description="Source file name")
    text: str = Field(..., description="Extracted document text")


def load_pdf(path: str | Path) -> Document:
    """Load a single PDF file and return a document with its text."""
    path = Path(path)
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return Document(
        filename=path.name,
        text="\n\n".join(pages).strip(),
    )
