"""Compare approaches against ``data/eval.json`` and print a coverage table.

Evaluates each approach's generated appeal (if present) on the same yardstick —
how many required issues it covers — so they can be compared side by side.

    uv run python -m src.eval.compare
"""

from __future__ import annotations

from pathlib import Path

from src.eval.coverage import CoverageResult, evaluate_file, load_eval

APPROACHES: list[tuple[str, str]] = [
    ("baseline", "baseline/apelacja_baseline.txt"),
    ("agent_linear", "agent_linear/apelacja.txt"),
    ("agent_langgraph", "agent_langgraph/apelacja.txt"),
    ("agent_planner", "agent_planner/apelacja.txt"),
]


def main() -> None:
    reports: list[tuple[str, CoverageResult]] = []
    for name, path in APPROACHES:
        if not Path(path).exists():
            print(f"pomijam {name}: brak pliku {path}")
            continue
        print(f"oceniam {name}...")
        reports.append((name, evaluate_file(path)))

    if not reports:
        print("\nBrak apelacji do oceny — najpierw wygeneruj je w poszczególnych podejściach.")
        return

    print(f"\n{'podejście':18} {'pokryte':>8} {'score':>7}")
    print("-" * 35)
    for name, r in reports:
        print(f"{name:18} {f'{r.covered}/{r.total}':>8} {r.score:>6.0%}")

    # brakujące zagadnienia per podejście (treść zagadnień z klucza, wg kolejności)
    issues = load_eval()
    for name, r in reports:
        missing = [iss for iss, res in zip(issues, r.results) if not res.covered]
        if missing:
            print(f"\n{name} — niepokryte zagadnienia ({len(missing)}):")
            for issue in missing:
                print(f"  • {issue[:90]}")


if __name__ == "__main__":
    main()
