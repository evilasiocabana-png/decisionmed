# Engineering Reverse Workflow

The PsychRx advice engine is built backward from the answer the physician needs.

## 1. Define The Expected Answer

The engine should answer:

- What is the strategy family?
- Why this strategy?
- What impairment is being targeted?
- What pharmacological target is relevant?
- If substituting, what candidates are compatible with the target?
- If associating, what candidates are compatible with the residual target?
- What safety cautions must be checked?
- What monitoring should follow?
- What evidence/source supports the statement?

## 2. Derive Required Fields

Each output section requires fields.

Example:

```text
Output: evaluate substitution
Required fields:
- current medication
- dose
- duration
- adherence
- response
- tolerability
- safety gate
- symptom target
- impairment domain
```

## 3. Generate Questions From Missing Fields

If a field is missing, the UI should ask a short question.

Example:

```text
Missing: duration
Question: Ha quanto tempo usa essa medicacao?
```

## 4. Resolve Safety Before Strategy

The first gate is always safety:

```text
suicide
mania_or_hypomania
substances
adherence
adverse_effects
interactions
qt_risk
pregnancy_or_lactation
metabolic_risk
```

If a required safety field is missing or positive, the engine should ask safety
questions before producing a strategy.

## 5. Produce A Table-Based Advice Object

After the required fields are present:

```text
clinical state
current medication
target symptoms
impairment
safety
-> decision_rules.csv
-> medication_strategy_table.csv
-> advice response
```

## 6. Keep The Table Auditable

Every medication candidate must include:

- source ID
- source title
- section
- source URL
- target domain
- cautions
- limits

No free-text candidate should enter the engine without traceability.
