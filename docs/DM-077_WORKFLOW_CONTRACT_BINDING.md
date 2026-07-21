# DM-077 — Workflow contract binding

Each workflow manifest must now match the exact workflow contract declared by its specialty pack. This prevents a valid-looking manifest from being attached to the wrong contract version.

The check is structural only; all workflows remain reference-only.
