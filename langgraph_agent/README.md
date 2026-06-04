# Agent w wersji LangGraph

> Te same umiejętności (`src/skills/*`) co w `linear_agent/`, spięte w graf.
> **Wynik jest taki sam — bo to ta sama logika.** Pytanie brzmi więc: skoro
> rezultat identyczny, **co właściwie daje LangGraph?**

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

## Morał warsztatowy

Logika umiejętności (`src/skills/*`) jest **niezależna od frameworka** — dlatego
ten sam kod działa i liniowo, i w grafie. LangGraph dokładamy na końcu po to, by
zyskać równoległość, obserwowalność, trwałość i human-in-the-loop — a nie po to,
by „model pisał lepiej".

## Uruchomienie

```bash
uv run python -m langgraph_agent.main   # → langgraph_agent/apelacja.txt
```
