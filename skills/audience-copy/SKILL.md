---
name: audience-copy
description: "Draft a post from a brief and check whether its factual claims fit the source."
---

# Audience copy

Draft a post from a brief and check whether its factual claims fit the source.

If the brief supplies a voice profile, select its brand, language, audience and channel before drafting. Use Brand voice when the task is to derive that profile from selected samples.

## Workflow

1. Identify who needs the information, the channel, the action and which details are cleared for use.
2. Draft the opening, event detail and action using only supported claims. Compare every name and date to the brief.
3. Preview the copy at its intended length. Flag missing details separately and return an editable draft.

## Try it

Draft a caption for a public reading with a confirmed date and no confirmed guest list.

**Expected result.** A caption containing the confirmed date and a usable next action without naming unconfirmed guests.

A confirmed reading date supports the invitation. A prospective guest list stays out of the caption until a source confirms it, even if omitting it makes the opening less dramatic.

**Limit.** A draft does not establish permission to post or rights to a photograph.

## Time captions

For a post with on-screen words, run `python3 caption_timing.py cards.txt` from this directory. Each line of the [sample](cards.txt) has start and end times in seconds followed by the text. The checker compares the displayed duration with its configured reading-speed estimate. Use `--help` to change the assumptions. Replay the actual export to judge reading effort.
