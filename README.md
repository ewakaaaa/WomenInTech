# Czy AI może napisać dobrą apelację?

> **Case study systemu, który zdałby egzamin radcowski.**
> Projekt warsztatowy przygotowany na konferencję **Women in Tech**.

## 📋 O projekcie

Czy AI potrafi napisać apelację na poziomie egzaminu radcowskiego? **Tak — ale tylko
przy odpowiedniej architekturze.**

Akta sprawy to setki stron żargonu, w których model musi znaleźć konkretne fakty.
Halucynacja w piśmie procesowym = przegrana sprawa, więc margines błędu jest zerowy.
Klasyczne RAG-i i chunkowanie tu nie wystarczą.

To 70-minutowe case study pokazuje, jak zbudować system, który radzi sobie z tym
zadaniem — oraz dlaczego bez radców prawnych weryfikujących każdy etap by się nie
udało. Sam pipeline to za mało.

### Co omawiamy

- **Wieloetapowe wnioskowanie** z walidacją **Pydantic** — jak utrzymać
  model na właściwym torze.
- Co robić, gdy model **gubi wątek w długim kontekście**, mimo że „powinien" go pamiętać.
- **Pełen przepływ na żywych aktach**: od plików wejściowych do gotowej apelacji.

### Czego nie będzie

Chunkowania, wektorowej bazy danych ani Graph RAG-a. Zamiast tego — podejście
wypracowane podczas pracy z prawdziwymi sprawami.

### Dla kogo

Dla osób, które znają podstawy LLM-ów i chcą zbudować coś, co działa **na produkcji**,
a nie tylko na demo.

## 📁 Dane

Akta z oficjalnego zadania na **egzamin radcowski 2025** (sprawa Daniela Dzika):
16 pism w `data/input/`, a klucz oceny — zagadnienia, które apelacja powinna
poruszyć — w `data/eval.json`.

📄 Źródło, opis sprawy i spis dokumentów → **[`data/README.md`](data/README.md)**.

## 🚀 Uruchomienie

Projekt używa **[uv](https://docs.astral.sh/uv/)** (zależności w `pyproject.toml`,
zablokowane w `uv.lock`). Jedna komenda tworzy `.venv` i instaluje wszystko:

```bash
uv sync
```

Polecenia w repo poprzedzaj `uv run` (np. `uv run python -m baseline.main`) — uv samo
użyje właściwego środowiska, bez ręcznej aktywacji `.venv`.

> Fallback bez uv: `python3 -m venv .venv && source .venv/bin/activate` (Windows:
> `.venv\Scripts\activate`), a potem `pip install -r requirements.txt`.

## 🤖 Konfiguracja LLM

Projekt korzysta z **OpenAI `gpt-5.4`**. Model podłączasz przez `.env`:

```bash
cp .env.example .env
```
```dotenv
LLM_BASE_URL=https://api.openai.com/v1
LLM_API_KEY=sk-...        # twój klucz z platform.openai.com
LLM_MODEL=gpt-5.4
```

Konfigurację sprawdzisz notebookiem `notebooks/setup.ipynb`.

### Dlaczego `gpt-5.4`?

Zadanie wymaga **dużego okna kontekstu** (sam prompt baseline to ~19 tys. tokenów)
oraz wiedzy prawniczej — wychwycenia subtelnych wątków proceduralnych. Próbowaliśmy
taniego **`gpt-5.4-mini`**, ale gubi on te niuanse — a użyty jako
sędzia w ewaluacji dodatkowo ich nie zalicza. Dlatego dla wiarygodnych
wyników (generacja i ocena) używamy `gpt-5.4`. Działa z każdym dostawcą zgodnym
z interfejsem OpenAI — wystarczy zmienić `LLM_BASE_URL`.

## 📓 Notebooki — jak uruchomić

- `setup.ipynb` (test konfiguracji),
- `baseline_walkthrough.ipynb` (naiwne podejście — sama generacja),
- `eval_walkthrough.ipynb` (ewaluacja na przykładzie baseline: pokrycie + jakość)
- `linear_walkthrough.ipynb` (agent liniowy krok po kroku).

### Najprościej: w przeglądarce (JupyterLab)

Jednorazowo zarejestruj kernel wskazujący na `.venv`:

```bash
.venv/bin/python -m ipykernel install --user --name womenintech --display-name "Python (WomenInTech)"
```

