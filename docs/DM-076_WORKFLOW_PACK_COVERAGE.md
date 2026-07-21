# DM-076 — Workflow pack coverage

Every registered specialty pack must now have exactly one workflow manifest at platform startup. A missing manifest raises a deterministic configuration error instead of allowing a specialty to appear as navigable without a working flow.

All workflows remain `reference_only`; this is a structural coverage guarantee, not a clinical readiness claim.
