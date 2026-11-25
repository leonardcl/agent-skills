---
name: artifact-inventory
description: "Create a passive inventory of a supplied archive and distinguish metadata from inference."
---

# Artifact inventory

Create a passive inventory of a supplied archive and distinguish metadata from inference.

## Workflow

1. Read the container directory without extracting or executing entries. Record names, sizes and the supplied artifact's digest.
2. Identify readable documentation from file signatures and encoding. Treat filenames as labels until their contents confirm their role.
3. Return an inventory with a source entry for each claim and list opaque files separately.

## Try it

List the text resources in a sample ZIP without running its contents.

**Expected result.** A digest and a list of observed resources with uncertainty marked for unreadable entries.

A ZIP entry named index.txt establishes a stored filename. Its purpose stays unconfirmed until the user supplies readable content or accompanying documentation.

**Limit.** Scope is passive documentation of supplied files. Encrypted or unrecognized contents stay unresolved.

## Inspect an example

Create a scratch directory containing a text file named `index.txt`. With Python 3 run `python3 -m zipfile -c sample.zip index.txt`, then `python3 -m zipfile -l sample.zip`. The listing should include one entry with its uncompressed length. Use `shasum -a 256 sample.zip` or the equivalent local file-hashing utility to identify the exact container. Record “index.txt, text supplied for this exercise” as an observation and keep the file unopened if you only need the directory.
