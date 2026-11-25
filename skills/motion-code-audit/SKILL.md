---
name: motion-code-audit
description: "Audit existing animation code and prioritize fixes with reproducible evidence."
---

# Motion code audit

Audit existing animation code and prioritize fixes with reproducible evidence.

## Workflow

Find the event handler, state change and properties that actually animate. Capture the reported input sequence, viewport and motion setting. Compare one open with open–close–open at the same size and with the same data.

Inspect a timeline for the moment of the hitch. Repeated layout work suggests testing which geometry change causes it. If frames arrive on time but the drawer jumps back, inspect its start value on reversal. If it looks closed but still takes clicks, inspect the settled state and hit area. Each observation points to a different repair.

Report the earliest confirmed cause and a way to replay it. Rank blocked or incorrect interactions ahead of cosmetic differences and identify where measurement on the target device remains necessary.

## Try it

A drawer animates smoothly once but stutters on repeated open and close.

**Expected result.** A prioritized audit tied to the repeated-toggle trace with a clear retest after each fix.

Compare the first open with close-open interruption while keeping data and viewport constant. A single smooth recording does not cover repeated activation.

**Limit.** A code pattern is a lead until the effect is observed.
