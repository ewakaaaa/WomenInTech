"""Linear agent — wires the skills in sequence (no LangGraph yet).

The same skills (``src/skills/*``) run one after another over plain Python
variables. Later, LangGraph will replace this hand-written sequencing and the
``for`` loops with conditional edges + Send — the skills themselves won't change.

    uv run python -m agent_linear.pipeline
"""

from __future__ import annotations

from src.descriptions import get_descriptions
from src.loader import Document, load_all
from src.skills.document.main import generate_document
from src.skills.document.schemas import GeneratedDocument
from src.skills.make_task.main import make_task
from src.skills.strategy.main import generate_strategy
from src.skills.tasks.main import generate_tasks
from src.sources import prepare_input_texts

GOAL = "Wygeneruj apelację z perspektywy obrony"


def run(
    goal: str = GOAL,
    model: str | None = None,
    documents: list[Document] | None = None,
) -> GeneratedDocument:
    documents = documents if documents is not None else load_all()
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
    # Generacja + ocena POKRYCIA z CLI (bez notebooka, bez halucynacji):
    #   uv run python -m agent_linear.pipeline
    import os

    from src.cost import cost_summary
    from src.eval.report import evaluate_appeal
    from src.llm import track_usage
    from src.output import save_appeal

    print("=== GENERACJA (agent liniowy) ===")
    documents = load_all()
    with track_usage() as gen_usage:
        document = run(documents=documents)
    appeal = document.tekst

    saved = save_appeal(appeal, "agent_linear")
    print(f"\nZapisano apelację: {saved} ({len(appeal):,} znaków)")
    print(f"Koszt generacji: {cost_summary(gen_usage, os.environ.get('LLM_MODEL', '?'))}")

    evaluate_appeal(appeal)
