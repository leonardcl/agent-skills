---
name: native-motion
description: "Design a React Native animation that follows a user gesture."
---

# Native motion

Design a React Native animation that follows a user gesture.

## Workflow

1. Map gesture distance and velocity into the sheet's position. Define cancel, dismiss and interrupted states.
2. Keep frame-by-frame updates on the appropriate animation thread and commit application state once the gesture settles.
3. Exercise short drags, quick flings, interrupted drags and the reduced-motion setting on a target device.

## Try it

A drag-to-dismiss sheet snaps back when released below a threshold.

**Expected result.** The sheet settles predictably and cancellation leaves content and focus intact.

During the return animation, touch the sheet again and drag in the opposite direction. Resume from the displayed offset and invalidate the old completion callback. Only the currently completing dismissal may remove the sheet. Verify that cancellation keeps it mounted, focusable and ready for the second drag. Keep per-frame position updates on the animation runtime when the installed library supports it.

**Limit.** Simulator timing does not establish physical-device performance.
