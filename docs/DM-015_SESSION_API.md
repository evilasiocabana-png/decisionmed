# DM-015 — Session API

## Escopo

Expõe criação e avanço de sessões estruturais por JSON e conecta o stepper ao
serviço. O contrato aceita somente `specialty_key` ou `step_key`, conforme o
endpoint. Campos extras, corpos acima de 1 KiB e conteúdo fora do contrato são
rejeitados.

As anotações permanecem em memória no navegador e nunca integram o corpo das
requisições. A API registra progresso técnico, não conteúdo clínico. Não há
persistência, diagnóstico, recomendação ou prescrição. Sem autenticação, ambos
os servidores recusam binding fora do loopback. O rollback é a reversão do
commit da missão.
