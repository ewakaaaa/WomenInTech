"""Baseline (version 0) — the naive approach.

Dump ALL case files into the model with a single prompt: "you are a lawyer,
write an appeal". This is the workshop starting point — it shows why a plain
single-shot prompt is the baseline, and lets us measure how many tokens the
whole case eats at once.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from baseline.prompts import SYSTEM_PROMPT
from src.llm import call_llm
from src.loader import Document, load_pdf


def load_all(input_dir: str | Path = "data/input") -> list[Document]:
    """Load every PDF from the directory, sorted by filename."""
    paths = sorted(Path(input_dir).glob("*.pdf"))
    if not paths:
        raise FileNotFoundError(f"No PDF files found in: {input_dir}")
    return [load_pdf(p) for p in paths]


def build_context(docs: list[Document]) -> str:
    """Concatenate all documents into one context, labeled by file name."""
    return "\n\n".join(f"=== {d.filename} ===\n{d.text}" for d in docs)


class Appeal(BaseModel):
    """The generated appeal."""

    tekst: str = Field(..., description="Pełna treść apelacji")


def generate_appeal(docs: list[Document], model: str | None = None) -> Appeal:
    """Naive baseline: send the whole case in one prompt and get the appeal."""
    context = build_context(docs)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": context},
    ]
    return call_llm(messages, response_model=Appeal, model=model)
