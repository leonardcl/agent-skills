---
name: color-system
description: "Define usable semantic colors for interface states."
---

# Color system

Define usable semantic colors for interface states.

## Workflow

1. Collect the rendered color pairs in each supported theme. Distinguish semantic role from palette shade.
2. Measure foreground/background contrast and check whether a shape, icon or label also communicates state.
3. Revise the semantic mappings and compare selected, warning and disabled states side by side.

## Try it

A selected row and a warning row use nearly identical colors.

**Expected result.** A token table and examples that distinguish selection from warning without relying only on color.

Add a state label or icon so selection and warning remain distinguishable even when viewed without color.

**Limit.** Transparent layers need measurement after compositing.
