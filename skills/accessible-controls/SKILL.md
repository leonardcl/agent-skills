---
name: accessible-controls
description: "Review semantic controls, focus movement and error recovery."
---

# Accessible controls

Review semantic controls, focus movement and error recovery.

## Workflow

Start with the control's job. A link navigates, a button performs an action, and an input needs a persistent label. Use the native element's keyboard behavior as the comparison. A styled label that responds to a click may have no keyboard or accessibility-tree counterpart.

Track focus through activation and recovery. In a modal, Tab should remain among its controls and dismissal should restore a usable focus target. On a failed form submission, inspect the invalid field's accessible name, invalid state and error description. Correct the value and submit again. Record the keys pressed, resulting focus and any stale error. Credit an announcement only if you heard it with the named assistive technology.

## Try it

A required field shows a red border after submission with no explanation.

**Expected result.** A user can identify the invalid field, hear or read the reason and submit after correcting it.

After a failed submission, connect the error text to the field and identify it without relying on color. Recheck the same field after a valid value.

**Limit.** Screen reader announcements vary across platform combinations.
