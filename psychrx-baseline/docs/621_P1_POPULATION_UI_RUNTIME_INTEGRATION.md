# 621 - P1 Population UI and Runtime Integration

## Objective

Insert population assessment into the existing patient-first consultation flow
without changing the essence of PsychRx.

## Implementation

- added the `Populacao` card immediately after consultation presentation;
- added birth date with a client-side age preview and authoritative backend age;
- kept pregnancy, lactation and postpartum separate;
- added explicit renal and hepatic status;
- transported sex context and optional weight;
- merged assessed population restrictions into the existing safety context;
- required population completion before a decision-support request;
- added the population summary to the existing reasoning panel;
- integrated population warnings into the Application Layer rule-table gate.

## Preserved Product Essence

The flow remains patient -> current state -> safety -> current treatment ->
response/tolerability -> traceable comparison -> physician decision. No disease
encyclopedia, automatic diagnosis, prescription or `Apply to case` path was
introduced.

## Declaration Final

The Interface collects and displays population context; the Application Layer
owns age derivation and blocking semantics.
