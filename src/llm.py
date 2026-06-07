"""Single entry point for calling the LLM.

Uses the `instructor` library, which forces a structured response matching a
Pydantic model. The client is OpenAI-compatible, so by changing `base_url`/
`api_key` in the `.env` file you can plug in any backend:

- OpenAI          -> https://api.openai.com/v1 (model: gpt-5.4)
- workshop proxy  -> any OpenAI-compatible endpoint

Configured via environment variables (see `.env.example`):
    LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
"""

from __future__ import annotations

import contextvars
import os
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TypeVar

import instructor
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

T = TypeVar("T", bound=BaseModel)

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

# Newer OpenAI models (gpt-5.x) require `max_completion_tokens` instead of
# `max_tokens`; Ollama and some proxies still use `max_tokens`.
_MAX_TOKENS_PARAM = (
    "max_completion_tokens" if "openai.com" in _BASE_URL else "max_tokens"
)

client = instructor.patch(
    OpenAI(
        base_url=_BASE_URL,
        # Ollama doesn't require a key — any placeholder works.
        api_key=os.getenv("LLM_API_KEY", "not-needed"),
    ),
    mode=instructor.Mode.MD_JSON,
)


# ── Token usage tracking (for cost accounting) ──────────────────────────


@dataclass
class Usage:
    """Accumulated usage (tokens + time) for a series of call_llm calls."""

    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    seconds: float = 0.0  # total LLM call time (wall-clock)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def seconds_per_call(self) -> float:
        return self.seconds / self.calls if self.calls else 0.0


_usage_var: contextvars.ContextVar = contextvars.ContextVar("llm_usage", default=None)
# The langgraph agent runs calls in parallel (threads), all adding to the same
# Usage counter — the lock guards increments against a race condition.
_usage_lock = threading.Lock()


@contextmanager
def track_usage():
    """Collect token usage of ``call_llm`` calls made within this block.

    with track_usage() as u:
        evaluate(appeal)
    print(u.calls, u.total_tokens)
    """
    usage = Usage()
    token = _usage_var.set(usage)
    try:
        yield usage
    finally:
        _usage_var.reset(token)


def _record_usage(
    result, messages: list[dict], model: str, seconds: float = 0.0
) -> None:
    """Add usage from a single call to the active counter (if any).

    First we try the real numbers from the API response (`_raw_response.usage`);
    if absent — we estimate with tiktoken (lazy import, since src.tokens imports
    from this module).
    """
    usage = _usage_var.get()
    if usage is None:
        return

    raw = getattr(result, "_raw_response", None)
    api_usage = getattr(raw, "usage", None)
    if api_usage is not None:
        prompt_tokens = getattr(api_usage, "prompt_tokens", 0) or 0
        completion_tokens = getattr(api_usage, "completion_tokens", 0) or 0
    else:
        from src.tokens import count_messages_tokens, count_tokens

        prompt_tokens = count_messages_tokens(messages, model)
        completion_tokens = count_tokens(result.model_dump_json(), model)

    with _usage_lock:
        usage.calls += 1
        usage.prompt_tokens += prompt_tokens
        usage.completion_tokens += completion_tokens
        usage.seconds += seconds


def call_llm(
    messages: list[dict],
    response_model: type[T],
    model: str | None = None,
    temperature: float = 0.0,
    max_tokens: int | None = None,
) -> T:
    """Call the model and return a response validated against `response_model`.

    Args:
        messages: list of messages in OpenAI format (role/content).
        response_model: Pydantic class the response must match.
        model: model name; defaults to LLM_MODEL.
        temperature: defaults to 0.0 for reproducibility.
        max_tokens: cap on output tokens; None lets the provider decide. Set it
            higher for long outputs (e.g. the final document) to avoid truncation.
    """
    kwargs = {}
    if max_tokens is not None:
        kwargs[_MAX_TOKENS_PARAM] = max_tokens
    t0 = time.perf_counter()
    result = client.chat.completions.create(
        model=model or DEFAULT_MODEL,
        messages=messages,
        response_model=response_model,
        temperature=temperature,
        **kwargs,
    )
    _record_usage(result, messages, model or DEFAULT_MODEL, time.perf_counter() - t0)
    return result


if __name__ == "__main__":
    # Quick smoke test — requires a configured .env.
    class Capital(BaseModel):
        country: str
        capital: str

    result = call_llm(
        messages=[{"role": "user", "content": "What is the capital of Poland?"}],
        response_model=Capital,
    )
    print(result)
