---
name: skill-discovery
description: "Find an installable skill and verify that its source and prerequisites match the request."
---

# Skill discovery

Find an installable skill and verify that its source and prerequisites match the request.

## Workflow

1. Describe the task in the user's words and search the supported registry or source repository.
2. Read the actual skill entry point, its dependencies, license and install instructions. Check that it supports the user's profile and input format.
3. Return the original source, installation scope and a small acceptance test. Install only when requested.

## Try it

Find a skill for formatting citations in a local Markdown notebook.

**Expected result.** A candidate with a verified entry point and a concrete test using one sample citation, or a clear account of the missing fit.

Accept a citation tool only after finding its supported Markdown input and output format. A search result with the right title is insufficient evidence for the installation recommendation.

**Limit.** A listing or download count does not verify behavior.
