# Prezentacja — plan warsztatu

> **Czy AI może napisać dobrą apelację? Case study systemu, który zdałby egzamin radcowski.**
> Format: 70 min, case study + live demo. Perspektywy Women in Tech Summit.

Tu trzymamy materiały do prezentacji (slajdy, notatki) i poniższy plan.

## Teza

AI potrafi napisać apelację na poziomie egzaminu radcowskiego — **ale tylko przy
odpowiedniej architekturze**. Sam prompt „napisz apelację" nie wystarczy; potrzebny
jest wieloetapowy agent **i** człowiek weryfikujący każdy etap.

## Plan slajd po slajdzie

> ⏱️ Czasy orientacyjne. **Treść** (slajdy 1–22) ≈ **~58 min**, na końcu **10–15 min na
> pytania** → ~68–73 min — napięte. Jak braknie czasu, najłatwiej skrócić demo na żywo:
> kod (17) i graf nieliniowy (21).

### Wstęp i kontekst — *~10 min*

1. **Przywitanie.** — *1 min*
2. **Agenda.** *(uzupełnimy na końcu)* — *1 min*
3. **Kim jestem.** Matematyczka → data scientist w COI. Najbardziej kojarzalna z
   chatbotem w mObywatelu, ale głównie pracuję w mniej widocznej działce prawnej.
   Na studiach nie wyobrażałam sobie siebie jako programistki — a teraz pokazuję
   publicznie swoje repo. *(„nigdy nie mów nigdy")* — *2 min*
4. **Repo na żywo.** Link do repozytorium — „jestem na konferencji i pokazuję wam
   swój kod". Zaproszenie: pobierzcie projekt i odpalajcie / patrzcie razem ze mną. — *2 min*
5. **Cel i motywacja.** Chcemy mieć **generator dokumentów** (pism prawniczych). — *1 min*
6. **Dane.** Udało się znaleźć świetne dane, bo: a) są **zanonimizowane**,
   b) mają **klucz odpowiedzi** → możemy *mierzyć* jakość, nie tylko „patrzeć, że ładne".
   Przybliżenie sprawy: **sprawa Daniela Dzika** — o co w niej chodzi (zob.
   [`data/README.md`](../data/README.md)). — *3 min*

### Baseline i jego problemy — *~10 min*

7. **Baseline + wyniki.** Warto zacząć od czegoś prostego — mamy punkt startowy.
   Pokaż wygenerowaną apelację + wynik ewaluacji `X/12` + niepokryte zagadnienia.
   Pointa: **„technicznie działa, ale czy *dobrze*?"** — *4 min*
8. **Pytanie do sali:** jakie widzicie z tym problemy? *(odpowiedzi złożą się w listę
   ograniczeń: zapchany kontekst, wszystko naraz, brak audytu, halucynacje…)* — *4 min*
9. **Eksperci domenowi.** Jak ważni są eksperci domenowi — i **jak człowiek
   podszedłby do tego zadania?** *(zawias do architektury)* — *2 min*

### Jak zrobiłby to człowiek (intuicja, bez kodu) — *~8 min*

10. **Plan jak człowiek (1):** najpierw pobieżnie przeglądasz, jakie masz dokumenty
    *(slajd: biurko z papierami)* i zapisujesz **główny cel** — „napisać apelację".
    *(wzmianka: na egzaminie zadaniem jest też ocena, czy apelacja ma podstawy — na
    warsztacie upraszczamy do jednego celu.)* — *1,5 min*
11. **Plan jak człowiek (2):** skoro wiem mniej więcej, co mam w papierach, zastanawiam
    się, **co trzeba sprawdzić** — np. przeczytać wszystkie zeznania i poszukać
    nieścisłości. Powstaje **lista TODO**. — *1,5 min*
12. **Plan jak człowiek (3):** realizuję rzeczy z listy TODO i **spisuję wnioski**. — *1,5 min*
13. **Plan jak człowiek (4):** happy path — przechodzę do **podsumowania i obmyślenia
    strategii** pisania apelacji. — *1,5 min*
