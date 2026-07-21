# DM-075 — Expiring safety-review authority

Safety-review authority decisions now expire after five minutes by default and are single-use. Expired or replayed decisions are fail-closed and audit-recorded before a review record can be created.

The local replay guard is thread-safe and in-memory; a production runtime must provide a durable shared implementation. This strengthens governance only and never enables clinical execution.
