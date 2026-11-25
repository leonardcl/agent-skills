"""Install or remove a named set of local skills using the existing profile helper."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
GROUPS = json.loads((ROOT / "integrations" / "groups.json").read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["list", "install", "status", "uninstall"])
    parser.add_argument("group", choices=sorted(GROUPS))
    parser.add_argument("--profile", type=Path)
    args = parser.parse_args()
    names = GROUPS[args.group]
    if args.action == "list":
        print("\n".join(names))
        return
    if args.profile is None:
        parser.error("select a discovery directory with --profile")
    profile = args.profile.expanduser().resolve()
    # Check all destinations before installing; profile.py also checks at link creation.
    if args.action == "install":
        for name in names:
            source = ROOT / "skills" / name
            entry = profile / name
            if not (source / "SKILL.md").is_file():
                parser.exit(1, f"Missing skill in checkout: {name}\n")
            if (entry.exists() or entry.is_symlink()) and not (entry.is_symlink() and entry.resolve() == source):
                parser.exit(1, f"Existing entry preserved: {entry}. Use profile.py for other individual skills.\n")
    for name in names:
        result = subprocess.run([sys.executable, ROOT / "tools/profile.py", args.action, "--profile", profile, name])
        if result.returncode:
            parser.exit(result.returncode)


if __name__ == "__main__":
    main()
