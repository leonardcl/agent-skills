---
name: interface-review-scope
description: "Complete an interface review with a defined scope and verifiable findings."
---

# Interface review scope

Complete an interface review with a defined scope and verifiable findings.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

Locate the requested screen or change, its entry point, changed states and exclusions. If the task concerns a patch, inspect the base and removed behavior as well as the new screen. Map the affected part of the diff to something a user can see or operate.

Drive the same sequence on comparable inputs. Distinguish a newly introduced failure, an older issue that the change exposes and a state you could not reach. For example, losing focus on export retry is a regression only if the previous route retained useful focus. Record the exact control, consequence and evidence. Give the smallest repair within scope and account for each requested state.

## Try it

Review only the export dialog and its error recovery.

**Expected result.** A scoped review covering normal, failure and recovery paths without unrelated redesign suggestions.

Close the report by naming each requested state. If the export service never failed during the test, report the error state as unverified.

**Limit.** Hidden service states need a fixture or test environment.
