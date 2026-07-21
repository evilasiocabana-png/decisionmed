# R01 Program Conversion Matrix

## Mission

R01-003 - ROADMAP_MIGRATION_EXECUTION_PLAN.

## Matrix

| Current Program | New Pipeline / Framework | Migration Status | Strategy | Risk | Priority |
| --- | --- | --- | --- | --- | --- |
| 00 Governance | Governance Foundation | Preserve | Keep explicit | Low | High |
| 01 Scientific Architecture | Clinical Architecture Framework | Preserve | Map as foundation | Low | High |
| 02 Clinical Operating Mind | Clinical Architecture + Runtime Shell | Map | Preserve concepts, separate runtime | Medium | High |
| 03 Knowledge Graph | Knowledge Framework | Map | Represent graph as knowledge framework concern | Medium | Medium |
| 04 Engineering Blueprint | Software Platform Framework | Map | Preserve as implementation guide | Low | Medium |
| 05 Clinical Kernel | Clinical Runtime Shell | Map | Keep kernel read-only until gates | Medium | High |
| 06 Software Platform | Software Platform Framework | Preserve | Keep baseline | Low | High |
| 07 Clinical Workspace | Clinical Workspace Framework | Preserve | Keep explicit product layer | Low | High |
| 08 Clinical Kernel Integration | Clinical Runtime Shell | Map | Represent integration under runtime shell | Medium | High |
| 09 Knowledge Population | Knowledge Framework + DrugClassPopulationPipeline | Map | Split framework and scientific population | Medium | High |
| 10 Clinical Runtime | Clinical Runtime Shell | Preserve | Keep read-only runtime baseline | Medium | High |
| 11 Safety Engine | SafetyPipeline + Clinical Release Governance | Map | Preserve hard gates | High | High |
| 12 Evidence Runtime | EvidencePipeline | Map | Preserve traceability | High | High |
| 13 Therapeutic Optimization | Clinical Release Governance | Defer | Keep prohibited until release decision | High | High |
| 14 Clinical Explanation | Clinical Release Governance | Preserve | Keep explainability as release requirement | Medium | High |
| 15 Clinical Snapshot | Clinical Runtime Shell | Map | Preserve as runtime component | Medium | Medium |
| 16 Clinical Timeline | Workspace + Runtime Shell | Map | Split presentation and runtime | Medium | Medium |
| 17 Clinical Navigation | Workspace + Runtime Shell | Map | Keep non-prescriptive | Medium | Medium |
| 18 Clinical Operating Mind | Clinical Architecture + Runtime Shell | Preserve | Keep conceptual and runtime split | Medium | High |
| 19 Clinical Quality | QA and Publication | Map | Move to QA governance | Medium | High |
| 20 Clinical Research | Clinical Release Governance | Defer | Preserve strategic intent | Medium | Low |
| 21 Scientific Validation | QA and Publication | Map | Preserve as scientific validation gate | High | High |
| 22 Knowledge Governance | Knowledge Framework + QA | Map | Preserve semantic governance | High | High |
| 23 Digital Clinical Twin | Clinical Release Governance | Defer | Preserve as future strategic platform | High | Low |
| 24 Clinical Simulation | Clinical Release Governance | Defer | Preserve as future strategic platform | High | Low |
| 25 Clinical Intelligence | Clinical Release Governance | Defer | Preserve behind release governance | High | Low |
| 26 Platform Maturity | Clinical Release Governance | Preserve | Keep certification gate | Medium | High |
| X01 Execution Protocol | Governance Foundation | Preserve | Keep state-driven protocol binding | Low | High |
| A01 Official Scientific Knowledge Base | Knowledge Framework | Map | Preserve schemas | Low | High |
| A02 Psychopharmacology Library | Knowledge Framework + Portfolio Pipeline | Map | Preserve metadata-only foundation | Medium | High |
| A02.5 SSRI Corpus | CorpusPipeline[SSRIs] | Migrated | Historical execution preserved | Low | Medium |
| A03 SSRIs | DrugClassPopulationPipeline[SSRIs] | Migrated | Preserve internal draft package | Medium | Medium |
| A04.0 SNRI Corpus | CorpusPipeline[SNRIs] + ValidationPipeline[SNRIs] | Migrated Pending | Resume paused validation after R01 approval | Medium | High |
| A04 SNRIs | DrugClassPopulationPipeline[SNRIs] | Migrated Pending | Execute after SNRI corpus gate | Medium | High |
| A05 NDRIs | DrugClassPopulationPipeline[NDRIs] | Planned | Execute by parameters | Medium | Medium |
| A06 NaSSAs | DrugClassPopulationPipeline[NaSSAs] | Planned | Execute by parameters | Medium | Medium |
| A07 TCAs | DrugClassPopulationPipeline[TCAs] | Planned | Add high-risk safety gates | High | Medium |
| A08 MAOIs | DrugClassPopulationPipeline[MAOIs] | Planned | Add interaction safety gates | High | Medium |
| A09 Atypical Antidepressants | DrugClassPopulationPipeline[AtypicalAntidepressants] | Planned | Support multimodal mechanisms | Medium | Medium |
| A10 FGAs | DrugClassPopulationPipeline[FGAs] | Planned | Add EPS and safety gates | High | Medium |
| A11 SGAs | DrugClassPopulationPipeline[SGAs] | Planned | Add metabolic monitoring gates | High | Medium |
| A12 Mood Stabilizers | DrugClassPopulationPipeline[MoodStabilizers] | Planned | Add serum-level gates | High | Medium |
| A13 Anxiolytics Hypnotics | DrugClassPopulationPipeline[AnxiolyticsHypnotics] | Planned | Add dependence/withdrawal gates | High | Medium |
| A14 ADHD Medications | DrugClassPopulationPipeline[ADHD] | Planned | Add controlled-substance gates | High | Medium |
| A15 Cognitive Enhancers | DrugClassPopulationPipeline[CognitiveEnhancers] | Planned | Add older-adult safety gates | High | Medium |

## Status Legend

- Preserve: stays explicit.
- Map: becomes represented by a framework or pipeline.
- Defer: remains future strategic capability, not active execution.
- Migrated: historical work maps cleanly.
- Migrated Pending: mapped but requires R01-004 approval.
- Planned: future pipeline execution.

## Final Declaration

Every current program has a preservation, mapping, deferral or planned execution strategy. No program is silently removed.
