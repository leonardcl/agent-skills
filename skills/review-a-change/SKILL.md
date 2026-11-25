---
name: review-a-change
description: "Review a change against its intended behavior and the callers relying on it."
---

# Review a change

Review a change against its intended behavior and the callers relying on it.

## Workflow

Read the intended behavior, base, patch and removed lines. Map each changed assumption to a caller or stored input it can affect. Pick an ordinary input and the nearest case where the old and new rules differ. For trimming, those might be an empty field, a field containing one space and a header with a leading space.

Drive the distinguishing input through the caller. Compare the outcome to the specification and, where possible, the base revision. Report a regression when the patch changes behavior a caller relies on. Mark an existing problem separately and show the supporting input. Give a file location and consequence for each finding, with the most consequential first.

## Try it

A patch skips whitespace before parsing a header.

**Expected result.** Each finding names the input, the expected outcome and the observed result. Unsupported suspicions are labeled.

A whitespace-only input can change from a parsed empty field to a missing header. Test both through the public parser before describing the change as harmless trimming.

**Limit.** A review of a diff covers only the paths examined.
