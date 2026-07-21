# DM-012 — Platform Readiness

## Escopo

Expõe pela Application Layer um relatório read-only dos gates técnicos de
domínio, evidência, conhecimento, segurança, especialidades e validação humana.
A interface consome apenas esse contrato e não acessa as camadas internas.

O relatório não declara prontidão clínica. `clinical_execution_allowed`
permanece falso e o gate de validação científica, regulatória e humana fica
sempre bloqueado nesta fase. O rollback é a reversão do commit da missão.
