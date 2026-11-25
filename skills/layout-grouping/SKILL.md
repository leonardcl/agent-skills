---
name: layout-grouping
description: "Improve layout by matching visual grouping to task structure."
---

# Layout grouping

Improve layout by matching visual grouping to task structure.

## Workflow

1. Mark the semantic groups before changing spacing. Inspect the vertical rhythm and reading order at two widths.
2. Adjust proximity, alignment and wrapping so related controls stay together with long labels.
3. Test keyboard order and scan the layout with sample data and validation messages present.

## Try it

An address form places the apartment field closer to billing than to street address.

**Expected result.** Address fields remain visually and semantically grouped at both widths.

Place an apartment validation message below its own field and check that billing controls still read as a separate group at narrow widths.

**Limit.** Short placeholder labels cannot establish behavior with localized content.
