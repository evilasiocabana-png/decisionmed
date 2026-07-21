# ADR-0001 - Governanca Arquitetural

## ID da Decisao

ADR-0001 - Governanca Arquitetural

## Data

2026-06-28

## Status

Aceito

## Contexto

O PsychRx esta definindo sua arquitetura antes de qualquer implementacao clinica. O projeto possui documentos que estabelecem separacao entre dominio, conhecimento, evidencia, raciocinio, seguranca, aplicacao, interface, auditoria e testes.

Como o sistema lida com raciocinio medico em psicofarmacologia, mudancas estruturais podem afetar seguranca clinica, rastreabilidade, explicabilidade e governanca cientifica.

Sem registro formal de decisoes arquiteturais, o projeto corre risco de:

- alterar camadas sem justificativa;
- introduzir dependencias proibidas;
- misturar conhecimento cientifico com algoritmo;
- permitir interface influenciar decisao clinica;
- perder rastreabilidade historica;
- criar inconsistencias entre documentos oficiais.

## Decisao

Toda decisao estrutural relevante do PsychRx devera ser registrada como Architecture Decision Record (ADR).

Nenhuma mudanca estrutural futura podera ocorrer sem ADR correspondente.

Uma decisao estrutural relevante inclui:

- criacao, remocao ou reorganizacao de pastas oficiais;
- alteracao nas regras de dependencia entre camadas;
- introducao de nova camada arquitetural;
- mudanca de responsabilidade entre camadas;
- mudanca em governanca de conhecimento, evidencia, seguranca ou auditoria;
- decisao que afete rastreabilidade ou explicabilidade;
- decisao que altere limites entre dominio, aplicacao e interface;
- excecao a regra arquitetural existente.

## Alternativas Consideradas

### Nao usar ADRs

Vantagem: menor custo documental imediato.

Desvantagem: maior risco de decisoes invisiveis, perda de contexto e violacoes arquiteturais futuras.

Motivo da rejeicao: inadequado para um projeto clinico que exige rastreabilidade.

### Registrar decisoes apenas em documentos gerais

Vantagem: centraliza documentacao em poucos arquivos.

Desvantagem: dificulta saber quando, por que e por quem uma decisao estrutural foi tomada.

Motivo da rejeicao: insuficiente para governanca arquitetural longitudinal.

### Usar ADRs para decisoes estruturais relevantes

Vantagem: preserva contexto, justificativa, alternativas, impacto e criterios de revisao.

Desvantagem: exige disciplina documental.

Motivo da aceitacao: melhor equilibrio entre rastreabilidade, governanca e manutencao futura.

## Justificativa

O PsychRx exige governanca arquitetural rigorosa porque qualquer acoplamento indevido pode comprometer seguranca clinica e explicabilidade.

ADRs permitem:

- registrar decisoes estruturais com contexto;
- justificar alteracoes;
- avaliar alternativas;
- mapear impacto;
- identificar riscos;
- conectar decisoes a documentos afetados;
- revisar decisoes quando o projeto evoluir.

Essa pratica reforca a Definition of Done do Codex, as regras de dependencia entre camadas e a estrutura oficial do repositorio.

## Impacto

Esta decisao impacta todas as missoes futuras que envolvam mudanca estrutural.

Pastas afetadas:

- `docs/adr/`
- `docs/`

Documentos relacionados:

- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `docs/LAYER_DEPENDENCY_RULES.md`
- `docs/CODEX_DEFINITION_OF_DONE.md`
- `docs/CODEX_MISSION_TEMPLATE.md`

Impacto operacional:

- toda mudanca estrutural futura deve criar ou atualizar uma ADR;
- Pull Requests devem verificar se ha ADR correspondente;
- missoes do Codex devem declarar quando uma ADR e necessaria;
- excecoes arquiteturais devem ser registradas formalmente.

## Riscos

Riscos mitigados:

- mudancas estruturais sem justificativa;
- acoplamento indevido entre camadas;
- perda de rastreabilidade;
- decisoes conflitantes;
- enfraquecimento da governanca cientifica;
- alteracoes arquiteturais invisiveis.

Riscos introduzidos:

- aumento de carga documental;
- possibilidade de ADRs superficiais;
- necessidade de manter ADRs atualizadas.

## Documentos Afetados

- `docs/adr/ADR_TEMPLATE.md`
- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `docs/LAYER_DEPENDENCY_RULES.md`
- `docs/CODEX_DEFINITION_OF_DONE.md`
- `docs/CODEX_MISSION_TEMPLATE.md`

## Criterios de Revisao Futuro

Esta ADR deve ser revisada quando:

- uma nova camada oficial for criada;
- a estrutura oficial do repositorio mudar;
- as regras de dependencia entre camadas forem alteradas;
- uma decisao estrutural precisar de excecao;
- Pull Requests comecarem a violar governanca arquitetural;
- o processo de ADR se mostrar insuficiente ou excessivo.
