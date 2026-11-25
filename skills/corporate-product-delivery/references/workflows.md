# Corporate product delivery workflows

## brainstorming

Restate a user problem and the constraint any idea must satisfy. Generate options with different mechanisms. Keep the cheapest experiment that distinguishes the leading options.

## changelog-generator

Group a supplied set of commits by user-visible change, link each claim to its revision and flag breaking changes. Omit internal churn unless it alters a user action.

## developer-growth-analysis

Use selected work samples and the developer’s stated goal. Identify a recurring, observable skill gap, one counterexample and a practice exercise. Exclude private chat activity and personal ranking.

## documentation

Choose the reader’s task and the version it applies to. Run the worked example from its documented starting state and report the output and missing prerequisite.

## incident-response

For a routine availability interruption, identify the affected user path, compare the last healthy and current fixture, and record the smallest reversible restoration. Verify recovery through the same path.

## langsmith-fetch

Use a supplied redacted trace export. Order spans by parent ID and timestamps, identify the first divergent input or error, and report only the fields needed to replay a benign local case.

## mcp-builder

Design a read-only local tool over synthetic records. Define its input schema, deterministic output and missing-record behavior. Check a valid ID and an unknown ID before considering a host integration.

## prd-writer

Describe the target user, baseline problem, expected result, non-goals and acceptance cases. Map each proposed requirement to evidence or an open product decision.

## roadmap-builder

Compare proposed outcomes against capacity, dependencies and confidence. Sequence by customer value and prerequisites. Identify the evidence that could move a later item forward.

## sprint-planning

Choose a sprint goal and compare ready work with actual capacity. Split items that cannot demonstrate a result independently and identify the dependency that could prevent the first usable increment.

## system-design

Draw the boundary around the request path, data owner and persistence layer. Walk a normal request, retry and dependency timeout. Record the consistency and capacity assumptions each choice requires.

## tech-debt

Locate the repeated cost using actual change examples. Compare the smallest repair with deferral, including migration risk. Define a measurable reduction in future work.

## testing-strategy

Map requirements to failure modes and choose a boundary that observes each one. Keep a small real entry-point check alongside fast isolated tests and state which external behavior remains unverified.
