---
name: merge-by-intent
description: "Resolve overlapping edits while preserving the behavior of both branches."
---

# Merge by intent

Resolve overlapping edits while preserving the behavior of both branches.

## Workflow

1. Read the base and both tips. Explain what each changed using the entry point or test that motivated it.
2. Resolve against the resulting contract. Search downstream for stale names and keep both branches' meaningful assertions.
3. Run the relevant tests on the merged tree and inspect the staged diff for accidentally lost edits.

## Try it

One branch renames a field and another adds validation to its former name.

**Expected result.** The new field name works and invalid values still fail through the normal API.

Keep the renamed field and apply validation to its new name. Search for the former name in tests and serialized fixtures as well as code.

**Limit.** Confirm genuinely conflicting product decisions before choosing a winner.
