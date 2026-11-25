"""Check pinned source coverage, local workflow targets and isolated lesson behavior."""
import csv
import json
import re
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def inventory():
    config = ROOT / "integrations"
    pins = json.loads((config / "sources.json").read_text())
    packs = json.loads((config / "groups.json").read_text())
    with (config / "source-map.tsv").open() as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len({(r["repository"], r["source_path"]) for r in rows}) != len(rows):
        raise ValueError("duplicate source entry")
    counts = Counter(r["repository"] for r in rows)
    if counts != {name: data["entries"] for name, data in pins.items()}:
        raise ValueError("source counts differ from pins")
    docs = {}
    for row in rows:
        name = row["local_skill"]
        pin = row["revision"]
        if pin != pins[row["repository"]]["revision"] or not re.fullmatch("[a-f0-9]{40}", pin):
            raise ValueError(f"bad source revision for {row['source_path']}")
        if not name:
            if not row["disposition"].startswith("Excluded "):
                raise ValueError(f"missing disposition for {row['source_path']}")
            continue
        skill = ROOT / "skills" / name
        if not (skill / "SKILL.md").is_file():
            raise ValueError(f"missing local skill {name}")
        if row["local_topic"]:
            if name not in docs:
                docs[name] = set(re.findall(r"^## (.+)$", (skill / "references/workflows.md").read_text(), re.M))
            if row["local_topic"] not in docs[name]:
                raise ValueError(f"unknown topic {name}/{row['local_topic']}")
    for names in packs.values():
        if len(set(names)) != len(names) or any(not (ROOT / "skills" / n / "SKILL.md").is_file() for n in names):
            raise ValueError("invalid install group")
    print(f"{len(rows)} pinned entries from {len(pins)} repositories; {len(packs)} install groups; all local targets resolved")


def check_ledger(folder):
    def call(project, db, *args, expected=0):
        result = subprocess.run([sys.executable, ROOT / "skills/continuous-learning-v2/ledger.py", "--db", folder / db,
                                 "--project", project, *args], capture_output=True, text=True)
        if result.returncode != expected:
            raise ValueError(f"unexpected exit for {args[0]}: {result.returncode}")
        return json.loads(result.stdout) if expected == 0 else None
    def alpha(*args, expected=0):
        return call("alpha", "a.sqlite", *args, expected=expected)
    alpha("propose", "label", "Check long labels")
    obs = ("observe", "label", "e1", "support", "Long title clipped")
    alpha(*obs)
    assert len(alpha(*obs)["observations"]) == 1
    alpha("review", "label", "accepted")
    assert alpha("observe", "label", "e2", "contradict", "Wrapped title fit in the second view")["status"] == "candidate"
    alpha("observe", "label", "e1", "support", "Changed evidence", expected=1)
    alpha("observe", "label", "x", "support", "token=example-only", expected=2)
    alpha("promote", "label", "shared", "Check text wrap", expected=1)
    alpha("revise", "label", "Check title wrap only in narrow rows")
    alpha("review", "label", "accepted")
    assert alpha("promote", "label", "shared", "Check title wrap") == {"destination":"shared", "wording":"Check title wrap"}
    alpha("promote", "label", "shared", "Check title wrap")
    assert alpha("show", "label")["approved_promotions"] == [["shared", "Check title wrap"]]
    assert alpha("review", "label", "retired")["status"] == "retired"
    call("beta", "a.sqlite", "show", "label", expected=1)
    call("beta", "b.sqlite", "propose", "other", "Use a labeled sample")
    call("beta", "b.sqlite", "show", "label", expected=1)
    assert b"example-only" not in (folder / "a.sqlite").read_bytes()
    with sqlite3.connect(folder / "other.sqlite") as other:
        other.execute("CREATE TABLE books (title TEXT)")
    before = (folder / "other.sqlite").read_bytes()
    call("beta", "other.sqlite", "propose", "other", "Use a labeled sample", expected=1)
    assert (folder / "other.sqlite").read_bytes() == before
    print("project isolation, duplicate, contradiction, correction, retirement, explicit promotion and private-marker exclusion passed")


if __name__ == "__main__":
    inventory()
    with tempfile.TemporaryDirectory() as tmp:
        check_ledger(Path(tmp))
