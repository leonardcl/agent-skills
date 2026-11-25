---
name: change-impact
description: "Identify the callers and persisted state affected by a proposed change."
---

# Change impact

Identify the callers and persisted state affected by a proposed change.

## Workflow

1. Trace readers, writers and migration paths. Include stored values created before the current version.
2. Build a matrix for new, existing and unknown values across each entry point.
3. Exercise the widest affected path in a disposable profile and record how to restore the previous state.

## Try it

Change a saved sort preference from a label to an identifier.

**Expected result.** The matrix shows how an old label loads, how a new ID saves and what happens to an unknown value.

A preference named by a translated label may decode differently after a locale change. Keep one fixture from the older format and another containing an unrecognized value.

**Limit.** Unreachable clients stay explicitly unverified.

## Preference migration example

| Stored value | First load | Next save |
| --- | --- | --- |
| No entry | Documented default | Current identifier |
| Recognized legacy label | Corresponding sort | Current identifier |
| Unknown value | Defined fallback | Follow the product's explicit preservation rule |

Set the fallback and preservation rule from the application contract before changing storage.
