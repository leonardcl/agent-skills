---
name: verify-user-path
description: "Build a repeatable local check for a user-visible feature."
---

# Verify user path

Build a repeatable local check for a user-visible feature.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Find the documented entry point. Start in a disposable data directory, record the build and perform a read-only readiness check.
2. Drive save and reopen through normal commands. Capture both the command results and the resulting file.
3. Clean up only processes and data created by the run. Reopen retained evidence and document the failure signal for the next reader.

## Try it

A command-line bookmark tool should save and reopen a reading position.

**Expected result.** A runnable check with input, expected exit status, evidence location and teardown that preserves the evidence.

A saved-position message proves little if the next launch forgets it. Use a new process against the same disposable directory and check the reopened position.

**Limit.** An unavailable platform or external service is a named coverage gap.
