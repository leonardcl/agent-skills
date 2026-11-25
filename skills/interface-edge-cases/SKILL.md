---
name: interface-edge-cases
description: "Stress-test ordinary interface behavior with realistic content and input sequences."
---

# Interface edge cases

Stress-test ordinary interface behavior with realistic content and input sequences.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Build local fixtures for each state and use the normal interface to reach them.
2. Vary the viewport, text size and event order independently. Record the first user-visible failure and the shortest sequence that shows it.
3. After a fix repeat the same fixture and one neighboring case.

## Try it

A list view must handle no items, a very long label and a missing image.

**Expected result.** A fixture table with reproducible layout, recovery or state findings.

Choose stress cases from what the component actually consumes. For a list with remote thumbnails, try a missing image, a long unbroken title and an empty response individually. Once each works alone, combine the long title with the fallback image in the narrow row. Preserve the triggering input, viewport and action when documenting a failure so another reader can replay it.

**Limit.** Scope is ordinary UI behavior in a user-controlled local example.
