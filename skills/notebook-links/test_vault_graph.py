from concurrent.futures import ThreadPoolExecutor
import os
import sys
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

READER = Path(__file__).with_name("vault_graph.py")


class VaultGraphTest(unittest.TestCase):
    def setUp(self):
        temp = TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "vault"
        self.root.mkdir()
        self.cache = self.root.parent / "cache"
        (self.root / "index.md").write_text(
            "# Index\nOriginal prose [[First Note#Details|one]].\n"
            "[[nickname]] [[Duplicate]] [[Missing]]\n"
            "`[[Example]]`\n```md\n[[Example]]\n```\n"
            "<!-- [[Example]] -->\n%% [[Example]] %%\n"
            "| [[First Note\\|display]] |\n"
        )
        with (self.root / "index.md").open("a") as f:
            f.write('[one](<one/Duplicate.md#Heading>) [external](https://example.org/first-note.md)\n')
        self.target = self.root / "first-note.md"
        self.target.write_text("---\naliases:\n  - Nickname\n---\n# First Note\n")
        for folder in ["one", "two"]:
            (self.root / folder).mkdir()
            (self.root / folder / "Duplicate.md").write_text("# Duplicate\n")
        (self.root / "outside.md").symlink_to(Path(__file__))

    def cli(self, *arguments, code=0):
        proc = subprocess.run(
            [sys.executable, str(READER), "--vault", self.root, "--cache-dir", self.cache, *arguments],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, code, proc.stdout + proc.stderr)
        return proc.stdout + proc.stderr

    def test_resolution_and_provenance(self):
        result = self.cli("query", "index")
        for part in ["index.md:2  Original prose", "first-note.md", "ambiguous: Duplicate",
                     "one/Duplicate.md", "two/Duplicate.md", "missing: Missing", "6 out link occurrence"]:
            self.assertIn(part, result)
        self.assertNotIn("Example", result)
        self.assertIn("3 in link occurrence", self.cli("query", "nickname", "--direction", "in", "--peer", "index"))
        self.assertIn("0 out link occurrence", self.cli("query", "first note", "--peer", "index", code=1))
        self.assertIn("Ambiguous", self.cli("query", "Duplicate", code=1))
        self.assertIn("Missing note", self.cli("query", "outside", code=1))
        self.assertIn("1 in link occurrence", self.cli("query", "one/Duplicate.md", "--direction", "in"))

    def test_malformed_cache_with_empty_notebook(self):
        import json
        for note in self.root.rglob("*.md"):
            note.unlink()
        self.cli("index")
        artifact, = self.cache.glob("*.json")
        for damaged in ("{", '{"format": 3, "notes": null}'):
            artifact.write_text(damaged)
            self.assertIn("0 notes", self.cli("index"))
            self.assertEqual(json.loads(artifact.read_text())["notes"], {})

    def test_update_and_deletion(self):
        self.assertIn("4 parsed", self.cli("index"))
        artifact, = self.cache.glob("*.json")
        timestamp = artifact.stat().st_mtime_ns
        self.assertIn("0 parsed", self.cli("index"))
        self.assertEqual(timestamp, artifact.stat().st_mtime_ns)
        self.assertNotIn(b"Original prose", artifact.read_bytes())
        self.assertEqual(artifact.stat().st_mode & 0o777, 0o600)
        focus = self.root / "index.md"
        metadata = focus.stat()
        focus.write_text(focus.read_text().replace("Original", "Updated!").replace("nickname", "lostname"))
        os.utime(focus, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
        result = self.cli("query", "index")
        self.assertIn("index.md:2  Updated! prose", result)
        self.assertIn("missing: lostname", result)
        self.target.unlink()
        self.assertIn("1 removed", self.cli("index"))
        self.assertIn("Missing note", self.cli("query", "Nickname", code=1))
        self.assertIn("missing: First Note", self.cli("query", "index"))

    def test_concurrent_rebuild_and_cache_recovery(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.cli("index"), range(2)))
        self.assertEqual(sum("4 parsed" in r for r in results), 1)
        self.assertEqual(sum("0 parsed" in r for r in results), 1)
        artifact, = self.cache.glob("*.json")
        artifact.write_text("{interrupted")
        self.assertIn("4 parsed", self.cli("index"))
        self.assertFalse(list(self.cache.glob("*.html")))


if __name__ == "__main__":
    unittest.main()
