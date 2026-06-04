"""Selecting and formatting source document texts for a task.

Given the documents a task asked for (by file name), build the text block the
skill will read. Shared by the linear agent and the LangGraph agent.
"""

from __future__ import annotations

from src.loader import Document


def prepare_input_texts(documents: list[Document], names: list[str] | None) -> str:
    """Return the text of the named documents, each wrapped in <name> tags."""
    if not names:
        return ""
    blocks = [
        f"<{doc.filename}>\n{doc.text}\n</{doc.filename}>"
        for doc in documents
        if doc.filename in names
    ]
    return "\n".join(blocks)
