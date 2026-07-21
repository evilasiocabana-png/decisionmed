# 638 - Program 28 Final Audit

## Audit Verdict

**Pass with an explicit scientific publication boundary.**

The requested implementation outcome is complete for the four monitoring
rules. The quoted pharmacological backlog has been reconciled but is not
scientifically complete because row-level publication gates remain open.

## Four Monitoring Rules

| Rule | Official source | Runtime eligible | Trigger tested |
| --- | --- | --- | --- |
| `TPC-005` | NICE NG222 1.4.12-1.4.21 | yes | yes |
| `TPC-012` | NICE CG185 1.10.14-1.10.24 | yes | yes |
| `TPC-014` | NICE CG178 1.3.5.1-1.3.6.4 | yes | yes |
| `TPC-015` | NICE CG178 1.3.5.1-1.3.6.5 | yes | yes |

## Backlog Audit

| Area | Total | Source-reconciled result | Runtime published |
| --- | ---: | --- | ---: |
| structured interaction profile gaps | 44 | 32 official interaction excerpt candidates; 12 source/anchor gaps | 0 |
| disease-use rows | 347 | 68 label matches; 259 guideline/off-label review; 20 source missing | 0 |
| Motor 2 rows | 1,444 | all classified; 436 without condition range | 0 |
| monitoring rules | 4 | four official guideline anchors published | 4 |

## Automated Validation

Command:

```text
python -m unittest discover -s tests -t .
```

Result:

```text
Ran 239 tests
OK
```

Additional validation:

- `python -m compileall -q application tests`: passed;
- `git diff --check`: passed;
- dual-gate negative test: passed;
- withdrawal, lithium, antipsychotic and unrelated-medication smoke tests:
  passed;
- restore tag, branch and external bundle: verified.

## Restore Point

- tag `restore/pre-scientific-promotion-20260720-27a4750`;
- branch `codex/restore-pre-scientific-promotion-20260720`;
- bundle
  `C:\Users\evcab\PsychRx_pre_scientific_promotion_20260720_27a4750.bundle`;
- base commit `27a47501c9ea7d74b6915e8e4a5a29090e626d3c`.

## Product Essence Audit

The flow remains patient-first. No disease encyclopedia, `Apply to case`
workflow, autonomous diagnosis, prescribing, dose calculation or automatic
taper was introduced.

## Declaration Final

The four monitoring rules are source-governed and enabled. The other quoted
counts remain visible as scientific publication debt, because certifying them
without row-level review would contradict PsychRx evidence governance and
clinical safety.
