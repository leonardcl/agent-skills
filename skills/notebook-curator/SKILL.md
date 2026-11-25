---
name: notebook-curator
description: "Save, find and connect evidence in a user-selected Markdown notebook."
---

# Notebook curator

Save, find and connect evidence in a user-selected Markdown notebook.

## Workflow

Use the directory named in the request first, then NOTEBOOK_DIR if the request gives no location. Resolve it and read a nearby note and the relevant index. Search titles, aliases and body text. When titles collide, follow the index path and compare the surrounding evidence before choosing a destination.

For a lookup, answer from the passages you found and give paths and headings. For a save, append to the existing topic or create a note beside comparable entries. Credit the source and its date when known. Preserve earlier evidence when a later report disagrees. Record what changed and what remains unknown. If the same source already records the observation, reuse it.

Use the notebook's existing link style. Resolve the link from the index file's own directory and open its target, including the heading if present. Qualify ambiguous links with their folder. Report the note and section so the reader can reopen them.

## Try it

Record a paper-folding test in a scratch notebook and link it from the topic index.

**Expected result.** An index link reaches the saved evidence, the source is identifiable and an unknown result is left open.

When the same observation is saved twice, keep one topic note and one index link. Add a dated revision only if the second report contributes a new observation or changes the decision.

**Limit.** Write only in the named notebook. Ask for its location if no root has been supplied.

## Scratch example

Create an empty folder, add a file named `Index.md` containing `# Index`, and supply this folder as the notebook. Ask the assistant to record “The square sheet folded flat on the first attempt. Durability was not measured.” A new or existing topic note should preserve both statements with their source. The index should contain a link that resolves to it. A second request with the same evidence should reuse the note and avoid duplicate links.
