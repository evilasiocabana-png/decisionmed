# 620 - P1 Patient Population Context Contract

## Objective

Represent population factors before routine pharmacological comparison, without
assuming that an unreported factor is absent.

## Contract

- age is calculated in the Application Layer from the date of birth;
- the canonical age bands are `CHILD`, `ADOLESCENT`, `ADULT`, `OLDER_ADULT` and
  `UNKNOWN`;
- pregnancy, lactation and postpartum are independent assessed states;
- renal and hepatic function are independent assessed states;
- sex context and weight can be transported without becoming automatic dose or
  treatment rules;
- missing or unknown required population states block routine comparison;
- child, adolescent, older-adult, perinatal and altered-organ contexts require
  population-specific review before routine ranking.

## Safety Boundary

This contract does not diagnose, calculate a dose, choose a medication or claim
that a population-specific evidence rule has been validated. It only records and
enforces the review boundary.

## Files

- `application/patient_population_context.py`;
- `application/clinical_decision_support_contract.py`;
- `tests/application/test_patient_population_context.py`.

## Declaration Final

Population absence is represented as uncertainty and never converted into an
adult, non-pregnant or organ-preserved assumption.
