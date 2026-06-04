"""Graph state for the planner agent.

The planner sits at the center: file descriptions and analysis results accumulate
in the state (reducers), and the planner reads them each round to decide the next
move. The two ``*In`` TypedDicts are the per-branch payloads sent via ``Send``.
"""

from __future__ import annotations

import operator
from typing import Annotated

from typing_extensions import TypedDict

from src.loader import Document
from src.skills.file_description.schemas import DescribedFile
from src.skills.make_task.schemas import TaskOutput
from src.skills.planner.schemas import PlannerDecision
from src.skills.tasks.schemas import Task


class PlannerState(TypedDict):
    """State shared across the planner graph."""

    goal: str
    documents: list[Document]
    files_out: Annotated[list[DescribedFile], operator.add]
    task_outputs: Annotated[list[TaskOutput], operator.add]
    decision: PlannerDecision
    rounds: int
    human_feedback: str
    document: str


class DescribeFileIn(TypedDict):
    """Payload for the per-file description branch."""

    goal: str
    document: Document


class RunTaskIn(TypedDict):
    """Payload for the per-task execution branch."""

    goal: str
    task: Task
    sources_text: str
