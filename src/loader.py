"""Wczytywanie akt sprawy z plików PDF do tekstu."""

from __future__ import annotations

from pathlib import Path

import pdfplumber
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Pojedynczy dokument z akt sprawy."""

    filename: str = Field(..., description="Nazwa pliku źródłowego")
    text: str = Field(..., description="Wyekstrahowany tekst dokumentu")
    n_pages: int = Field(..., description="Liczba stron w dokumencie")

    @property
    def n_chars(self) -> int:
        return len(self.text)


def load_pdf(path: str | Path) -> Document:
    """Wczytuje pojedynczy plik PDF i zwraca dokument z tekstem."""
    path = Path(path)
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return Document(
        filename=path.name,
        text="\n\n".join(pages).strip(),
        n_pages=len(pages),
    )


def load_documents(input_dir: str | Path = "data/input") -> list[Document]:
    """Wczytuje wszystkie pliki PDF z katalogu, posortowane wg nazwy."""
    input_dir = Path(input_dir)
    pdf_paths = sorted(input_dir.glob("*.pdf"))
    if not pdf_paths:
        raise FileNotFoundError(f"Brak plików PDF w katalogu: {input_dir}")
    return [load_pdf(p) for p in pdf_paths]


if __name__ == "__main__":
    docs = load_documents()
    print(f"Wczytano {len(docs)} dokument(ów):\n")
    for doc in docs:
        print(f"  • {doc.filename}  —  {doc.n_pages} str.,  {doc.n_chars} znaków")
