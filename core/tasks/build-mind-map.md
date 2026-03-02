# build-mind-map

```yaml
---
task: TSK-090
execution_type: Agent
responsible: "@jarvis"
---
```

## Task Anatomy

| Field | Value |
|-------|-------|
| task_name | Build Mind Map |
| status | active |
| responsible_executor | @jarvis |
| execution_type | Agent |
| input | Clone DNA path |
| output | Cognitive mind map |
| action_items | 3 |
| acceptance_criteria | Graph with nodes and edges generated |

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| source_code | string | yes | Clone source code |
| dna_path | string | yes | Path to DNA directory |

## Outputs

| Output | Type | Location | Description |
|--------|------|----------|-------------|
| mind_map | json | knowledge/mind-maps/{source}-map.json | Graph data |
| visualization | md | knowledge/mind-maps/{source}-map.md | Markdown visualization |

## Execution

### Phase 1: Extract nodes from DNA layers
### Phase 2: Detect edges using core/intelligence/edge_detector.py
### Phase 3: Build graph using core/intelligence/graph_builder.py

## Acceptance Criteria
- [ ] All DNA elements represented as nodes
- [ ] Edges classified by relationship type
- [ ] Markdown visualization generated
