---
name: behavior-specification
description: "Turn settled decisions into a testable specification."
---

# Behavior specification

Turn settled decisions into a testable specification.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

Start with a settled decision and trace one user journey from entry state through action to observable result. Define ambiguous terms with contrasting examples. A saved paragraph might mean the last one opened or the last one completed. Those differ when a reader leaves halfway through.

Separate current implementation facts from assumptions the design depends on. Verify that saved paragraph IDs survive edits before relying on them. If that is unknown, name the missing evidence. Give each agreed rule an acceptance example and a boundary at which to check it. Keep unresolved product choices visible so implementers can tell which cases are ready.

## Try it

A bookmark should reopen the last paragraph a reader completed.

**Expected result.** A spec with normal, first-use and missing-paragraph examples plus remaining questions.

A bookmark that points to a deleted paragraph needs an explicit fallback. Show that state alongside first use and ordinary reopening so an implementer can distinguish them.

**Limit.** Do not silently settle open product choices.
