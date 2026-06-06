# Ewaluacja

Wygenerować apelację to jedno — ale skąd wiadomo, że jest **dobra**? Ten moduł
odpowiada na to liczbami. Zadajemy dwa pytania:

1. **Czy apelacja porusza to, co powinna?** → pokrycie (`coverage`)
2. **Jak jest napisana?** → jakość/forma (`quality`)

Wyniki poszczególnych podejść porównujesz, odczytując je z logów przebiegów
(`<metoda>/output/run_*.log`) albo z notebooka `notebooks/eval_walkthrough.ipynb`.

Klucz oceny to `data/eval.json` — lista zagadnień, które dobra apelacja powinna
podnieść (zarzuty + wnioski).

## 1. Pokrycie — `coverage.py`

Dla **każdego** zagadnienia z `data/eval.json` sędzia-LLM (egzaminator) decyduje,
czy apelacja faktycznie je porusza (wraz z istotą argumentacji, nie tylko wzmianką).

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
