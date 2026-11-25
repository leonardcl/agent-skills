---
name: design-specification
description: "Record design decisions as reusable tokens and component rules."
---

# Design specification

Record design decisions as reusable tokens and component rules.

## Workflow

1. Inspect an existing wide and narrow view. Record measured type, spacing, surface and focus values with their source.
2. Describe the sidebar transition using the event that triggers it, where focus goes and how it reopens.
3. Build one sample state from the draft rules, compare it to the source and mark any value that remains proposed.

## Try it

Document a reading interface whose sidebar collapses on small screens.

**Expected result.** A short design spec containing token values, sidebar behavior and an example of visible keyboard focus.

With focus on a sidebar link, shrink the viewport through the actual transition width. Record the disappearing element, the new focus target and the control that restores the menu. Sample a second occurrence before naming a reusable token. If two identical-looking gaps come from different layout rules, document the local exception.

**Limit.** A single screenshot cannot establish interaction or dark-theme behavior.
