---
name: blind-test
description: Blind testing for clone fidelity validation. Measures how accurately a clone reproduces the original person's thinking.
---

> **Auto-Trigger:** When clone fidelity needs validation or blind test is requested
> **Keywords:** "blind test", "fidelity", "validacao clone", "teste cego"
> **Prioridade:** MEDIA
> **Tools:** Read, Grep, Glob, Write, Bash

## Overview

Executes blind fidelity tests to validate how accurately a mind clone reproduces the original person's reasoning, vocabulary, and decision patterns. Generates test prompts, collects clone responses, and evaluates against known source material.

## References

- `core/protocols/blind-testing-protocol.md` - Full blind test protocol
- `core/schemas/fidelity-report.schema.json` - Schema for fidelity reports
- `core/templates/validation/` - Validation templates and rubrics

## Tasks

- **TSK-050** `generate-blind-test` - Generate blind test prompts from source material
- **TSK-051** `evaluate-blind-test` - Evaluate clone responses against ground truth

## Quando Ativar

- User requests clone fidelity validation
- After completing a new clone or major clone update
- When user mentions "blind test", "teste cego", or "fidelity"
- During quality assurance of clone output
- Before deploying a clone to production use

## Quando NAO Ativar

- Normal clone emulation sessions (use /emulate)
- DNA extraction or pipeline processing
- General knowledge queries
- Roundtable or debate sessions (use respective skills)

## Workflow

1. **Select Source** - Identify clone and source material for ground truth
2. **Generate Prompts** - Run TSK-050 to create blind test questions
3. **Collect Responses** - Get clone responses without revealing expected answers
4. **Evaluate** - Run TSK-051 to score against ground truth
5. **Report** - Generate fidelity report per `fidelity-report.schema.json`

## Fidelity Dimensions

- **Voice Match** - Vocabulary, tone, speech patterns
- **Reasoning Match** - Decision logic, framework application
- **Knowledge Match** - Facts, numbers, heuristics accuracy
- **Philosophy Match** - Core beliefs and worldview alignment
