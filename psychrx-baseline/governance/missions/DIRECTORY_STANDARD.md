# Directory Standard - SSRI Knowledge Base

## Purpose

Define the standard directory structure for every SSRI in the Program A03 Knowledge Base.

## Standard Drug Directory

Each core SSRI must have one root directory under:

```text
KnowledgeBase/SSRIs/
```

## Standard Sections

Every drug directory must contain exactly the same section directories:

- Identification;
- Mechanism;
- Pharmacokinetics;
- Pharmacodynamics;
- Indications;
- Posology;
- Safety;
- Contraindications;
- Precautions;
- Interactions;
- AdverseEffects;
- Monitoring;
- Evidence;
- Guidelines;
- Editorial;
- Metadata;
- Traceability;
- Manifest.

## Standard Template Files

Every section must contain:

- `README.md`;
- `MANIFEST.json`;
- `STATUS.json`;
- `EDITORIAL_STATUS.json`;
- `TRACEABILITY.json`;
- `METADATA.json`.

## Content Rule

These files are structural placeholders only. They must not contain:

- dose;
- indication;
- mechanism;
- pharmacokinetics;
- pharmacodynamics;
- safety statement;
- interaction;
- contraindication;
- adverse effect;
- monitoring instruction;
- evidence grade;
- recommendation;
- prescription.

## Declaration Final

The SSRI directory standard exists to keep future scientific modeling symmetrical and auditable. It does not authorize content population.
