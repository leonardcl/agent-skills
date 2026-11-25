# Agent skills

A collection of portable instructions for reviewing changes, organizing notes, designing interfaces, editing writing and checking finished work. Start with the [catalog](CATALOG.md). Each entry links to the workflow, a realistic input, the expected result and its limits. Each skill directory also carries its own origin statement and license.

## Try a skill before installing it

Clone the collection into a directory you can keep. Open your assistant in the checkout and ask it to read [Evidence notes](skills/evidence-notes/SKILL.md).

```sh
git clone https://github.com/leonardcl/agent-skills.git
cd agent-skills
```

> In a scratch notebook, record that three of four participants found the receipt link in layout B. Nobody measured task time. Link the note from the index and show me the entry.

Give the assistant a disposable notebook directory containing an `Index.md` file. The entry should credit the session report, keep the count intact and leave task time open. Open the resulting index link. For backlink questions, the [notebook reader](skills/notebook-links/SKILL.md) includes a runnable two-note example and a test for ambiguous names. The [notebook curator](skills/notebook-curator/SKILL.md) follows the structure of a notebook you explicitly select.

## Choose an optional workflow group

For Three.js rendering or games, corporate decisions, financial research, marketing, project learning and communication, see the [offline integration guide](INTEGRATIONS.md). The repository contains the usable instructions and examples. A local copy of this checkout is enough to install the groups.

## Install one skill

On macOS or Linux run the helper from the checkout with Python 3.9 or later. Choose the discovery directory your host uses. Each command installs one link. The helper reports a conflict and preserves an existing file, directory or link from another installation.

```sh
# Shared profile, for hosts that read this directory
python3 tools/profile.py install --profile "$HOME/.agents/skills" notebook-curator

# Personal Claude Code profile
python3 tools/profile.py install --profile "$HOME/.claude/skills" notebook-curator
```

You can also pass an explicit project skill directory or a separate Claude profile's `skills` folder. When both profiles already resolve to the same directory, one installation is enough. To try the mechanism without changing a real profile, use `--profile "$(mktemp -d)"`. Keep the checkout at its installed location. Start a fresh assistant session, request the skill by name, and check the output against its example. Host-specific discovery is described in the [Claude Code skill guide](https://code.claude.com/docs/en/skills) and the [Codex skill guide](https://developers.openai.com/codex/skills/).

For a host without symlink support, copy the complete chosen directory from `skills/` to its skill discovery directory. Keep the origin, license, helper files and any `agents/` metadata together. A copied skill can also be used by opening its `SKILL.md` directly.

## Dependencies and optional tools

Most workflows need only their instructions and the input named in the example. Tasks involving a real interface, video, board or source tree require that artifact and a suitable viewer or development environment. A textual walkthrough cannot certify the finished application or physical device.

| Skill | Local requirements | What you can check |
| --- | --- | --- |
| [Notebook links](skills/notebook-links/SKILL.md) | Python 3.9+, PyYAML 6, macOS or Linux | Indexing, backlinks, ambiguous names and cache recovery |
| [Slide file review](skills/slide-file-review/SKILL.md) | Python 3 | Font and geometry findings on a synthetic PPTX |
| [Interface accessibility](skills/interface-accessibility/SKILL.md) | Python 3 | Nine reference contrast pairs |
| [Room layout](skills/room-layout/SKILL.md) | Python 3 | Scaled SVGs, room schedules, structured scene geometry and furniture/clearance conflicts |
| [Audience copy](skills/audience-copy/SKILL.md) | Python 3 | Reading-time estimates for on-screen captions |
| [Bounded iteration](skills/bounded-iteration/SKILL.md) | Bash | An append-only decision log for a local run |

For document editing, framework-specific animation, hosted integrations and optional project planning tools, see [upstream distributions](UPSTREAM.md). Their maintainers supply installation steps and version-specific dependencies.

## Update, pin or remove a skill

Record the revision you tested with `git rev-parse HEAD`. To review an update, fetch the public repository, inspect what changed, then fast-forward the checkout:

```sh
git fetch origin
git diff --stat HEAD..origin/main
git diff HEAD..origin/main -- skills/notebook-curator
git merge --ff-only origin/main
python3 tools/verify.py
```

Linked skills see the updated files. Reload the assistant session. To stay on a reviewed revision, use a separate clean clone and check out its commit with `git switch --detach COMMIT` before linking. For copied skills, compare the old and new folders, preserve any personal edits separately, then replace only the chosen copy.

```sh
python3 tools/profile.py status --profile "$HOME/.claude/skills" notebook-curator
python3 tools/profile.py uninstall --profile "$HOME/.claude/skills" notebook-curator
```

Repeat uninstall for each profile you used, before moving or removing the checkout. For a manual copy, inspect its path and remove that single directory when ready. Notebook files and project inputs live outside the installed skill.

## Troubleshooting

- **Skill missing from the picker.** Confirm the host reads the intended profile, inspect the linked `SKILL.md`, then start a fresh session. Some workflows support explicit invocation only.
- **A name is already installed.** Inspect the existing entry and use a scratch or project profile to compare the two. An existing directory may contain local edits.
- **A helper cannot find its sample.** Run the example from the skill directory or supply full paths to the script and its input. The profile helper runs from the checkout.
- **The notebook reader reports a missing module.** Check `python3 -c 'import yaml'` with the interpreter you plan to use. Install the declared dependency in that environment if needed. Keep the cache outside the notebook. Use a notebook-relative note path to distinguish duplicate titles.
- **An update will not fast-forward.** Inspect `git status` and `git log --oneline --left-right HEAD...origin/main`. Preserve your local work or install from a second clean clone.
- **A test needs an unavailable device or service.** Report the unmet prerequisite and the user path it prevented. A local fixture proves only the behavior it exercises.

## Verify and maintain the collection

Run `python3 tools/verify.py` to check names, catalog entries, notices, source syntax and local links. With Bash and PyYAML 6 available, run `python3 tools/verify.py --examples` to exercise clean profile installation, repeat installation, removal, collision handling and the bundled helpers for six skills. All mutable test inputs live in temporary directories.

To add or revise a skill, work in a clean clone of this public repository. Prepare the selected changes in that checkout, inspect every new file and reference, retain licenses, and replace examples with original fixtures. Exercise the old and new workflow on the same input. Distinguish a static review from results observed through an actual entry point. Review `git diff --cached`, including file modes and metadata, before a deliberate commit and push. The included tools read this collection and write to explicitly chosen local targets. Publishing is a separate Git operation.

## Attribution

See the origin statement and license inside each skill directory. Some are original workflows, others are edited teaching editions of permissively licensed work. The [catalog](CATALOG.md) identifies the distinction. The license in a given directory covers the material identified there. This collection has no blanket grant over independent upstream packages.
