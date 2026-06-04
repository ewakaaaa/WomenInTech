# Graf planera (agent nieliniowy)

Diagram generowany z kodu (`graph.get_graph().draw_mermaid()`, zob. `graph.py`).

```mermaid
graph TD;
	__start__([<p>__start__</p>]):::first
	load(load)
	file_description(file_description)
	planner(planner)
	make_task(make_task)
	human(human)
	document(document)
	conclude(conclude)
	__end__([<p>__end__</p>]):::last
	__start__ --> load;
	file_description --> planner;
	human --> planner;
	load -.-> file_description;
	make_task --> planner;
	planner -.-> conclude;
	planner -.-> document;
	planner -.-> human;
	planner -.-> make_task;
	conclude --> __end__;
	document --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

**Planer jest centrum** — wszystko do niego wraca i to on decyduje, co dalej:
- `analyze` → `make_task` (fan-out po zadaniach) → z powrotem do `planner`,
- `ask_human` → `human` (pauza `interrupt`, czeka na radcę) → z powrotem do `planner`,
- `write` → `document` → koniec,
- `no_grounds` → `conclude` → koniec.

Pętle `make_task → planner` i `human → planner` to istota **nieliniowości** —
graf może zawracać, dopóki planer nie uzna, że ma dość (bezpiecznik: max rund).
