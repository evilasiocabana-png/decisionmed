# DM-020 — Schemas governados de formulário clínico

## Objetivo

Criar o contrato técnico que permitirá formulários diferentes por especialidade
sem colocar significado clínico, regra ou evidência dentro da interface.

## Garantias

- cada campo aponta para um `KnowledgeObject` registrado;
- `KnowledgeObject` continua ligado a `EvidenceSource`;
- schema validado exige revisão humana e conhecimento validado;
- tipo, seção e opções são imutáveis e versionados;
- nenhuma definição ou schema libera execução clínica;
- esta missão não popula campos reais de nenhuma especialidade.

## Fluxo futuro

`EvidenceSource -> KnowledgeObject -> ClinicalFieldDefinition -> SpecialtyFormSchema`

Somente após validação científica e humana os schemas poderão ser considerados
por uma missão posterior de runtime. A interface continuará consumindo contratos
da aplicação, nunca o catálogo de conhecimento diretamente.

## Reversão

Remover os contratos, registry, exports e testes. Não há persistência ou migração.
