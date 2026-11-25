---
name: interaction-motion
description: "Design a transition that explains an interface state change."
---

# Interaction motion

Design a transition that explains an interface state change.

## Workflow

Identify the state change the user could lose track of and the element that should stay anchored. If revealing the details already makes the change clear, a direct swap can suffice. For an expanding panel, keep its trigger in place while the content changes.

Choose the smallest property change that conveys the relationship. Reverse the action during entry. A panel that restarts from its fully open height will jump. Retarget it from its current position. Under reduced motion, remove the travel while preserving the same expanded state, focus and available controls. Check a second rapid toggle for stale hit targets.

## Try it

A details panel abruptly replaces its summary.

**Expected result.** The panel ends in the correct state after a rapid toggle and the reduced-motion path stays intelligible.

Interrupt an opening panel with a close request. Check the final expanded state and hit area in addition to whether the transition looked smooth.

**Limit.** Duration and easing must be judged on the target device.
