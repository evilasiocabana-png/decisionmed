# ADR Template

## ID da Decisao

ADR-XXXX - Titulo curto da decisao

## Data

AAAA-MM-DD

## Status

Proposto | Aceito | Substituido | Depreciado | Rejeitado

## Contexto

Descrever o problema, tensao arquitetural, necessidade clinica, restricao ou mudanca estrutural que exige decisao.

Incluir:

- contexto do projeto;
- documentos relacionados;
- limites clinicos ou arquiteturais;
- dependencias envolvidas;
- motivo pelo qual a decisao precisa ser registrada.

## Decisao

Descrever claramente a decisao tomada.

A decisao deve ser especifica o suficiente para orientar implementacoes, revisoes e futuras missoes do Codex.

## Alternativas Consideradas

Listar alternativas avaliadas.

Para cada alternativa, registrar:

- descricao;
- vantagens;
- desvantagens;
- motivo para aceitar ou rejeitar.

## Justificativa

Explicar por que a decisao escolhida e a mais adequada para o PsychRx.

Considerar:

- seguranca clinica;
- separacao entre camadas;
- rastreabilidade;
- explicabilidade;
- governanca cientifica;
- manutencao futura;
- coerencia com documentos oficiais.

## Impacto

Descrever o impacto esperado.

Incluir:

- pastas afetadas;
- documentos afetados;
- camadas afetadas;
- dependencias criadas ou removidas;
- impactos sobre testes;
- impactos sobre futuras missoes.

## Riscos

Listar riscos introduzidos ou mitigados pela decisao.

Exemplos:

- acoplamento indevido;
- mistura entre conhecimento e algoritmo;
- perda de rastreabilidade;
- ambiguidade clinica;
- aumento de complexidade;
- dependencia proibida;
- impacto em documentacao existente.

## Documentos Afetados

Listar documentos que devem ser atualizados, revisados ou consultados.

Exemplo:

- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `docs/LAYER_DEPENDENCY_RULES.md`
- `docs/CODEX_DEFINITION_OF_DONE.md`

## Criterios de Revisao Futuro

Definir quando esta decisao deve ser revisada.

Exemplos:

- nova camada arquitetural;
- mudanca estrutural relevante;
- conflito com outra ADR;
- surgimento de dependencia proibida;
- necessidade de implementacao que nao se encaixa na decisao;
- alteracao nos principios clinicos do PsychRx.
