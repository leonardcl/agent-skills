---
name: direct-manipulation
description: "Design a gesture-driven interaction with continuity, cancellation and a clear resting state."
---

# Direct manipulation

Design a gesture-driven interaction with continuity, cancellation and a clear resting state.

## Workflow

Follow the same object from pickup through release. Track the offset between touch and object. When a user grabs the preview again during its return animation, start the new drag from its visible position. Restarting at the thumbnail introduces a jump.

Define how distance and release velocity choose between returning and dismissing. Try a slow drag just short of the boundary, a quick flick from the same position and a reversal before release. Check that focus, hit target and dismiss state agree after each settles. Provide a button or keyboard route to the same destination.

## Try it

Dragging down a photo preview should return it to its thumbnail.

**Expected result.** A gesture contract and evidence for cancellation, completion and keyboard or button access.

Reverse the drag before releasing. The visual state and close action should agree even after the finger changes direction.

**Limit.** Platform conventions and device capabilities may differ.
