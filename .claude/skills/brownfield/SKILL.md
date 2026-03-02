---
name: brownfield
description: Brownfield pipeline for incremental clone updates. Processes new material into an existing clone without full rebuild.
---

> **Auto-Trigger:** When new material arrives for an existing clone that needs incremental update
> **Keywords:** "brownfield", "incremental", "update clone", "atualizar clone", "delta"
> **Prioridade:** MEDIA
> **Tools:** Read, Grep, Glob, Write, Edit, Bash

## Overview

Handles incremental updates to existing clones when new source material becomes available. Detects deltas between existing DNA and new content, processes only the differences, and merges updates without destroying existing knowledge.

## References

- `core/protocols/brownfield-detection.md` - Delta detection and merge protocol
- `core/workflows/wf-brownfield-update.yaml` - Workflow definition for incremental updates

## Quando Ativar

- New material arrives for a person who already has a clone
- User mentions "brownfield", "incremental", "update clone", or "delta"
- When updating an existing clone with additional sources
- After ingesting new content for a known person

## Quando NAO Ativar

- First-time clone creation (use full greenfield pipeline)
- Clone emulation or activation (use /emulate)
- Quality validation (use /blind-test)
- Unrelated pipeline processing for new persons

## Workflow

1. **Detect Existing Clone** - Identify current DNA state and processed sources
2. **Compute Delta** - Compare new material against already-processed sources
3. **Process Delta Only** - Run pipeline on new material only
4. **Merge Results** - Integrate new DNA elements into existing layers
5. **Validate Integrity** - Ensure no existing knowledge was corrupted
6. **Update Version** - Increment clone version and update metadata

## Delta Types

- **New Source** - Entirely new material from the same person
- **Updated Source** - Revised version of previously processed material
- **Cross-Reference** - New material that enriches existing themes
