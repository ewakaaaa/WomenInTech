# Ewaluacja

Wygenerować apelację to jedno — ale skąd wiadomo, że jest **dobra**? Ten moduł
odpowiada na to liczbami. Zadajemy dwa pytania:

1. **Czy apelacja porusza to, co powinna?** → pokrycie (`coverage`)
2. **Jak jest napisana?** → jakość/forma (`quality`)

Wyniki poszczególnych podejść porównujesz, odczytując je z logów przebiegów
(`<metoda>/output/run_*.log`) albo z notebooka `notebooks/eval_walkthrough.ipynb`.

Klucz oceny to `data/eval.json` — lista zagadnień, które dobra apelacja powinna
podnieść (zarzuty + wnioski).

---

## 1. Pokrycie — `coverage.py`

Dla **każdego** zagadnienia z `data/eval.json` sędzia-LLM (egzaminator) decyduje,
czy apelacja faktycznie je porusza (wraz z istotą argumentacji, nie tylko wzmianką).

- `evaluate(appeal_text, print_results=True)` → `CoverageResult` z `covered`,
  `total`, `score` (`covered / total`) i werdyktem per zagadnienie.
- `evaluate_file(path)` — to samo dla apelacji zapisanej w pliku.

Jedna liczba (`score`) porównywalna między wszystkimi podejściami. Pokrycie + jakość
na przykładzie baseline pokazuje notebook `notebooks/eval_walkthrough.ipynb`; z CLI
ocenę zapisanej apelacji odpalisz przez `uv run python -m src.eval.report <metoda>`.

## 2. Jakość / forma — `quality.py`

Ocena „miękka", jak u egzaminatora — nie *czy* odhaczono punkty, ale **jak**
pismo jest napisane. Wg trzech ustawowych kryteriów (art. 36⁴ ustawy o radcach
prawnych), w skali 2–6:

1. zachowanie wymogów formalnych (np. właściwy sąd odwoławczy),
2. właściwość zastosowania i interpretacji przepisów,
3. poprawność zaproponowanego rozwiązania.

- `evaluate_quality(appeal_text)` → `QualityVerdict` (3 oceny 2–6 + `reasoning` + `srednia`).
- **Sędzią jest mocny model** (`gpt-5.4`, `QUALITY_JUDGE_MODEL`) — `gpt-5.4-mini`
  jako oceniający nie wyłapuje błędów formalnych i nie różnicuje pism.

```bash
uv run python -m src.eval.quality agent_linear   # ocena najnowszej zapisanej apelacji
```

---

## Dwa mierniki, dwa spojrzenia

| Miernik | Pyta | Łapie |
|---------|------|-------|
| **pokrycie** (`coverage`) | czy poruszono wymagane zagadnienia? | **pominięty** zarzut (twardy klucz) |
| **jakość** (`quality`) | jak napisane — forma i argumentacja? | słaba **forma**/warsztat (miękka ocena) |

Same punkty to nie wszystko — apelację ocenia się też za formę i jakość
argumentacji, dlatego potrzebne są oba spojrzenia.
