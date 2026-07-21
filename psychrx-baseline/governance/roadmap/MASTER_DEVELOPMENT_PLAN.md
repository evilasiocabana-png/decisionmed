# Master Development Plan - PsychRx

## Status

Documento oficial.

Data: 2026-06-30

Versao: 0.2

Funcao: indice mestre do desenvolvimento do PsychRx.

## 1. Papel do MDP

O Master Development Plan nao e um documento grande de detalhe.

Ele e o indice mestre que organiza o projeto em:

```text
PROGRAM
-> PHASE
-> SPRINT
-> MISSION
-> TASK
```

Os detalhes de cada programa, fase, sprint, missao e tarefa devem ficar em documentos separados.

## 2. Autoridade

O MDP governa a execucao do projeto e fica acima do roadmap como plano diretor de desenvolvimento.

Ele nao substitui:

- Constituicao Clinica;
- Manifesto;
- Principios Arquiteturais;
- Ontologia;
- ADRs aprovados;
- contratos de seguranca, evidencia e rastreabilidade.

Ordem de prevalencia:

1. Constituicao Clinica.
2. Manifesto.
3. Principios Arquiteturais.
4. Ontologia.
5. ADRs aprovados.
6. Master Development Plan.
7. Roadmaps, sprints, missoes e tarefas derivados.

## 3. Documentos Operacionais do MDP

O MDP depende dos seguintes documentos de navegacao e controle:

| Documento | Funcao |
| --- | --- |
| `PROJECT_CHARTER.md` | Porta de entrada executiva do projeto. |
| `PROJECT_INDEX.md` | Indice dos documentos oficiais e sua funcao. |
| `PROJECT_TREE.md` | Arvore PROGRAM -> PHASE -> SPRINT -> MISSION. |
| `PROJECT_PROGRESS.md` | Estado visual de progresso por programa. |
| `PROJECT_STATUS.md` | Estado atual operacional do projeto. |
| `NEXT_MISSION.md` | Proxima missao autorizada para execucao. |
| `PROJECT_DEPENDENCIES.md` | Dependencias entre programas, documentos, camadas e motores. |
| `PROJECT_GLOSSARY.md` | Glossario oficial para reduzir ambiguidade. |
| `PROJECT_KNOWLEDGE_MAP.md` | Mapa dos dominios de conhecimento do PsychRx. |

## 4. Estrutura Enterprise Oficial

```text
PROGRAM
    PHASE
        SPRINT
            MISSION
                TASK
```

Definicoes:

- PROGRAM: grande linha de desenvolvimento.
- PHASE: etapa dentro de um programa.
- SPRINT: ciclo de entrega com objetivo definido.
- MISSION: incremento pequeno, rastreavel e revisavel.
- TASK: acao concreta dentro de uma missao.

## 5. Programas Oficiais

| Program | Nome | Volume |
| --- | --- | --- |
| 00 | Governance | Volume I |
| 01 | Scientific Architecture | Volume I |
| 02 | Clinical Operating Mind | Volume I |
| 03 | Knowledge Graph | Volume I |
| 04 | Drug Intelligence | Volume II |
| 05 | Clinical Kernel | Volume II |
| 06 | Software Platform | Volume II |
| 07 | Clinical Experience | Volume II |
| 08 | Dashboard | Volume III |
| 09 | Mobile | Volume III |
| 10 | Knowledge Population | Volume III |
| 11 | Clinical Reasoning | Volume III |
| 12 | AI | Volume IV |
| 13 | Multiagent | Volume IV |
| 14 | Validation | Volume IV |
| 15 | Production | Volume IV |

## 6. Volumes Oficiais

### Volume I - Governance and Architecture

Programas 00 a 03.

### Volume II - Clinical Knowledge and Clinical Kernel

Programas 04 a 07.

### Volume III - Platform, UX and Applications

Programas 08 a 11.

### Volume IV - AI, Multiagent, Validation and Production

Programas 12 a 15.

## 7. Regras de Expansao

O MDP deve permanecer curto.

Quando um programa precisar de detalhe, criar documento proprio.

Quando uma fase precisar de detalhe, criar documento proprio.

Quando um sprint precisar de detalhe, criar documento proprio.

Quando uma missao precisar ser executada, registrar em `NEXT_MISSION.md`.

## 8. Regra de Execucao

Nenhum agente deve iniciar trabalho sem verificar:

1. `PROJECT_CHARTER.md`
2. `PROJECT_STATUS.md`
3. `PROJECT_TREE.md`
4. `PROJECT_DEPENDENCIES.md`
5. `NEXT_MISSION.md`
6. ADRs relacionados
7. documentos obrigatorios da missao

## 9. Limites Permanentes

O PsychRx nao deve:

- prescrever automaticamente;
- substituir o medico;
- executar decisao clinica sem supervisao medica;
- criar regra terapeutica sem evidencia rastreavel;
- misturar conhecimento cientifico com algoritmo;
- permitir que interface decida conduta;
- ocultar incertezas;
- apresentar estrategia sem justificativa;
- remover explicabilidade;
- remover rastreabilidade.

## 10. Declaracao Final

O Master Development Plan e o indice mestre do sistema operacional de desenvolvimento do PsychRx. Ele nao tenta conter todo o projeto em um unico arquivo. Ele aponta para os documentos certos, preserva a hierarquia enterprise e permite que qualquer agente entre no projeto, descubra o estado atual e execute a proxima missao sem depender de contexto humano informal.
