---
name: optional-project-skills
description: "Enable an optional set of installed skills for one project and verify where the names resolve."
---

# Optional project skills

Enable an optional set of installed skills for one project and verify where the names resolve.

## Workflow

1. Select the explicit project profile, the candidate skill directory and the discovery path supported by the host. Check the destination for existing entries.
2. Create only the requested links in the chosen profile. Resolve each link and read its entry point before starting a fresh session.
3. Remove only links owned by the checkout and verify other projects still resolve their original skills.

## Try it

Make a reading-note skill discoverable only for a disposable project.

**Expected result.** An install and uninstall in a scratch profile leave a pre-existing unrelated skill intact.

Create one unrelated entry beside the test skill before installing. After uninstall, verify that the unrelated entry still exists and belongs to its original location.

**Limit.** An assistant that discovers skills only at session start needs a new session.

## Try an isolated profile

From the checkout, set `scratch=$(mktemp -d)`, then run `python3 tools/profile.py install --profile "$scratch" evidence-notes`. Read the linked `SKILL.md`, run the same command again, then use `python3 tools/profile.py uninstall --profile "$scratch" evidence-notes`. The second install should recognize the same link and uninstall should remove only that link.
