# Track C UX Acceptance Test Plan

## Status

Governed test plan.

## Required Automated Tests

Run:

```text
python -m unittest discover -s tests/interfaces -t .
python -m unittest discover -s tests -t .
```

## Required UI Assertions

The static web app must contain:

- `consultation-summary`;
- `technical-reference`;
- `filter-console`;
- `data-gap`;
- `filter-table-confidence`;
- `calculateStage`;
- `calculateOperationalConfidence`.

## Required Manual Browser Verification

Open:

```text
http://127.0.0.1:8765/
```

Verify:

- the first visible workflow asks how the patient is today;
- the screen focuses on the consultation, not documentation;
- technical reference is collapsed by default;
- no horizontal overflow is present in narrow Chrome viewport;
- no prescription, dose, drug selection or treatment ranking is visible;
- the app remains read-only.

## Gate

Track C UX Implementation may be considered technically created only if tests pass and runtime clinical decisioning remains disabled.

