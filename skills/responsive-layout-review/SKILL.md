---
name: responsive-layout-review
description: "Check how content and controls reflow across widths and input methods."
---

# Responsive layout review

Check how content and controls reflow across widths and input methods.

## Workflow

1. Inspect the narrowest supported viewport with real-length labels and enlarged text.
2. Trace the overflow to its containing element. Check wrapping, min-width, keyboard focus and the final tap target.
3. Repeat on a wide viewport and at the breakpoint where the layout changes. Record each width and result.

## Try it

A filter panel clips the last option on a narrow phone.

**Expected result.** A specific overflow cause and evidence that the last option stays reachable on both sides of the breakpoint.

At the narrow width, tab to the last filter and verify its label and activation target are both reachable. A page with no horizontal scrollbar can still clip a nested panel.

**Limit.** Device chrome and on-screen keyboards need a device or an equivalent test environment.
