# DM-063 — Question Engine output validation

## Outcome

DecisionMEd can validate a structurally complete `QuestionEngineResult` against
the exact `GovernedReasoningInput` and the declared `QuestionEngine` port. The
validator returns an immutable receipt that fingerprints the complete output.

## Fail-closed checks

- result fingerprint and trace match the exact governed input;
- engine id, provider and contract version match the supplied port;
- every open gap and question targets a field in the governed form schemas;
- question knowledge and evidence references are subsets of the binding;
- each question cites the Knowledge Object governing its field;
- cited evidence is anchored by the cited Knowledge Objects;
- governed Knowledge, Evidence and schemas remain current.

## Safety boundary

The validator never calls `QuestionEngine.generate`. It creates no clinical
question, recommendation or decision. The receipt explicitly keeps engine,
reasoning and clinical execution disabled. The real catalog remains draft and
cannot enter this validated path.

## Rollback

Revert the DM-063 commit. The change adds one isolated validator module, its
exports, tests and this document; it does not change existing engine contracts.
