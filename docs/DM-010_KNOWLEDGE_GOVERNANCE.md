# DM-010 — KnowledgeObject governado

## Escopo

Cria um contrato versionado para objetos de conhecimento e um registro que
exige referências a `EvidenceSource` já catalogadas. Objetos marcados como
validados exigem data, revisor humano e metadados das fontes validados.

## Limites

Nenhum objeto clínico real é incluído. `runtime_eligible` permanece sempre
falso: validação de metadados não equivale a liberação científica, editorial,
regulatória ou clínica. Knowledge descreve conteúdo; não executa algoritmos.

Não há banco, rede, motor, recomendação ou prescrição. O rollback é a reversão
do commit da missão.
