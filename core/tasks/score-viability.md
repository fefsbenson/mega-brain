# score-viability

```yaml
---
task: TSK-012
execution_type: Agent
responsible: "@jarvis"
---
```

## Task Anatomy

| Field | Value |
|-------|-------|
| task_name | Score Viability (APEX) |
| status | active |
| responsible_executor | @jarvis |
| execution_type | Agent |
| input | Source files to evaluate |
| output | Viability report with APEX score |
| action_items | 4 |
| acceptance_criteria | Score calculated, verdict assigned |

---

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| source_code | string | yes | Source identifier (e.g., CG, JM) |
| files | array | yes | List of files to evaluate |
| threshold | number | no | Minimum score to proceed (default: 60) |

---

## Outputs

| Output | Type | Location | Description |
|--------|------|----------|-------------|
| viability_report | yaml | `artifacts/triage/{source_code}-viability.yaml` | Structured APEX score |
| verdict | enum | - | HIGH, MODERATE, LOW, REJECT |
| selected_files | array | - | Files that pass threshold (for selective processing) |

---

## Execution

### Phase 1: Material Scan
**Quality Gate:** QG-TRIAGE-001

1. Load all source files from input
2. Identify file types (transcript, PDF, video notes)
3. Estimate total content volume (word count, duration)
4. Check for duplicates against existing knowledge base

### Phase 2: APEX Scoring
**Quality Gate:** QG-TRIAGE-002

1. Score Authenticity (0-100): originality, first-person content, unique voice
2. Score Practicality (0-100): frameworks, methodologies, actionable steps
3. Score Expertise (0-100): domain depth, specific metrics, case studies
4. Score X-factor (0-100): novel insights, contrarian views, memorable concepts
5. Calculate weighted average: A(25%) + P(30%) + E(25%) + X(20%)

### Phase 3: Verdict Assignment
**Quality Gate:** QG-TRIAGE-003

1. Map score to verdict (HIGH/MODERATE/LOW/REJECT)
2. For MODERATE: identify best files for selective processing
3. For LOW: identify only key insights worth extracting
4. Generate recommendation with reasoning

### Phase 4: Report Generation
**Quality Gate:** QG-TRIAGE-004

1. Generate viability report using `core/templates/assessment/viability-report.yaml`
2. Save to `artifacts/triage/`
3. Log decision in session

---

## Acceptance Criteria

- [ ] All 4 APEX dimensions scored independently
- [ ] Weighted average calculated correctly
- [ ] Verdict matches score range
- [ ] Report saved to artifacts/triage/
- [ ] Selective file list generated for MODERATE verdicts

---

## Handoff

| Next Task | Trigger | Data Passed |
|-----------|---------|-------------|
| normalize-entities (TSK-002) | verdict = HIGH or MODERATE | selected_files, source_code |
| (none) | verdict = LOW or REJECT | viability_report only |
