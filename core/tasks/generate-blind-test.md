# generate-blind-test

```yaml
---
task: TSK-050
execution_type: Agent
responsible: "@jarvis"
---
```

## Task Anatomy

| Field | Value |
|-------|-------|
| task_name | Generate Blind Test |
| status | active |
| responsible_executor | @jarvis |
| execution_type | Agent |
| input | Clone identifier, test count |
| output | Blind test scenarios |
| action_items | 3 |
| acceptance_criteria | Scenarios cover all 5 DNA layers |

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| clone_id | string | yes | Clone source code or name |
| test_count | number | no | Number of scenarios (default: 10) |

## Outputs

| Output | Type | Location | Description |
|--------|------|----------|-------------|
| test_scenarios | yaml | artifacts/validation/{clone}-blind-test.yaml | Test scenarios |

## Execution

### Phase 1: Clone Analysis
1. Load clone DNA-CONFIG.yaml
2. Extract key elements from each DNA layer
3. Identify distinctive decision patterns from MEMORY.md

### Phase 2: Scenario Generation
1. Generate scenarios testing each DNA layer
2. Create expected response patterns
3. Include distractor scenarios (outside clone's domain)

### Phase 3: Template Output
1. Format using core/templates/validation/blind-test-template.yaml
2. Save to artifacts/validation/

## Acceptance Criteria
- [ ] Min 2 scenarios per DNA layer
- [ ] Distractor scenarios included
- [ ] Expected patterns documented
