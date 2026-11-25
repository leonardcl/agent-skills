---
name: swift-state-review
description: "Review Swift state ownership and concurrency at an observable boundary."
---

# Swift state review

Review Swift state ownership and concurrency at an observable boundary.

## Workflow

1. Trace who owns the state and where each asynchronous result crosses an isolation boundary.
2. Choose cancellation, request identity or actor isolation according to the actual invariant. Handle failure and cancellation explicitly.
3. Drive two lookups whose completion order is reversed and observe the final published value.

## Try it

An older async lookup completes after a newer query and overwrites its result.

**Expected result.** The newer query remains visible and cancelled work cannot overwrite its result.

Start query A, then B, and deliver A last. The final published result should still belong to B; main-actor isolation alone does not establish response ordering.

**Limit.** Compiler diagnostics depend on the installed Swift version and isolation settings.
