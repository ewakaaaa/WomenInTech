# Agent w wersji LangGraph

> Te same umiejętności (`src/skills/*`) co w `agent_linear/`, spięte w graf.
> **To ta sama logika** — więc o jakość pisma tu nie chodzi. Pytanie brzmi:
> skoro podejście jest to samo, **co właściwie daje LangGraph?** Krótko: nie zmienia
> *co* agent robi, tylko **jak szybko** to liczy (przy tym samym koszcie).
>
> ⚠️ Dlatego **pokrycia i jakości nie raportujemy tutaj** — mierzymy je na
> `agent_linear/`  

📊 Diagram grafu (mermaid, generowany z kodu): [`graph.md`](graph.md).

## Krótka odpowiedź

LangGraph nie zmienia *co* agent robi — zmienia *jak to jest wykonywane,
obserwowane i utrzymywane*. Wartość nie leży w treści apelacji, tylko w
inżynierii wokół niej.

## Co realnie zyskujemy (przy tej samej logice)

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
   (mermaid) — obrazek na slajd robi się z kodu.

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
równoległość i checkpointing „za darmo"), ale do **systemu produkcyjnego**
warto świadomie rozważyć, czy chcemy się na nim opierać — czasem własna, lekka
orkiestracja (jak `agent_linear/`) jest tańsza w utrzymaniu niż dług zależności.

## Morał warsztatowy

Logika umiejętności (`src/skills/*`) jest **niezależna od frameworka** — dlatego
ten sam kod działa i liniowo, i w grafie.

## Uruchomienie (CLI)

```bash
uv run python -m agent_langgraph.main
```

## Wyniki — tylko czas i koszt (`gpt-5.4`)

| miara | wynik | liner (sekwencyjnie) |
|-------|-------|----------------------|
| **czas metody (wall-clock, równolegle)** | **169,8 s** (~2,8 min) | 433,5 s |
| suma czasów wywołań LLM / przyspieszenie | 442,3 s → **≈2,6×** | — |
| **koszt metody** (cały graf) | **$0,7349** (88 188 wej + 34 292 wyj tok) | ~$0,743 |

Puenta: **koszt taki sam jak liner** (~$0,74 — fan-out nie podbija liczby wywołań),
a realny czas **≈2,6× krótszy** dzięki równoległości.
