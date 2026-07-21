# A01-001 - Scientific Knowledge Schema

## Objetivo

Definir o schema oficial da Base de Conhecimento Cientifico do PsychRx.

## Entidades Suportadas

- Drug
- Mechanism
- Receptor
- Diagnosis
- Syndrome
- Symptom
- Therapeutic Goal
- Constraint
- Interaction
- Contraindication
- Monitoring
- Evidence
- Guideline
- Reference

## Campos Obrigatorios

- semantic version;
- scientific version;
- traceability;
- editorial review;
- knowledge lifecycle.

## Implementacao Estrutural

O schema foi criado em `scientific_knowledge/schema/scientific_schema.py` e nos modelos imutaveis de `scientific_knowledge/models/knowledge_models.py`.

## Restricoes

Nenhum conteudo clinico real foi populado.

## Declaracao Final

O schema cientifico oficial existe como contrato estrutural, nao como biblioteca clinica validada.

