"""Baseline (version 0) — the naive approach.

Dump ALL case files into the model with a single prompt: "you are a lawyer,
write an appeal". Running this module generates the appeal and saves it to a
text file, which the evaluator (``baseline/eval.py``) then reads.

    uv run python -m baseline.main
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from baseline.prompts import SYSTEM_PROMPT
from src.llm import call_llm
from src.loader import Document, load_all
from src.tokens import count_tokens

OUTPUT_PATH = "baseline/apelacja_baseline.txt"


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


if __name__ == "__main__":
    docs = load_all()
    context = build_context(docs)
    prompt_tokens = count_tokens(SYSTEM_PROMPT + "\n\n" + context)

    print(f"Documents loaded: {len(docs)}")
    print(f"Context characters: {len(context):,}")
    print(f"Prompt tokens (input): ~{prompt_tokens:,}")

    print("Generating appeal...")
    appeal = generate_appeal(docs)

    output = Path(OUTPUT_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(appeal.tekst, encoding="utf-8")
    print(f"Saved appeal to {OUTPUT_PATH} ({len(appeal.tekst):,} chars)")
