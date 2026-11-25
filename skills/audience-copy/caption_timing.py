"""Check the reading time of caption cards. Derived from Instagram Agent Skill. See LICENSE."""
import argparse
import json
import math
import re
import sys

from pathlib import Path


def die(message):
    raise SystemExit(message)


def read_text(path):
    try:
        return sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as error:
        die(str(error))


def words(text):
    return re.findall(r"[\w]+(?:['’-][\w]+)*", text)


TIME = r"(\d+(?:\.\d+)?f|\d+:\d{1,2}(?:\.\d+)?|\d+(?:\.\d+)?)"
LINE_RE = re.compile(r"^\s*" + TIME + r"\s*[-–]\s*" + TIME + r"\s+(.+?)\s*$")


def seconds(token, fps):
    if token.endswith("f"):
        return float(token[:-1]) / fps
    if ":" in token:
        m, s = token.split(":")
        return int(m) * 60 + float(s)
    return float(token)


def parse(raw, fps):
    cards, bad = [], []
    for n, line in enumerate(raw.lstrip("\ufeff").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = LINE_RE.match(line)
        if not m:
            bad.append(n)
            continue
        start, end = seconds(m.group(1), fps), seconds(m.group(2), fps)
        cards.append({"start": start, "end": end, "text": m.group(3)})
    cards.sort(key=lambda c: c["start"])     # the hook is the earliest card, not the first line
    # Lines that leave together are one card: two lines shown at once, or a second line
    # that appears while the first line remains on screen.
    merged = []                              # "together": within a quarter of a second
    for c in cards:
        if merged and abs(c["end"] - merged[-1]["end"]) <= 0.25 and c["start"] < merged[-1]["end"]:
            merged[-1]["text"] += " / " + c["text"]
            merged[-1]["end"] = max(merged[-1]["end"], c["end"])
        else:
            merged.append(c)
    return merged, bad


def analyse(cards, cps=15.0, min_hold=1.0, hook_by=1.0, max_words=12, cta_hold=4.0, target=None):
    rows, notes = [], []
    for i, c in enumerate(cards):
        shown = c["end"] - c["start"]
        need = max(min_hold, len(c["text"].replace(" / ", " ")) / cps)
        n_words = len(words(c["text"]))
        flags = []
        if shown <= 0:
            flags.append("ends before it starts")
        elif shown + 1e-6 < need:
            flags.append(f"up {shown:.1f}s, needs {need:.1f}s to read")
        if n_words > max_words:
            flags.append(f"{n_words} words, over {max_words}: split it")
        if i == 0:
            if c["start"] > hook_by:
                flags.append(f"hook appears at {c['start']:.1f}s, after {hook_by:.1f}s")
            if n_words > 6:
                flags.append(f"hook card has {n_words} words; 6 or fewer reads in one glance")
        if i + 1 < len(cards) and cards[i + 1]["start"] < c["end"] - 1e-6:
            flags.append(f"still up when the next card arrives at {cards[i + 1]['start']:.1f}s")
        if i == len(cards) - 1 and shown + 1e-6 < cta_hold:
            flags.append(f"last card holds {shown:.1f}s; the ask needs {cta_hold:.0f}s")
        rows.append({**c, "shown": round(shown, 2), "need": round(need, 2),
                     "words": n_words, "flags": flags})
    if target and cards:
        end = max(c["end"] for c in cards)
        if abs(end - target) > 2:
            notes.append(f"words end at {end:.1f}s against a {target:.0f}s target")
    return {"cards": rows, "notes": notes,
            "verdict": "FIX" if any(r["flags"] for r in rows) or notes else "READY"}


def tc(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def render(a, out=sys.stdout):
    print("\nON-SCREEN CARDS\n" + "=" * 78, file=out)
    for r in a["cards"]:
        mark = "  " if not r["flags"] else "!!"
        text = r["text"] if len(r["text"]) <= 46 else r["text"][:43] + "..."
        print(f"{mark} {tc(r['start'])}-{tc(r['end'])}  {r['shown']:4.1f}s (need {r['need']:.1f})  "
              f"{text}", file=out)
        for f in r["flags"]:
            print(f"      ^ {f}", file=out)
    for n in a["notes"]:
        print(f"   - {n}", file=out)
    print("-" * 78 + f"\n  VERDICT  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Check on-screen text cards against reading time.")
    ap.add_argument("input", nargs="?", default="-")
    ap.add_argument("--fps", type=lambda v: float(v) if float(v) > 0 else ap.error("--fps must be over 0"),
                    default=30.0)
    ap.add_argument("--cps", type=float, default=15.0, help="characters a viewer reads per second")
    ap.add_argument("--min-hold", type=float, default=1.0)
    ap.add_argument("--hook-by", type=float, default=1.0)
    ap.add_argument("--max-words", type=int, default=12)
    ap.add_argument("--cta-hold", type=float, default=4.0)
    ap.add_argument("--target", type=float, help="intended length in seconds")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not all(math.isfinite(value) and value > 0 for value in (args.fps, args.cps)):
        ap.error("frame rate and characters per second must be positive finite numbers")
    if any(not math.isfinite(value) or value < 0 for value in (args.min_hold, args.hook_by, args.cta_hold)):
        ap.error("caption timing thresholds must be finite and nonnegative")
    raw = read_text(args.input)
    cards, bad = parse(raw, args.fps)
    if bad:
        ap.error(f"invalid line(s) {', '.join(map(str, bad))}: expected START-END text")
    if not cards:
        die("no cards found")
    a = analyse(cards, args.cps, args.min_hold, args.hook_by, args.max_words, args.cta_hold,
                args.target)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "READY" else 1)


if __name__ == "__main__":
    main()
