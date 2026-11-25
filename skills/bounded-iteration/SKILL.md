---
name: bounded-iteration
description: "Iterate on a local project until a measurable condition holds."
---

# Bounded iteration

Iterate on a local project until a measurable condition holds.

## Workflow

1. Record the input set and the exact comparison used to detect changes. Save a baseline in scratch.
2. Change one cause of a mismatch, rerun the comparison and record the observed difference.
3. Stop at success, the agreed budget or a repeated result with no new lead. Leave a resumable note showing the last command.

## Try it

Normalize three local sample files so a second run produces no changes.

**Expected result.** All three outputs match the expected form and a second pass has an empty diff, or the report names the remaining mismatch.

For three tracked files, compare the first output against the expected fixture, then hash all three outputs again after the second run. A successful second invocation can still have rewritten a file.

**Limit.** Choose a finite input set and a local, reversible operation.

## Keep the run log

With Bash, run `bash log.sh run.tsv normalize "Keep line order" "Order carries meaning" "three sample files" "second diff empty"` from this directory, using a scratch output path in your actual project. The helper appends a timestamped row and creates the header on the first write. Use one writer per log.
