---
name: interaction-motion
description: "Design a transition that explains an interface state change."
---

# Interaction motion

Design a transition that explains an interface state change.

## Workflow

1. Identify the entering and departing elements and keep a stable visual anchor.
2. Choose the properties that express continuity, interrupt the animation halfway and test the final state after rapid toggles.
3. Compare full-motion and reduced-motion paths using the same sequence of actions.

## Try it

A details panel abruptly replaces its summary.

**Expected result.** The panel ends in the correct state after a rapid toggle and the reduced-motion path stays intelligible.

Interrupt an opening panel with a close request. Check the final expanded state and hit area in addition to whether the transition looked smooth.

**Limit.** Duration and easing must be judged on the target device.
