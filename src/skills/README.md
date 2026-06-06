# Umiejętności (skills)

Każda umiejętność to **czysta funkcja** z `<umiejętność>/main.py` (wejście →
wyjście walidowane przez Pydantic). Robi jedną rzecz i nie wie nic o pozostałych
— dzięki temu da się ją testować osobno i opakować jako węzeł grafu.

Te same skille spinają dwa podejścia:

- [`agent_linear/`](../../agent_linear/) — wywołuje je po kolei (pętle `for`),
- [`agent_langgraph/`](../../agent_langgraph/) — to samo, ale z równoległym fan-outem (`Send`).

Jest jeszcze [`agent_planner/`](../../agent_planner/) — agent **nieliniowy** (planer
decydujący, co dalej), ale to **tylko idea** (README + diagram, bez kodu), więc nie
spina tu żadnego skilla.

Pliki spinające (`main.py` / `graph.py`) tylko wołają umiejętności i
przekazują wyniki — logika siedzi w skillach.

## Co robi każda umiejętność (i jaki problem baseline rozwiązuje)

Baseline (`baseline/`) robił wszystko jednym promptem — całe akta w jeden strzał.
Agent rozbija to na umiejętności, każda rozwiązuje konkretny problem naiwnego
podejścia (lista problemów: [`baseline/README.md`](../../baseline/README.md)).

| Umiejętność | Funkcja (wejście → wyjście) | Co robi | Jaki problem baseline rozwiązuje |
|-------------|------------------------------|---------|----------------------------------|
| **file_description** | `generate_file_description(document, goal)` → `DescribedFile` | Zamienia surowe akta w zwięzłe, ukierunkowane na cel opisy — „mapę" sprawy. | Mniej szumu: planer nie czyta 16 pełnych dokumentów, tylko wie, gdzie czego szukać. |
| **tasks** | `generate_tasks(goal, described_files)` → `Tasks` | Rozbija wielki cel na małe kroki; każdy wskazuje, **które** dokumenty są mu potrzebne (`task.input`). | „Wszystko naraz" → dziel i rządź. Plan jest też **śladem**, co i czemu robimy. |
| **make_task** | `make_task(goal, task, sources_text)` → `TaskOutput` | Wykonuje **jeden** krok na **tylko** wskazanych dokumentach. | Zapchany kontekst i „lost in the middle"; **izolacja błędu** (zły krok nie psuje reszty, da się go powtórzyć); **audytowalność**. |
| **strategy** | `generate_strategy(goal, task_outputs)` → `Strategy` | Z zebranych analiz wybiera linię obrony / najlepsze podejście. | Świadomy, spójny kierunek zamiast przypadkowego — zanim zacznie się pisać. |
| **document** | `generate_document(goal, strategy, task_outputs)` → `GeneratedDocument` | Pisze pismo na **gotowej analizie i strategii**, a nie na surowych aktach. | Mniej halucynacji i pominięć — model opiera się na zweryfikowanych faktach. |

Krótko: **mały, skupiony kontekst na każdym etapie + jawny plan + możliwość
weryfikacji i powtórzenia kroku** — to jest to, czego baseline nie daje.

## Sedno — selektywny kontekst

Różnica wobec `baseline/` (gdzie całe akta lecą w jeden prompt): tutaj `tasks`
decyduje, **które** dokumenty są potrzebne do danego kroku, a `make_task` (przez
`prepare_input_texts` z [`src/sources.py`](../sources.py)) widzi **tylko ten
wycinek**. Model nigdy nie ogląda wszystkiego naraz — pracuje na małych, trafnych
fragmentach.

## Anatomia jednej umiejętności

Każdy katalog ma ten sam układ:

- `main.py` — czysta funkcja (np. `generate_tasks`), jedyne wejście,
- `prompts.py` — system/user prompt,
- `schemas.py` — modele Pydantic wejścia/wyjścia (kontrakt umiejętności).
