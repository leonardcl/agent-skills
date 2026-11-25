---
name: module-boundaries
description: "Plan a module boundary around a behavior shared by callers."
---

# Module boundaries

Plan a module boundary around a behavior shared by callers.

## Workflow

1. Trace both callers from input to visible result. Write down the rounding contract each caller promises.
2. Sketch two interfaces. Walk an empty report and a half-cent tie through both before choosing a boundary.
3. Move the smallest shared calculation behind the chosen interface. Keep presentation and rounding policy explicit at call sites.

## Try it

Two report screens calculate the same total using different rounding rules.

**Expected result.** A caller table, an interface sketch and a regression case for each rounding policy.

Rounding at display time and rounding each line item can produce different totals. Keep the input amounts exact and test a half-cent tie at both callers before extracting the shared operation.

**Limit.** Conflicting product rules need a decision before consolidating them.
