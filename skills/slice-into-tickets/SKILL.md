---
name: slice-into-tickets
description: "Split a specification into independently checkable work items."
---

# Slice into tickets

Split a specification into independently checkable work items.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Trace the smallest complete user path and slice vertically from input to visible result.
2. For each ticket, include context, expected behavior, dependencies and an observable check. Identify work that can proceed independently.
3. Walk the dependency order and make sure the final ticket introduces no hidden integration step.

## Try it

Add a searchable local book list with a clear-empty-state action.

**Expected result.** Tickets cover a first usable search, empty state and clear action with acceptance checks.

A first slice can search a static list and display at least one result. A later slice adds clearing from the empty state while reusing the already working result path.

**Limit.** Creating or assigning tickets in a shared tracker requires the user's request.
