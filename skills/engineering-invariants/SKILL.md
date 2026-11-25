---
name: engineering-invariants
description: "Use a concrete invariant to guide an implementation choice."
---

# Engineering invariants

Use a concrete invariant to guide an implementation choice.

## Workflow

1. Write the invariant in terms a caller can observe. Identify the boundary that can enforce it across retries.
2. Trace two identical runs, a partial failure and a concurrent request through the proposed design.
3. Exercise the smallest case that distinguishes the designs and record which state survives each interruption.

## Try it

Retrying the same local import duplicates records.

**Expected result.** An invariant, a boundary decision and evidence that a repeated import leaves one logical record.

A second import can successfully return twice and still be wrong. Count logical records after both runs and specify the identity rule that makes two submissions equivalent.

**Limit.** Use concurrency claims only when an actual interleaving or atomic guarantee supports them.
