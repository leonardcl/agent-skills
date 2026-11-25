---
name: task-routing
description: "Choose an execution path for a request with several plausible deliverables."
---

# Task routing

Choose an execution path for a request with several plausible deliverables.

## Workflow

1. Extract the user-visible goal and the observable decision at the end. Check whether the request asks for diagnosis, options or an implementation.
2. Inspect the cheapest available evidence before splitting the work. Keep dependent decisions sequential.
3. Choose one next action and specify what result would change the route. Return to the original goal when that evidence arrives.

## Try it

Someone asks to improve search but supplies only a slow search example.

**Expected result.** A scoped route with a baseline measurement, an explicit change boundary and a completion check.

A slow query supplies a symptom. Record one query and dataset size, measure its current latency and establish whether the request ends at diagnosis or includes a patch.

**Limit.** An ambiguous goal can justify one focused question.
