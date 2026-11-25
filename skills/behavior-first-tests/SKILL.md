---
name: behavior-first-tests
description: "Grow a change one observable behavior at a time."
---

# Behavior first tests

Grow a change one observable behavior at a time.

## Workflow

Pick one promised result and the closest entry point that can produce it. Derive the expected value from the caller's contract. For an empty reading list, assert on the message a reader sees. Calling a helper that counts items misses a view that never displays the result.

Run the test against the old behavior. If it passes, check whether the feature exists already or whether the assertion misses the symptom. A missing dependency or broken fixture is a setup failure. Resolve that first, then get a failure on the intended assertion.

Implement that behavior and rerun the check. Add the next case where the contract changes, such as a populated list that should still show its first book. Refactor with both cases passing.

## Try it

An empty reading list should show a helpful message.

**Expected result.** A red-to-green record and passing empty and nonempty behavior checks.

The regression assertion should check the visible empty-list message. A test against the existence of an empty array would pass before the missing UI is implemented.

**Limit.** A test that already passes may describe an existing behavior or the wrong boundary.
