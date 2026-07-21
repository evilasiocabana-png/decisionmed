# DM-021 — Validação estrutural de entrada clínica

## Resultado

A primeira implementação dentro de `decisionmed/application/` valida payloads
contra `SpecialtyFormSchema` sem acessar interface, persistência ou algoritmo
clínico.

Ela verifica somente:

- presença de campos obrigatórios;
- rejeição de campos desconhecidos;
- tipos primitivos estritos;
- números finitos e texto limitado;
- escolhas pertencentes ao conjunto governado.

## Limites de segurança

O resultado não contém os valores recebidos, não cria `ClinicalObservation`, não
persiste dados e sempre informa `clinical_execution_allowed = False`. Validade
estrutural não significa validade clínica.

Não há endpoint ou ligação com a interface nesta missão. Essa integração depende
de controles de privacidade e de schemas clínicos efetivamente validados.

## Reversão

Remover o pacote `application`, seu teste e este documento. Nenhum dado é afetado.
