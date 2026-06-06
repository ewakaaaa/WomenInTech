"""Estimate LLM call costs from token usage (``src.llm.Usage``).

Prices per 1M tokens (USD), as of June 2026 — update per
https://platform.openai.com/docs/pricing. Local models (Ollama) = 0.

    from src.llm import track_usage
    from src.cost import estimate_cost, cost_summary

    with track_usage() as u:
        evaluate(appeal)
    print(cost_summary(u, "gpt-5.4-mini"))
"""

from __future__ import annotations

from src.llm import Usage

# model -> (input price, output price) per 1M tokens [USD]
PRICES: dict[str, tuple[float, float]] = {
    "gpt-5.5": (5.00, 30.00),
    "gpt-5.4": (2.50, 15.00),  # closest equivalent to "full GPT-5" (as in DoGeDo)
    "gpt-5.4-mini": (0.75, 4.50),
    "gpt-5.4-nano": (0.20, 1.25),
}


def price_per_million(model: str) -> tuple[float, float]:
    """Prices (input, output) per 1M tokens; (0, 0) for unknown/local models."""
    return PRICES.get(model, (0.0, 0.0))


def estimate_cost(usage: Usage, model: str) -> float:
    """Cost in USD for the given token usage and model."""
    price_in, price_out = price_per_million(model)
    return usage.prompt_tokens / 1e6 * price_in + usage.completion_tokens / 1e6 * price_out


def cost_per_call(usage: Usage, model: str) -> float:
    """Average cost of a single LLM call in USD."""
    return estimate_cost(usage, model) / usage.calls if usage.calls else 0.0


def cost_summary(usage: Usage, model: str) -> str:
    """Human-readable usage summary: tokens, cost and time."""
    total = estimate_cost(usage, model)
    czas = f"{usage.seconds:.1f}s (≈{usage.seconds_per_call:.1f}s/wyw.)"
    if model not in PRICES:
        return (
            f"{model}: {usage.calls} wywołań, {usage.total_tokens:,} tok, {czas} "
            f"(brak cennika — koszt $0.00)"
        )
    return (
        f"{model}: {usage.calls} wywołań, "
        f"{usage.prompt_tokens:,} wej + {usage.completion_tokens:,} wyj tok "
        f"= ${total:.4f} (≈ ${cost_per_call(usage, model):.5f}/wyw.) | {czas}"
    )
