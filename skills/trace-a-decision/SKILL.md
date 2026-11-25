---
name: trace-a-decision
description: "Explain how a behavior works or why a design changed using repository evidence."
---

# Trace a decision

Explain how a behavior works or why a design changed using repository evidence.

## Workflow

For a question about *how*, follow one input through its normal entry point to the first transition that accounts for the observed output. Read the caller as well as the function. A parser may preserve a blank line even when the renderer later drops it.

For *why*, find the change that introduced the behavior. Inspect its parent, the test added with it and any linked decision. A blame line that only reformats the code can take you to the wrong change. Give the path or revision supporting each claim. If history establishes when behavior changed but contains no rationale, report the date or revision and leave the reason open.

## Try it

Why does a reader retain blank lines between paragraphs?

**Expected result.** A source-backed explanation with distinct sections for present behavior and historical intent.

A test can prove that blank lines survive parsing. Only a dated decision, issue or review can support the additional claim that editors requested it.

**Limit.** Implementation alone rarely establishes an author's motivation.