14. **Plan jak człowiek (5):** skoro wiem, co chcę napisać — **piszę apelację**. — *1,5 min*

### Reveal, oddech i kod — *~13 min*

15. **Reveal: to jest dokładnie nasz agent.** Mapowanie kroków człowieka na umiejętności: — *2 min*

    | człowiek | umiejętność |
    |----------|-------------|
    | przegląda papiery, notuje co ważne | `generate_file_description` |
    | robi listę TODO, co sprawdzić | `generate_tasks` |
    | realizuje TODO, spisuje wnioski | `make_task` |
    | podsumowuje, obmyśla strategię | `generate_strategy` |
    | pisze apelację | `generate_document` |

16. **🫁 Oddech — anegdota.** Przed gęstą częścią techniczną: ostatnio ktoś zapytał
    mnie o top-3 rzeczy, które powinien umieć data scientist *(skren z LinkedIna)*.
    Jedna z nich — odróżniająca mida od seniora — to to, że senior nie tylko zrobi
    zadanie, ale **zaplanuje całe rozwiązanie**. *(I to właśnie przed chwilą zrobiliśmy.)* — *2 min*
17. **Kod na żywo:** `notebooks/baseline_walkthrough.ipynb` — odpalamy umiejętności po kolei i
    oglądamy outputy każdego etapu. Przy okazji pokazujemy, jak agent **rozwiązuje
    problemy ze slajdu 8**: — *9 min*
    - **podsumowania zamiast pełnych akt** → mniej tokenów (opisy plików, nie 16 pełnych dokumentów),
    - **analiza wybranych dokumentów**, a nie wszystkich naraz → selektywny kontekst (model widzi tylko trafny wycinek),
    - **rozbicie dużego zadania na małe kawałki** → łatwiej i dokładniej, każdy krok robi jedno,
    - **przekazywanie głównego celu** (`goal`) przez wszystkie etapy → swego rodzaju **pamięć agenta**, dzięki której nie gubi kierunku.

### Jak to się spina i wyniki — *~6 min*

18. **Structured output — klej całego pipeline'u.** Bez tego nie dałoby się spiąć
    umiejętności w jeden przepływ. Nie ma tu żadnej magii — po prostu **polegamy** na
    tym, że każda umiejętność zwraca **typowany obiekt** (Pydantic), więc dokładnie
    wiem, jakiego outputu się spodziewać i mogę go podać dalej. Bez structured output
    te kroki by się nie połączyły. — *3 min*
19. **Pokazujemy wyniki** — apelacja agenta + porównanie z baseline
    (`uv run python -m src.eval.compare`): pokrycie `Y/12` vs `X/12`. — *3 min*

### LangGraph, graf nieliniowy i puenta — *~12 min*

20. **LangGraph — co wnosi, toole i koszt.** Mamy logikę **napisaną czystymi
    funkcjami**, więc łatwo ją opakować w węzły — ta sama logika, tylko jako graf.
    Co dostajemy w zamian: — *~5 min*
    - **wspólny State przenoszony między krokami** — jawny i czysty,
    - **równoległość (fan-out `Send`)** — opisy plików i wykonanie zadań liczą się
      **współbieżnie**, podczas gdy w `agent_linear` były to sekwencyjne pętle `for`
      → to samo, ale szybciej,
    - **diagram grafu z kodu** — LangGraph rysuje graf w **mermaid** automatycznie
      (`graph.get_graph().draw_mermaid()`), więc obrazek na slajd robi się sam,
    - **toole** — agentowi można dać narzędzia (function calling): model sam decyduje,
      którego użyć. U nas planer decyduje o akcjach i tworzy zadania — ten sam pomysł,
      zrealizowany przez **structured output** (bez formalnych tooli); LangGraph spina
      toole bez wysiłku, gdyby były potrzebne,
    - **łatwy human-in-the-loop** — możemy wstawić pauzę, np. na **potwierdzenie strategii
      przez radcę**, zanim agent napisze pismo → dokładnie to, czego potrzebujemy.
    - **⚠️ Przestroga:** to kolejna, niemała **zależność** (dług) — świetne do POC, na
      produkcji rozważ świadomie.
