# Medication Management Flow Map

Mission: PSYCHRX_MISSAO_UNICA_FLUXO_MANEJO_MEDICAMENTOSO

Scope: current-state flow mapping before implementation.

## Current Executable Flow

```text
Physician clicks consultation fields
        |
        v
interfaces/web/static/index.html
        |
        v
interfaces/web/static/app.js
        |
        v
buildDecisionSupportRequest()
        |
        v
POST /api/decision-support
        |
        v
interfaces/web/server.py
        |
        v
ClinicalDecisionSupportService.build_response()
        |
        v
DecisionSupportRuleTable.build()
        |
        v
MedicationStrategyTable
        |
        v
MotorTableRepository
        |
        v
knowledge_base/decision_support_engine/tables/
Tabela_Motor_Unificada_audit_evilasio.xlsx
        |
        v
ClinicalDecisionSupportResponse
        |
        v
renderDecisionSupportResponse()
        |
        v
Conselho do motor in the local app
```

## Current Inputs

The current UI collects:

- patient label;
- birth date;
- diagnostic context, if known;
- current clinical state;
- symptoms;
- observed signs;
- functional impairment domains;
- impairment severity;
- clinical stability;
- comorbidities;
- current medication list;
- dose number and unit;
- frequency;
- treatment duration;
- safety answers;
- physician final decision fields.

## Current Outputs

The current local motor can return:

- suggested direction;
- clinical rationale;
- impairment targets;
- substitution candidates;
- association candidates;
- evidence/citation text from local tables;
- pharmacological target;
- therapeutic dose target text;
- safety warnings;
- confidence status;
- prescription boundary.

## Target Flow From Mission

```text
ABRIR CONSULTA
      |
      v
IDENTIFICAR MOMENTO TERAPEUTICO
      |
      v
RECONCILIAR MEDICACOES ATUAIS
      |
      v
RECONSTRUIR HISTORICO FARMACOLOGICO
      |
      v
AVALIAR DOSE + TEMPO + ADESAO + RESPOSTA + TOLERABILIDADE
      |
      v
CLASSIFICAR O PROBLEMA MEDICAMENTOSO
      |
      v
EXECUTAR BARREIRA DE SEGURANCA
      |
      v
DEFINIR OBJETIVO COM O MEDICO
      |
      v
COMPARAR ESTRATEGIAS
      |
      v
COMPARAR OPCOES FARMACOLOGICAS
      |
      v
MEDICO SELECIONA A CONDUTA
      |
      v
REGISTRAR PLANO DE IMPLEMENTACAO
      |
      v
GERAR PLANO DE MONITORIZACAO
      |
      v
REAVALIAR
      |
      v
ATUALIZAR CLINICAL SNAPSHOT
      |
      v
REGISTRAR AUDITORIA E NOVO CICLO
```

## Gap Between Current and Target

The current app starts around "collect current state" and jumps directly to a
local table-based response. The target flow requires several intermediate
objects and checkpoints that do not yet exist as executable components.

Missing executable checkpoints:

- therapeutic moment classification;
- medication reconciliation as a formal object;
- pharmacological history reconstruction;
- adequate trial assessment;
- medication problem classification;
- full Safety Engine execution with trace;
- explicit therapeutic objective selection;
- strategy comparison;
- pharmacological option comparison;
- physician decision persistence;
- implementation plan;
- monitoring plan;
- reassessment cycle;
- Clinical Snapshot update;
- audit trail.

## Current Data Objects

Existing or partial:

- `ClinicalDecisionSupportRequest`
- `CurrentMedicationPayload`
- `ClinicalSafetyPayload`
- `ClinicalDecisionSupportResponse`
- `MedicationStrategyEntry`
- `MotorTableEntry`
- `RuleTableContext`

Missing:

- Patient domain entity for medication management.
- Consultation aggregate.
- MedicationEpisode.
- MedicationTrial.
- MedicationReconciliation.
- TherapeuticMoment.
- AdequateTrialAssessment.
- MedicationProblem.
- SafetyGateResult.
- TherapeuticObjective.
- StrategyComparison.
- PharmacologicalOptionComparison.
- PhysicianDecision.
- ImplementationPlan.
- MonitoringPlan.
- Reassessment.
- MedicationManagementAuditEntry.

## Safety Flow

Current safety behavior:

```text
UI safety answers -> RuleTableContext.safety -> _safety_warnings()
-> blocked response when unsafe or incomplete
```

Target safety behavior:

```text
UI safety answers -> normalized safety state -> Safety Engine
-> risks + constraints + blocking decision + trace + audit
-> downstream strategy gate
```

## Table Motor Flow

Current motor data source:

```text
Tabela_Motor_Unificada_audit_evilasio.xlsx
```

Current reader:

```text
application/motor_table_repository.py
```

Current usage:

```text
find current medication
find substitution candidates
find association candidates
return local citation to table row
```

Target usage:

```text
table motor + source evidence + safety + adequate trial + clinical objective
-> strategy comparison
-> option comparison
-> physician-facing explanation
-> monitoring and reassessment plan
```

## Flow Decision

The current flow is sufficient to build from, but not sufficient to claim the
full medication management cycle. The next phase should not rewrite the app from
zero. It should formalize the existing click-first consultation path into
explicit application/domain objects, then route the existing local table motor
through those objects.
