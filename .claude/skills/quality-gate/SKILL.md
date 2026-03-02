---
name: quality-gate
description: Quality gate enforcement during pipeline processing. Validates checkpoints before advancing phases.
---

> **Auto-Trigger:** When pipeline processing hits a checkpoint or gate validation is needed
> **Keywords:** "quality gate", "checkpoint", "gate", "aprovacao", "QG-"
> **Prioridade:** ALTA
> **Tools:** Read, Grep, Glob, Bash

## Overview

Enforces the 9-checkpoint quality gate system during pipeline processing. Each gate (QG-001 through QG-009) must pass before the pipeline advances to the next stage. Validates output against schema, checks completeness, and blocks advancement when criteria are not met.

## References

- `core/protocols/quality-gates-9-checkpoints.md` - Full protocol with all 9 gates
- `core/schemas/quality-gate.schema.json` - JSON schema for gate validation records

## Quando Ativar

- Pipeline processing reaches a stage boundary
- User mentions "quality gate", "checkpoint", or "QG-" prefix
- Before advancing from one pipeline phase to the next
- When validating batch output quality
- When user requests gate status or approval

## Quando NAO Ativar

- General conversation not related to pipeline processing
- Simple file reads or edits unrelated to gates
- Knowledge extraction without pipeline context
- Agent creation or DNA work (use respective skills)

## Workflow

1. **Identify Gate** - Determine which QG checkpoint applies (QG-001 through QG-009)
2. **Load Protocol** - Read `core/protocols/quality-gates-9-checkpoints.md` for gate criteria
3. **Validate Output** - Check artifacts against `core/schemas/quality-gate.schema.json`
4. **Report Result** - PASS (advance), WARN (advance with notes), or FAIL (block)
5. **Log Decision** - Record gate result with timestamp and artifacts checked

## Gate Result Format

```
QG-{NNN}: {PASS|WARN|FAIL}
Artifacts checked: [list]
Criteria met: X/Y
Notes: [details if WARN or FAIL]
```