21. **Graf nieliniowy: agent z planerem + wynik.** Dotąd graf był liniowy (to samo, co
    pipeline). Teraz **`agent_planner`** — planer w centrum **sam decyduje** (analizuj /
    zapytaj człowieka / pisz / brak podstaw), więc graf **zawraca w pętli**. — *~4 min*
    - pokaż **diagram** (nieliniowy, „hub" — `agent_planner/graph.md`),
    - **human-in-the-loop na żywo** (`notebooks/planner_walkthrough.ipynb`): planer pauzuje,
      pyta mnie (radcę) o potwierdzenie — wpisuję decyzję, graf leci dalej,
    - pokaż **wynik** + ewaluację (`uv run python -m src.eval.compare`),
    - puenta: **tego nie zrobisz liniowym pipeline'em** — cykle + człowiek w pętli.
22. **Take-awaye.** Wracamy do **anegdoty o top-3 umiejętnościach DS** — pierwszą
    (zaplanowanie całego rozwiązania) właśnie zobaczyliśmy w praktyce. Kluczowe przekazy
    (poniżej), w tym przestroga: **nie zaczynaj od nauki frameworka ani od razu od
    złożonego agenta** — zacznij od logiki i baseline, a LangGraph/agenta dokładaj
    świadomie na końcu. — *~3 min*

### Pytania (Q&A) — *10–15 min*

Zarezerwowane na sam koniec. *(Agendę ze slajdu 2 uzupełniamy na końcu — pamiętać,
żeby zapowiedzieć, że pytania zbieramy na finał.)*

## Demo — checklista

- [ ] `.env` z działającym kluczem LLM (zapasowy backend: Ollama / proxy)
- [ ] Wygenerowane apelacje w `baseline/`, `agent_linear/`, `agent_langgraph/` (na wypadek braku sieci)
- [ ] Wyniki `uv run python -m src.eval.compare` zrzucone do slajdu (plan B bez live)
- [ ] `uv run jupyter lab` — sprawdzone `notebooks/baseline_walkthrough.ipynb` i `notebooks/planner_walkthrough.ipynb`
- [ ] Diagram grafu nieliniowego (`agent_planner/graph.md`) + przećwiczone demo human-in-the-loop
- [ ] Diagram grafu (mermaid z `agent_langgraph`)
- [ ] *(opcjonalnie)* `uv run langgraph dev` — Studio jako bonus, jeśli zostanie czas
- [ ] Skren z LinkedIna (slajd 16 — oddech/anegdota)

## Kluczowe przekazy (take-aways)

1. Architektura > pojedynczy prompt — margines błędu zero wymusza etapowość.
2. **Selektywny kontekst** zamiast wrzucania wszystkiego (bez chunkowania/wektorów).
3. Logika umiejętności **niezależna od frameworka** — to samo działa liniowo i w grafie.
4. LangGraph daje równoległość/obserwowalność/Studio, ale to dług zależności.
5. **Człowiek w pętli** jest częścią systemu, nie dodatkiem.
6. **Nie zaczynaj od frameworka** ani od razu od złożonego agenta — najpierw logika
   i baseline, framework dokładaj świadomie na końcu (inaczej uczysz się narzędzia
   zamiast rozwiązywać problem).
7. Callback do anegdoty: **planowanie całego rozwiązania** (mid → senior) to jedna z
   top-3 umiejętności DS — i właśnie ją dziś przećwiczyliśmy.

## Do uzupełnienia

- [ ] Realne liczby do tabeli wyników (po uruchomieniu na żywo)
- [ ] Slajdy
