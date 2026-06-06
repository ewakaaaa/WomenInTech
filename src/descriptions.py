"""Document descriptions (file_description) with an on-disk cache.

Describing the case files takes one LLM call per document — expensive, and the
result is reused many times (linear agent, langgraph, planner). So we compute it
once, save it to JSON, and later runs/agents load the ready descriptions.

The cache lives in `data/output/described.json` (outside git). `refresh=True`
recomputes from scratch (e.g. after a model change — descriptions are
model-dependent).
"""

from __future__ import annotations

import json
from pathlib import Path

from src.loader import Document, load_all
from src.skills.file_description.main import generate_file_description
from src.skills.file_description.schemas import DescribedFile

CACHE_PATH = Path(__file__).resolve().parents[1] / "data" / "output" / "described.json"
DEFAULT_GOAL = "Zrozumieć akta sprawy i wskazać, co zawiera każdy dokument"


def describe_documents(
    documents: list[Document], goal: str = DEFAULT_GOAL, model: str | None = None
) -> list[DescribedFile]:
    """Describe each document (one LLM call per file)."""
    return [generate_file_description(doc, goal, model=model) for doc in documents]


def descriptions_cached(path: str | Path = CACHE_PATH) -> bool:
    """Whether a saved description cache exists."""
    return Path(path).exists()


def save_descriptions(
    described: list[DescribedFile], path: str | Path = CACHE_PATH
) -> Path:
    """Save descriptions to JSON (human-readable UTF-8)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [d.model_dump() for d in described]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_descriptions(path: str | Path = CACHE_PATH) -> list[DescribedFile]:
    """Load descriptions from the cache."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [DescribedFile(**d) for d in data]


def get_descriptions(
    documents: list[Document] | None = None,
    goal: str = DEFAULT_GOAL,
    model: str | None = None,
    refresh: bool = False,
    path: str | Path = CACHE_PATH,
) -> list[DescribedFile]:
    """Return descriptions from the cache; if missing (or refresh=True) — compute and save.

    Computed once; later calls (including from other agents) load from the file.
    """
    if not refresh and descriptions_cached(path):
        return load_descriptions(path)
    docs = documents if documents is not None else load_all()
    described = describe_documents(docs, goal, model=model)
    save_descriptions(described, path)
    return described
