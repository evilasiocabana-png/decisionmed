# DecisionMEd

Plataforma clínica multiespecialidade derivada de uma cópia independente do PsychRx.

## Estado inicial

- `psychrx-baseline/`: cópia limpa e verificável do PsychRx, sem histórico Git, ambientes virtuais ou caches.
- `ANALISE_VIABILIDADE_DECISIONMED.md`: análise da arquitetura multiespecialidade proposta.
- `BASELINE_MANIFEST.md`: origem, integridade e validação da cópia.

O PsychRx original em `C:\Users\evcab\PsychRx` não deve ser alterado pelo desenvolvimento do DecisionMEd.

## Primeiro objetivo arquitetural

Extrair do baseline um núcleo clínico comum e um contrato de `SpecialtyPack`, mantendo psiquiatria como o primeiro pacote e sem duplicar conhecimento clínico na interface.
