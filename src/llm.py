"""Single entry point for calling the LLM.

Uses the `instructor` library, which forces a structured response matching a
Pydantic model. The client is OpenAI-compatible, so by changing `base_url`/
`api_key` in the `.env` file you can plug in any backend:

- OpenAI          -> https://api.openai.com/v1
- local model     -> Ollama: http://localhost:11434/v1 (e.g. qwen2.5:14b)
- workshop proxy  -> https://llm-api.dataworkshop.eu

Configured via environment variables (see `.env.example`):
    LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
"""

from __future__ import annotations

import contextvars
import os
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

# Nowe modele OpenAI (gpt-5.x) wymagają `max_completion_tokens` zamiast
# `max_tokens`; Ollama i część proxy nadal używają `max_tokens`.
_MAX_TOKENS_PARAM = "max_completion_tokens" if "openai.com" in _BASE_URL else "max_tokens"

client = instructor.patch(
    OpenAI(
        base_url=_BASE_URL,
        # Ollama doesn't require a key — any placeholder works.
        api_key=os.getenv("LLM_API_KEY", "not-needed"),
    ),
    mode=instructor.Mode.MD_JSON,
)


# ── Pomiar zużycia tokenów (do liczenia kosztów) ──────────────────────────


@dataclass
class Usage:
    """Zliczone zużycie tokenów dla serii wywołań call_llm."""

    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


_usage_var: contextvars.ContextVar = contextvars.ContextVar("llm_usage", default=None)


@contextmanager
def track_usage():
    """Zbieraj zużycie tokenów wywołań ``call_llm`` wykonanych w tym bloku.

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


def _record_usage(result, messages: list[dict], model: str) -> None:
    """Dopisz zużycie z jednego wywołania do aktywnego licznika (jeśli jest).

    Najpierw próbujemy realnych liczb z odpowiedzi API (`_raw_response.usage`);
    gdy ich brak — szacujemy tiktokenem (import leniwy, bo src.tokens importuje
    z tego modułu).
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

    usage.calls += 1
    usage.prompt_tokens += prompt_tokens
    usage.completion_tokens += completion_tokens


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
    result = client.chat.completions.create(
        model=model or DEFAULT_MODEL,
        messages=messages,
        response_model=response_model,
        temperature=temperature,
        **kwargs,
    )
    _record_usage(result, messages, model or DEFAULT_MODEL)
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

