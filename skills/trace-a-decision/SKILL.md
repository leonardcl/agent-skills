---
name: trace-a-decision
description: "Explain how a behavior works or why a design changed using repository evidence."
---

# Trace a decision

Explain how a behavior works or why a design changed using repository evidence.

## Workflow

1. Trace one example from input to output and locate the first line that preserves the blank line.
2. For historical intent, find the introducing change and read the surrounding discussion or test. Keep mechanism and motivation separate.
3. Cite the strongest primary artifact for each claim and state what evidence would resolve gaps.

## Try it

Why does a reader retain blank lines between paragraphs?

**Expected result.** A source-backed explanation with distinct sections for present behavior and historical intent.

A test can prove that blank lines survive parsing. Only a dated decision, issue or review can support the additional claim that editors requested it.

**Limit.** Implementation alone rarely establishes an author's motivation.
