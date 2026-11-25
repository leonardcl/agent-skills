# Selected observations and candidate lessons

Use the project’s authorized existing memory system when it has one. For an explicit local ledger, the [project ledger helper](../ledger.py) keeps a SQLite file at the path the user chooses. Give it a new private path per project. Its project binding rejects an attempt to open the same database as another project. It reads no transcripts, home profiles or other projects.

Use only an approved, short redacted paraphrase. Keep source IDs local and opaque. Named people, unreleased material, credentials and raw messages stay out of the ledger. If the selected material cannot be represented without disclosing it, skip that observation. This requires human judgment, including for strings that look harmless in isolation.

Example with Python 3 in a private scratch directory:

```sh
python3 ledger.py --db reading.sqlite --project reading propose wrap "Wrap long titles before reducing type"
python3 ledger.py --db reading.sqlite --project reading observe wrap r1 support "Long title clipped in the narrow list"
python3 ledger.py --db reading.sqlite --project reading observe wrap r1 support "Long title clipped in the narrow list"
python3 ledger.py --db reading.sqlite --project reading observe wrap r2 contradict "The other view already wrapped; its parent clipped the row"
python3 ledger.py --db reading.sqlite --project reading show wrap
python3 ledger.py --db reading.sqlite --project reading revise wrap "Inspect the fixed-height parent when wrapped rows clip"
python3 ledger.py --db reading.sqlite --project reading review wrap accepted
```

The repeated observation ID contributes once. A changed report under the same ID is a conflict. Give a correction its own ID and revise or retire the original lesson explicitly. A new counterexample reopens even an accepted candidate for review. Retirement preserves the evidence for audit.

Broader use is a separate user decision. Ask which project or audience may receive which general wording. After approval, use `promote ID DESTINATION "approved general wording"` to record the decision in the originating database and print that wording for review. It does not publish, create a global profile or transfer evidence. Writing to another destination requires its own authority.

The upstream observes tool events through hooks, can start a background observer and can construct histories from sessions. Those components require upstream installation, permissions, project selection, retention limits and an explicit data decision. None are included or started by the portable edition.
