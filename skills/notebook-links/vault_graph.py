#!/usr/bin/env python3
"""Read a local Obsidian wikilink graph with line-level provenance."""
import argparse
from collections import defaultdict
import fcntl
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import sys
import tempfile
import unicodedata
from urllib.parse import unquote

import yaml

VAULT = os.environ.get("NOTEBOOK_DIR")
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "notebook-links"
FORMAT = 3
WIKI = re.compile(r"(?<!\\)\[\[([^\[\]\n]+)\]\]")
INLINE_MD = re.compile(
    r"""(?<!\\)\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|((?:[^\s()]|\([^()]*\))+))"""
    r"""(?:\s+(?:"[^"]*"|'[^']*'))?\s*\)"""
)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
IGNORED = re.compile(r"<!--.*?(?:-->|\Z)|%%.*?(?:%%|\Z)|(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", re.S)


def key(name):
    return unicodedata.normalize("NFC", name).casefold()


def loose(name):
    return re.sub(r"[-\s]+", " ", key(name)).strip()


def note_links(source):
    # Blank examples before scanning and retain original line numbers.
    visible = []
    fence = ""
    for line in source.splitlines():
        match = FENCE.match(line)
        if fence:
            if match and match[1].startswith(fence) and not match[2].strip():
                fence = ""
            visible.append("")
        elif match:
            fence = match[1]
            visible.append("")
        else:
            visible.append(line)
    body = IGNORED.sub(lambda m: "\n" * m[0].count("\n"), "\n".join(visible))
    for n, line in enumerate(body.splitlines(), 1):
        for reference in WIKI.findall(line):
            target = re.split(r"\\?\|", reference, maxsplit=1)[0].split("#", 1)[0].strip()
            if target:
                yield n, target
        for match in INLINE_MD.finditer(line):
            target = match[1] or match[2]
            if target.startswith("//") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if target.lower().endswith(".md"):
                yield n, target if target.startswith("/") else "./" + target


def note_aliases(source):
    front = re.match(r"\A---[ \t]*\n(.*?)\n(?:---|\.\.\.)[ \t]*(?:\n|$)", source, re.S)
    if not front or not re.search(r"(?m)^aliases?\s*:", front[1]):
        return [], False
    try:
        meta = yaml.load(front[1], Loader=yaml.BaseLoader)
    except yaml.YAMLError:
        return [], True
    aliases = meta.get("aliases", meta.get("alias", [])) if isinstance(meta, dict) else []
    aliases = aliases if isinstance(aliases, list) else [aliases]
    return [a.strip() for a in aliases if isinstance(a, str) and a.strip()], False


def fail(error):
    raise error


def refresh(root, cache):
    # A content digest catches edits even if an editor preserves size and mtime.
    cache.mkdir(mode=0o700, parents=True, exist_ok=True)
    name = hashlib.sha256(os.fsencode(root)).hexdigest()
    path = cache / (name + ".json")
    with (cache / (name + ".lock")).open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            saved = json.loads(path.read_bytes())
            if saved["format"] != FORMAT or not isinstance(saved["notes"], dict):
                raise ValueError("invalid cache format")
            old = saved["notes"]
            rebuild = False
        except (FileNotFoundError, ValueError, KeyError, TypeError):
            old = {}
            rebuild = True
        notes = {}
        changed = 0
        for base, dirs, files in os.walk(root, onerror=fail):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not (Path(base) / d).is_symlink())
            for filename in sorted(files):
                if filename.startswith(".") or not filename.lower().endswith(".md"):
                    continue
                note = Path(base) / filename
                if note.is_symlink() or not note.is_file():
                    continue
                rel = note.relative_to(root).as_posix()
                data = note.read_bytes()
                digest = hashlib.sha256(data).hexdigest()
                entry = old.get(rel)
                if not entry or entry["hash"] != digest:
                    source = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
                    aliases, invalid = note_aliases(source)
                    entry = dict(hash=digest, aliases=aliases, bad_alias_yaml=invalid, links=list(note_links(source)))
                    changed += 1
                notes[rel] = entry
        removed = len(old.keys() - notes.keys())
        if changed or removed or rebuild:
            with tempfile.NamedTemporaryFile(mode="w", dir=cache, delete=False) as temp:
                try:
                    json.dump(dict(format=FORMAT, notes=notes), temp, separators=(",", ":"), ensure_ascii=False)
                    temp.flush()
                    os.replace(temp.name, path)
                finally:
                    Path(temp.name).unlink(missing_ok=True)
    return notes, changed, removed, path


