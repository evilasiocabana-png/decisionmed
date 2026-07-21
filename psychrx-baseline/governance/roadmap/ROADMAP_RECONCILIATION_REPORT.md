# Roadmap Reconciliation Report

## Objetivo

Registrar a reconciliacao entre o estado atual da documentacao do PsychRx e o roadmap enterprise definido pelo CTO.

## Documentos Existentes Identificados

Foram identificados documentos numerados de `000` a `051`, alem de `065_DEPENDENCY_AUDIT.md`.

Tambem existem documentos duplicados por numero entre `007` e `015`, criados em fases anteriores do projeto.

## Arquivos Ja Existentes

Exemplos de documentos ja existentes:

- `000_MANIFEST.md`
- `001_CONSTITUICAO_CLINICA.md`
- `002_PRINCIPIOS_ARQUITETURAIS.md`
- `003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `004_MODELO_DO_PACIENTE.md`
- `005_MODELO_DO_PSICOFARMACO.md`
- `006_FLUXO_DE_DECISAO_CLINICA.md`
- `031_DOMAIN_MODEL.md`
- `040_KNOWLEDGE_COMPUTING_ARCHITECTURE.md`
- `050_ENGINEERING_BLUEPRINT.md`
- `051_DOMAIN_IMPLEMENTATION_SPEC.md`
- `065_DEPENDENCY_AUDIT.md`

## Inconsistencias Encontradas

1. Alguns arquivos `.md` fundadores exibem conteudo binario de Word quando lidos diretamente como texto.
2. Existem numeros duplicados em documentos diferentes, especialmente entre `007` e `015`.
3. O roadmap novo redefine faixas de missoes, mas o projeto ja possui documentos criados na numeracao anterior.
4. A lacuna `052-064` existe no repositorio documental atual.
5. O documento `065_DEPENDENCY_AUDIT.md` existe fora da sequencia enterprise proposta.

## Decisao de Reconciliacao

Os documentos existentes nao foram renomeados nem sobrescritos.

A nova organizacao enterprise foi registrada em `ROADMAP_ENTERPRISE.md`.

A decisao estrutural foi registrada em `docs/adr/0003_ROADMAP_ENTERPRISE.md`.

Os documentos novos dos Sprints 14-17 foram criados nas faixas `112-143`, porque essas missoes estavam explicitamente definidas no anexo e ainda nao existiam.

## Documentos Criados Nesta Atualizacao

- `ROADMAP_ENTERPRISE.md`
- `ROADMAP_RECONCILIATION_REPORT.md`
- `docs/adr/0003_ROADMAP_ENTERPRISE.md`
- `112_CLINICAL_WORKFLOW.md` ate `143_API_BASELINE.md`

## Pendencias

- Converter ou substituir com cautela os `.md` que contem binario de Word.
- Definir ADR para qualquer renumeracao retroativa.
- Decidir se `065_DEPENDENCY_AUDIT.md` sera mantido como documento historico ou remapeado em uma faixa futura.
- Criar missoes futuras para `144-259` apenas quando o CTO liberar os respectivos sprints.

## Proximos Passos Recomendados

1. Criar ADR sobre a adocao do Roadmap Enterprise.
2. Criar uma matriz de equivalencia entre documentos antigos e faixas novas.
3. Congelar documentos fundadores antes de qualquer renumeracao.
4. Executar proximos sprints com uma missao por documento.

## Declaracao Final

A reconciliacao preserva o historico existente, evita sobrescrita de documentos fundadores e cria uma base clara para a evolucao enterprise do PsychRx.
