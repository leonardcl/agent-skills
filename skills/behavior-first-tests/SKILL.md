---
name: behavior-first-tests
description: "Grow a change one observable behavior at a time."
---

# Behavior first tests

Grow a change one observable behavior at a time.

## Workflow

1. Write a test at the public boundary for one concrete empty list. Run it and confirm its failure describes the missing behavior.
2. Make the smallest change that passes. Add a nonempty-list example before refactoring shared rendering.
3. Rerun both examples after cleanup and retain the output that proves the new path was exercised.

## Try it

An empty reading list should show a helpful message.

**Expected result.** A red-to-green record and passing empty and nonempty behavior checks.

The regression assertion should check the visible empty-list message. A test against the existence of an empty array would pass before the missing UI is implemented.

**Limit.** A test that already passes may describe an existing behavior or the wrong boundary.
