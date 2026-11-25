---
name: mobile-interactions
description: "Improve touch and viewport behavior in a mobile web interface."
---

# Mobile interactions

Improve touch and viewport behavior in a mobile web interface.

## Workflow

1. Drive the form in portrait and landscape with the on-screen keyboard visible. Record viewport and scroll-container behavior.
2. Check safe areas, focus visibility and tap target reachability. Compare pointer hover effects on touch and mouse.
3. Fix the containing layout and repeat the full edit-submit flow on a representative device.

## Try it

A footer button is covered by the keyboard while editing a field.

**Expected result.** The focused control and final action remain reachable during text entry.

After the keyboard opens, scroll the active field and submit button into reach on a real device. A desktop height reduction tests only part of this behavior.

**Limit.** Desktop emulation may differ from the device keyboard and browser chrome.
