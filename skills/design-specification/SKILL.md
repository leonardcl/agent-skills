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

“Sidebar collapses” leaves keyboard behavior undecided. Record whether focus moves to the opener when a focused item disappears, then exercise the breakpoint with focus inside the sidebar.

**Limit.** A single screenshot cannot establish interaction or dark-theme behavior.
