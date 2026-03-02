# compile-system-prompt

```yaml
---
task: TSK-080
execution_type: Agent
responsible: "@jarvis"
---
```

## Task Anatomy

| Field | Value |
|-------|-------|
| task_name | Compile System Prompt |
| status | active |
| responsible_executor | @jarvis |
| execution_type | Agent |
| input | DNA-CONFIG.yaml, clone type |
| output | Deployable system prompt |
| action_items | 4 |
| acceptance_criteria | Prompt compiles, all DNA layers included |

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| source_code | string | yes | Clone source code |
| clone_type | enum | no | generalist or specialist (default: specialist) |

## Outputs

| Output | Type | Location | Description |
|--------|------|----------|-------------|
| system_prompt | md | agents/persons/{source}/SYSTEM-PROMPT.md | Compiled prompt |
| comm_patterns | yaml | agents/persons/{source}/COMM-PATTERNS.yaml | Communication patterns |

## Execution

### Phase 1: Load DNA and SOUL
1. Read DNA-CONFIG.yaml for source references
2. Load SOUL.md for voice and identity
3. Load MEMORY.md for experiential knowledge

### Phase 2: Select Template
1. If generalist: use core/templates/agents/system-prompt-generalista.md
2. If specialist: use core/templates/agents/system-prompt-specialist.md

### Phase 3: Apply Communication Patterns
1. Load core/templates/agents/communication-patterns.yaml
2. Map DNA elements to communication style
3. Generate clone-specific patterns

### Phase 4: Compile and Output
1. Fill template with DNA, SOUL, MEMORY data
2. Apply communication patterns
3. Save compiled prompt

## Acceptance Criteria
- [ ] All 5 DNA layers represented in prompt
- [ ] Voice patterns from SOUL.md preserved
- [ ] Communication patterns applied
- [ ] Prompt is self-contained (no external refs needed at runtime)

## Handoff
| Next Task | Trigger | Data Passed |
|-----------|---------|-------------|
| (terminal) | - | system_prompt path |
