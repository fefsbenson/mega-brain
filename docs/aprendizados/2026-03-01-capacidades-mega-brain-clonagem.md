# Capacidades do Mega Brain - Sistema de Clonagem Cognitiva

> **Data:** 2026-03-01
> **Sessao:** #9
> **Tipo:** Inventario de Capacidades
> **Status:** Arquiteturalmente completo, aguardando primeira execucao

---

## O Que e o Mega Brain

Fabrica de clones cognitivos. Transforma material bruto de especialistas (videos, transcricoes, livros, podcasts) em replicas fieis de como a pessoa pensa — nao o que ela diz, mas como ela raciocina, decide e prioriza.

**Meta de fidelidade:** < 10% de distinguibilidade (94%+ fidelidade em blind test).

---

## Arsenal Atual (Marco 2026-03-01)

| Componente | Quantidade | Status |
|------------|------------|--------|
| Skills (slash commands) | 52 | Operacionais |
| Workflows YAML | 6 | Definidos |
| Protocolos | 9 | Documentados |
| Scripts Python | 25 | Implementados (0 stubs) |
| Templates | 25+ | Oficiais |
| JSON Schemas | 14 | Validados |
| Task Definitions | 16 | Atomicas |
| Agentes Conclave | 3 | Ativos (Critic, Advocate, Synthesizer) |
| Pattern Configs | 4 | Calibrados |
| Quality Gates | 9 | Definidos |

---

## DNA Cognitivo: 8 Camadas

### Fase 1 — Conhecimento Explicito (extraido de declaracoes diretas)

| Camada | ID Pattern | O Que Captura |
|--------|-----------|---------------|
| L5 Methodologies | MET-XX-NNN | Passo-a-passo, receitas, procedimentos |
| L4 Frameworks | FW-XX-NNN | Modelos nomeados, sistemas multi-componente |
| L3 Heuristics | HEUR-XX-NNN | Regras, thresholds, atalhos de decisao |
| L2 Mental Models | MM-XX-NNN | Lentes de pensamento, analogias |
| L1 Philosophies | FIL-XX-NNN | Crencas core, visao de mundo |

### Fase 2 — Cognicao Profunda (inferida via triangulacao, 3+ fontes)

| Camada | ID Pattern | O Que Captura | Requisito |
|--------|-----------|---------------|-----------|
| L6 Values Hierarchy | VAL-XX-NNN | Valores reais revelados por trade-offs | 3+ fontes independentes |
| L7 Core Obsessions | OBS-XX-NNN | 2-5 drivers cognitivos profundos | Presentes em 50%+ do material |
| L8 Productive Paradoxes | PAR-XX-NNN | Contradicoes que coexistem | Validacao humana obrigatoria (Gold Gate) |

### Cascata de Raciocinio do Agente

```
L5 -> L4 -> L3 -> L2 -> L1 -> L6 check -> L7 check -> L8 check
(mais concreto primeiro)
```

---

## Pipeline Completo: Materia Bruta ao Clone Vivo

### Fluxo Principal

```
Material Bruto (video, transcricao, PDF, livro)
    |
    v
INGEST (/ingest) - Download, metadata, colocar em inbox/
    |
    v
APEX TRIAGE (/apex-score) - QG-1
    4 dimensoes: Autenticidade, Praticidade, Expertise, X-Factor
    < 50 = REJECT | 50-60 = CONDICIONAL | > 60 = GO
    |
    v
FOUNDATION - Normalizar entidades + detectar roles + analisar temas
    |
    v
EXTRACTION (/extract-dna) - QG-2
    L1 -> L2 -> L3 -> L4 -> L5 (uma a uma, bloqueante)
    Output: DNA-CONFIG.yaml
    |
    v
PIPELINE JARVIS (/process-jarvis)
    8 sub-fases por batch:
    Chunking -> Entity Resolution -> Insight Extraction ->
    Narrative Synthesis -> Dossier Compilation ->
    Agent Enrichment -> Finalization
    |
    v
VALIDACAO (validate-cascade)
    Verifica cascateamento para todos os destinos declarados
    |
    v
DNA PROFUNDO (L6 + L7 + L8) - QG-3, QG-4, QG-5
    So roda APOS todos os batches da pessoa
    |
    v
BLIND TEST (/blind-test) - QG-6, QG-7
    100-120 cenarios de teste
    GOLD: < 10% distinguivel | SILVER: 10-20% | FAIL: > 30%
    |
    v
COMPILATION (/compile-prompt) - QG-8, QG-9
    DNA -> System Prompt deployavel
    |
    v
CLONE DEPLOYED
    SOUL.md + MEMORY.md + DNA-CONFIG.yaml + prompts/
```

### 9 Quality Gates (checkpoints humanos obrigatorios)

| Gate | Momento | Tipo |
|------|---------|------|
| QG-1 | Pos-APEX scoring | GO/NO-GO humano |
| QG-2 | Pos-inventario de fontes | Threshold (5+ fontes) |
| QG-3 | Pos-L6 Values | Confirmacao humana |
| QG-4 | Pos-L7 Obsessions | Confirmacao humana |
| QG-5 | Pos-L8 Paradoxes | GOLD GATE - validacao profunda |
| QG-6 | Pos-system prompt | Aprovacao humana |
| QG-7 | Pos-blind testing | Metrica (80%+ fidelidade) |
| QG-8 | Pos-brownfield update | Regressao (< 5% queda) |
| QG-9 | Sign-off final | Autorizacao para deploy |

