# evaluate-blind-test

```yaml
---
task: TSK-051
execution_type: Agent
responsible: "@jarvis"
---
```

## Task Anatomy

| Field | Value |
|-------|-------|
| task_name | Evaluate Blind Test |
| status | active |
| responsible_executor | @jarvis |
| execution_type | Agent |
| input | Test results, expected patterns |
| output | Fidelity report |
| action_items | 3 |
| acceptance_criteria | Fidelity score calculated |

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| test_results | yaml | yes | Clone responses to blind test |
| expected_patterns | yaml | yes | Expected response patterns |

## Outputs

| Output | Type | Location | Description |
|--------|------|----------|-------------|
| fidelity_report | json | artifacts/validation/{clone}-fidelity.json | Fidelity score and analysis |

## Execution

### Phase 1: Compare responses to expected patterns
### Phase 2: Calculate fidelity score (0-100) per layer
### Phase 3: Generate report using core/templates/validation/fidelity-report.md

## Acceptance Criteria
- [ ] Per-layer fidelity scores calculated
- [ ] Overall fidelity score computed
- [ ] Gap analysis documented
