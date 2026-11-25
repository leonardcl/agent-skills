---
name: verify-user-path
description: "Build a repeatable local check for a user-visible feature."
---

# Verify user path

Build a repeatable local check for a user-visible feature.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

Identify the user's entry point and the effect that can outlive the process, request or screen. Find the project's normal startup and readiness signal. Record prerequisites, use a disposable data location and avoid using a pre-existing process as proof that the tested build started.

Choose an input that makes a false pass visible. Save a distinctive position, close the process and reopen the same notebook in a new process. Check the position itself. As a control, a fresh notebook should open at its documented default. If both show the saved value, inspect which data directory the app actually opened.

Keep the command, expected result, actual result and evidence needed to replay it. Stop only resources created for this run and verify the evidence remains readable after teardown.

## Try it

A command-line bookmark tool should save and reopen a reading position.

**Expected result.** A runnable check with input, expected exit status, evidence location and teardown that preserves the evidence.

A saved-position message proves little if the next launch forgets it. Use a new process against the same disposable directory and check the reopened position.

**Limit.** An unavailable platform or external service is a named coverage gap.
