# Graf agenta (LangGraph)

Diagram generuje się automatycznie z kodu:
`graph.get_graph().draw_mermaid()` (zob. `graph.py`).

```mermaid
graph TD;
	__start__([<p>__start__</p>]):::first
	load(load)
	generate_file_description(generate_file_description)
	generate_tasks(generate_tasks)
	make_task(make_task)
	generate_strategy(generate_strategy)
	generate_document(generate_document)
	__end__([<p>__end__</p>]):::last
	__start__ --> load;
	generate_file_description --> generate_tasks;
	generate_strategy --> generate_document;
	generate_tasks -.-> make_task;
	load -.-> generate_file_description;
	make_task --> generate_strategy;
	generate_document --> __end__;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

Przerywane strzałki (`-.->`) to krawędzie warunkowe z fan-outem przez `Send`:
- `__start__ → load` wczytuje akta,
- `load -.-> generate_file_description` — jedna gałąź na każdy dokument (równolegle),
- `generate_tasks -.-> make_task` — jedna gałąź na każde zadanie (równolegle).
