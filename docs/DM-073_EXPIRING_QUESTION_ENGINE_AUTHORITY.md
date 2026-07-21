# DM-073 — Expiring Question Engine authority

An external authorization decision for a Question Engine invocation is now valid only for a short, configurable duration (five minutes by default). The application service checks freshness after exact identity matching and before it records authorization or calls an engine.

An expired decision is fail-closed, produces a metadata-only audit event and returns no generated output. This adds an authorization safeguard only; it does not enable reasoning or clinical execution.
