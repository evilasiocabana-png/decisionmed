# 049 - Implementation Order

## 1. Objetivo

Definir a ordem oficial de implementacao futura do PsychRx, sem iniciar implementacao, criar codigo ou escolher tecnologia.

## 2. Missao

Estabelecer prioridades para que o Codex implemente pequenas missoes executaveis sem violar arquitetura, dominio, seguranca, evidencia ou testes.

## 3. Principios

- Implementar base antes de interface.
- Implementar dominio antes de application.
- Implementar contratos antes de motores.
- Implementar seguranca antes de estrategia.
- Implementar testes junto com cada unidade.
- Nao implementar conhecimento hardcoded.

## 4. Ordem Recomendada

1. Estrutura de repositorio e camadas.
2. Contratos de dominio.
3. Objetos de conhecimento computacional.
4. Modelos de rastreabilidade e versionamento.
5. Validacoes de dominio e conhecimento.
6. Safety First primitives.
7. Clinical Snapshot.
8. Question Engine.
9. Diagnostic Reasoning Engine.
10. Therapeutic Objective Engine.
11. Constraint e Evidence integration.
12. Strategy Generation.
13. Strategy Comparison.
14. Explanation Engine.
15. Monitoring Engine.
16. Longitudinal Reasoning.
17. Application orchestration.
18. Interfaces.
19. Audit hardening.

## 5. Dependencias

Nenhum modulo deve ser implementado antes de seus contratos e testes esperados.

Strategy depende de Objective, Safety, Constraint e Evidence. Interface depende de Application. Application depende de contratos.

## 6. Modulos

Cada modulo deve ser implementado por missoes pequenas, idealmente alterando de 1 a 5 arquivos.

## 7. Prioridades

Prioridade maxima:

- dominio;
- seguranca;
- contratos;
- rastreabilidade;
- testes;
- explicabilidade.

Prioridade posterior:

- interface;
- otimizacao;
- experiencia visual;
- automacoes auxiliares.

## 8. Criterios de Conclusao

Uma missao futura so conclui quando:

- escopo foi respeitado;
- testes passaram;
- contratos foram mantidos;
- documentacao foi atualizada;
- rastreabilidade foi preservada;
- nao houve dependencia proibida.

## 9. Definition of Done

Aplicar `CODEX_DEFINITION_OF_DONE.md` como regra obrigatoria.

Missao nao esta concluida se quebrou testes, misturou conhecimento com algoritmo, removeu explicabilidade ou alterou arquivos fora do escopo.

## 10. Limites

Este documento nao cria tarefas de codigo ainda. Ele define ordem de implementacao futura.

## 11. Declaracao Final

Implementation Order transforma arquitetura em sequencia disciplinada.

No PsychRx, implementar fora de ordem e criar divida clinica e arquitetural.
