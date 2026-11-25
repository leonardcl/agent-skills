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

A saved folder choice records intent. Recheck that the directory still exists, then create and remove a uniquely named scratch file there to prove write access. If that fails after a restart, resume at folder selection or permissions with the exact failing path. Retain unrelated files and skip later steps that depend on successful writing.

**Limit.** A setup guide must not treat reading the instructions as completing a step.
