---
name: compare-ui-variants
description: "Create comparable interface variants for a choice the user can actually evaluate."
---

# Compare ui variants

Create comparable interface variants for a choice the user can actually evaluate.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Keep the dataset, available actions and viewport constant. Vary the one interaction that matters to the decision.
2. Build both variants and preserve their state independently. Label them by behavior and provide a simple switch.
3. Run the same task in both, including closing and reopening filters, and capture the observed trade-off.

## Try it

Compare an inline and a drawer-based filter for a small list.

**Expected result.** Two working alternatives with the same task and a mechanism for selecting or documenting the chosen one.

Preserve the same selected filter and list contents in both variants. A drawer that clears the selection on close tests a different behavior from an inline control that retains it.

**Limit.** Differences in unrelated content confound a comparison.
