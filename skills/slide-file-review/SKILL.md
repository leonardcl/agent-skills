---
name: slide-file-review
description: "Inspect a finished slide file for text, geometry and font issues before handoff."
---

# Slide file review

Inspect a finished slide file for text, geometry and font issues before handoff.

## Workflow

1. Run the bundled checker on a copy of the PPTX. Read each reported slide number and shape name in the source deck.
2. Open the affected slide in its target viewer. Distinguish intentional bleed from clipped body text, especially with substituted fonts.
3. Fix the editable source, export again and rerun the same command. Record any remaining intentional exceptions.

## Try it

Inspect a presentation with a text box extending past the right edge.

**Expected result.** A slide and shape reference, the visible consequence and the result of checking the corrected export.

A photograph may bleed beyond the canvas intentionally. The same bounds on a paragraph can hide its last word. Cite the actual shape type and inspect the text in presentation mode.

**Limit.** Static XML checks cannot certify identical rendering on another device.

## Run the checker

From this directory run `python3 check_deck.py --self-test` for a synthetic deck with planted faults. To inspect your own file, run `python3 check_deck.py sample.pptx`. Python 3 reads the XML directly. Exit codes 0, 1 and 2 mean no errors, detected errors and unreadable input respectively. Warnings may appear even with exit code 0. The file is opened read-only.

Supply font directories in `DECK_FONT_DIRS` (separate multiple paths using your platform path separator) to check font filenames. Without a font directory, the checker reports that the local font lookup was skipped.
