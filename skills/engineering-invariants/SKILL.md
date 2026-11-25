---
name: engineering-invariants
description: "Use a concrete invariant to guide an implementation choice."
---

# Engineering invariants

Use a concrete invariant to guide an implementation choice.

## Workflow

Express the rule in externally visible terms. For a retried import, define what makes two records the same logical item. Inspect where that identity is stored and what else changes when the write succeeds.

Walk through an interruption after writing the record but before acknowledging completion. Then interleave two requests that both see no existing item. A pre-write lookup alone lets both proceed. Compare designs at the shared write boundary, for example enforcing uniqueness there and returning the existing record on a duplicate. Check both the record count and any separately emitted effect. A single stored record can still produce two notifications.

## Try it

Retrying the same local import duplicates records.

**Expected result.** An invariant, a boundary decision and evidence that a repeated import leaves one logical record.

A second import can successfully return twice and still be wrong. Count logical records after both runs and specify the identity rule that makes two submissions equivalent.

**Limit.** Use concurrency claims only when an actual interleaving or atomic guarantee supports them.
