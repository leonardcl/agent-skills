---
name: interface-review-scope
description: "Complete an interface review with a defined scope and verifiable findings."
---

# Interface review scope

Complete an interface review with a defined scope and verifiable findings.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. List the entry path, states and requested exclusions. Reach each state with representative local inputs.
2. For each observed issue record the exact control, consequence, evidence and smallest repair.
3. Reconcile the final report with the scope, including states that could not be reached and why.

## Try it

Review only the export dialog and its error recovery.

**Expected result.** A scoped review covering normal, failure and recovery paths without unrelated redesign suggestions.

Close the report by naming each requested state. If the export service never failed during the test, report the error state as unverified.

**Limit.** Hidden service states need a fixture or test environment.
