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

A drag released below the dismiss threshold should return to its resting position without losing focus or committing dismissal.

**Limit.** Simulator timing does not establish physical-device performance.
