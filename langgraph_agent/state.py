"""Graph state for the LangGraph agent.

``OverallState`` is the shared state that flows through the graph. The two
``*In`` TypedDicts are the small payloads sent to fan-out nodes via ``Send`` —
each parallel branch receives only what it needs.
"""

from __future__ import annotations

import operator
from typing import Annotated

from typing_extensions import TypedDict

from src.loader import Document
from src.skills.file_description.schemas import DescribedFile
from src.skills.make_task.schemas import TaskOutput
from src.skills.strategy.schemas import Strategy
from src.skills.tasks.schemas import Task


class OverallState(TypedDict):
    """State shared across the whole graph."""

    goal: str
    documents: list[Document]
    files_out: Annotated[list[DescribedFile], operator.add]
    tasks: list[Task]
    tasks_out: Annotated[list[TaskOutput], operator.add]
    strategy: Strategy
    document: str


class DescribeFileIn(TypedDict):
    """Payload sent to the per-file description branch."""

    goal: str
    document: Document


class RunTaskIn(TypedDict):
    """Payload sent to the per-task execution branch."""

    goal: str
    task: Task
    sources_text: str
