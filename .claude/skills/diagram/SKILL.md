---
name: diagram
description: Generate a Mermaid diagram from the codebase — architecture/module graph, entity-relationship, sequence, or flowchart — read from the actual code. Use when the user says "draw a diagram", "diagram the architecture", "generate an ER diagram", "make a sequence diagram", "visualize this flow", or "show how these pieces connect".
argument-hint: "[diagram type and subject, e.g. 'ER diagram of the models' or 'sequence for the login flow']"
allowed-tools: Bash, Read, Grep, Glob
disable-model-invocation: false
---

## Project layout

!`ls 2>/dev/null`

!`git ls-files 2>/dev/null | grep -vE '\.(png|jpg|svg|lock|min\.)' | head -40 || find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -40`

## Instructions

Generate a Mermaid diagram for what the user described in `$ARGUMENTS`. If the type or subject is unclear, pick the most useful diagram for the request and say why; ask only if you genuinely can't tell what to draw.

### Choose the diagram type

- **Architecture / module graph** (`graph TD`/`flowchart`) — how top-level components, services, or modules depend on each other. Default when the user says "architecture" or "how it connects".
- **Entity-relationship** (`erDiagram`) — data models/tables and their relationships, with key fields and cardinality. Use for "ER diagram", "schema", "models".
- **Sequence** (`sequenceDiagram`) — the ordered interaction between participants for a specific flow (request → handler → service → db). Use for "sequence" or "the X flow".
- **Flowchart / state** — branching logic or a state machine within a function or feature.

### Method

1. **Read the real code** for the chosen subject — module imports/dependencies, schema/model definitions, or the call chain of the named flow. Trace actual relationships; don't draw an idealized architecture.
2. **Build the Mermaid source.** Use clear node labels taken from real names (modules, classes, tables, endpoints). For ER diagrams, include primary/foreign keys and cardinality (`||--o{`). For sequence diagrams, order the calls as they actually execute and include returns where meaningful.
3. **Keep it legible.** Group or collapse detail when a full graph would be unreadable — show the meaningful structure, not every file. Note what you abstracted.
4. **Output a fenced ```mermaid block** so it renders. If the user wants it persisted, offer to write it into the README or a `docs/` file rather than assuming.

### Rules

1. Diagram what the code actually does — every node and edge must trace to a real module, model, or call. Don't invent components or relationships.
2. Mark anything inferred or uncertain (e.g. a dynamically-resolved dependency) rather than drawing it as fact.
3. Keep the Mermaid syntax valid and minimal; prefer a readable subset over an exhaustive but unreadable graph.
4. Don't write files unless asked — output the diagram inline first, then offer to save it.
5. Briefly explain the diagram after it: what the main nodes are and how to read the key relationships.