Potem uruchom serwer:

```bash
.venv/bin/jupyter lab
```

Otworzy się przeglądarka → wejdź w `notebooks/` → otwórz plik `.ipynb` →
uruchamiaj komórki **Shift+Enter**. Kernel (prawy górny róg): **Python (WomenInTech)**.

### Import `src.*` w notebookach (jednorazowo)

Notebooki leżą w `notebooks/`, więc kernel startuje w tym katalogu i domyślnie **nie
widzi** pakietów z katalogu głównego (`src`, `baseline`, `agent_*`) — `import src.llm`
rzuca `ModuleNotFoundError: No module named 'src'`. Najprościej dodać ścieżkę projektu
do `.venv` (raz):

```bash
.venv/bin/python -c "import site, os; open(site.getsitepackages()[0] + '/womenintech.pth', 'w').write(os.getcwd())"
```

To tworzy plik `womenintech.pth` w `site-packages`, który przy **każdym starcie
kernela** dokłada katalog projektu do `sys.path` — importy działają z dowolnego
notebooka. Po utworzeniu pliku **zrestartuj kernel** (Kernel → Restart Kernel),
bo `.pth` czyta się tylko przy starcie.

## 📂 Struktura projektu

```
WomenInTech/
├── data/
│   ├── input/         # akta sprawy (pojedyncze PDF-y)
│   └── eval.json      # lista zagadnień, które apelacja powinna poruszyć
├── src/               # wspólne moduły
│   ├── loader.py      # wczytywanie PDF do tekstu (Document, load_pdf, load_all)
│   ├── llm.py         # call_llm — jeden punkt wywołania LLM (instructor + OpenAI-compatible)
│   ├── tokens.py      # liczenie tokenów (count_tokens, count_messages_tokens)
│   ├── sources.py     # prepare_input_texts — selektywny kontekst (wybór dok. po nazwie)
│   ├── eval/          # ewaluacja: coverage.py (pokrycie) + quality.py (jakość/forma)
│   └── skills/        # umiejętności agenta — jeden folder per umiejętność
│       ├── file_description/  # generate_file_description (main.py, prompts.py, schemas.py)
│       ├── tasks/             # generate_tasks
│       ├── make_task/         # make_task
│       ├── strategy/          # generate_strategy
│       └── document/          # generate_document
├── baseline/          # wersja 0 — naiwne podejście (wszystko → jeden prompt)
│   ├── prompts.py     # system prompt
│   ├── main.py        # generuje apelację → baseline/output/
│   ├── output/        # apelacje + logi przebiegów (artefakty, poza gitem)
│   └── README.md      # podsumowanie i wyniki baseline
├── agent_linear/      # agent liniowy — te same umiejętności spięte po kolei (bez LangGraph)
│   ├── main.py        # run() spina umiejętności → zapis apelacji + ocena pokrycia
│   └── README.md      # opis procesu krok po kroku
├── agent_langgraph/   # ten sam agent jako graf LangGraph (fan-out przez Send)
│   ├── state.py       # OverallState (z reducerami) + payloady Send
│   ├── graph.py       # węzły opakowujące umiejętności + routing + skompilowany graph
│   ├── main.py        # uruchomienie → agent_langgraph/output/
│   ├── graph.md       # diagram grafu (mermaid, generowany z kodu)
│   └── README.md      # po co LangGraph, skoro wynik ten sam co liniowo
├── agent_planner/     # agent nieliniowy — TYLKO idea (bez kodu): README + diagram
│   ├── graph.md       # diagram grafu cyklicznego (planer = hub) — mermaid
│   └── README.md      # jak działałby planer + human-in-the-loop (kierunek „co dalej?")
├── notebooks/         # setup + baseline/eval/linear (demo na gpt-5.4-mini)
├── presentation/      # materiały i plan prezentacji warsztatowej
├── .env.example       # szablon konfiguracji LLM (skopiuj do .env)
├── pyproject.toml     # zależności (uv)
├── uv.lock            # zablokowane wersje
└── requirements.txt   # fallback dla pip
```

## 🛠️ Wymagania

- Python **≥ 3.12** (zob. `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) (zalecane) — albo pip + `requirements.txt`
- dostęp do modelu LLM przez API (OpenAI, `gpt-5.4`)
