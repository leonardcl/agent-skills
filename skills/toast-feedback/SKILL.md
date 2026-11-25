---
name: toast-feedback
description: "Choose and verify toast feedback for a short-lived interface action."
---

# Toast feedback

Choose and verify toast feedback for a short-lived interface action.

## Workflow

1. Check the installed notification library's API and locate the existing app-level toast host.
2. Associate pending and final messages with one operation so retries update the right notification. Keep recoverable errors actionable.
3. Trigger success and failure in a scratch view and verify announcements and dismissal without relying on color.

## Try it

Saving a local note may succeed, fail or be retried.

**Expected result.** One feedback sequence per save, an actionable error and no accumulating duplicate notifications.

If no message appears, trigger a simple notification inside the existing host before debugging the save callback. If pending never clears, compare the identifiers used to create and update it. Give independent saves distinct identifiers. For a retry on the same note, guard against an older completion replacing the current result. Force the first attempt to finish last and verify that the message still describes the latest save.

**Limit.** Long-lived or blocking problems need a durable surface.
