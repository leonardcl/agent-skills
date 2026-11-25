"""Validate the release layout, local links and executable examples in scratch."""
import argparse
import ast
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(*args, expected=0, cwd=ROOT):
    proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    require(proc.returncode == expected, f"{args}: exit {proc.returncode}\n{proc.stdout}\n{proc.stderr}")
    return proc.stdout + proc.stderr


def structure():
    catalog = (ROOT / "CATALOG.md").read_text()
    names = []
    for skill in sorted(SKILLS.iterdir()):
        name = skill.name
        names.append(name)
        body = (skill / "SKILL.md").read_text()
        require(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name), f"Invalid name {name}")
        require(body.startswith(f"---\nname: {name}\n") and "\ndescription: " in body.split("---", 2)[1], name)
        require("**Limit.**" in body and "**Expected result.**" in body, f"Missing example criteria in {name}")
        for filename in ("LICENSE", "ORIGIN.md"):
            require((skill / filename).stat().st_size > 0, f"{name}/{filename}")
        require(f"(skills/{name}/SKILL.md)" in catalog, f"Missing catalog entry for {name}")
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        require(not path.is_symlink(), f"Unexpected symlink {path}")
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8")
        if path.suffix == ".py":
            ast.parse(body, str(path))
        if path.suffix == ".md":
            for dest in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", body):
                url = urlparse(dest)
                if url.scheme or not url.path:
                    continue
                target = (path.parent / unquote(url.path)).resolve()
                require(target.is_relative_to(ROOT) and target.is_file(), f"Broken local link {path}: {dest}")
    print(f"{len(names)} skills, notices, catalog entries and local links checked")
    return names


def examples(names):
    python = sys.executable
    with TemporaryDirectory() as temp:
        scratch = Path(temp)
        for profile in (scratch / "shared", scratch / "claude"):
            for name in names:
                run(python, ROOT / "tools/profile.py", "install", "--profile", profile, name)
                require((profile / name / "SKILL.md").samefile(SKILLS / name / "SKILL.md"), name)
            run(python, ROOT / "tools/profile.py", "install", "--profile", profile, names[0])
            for name in names:
                run(python, ROOT / "tools/profile.py", "uninstall", "--profile", profile, name)
            require(not list(profile.iterdir()), f"Residual entries in {profile}")
        profile = scratch / "shared"
        (profile / names[0]).mkdir()
        for action in ("install","uninstall"):
            run(python, ROOT / "tools/profile.py", action, "--profile", profile, names[0], expected=1)
        require((profile / names[0]).is_dir(), "Conflicting entry was lost")
        run(python, SKILLS / "notebook-links/test_vault_graph.py")
        slides = run(python, SKILLS / "slide-file-review/check_deck.py", "--self-test")
        require("5 findings" in slides, slides)
        ratio = run(python, SKILLS / "interface-accessibility/contrast-check.py", "--selftest")
        require("9 reference pairs" in ratio, ratio)
        room = SKILLS / "room-layout"
        run(python, room / "plan.py", room / "study.json", scratch / "study.svg")
        plan = json.loads((room / "study.json").read_text())
        plan["items"][0]["rect"][0] = 0
        (scratch / "conflict.json").write_text(json.dumps(plan))
        require("overlaps" in run(python, room / "plan.py", scratch / "conflict.json", scratch / "overlap.svg", expected=1), "Missing door conflict")
        run(python, room / "floor_plan.py", room / "two-rooms.json", scratch / "drawing")
        level = json.loads((scratch / "drawing/scene.json").read_text())["levels"][0]
        require(len(level["rooms"]) == 2 and len(level["walls"]) == 7, "Unexpected room geometry")
        require((scratch / "drawing/level-1.svg").is_file(), "Missing scaled drawing")
        cards = SKILLS / "audience-copy"
        require("READY" in run(python, cards / "caption_timing.py", cards / "cards.txt"), "Caption sample")
        log = scratch / "decisions.tsv"
        for phase in ("first", "repeat"):
            run("bash", SKILLS / "bounded-iteration/log.sh", log, phase, "keep order", "same input", "diff", "empty")
        require(len(log.read_text().splitlines()) == 3, "Expected header and two decisions")
    print("Both scratch profiles, collision preservation and six executable skill examples passed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples", action="store_true", help="also run helper and discovery examples (requires PyYAML and Bash)")
    args = parser.parse_args()
    try:
        names = structure()
        if args.examples:
            examples(names)
    except (ValueError, OSError) as error:
        sys.exit(str(error))
