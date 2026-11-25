---
name: motion-vocabulary
description: "Translate an observed motion into a precise description a designer can implement."
---

# Motion vocabulary

Translate an observed motion into a precise description a designer can implement.

## Workflow

1. Inspect the first, middle and last frames. Name the moving object, transform origin, trajectory and settling behavior.
2. Distinguish overshoot from a bounce caused by collision. Describe any opacity change separately.
3. Give one implementation-neutral sentence and a check that would distinguish it from the nearest alternative.

## Try it

Describe a menu that grows from its triggering button and briefly passes its final size.

**Expected result.** A description identifies scaling from the control and overshoot, with the final stable state specified.

If scale exceeds the final size and then settles, describe overshoot. A changing shadow alone does not establish that the underlying object moved.

**Limit.** Frames do not reveal the exact easing function without measurements.
