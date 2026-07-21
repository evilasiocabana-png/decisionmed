# Editorial Status Standard - Program A03

## Purpose

Define the official editorial status lifecycle for Program A03 objects.

## Status Principles

- Every object must have one editorial status.
- Status transitions must be explicit.
- Publication requires prior validation.
- Scientific review is a future gate, not a current authorization.
- Metadata-only objects cannot be treated as scientific content.

## Official States

| Status | Meaning |
| --- | --- |
| Draft | Initial administrative state. |
| Initialized | Structure exists. |
| Metadata Complete | Required administrative metadata is present. |
| Source Bound | Source IDs are structurally linked. |
| Editorial Review | Object awaits editorial review. |
| Scientific Review | Object awaits future scientific review after authorized population. |
| Validated | Object passed required future validation gates. |
| Published | Object is published after future authorization. |
| Deprecated | Object should no longer be active. |
| Archived | Object is retained for audit only. |

## Prohibited Interpretation

Editorial status does not mean:

- clinical validity;
- therapeutic recommendation;
- evidence grade;
- prescription authorization;
- runtime readiness.

## Declaration Final

Editorial status is administrative governance. It is not scientific validation.
