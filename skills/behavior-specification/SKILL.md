---
name: behavior-specification
description: "Turn settled decisions into a testable specification."
---

# Behavior specification

Turn settled decisions into a testable specification.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Trace a representative user journey, then record entry state, action and observable outcome.
2. Define ambiguous terms and how missing or stale data behaves. Record unresolved policy separately.
3. Give each requirement an acceptance example and map examples back to the original decision notes.

## Try it

A bookmark should reopen the last paragraph a reader completed.

**Expected result.** A spec with normal, first-use and missing-paragraph examples plus remaining questions.

A bookmark that points to a deleted paragraph needs an explicit fallback. Show that state alongside first use and ordinary reopening so an implementer can distinguish them.

**Limit.** Do not silently settle open product choices.
