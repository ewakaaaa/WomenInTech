# Ewaluacja

Wygenerować apelację to jedno — ale skąd wiadomo, że jest **dobra**? Ten moduł
odpowiada na to liczbami. Zadajemy dwa niezależne pytania:

1. **Czy apelacja porusza to, co powinna?** → pokrycie (`coverage`, `compare`)
2. **Czy apelacja czegoś nie zmyśliła?** → ugruntowanie / halucynacje (`grounding`)

Klucz oceny to `data/eval.json` — lista zagadnień, które dobra apelacja powinna
podnieść (zarzuty + wnioski).

---

## 1. Pokrycie — `coverage.py`

Dla **każdego** zagadnienia z `data/eval.json` sędzia-LLM (egzaminator) decyduje,
czy apelacja faktycznie je porusza (wraz z istotą argumentacji, nie tylko wzmianką).

- `evaluate(appeal_text)` → `CoverageResult` z `covered`, `total`, `score`
  (`covered / total`) i werdyktem per zagadnienie.
- `evaluate_file(path)` — to samo dla apelacji zapisanej w pliku.

Jedna liczba (`score`) porównywalna między wszystkimi podejściami. Powtarzalność
oceny (kilka przebiegów → średnia) oraz koszt pokazuje notebook
`notebooks/baseline_and_eval.ipynb`.

## 2. Porównanie podejść — `compare.py`

Ocenia gotowe apelacje (pliki `.txt`) z poszczególnych podejść tym samym
miernikiem pokrycia i drukuje tabelę obok siebie + listę niepokrytych zagadnień.

```bash
uv run python -m src.eval.compare
```

Wymaga wcześniej wygenerowanych apelacji (np. `baseline/apelacja_baseline.txt`).

## 3. Halucynacje / ugruntowanie — `grounding.py`

Sprawdza, czy apelacja nie powołuje faktów (dat, kwot, nazwisk, zdarzeń,
cytatów), których w aktach nie ma. Zbudowane **etapowo**:

- **Etap 1 — ekstrakcja** (`extract_claims`): rozkłada apelację na atomowe
  twierdzenia faktyczne (pomija oceny i argumentację prawną).
- **Etap 2 — weryfikacja** *bez wczytywania wszystkich akt*:
  - **2a** (`select_sources`): na podstawie krótkich **opisów dokumentów**
    (`describe_documents` → skill `file_description`) LLM wybiera, w których
    plikach sprawdzić dane twierdzenie,
  - **2b** (`verify_claim`): wczytujemy tekst **tylko wybranych** plików i w nich
    weryfikujemy fakt → `supported` / `unsupported` / `contradicted` + cytat,
  - `check_claim` spina 2a + 2b dla jednego twierdzenia.
- **Etap 3 — agregacja** (`evaluate_grounding`): wskaźnik halucynacji
  (niepotwierdzone + sprzeczne / wszystkie) + raport `GroundingResult` z
  werdyktem per twierdzenie.

```bash
uv run python -m src.eval.grounding        # demo Etapów 1–2 na przykładzie
```

End-to-end (Etap 1→2→3) z poziomu kodu:

```python
from src.loader import load_all
from src.eval.grounding import evaluate_grounding

result = evaluate_grounding(appeal_text, load_all())
print(result.hallucination_rate)          # np. 0.15 = 15% faktów bez oparcia w aktach
```

---

## Dwa mierniki, dwa ryzyka

| Miernik | Pyta | Łapie ryzyko |
|---------|------|--------------|
| **pokrycie** | czy poruszono wymagane zagadnienia? | apelacja **pomija** istotny zarzut |
| **ugruntowanie** | czy fakty pochodzą z akt? | apelacja **zmyśla** fakty (halucynacje) |

Wysokie pokrycie przy zmyślonych faktach to wciąż zła apelacja — dlatego oba
mierniki są potrzebne.
