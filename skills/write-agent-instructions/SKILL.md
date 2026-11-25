---
name: write-agent-instructions
description: "Write agent instructions with a precise trigger and observable completion criteria."
---

# Write agent instructions

Write agent instructions with a precise trigger and observable completion criteria.

## Workflow

1. Replace the vague trigger with the user request that selects the workflow. Identify a nearby request that should take a different path.
2. Name the artifact each step reads or produces. Move conditional background behind a reachable relative link.
3. Run a small example from a fresh directory, open the referenced resources and compare the result against the stated completion condition.

## Try it

A skill says to check a notebook but gives no indication of completion.

**Expected result.** A standalone skill whose trigger, inputs, example and final check a new reader can follow.

“Review the notes” can end at inspection. “Open the index link and show the destination heading” makes an incorrect or missing link detectable from the delivered result.

**Limit.** Trigger wording still depends on how a particular host discovers skills.
