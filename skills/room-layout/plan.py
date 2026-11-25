"""Render one measured rectangular room and check proposed occupied areas."""
import argparse
import json
import math
from pathlib import Path
from xml.etree import ElementTree as ET


def dimensions(values, count):
    if len(values) != count or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError(f"expected {count} finite coordinates")
    return values


def render(data):
    width, depth = dimensions(data["room"], 2)
    if min(width, depth) <= 0:
        raise ValueError("room dimensions must be positive")
    boxes, findings = [], []
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", viewBox=f"0 0 {width} {depth}")
    ET.SubElement(svg, "title").text = data.get("title", "Room plan in metres")
    ET.SubElement(svg, "rect", width=str(width), height=str(depth), fill="white", stroke="black", attrib={"stroke-width": "0.04"})
    for item in data["items"]:
        x, y, w, d = dimensions(item["rect"], 4)
        name = item["name"]
        if min(w, d) <= 0 or not isinstance(name, str) or not name.strip():
            raise ValueError("each item needs a name and positive dimensions")
        if min(x, y) < 0 or x + w > width or y + d > depth:
            findings.append(f"{name} extends outside the room")
        for other, a, b, c, e in boxes:
            if max(a, x) < min(a+c, x+w) and max(b, y) < min(b+e, y+d):
                findings.append(f"{name} overlaps {other}")
        boxes.append((name, x, y, w, d))
        ET.SubElement(svg, "rect", x=str(x), y=str(y), width=str(w), height=str(d), fill="#ddebf1", stroke="#29475b", attrib={"stroke-width": "0.02"})
        ET.SubElement(svg, "text", x=str(x+0.04), y=str(y+min(d/2,0.17)), attrib={"font-size":"0.12"}).text = name
    return ET.tostring(svg, encoding="unicode"), findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("svg", type=Path)
    args = parser.parse_args()
    if args.svg.suffix.lower() != ".svg" or args.svg.resolve() == args.plan.resolve():
        parser.error("choose a separate .svg output")
    try:
        svg, findings = render(json.loads(args.plan.read_text(encoding="utf-8")))
        with args.svg.open("x", encoding="utf-8") as output:
            output.write(svg)
    except (KeyError, TypeError, ValueError, OSError) as error:
        parser.exit(2, f"{error}\n")
    for message in findings:
        print(message)
    print(f"{len(findings)} overlap or boundary findings")
    return int(bool(findings))


if __name__ == "__main__":
    raise SystemExit(main())
