# DM-009 — EvidenceSource metadata-only

## Escopo

Cria o contrato e o registro determinístico de metadados de fontes científicas
ou regulatórias. Nenhuma fonte real, afirmação clínica ou regra terapêutica é
adicionada nesta missão.

## Gate permanente

`EvidenceSource.runtime_eligible` permanece sempre falso. Mesmo metadados com
status `validated` não autorizam uso clínico: ainda serão necessários conteúdo
revisado, qualidade, força, conflitos, aplicabilidade e aprovação editorial.

Não há banco, acesso à rede, recomendação ou integração com motores. O rollback
é a reversão do commit da missão.
