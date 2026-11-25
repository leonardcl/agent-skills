---
name: component-visual-review
description: "Review interface hierarchy and state changes at component level."
---

# Component visual review

Review interface hierarchy and state changes at component level.

## Workflow

1. Identify the primary decision and the consequence of each action. Compare type, spacing, placement and focus order.
2. Walk through loading, success, error and dismissal. Record which visual cue communicates each state.
3. Revise one state and compare it with the original using the same content and viewport.

## Try it

Two actions in a confirmation dialog appear equally prominent.

**Expected result.** A state-by-state review and an example that makes the consequential choice recognizable.

Record which action draws attention, which gets initial focus and what Return actually does. A prominent destructive button can still leave the safe action focused. If the primary action changes while a request is pending, check the same keys again and ensure its visible label still describes the result. Compare identical dialog content when assessing an emphasis change.

**Limit.** A static design cannot demonstrate that a control works.