class Resolver:
    def __init__(self, notes):
        self.paths = defaultdict(set)
        self.names = defaultdict(set)
        self.variants = defaultdict(set)
        for path, note in notes.items():
            name = Path(path).stem
            self.paths[key(path[:-3])].add(path)
            for label in [name, *note["aliases"]]:
                self.names[key(label)].add(path)
                self.variants[loose(label)].add(path)

    @lru_cache(maxsize=None)
    def resolve(self, label, parent=""):
        name = label[:-3] if label.lower().endswith(".md") else label
        if "/" in name:
            if name.startswith(("./", "../")):
                names = [posixpath.normpath(posixpath.join(parent, name))]
            else:
                names = [name.lstrip("/")]
                if parent and not name.startswith("/"):
                    names.append(posixpath.normpath(posixpath.join(parent, name)))
            return sorted(set().union(*(self.paths.get(key(n), ()) for n in names)))
        return sorted(self.names.get(key(name)) or self.variants.get(loose(name), ()))


def require(resolver, label):
    matches = resolver.resolve(label)
    if len(matches) == 1:
        return matches[0]
    raise ValueError(("Ambiguous: " + ", ".join(matches)) if matches else "Missing note: " + label)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, default=VAULT, required=not VAULT)
    parser.add_argument("--cache-dir", type=Path, default=CACHE)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("index", help="refresh and count all supported note-link occurrences")
    query = sub.add_parser("query", help="read source and traverse one hop")
    query.add_argument("note")
    query.add_argument("--direction", choices=["in", "out"], default="out")
    query.add_argument("--peer", help="restrict to one resolved neighbor")
    query.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()
    root, cache = args.vault.resolve(strict=True), args.cache_dir.resolve()
    if not root.is_dir() or cache.is_relative_to(root):
        raise ValueError("Choose a vault directory and a cache outside that vault.")
    if args.command == "query" and args.limit < 1:
        raise ValueError("--limit must be positive")
    notes, changed, removed, path = refresh(root, cache)
    resolver = Resolver(notes)
    counts = dict(resolved=0, missing=0, ambiguous=0)
    pairs = set()
    indexed = args.command == "index"
    focus = None if indexed else require(resolver, args.note)
    peer = None if indexed or not args.peer else require(resolver, args.peer)

    @lru_cache(maxsize=64)
    def lines(note):
        data = (root / note).read_bytes()
        if hashlib.sha256(data).hexdigest() != notes[note]["hash"]:
            raise ValueError(f"Source changed during query: {note}. Run again.")
        return data.decode("utf-8-sig").splitlines()

    def describe(note):
        source = lines(note)
        start = next((i for i, line in enumerate(source) if line.startswith("# ")), 0)
        print(f"{root / note}:{start + 1}  {source[start] if source else '(empty note)'}")

    if focus:
        describe(focus)
    seen = 0
    for src, note in notes.items():
        if not indexed and args.direction == "out" and src != focus:
            continue
        parent = posixpath.dirname(src)
        for n, label in note["links"]:
            matches = resolver.resolve(label, parent if "/" in label else "")
            status = "ambiguous" if len(matches) > 1 else "resolved" if matches else "missing"
            if indexed:
                counts[status] += 1
                if len(matches) == 1:
                    pairs.add((src, matches[0]))
                continue
            dest = matches[0] if len(matches) == 1 else None
            other = dest if args.direction == "out" else src
            if (args.direction == "in" and dest != focus) or (peer and other != peer):
                continue
            seen += 1
            if seen <= args.limit:
                evidence = lines(src)[n - 1].strip()
                print(f"  {root / src}:{n}  {evidence}")
                if dest:
                    print(f"    -> {root / dest}")
                else:
                    print(f"    {status}: {label}" + (" | " + " | ".join(matches) if matches else ""))
    if indexed:
        print(f"{len(notes)} notes, {changed} parsed, {removed} removed, {counts}")
        print(f"{len(pairs)} distinct directed note pairs")
        print(f"Invalid alias frontmatter: {sum(n['bad_alias_yaml'] for n in notes.values())}\nCache: {path}")
    else:
        if peer and seen:
            describe(peer)
        print(f"{seen} {args.direction} link occurrence(s), {min(seen, args.limit)} shown")
        if peer and not seen:
            return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        sys.exit(str(exc))
