# Corporate data research workflows

## csv-data-summarizer

Read a local table with its actual delimiter and header. Report row grain, distinct keys, missing counts and descriptive statistics with units. Check one summary against a manual calculation.

## data-context-extractor

Build a small data dictionary from headers, documented definitions and sample rows. Label inferred meanings as provisional and identify joins whose keys are not unique.

## data-exploration

Inspect distributions, ranges and outliers before testing a hypothesis. Compare slices with their denominators, retain missing values in the profile and record the next question the data can answer.

## data-validation

Translate declared constraints into checks for key uniqueness, required values, ranges and cross-table totals. Return failing row identifiers from a synthetic copy and reconcile passed plus failed counts.

## data-visualization

Choose the chart from the comparison: ordered time for a trend, shared baseline for categories, points for a relationship. Label units and sample size and verify plotted values against the source rows.

## interactive-dashboard-builder

Start with one decision and a filter that changes its underlying denominator. Verify the displayed totals before and after filtering and show an explicit empty result for a slice with no rows.

## postgres

Inspect a supplied schema dump or explicitly local read-only sample. Check grain and key cardinality before aggregating. Compare a hand-counted subset with the resulting grouped query.

## search-strategy

Break an information need into terms, synonyms and a source order. Search the supplied local corpus, record relevant misses and refine the query against a known relevant example.

## source-management

Assign a stable source ID, date, provenance and access boundary to each supplied document. Deduplicate versions while preserving the original citation and record which claims depend on superseded data.

## sql-queries

Write a local read-only query that states its grouping grain and time bounds. Compare counts before and after each join and keep null-handling explicit. Reconcile to a source subtotal.

## statistical-analysis

Specify the estimand, unit of observation and sample selection before calculating. Inspect paired versus independent observations, show uncertainty and keep exploratory findings separate.
