# Schema Index

> **Versão:** 1.1.0
> **Última Atualização:** 2026-02-28

## Schemas Disponíveis

| Schema | Arquivo de Estado | Propósito |
|--------|-------------------|-----------|
| `chunks-state.schema.json` | `/artifacts/chunks/CHUNKS-STATE.json` | Chunks extraídos das fontes |
| `canonical-map.schema.json` | `/artifacts/canonical/CANONICAL-MAP.json` | Mapa de entidades canônicas |
| `insights-state.schema.json` | `/artifacts/insights/INSIGHTS-STATE.json` | Insights extraídos |
| `narratives-state.schema.json` | `/artifacts/narratives/NARRATIVES-STATE.json` | Narrativas sintetizadas |
| `file-registry.schema.json` | `/system/REGISTRY/file-registry.json` | Registry de arquivos processados |
| `decisions-registry.schema.json` | `/logs/SYSTEM/decisions-registry.json` | Decisões e precedentes |
| `dna-mental-8-layer.schema.json` | `/knowledge/dna/persons/{PERSON}/DNA-MENTAL.json` | 8-layer cognitive architecture (DNA Mental) |
| `viability-score.schema.json` | `/artifacts/triage/{SOURCE}-viability.yaml` | APEX viability scoring for pre-pipeline triage |
| `quality-gate.schema.json` | - | Quality gate checkpoint definitions (9 gates) |
| `fidelity-report.schema.json` | `/artifacts/validation/{CLONE}-fidelity.json` | Clone fidelity blind test results |
| `mind-map.schema.json` | `/knowledge/mind-maps/{SOURCE}-map.json` | Cognitive mind map graph structure |
| `debate-session.schema.json` | `/logs/council/DEBATE-{date}.json` | Enhanced debate session with scoring |
| `workflow-module.schema.json` | - | Modular workflow component definition |

## Sistema de IDs Unificado

### Padrões de ID

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Source ID | `PREFIX` + `NNN` | `JL001`, `CG003`, `HR001` |
| Chunk ID | `SOURCE_ID` + `-` + `NNN` | `JL001-001`, `CG003-015` |
| Decision ID | `YYYYMMDDHHMMSS-ORIGIN-DEST` | `20251215130249-CRO-CFO` |
| Precedent ID | `PREC-YYYY-NNN` | `PREC-2025-001` |
| Philosophy ID | `FIL-PREFIX-NNN` | `FIL-AH-001` |
| Mental Model ID | `MM-PREFIX-NNN` | `MM-AH-005` |
| Heuristic ID | `HEUR-PREFIX-NNN` | `HEUR-CG-018` |
| Framework ID | `FW-PREFIX-NNN` | `FW-AH-003` |
| Methodology ID | `MET-PREFIX-NNN` | `MET-CG-005` |
| Value ID | `VAL-PREFIX-NNN` | `VAL-AH-001` |
| Obsession ID | `OBS-PREFIX-NNN` | `OBS-AH-001` |
| Paradox ID | `PAR-PREFIX-NNN` | `PAR-AH-001` |

### Prefixos de Fonte Registrados

| Prefixo | Pessoa/Canal | Empresa |
|---------|--------------|---------|
| `JL` | Jordan Lee | AI Business |
| `CJ` | Charlie Johnson Show | - |
| `MT` | Max Tornow | Max Tornow Podcast |
| `HR` | Alex Hormozi | - |
| `CG` | Cole Gordon | - |
| `SS` | Sam Oven | Setterlun University |

## Foreign Keys (Rastreabilidade)

```
file-registry.json
    ├─ source_id ──────────────────┐
    └─ chunk_count                 │
                                   ▼
CHUNKS-STATE.json ◄────────────────┘
    ├─ source_id
    └─ chunks[]
        └─ chunk_id ───────────────┐
                                   │
INSIGHTS-STATE.json ◄──────────────┤
    └─ chunk_id                    │
        └─ insight_id ─────────────┤
                                   │
NARRATIVES-STATE.json ◄────────────┤
    └─ evidence_chain[] (chunk_ids)│
                                   │
decisions-registry.json ◄──────────┘
    └─ chunk_ids[]
    └─ sources[] (knowledge files)
```

## Validação

### Usando Python

```python
import json
import jsonschema

# Load schema
with open('system/SCHEMAS/chunks-state.schema.json') as f:
    schema = json.load(f)

# Load data
with open('artifacts/chunks/CHUNKS-STATE.json') as f:
    data = json.load(f)

# Validate
jsonschema.validate(data, schema)
```

### CLI (se jsonschema instalado)

```bash
python -m jsonschema -i CHUNKS-STATE.json chunks-state.schema.json
```

## Regras de Incremento

1. **Nunca deletar** - apenas adicionar ou marcar como deprecated
2. **Sempre validar** antes de salvar
3. **Incrementar version** em cada mudança
4. **Manter change_log** para auditoria
