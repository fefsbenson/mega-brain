---
name: apex-score
description: "Pre-pipeline triage using APEX viability scoring. Evaluates source material before committing to full pipeline processing."
---

> **Auto-Trigger:** Before starting pipeline processing on new source material
> **Keywords:** "apex", "viability", "triage", "score", "pre-pipeline", "avaliar fonte", "vale a pena processar"
> **Prioridade:** ALTA

---

# APEX Viability Scoring - Pre-Pipeline Triage

## Overview

Scores source material viability BEFORE committing pipeline resources. Uses the APEX framework (Authenticity, Practicality, Expertise, X-factor) to determine if material is worth full processing.

**Anunciar no inicio:** "Ativando APEX scoring para avaliar viabilidade da fonte."

## Quando Ativar

- New source material arrives in INBOX
- User asks "should we process this?"
- Before `/jarvis-full` or `/process-jarvis` on new source
- When evaluating whether a mentor/expert has enough material

## Quando NAO Ativar

- Material already in pipeline (already committed)
- User explicitly wants to skip triage
- Re-processing existing source (use brownfield instead)

## Processo

### 1. Load Schema
Read `core/schemas/viability-score.schema.json` for scoring criteria.

### 2. Evaluate Material
For each source file, score across 4 dimensions:

| Dimension | Weight | What to Evaluate |
|-----------|--------|-------------------|
| **A**uthenticity | 25% | Is this the expert's own content? Original thinking? |
| **P**racticality | 30% | Actionable frameworks? Concrete methodologies? |
| **E**xpertise | 25% | Depth of domain knowledge? Unique insights? |
| **X**-factor | 20% | Novel perspectives? Contrarian views? Memorable? |

### 3. Generate Report
Use template from `core/templates/assessment/viability-report.yaml` to produce structured output.

### 4. Decision Matrix

| Score | Verdict | Action |
|-------|---------|--------|
| 80-100 | HIGH VIABILITY | Proceed to full pipeline |
| 60-79 | MODERATE | Process selectively (best files only) |
| 40-59 | LOW | Extract key insights only, skip full pipeline |
| 0-39 | REJECT | Do not process, document reason |

## Output

```yaml
viability_report:
  source: "{SOURCE_NAME}"
  score: {0-100}
  verdict: "{HIGH|MODERATE|LOW|REJECT}"
  dimensions:
    authenticity: {0-100}
    practicality: {0-100}
    expertise: {0-100}
    x_factor: {0-100}
  recommendation: "{action}"
  files_evaluated: {count}
```

## Integration

- Task: `core/tasks/score-viability.md` (TSK-012)
- Schema: `core/schemas/viability-score.schema.json`
- Report template: `core/templates/assessment/viability-report.yaml`
- Pipeline: `phase_0 (TRIAGE)` in `wf-pipeline-full.yaml`
