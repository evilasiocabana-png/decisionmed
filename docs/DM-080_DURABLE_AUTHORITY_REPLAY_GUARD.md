# DM-080 — Proteção durável contra repetição de autorizações

`SQLiteAuthorityDecisionReplayGuard` fornece uma implementação process-shared
para as portas de replay de Question Engine e revisão de segurança. A reserva é
atômica por namespace, provedor e referência; reiniciar o serviço não permite
reutilizar uma decisão já reservada.

Ela não é ativada pela composição local e não concede autoridade, não executa
raciocínio clínico e não libera execução clínica. Uma implantação futura deve
configurar explicitamente o caminho protegido do banco e o namespace correto.
