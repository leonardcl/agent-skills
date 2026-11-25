---
name: debug-feedback-loop
description: "Diagnose a reproducible application defect with a short local feedback loop."
---

# Debug feedback loop

Diagnose a reproducible application defect with a short local feedback loop.

## Workflow

Start at the entry point where the failure was reported. Choose an assertion that would turn red even if the program exits successfully. Save the command, disposable input and actual output. Shrink the input one change at a time while it still fails. Keep a similar passing case as a control.

Trace where the observed value first goes wrong. For the tied-label example below, inspect the IDs after reading, sorting and emitting. If all IDs reach the emitter, changing the comparator cannot recover the missing record. If the IDs disappear earlier, test that boundary before touching the emitter. Change one variable per run and remove temporary probes when finished.

Keep a regression check at a boundary that exercises the cause. Rerun the *original* command and the control after fixing it. Report the first bad transition, the red and green output and any case you could not reproduce.

If the failure comes and goes, record failures per attempt with the same input and conditions. Save the order of events or the seed from a failing run and replay it. If only another environment fails, identify the smallest observation needed there. A green substitute is inconclusive.

## Try it

A list loses its last item after sorting three equal labels.

**Expected result.** Three distinct IDs survive the sort. A non-tied control preserves its previous order.

Use distinct IDs with equal labels. A set of labels cannot show that the sorting path dropped a record. Compare the IDs before and after the operation.

**Limit.** Intermittent failures need a recorded frequency or trace before a fix can be credited.
