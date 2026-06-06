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
ten sam kod działa i liniowo, i w grafie. LangGraph dokładamy na końcu po to, by
zyskać równoległość, obserwowalność, trwałość i human-in-the-loop — a nie po to,
by „model pisał lepiej".

## Uruchomienie (CLI)

```bash
# sama generacja (BEZ oceny); model z .env (gpt-5.4)
uv run python -m agent_langgraph.main
```

Zapisuje apelację i log przebiegu do `agent_langgraph/output/` (jak baseline i
agent liniowy). Świadomie **bez ewaluacji** — pokrycie i jakość są jak u linera
(ta sama logika), więc tu interesują nas tylko dwie rzeczy:

- **czas wall-clock** — realny czas przy równoległym fan-oucie; powinien być
  wyraźnie krótszy niż suma czasów wywołań LLM (zysk z `Send`),
- **koszt metody** — sprawdzamy, czy LangGraph go **nie podbija**. Z założenia ma
  wyjść jak u linera (~$0,743): te same skille, te same wywołania, opisy z cache —
  fan-out zmienia tylko kolejność, nie liczbę wywołań. Większy koszt = sygnał, że
  graf gdzieś dubluje wywołania.

## Wyniki (`gpt-5.4`)

Te same skille i ten sam plan co `agent_linear`, więc **pokrycie i jakość są jak
u linera** (67% / 4,33) — tu ich nie liczymy ponownie. Mierzymy czas i koszt.

Przebieg 2026-06-06 (`gpt-5.4`, 12 wywołań):

| miara | wynik | liner (sekwencyjnie) |
|-------|-------|----------------------|
| **czas metody (wall-clock, równolegle)** | **169,8 s** (~2,8 min) | 433,5 s |
| suma czasów wywołań LLM / przyspieszenie | 442,3 s → **≈2,6×** | — |
| **koszt metody** (cały graf) | **$0,7349** (88 188 wej + 34 292 wyj tok) | ~$0,743 |
| pokrycie / jakość | _≈ liner: 67% / 4,33 (nie liczone ponownie)_ | 67% / 4,33 |

Puenta: **koszt taki sam jak liner** (~$0,74 — fan-out nie podbija liczby wywołań),
a realny czas **≈2,6× krótszy** dzięki równoległości. Pełny log:
`agent_langgraph/output/run_<znacznik>.log`.
