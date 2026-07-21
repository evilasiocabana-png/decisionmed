# 000 Manifest - PsychRx

## Identidade

PsychRx e uma plataforma de apoio ao raciocinio medico em psicofarmacologia.

O PsychRx nao substitui o medico.

O PsychRx nao prescreve.

O PsychRx nao responde casos clinicos como ferramenta assistencial autonoma.

O PsychRx organiza dados clinicos, identifica riscos, compara estrategias, explicita incertezas e apoia a explicacao do raciocinio.

## Estado Atual

Data desta atualizacao: 2026-07-03

Versao documental: 0.5

Status: em construcao documental enterprise, com app localhost read-only funcional, Program A03 concluido como pacote cientifico interno draft para SSRIs, Program A04.0 concluido como corpus cientifico SNRI controlado e Program A04 ativo com bloqueio pre-extracao por falta de selecao de secoes de fonte.

## Principios Fundadores

1. Paciente no centro.
2. Medico como decisor final.
3. Raciocinio antes de estrategia.
4. Seguranca clinica como primeira camada.
5. Nenhuma estrategia sem justificativa.
6. Nenhuma informacao clinica sem fonte rastreavel.
7. Conhecimento cientifico separado de algoritmo.
8. Arquitetura modular.
9. Rastreabilidade total.
10. Explicabilidade obrigatoria.

## Limites Clinicos

O PsychRx nunca deve:

- prescrever automaticamente;
- escolher conduta pelo medico;
- ocultar incertezas;
- apresentar recomendacao sem justificativa;
- apresentar regra terapeutica sem fonte cientifica;
- misturar evidencia cientifica com logica executavel;
- permitir que interface decida conduta;
- contornar a camada de seguranca clinica.

## Arquitetura Oficial

Camadas oficiais:

```text
docs/
domain/
knowledge/
evidence/
clinical_kernel/
reasoning/
safety/
application/
clinical_experience/
interfaces/
adapters/
infrastructure/
audit/
tests/
```

## Clinical Experience Layer

A `Clinical Experience Layer` e camada oficial da arquitetura.

Funcao: transformar o raciocinio do PsychRx em uma experiencia rapida, silenciosa e util durante a consulta.

Ela organiza a consulta.

Ela nao decide conduta.

Ela nao prescreve.

Componentes oficiais:

```text
clinical_experience/
â”œâ”€â”€ consultation_room/
â”œâ”€â”€ clinical_card_stack/
â”œâ”€â”€ guided_anamnesis/
â”œâ”€â”€ live_question_panel/
â”œâ”€â”€ symptom_capture/
â”œâ”€â”€ strategy_panel/
â”œâ”€â”€ risk_panel/
â”œâ”€â”€ monitoring_timeline/
â”œâ”€â”€ evidence_summary/
â””â”€â”€ patient_friendly_mode/
```

## Interfaces Oficiais

Superficies de apresentacao conceitual:

```text
interfaces/
â”œâ”€â”€ desktop_dashboard/
â”œâ”€â”€ tablet_view/
â”œâ”€â”€ mobile_view/
â””â”€â”€ web/
```

As interfaces apresentam resultados vindos da aplicacao e da experiencia clinica. Interfaces nao criam regra clinica, nao interpretam evidencia e nao decidem conduta.

## App Localhost

O projeto possui um app local funcional em:

```text
http://127.0.0.1:8765/
```

Estado do app:

- read-only;
- sem prescricao;
- sem motor clinico;
- sem IA;
- sem banco de dados;
- sem dados reais de pacientes;
- com Clinical Experience Layer visivel;
- com contrato de seguranca clinica visivel.

## Roadmap Enterprise

O roadmap enterprise passa a orientar a evolucao do PsychRx.

Documentos relacionados:

- `docs/MASTER_DEVELOPMENT_PLAN.md`
- `docs/PROJECT_CHARTER.md`
- `docs/PROJECT_INDEX.md`
- `docs/PROJECT_TREE.md`
- `docs/PROJECT_PROGRESS.md`
- `docs/PROJECT_STATUS.md`
- `docs/NEXT_MISSION.md`
- `docs/ROADMAP_ENTERPRISE.md`
- `docs/ROADMAP_RECONCILIATION_REPORT.md`
- `docs/adr/0003_ROADMAP_ENTERPRISE.md`
- `docs/adr/0007_MASTER_DEVELOPMENT_PLAN.md`

## Master Development Plan

O `MASTER_DEVELOPMENT_PLAN.md` passa a ser o plano diretor de execucao do PsychRx.

