# DM-018 — Linhagem append-only de ClinicalSnapshot

## Resultado

`ClinicalSnapshotStore` preserva revisões imutáveis em ordem cronológica. Cada
revisão referencia a anterior; sujeito e especialidade não podem mudar dentro da
mesma linhagem.

## Segurança

- armazenamento apenas em memória, limitado e não exposto por API;
- nenhuma atualização ou exclusão de revisão existente;
- auditoria SHA-256 recebe somente IDs técnicos, especialidade e predecessor;
- valores clínicos e referência do sujeito não entram no log;
- o serviço não autoriza execução clínica.

Esta estrutura não é prontuário e não oferece retenção médico-legal. Persistência
futura dependerá de autenticação, criptografia, política de retenção e validação
regulatória.

## Reversão

Remover o serviço, os campos de linhagem e os respectivos testes. Como o estado é
volátil, não existe migração ou dado persistido a reverter.
