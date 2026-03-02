---
name: mind-map
description: Cognitive mind mapping from DNA. Generates visual knowledge graphs from a clone's cognitive layers.
---

> **Auto-Trigger:** When user wants to visualize a clone's knowledge structure as a mind map or graph
> **Keywords:** "mind map", "mapa mental", "mapa cognitivo", "grafo", "graph"
> **Prioridade:** MEDIA
> **Tools:** Read, Grep, Glob, Write, Bash

## Overview

Generates cognitive mind maps from a clone's DNA layers. Visualizes the relationships between philosophies, mental models, heuristics, frameworks, and methodologies as an interconnected knowledge graph. Outputs structured data that can be rendered visually.

## References

- `core/protocols/mind-mapping.md` - Mind mapping protocol and node taxonomy
- `core/schemas/mind-map.schema.json` - JSON schema for mind map data structure
- `core/workflows/wf-mind-mapper.yaml` - Workflow definition for map generation

## Tasks

- **TSK-090** - Generate cognitive mind map from DNA

## Quando Ativar

- User wants to visualize a clone's knowledge structure
- User mentions "mind map", "mapa mental", "mapa cognitivo", or "grafo"
- When exploring connections between DNA elements
- For presentations or documentation of clone knowledge

## Quando NAO Ativar

- Clone emulation or activation (use /emulate)
- DNA extraction or pipeline processing
- Simple DNA viewing (use /view-dna)
- Prompt compilation (use /compile-prompt)

## Workflow

1. **Select Clone** - Identify target clone and DNA directory
2. **Load DNA Layers** - All 5 cognitive layers
3. **Extract Nodes** - Each DNA element becomes a node with type and metadata
4. **Map Edges** - Identify relationships (supports, contradicts, extends, applies)
5. **Generate Output** - Produce mind map per `mind-map.schema.json`
6. **Render** - Output as structured JSON, Mermaid diagram, or ASCII visualization

## Node Types

- **Philosophy** - Core belief (root level)
- **Mental Model** - Thinking framework (second level)
- **Heuristic** - Decision rule (third level)
- **Framework** - Structured methodology (fourth level)
- **Methodology** - Step-by-step process (leaf level)

## Edge Types

- `supports` - One element reinforces another
- `contradicts` - Elements in tension
- `extends` - One builds on another
- `applies` - Concrete application of abstract concept
