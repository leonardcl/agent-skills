---
name: review-a-change
description: "Review a change against its intended behavior and the callers relying on it."
---

# Review a change

Review a change against its intended behavior and the callers relying on it.

## Workflow

1. Read the change and establish its public contract from callers and tests.
2. Trace empty input, ordinary input and input where spaces carry meaning. Identify the first observable divergence.
3. Write each finding with file location, a minimal example and user impact. Rerun an existing check where possible.

## Try it

A patch skips whitespace before parsing a header.

**Expected result.** Each finding names the input, the expected outcome and the observed result. Unsupported suspicions are labeled.

A whitespace-only input can change from a parsed empty field to a missing header. Test both through the public parser before describing the change as harmless trimming.

**Limit.** A review of a diff covers only the paths examined.
