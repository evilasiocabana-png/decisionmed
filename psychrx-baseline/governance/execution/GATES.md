# Governance Gates

These gates apply to all future PsychRx execution.

## State Gate

No mission may start without reading `governance/execution/EXECUTION_STATE.json`.

## Mission Gate

No mission may start without:

- clear mission identifier;
- clear scope;
- permitted files;
- prohibited files;
- acceptance criteria;
- expected validation.

## Status Gate

No mission is complete until project status files are updated or explicitly confirmed unchanged.

## Execution Log Gate

No mission is complete without an execution report or execution log entry.

## Scientific Traceability Gate

No clinical or scientific content may enter the knowledge base without:

- source;
- source anchor;
- selected section;
- target field;
- reviewable content;
- traceability status.

## Clinical Safety Gate

No change may introduce:

- automatic prescription;
- automatic diagnostic inference;
- autonomous therapeutic recommendation;
- dose suggestion;
- medication selection;
- clinical runtime consumption of draft knowledge.

## A04 Gate

A04-009 remains blocked until `A04_SOURCE_SECTION_SELECTION_REQUIRED` is resolved.

The required chain is:

```text
Specific source
-> Specific section
-> Psychopharmacological field
-> Reviewable content
```
