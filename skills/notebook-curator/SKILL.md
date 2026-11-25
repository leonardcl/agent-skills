---
name: notebook-curator
description: "Save, find and connect evidence in a user-selected Markdown notebook."
---

# Notebook curator

Save, find and connect evidence in a user-selected Markdown notebook.

## Workflow

1. Take the notebook directory explicitly from the user or NOTEBOOK_DIR. Resolve the directory and read its index and naming convention.
2. Find an existing note by topic and inspect its surrounding section. Append the observation with its source, date if known and the question left open.
3. Link the note from the relevant index using the notebook's conventions. Reopen the actual files and report the relative path and heading.

## Try it

Record a paper-folding test in a scratch notebook and link it from the topic index.

**Expected result.** An index link reaches the saved evidence, the source is identifiable and an unknown result is left open.

When the same observation is saved twice, keep one topic note and one index link. Add a dated revision only if the second report contributes a new observation or changes the decision.

**Limit.** Write only in the named notebook. Ask for its location if no root has been supplied.

## Scratch example

Create an empty folder, add a file named `Index.md` containing `# Index`, and supply this folder as the notebook. Ask the assistant to record “The square sheet folded flat on the first attempt. Durability was not measured.” A new or existing topic note should preserve both statements with their source. The index should contain a link that resolves to it. A second request with the same evidence should reuse the note and avoid duplicate links.
