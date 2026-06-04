"""Token counting helpers.

Reusable across the project — useful for measuring prompt size, deciding when
context is too large, and reporting cost.
"""

from __future__ import annotations

import tiktoken

from src.llm import DEFAULT_MODEL


def _get_encoding(model: str) -> tiktoken.Encoding:
    """Return the tiktoken encoding for a model, with a safe fallback."""
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback for models tiktoken doesn't know (e.g. local/Ollama).
        return tiktoken.get_encoding("o200k_base")


def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """Count tokens of a text for the given model (tiktoken estimate)."""
    return len(_get_encoding(model).encode(text))


def count_messages_tokens(messages: list[dict], model: str = DEFAULT_MODEL) -> int:
    """Approximate token count for a list of chat messages (role + content)."""
    encoding = _get_encoding(model)
    total = 0
    for message in messages:
        total += len(encoding.encode(message.get("content", "")))
        total += len(encoding.encode(message.get("role", "")))
    return total
