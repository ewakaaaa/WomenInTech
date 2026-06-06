# Agent w wersji LangGraph

> Te same umiejętności (`src/skills/*`) co w `agent_linear/`, spięte w graf.
> **Wynik jest taki sam — bo to ta sama logika.** Pytanie brzmi więc: skoro
> rezultat identyczny, **co właściwie daje LangGraph?**

📊 Diagram grafu (mermaid, generowany z kodu): [`graph.md`](graph.md).

## Krótka odpowiedź

LangGraph nie zmienia *co* agent robi — zmienia *jak to jest wykonywane,
obserwowane i utrzymywane*. Wartość nie leży w treści apelacji, tylko w
inżynierii wokół niej.

## Co realnie zyskujemy (przy identycznym wyniku)

1. **Równoległość za darmo (fan-out przez `Send`)**
   W `agent_linear` opis 16 plików i wykonanie zadań idą w pętli `for` —
   jeden po drugim. W grafie `Send` rozsyła je **równolegle**, a reducery
   (`operator.add` na `files_out`/`tasks_out`) same scalają wyniki. Ten sam
   rezultat, krótszy czas.

2. **Stan jako kontrakt, nie zmienne lokalne**
   `OverallState` jawnie opisuje, co płynie przez pipeline. Scalanie wyników z
   równoległych gałęzi obsługują reducery — nie trzeba tego pisać ręcznie.

3. **Obserwowalność i streaming**
   `graph.stream(...)` pozwala podglądać wykonanie węzeł po węźle (co jest
   nieocenione przy długim, wieloetapowym wnioskowaniu). Graf rysuje się sam
   (mermaid), a w **LangGraph Studio** można go klikać i debugować.

4. **Trwałość i wznawianie (checkpointing)**
   Dokładając checkpointer, dostajemy zapamiętywanie stanu: wznowienie po błędzie,
   ponowienie pojedynczego węzła, „time travel", a także **human-in-the-loop**
   (przerwij → poproś radcę o akceptację etapu → kontynuuj).

5. **Sterowanie przepływem deklaratywnie**
   Pętle, warunki, ponowienia i rozgałęzienia opisuje się krawędziami grafu, a nie
   imperatywnym `if`/`for`. Łatwiej to rozszerzać (nowe węzły, podgrafy) bez
   przepisywania orkiestracji.

## Duży minus: uzależnienie od biblioteki

LangGraph to **kolejna zależność** w projekcie — i to niemała (ciągnie za sobą
sporo pakietów). Dokładając ją do `pyproject.toml`, wiążemy architekturę z konkretnym
frameworkiem: jego API, modelem stanu, cyklem wydań i ewentualnymi breaking changes.
Gdy framework zmieni interfejs albo przestanie być rozwijany, to nasz problem.

Dlatego trzymamy logikę umiejętności (`src/skills/*`) **poza** grafem — żeby to
uzależnienie dało się w razie czego odpiąć. To jeden z powodów, dla których warto
oddzielić logikę od frameworka.

Wniosek: LangGraph jest **świetny do POC** i szybkiego prototypowania (dostajesz
równoległość, Studio, checkpointing „za darmo"), ale do **systemu produkcyjnego**
warto świadomie rozważyć, czy chcemy się na nim opierać — czasem własna, lekka
orkiestracja (jak `agent_linear/`) jest tańsza w utrzymaniu niż dług zależności.

## Morał warsztatowy

Logika umiejętności (`src/skills/*`) jest **niezależna od frameworka** — dlatego
ten sam kod działa i liniowo, i w grafie. LangGraph dokładamy na końcu po to, by
zyskać równoległość, obserwowalność, trwałość i human-in-the-loop — a nie po to,
by „model pisał lepiej".

## Uruchomienie (CLI)

```bash
# generacja apelacji + ocena (pokrycie + jakość); model z .env (gpt-5.4)
uv run python -m agent_langgraph.main
```

Zapisuje apelację i log przebiegu do `agent_langgraph/output/` (jak baseline i
agent liniowy). W logu znajdziesz **koszt metody** (sama generacja, wszystkie
wywołania grafu), **czas wall-clock** (realny, przy równoległości krótszy niż suma
czasów wywołań LLM — to właśnie zysk z `Send`) oraz — osobno — koszt ewaluacji.

## Wyniki ewaluacji (`gpt-5.4`)

Te same skille i ten sam plan co `agent_linear`, więc **pokrycie i jakość wychodzą
jak u linera** (różnica jest w *sposobie* wykonania, nie w treści). Sedno tej wersji
to **czas wall-clock**: kroki `make_task` biegną równolegle, więc realny czas jest
krótszy niż suma czasów wywołań (liner: ~433 s sekwencyjnie).

| miara | wynik |
|-------|-------|
| **koszt metody** (cały graf) | _do uzupełnienia po przebiegu_ |
| **czas metody (wall-clock, równolegle)** | _do uzupełnienia_ |
| suma czasów wywołań LLM / przyspieszenie | _do uzupełnienia_ |
| **pokrycie** (zagadnienia z `data/eval.json`) | _≈ jak liner (67%)_ |
| **jakość** (średnia 2–6, sędzia `gpt-5.4`) | _≈ jak liner (4,33/6)_ |

> **TODO:** puścić `uv run python -m agent_langgraph.main` na `gpt-5.4` i wpisać
> realne liczby (zwłaszcza wall-clock vs ~433 s linera) z logu `agent_langgraph/output/run_<znacznik>.log`.

## LangGraph Studio

Graf jest wystawiony w `langgraph.json` (w korzeniu repo) jako `appeal_agent`,
wskazując na `agent_langgraph/graph.py:graph`.

```bash
uv run langgraph dev
```

Polecenie startuje lokalny serwer i otwiera **LangGraph Studio** w przeglądarce —
można tam klikać graf, podglądać stan po każdym węźle i uruchamiać przebiegi.

Wejście to tylko cel, np.:

```json
{ "goal": "Wygeneruj apelację z perspektywy obrony" }
```

Akta wczytuje sam graf — pierwszy węzeł `load` woła `load_all()` z `data/input/`,
dzięki czemu w Studio nie trzeba podawać dokumentów ręcznie. Wymaga skonfigurowanego
`.env` (klucz LLM).
