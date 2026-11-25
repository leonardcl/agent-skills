"""Maintain a manually selected, project-bound candidate lesson ledger."""
import argparse
import json
import re
import sqlite3
from pathlib import Path


def identifier(value):
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,79}", value):
        raise argparse.ArgumentTypeError("use a short opaque identifier")
    return value


def bounded(value):
    value = value.strip()
    if not value or len(value) > 280 or "\n" in value:
        raise argparse.ArgumentTypeError("use one redacted sentence of up to 280 characters")
    # Reject common accidental identifiers. The person selecting evidence decides its sensitivity.
    if re.search(r"\S+@\S+|https?://|(?:/Users/|/home/)|(?:password|token|secret|api[_ -]?key)\s*[:=]|BEGIN .*PRIVATE KEY", value, re.I):
        raise argparse.ArgumentTypeError("remove personal identifiers, links and credential-like material")
    return value


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--db", required=True, type=Path)
    cli.add_argument("--project", required=True, type=identifier)
    sub = cli.add_subparsers(dest="action", required=True)
    for action in ("propose", "observe", "show", "revise", "review", "promote"):
        p = sub.add_parser(action)
        p.add_argument("lesson", type=identifier)
        if action in ("propose", "revise"):
            p.add_argument("wording", type=bounded)
        if action == "observe":
            p.add_argument("event", type=identifier)
            p.add_argument("direction", choices=("support", "contradict"))
            p.add_argument("evidence", type=bounded)
        if action == "review":
            p.add_argument("status", choices=("candidate", "accepted", "retired"))
        if action == "promote":
            p.add_argument("destination", type=identifier)
            p.add_argument("wording", type=bounded)
    return cli


def apply(db, args):
    db.execute("BEGIN IMMEDIATE")
    tables = {row[0] for row in db.execute("SELECT name FROM sqlite_schema WHERE type='table'")}
    if tables and not {"scope", "lessons", "events", "promotions"} <= tables:
        raise ValueError("choose a new file or an existing lesson ledger")
    db.execute("CREATE TABLE IF NOT EXISTS scope (singleton INTEGER PRIMARY KEY CHECK(singleton=1), project TEXT NOT NULL)")
    db.execute("INSERT OR IGNORE INTO scope VALUES (1, ?)", (args.project,))
    if db.execute("SELECT project FROM scope").fetchone()[0] != args.project:
        raise ValueError("database belongs to another project")
    db.execute("CREATE TABLE IF NOT EXISTS lessons (id TEXT PRIMARY KEY, wording TEXT NOT NULL, status TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS events (lesson TEXT, id TEXT, direction TEXT, evidence TEXT, PRIMARY KEY(lesson,id))")
    db.execute("CREATE TABLE IF NOT EXISTS promotions (lesson TEXT, destination TEXT, wording TEXT, PRIMARY KEY(lesson,destination,wording))")
    key = (args.lesson,)
    lesson = db.execute("SELECT wording,status FROM lessons WHERE id=?", key).fetchone()
    if args.action == "propose":
        if lesson and lesson[0] != args.wording:
            raise ValueError("lesson exists; use revise to change wording")
        db.execute("INSERT OR IGNORE INTO lessons VALUES (?,?,'candidate')", (*key, args.wording))
    elif not lesson:
        raise ValueError("unknown lesson")
    elif args.action == "observe":
        previous = db.execute("SELECT direction,evidence FROM events WHERE lesson=? AND id=?", (*key,args.event)).fetchone()
        observation = (args.direction, args.evidence)
        if previous and previous != observation:
            raise ValueError("event ID already used; supply a new ID for corrected evidence")
        if not previous:
            db.execute("INSERT INTO events VALUES (?,?,?,?)", (*key,args.event,*observation))
            if args.direction == "contradict" and lesson[1] == "accepted":
                db.execute("UPDATE lessons SET status='candidate' WHERE id=?", key)
    elif args.action == "revise":
        db.execute("UPDATE lessons SET wording=?,status='candidate' WHERE id=?", (args.wording,*key))
    elif args.action == "review":
        db.execute("UPDATE lessons SET status=? WHERE id=?", (args.status,*key))
    elif args.action == "promote":
        if lesson[1] != "accepted" or args.destination == args.project:
            raise ValueError("promotion requires an accepted lesson and a distinct, approved destination")
        db.execute("INSERT OR IGNORE INTO promotions VALUES (?,?,?)", (*key,args.destination,args.wording))
        return {"destination":args.destination, "wording":args.wording}
    wording,status = db.execute("SELECT wording,status FROM lessons WHERE id=?", key).fetchone()
    events = db.execute("SELECT id,direction,evidence FROM events WHERE lesson=? ORDER BY id", key).fetchall()
    result = {"lesson": args.lesson, "status": status, "wording": wording, "observations": events}
    if args.action == "show":
        result["approved_promotions"] = db.execute(
            "SELECT destination,wording FROM promotions WHERE lesson=? ORDER BY destination,wording", key
        ).fetchall()
    return result


def main():
    cli = parser()
    args = cli.parse_args()
    if not args.db.is_file() and args.action != "propose":
        cli.error("choose an existing project ledger or propose its first lesson")
    try:
        with sqlite3.connect(args.db) as db:
            result = apply(db, args)
        print(json.dumps(result, ensure_ascii=False))
    except (sqlite3.Error, ValueError) as error:
        cli.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
