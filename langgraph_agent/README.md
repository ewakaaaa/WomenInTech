# Agent w wersji LangGraph

> Te same umiejętności (`src/skills/*`) co w `linear_agent/`, spięte w graf.
> **Wynik jest taki sam — bo to ta sama logika.** Pytanie brzmi więc: skoro
> rezultat identyczny, **co właściwie daje LangGraph?**

📊 Diagram grafu (mermaid, generowany z kodu): [`graph.md`](graph.md).

## Krótka odpowiedź

LangGraph nie zmienia *co* agent robi — zmienia *jak to jest wykonywane,
obserwowane i utrzymywane*. Wartość nie leży w treści apelacji, tylko w
inżynierii wokół niej.

## Co realnie zyskujemy (przy identycznym wyniku)

1. **Równoległość za darmo (fan-out przez `Send`)**
   W `linear_agent` opis 16 plików i wykonanie zadań idą w pętli `for` —
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
orkiestracja (jak `linear_agent/`) jest tańsza w utrzymaniu niż dług zależności.

## Morał warsztatowy

Logika umiejętności (`src/skills/*`) jest **niezależna od frameworka** — dlatego
ten sam kod działa i liniowo, i w grafie. LangGraph dokładamy na końcu po to, by
zyskać równoległość, obserwowalność, trwałość i human-in-the-loop — a nie po to,
by „model pisał lepiej".

## Uruchomienie (CLI)

```bash
uv run python -m langgraph_agent.main   # → langgraph_agent/apelacja.txt
```

## LangGraph Studio

Graf jest wystawiony w `langgraph.json` (w korzeniu repo) jako `appeal_agent`,
wskazując na `langgraph_agent/graph.py:graph`.

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
