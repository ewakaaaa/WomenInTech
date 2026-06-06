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

Akta pochodzą z oficjalnego zadania na **egzamin radcowski 2025**, opublikowanego przez
Ministerstwo Sprawiedliwości:

> https://www.gov.pl/web/sprawiedliwosc/zadania-wraz-z-opisem-istotnych-zagadnien-na-egzamin-radcowski-w-2025-r2

Pliki zostały **pobrane** i **podzielone na pojedyncze dokumenty** (po jednym
piśmie na plik), umieszczone w `data/input/`. 

Plik `data/eval.json` to **lista zagadnień, które apelacja powinna poruszyć**.

## 🚀 Uruchomienie

### 1. Środowisko wirtualne (`.venv`)

```bash
# Utworzenie środowiska
python3 -m venv .venv

# Aktywacja
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows (PowerShell / cmd)
```

### 2. Instalacja zależności

```bash
pip install --upgrade pip
pip install pdfplumber pydantic
```

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
oraz „skoków" prawniczych — wychwycenia subtelnych wątków proceduralnych. Próbowaliśmy
taniego **`gpt-5.4-mini`** (kilka razy taniej), ale gubi on te niuanse — a użyty jako
sędzia w ewaluacji dodatkowo ich nie zalicza („podwójne wąskie gardło mini": słaby
autor nie robi skoków prawnych, słaby sędzia ich nie docenia). Dlatego dla wiarygodnych
wyników (generacja i ocena) używamy `gpt-5.4`. Działa z każdym dostawcą zgodnym
z interfejsem OpenAI — wystarczy zmienić `LLM_BASE_URL`.

### Który model gdzie? (ważne)

Rozdzieliliśmy dwa zastosowania, żeby nie przepalać budżetu na demo:

| gdzie | model | po co |
|---|---|---|
| **notebooki** (`notebooks/*.ipynb`) | `gpt-5.4-mini` | **cele demonstracyjne** — tanio przeklikać przepływ na żywo na warsztacie. Model wymuszony w komórce konfiguracyjnej (`os.environ["LLM_MODEL"] = "gpt-5.4-mini"`), niezależnie od `.env`. |
| **moduły podejść** (`python -m baseline.main`, `python -m agent_linear.main`) | `gpt-5.4` (z `.env`) | **właściwe wyniki** — to z nich pochodzą liczby w `WYNIKI.md` i w README podejść. |

Wyjątek: **ocena jakości** (`src/eval/quality.py`) zawsze idzie mocnym sędzią
(`gpt-5.4`), nawet wywołana z notebooka — tani model nie wyłapuje błędów formalnych.

> ⚠️ Liczby czasu (s/wywołanie) w `WYNIKI.md` trzeba jeszcze raz przeliczyć po dodaniu
> pomiaru czasu — uruchamiając moduły podejść na `gpt-5.4`.

## 📓 Notebooki — jak uruchomić

W `notebooks/`: `setup.ipynb` (test konfiguracji), `baseline_walkthrough.ipynb`
(naiwne podejście — sama generacja), `eval_walkthrough.ipynb` (ewaluacja na przykładzie
baseline: pokrycie + jakość), `linear_walkthrough.ipynb` (agent liniowy krok po kroku),
`planner_walkthrough.ipynb` (planer).

> Najpierw uzupełnij `.env` (klucz `LLM_API_KEY`) — notebooki czytają stąd klucz.
> **Model w notebookach jest wymuszony na `gpt-5.4-mini`** (tanie demo), więc wartość
> `LLM_MODEL` z `.env` nie ma tu znaczenia. Po właściwe wyniki uruchom moduły podejść
> (`python -m baseline.main`) — tam działa `gpt-5.4` z `.env`.

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

### W edytorze Zed

Zed **nie renderuje `.ipynb`** (pokazuje surowy JSON), ale ma **REPL**. Pracuj na
pliku `.py` z komórkami `# %%`:

1. Otwórz plik `.py` w Zedzie.
2. Postaw kursor w komórce (między znacznikami `# %%`).
3. Otwórz paletę: **⌘ ⇧ P** → wpisz **`repl: run`** (lub skrót **⌃ ⇧ Return**).

