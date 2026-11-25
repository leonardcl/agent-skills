---
name: debug-feedback-loop
description: "Diagnose a reproducible application defect with a short local feedback loop."
---

# Debug feedback loop

Diagnose a reproducible application defect with a short local feedback loop.

## Workflow

1. Capture the smallest public input and both observed and expected output.
2. State one hypothesis and the observation that would distinguish it from a competing cause. Add one temporary observation at that boundary.
3. Repeat with an unchanged control, fix the first incorrect transition and run the original entry point again.

## Try it

A list loses its last item after sorting three equal labels.

**Expected result.** Three distinct IDs survive the sort. A non-tied control preserves its previous order.

Use distinct IDs with equal labels. A set of labels cannot show that the sorting path dropped a record. Compare the IDs before and after the operation.

**Limit.** Intermittent failures need a recorded frequency or trace before a fix can be credited.
