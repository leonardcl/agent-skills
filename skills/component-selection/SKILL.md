---
name: component-selection
description: "Choose a component library based on the project's actual constraints."
---

# Component selection

Choose a component library based on the project's actual constraints.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

Start with the controls and dependencies already available in the project. Use a representative interaction to decide what is missing. For a date picker, establish whether the requirement concerns display, typed input, stored value or all three. A correctly translated month label tells you nothing about parsing an ambiguous numeric date.

Compare only candidates that meet the required platform and license constraints. Exercise the deciding case with the installed version: type a date whose day and month can be swapped, navigate by keyboard, submit and read back the stored date. Compare that result with the expected date in the requested locale. Prefer the existing control when it passes the same case. Record the failing requirement if an additional dependency earns its place.

## Try it

Choose a date picker that supports keyboard navigation and a required locale.

**Expected result.** A decision record with a working sample, required behaviors checked and remaining trade-offs.

Demonstrate one locale-specific date and one keyboard-only selection before choosing the library. Capture the installed version with the sample.

**Limit.** Package features, licenses and maintenance status require checking the actual version.
