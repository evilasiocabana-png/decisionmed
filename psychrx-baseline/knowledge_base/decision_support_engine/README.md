# PsychRx Decision Support Engine Tables

This folder is the working area for the local "motor conselho".

Goal:
- Build the advice engine from explicit tables.
- Make consultation questions emerge from the table requirements.
- Avoid depending on a specialized GPT during clinical use.
- Keep outputs as physician decision support, not autonomous prescribing.

Core idea:

```text
Desired engine output
-> required clinical fields
-> missing field detection
-> question generated for the physician
-> local rule table response
```

Current folders:

- `tables/`: editable CSV tables used to design the engine.
- `schemas/`: column definitions and validation expectations.
- `docs/`: design notes and reverse-engineering workflow.
- `backlog/`: gaps to fill before runtime use.

Initial tables:

- `medication_strategy_table.csv`
- `decision_rules.csv`
- `question_derivation_matrix.csv`
- `safety_gate_questions.csv`

Evidence preparation layer:

- `theory_to_practice_matrix.csv`: connects didactic concerns to required app inputs, motor checks and official guideline anchors.
- `medication_official_claims.csv`: stores short indication, dosage, mechanism, warning and interaction anchors extracted from official product information.
- `medication_disease_use_evidence_review.csv`: classifies each disease-use relationship for formal review.
- `medication_evidence_gap_matrix.csv`: summarizes remaining evidence gaps for every medication.
- `motor2_gap_resolution_matrix.csv`: classifies every Motor 2 relationship without overwriting the original matrix.
- `PsychRx_Matriz_Teoria_Pratica_Evidencias.xlsx`: review workbook containing the complete preparation layer.
- `toxidrome_screening_matrix.csv`: source-anchored observable signs used to interrupt routine flow and request urgent medical assessment. It may display toxidrome definitions and antidote/countermeasure names when an official source supports them, but it does not diagnose a toxidrome, calculate emergency doses, choose route, perform decontamination instructions or create autonomous treatment rules.

The didactic PDF defines what the motor should observe. It does not validate clinical claims. Official regulatory and guideline sources provide the reviewable anchors. Every row in this preparation layer remains `runtime_eligible=false` until scientific normalization and editorial approval are complete.

Permanent boundaries:

- The table can suggest a strategy family for physician review.
- The table can expose evidence, target, cautions and monitoring.
- The table must not create autonomous diagnosis.
- The table must not replace physician prescription.
- Drug-specific candidates require source traceability.

Research source policy:

- Official source rules are defined in `docs/decision_support_engine/MOTOR_RESEARCH_SOURCE_POLICY.md`.
- Pending explanatory fields must remain `PENDENTE_PESQUISAR` until a source, edition/version, section and reviewable location are registered.
- Preferred sources include Stahl's Essential Psychopharmacology, Stahl's Prescriber's Guide, Goodman & Gilman, APA, NICE, FDA/DailyMed, EMA and ANVISA.
