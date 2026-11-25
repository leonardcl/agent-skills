---
name: notebook-links
description: "Trace outgoing Markdown links and backlinks with source-line evidence in a selected notebook."
---

# Notebook links

Trace outgoing Markdown links and backlinks with source-line evidence in a selected notebook.

## Workflow

1. Pass the explicit notebook and an external cache to the bundled reader. Index once and review missing or ambiguous targets.
2. Query Reading with the incoming direction. Open the originating line and distinguish an authored reference from an inferred reverse edge.
3. For duplicate basenames use a notebook-relative path. Report the count and unresolved references separately.

## Try it

An Index note contains a link to Reading. Find who linked to Reading and show the source line.

**Expected result.** The incoming query reports Index.md and its line number. An outgoing query on Reading shows no authored return link unless one exists.

An incoming edge belongs to the note that contains the link. Quote that line, then query the target in the outgoing direction before claiming a reciprocal link.

**Limit.** The reader skips symlinks and hidden directories. It resolves documents rather than heading-level graph nodes.

## Run the reader

Use Python 3.9 or later on macOS or Linux with PyYAML 6 installed in the same environment. From this skill directory, run the commands below. If you need PyYAML, install the [declared dependency](requirements.txt) in your own virtual environment.

```sh
scratch=$(mktemp -d)
mkdir "$scratch/notes"
printf '# Index\nSee [[Reading]].\n' > "$scratch/notes/Index.md"
printf '# Reading\n' > "$scratch/notes/Reading.md"
python3 vault_graph.py --vault "$scratch/notes" --cache-dir "$scratch/cache" index
python3 vault_graph.py --vault "$scratch/notes" --cache-dir "$scratch/cache" query Reading --direction in
python3 test_vault_graph.py
```

Expect two notes, one resolved reference and an incoming occurrence at `Index.md:2`. The cache stores note names, aliases and link targets. Use a directory you control outside the notebook. You may set `NOTEBOOK_DIR` instead of passing `--vault`. Query snippets include original text. Use a local terminal for material you want to keep off hosted services.

For a separate document-to-wiki compilation workflow, consult the [pinned upstream instructions](https://github.com/LCccode/Karpathy-wiki-graph/tree/1efa4fe605ac457a61972293976d7d94bda04587). Stage copies in a separate knowledge base and keep the source notebook intact.
