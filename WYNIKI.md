# Wyniki (roboczo)

Zebrane liczby z dotychczasowych przebiegów. Plik roboczy — docelowo część przeniesiemy
do README poszczególnych podejść.

## Dane

- **Pokrycie** — odsetek zagadnień z `data/eval.json` (12 pozycji) poruszonych w apelacji,
  ocena sędzią-LLM (`src/eval/coverage.py`).
- **Jakość** — ocena „miękka" 2–6 wg kryteriów egzaminu radcowskiego, średnia z 3 kryteriów
  (`src/eval/quality.py`). Sędzią jest **gpt-5.4** (tani model nie wyłapuje błędów formalnych).
- Koszty: ceny z `src/cost.py` (gpt-5.4 = $2.50/$15 za 1M tok; mini = $0.75/$4.50).

## Pokrycie

| podejście | model generacji | sędzia | pokrycie |
|---|---|---|---|
| baseline     | gpt-5.4-mini | mini    | ~47% |
| agent_linear | gpt-5.4-mini | mini    | ~42–50% |
| baseline     | **gpt-5.4**  | gpt-5.4 | **58% (7/12)** — przebieg 2026-06-06 (wcześniej 42%, duża wariancja) |
| agent_linear | **gpt-5.4**  | gpt-5.4 | **67%** |

Wniosek: przewaga agenta liniowego nad baseline ujawnia się dopiero z **mocnym modelem**
(generacja *i* sędzia). Na samym mini wszystko spłaszcza się do ~42–50% — „podwójne wąskie
gardło mini": słaby autor nie robi skoków prawnych, słaby sędzia ich nie docenia.

## Jakość (sędzia gpt-5.4)

| podejście | model generacji | jakość (śr. 2–6) |
|---|---|---|
| baseline     | gpt-5.4 | **4.33** (przebieg 2026-06-06: formalne 5 · zastosowanie 4 · poprawność 4; wcześniej 3.33 — wariancja) |
| agent_linear | gpt-5.4 | **4.33** |

## Koszt i czas metody (sama generacja, bez ewaluacji)

| podejście | model | koszt metody | czas metody |
|---|---|---|---|
| baseline     | **gpt-5.4** | **~$0.105** (1 wyw., 19 473 wej + 3 757 wyj) | **48,3 s** |
| agent_linear | **gpt-5.4** | _do uzupełnienia_ (puścić `python -m agent_linear.main`) | _do uzupełnienia_ |

Koszt ewaluacji liczony osobno (przebieg baseline 2026-06-06): pokrycie ~$0.161 (12 wyw., 40,5 s),
jakość ~$0.031 (1 wyw., 18,7 s).

Linear jest droższy (wiele wywołań: opisy → plan → wykonanie kroków → strategia → dokument).
Ograniczenie planu do **maks. 10 kroków** trzyma górną granicę kosztu w ryzach
(wcześniej 19–20 kroków → ~$1.46).

> **TODO:** puścić `python -m agent_linear.main` na `gpt-5.4`, żeby uzupełnić koszt i czas linera.

## Notatki

- Notebooki (`baseline_walkthrough`, `eval_walkthrough`, `linear_walkthrough`) chodzą na
  **gpt-5.4-mini** — to tanie demo; liczby „produkcyjne" pochodzą z `__main__` modułów na gpt-5.4.
- Transkrypcja akt z `DoGeDo_2` zweryfikowana jako wierna 1:1.
