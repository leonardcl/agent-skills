# Offline integration guide

Choose a skill by the result you need. Every listed group contains actual skill directories in this checkout. OpenDesign's `threejs` discovery name resolves to the single local CloudAI-X rendering edition.

| Outcome | Group | First entry |
| --- | --- | --- |
| A visible, selectable object, camera, light or asset budget | rendering | [Three.js](skills/threejs/SKILL.md) |
| A game with controls, a goal, feedback and restart | games | [Three.js game creation](skills/threejs-game-creation/SKILL.md) |
| A decision for an organization, internal model, operations review or supplier choice | corporate | [Corporate decisions](skills/corporate-decisions/SKILL.md) |
| A read-only comparison of public prices, filings, estimates or dated observations | markets | [Public market research](skills/public-market-research/SKILL.md) |
| Customer evidence, conversion diagnosis or an experiment, campaign or retention plan | marketing | [Marketing research and conversion](skills/marketing-research-conversion/SKILL.md) |
| Close out project work or review a reusable lesson within its memory authority | learning | [Cycle](skills/cycle/SKILL.md) and [Continuous learning v2](skills/continuous-learning-v2/SKILL.md) |
| Apply an evidence-backed brand voice or request an answer-first response | communication | [Brand voice](skills/brand-voice/SKILL.md) and [Answer first](skills/answer-first/SKILL.md) |

For example, use corporate financial analysis to decide whether an internal project covers its fixed cost. Use public market research to reconcile a company's dated results with consensus. Use marketing research and conversion to explain where prospective users abandon registration.

## Invoke a workflow or a named topic

In a host with skill invocation, try `$threejs threejs-geometry` for mesh decisions, `$threejs-game-creation` for a playable loop, `$corporate-legal-procurement supplier-scorecard` for a supplied vendor comparison, or `$marketing-research-conversion attribution` for a fictional funnel. A host with slash commands uses its own invocation syntax. Each specialization is directly selectable by name within the native skill. Use the source map to resolve alternate upstream names.

## Activate only the group you need

From a stable checkout, list the exact names before installing. Choose an actual discovery directory supported by your host. The same commands work with a temporary profile during evaluation.

```sh
python3 tools/packs.py list marketing
python3 tools/packs.py install marketing --profile "$HOME/.agents/skills"
python3 tools/packs.py status marketing --profile "$HOME/.agents/skills"
python3 tools/packs.py uninstall marketing --profile "$HOME/.agents/skills"
```

For Claude Code select its personal skills directory instead. If two profile directories resolve to the same place, install there once. To enable just one specialty, use `python3 tools/profile.py install --profile "$HOME/.agents/skills" corporate-legal-procurement`. The pack installer preserves a conflicting file, directory or foreign link and identifies the conflict. Use the single-skill helper for other names when you want to retain an existing custom equivalent. Each group in [the membership list](integrations/groups.json) can be installed independently.

The [source map](integrations/source-map.tsv) records each upstream entry point, its immutable revision, component provenance, disposition, local skill and exact topic. A topic is the matching heading in that skill's `references/workflows.md`. When a row names an existing standalone equivalent, use the optional `existing-equivalents` group or install just its listed skill. This group also supplies the existing writing companions for Brand voice and Answer first. Multiple source names can share one implementation. The domain references are also usable directly from the public checkout. A normal install creates discovery links only. No hooks, account access, background services or purchases are configured.

## Reproduce and update

Record `git rev-parse HEAD` before installing. To reproduce a release, clone this collection and check out the full release SHA before creating profile links. To update, fetch, inspect the changes to the installed skills, [pins](integrations/sources.json), [component map](integrations/source-map.tsv) and notices, then fast-forward the checkout. Run `python3 tools/verify.py --examples` and `python3 tools/verify_integrations.py` and start a fresh host session. A linked skill follows its checkout. Preserve a separate pinned checkout when you need both versions. For an upstream refresh, review the pinned component and its dependencies, update the local method and source map, then rerun the same fixtures before changing pins.

