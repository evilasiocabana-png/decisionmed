# ADR-0002 - Separacao entre Plataforma e Base de Conhecimento

## ID da Decisao

ADR-0002 - Separacao entre `psychrx-platform` e `psychrx-knowledge`

## Data

2026-06-28

## Status

Aceito

## Contexto

O PsychRx avancou ate a construcao inicial do Domain Layer e da estrutura da Knowledge Layer.

O Sprint 9 proposto, Clinical Knowledge Population, introduz uma mudanca estrutural relevante: separar o projeto em duas linhas paralelas:

- Linha A - Software, responsavel pela plataforma;
- Linha B - Conhecimento Cientifico, responsavel pela populacao e governanca da base clinica.

Essa decisao surge antes da insercao de diretrizes, psicofarmacos, interacoes, contraindicações, efeitos adversos ou regras clinicas.

Documentos relacionados:

- `docs/040_KNOWLEDGE_COMPUTING_ARCHITECTURE.md`;
- `docs/050_ENGINEERING_BLUEPRINT.md`;
- `docs/LAYER_DEPENDENCY_RULES.md`;
- `docs/EVIDENCE_TRACEABILITY_POLICY.md`;
- `docs/SPRINT_GUARDRAILS.md`;
- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`.

O projeto exige que mudancas estruturais relevantes sejam registradas como ADR antes de execucao.

## Decisao

Propor a separacao arquitetural entre:

```text
psychrx-platform/
```

Repositorio ou area responsavel pelo software, camadas de dominio, conhecimento computacional, raciocinio, seguranca, aplicacao, interfaces, auditoria e testes de plataforma.

```text
psychrx-knowledge/
```

Repositorio ou area responsavel exclusivamente por conhecimento cientifico estruturado, incluindo:

- guidelines;
- drugs;
- evidence;
- contraindications;
- interactions;
- monitoring;
- clinical_rules;
- references.

Com esta ADR em status `Aceito`, a decisao oficial e separar plataforma e base de conhecimento. Nenhuma populacao real de diretriz, psicofarmaco, interacao, contraindicação, efeito adverso ou regra clinica deve ser iniciada dentro da plataforma.

O Sprint 9 devera ocorrer em `psychrx-knowledge` ou, ate a criacao fisica desse repositorio, em uma area formalmente isolada equivalente e tratada como futura extracao para repositorio proprio.

## Alternativas Consideradas

### Alternativa 1 - Manter software e conhecimento no mesmo repositorio

Vantagens:

- menor complexidade inicial;
- menos coordenacao entre repositorios;
- execucao local mais simples.

Desvantagens:

- maior risco de misturar conteudo cientifico com implementacao;
- revisoes clinicas e tecnicas ficam acopladas;
- atualizacoes de diretrizes podem gerar alteracoes no software;
- maior risco de retrabalho e regressao.

Motivo para rejeicao parcial:

Pode ser aceitavel temporariamente para infraestrutura vazia, mas nao e ideal para populacao cientifica real.

### Alternativa 2 - Separar plataforma e conhecimento em repositorios distintos

Vantagens:

- reduz acoplamento entre engenharia e conteudo cientifico;
- permite versionamento independente da base de conhecimento;
- facilita revisao cientifica por equipe clinica;
- melhora auditoria de mudancas em fontes e conhecimento;
- permite que a plataforma consuma uma biblioteca estavel e versionada.

Desvantagens:

- exige contratos claros de consumo;
- exige processo de sincronizacao entre repositorios;
- exige governanca de releases da base de conhecimento.

Motivo para aceitacao proposta:

E a alternativa mais coerente com a separacao entre conhecimento cientifico, conhecimento computacional e logica de execucao.

### Alternativa 3 - Monorepo com areas fortemente isoladas

Vantagens:

- preserva um unico repositorio;
- reduz complexidade operacional inicial;
- permite isolamento por pastas e regras.

Desvantagens:

- ainda permite acoplamento acidental;
- dificulta versionamento independente;
- mistura PRs clinicos e tecnicos no mesmo fluxo;
- pode enfraquecer governanca cientifica no longo prazo.

Motivo para manter como fallback:

Pode ser usado como etapa intermediaria se a criacao de segundo repositorio ainda nao estiver operacionalmente aprovada.

## Justificativa

O principal ativo do PsychRx e o conhecimento clinico estruturado.

Misturar populacao cientifica com implementacao de software aumenta risco de:

- conhecimento hardcoded;
- regressao em motores;
- revisoes clinicas afetando codigo;
- perda de rastreabilidade;
- dificuldade de auditoria;
- dependencia indevida entre conteudo e plataforma.

A separacao proposta preserva:

- seguranca clinica;
- governanca cientifica;
- rastreabilidade;
- versionamento independente;
- explicabilidade;
- separacao entre conhecimento e algoritmo.

## Impacto

Pastas e repositorios afetados:

- possivel criacao de `psychrx-platform/`;
- possivel criacao de `psychrx-knowledge/`;
- revisao da responsabilidade da pasta atual `knowledge/`;
- revisao da responsabilidade da pasta atual `knowledge_core/`;
- revisao da responsabilidade da pasta atual `knowledge_governance/`.

Documentos afetados:

- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`;
- `docs/LAYER_DEPENDENCY_RULES.md`;
- `docs/040_KNOWLEDGE_COMPUTING_ARCHITECTURE.md`;
- `docs/050_ENGINEERING_BLUEPRINT.md`;
- futuros documentos do Sprint 9.

Impactos sobre testes:

- sera necessario testar contratos de consumo da biblioteca de conhecimento;
- sera necessario validar versionamento e rastreabilidade entre repositorios;
- testes de plataforma nao devem depender de conteudo cientifico real salvo fixtures controladas.

Impactos sobre futuras missoes:

- Sprint 9 nao deve popular conhecimento real ate que a separacao ou uma alternativa formal seja aprovada;
- missoes de conhecimento devem alterar apenas `psychrx-knowledge` ou a area formal equivalente;
- missoes de software devem alterar apenas `psychrx-platform` ou a area formal equivalente.

## Riscos

Riscos mitigados:

- mistura entre conhecimento e algoritmo;
- PRs clinicos alterando software;
- atualizacao cientifica quebrando plataforma;
- perda de rastreabilidade;
- auditoria fraca de conteudo cientifico.

Riscos introduzidos:

- aumento de complexidade operacional;
- necessidade de contratos entre repositorios;
- necessidade de versao compativel entre plataforma e conhecimento;
- possivel duplicacao temporaria durante migracao.

## Documentos Afetados

- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `docs/LAYER_DEPENDENCY_RULES.md`
- `docs/040_KNOWLEDGE_COMPUTING_ARCHITECTURE.md`
- `docs/050_ENGINEERING_BLUEPRINT.md`
- `docs/SPRINT_GUARDRAILS.md`
- `docs/EVIDENCE_TRACEABILITY_POLICY.md`

## Criterios de Revisao Futuro

Esta ADR deve ser revisada quando:

- for aprovada ou rejeitada a criacao de `psychrx-knowledge`;
- for definida a forma de consumo da base de conhecimento pela plataforma;
- houver contrato formal de versionamento entre plataforma e conhecimento;
- surgir necessidade de mover conhecimento cientifico real para fora do repositorio atual;
- a equipe clinica iniciar revisao de conteudo cientifico versionado;
- houver conflito com ADR futura sobre estrutura de repositorios.
