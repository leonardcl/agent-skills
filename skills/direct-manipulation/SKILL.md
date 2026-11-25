---
name: direct-manipulation
description: "Design a gesture-driven interaction with continuity, cancellation and a clear resting state."
---

# Direct manipulation

Design a gesture-driven interaction with continuity, cancellation and a clear resting state.

## Workflow

1. Identify the same object before and after the transition. Keep the user's touch point attached to its visual position.
2. Specify release behavior for a slow partial drag, reversal and fast completion. Preserve a non-gesture route.
3. Drive each case and verify that the destination can immediately accept the next interaction.

## Try it

Dragging down a photo preview should return it to its thumbnail.

**Expected result.** A gesture contract and evidence for cancellation, completion and keyboard or button access.

Reverse the drag before releasing. The visual state and close action should agree even after the finger changes direction.

**Limit.** Platform conventions and device capabilities may differ.
