---
name: compile-prompt
description: Compile DNA into a deployable system prompt. Transforms extracted knowledge into a standalone prompt for external use.
---

> **Auto-Trigger:** When user wants to generate a deployable system prompt from a clone's DNA
> **Keywords:** "compile prompt", "compilar prompt", "system prompt", "gerar prompt"
> **Prioridade:** MEDIA
> **Tools:** Read, Grep, Glob, Write

## Overview

Compiles a clone's full DNA (5 cognitive layers, SOUL, MEMORY) into a standalone system prompt that can be deployed in external LLM applications. Supports generalist and specialist prompt templates with configurable communication patterns.

## References

- `core/protocols/prompt-compilation.md` - Compilation protocol and rules
- `core/templates/agents/system-prompt-generalista.md` - Generalist prompt template
- `core/templates/agents/system-prompt-specialist.md` - Specialist prompt template
- `core/templates/agents/communication-patterns.yaml` - Voice and communication config

## Tasks

- **TSK-080** - Compile DNA into deployable system prompt

## Quando Ativar

- User wants to export a clone as a system prompt
- User mentions "compile prompt", "system prompt", or "gerar prompt"
- When deploying a clone to an external platform (GPT, API, chatbot)
- After clone is validated and ready for production use

## Quando NAO Ativar

- Clone emulation within Mega Brain (use /emulate)
- DNA extraction or pipeline processing
- Clone validation or blind testing (use /blind-test)
- Internal agent creation (use /create-agent)

## Workflow

1. **Select Clone** - Identify target clone and its DNA directory
2. **Choose Template** - Generalist or specialist based on use case
3. **Load DNA Layers** - All 5 layers (philosophies through methodologies)
4. **Load Communication Patterns** - Voice, tone, vocabulary from SOUL
5. **Compile** - Merge into template following `prompt-compilation.md` rules
6. **Output** - Generate standalone system prompt file

## Output Formats

- **Markdown** - For documentation and manual deployment
- **Plain text** - For direct paste into LLM system prompt fields
- **JSON** - For API-based deployment with structured metadata
