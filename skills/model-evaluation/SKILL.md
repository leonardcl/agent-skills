---
name: model-evaluation
description: "Compare models on a fixed held-out dataset with reproducible metrics."
---

# Model evaluation

Compare models on a fixed held-out dataset with reproducible metrics.

## Workflow

1. Freeze the examples, label definitions, split and metric before comparing outputs. Group related examples to prevent leakage.
2. Run both candidates on the same IDs. Report the numerator, denominator and handling of missing predictions.
3. Inspect paired disagreements and group errors by an interpretable slice. Keep exploratory tuning separate from the held-out comparison.

## Try it

Two text classifiers predict labels on the same set of short reviews.

**Expected result.** A protocol, confusion counts, paired error examples and uncertainty appropriate to the sample size.

If each classifier gets three of four examples correct, the shared accuracy does not identify which individual cases changed. Pair predictions by example ID and show both disagreements.

**Limit.** A small or unrepresentative holdout cannot establish real-world performance.

## Hand-check a paired comparison

Use labels A, B, B, A for four held-out items. Candidate P predicts A, A, B, A. Candidate Q predicts B, B, B, A. Both score 3/4. The first two items are disagreements in opposite directions. Reporting only accuracy would hide that difference. Keep a row per item so another reader can recover both numerators.
