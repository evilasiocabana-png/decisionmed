# Medication Management Gap Matrix

Mission: PSYCHRX_MISSAO_UNICA_FLUXO_MANEJO_MEDICAMENTOSO

Scope: Phase 1 baseline audit matrix.

Legend:

- Sim: present enough for the current app.
- Parcial: present but incomplete or structural.
- Nao: not implemented as an executable project capability.

| Componente | Existe | Integrado | Executavel | Persistente | Testado | Bloqueios |
|---|---:|---:|---:|---:|---:|---|
| Interface de consulta | Sim | Sim | Sim | Nao | Sim | Needs workflow consolidation and fewer parallel/static blocks. |
| Application layer | Sim | Sim | Sim | Nao | Sim | Current service is request/response, not a full medication-management orchestrator. |
| Clinical Decision Support contract | Sim | Sim | Sim | Nao | Sim | Contract is display-safe but not a full clinical lifecycle model. |
| Clinical Snapshot | Parcial | Parcial | Parcial | Nao | Sim | Snapshot is structural/read-only and not updated by reassessment. |
| Clinical Kernel | Parcial | Parcial | Parcial | Nao | Sim | Kernel structures exist but are not the active medication-management runtime. |
| Safety Engine | Parcial | Parcial | Parcial | Nao | Sim | UI safety gate exists; full engine trace and persistence are not wired to the app flow. |
| Evidence Runtime | Parcial | Parcial | Parcial | Nao | Sim | Evidence structures exist; current motor uses local table citations, not full source-section runtime evidence. |
| Therapeutic Optimization | Parcial | Parcial | Parcial | Nao | Sim | Strategy families exist; full comparison engine is not implemented. |
| Clinical Timeline | Parcial | Parcial | Parcial | Nao | Sim | Timeline is structural and not a persisted follow-up/reassessment loop. |
| Medication Timeline | Nao | Nao | Nao | Nao | Nao | Requires MedicationEpisode, MedicationTrial, reassessment, and monitoring model. |
| Medication reconciliation | Parcial | Parcial | Sim | Nao | Sim | Current medication list exists, but no formal reconciliation object or validation. |
| Pharmacological history | Nao | Nao | Nao | Nao | Nao | No medication history/trial reconstruction. |
| Adequate trial assessment | Nao | Nao | Nao | Nao | Nao | Dose, time, adherence, response, tolerability are collected but not formally evaluated. |
| Medication problem classification | Nao | Nao | Nao | Nao | Nao | No taxonomy for partial response, no response, intolerance, interaction, relapse, etc. |
| Strategy comparison | Parcial | Parcial | Parcial | Nao | Sim | Current rule table selects broad action; no side-by-side strategy comparison. |
| Pharmacological option comparison | Parcial | Parcial | Parcial | Nao | Sim | Candidate lookup exists from table motor; no full comparison or ranking lifecycle. |
| Physician final decision | Parcial | Parcial | Parcial | Nao | Sim | UI fields exist, but decision is not persisted or linked to audit/reassessment. |
| Implementation plan | Nao | Nao | Nao | Nao | Nao | Not modeled yet. |
| Monitoring plan | Parcial | Parcial | Parcial | Nao | Sim | Response can list monitoring targets; no plan object or schedule. |
| Reassessment cycle | Nao | Nao | Nao | Nao | Nao | No loop from follow-up to updated snapshot. |
| Audit trail | Parcial | Parcial | Parcial | Nao | Parcial | Governance logs exist; clinical action audit is not persisted per consultation. |
| Tabelas farmacologicas | Sim | Sim | Sim | Sim | Sim | Local reviewed tables exist; need controlled mapping into domain workflow. |
| Tabela Motor Unificada | Sim | Sim | Sim | Sim | Sim | Workbook reader exists; row-level clinical claims still require careful scope control. |
| Persistence | Nao | Nao | Nao | Nao | Nao | No patient/consultation storage. |
| Tests | Sim | Sim | Sim | Nao aplicavel | Sim | Tests cover structure, UI markers, and current support service; more lifecycle tests needed. |
| Governance | Sim | Sim | Sim | Sim | Parcial | State docs are extensive but have historical drift. |

## Blocking Items Before Full Medication Management

1. Accept this baseline audit.
2. Define medication-management domain/application model.
3. Add a formal medication reconciliation object.
4. Add adequate-trial assessment.
5. Add medication problem classification.
6. Route Safety Engine as a real gate before strategy comparison.
7. Convert current table motor output into a governed comparison workflow.
8. Add persistence or explicitly decide that MVP remains session-only.
9. Add audit entries for motor response and physician final decision.
10. Add reassessment loop to update Clinical Snapshot.

## Phase 1 Decision

The current codebase is ready for Phase 2 only after this audit is reviewed. No
runtime activation, prescription automation, or autonomous medication selection
is authorized by this audit.
