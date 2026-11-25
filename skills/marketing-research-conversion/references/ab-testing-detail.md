# Metrics Selection

Selected from the MIT-licensed ab-testing workflow by Corey Haines. Use with a supplied local fixture.

### Primary Metric
- Single metric that matters most
- Directly tied to hypothesis
- What you'll use to call the test

### Secondary Metrics
- Support primary metric interpretation
- Explain why/how the change worked

### Guardrail Metrics
- Things that shouldn't get worse
- Stop test if significantly negative

### Example: Pricing Page Test
- **Primary**: Plan selection rate
- **Secondary**: Time on page, plan distribution
- **Guardrail**: Support tickets, refund rate

### Opt-In Elements: Measure the Exposed Group
When a change only reaches visitors who interact with it (a hero video, a calculator, a chat widget), a test on overall conversion is underpowered: if 10% of visitors click play, the other 90% add noise and no signal. Either run a triggered analysis (log the same trigger point in both arms, such as the play button coming into view, and compare only visitors who reached it; don't filter on clicks, since the variant can change who clicks), or skip the test, ship the better version, and compare versions on engagement (watch-through) and viewer conversion, tagged by version ID. The second is a directional comparison, not a controlled test.

---
