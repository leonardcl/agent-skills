---
name: interface-language
description: "Write interface text that explains a state and the next available action."
---

# Interface language

Write interface text that explains a state and the next available action.

## Workflow

1. Identify what completed, what the user might lose and which recovery action exists.
2. Write the title and action labels in the same terms the rest of the interface uses. Keep technical diagnostics separate.
3. Read the message in context with actual buttons and test that choosing the promised action is possible.

## Try it

A dialog says “Something happened” after a save fails.

**Expected result.** A failure message identifies the unsaved change and offers an available retry path.

“Your note is still here. Try saving again.” works only if the draft remains and retry is available. Check both before shipping that message.

**Limit.** If the cause is unknown, state only what the application observed.
