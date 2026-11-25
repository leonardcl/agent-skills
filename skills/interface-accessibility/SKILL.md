---
name: interface-accessibility
description: "Check the accessibility of a complete interaction using keyboard and contrast evidence."
---

# Interface accessibility

Check the accessibility of a complete interaction using keyboard and contrast evidence.

## Workflow

1. Follow the form using only a keyboard, including its validation error and recovery. Record focus position at each state.
2. Inspect the accessible name and state announcement. Measure the actual foreground and background colors for text and focus indicators.
3. Repeat the failing step after a fix and record the original and revised result.

## Try it

Tab through a search form whose submit button uses light gray text.

**Expected result.** A keyboard trace, actual contrast measurement and issue location for each failed state.

A gray label can appear acceptable at a glance while missing the normal-text threshold. Compare the unrounded ratio with the threshold and retest the actual composited colors.

**Limit.** A two-color measurement cannot establish accessibility of an entire interface.

## Measure a text pair

From this skill directory run `python3 contrast-check.py 777777 FFFFFF`. Expect a ratio near 4.48 and a failure for normal text. The 3:1 large-text threshold applies at 18 pt regular or 14 pt bold. The [WCAG contrast criterion](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) defines the exceptions. Run `python3 contrast-check.py --selftest` to recalculate each reference pair.

| Pairing (text on background) | Ratio | Normal text (4.5) | Large text (3.0) |
|------------------------------|-------|-------------------|------------------|
| Black on white | 21.00 | Pass | Pass |
| White on black | 21.00 | Pass | Pass |
| White on #333333 | 12.63 | Pass | Pass |
| White on #666666 | 5.74 | Pass | Pass |
| #777777 on white | 4.48 | Fail | Pass |
| #777777 on #070707 | 4.50 | Fail | Pass |
| White on #888888 | 3.54 | Fail | Pass |
| White on #999999 | 2.85 | Fail | Fail |
| #555555 on black | 2.82 | Fail | Fail |
