---
name: review-code-contracts
description: "Check code changes for correctness, maintenance cost and preserved caller contracts."
---

# Review code contracts

Check code changes for correctness, maintenance cost and preserved caller contracts.

## Workflow

Start at the changed boundary and read a caller that consumes its result. Write down the distinctions that caller needs to preserve. Missing and zero matter for an average, while a count label might intentionally show the same fallback for both. Look at the reader, writer and error path before recommending a change to a shared default.

Follow a pair of inputs that would separate the old and new contracts. With scores of 8 and missing, ignoring the absent score yields 8. Replacing it with zero yields 4. Verify which rule the application promises and where the conversion happens. Report the smallest example that demonstrates a consequence, its location and which callers you checked.

## Try it

Review a change that maps missing values to zero in a report.

**Expected result.** A finding identifies conflated values and the affected caller, or records evidence that both remain distinct.

A missing score and a genuine score of zero may look identical in the report while requiring different totals. Trace both through the aggregate and the displayed cell.

**Limit.** Static review cannot establish runtime properties that depend on deployment configuration.
