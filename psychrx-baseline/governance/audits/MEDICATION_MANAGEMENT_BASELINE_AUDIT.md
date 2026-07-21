# Medication Management Baseline Audit

Mission: PSYCHRX_MISSAO_UNICA_FLUXO_MANEJO_MEDICAMENTOSO

Scope: Phase 1 baseline audit only. No implementation was performed in this
phase because the mission explicitly blocks code changes before this audit.

## Executive Summary

The repository already contains a usable local consultation app, a structured
decision-support contract, a local deterministic rule table, and a unified motor
workbook reader. The current implementation can collect a compact clinical
state, current medication entries, safety answers, and functional impairment,
then return a local table-based decision-support response.

The repository does not yet contain the complete longitudinal medication
management workflow requested by the mission. The missing parts are mainly:
explicit medication-management domain entities, adequate-trial evaluation,
medication problem classification, persistent consultation history, longitudinal
monitoring, reassessment loops, and audited lifecycle transitions from motor
advice to physician final decision.

The current state should therefore be treated as a functional local decision
support prototype, not as the final medication management system.

## Required Baseline Questions

### 1. Onde os dados do paciente entram?

Patient and consultation inputs enter through the local web UI in
`interfaces/web/static/index.html` and `interfaces/web/static/app.js`.

The UI sends structured data to `POST /api/decision-support`, implemented in
`interfaces/web/server.py`. The request is handled by
`application.clinical_decision_support_service.ClinicalDecisionSupportService`.

Current captured fields include patient label, birth date, diagnostic context,
clinical state, symptoms, observed signs, impairment domains, impairment
severity, stability, comorbidities, current medications, and safety answers.

### 2. Existe contexto clinico real ou contexto vazio?

There is a partial clinical context. The interface captures a clinical context
and current state, but this context is not yet represented as a full domain
ClinicalContext aggregate with lifecycle, validation, persistence, and audit.

### 3. O Snapshot e construido a partir da interface?

Not fully. The UI has snapshot-like presentation and the application layer has
structural view models, but there is no complete Clinical Snapshot update
pipeline fed directly from the consultation interface and persisted across
visits.

### 4. O tratamento atual e representado?

Partially. Current treatment is represented in the decision-support contract by
`CurrentMedicationPayload` with name, dose value, unit, frequency, duration,
adherence, response, and tolerability. It is not yet a full domain
MedicationEpisode with indication, route, start date, change history, and
longitudinal response tracking.

### 5. O historico farmacologico e representado?

No complete pharmacological history exists. The current app captures current
medications and limited previous-prescription context in the UI, but there is no
MedicationTrial, MedicationHistory, failed-trial registry, or longitudinal
medication timeline.

### 6. Dose, tempo, adesao, resposta e tolerabilidade sao avaliados?

Partially. The UI collects dose, frequency, duration, adherence-related safety,
response, and tolerability fields. The local rule table uses only a small part
of this information. There is no formal adequate-trial evaluator that determines
whether dose, time, adherence, and tolerability are sufficient before declaring
non-response or failure.

### 7. Existe classificacao do problema medicamentoso?

No explicit medication problem taxonomy exists. The current rule table maps
stability and safety into broad actions such as maintain, optimize, increase,
substitute, or investigate before change. It does not classify problems such as
subtherapeutic dose, inadequate duration, poor adherence, intolerance, adverse
effect, interaction, relapse, partial response, no response, or diagnostic
uncertainty as first-class objects.

### 8. O Safety Engine recebe dados reais?

Partially. The UI captures safety answers and the local decision-support rule
table blocks unsafe scenarios. Structural Safety Engine packages and tests exist,
but the production app endpoint does not yet route real consultation state
through a complete Safety Engine lifecycle with constraints, risks, trace,
blocking decision, and audit persistence.

### 9. A base farmacologica esta ligada ao caso clinico?

Partially. The local motor is linked through:

- `knowledge_base/decision_support_engine/tables/Tabela_Motor_Unificada_audit_evilasio.xlsx`
- `application.motor_table_repository.MotorTableRepository`
- `application.medication_strategy_table.MedicationStrategyTable`
- `application.decision_support_rule_table.DecisionSupportRuleTable`

This provides table-based candidates, targets, cautions, dose ranges, and local
citations. It is not yet a full scientific evidence runtime with source section
traceability, review state, and runtime eligibility.

### 10. O sistema compara estrategias reais?

Partially. The local motor can output strategy families and candidate options,
but it does not yet perform a full strategy comparison across maintain,
optimize, substitute, associate, taper, withdraw, monitor, or investigate using
an explicit Therapeutic Optimization Engine.

### 11. Existe persistencia por paciente e consulta?

No. The local app is currently request/response and in-memory/browser-state
oriented. There is no patient consultation repository, database, file-backed
session store, or audit-persistent medication management record.

### 12. Existe monitorizacao longitudinal?

No complete longitudinal monitoring exists. The app can display monitoring
targets in the response, but there is no Clinical Timeline or Medication
Timeline that stores follow-up dates, response checkpoints, adverse effects,
labs, scales, or reassessment outcomes.

### 13. A reavaliacao atualiza o Snapshot?

No. Reassessment is not yet implemented as a closed loop that updates the
Clinical Snapshot and opens a new medication-management cycle.

### 14. Quais componentes sao apenas estruturais/read-only?

Structural or mostly read-only components include:

- App view model and clinical workspace cards in `application/app_service.py`.
- Clinical Kernel, Safety Engine, Evidence Runtime, Therapeutic Optimization,
  Clinical Snapshot, Clinical Timeline, and related governance/test packages.
- Program/track governance documents that define future capabilities but do not
  activate clinical runtime behavior.

### 15. Quais componentes estao bloqueados por governanca?

The following remain blocked unless a specific governed mission unlocks them:

- Autonomous prescription.
- Autonomous patient-specific medication selection.
- Dose recommendation as an order.
- Clinical runtime activation as a decision engine.
- Therapeutic recommendation without source traceability and safety gate.
- Scientific content extraction outside approved source-section gates.
- Runtime use of draft scientific knowledge.

### 16. Existem duplicacoes, fluxos mortos ou abstracoes sem uso?

Yes. The repository has accumulated several governance layers and historical
roadmap states. Some documents still describe earlier read-only phases while the
local app now includes a table-based decision-support prototype. There is also a
split between structural application widgets and the newer local motor pathway.

The most important practical duplication is that the app has both:

- static/structural clinical workspace content; and
- dynamic decision-support output from the local motor.

These should be reconciled in the next implementation phase so the workflow is
single, click-first, and state-driven.

## Baseline Conclusion

The project has enough material to start the medication-management build, but
not by skipping straight to a full motor. The safe next step is to create the
explicit medication-management domain/application model around the flow already
visible in the UI and local table motor.

Implementation remains blocked until this baseline audit is accepted or the
next governed mission explicitly authorizes Phase 2.
