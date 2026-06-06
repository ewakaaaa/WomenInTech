"""Baseline (version 0) — the naive approach.

Dump ALL case files into the model with a single prompt: "you are a lawyer,
write an appeal". Running this module generates the appeal and saves it to a
text file, which the evaluator (``baseline/eval.py``) then reads.

    uv run python -m baseline.main
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from baseline.prompts import SYSTEM_PROMPT
from src.llm import call_llm
from src.loader import Document, load_all
from src.tokens import count_tokens


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
    # Generation + evaluation (coverage + quality) from the CLI (model from .env, e.g. gpt-5.4):
    #   uv run python -m baseline.main
    import os

    from src.cost import cost_summary
    from src.eval.report import evaluate_appeal
    from src.llm import track_usage
    from src.output import save_appeal, tee_output

    # tee_output: all prints (generation + checks from evaluate) also go to the log file.
    with tee_output("baseline") as log_path:
        docs = load_all()
        prompt_tokens = count_tokens(SYSTEM_PROMPT + "\n\n" + build_context(docs))
        print(f"Dokumentów: {len(docs)} | prompt: ~{prompt_tokens:,} tokenów\n")

        print("=== GENERACJA (baseline) ===")
        with track_usage() as gen_usage:
            appeal = generate_appeal(docs).tekst

        saved = save_appeal(appeal, "baseline")
        print(f"Zapisano apelację: {saved} ({len(appeal):,} znaków)")
        print(f"KOSZT METODY (sama generacja, bez ewaluacji): {cost_summary(gen_usage, os.environ.get('LLM_MODEL', '?'))}")
        print(f"Czas metody:  {gen_usage.seconds:.1f}s ({gen_usage.calls} wyw., ≈{gen_usage.seconds_per_call:.1f}s/wyw.)")

        evaluate_appeal(appeal)

    print(f"\nLog z przebiegu zapisany: {log_path}")