The two browser examples require an installed Three.js package, a loopback static server and a WebGL-capable browser. They make no external requests during use. The ledger requires Python 3 and its standard SQLite module. Narrative tasks run from supplied artifacts. Native host memory and work-item writes require authorization and a reachable supported host. The repository never enables them.

## Pinned sources and boundaries

| Upstream | Entries reviewed | Local treatment |
| --- | ---: | --- |
| [CloudAI-X/threejs-skills at 0e181866f095](https://github.com/CloudAI-X/threejs-skills/tree/0e181866f095b5f06d005133876e926515390d95) | 13 | MIT technical excerpts for all 13 modules and a local interactive viewer. |
| [affaan-m/ECC at 4adeee6732a1](https://github.com/affaan-m/ECC/tree/4adeee6732a12d1540f49a4d50a38ce8c97f9a53) | 2 | Two selected MIT workflows: manual project learning and a scoped voice profile. Upstream observer, transcript hooks and account readers are not installed. |
| [ayghri/i-have-adhd at 1ecea1993b7f](https://github.com/ayghri/i-have-adhd/tree/1ecea1993b7fce257ffbd686c070948b5e07eda6) | 1 | MIT adaptation for a user-selected response style without diagnostic assumptions or persistent global settings. |
| [coreyhaines31/marketingskills at 8fd2fcade2fd](https://github.com/coreyhaines31/marketingskills/tree/8fd2fcade2fd6629026e9dfe6d133b55b36968b9) | 53 | Offline research, conversion, acquisition, lifecycle and positioning procedures. Distribution, contact enrichment, spend and live sends are excluded. |
| [himself65/finance-skills at a0850786e72a](https://github.com/himself65/finance-skills/tree/a0850786e72aa23b92862f9f1635b0de506fe206) | 26 | Local read-only methods for supplied public snapshots. Private readers and hosted data connectors are replaced by selected public exports. Conflict-specific monitoring is excluded. |
| [majidmanzarpour/threejs-game-skills at 8286774b22a2](https://github.com/majidmanzarpour/threejs-game-skills/tree/8286774b22a2566bf894dbc825825c16921866af) | 9 | Nine reviewed roles mapped to local game workflows and a playable example. Generator credentials, paid asset services and third-party art were excluded. |
| [nexu-io/open-design at 5fdcc3db1e31](https://github.com/nexu-io/open-design/tree/5fdcc3db1e31bd4fa70f673041b78e87977507c3) | 1 | One discovery alias for the same local rendering skill. No second implementation or platform dependency. |
| [safety-quotient-lab/psychology-agent at 38f8a43e55ac](https://github.com/safety-quotient-lab/psychology-agent/tree/38f8a43e55ac5b15102b64a52008fe4587b67127) | 1 | Modified Apache-2.0 cycle with NOTICE. Local outcome routing replaces lab-specific memory, commit and export steps. No model weights or datasets. |
| [w95/awesome-claude-corporate-skills at 78dbc7c71992](https://github.com/w95/awesome-claude-corporate-skills/tree/78dbc7c719920610d5b1c60bd13d9bb52d711c7a) | 166 | Per-component inventory across 14 departments. Independently authored procedures or existing local equivalents. The aggregate MIT notice does not determine external component rights. |

The corporate aggregate labels its third-party providers independently. Its four office-format components declare proprietary terms, and several other components carry their own Apache notices. No source text, binaries, templates or scripts from those aggregated third-party components are bundled. The local office-format skill covers ordinary editable artifacts using an installed viewer or library. Vendor-only fidelity and hosted functionality remain unverified. MIT notices for the named distributions and the cycle Apache notice travel with their editions.

The capability map counts named workflows, not every upstream platform feature. Service-specific inputs may be used as supplied public exports. A local fixture demonstrates processing of that export only. The selected examples do not certify paid services, personalized financial or legal conclusions, physical mobile devices, private accounts, outreach or live project-memory writes.
