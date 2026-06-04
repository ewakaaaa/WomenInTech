"""Run the baseline and report token usage.

    uv run python -m baseline
"""

from baseline.baseline import build_context, load_all
from baseline.prompts import SYSTEM_PROMPT
from src.tokens import count_tokens

docs = load_all()
context = build_context(docs)
prompt_tokens = count_tokens(SYSTEM_PROMPT + "\n\n" + context)

print(f"Documents loaded: {len(docs)}")
print(f"Context characters: {len(context):,}")
print(f"Prompt tokens (input): ~{prompt_tokens:,}")