Ele governa a decomposicao por volumes, programas, fases, sprints e missoes.

Ele nao substitui a Constituicao Clinica, o Manifesto, os Principios Arquiteturais, a Ontologia ou os ADRs aprovados.

O MDP fica acima do roadmap como plano de desenvolvimento e governanca executiva, enquanto o roadmap permanece como mapa sequencial resumido.

Trilhas paralelas oficiais:

1. Arquitetura e Engenharia.
2. Conhecimento Cientifico.
3. Experiencia Clinica.
4. Qualidade e Governanca.
5. Inteligencia Clinica.

## Track A - Scientific Knowledge Expansion

O Track A organiza a expansao da Base Oficial de Conhecimento Cientifico.

Estado atual:

- Program A01 concluido como base estrutural oficial de conhecimento cientifico.
- Program A02 concluido como biblioteca psicofarmacologica metadata-only.
- Program A02.5 concluido como ingestao, normalizacao administrativa, validacao estrutural, registro editorial e publicacao controlada do corpus SSRI.
- Program X01 concluido como Project Execution Protocol e sistema operacional de execucao governada.
- Program A03 concluido como pacote cientifico interno draft para SSRIs.
- A03 consolidou portfolio SSRI, modelos cientificos estruturais, mecanismos, farmacocinetica, farmacodinamica, evidencia metadata-only, QA e pacote interno de publicacao.
- O pacote A03 permanece draft, interno, nao publicado para runtime e nao consumivel clinicamente.
- Program A04.0 concluido como SNRI Scientific Corpus, com discovery, catalogo, intake, metadata normalization, validation, editorial registration, corpus publication e completion gate.
- Program A04 foi desbloqueado para continuacao governada da Scientific Content Population de SNRIs.
- A04 criou o portfolio metadata-only de SNRIs: Venlafaxine, Desvenlafaxine, Duloxetine, Levomilnacipran e Milnacipran.
- A04-003 reconciliou a dependencia de corpus, A04-004 definiu o plano de execucao, A04-005 criou profile shells vazios, A04-006 criou o source anchor plan e A04-007 criou a matriz de rastreabilidade campo-fonte.
- A04-008 avaliou os gates de extracao e bloqueou A04-009.
- A04-008A criou anchors administrativos definitivos para droga-campo.
- A04-008B criou o pacote de protocolo de extracao e manteve A04-009 bloqueada por falta de selecao de secoes de fonte.
- A04-008C registrou o bloqueio por ausencia de secoes selecionaveis locais.
- A04-008D registrou locators de textos-fonte.
- A04-008E criou o plano de locators de secoes.
- A04-008F confirmou o gate oficial com zero secoes selecionadas, zero secoes revisaveis e A04-009 impedida de iniciar.
- A04 esta ativo em `BLOCKED - A04_SOURCE_SECTION_SELECTION_REQUIRED`.
- O proximo passo autorizado e resolver formalmente a cadeia Fonte especifica -> Secao especifica -> Campo do psicofarmaco -> Conteudo revisavel antes de qualquer populacao de mecanismo, PK, PD, safety, evidencia, QA ou publicacao.

Limites permanentes do Track A:

- nenhum conhecimento pode ser publicado sem rastreabilidade;
- nenhum campo cientifico pode ser exposto ao runtime antes de gate editorial e cientifico;
- nenhuma recomendacao terapeutica pode nascer na Knowledge Base;
- nenhuma prescricao pode ser criada;
- nenhuma regra executavel pode ser misturada com conhecimento cientifico.
- nenhum programa de nova classe farmacologica pode popular campos cientificos antes de seu corpus especifico.

## Decisoes Arquiteturais Registradas

- `docs/adr/0001_GOVERNANCA_ARQUITETURAL.md`
- `docs/adr/0002_SEPARACAO_PLATFORM_KNOWLEDGE.md`
- `docs/adr/0003_ROADMAP_ENTERPRISE.md`
- `docs/adr/0004_LOCALHOST_APP_SHELL.md`
- `docs/adr/0005_CLINICAL_EXPERIENCE_LAYER.md`
- `docs/adr/0006_MANIFEST_MARKDOWN_REPAIR.md`
- `docs/adr/0007_MASTER_DEVELOPMENT_PLAN.md`
- `docs/adr/0045_A03_PHASE3_REFACTORED_DRUG_SCIENTIFIC_MODELING.md`
- `docs/adr/0046_PROJECT_EXECUTION_PROTOCOL.md`
- `docs/adr/0047_A03_SCIENTIFIC_KNOWLEDGE_ACQUISITION_LAYER.md`
- `docs/adr/0048_AUTO_EXECUTION_PROTOCOL.md`