Wynik pojawia się pod komórką; pierwsze uruchomienie startuje kernel.

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
│       ├── document/          # generate_document
│       └── planner/           # plan_next — decyzja: analyze / ask_human / write / no_grounds
├── baseline/          # wersja 0 — naiwne podejście (wszystko → jeden prompt)
│   ├── prompts.py             # system prompt
│   ├── main.py                # generuje apelację → baseline/apelacja_baseline.txt
│   ├── apelacja_baseline.txt  # wygenerowana apelacja (artefakt)
│   └── README.md              # podsumowanie i wyniki baseline
├── agent_linear/      # agent liniowy — te same umiejętności spięte po kolei (bez LangGraph)
│   ├── main.py        # run() spina umiejętności → zapis apelacji + ocena pokrycia
│   └── README.md      # opis procesu krok po kroku
├── agent_langgraph/   # ten sam agent jako graf LangGraph (fan-out przez Send)
│   ├── state.py       # OverallState (z reducerami) + payloady Send
│   ├── graph.py       # węzły opakowujące umiejętności + routing + skompilowany graph
│   ├── main.py        # uruchomienie → agent_langgraph/apelacja.txt
│   ├── graph.md       # diagram grafu (mermaid, generowany z kodu)
│   └── README.md      # po co LangGraph, skoro wynik ten sam co liniowo
├── agent_planner/     # agent nieliniowy — planer w centrum, pętle + human-in-the-loop
│   ├── state.py       # PlannerState + payloady Send
│   ├── graph.py       # graf cykliczny (planer = hub) + interrupt
│   ├── main.py        # uruchomienie z checkpointerem → agent_planner/apelacja.txt
│   ├── graph.md       # diagram grafu (mermaid)
│   └── README.md      # jak działa planer i human-in-the-loop
├── notebooks/         # setup + baseline/eval/linear/planner_walkthrough (demo na gpt-5.4-mini)
├── presentation/      # materiały i plan prezentacji warsztatowej
├── langgraph.json     # konfiguracja LangGraph Studio (uv run langgraph dev)
├── .env.example       # szablon konfiguracji LLM (skopiuj do .env)
├── pyproject.toml     # zależności (uv)
├── uv.lock            # zablokowane wersje
└── requirements.txt   # fallback dla pip
```

### Moduły

- **`src/loader.py`** — `load_pdf(path)` wczytuje pojedynczy plik PDF i zwraca
  `Document` (Pydantic) z nazwą pliku i wyekstrahowanym tekstem; `load_all(dir)`
  wczytuje wszystkie PDF-y z katalogu.
- **`src/llm.py`** — `call_llm(messages, response_model, ...)` zwraca odpowiedź
  zwalidowaną względem modelu Pydantic. Klient jest zgodny z interfejsem OpenAI,
  więc przez zmianę `base_url`/`api_key` w `.env` można podpiąć dowolnego dostawcę
  zgodnego z interfejsem OpenAI (OpenAI, proxy itp.).
- **`src/tokens.py`** — pomocnicze liczenie tokenów (tiktoken) dla tekstu i listy
  wiadomości.
- **`src/eval/`** — ewaluacja: `coverage.py` (`evaluate(appeal_text)` ocenia pokrycie
  zagadnień z `data/eval.json`, LLM-as-judge) oraz `quality.py` (ocena jakości/formy
  wg kryteriów egzaminu radcowskiego). Wyniki podejść porównujesz, odczytując je z notebooków.
- **`src/sources.py`** — `prepare_input_texts(documents, names)` zwraca tekst tylko
  wybranych dokumentów (selektywny kontekst); współdzielone przez agenta liniowego
  i wersję LangGraph.
- **`src/skills/`** — umiejętności agenta, każda w osobnym folderze (`main.py` =
  czysta funkcja, `prompts.py`, `schemas.py`): `file_description`, `tasks`,
  `make_task`, `strategy`, `document`, `planner`.
- **`baseline/`** — naiwna „wersja 0": całe akta + jeden prompt „napisz apelację".
  Punkt wyjścia warsztatu (szczegóły w `baseline/README.md`).
- **`agent_linear/`** — agent liniowy: te same umiejętności (`src/skills/*`) spięte
  po kolei, bez LangGraph. Pętle `for` to miejsca, które później zastąpi fan-out
  grafu.
- **`agent_langgraph/`** — ten sam agent jako graf LangGraph: węzły to cienkie
  opakowania umiejętności, a pętle z agenta liniowego zastępuje fan-out przez `Send`
  (jeden plik / jedno zadanie na gałąź), z reducerami zbierającymi wyniki. Można go
  uruchomić w **LangGraph Studio** (`uv run langgraph dev`) — szczegóły i odpowiedź
  „po co LangGraph" w `agent_langgraph/README.md`.
- **`agent_planner/`** — agent **nieliniowy**: planer („mózg operacji") w centrum
  grafu decyduje, co dalej (analizuj / zapytaj człowieka / pisz / brak podstaw), więc
  graf zawraca w pętli. Pokazuje **cykle** i **human-in-the-loop** (pauza na
  potwierdzenie radcy) — czyli to, co LangGraph dokłada ponad liniowy pipeline.
- **`notebooks/`** (`uv run jupyter lab`, **demo na `gpt-5.4-mini`**): `setup.ipynb`
  (konfiguracja LLM + test — zacznij tutaj), `baseline_walkthrough.ipynb` (naiwne podejście —
  sama generacja apelacji), `eval_walkthrough.ipynb` (ewaluacja na przykładzie baseline:
  pokrycie + jakość), `linear_walkthrough.ipynb` (umiejętności krok po kroku),
  oraz `planner_walkthrough.ipynb` (agent nieliniowy z human-in-the-loop — pauza na Twoją decyzję).
- **`presentation/`** — plan i materiały do warsztatu (`presentation/README.md`).

## 🛠️ Wymagania

- Python 3.x
- Pydantic
- dostęp do modelu LLM przez API (OpenAI, `gpt-5.4`)
