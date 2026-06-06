"""Linear agent — wires the skills in sequence (no LangGraph yet).

The same skills (``src/skills/*``) run one after another over plain Python
variables. Later, LangGraph will replace this hand-written sequencing and the
``for`` loops with conditional edges + Send — the skills themselves won't change.

    uv run python -m agent_linear.pipeline
"""

from __future__ import annotations

from pathlib import Path

from src.descriptions import get_descriptions
from src.loader import load_all
from src.skills.document.main import generate_document
from src.skills.document.schemas import GeneratedDocument
from src.skills.make_task.main import make_task
from src.skills.strategy.main import generate_strategy
from src.skills.tasks.main import generate_tasks
from src.sources import prepare_input_texts

GOAL = "Wygeneruj apelację z perspektywy obrony"
OUTPUT_PATH = "agent_linear/apelacja.txt"


def run(goal: str = GOAL, model: str | None = None) -> GeneratedDocument:
    documents = load_all()
    print(f"Loaded {len(documents)} documents")

    # 1. generate_file_description — opisz każdy dokument (z cache: liczone raz)
    described = get_descriptions(documents, goal, model=model)
    print(f"Described {len(described)} files")

    # 2. generate_tasks — zaplanuj kroki analizy
    tasks = generate_tasks(goal, described, model=model)
    print(f"Planned {len(tasks.thoughts)} tasks")

    # 3. make_task — wykonaj każdy krok na wybranych dokumentach
    task_outputs = []
    for i, task in enumerate(tasks.thoughts, 1):
        sources_text = prepare_input_texts(documents, task.input)
        task_outputs.append(make_task(goal, task, sources_text, model=model))
        print(f"  task {i}/{len(tasks.thoughts)} done")

    # 4. generate_strategy — wybierz najlepszą strategię
    strategy = generate_strategy(goal, task_outputs, model=model)
    print("Strategy ready")

    # 5. generate_document — napisz pismo
    document = generate_document(goal, strategy, task_outputs, model=model)
    print("Document generated")

    return document


if __name__ == "__main__":
    document = run()

    output = Path(OUTPUT_PATH)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document.tekst, encoding="utf-8")
    print(f"Saved to {OUTPUT_PATH} ({len(document.tekst):,} chars)")
