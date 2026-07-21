# ADR 0007 - Master Development Plan

## Status

Aceito.

## Data

2026-06-30

## Contexto

O PsychRx evoluiu de uma fase de documentos fundadores para uma arquitetura enterprise com roadmap, Clinical Experience Layer, app localhost read-only e multiplas trilhas futuras.

O roadmap existente define uma sequencia macro, mas nao e suficiente para governar um projeto de varios anos com dezenas de sprints, centenas de missoes, validacao cientifica, experiencia clinica, software, IA, multiagentes e producao.

Era necessario criar um documento superior ao roadmap, capaz de organizar programas, fases, sprints, missoes, gates, riscos e Definition of Done.

## Decisao

Criar `governance/roadmap/MASTER_DEVELOPMENT_PLAN.md` como indice mestre oficial de desenvolvimento do PsychRx.

O MDP passa a governar a decomposicao executiva do projeto, sem substituir os documentos fundadores.

Ele fica acima do roadmap enterprise como documento de planejamento e execucao, mas permanece curto. Detalhes operacionais devem ficar em documentos separados.

O MDP permanece subordinado a:

1. Constituicao Clinica.
2. Manifesto.
3. Principios Arquiteturais.
4. Ontologia.
5. ADRs aprovados.

## Alternativas Consideradas

### Manter apenas o Roadmap Enterprise

Rejeitada. O roadmap resume sequencia macro, mas nao define governanca suficiente para programas, fases, gates e missoes.

### Criar centenas de missoes em um unico documento

Rejeitada. Isso aumentaria risco de inconsistencia, duplicacao, fadiga de revisao e perda de rastreabilidade.

### Criar um MDP incremental por volumes

Aceita. Permite governanca de longo prazo com expansao progressiva, revisavel e controlada.

### Usar o MDP como indice mestre e mover detalhes para documentos satelites

Aceita. Reduz tamanho do MDP e transforma o repositorio em um sistema navegavel por agentes.

## Impacto

- `MASTER_DEVELOPMENT_PLAN.md` passa a ser referencia obrigatoria para localizar a estrutura PROGRAM -> PHASE -> SPRINT -> MISSION -> TASK.
- Documentos satelites passam a controlar status, arvore, dependencias, glossario, conhecimento e proxima missao.
- `ROADMAP_ENTERPRISE.md` permanece como mapa sequencial resumido.
- O Manifesto passa a referenciar o MDP.
- Mudancas estruturais futuras continuam exigindo ADR.

## Riscos

- O MDP pode crescer demais se tentar detalhar todas as missoes de uma vez.
- A equipe pode confundir o MDP com autorizacao de implementacao imediata.
- Programas futuros podem precisar de reconciliacao com documentos historicos.

## Mitigacoes

- Expandir o MDP por volumes.
- Manter cada missao pequena.
- Exigir ADR para mudanca estrutural.
- Preservar documentos fundadores acima do MDP.
- Usar gates antes de implementacao e producao.

## Documentos Afetados

- `governance/roadmap/MASTER_DEVELOPMENT_PLAN.md`
- `docs/PROJECT_CHARTER.md`
- `governance/execution/PROJECT_INDEX.md`
- `governance/execution/PROJECT_TREE.md`
- `governance/execution/PROJECT_PROGRESS.md`
- `governance/execution/PROJECT_STATUS.md`
- `governance/execution/NEXT_MISSION.md`
- `docs/PROJECT_DEPENDENCIES.md`
- `docs/PROJECT_GLOSSARY.md`
- `docs/PROJECT_KNOWLEDGE_MAP.md`
- `docs/000_MANIFEST.md`
- `docs/ROADMAP_ENTERPRISE.md`

## Criterios de Revisao Futura

Este ADR deve ser revisado quando:

- um volume completo do MDP for detalhado;
- houver mudanca estrutural na hierarquia de programas;
- o projeto iniciar fase de producao;
- um novo repositorio oficial for criado;
- a governanca de IA ou multiagentes for formalizada.

## Declaracao Final

O Master Development Plan passa a ser o instrumento oficial para transformar a visao arquitetural do PsychRx em execucao ordenada, auditavel e sustentavel, preservando a Constituicao Clinica, a seguranca, a rastreabilidade e o medico como decisor final.