## Documentos de Referencia Atual

- `docs/001_CONSTITUICAO_CLINICA.md`
- `docs/002_PRINCIPIOS_ARQUITETURAIS.md`
- `docs/003_ONTOLOGIA_PSICOFARMACOLOGIA.md`
- `docs/004_MODELO_DO_PACIENTE.md`
- `docs/005_MODELO_DO_PSICOFARMACO.md`
- `docs/006_FLUXO_DE_DECISAO_CLINICA.md`
- `docs/LAYER_DEPENDENCY_RULES.md`
- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `docs/CLINICAL_SAFETY_CONTRACT.md`
- `docs/EVIDENCE_TRACEABILITY_POLICY.md`
- `docs/CLINICAL_EXPERIENCE_LAYER.md`
- `docs/LOCALHOST_APP.md`
- `docs/MASTER_DEVELOPMENT_PLAN.md`
- `docs/PROJECT_CURRENT_STATE.md`
- `docs/PROGRAM_A03_COMPLETION_REPORT.md`
- `docs/PROGRAM_A04_0_COMPLETION_REPORT.md`
- `docs/PROGRAM_A04_STATUS.md`
- `docs/A04_003_SNRI_SOURCE_CORPUS_INTAKE_RECONCILIATION.md`
- `docs/A04_004_SNRI_POPULATION_EXECUTION_PLAN.md`
- `docs/A04_005_SNRI_PROFILE_SHELLS.md`
- `docs/A04_006_SNRI_SOURCE_ANCHOR_PLAN.md`
- `docs/A04_007_SNRI_FIELD_TRACEABILITY_MATRIX.md`
- `docs/A04_008_SNRI_EXTRACTION_GATES.md`
- `docs/A04_008A_SNRI_SOURCE_ANCHOR_FINALIZATION.md`
- `docs/A04_008B_SNRI_EXTRACTION_PROTOCOL_PACKAGE.md`
- `docs/A04_008C_SNRI_SOURCE_SECTION_SELECTION_OR_BLOCKER.md`
- `docs/A04_008D_SNRI_SOURCE_TEXT_ACQUISITION_PACKAGE.md`
- `docs/A04_008E_SNRI_SOURCE_SECTION_LOCATOR_PLAN.md`
- `docs/A04_008F_SNRI_SOURCE_SECTION_SELECTION_GATE.md`
- `docs/NEXT_MISSION.md`

## Status por Area

| Area | Status |
| --- | --- |
| Governanca arquitetural | Criada |
| Fundacao clinica | Criada |
| Arquitetura cientifica | Criada |
| Motores conceituais | Documentados |
| Nucleo do raciocinio clinico | Documentado |
| Knowledge Layer | Estrutura inicial criada |
| Domain Layer | Estrutura inicial criada |
| Clinical Experience Layer | Oficializada |
| Localhost App | Funcional read-only |
| API clinica real | Nao iniciada |
| Persistencia | Nao iniciada |
| IA clinica | Nao iniciada |
| Prescricao automatica | Proibida |
| Track A - Program A03 | Concluido como pacote cientifico interno draft para SSRIs |
| Track A - Program A04.0 | Concluido como SNRI Scientific Corpus controlado |
| Track A - Program A04 | Ativo; A04-009 bloqueada; estado atual BLOCKED - A04_SOURCE_SECTION_SELECTION_REQUIRED; zero secoes selecionadas e zero secoes revisaveis |

## Inconsistencias Conhecidas

- Alguns documentos antigos com extensao `.md` ainda podem conter conteudo binario de Word.
- Existem duplicidades de numeracao herdadas das fases iniciais.
- A lacuna documental `052-064` ainda existe.
- `065_DEPENDENCY_AUDIT.md` existe como documento historico fora da nova sequencia enterprise.

Essas inconsistencias devem ser tratadas por ADRs especificas antes de renumeracao ou reescrita ampla.

## Regra de Evolucao

Toda nova missao deve:

- ter objetivo claro;
- ter escopo limitado;
- respeitar documentos fundadores;
- respeitar ADRs;
- preservar Clinical Safety;
- preservar Evidence Traceability;
- incluir testes quando houver software;
- atualizar documentacao proporcional;
- manter medico como decisor final.

## Declaracao Final

O PsychRx existe para apoiar o raciocinio medico em psicofarmacologia com arquitetura segura, conhecimento rastreavel, experiencia clinica util e explicabilidade. Ele deve permanecer assistivo, auditavel e centrado no paciente, sem se tornar prescritor automatico.




