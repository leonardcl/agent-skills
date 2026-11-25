---
name: project-handoff
description: "Prepare a checkpoint that another person can resume from a clean checkout."
---

# Project handoff

Prepare a checkpoint that another person can resume from a clean checkout.

## Workflow

1. Record the revision, changed files and command that last passed. Separate committed changes from working edits.
2. Write the smallest action that tests the open case and describe its expected output.
3. Read the handoff cold. Verify referenced paths and state which prerequisite another machine needs.

## Try it

A parser fix passes locally but the empty-input case is still untested.

**Expected result.** A new reader can locate the change and run the empty-input check without reading the chat.

A passing parser test and an untried empty string are different evidence. Include the exact empty input, the expected exit status and the working directory required to run it.

**Limit.** Do not include credentials or private transcripts in a shared handoff.