---

## Modos de Ativacao do Clone

| Modo | Comando | Descricao |
|------|---------|-----------|
| Single | /emulate | Clone unico, responde em primeira pessoa |
| Dual | /dual-mode | 2 clones lado a lado, 3 rounds |
| Roundtable | /roundtable | 3-4 clones, 5 fases de debate |
| Conclave | /conclave | Agentes de CARGO, deliberacao formal com Critic + Advocate + Synthesizer |

---

## Capacidades Especiais

### Brownfield (/brownfield)
Atualizacao incremental. Novo material para pessoa ja clonada: faz diff, extrai so camadas afetadas. Economia de 60-75% dos tokens. Rollback automatico se fidelidade cair > 5%.

### Blind Test (/blind-test)
100-120 cenarios gerados automaticamente. Score composto: Content 30% + Linguistic 25% + Reasoning 25% + Emotional 10% + Paradox 10%.

### Mind Map (/mind-map)
Mapeamento visual das interconexoes entre elementos do DNA. Grafo navegavel: nos = conceitos, arestas = relacoes.

### Compile Prompt (/compile-prompt)
Exporta DNA para system prompt standalone. Generalista (todos os dominios, 4-8K tokens) ou Especialista (filtrado, 2-4K tokens). Funciona em QUALQUER LLM.

### Boardroom
Debates entre agentes transformados em episodios de podcast via TTS (Edge TTS + NotebookLM).

### APEX Scoring (/apex-score)
Triagem pre-pipeline. Avalia se material vale processar ANTES de gastar tokens.

### Rastreabilidade 100%
Todo item de DNA rastreavel ate o arquivo bruto original. Cadeia: DNA -> Insight -> Chunk -> Arquivo RAIZ. 5 elementos sempre prontos: QUEM, QUANDO, ONDE, TEXTO, PATH.

---

## Arquivos-Chave por Clone Deployado

```
agents/persons/{nome}/
    AGENT.md          - Definicao operacional (11 partes, Template V3)
    SOUL.md           - Identidade e voz
    MEMORY.md         - Experiencia acumulada
    DNA-CONFIG.yaml   - Configuracao de fontes e DNA
    prompts/
        generalista.md       - System prompt completo
        specialist-{N}.md    - System prompt filtrado por dominio
```

---

## Workflows YAML Disponiveis

| Workflow | Proposito |
|----------|-----------|
| wf-pipeline-full.yaml | Pipeline completo: triage -> ingest -> process -> enrich -> compile |
| wf-extract-dna.yaml | Extracao de DNA Cognitivo (5 camadas) |
| wf-ingest.yaml | Ingestao de material no INBOX |
| wf-conclave.yaml | Sessao de deliberacao do Conselho |
| wf-brownfield-update.yaml | Atualizacao incremental de clone existente |
| wf-mind-mapper.yaml | Mapeamento cognitivo de interconexoes |

---

## Protocolos Documentados

| Protocolo | Proposito |
|-----------|-----------|
| blind-testing-protocol.md | Medicao de fidelidade via testes cegos |
| brownfield-detection.md | Deteccao e classificacao de cenarios incrementais |
| clone-activation.md | Carregamento, ativacao e encarnacao de clones |
| dna-mental-extraction.md | Extracao de DNA de 8 camadas |
| enhanced-debate.md | Argumentacao multi-agente com scoring |
| mind-mapping.md | Visualizacao de interconexoes cognitivas |
| modular-workflows.md | Arquitetura modular composavel |
| prompt-compilation.md | Compilacao de DNA em system prompts |
| quality-gates-9-checkpoints.md | 9 gates de validacao humana |

---

## Estado em Marco 2026

- **Arquitetura:** Completa (0 stubs, 0 placeholders)
- **Clones ativos:** 0 (fabrica pronta, aguardando materia-prima)
- **Upstream:** 24 commits a frente de origin/main, 14 PRs abertos
- **Proximo passo:** Ingerir material bruto e executar primeiro pipeline

---

## Visao Futura (PRD documentado)

10 propostas de evolucao alem do estado atual:

| Prioridade | Proposta | Descricao |
|------------|----------|-----------|
| P1 | Temporal Evolution | Rastrear como visoes mudam ao longo do tempo |
| P2 | Real-Time Learning | Atualizar clones sem reprocessamento completo |
| P3 | Cross-Clone Transfer | Insights de um clone informam outro |
| P4 | Predictive Decisions | Prever decisoes novas, nao so replay |
| P5 | Emotional Resonance | Registro emocional alem de tom/voz |
| P6 | Adversarial Testing | Testes de stress para modos de falha |
| P7 | Collective Intelligence | Inteligencia emergente de multi-clone |
| P8 | Meta-Cognitive Awareness | Clone explica sua propria cadeia de raciocinio |
| P9 | Cultural Calibration | Adaptar conselhos US-centric para contextos globais |
| P10 | Clone Genealogy | Linhagem intelectual entre clones |

Caminho critico: P1 -> P2 -> P3 -> P6 -> P7 -> P9.

---

*Registrado por JARVIS | Sessao #9 | 2026-03-01*
