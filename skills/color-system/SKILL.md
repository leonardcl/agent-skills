---
name: color-system
description: "Define usable semantic colors for interface states."
---

# Color system

Define usable semantic colors for interface states.

## Workflow

Inventory colors by what they communicate in the actual UI. Map each role to a foreground, background and any border in each theme. Two roles can share a palette shade until their behavior diverges. If warning text and selected text both use one generic accent, changing it to fix an alert can silently recolor the selection.

Measure the pair at the place it appears, after any transparency is composited. Compare selection alone, warning alone and a selected row with a warning. Give each meaning a cue that survives all three states, such as a selection mark beside the title and a warning label beside the affected value. Record the rendered pair and recheck its other consumers when a shared token changes.

## Try it

A selected row and a warning row use nearly identical colors.

**Expected result.** A token table and examples that distinguish selection from warning without relying only on color.

Add a state label or icon so selection and warning remain distinguishable even when viewed without color.

**Limit.** Transparent layers need measurement after compositing.
