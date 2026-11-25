# Agent Skills

Reusable skills for coding and research assistants. Each skill has a directory with a SKILL.md file describing when to use it, what to do, and how to check the result.

## Try evidence notes

Use [evidence-notes](skills/evidence-notes/SKILL.md) to save a decision or test result in a Markdown notebook. Download or clone this repository, open a local assistant in the checkout, and give it a scratch notebook and this prompt:

> Read skills/evidence-notes/SKILL.md. Record that three of four participants found the receipt link in layout B during my prototype test. We did not measure task time. Show me the resulting entry.

The entry should preserve the count, identify your report as the source, and leave task time open. Check the link from the surrounding notebook.

## Install and update

For Claude Code, copy the evidence-notes directory from skills into ~/.claude/skills. Agents that discover the shared user skill directory can read it from ~/.agents/skills. Open a fresh session and ask for evidence-notes by name.

For a linked installation on macOS or Linux, run these commands from the checkout:

    mkdir -p "$HOME/.agents/skills"
    ln -s "$PWD/skills/evidence-notes" "$HOME/.agents/skills/evidence-notes"

Keep the clone at that location. Run the following in the clone to update linked skills, then start a fresh session:

    git pull --ff-only

For a copied installation, review the updated skill and copy its directory again. Keep personal customizations in a separate folder.
