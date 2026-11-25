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

For equal-date entries arriving as B, A, show whether they remain B, A and which check exercised that case. Distinguish a code-only rollback from persisted changes. If sorting only affects rendering, reverting can restore the previous view. If a migration rewrote stored order, say what evidence or backup would be needed to recover it.

**Limit.** Draft text alone does not establish that CI ran or that a change was merged.
