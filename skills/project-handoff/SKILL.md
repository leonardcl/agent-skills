---
name: project-handoff
description: "Prepare a checkpoint that another person can resume from a clean checkout."
---

# Project handoff

Prepare a checkpoint that another person can resume from a clean checkout.

## Workflow

Write down the intended result and where work stopped. Inspect the current revision, tracked changes and untracked inputs. Identify what a checkout at that revision actually contains. A locally passing command that depends on a working edit or fixture needs a way to recover that exact input. Name an available patch or artifact and its base, or mark the step blocked until the author supplies it. A path on the first machine alone cannot transfer the work.

Give the last observed command, working directory, prerequisites and result. For the next action, name a single unresolved question, the command or input that distinguishes its outcomes, and what each outcome means. Mark a proposed command as unrun until someone tries it.

On resuming, compare the handoff's revision and required files to the checkout in front of you. If they differ, state what changed before carrying forward a test result. Verify that the paths and instructions in the handoff make sense to a reader who has no chat history.

## Try it

A parser fix passes locally but the empty-input case is still untested.

**Expected result.** A new reader can locate the change and run the empty-input check without reading the chat.

A passing parser test and an untried empty string are different evidence. Include the exact empty input, the expected exit status and the working directory required to run it.

**Limit.** Do not include credentials or private transcripts in a shared handoff.
