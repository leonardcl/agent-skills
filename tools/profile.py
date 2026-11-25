"""Link one selected skill into a discovery directory on macOS or Linux."""
import argparse
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "uninstall", "status"))
    parser.add_argument("--profile", type=Path, required=True, help="skill discovery directory")
    parser.add_argument("skill", help="one directory name from the catalog")
    args = parser.parse_args()
    skills = Path(__file__).resolve().parents[1] / "skills"
    if args.skill in (".", "..") or Path(args.skill).name != args.skill:
        parser.error("choose one skill name from the catalog")
    source = skills / args.skill
    profile = args.profile.expanduser().resolve()
    if profile == skills or skills in profile.parents:
        parser.error("choose a profile outside the collection")
    entry = profile / args.skill
    if args.action == "install":
        if source.is_symlink() or not (source / "SKILL.md").is_file():
            parser.error("skill missing from this checkout")
        profile.mkdir(parents=True, exist_ok=True)
        try:
            entry.symlink_to(source, target_is_directory=True)
        except FileExistsError:
            if not entry.is_symlink() or entry.resolve() != source:
                parser.exit(1, f"Existing entry preserved: {entry}\n")
        print(f"Linked {entry} to {source}")
    elif entry.is_symlink() and entry.resolve() == source:
        if args.action == "uninstall":
            entry.unlink()
            print(f"Removed link {entry}")
        else:
            print(f"Linked to {source}")
    elif entry.exists() or entry.is_symlink():
        parser.exit(1, f"Existing entry belongs to another installation: {entry}\n")
    else:
        print(f"No link at {entry}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError) as exc:
        sys.exit(str(exc))
