# DM-022 — Carregador de catálogo governado externo

## Resultado

A plataforma agora consome, de uma pasta externa, três arquivos versionados:
`evidence.json`, `knowledge.json` e `form-schemas.json`.

O carregamento é fail-closed: nomes e campos são exatos, chaves duplicadas são
rejeitadas, arquivos têm limite de tamanho, links simbólicos são bloqueados e
todas as referências são validadas na sequência:

`EvidenceSource -> KnowledgeObject -> SpecialtyFormSchema`

## Separação arquitetural

Conforme ADR-0002 do PsychRx, nenhum conteúdo científico real foi adicionado ao
repositório da plataforma. O caminho do catálogo é fornecido externamente, o que
permite versionamento e revisão clínica independentes.

## Limites

Carregar metadados não ativa runtime clínico. Os contratos continuam retornando
`clinical_execution_allowed = False`; não há endpoint, persistência ou regra.

## Reversão

Remover o carregador, exports, testes e este documento. Não há dado persistido.
