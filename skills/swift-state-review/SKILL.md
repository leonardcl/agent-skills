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

Use controlled completions so B succeeds before A returns, then repeat with A failing. A stale error or a stale completion that clears B’s loading state can be just as visible as a stale value. Compare the request identity at publication after each suspension that can outlive the current request. Cancellation alone is sufficient only if the operation and its callbacks honor it.

**Limit.** Compiler diagnostics depend on the installed Swift version and isolation settings.
