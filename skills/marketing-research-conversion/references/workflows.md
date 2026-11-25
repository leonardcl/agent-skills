# Marketing research conversion workflows

## ab-testing

State one population, randomized unit, change and primary outcome. Fix the decision window before looking at results. Report counts and denominators in each arm and check guardrails before interpreting uplift. See the [detailed guidance](ab-testing-detail.md).

## analytics

Define the unit, event, eligible denominator and attribution window. Use a local event sample to calculate the funnel, deduplicating retries by event or user identity according to the stated metric. See the [detailed guidance](analytics-detail.md).

## attribution

Order each fictional customer journey by timestamp. Compute first-touch and last-touch credit on the same sales and reconcile both totals to recorded revenue. Credit reallocation alone cannot establish incrementality.

## conversion-tracking

Specify the exact action that should count, event identity and expected payload. Replay a duplicate and a failed completion in local event data. Reconcile successful unique actions with the summary count.

## cro

Locate the first large drop in a comparable funnel. Inspect the page at that step with the supplied intent and device constraints. Propose one mechanism and test that the revised route still reaches the primary action. See the [detailed guidance](cro-detail.md).

## customer-research

Choose the study question first. Code selected anonymized observations by task, trigger and obstacle, retaining source IDs. Keep behavior separate from interpretation and count participants rather than repeated mentions.

## paywalls

Identify when the user encounters the limit, what remains accessible and how an upgrade changes the outcome. Compare exposure, upgrade and abandonment using the same cohort and confirm the exit route works. See the [detailed guidance](paywalls-detail.md).

## popups

Choose a trigger related to the visitor’s current task. Define frequency cap, dismissal and suppression after completion. Test a returning visitor and keyboard dismissal before judging conversion impact. See the [detailed guidance](popups-detail.md).

## signup

Count eligible sessions, starts and successful registrations. Inspect each required field and its error recovery. Test one valid entry, one invalid entry and a return after correction before proposing fewer fields. See the [detailed guidance](signup-detail.md).
