---
name: dual-mode
description: Dual clone comparison mode. Activates two clones side by side to compare perspectives on the same question.
---

> **Auto-Trigger:** When user wants to compare two clones' perspectives on the same topic
> **Keywords:** "dual mode", "comparar clones", "dois clones", "side by side"
> **Prioridade:** MEDIA
> **Tools:** Read, Grep, Glob

## Overview

Activates two mind clones simultaneously to provide side-by-side comparison of their perspectives on a given question or topic. Each clone responds independently using its own DNA, then differences and convergences are highlighted.

## References

- `core/protocols/clone-activation.md` - Activation protocol for loading clone identity

## Quando Ativar

- User wants to compare two specific persons' views
- User mentions "dual mode", "comparar clones", "side by side", or "dois clones"
- When a decision benefits from two expert perspectives
- User names two persons and asks for their take on something

## Quando NAO Ativar

- Single clone emulation (use /emulate)
- Three or more clones in discussion (use /roundtable)
- Clone creation, update, or validation workflows
- General knowledge queries not requiring comparison

## Workflow

1. **Identify Both Clones** - Resolve two person names to clone directories
2. **Load Clone A** - Full cognitive stack (SOUL, MEMORY, DNA)
3. **Load Clone B** - Full cognitive stack (SOUL, MEMORY, DNA)
4. **Present Question** - Same question to both clones
5. **Collect Responses** - Each clone responds independently using its DNA
6. **Compare** - Highlight convergences, divergences, and unique insights

## Output Format

```
[CLONE A - {Person A}]
{Response using A's DNA and voice}

[CLONE B - {Person B}]
{Response using B's DNA and voice}

[COMPARISON]
Convergences: [where they agree]
Divergences: [where they differ and why]
Unique insights: [what each brings that the other doesn't]
```
