"""Loading case files from PDF into text."""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber
from pydantic import BaseModel, Field

# Powtarzający się nagłówek arkusza egzaminacyjnego — czysty szum w każdym pliku.
_EXAM_HEADER = re.compile(
    r"EGZAMIN\s+RADCOWSKI\s*[-–]\s*PRAWO\s+(CYWILNE|KARNE)", re.IGNORECASE
)

# Katalog z aktami liczony od korzenia repo (a nie od bieżącego katalogu), żeby
# `load_all()` działało niezależnie od tego, skąd uruchomiono kod (np. notebook
# w notebooks/).
_DEFAULT_INPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "input"


class Document(BaseModel):
    """A single document from the case files."""
    filename: str = Field(..., description="Source file name")
    text: str = Field(..., description="Extracted document text")


def clean_text(text: str) -> str:
    """Strip the repeated exam-sheet header from the extracted text."""
    return _EXAM_HEADER.sub("", text)


def load_pdf(path: str | Path) -> Document:
    """Load a single PDF file and return a document with its text."""
    path = Path(path)
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return Document(
        filename=path.name,
        text=clean_text("\n\n".join(pages)).strip(),
    )


def load_all(input_dir: str | Path = _DEFAULT_INPUT_DIR) -> list[Document]:
    """Load every PDF from a directory, sorted by filename."""
    paths = sorted(Path(input_dir).glob("*.pdf"))
    if not paths:
        raise FileNotFoundError(f"No PDF files found in: {input_dir}")
    return [load_pdf(p) for p in paths]
