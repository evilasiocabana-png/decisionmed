# DM-014 — Workflow Sessions

## Escopo

Cria sessões estruturais em memória para acompanhar especialidade, posição e
etapas concluídas na ordem definida pelo manifest. Início e avanço geram
`DomainEvent` na trilha de auditoria.

## Limites de dados

O serviço não possui parâmetro para nome, documento, contato, anotações,
sintomas ou qualquer conteúdo livre. Ele registra apenas identificadores
técnicos de sessão, fluxo e etapa. `clinical_execution_allowed` permanece falso
mesmo quando todas as etapas forem concluídas.

Não há persistência, diagnóstico, recomendação ou prescrição. O rollback é a
reversão do commit da missão.
