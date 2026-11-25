---
name: guided-setup
description: "Turn a manual setup procedure into a resumable local guide."
---

# Guided setup

Turn a manual setup procedure into a resumable local guide.

## Workflow

1. Separate steps the tool can observe from choices only the user can make. Record prerequisites and a recovery point for each choice.
2. Present one action at a time and test its observable result. Detect previously completed stages so a restart skips them safely.
3. Try success, interruption and an unwritable folder in a disposable profile. Report the exact step needing intervention.

## Try it

Guide someone through selecting a notes folder and verifying write access.

**Expected result.** A guide that resumes at the first unfinished stage and identifies an invalid folder before proceeding.

Restart after choosing the folder but before writing a sample. The second run should detect the selected folder, perform the missing check and leave an unrelated file intact.

**Limit.** A setup guide must not treat reading the instructions as completing a step.
