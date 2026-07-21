# DM-011 — Safety First estrutural

## Escopo

Cria contratos imutáveis para resultados e achados de checagens de segurança,
além de um coordenador fail-closed que agrega resultados externos rastreáveis.

O coordenador não lê dados de pacientes e não contém contraindicações,
interações, limites ou regras clínicas. Checagens ausentes, não avaliadas ou
sem metadados de evidência validados mantêm o gate incompleto. Achado crítico
mantém o gate bloqueado.

Mesmo `ready_for_human_review` mantém `clinical_execution_allowed = false`.
Não há estratégia, recomendação ou prescrição. O rollback é a reversão do
commit da missão.
