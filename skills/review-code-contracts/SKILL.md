---
name: review-code-contracts
description: "Check code changes for correctness, maintenance cost and preserved caller contracts."
---

# Review code contracts

Check code changes for correctness, maintenance cost and preserved caller contracts.

## Workflow

1. Identify which callers distinguish zero from missing and read their expectations at the boundary.
2. Trace a missing value, an actual zero and a normal value through the changed code. Compare the observable results.
3. Report only findings backed by a location, consequence and checkable example. Include a minimal corrective direction.

## Try it

Review a change that maps missing values to zero in a report.

**Expected result.** A finding identifies conflated values and the affected caller, or records evidence that both remain distinct.

A missing score and a genuine score of zero may look identical in the report while requiring different totals. Trace both through the aggregate and the displayed cell.

**Limit.** Static review cannot establish runtime properties that depend on deployment configuration.
