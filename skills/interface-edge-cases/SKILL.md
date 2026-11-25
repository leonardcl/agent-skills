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

Use an empty list, a long unbroken label and an unavailable image as separate fixtures. Record which single input first causes the layout to fail.

**Limit.** Scope is ordinary UI behavior in a user-controlled local example.
