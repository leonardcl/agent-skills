---
name: motion-code-audit
description: "Audit existing animation code and prioritize fixes with reproducible evidence."
---

# Motion code audit

Audit existing animation code and prioritize fixes with reproducible evidence.

## Workflow

1. Locate the actual triggers and rendering properties. Record device, input sequence and reduced-motion preference.
2. Distinguish layout work, interrupted transitions and state bugs by varying one condition at a time.
3. Rank each finding by impact and give a verification recipe a second developer can run.

## Try it

A drawer animates smoothly once but stutters on repeated open and close.

**Expected result.** A prioritized audit tied to the repeated-toggle trace with a clear retest after each fix.

Compare the first open with close-open interruption while keeping data and viewport constant. A single smooth recording does not cover repeated activation.

**Limit.** A code pattern is a lead until the effect is observed.
