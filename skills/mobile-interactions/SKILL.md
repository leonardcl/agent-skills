---
name: mobile-interactions
description: "Improve touch and viewport behavior in a mobile web interface."
---

# Mobile interactions

Improve touch and viewport behavior in a mobile web interface.

## Workflow

Reproduce the blocked action on the target device. With the keyboard open, identify what actually scrolls, which element owns focus and whether the final control is inside that scrollable area. A fixed footer can fit the layout viewport while sitting behind the keyboard.

If the outer page can scroll but the form cannot, inspect nested overflow and height constraints. If only a fixed action is hidden, compare its position with the visible viewport and bottom inset before changing the whole layout. Retest typing, scrolling to the final action, submitting and dismissing the keyboard in both orientations. Identify simulated checks separately from physical-device observations.

## Try it

A footer button is covered by the keyboard while editing a field.

**Expected result.** The focused control and final action remain reachable during text entry.

After the keyboard opens, scroll the active field and submit button into reach on a real device. A desktop height reduction tests only part of this behavior.

**Limit.** Desktop emulation may differ from the device keyboard and browser chrome.
