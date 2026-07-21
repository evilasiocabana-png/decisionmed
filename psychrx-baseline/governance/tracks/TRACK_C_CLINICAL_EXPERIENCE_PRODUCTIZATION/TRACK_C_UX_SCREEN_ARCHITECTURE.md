# Track C UX Screen Architecture

## Status

Governed implementation specification.

## Primary Screen

The primary screen is the Consultation Room.

It is organized as:

```text
Patient speech
↓
Read-only session status
↓
Quick filters
↓
Consultation flow
↓
Reasoning filters
↓
Clinical workbench
↓
Operational summary
```

## Clinical Workbench Panels

### 01 - Hoje

Captures the current reason for consultation, distress, functionality, current symptoms and symptoms that must be investigated.

### 02 - Estado Clinico

Organizes stability, response, clinical context, changes since the prior encounter and observed signs.

### 03 - Seguranca e Plano

Keeps safety categories visible and organizes current treatment context, follow-up and objectives.

This panel does not prescribe, suggest dose, select medication or rank treatment options.

## Secondary Reference Area

The following areas are secondary and must remain outside the primary consultation flow:

- safety contract details;
- Clinical Operating Mind conceptual flow;
- official component catalog;
- conceptual dashboard panels;
- enterprise roadmap;
- Clinical Widget Library.

These are grouped under:

```text
Referencia tecnica e governanca
```

## Responsive Rule

On smaller screens, all main consultation regions stack vertically. Horizontal scrolling is forbidden for the primary workflow.

## Clinical Safety Boundary

The screen is allowed to organize information. It is not allowed to decide conduct.

