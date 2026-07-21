# Track C UX Read-Only Components

## Status

Governed implementation catalog.

## Components

### Patient Speech Input

Purpose: capture the patient's current narrative in free text for organization during the visit.

Boundary: not interpreted as diagnosis or recommendation.

### Session Insight

Purpose: summarize active filters, stage and operational confidence.

Boundary: confidence is operational UI completeness only, not diagnostic confidence.

### Quick Filters

Purpose: let the clinician mark common domains such as sleep, mood, anxiety, change and adverse effects.

Boundary: quick filters do not create clinical decisions.

### Consultation Flow

Purpose: show the intended consultation path.

Boundary: flow is navigational, not a clinical protocol.

### Reasoning Filters

Purpose: show the next organizational step and critical missing information.

Boundary: missing information does not block real medical judgment.

### Clinical Workbench

Purpose: organize current state, stability and safety/follow-up in three practical panels.

Boundary: no prescription, no drug ranking, no patient-specific treatment selection.

### Technical Reference

Purpose: preserve architecture and governance visibility without polluting the first consultation experience.

Boundary: reference content is not clinical runtime.

## Non-Prescriptive Language Rule

All user-facing language must use organization verbs:

- registrar;
- organizar;
- revisar;
- acompanhar;
- confirmar;
- investigar.

Forbidden action verbs in autonomous UI behavior:

- prescrever;
- recomendar;
- escolher;
- indicar dose;
- diagnosticar automaticamente.

