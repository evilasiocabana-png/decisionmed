# Mission Supersedence Policy

## Objective

Define how PsychRx handles outdated, renamed, blocked or superseded missions without deleting history.

## Status Labels

Allowed mission status labels:

- `active`
- `completed`
- `blocked`
- `superseded`
- `historical`
- `pending`
- `gate`

## Rules

1. Never delete historical mission documents only because a later ADR changed the roadmap.
2. Mark superseded missions explicitly.
3. Keep blocked reports when they explain governance decisions.
4. Update `NEXT_MISSION.md` so it never points to a superseded or completed mission.
5. Preserve ADR history.

## Example

A03-025 was received out of order. It was first recorded as blocked, then later became executable after A03-022 through A03-024 were completed.

The block document remains valid as a historical record.

## Required Fields for Supersedence Notes

Every supersedence note must state:

- original mission;
- superseding mission or ADR;
- reason;
- date;
- current next mission;
- whether execution is allowed.

## Declaration Final

PsychRx preserves history while preventing old prompts from controlling future execution.
