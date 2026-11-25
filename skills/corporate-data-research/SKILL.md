---
name: corporate-data-research
description: "Summarize, check and visualize supplied tabular data using reproducible local analysis."
---

# Corporate data research

Establish row grain, key, units, observation window and missing-value handling. Inspect duplicates before joining. Keep a small reconciliation table of input counts, exclusions and output totals. Use a read-only local database or a copy of the data.

Choose the [task procedure](references/workflows.md) matching the requested outcome. Available topics include csv-data-summarizer, data-context-extractor, data-exploration, data-validation.

## Try it

A three-row export has two identical rows for the same invoice and one distinct invoice.

**Expected result.** A report shows raw row count, the chosen identity rule and both the raw and deduplicated totals.

**Limit.** A local extract establishes the contents of the supplied snapshot only.
