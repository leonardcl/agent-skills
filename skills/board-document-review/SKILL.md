---
name: board-document-review
description: "Review schematic and board documents for consistency using a low-voltage example."
---

# Board document review

Review schematic and board documents for consistency using a low-voltage example.

## Workflow

1. Match reference designators and connector orientation across the schematic, board and supplied datasheet. Record revision and viewing side.
2. Trace each pin from number to net and compare pad numbering, including the mirrored bottom view.
3. Report discrepancies with sheet, pad and confidence. Attach the design-rule report when supplied and distinguish observed violations from unresolved checks.

## Try it

Check whether a sensor connector uses the same pin order in the schematic and PCB.

**Expected result.** A pin-by-pin comparison identifies reversed numbering or records when the drawing cannot settle orientation.

Pin 1 on a mating connector can appear on opposite sides in front and rear views. Label the viewing side on both diagrams before calling the pad order reversed.

**Limit.** A document review cannot prove electrical performance or certify fabrication readiness.
