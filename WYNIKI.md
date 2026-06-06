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
| baseline     | **gpt-5.4**  | gpt-5.4 | **42%** |
| agent_linear | **gpt-5.4**  | gpt-5.4 | **67%** |

Wniosek: przewaga agenta liniowego nad baseline ujawnia się dopiero z **mocnym modelem**
(generacja *i* sędzia). Na samym mini wszystko spłaszcza się do ~42–50% — „podwójne wąskie
gardło mini": słaby autor nie robi skoków prawnych, słaby sędzia ich nie docenia.

## Jakość (sędzia gpt-5.4)

| podejście | model generacji | jakość (śr. 2–6) |
|---|---|---|
| baseline     | gpt-5.4 | **3.33** |
| agent_linear | gpt-5.4 | **4.33** |

## Koszt generacji (jednorazowo)

| podejście | gpt-5.4-mini | gpt-5.4 |
|---|---|---|
| baseline     | ~$0.023 | ~$0.076 |
| agent_linear | ~$0.20  | ~$0.67–1.46 |

Linear jest droższy (wiele wywołań: opisy → plan → wykonanie kroków → strategia → dokument).
Ograniczenie planu do **maks. 10 kroków** trzyma górną granicę kosztu w ryzach
(wcześniej 19–20 kroków → ~$1.46).

## Czas (do uzupełnienia)

Pomiar czasu (`s/wywołanie`) dodaliśmy do `Usage`/`cost_summary` **po** tych przebiegach,
więc powyższe liczby go nie mają. **TODO:** przepuścić jeszcze raz `python -m baseline.main`
i `python -m agent_linear.main` na `gpt-5.4`, żeby zebrać czas (i odświeżyć koszty).

## Notatki

- Notebooki (`baseline_walkthrough`, `eval_walkthrough`, `linear_walkthrough`) chodzą na
  **gpt-5.4-mini** — to tanie demo; liczby „produkcyjne" pochodzą z `__main__` modułów na gpt-5.4.
- Transkrypcja akt z `DoGeDo_2` zweryfikowana jako wierna 1:1.
