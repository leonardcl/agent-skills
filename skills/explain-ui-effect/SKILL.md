---
name: explain-ui-effect
description: "Explain an interface effect from visible evidence and accessible implementation details."
---

# Explain ui effect

Explain an interface effect from visible evidence and accessible implementation details.

Use this workflow when the user selects it or specifically asks for this deliverable.

## Workflow

1. Compare adjacent frames and distinguish translation, shadow and changes in surrounding layout.
2. If the source is available inspect the computed styles for the same state. Without source, label the proposed mechanism as inference.
3. Describe the smallest independent example that would distinguish two possible implementations.

## Try it

A card seems to lift when focused in a demo.

**Expected result.** An evidence-backed description and a small verification recipe for the effect.

Stable element bounds and a changing shadow support elevation styling. A measured vertical change in the element's transform supports translation as well.

**Limit.** A recording alone rarely establishes the original implementation.
