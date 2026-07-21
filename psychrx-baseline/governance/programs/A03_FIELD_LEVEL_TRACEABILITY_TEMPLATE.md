# A03 - Field Level Traceability Template

## Objetivo

Definir o template obrigatorio para cada campo populado em um medicamento SSRI.

## Template

```text
drug_id:
drug_name:
field_name:
field_value:
source_id:
source_title:
source_year:
source_url_or_identifier:
evidence_type:
evidence_quality:
recommendation_strength:
known_conflicts:
clinical_applicability:
review_date:
editorial_status:
editorial_reviewer:
scientific_validation_status:
semantic_validation_status:
knowledge_version:
semantic_version:
publication_version:
trace_id:
```

## Status Permitidos

- draft;
- awaiting validation;
- validated;
- deprecated;
- conflicting evidence.

## Regra

Nenhum `field_value` pode ser considerado oficial se qualquer metadado obrigatorio estiver ausente.

## Declaracao Final

A rastreabilidade por campo e obrigatoria para impedir conhecimento clinico opaco.

