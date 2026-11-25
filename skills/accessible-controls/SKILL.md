---
name: accessible-controls
description: "Review semantic controls, focus movement and error recovery."
---

# Accessible controls

Review semantic controls, focus movement and error recovery.

## Workflow

1. Inspect the field's accessible name, required state and error association.
2. Submit an empty value with the keyboard. Locate focus and the announced feedback, then correct the value.
3. Check the valid path and record the specific semantics and behavior needed for recovery.

## Try it

A required field shows a red border after submission with no explanation.

**Expected result.** A user can identify the invalid field, hear or read the reason and submit after correcting it.

After a failed submission, connect the error text to the field and identify it without relying on color. Recheck the same field after a valid value.

**Limit.** Screen reader announcements vary across platform combinations.
