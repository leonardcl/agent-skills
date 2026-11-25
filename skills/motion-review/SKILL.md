---
name: motion-review
description: "Review an implemented animation for timing, interruption and accessibility."
---

# Motion review

Review an implemented animation for timing, interruption and accessibility.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Map each entry and exit path to its state change and final focus target.
2. Review at full speed and frame-step the inconsistent exit. Repeat with reduced motion and a quick reopen.
3. Record a timecoded or code-located finding and verify the same dismissal paths after the fix.

## Try it

A dialog disappears instantly on Escape but fades out when dismissed with a pointer.

**Expected result.** Both dismissal routes end in the same focus state and have explainable motion behavior.

Dismiss once with Escape and once with the close button. Compare focus restoration after the transition as well as the visible exit.

**Limit.** Timing judgments depend on device and input conditions.
