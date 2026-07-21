# DM-013 — Audit Ledger técnico

## Escopo

Cria uma trilha de auditoria em memória, append-only e encadeada por SHA-256.
Ela registra apenas metadados técnicos limitados de `DomainEvent`, mantém ordem,
origem temporal e `trace_id`, e permite detectar alteração do conteúdo.

## Limites

Não é armazenamento persistente ou médico-legal. Metadados não devem conter
nome, documento, contato, narrativa clínica ou outro identificador de paciente.
Audit registra e verifica; não altera resultado nem decide conduta.

O rollback é a reversão do commit da missão.
