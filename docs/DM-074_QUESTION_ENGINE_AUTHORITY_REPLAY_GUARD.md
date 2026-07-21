# DM-074 — Question Engine authority replay guard

Each exact Question Engine authority decision can now be reserved only once before an engine invocation. A replay is fail-closed, audit-recorded and reaches no engine.

The local default is a thread-safe in-memory guard. The contract is injectable so a future runtime outside this local reference platform must use a durable shared implementation. This work does not enable reasoning or clinical execution.
