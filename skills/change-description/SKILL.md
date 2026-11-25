---
name: change-description
description: "Write a reviewable change summary with evidence and integration risks."
---

# Change description

Write a reviewable change summary with evidence and integration risks.

## Workflow

1. Compare the proposed branch with its intended base. Identify the one user-visible difference and affected callers.
2. Describe the change with a before-and-after example. Include the exact validation performed and the result.
3. Identify migration or rollback considerations and which area deserves the reviewer's attention first.

## Try it

A patch changes date sorting and adds a test for equal dates.

**Expected result.** A review description covers the tie case, the passing command and remaining integration risk.

“Stable on equal dates” is checkable. Show the two equal-date entries in their original order, give the expected order after sorting, and identify the test that exercised the branch.

**Limit.** Draft text alone does not establish that CI ran or that a change was merged.
