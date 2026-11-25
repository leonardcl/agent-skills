---
name: comment-review
description: "Remove low-value commentary while preserving rationale and constraints."
---

# Comment review

Remove low-value commentary while preserving rationale and constraints.

## Workflow

1. Read the adjacent implementation and history for each comment. Categorize rationale, external constraint or mechanical restatement.
2. Delete or shorten restatements while preserving the detail a future maintainer cannot infer from the code.
3. Inspect the diff for behavior changes and rerun the existing test if the language treats comments as directives.

## Try it

A loop has one comment restating its condition and another explaining archive compatibility.

**Expected result.** A comment-only edit retaining the archive constraint and any tool directives.

Keep the reason an archived file uses an older delimiter. A comment saying that the loop advances to the next row can go if the control structure already shows it.

**Limit.** Generated sources, license notices and compiler annotations require separate handling.
