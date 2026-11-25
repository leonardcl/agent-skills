---
name: interaction-polish
description: "Refine a frequently used component using observable interaction details."
---

# Interaction polish

Refine a frequently used component using observable interaction details.

## Workflow

1. Measure the control's resting geometry and record a normal and rapid sequence.
2. Remove layout shifts, distinguish press feedback from committed state and respect reduced motion.
3. Compare the revised control at the same viewport using mouse, keyboard and repeated activation.

## Try it

A frequently pressed toggle feels sluggish and shifts its label.

**Expected result.** Stable label position and immediate feedback that matches the final toggle state.

Track the label bounds before and after activation. A fixed-width control can still shift its content when the type weight or icon changes.

**Limit.** Perceived quality needs direct inspection of the running control.
