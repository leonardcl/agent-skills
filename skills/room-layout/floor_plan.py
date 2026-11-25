"""Build measured floor-plan SVGs and a structured scene without network access."""
import argparse
from collections import defaultdict, deque
import datetime
import html
import json
import math
import pathlib
import re
import sys

CELL = 0.05


ITEMS = {
 "bed_single": (1.0, 2.05, .5, {"sides": ("one", .45, .75)}, ""), "bed_double": (1.6, 2.1, .5, {"sides": ("both", .45, .75), "front": (.45, .75)}, ""),
 "bed_king": (1.8, 2.1, .5, {"sides": ("both", .45, .75), "front": (.45, .75)}, ""), "bunk": (1.0, 2.05, 1.7, {"sides": ("one", .45, .75)}, ""),
 "crib": (.7, 1.3, .9, {"front": (.45, .75)}, ""), "nightstand": (.45, .4, .5, {}, "soft"), "wardrobe": (1.8, .6, 2.2, {"front": (.6, .75)}, ""),
 "dresser": (1.0, .45, .8, {"front": (.6, .75)}, ""), "desk": (1.2, .6, .75, {"front": (.6, .9)}, ""), "bookshelf": (.9, .3, 1.9, {"front": (.45, .75)}, ""),
 "cabinet": (1.2, .4, .85, {"front": (.45, .75)}, ""), "tall_cabinet": (.6, .6, 2.2, {"front": (.6, .75)}, ""), "shoe_cabinet": (1.0, .35, 1.0, {"front": (.45, .75)}, ""),
 "bench": (1.1, .4, .45, {}, "soft"), "sofa2": (1.6, .88, .78, {"front": (.3, .4)}, ""), "sofa3": (2.1, .9, .78, {"front": (.3, .4)}, ""),
 "sofa_l": (2.6, 1.6, .78, {"front": (.3, .4)}, ""), "armchair": (.8, .82, .8, {"front": (.3, .4)}, "soft"), "coffee_table": (1.1, .6, .38, {}, "soft"),
 "side_table": (.45, .45, .5, {}, "soft"), "tv": (1.8, .4, .5, {}, ""), "rug": (2.4, 1.7, .012, {}, "flat"),
 "dining2": (.8, .7, .75, {"seats": (.6, .81)}, ""), "dining4": (1.3, .8, .75, {"seats": (.6, .81)}, ""), "dining6": (1.8, .9, .75, {"seats": (.6, .81)}, ""),
 "dining8": (2.3, 1.0, .75, {"seats": (.6, .81)}, ""), "dining_round": (1.1, 1.1, .75, {"seats": (.6, .81)}, ""), "stool": (.38, .38, .65, {}, "soft"),
 "counter": (2.0, .6, .9, {"front": (.9, 1.07)}, ""), "island": (1.8, .9, .9, {"front": (.9, 1.07)}, ""), "sink": (.8, .6, .9, {}, "on"), "hob": (.6, .6, .9, {}, "on"),
 "fridge": (.7, .7, 1.8, {"front": (.75, 1.07)}, ""), "oven_tall": (.6, .6, 2.2, {"front": (.75, 1.07)}, ""), "wall_cabinet": (1.6, .35, .7, {}, "up"), "hood": (.6, .5, .3, {}, "up"),
 "toilet": (.38, .68, .78, {"front": (.53, .76), "sides": ("both", .19, .26)}, ""), "squat": (.45, .6, .25, {"front": (.45, .6)}, ""), "basin": (.5, .42, .85, {"front": (.53, .76)}, ""),
 "vanity": (.9, .48, .85, {"front": (.53, .76)}, ""), "vanity2": (1.4, .5, .85, {"front": (.53, .76)}, ""), "shower": (.9, .9, 2.0, {"front": (.53, .76)}, "soft"),
 "bathtub": (1.6, .72, .55, {"front": (.53, .76)}, ""), "washer": (.6, .6, .85, {"front": (.6, .9)}, "under"), "dishwasher": (.6, .6, .85, {"front": (.6, .9)}, "under"), "oven": (.6, .58, .6, {"front": (.6, .9)}, "under"), "screen": (2.0, .05, 2.2, {}, ""), "laundry": (1.3, .62, .85, {"front": (.6, .9)}, ""),
 "piano": (1.5, .6, 1.2, {"front": (.6, .9)}, ""), "plant": (.4, .4, .9, {}, "soft"), "plant_tall": (.55, .55, 1.7, {}, "soft"), "floor_lamp": (.38, .38, 1.55, {}, "soft"),
 "pendant": (.4, .4, .3, {}, "up"), "ceiling_light": (.5, .5, .08, {}, "up"), "art": (.8, .04, .6, {}, "up"), "mirror": (.6, .04, .9, {}, "up"), "shelf_wall": (1.0, .24, .04, {}, "up"),
 "ac": (.85, .22, .3, {}, "up"), "curtain": (1.8, .1, 2.4, {}, "up"), "box": (1.0, 1.0, 1.0, {}, ""), "prayer_mat": (.7, 1.2, .012, {}, "flat"), "stairs": (.9, 3.0, 2.8, {}, ""),
 "car": (1.8, 4.5, 1.5, {}, "out"), "motorbike": (.75, 1.95, 1.1, {}, "out"), "bicycle": (.55, 1.75, 1.05, {}, "out"), "tree": (2.6, 2.6, 4.5, {}, "out"), "palm": (2.0, 2.0, 4.0, {}, "out"),
 "shrub": (.8, .8, .7, {}, "out"), "hedge": (2.0, .5, 1.1, {}, "out"), "fence": (2.0, .1, 1.5, {}, "out"), "gate": (3.0, .08, 1.5, {}, "out flat"), "outdoor_table": (1.2, .8, .74, {}, "out"),
 "lounger": (.7, 1.9, .4, {}, "out"), "pond": (2.0, 1.2, .05, {}, "out flat"), "stepping": (.6, .4, .04, {}, "out flat"), "water_tank": (1.0, 1.0, 1.3, {}, "out"), "ac_outdoor": (.8, .3, .6, {}, "out"),
 "washing_line": (1.8, .5, 1.6, {}, "out"), "post": (.2, .2, 2.8, {}, "out"),
}


Z_UP = {"wall_cabinet": 1.45, "hood": 1.55, "pendant": None, "ceiling_light": None, "art": 1.25, "mirror": 1.1, "shelf_wall": 1.4, "ac": None, "curtain": 0.0}


OUTDOOR = {"garden", "terrace", "carport", "balcony", "yard", "paving", "service_yard", "driveway"}


FACE = {"down": 0, "left": 90, "up": 180, "right": 270}


COLOUR = {"facade": "#e8e2d6", "plinth": "#77716a", "frame": "#2f2d2b", "roof": "#70513f", "wall": "#f1ece3", "ceiling": "#f7f5f1", "wood": "#a67c52", "fabric": "#76806f",
          "metal": "#3b3a38", "counter": "#d6d0c5", "cabinet": "#e4ddd0", "accent": "#a8502f", "door": "#8a6644", "linen": "#efe9de"}


class Bad(Exception):
    """The file cannot be understood at all."""


def r3(p): return (round(p[0], 3), round(p[1], 3))


def edges(poly): return [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]


def signed(poly): return sum(a[0] * b[1] - b[0] * a[1] for a, b in edges(poly)) / 2


def area(poly): return abs(signed(poly))


def bbox(poly): xs, ys = [p[0] for p in poly], [p[1] for p in poly]; return min(xs), min(ys), max(xs), max(ys)


def rect_poly(r): x, y, w, d = r; return [(x, y), (x + w, y), (x + w, y + d), (x, y + d)]


def inside(p, poly):
    x, y = p; c = False
    for (x1, y1), (x2, y2) in edges(poly):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c


def seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def inset(poly, dist):
    """Move edge i inwards by dist[i]; poly has positive signed area, so inwards is (-uy, ux)."""
    lines = []
    for (a, b), d in zip(edges(poly), dist):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        lines.append(((a[0] - uy * d, a[1] + ux * d), (ux, uy)))
    out = []
    for i in range(len(lines)):
        (p, u), (q, v) = lines[i - 1], lines[i]; den = u[0] * v[1] - u[1] * v[0]
        if abs(den) < 1e-9: out.append(q); continue
        t = ((q[0] - p[0]) * v[1] - (q[1] - p[1]) * v[0]) / den
        out.append((p[0] + u[0] * t, p[1] + u[1] * t))
    return out


def rot(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return (v[0] * c - v[1] * s, v[0] * s + v[1] * c)


def local_rect(it, x0, y0, x1, y1):
    """Rectangle given in the item's own frame, as plan points."""
    return [tuple(a + b for a, b in zip(it["at"], rot(p, it["rot"]))) for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]


def footprint(it):
    if it["type"] in ("tree", "palm"): return local_rect(it, -.2, -.2, .2, .2)  # you walk under the crown
    return local_rect(it, -it["w"] / 2, -it["d"] / 2, it["w"] / 2, it["d"] / 2)


def load(path):
    try: home = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    except ValueError as e: raise Bad("not valid JSON: %s" % e)
    return prepare(home)


def prepare(home):
    home["style"] = {**COLOUR, **home.get("style", {})}
    w = home.setdefault("walls", {}); w.setdefault("ext", .15); w.setdefault("int", .12)
    site = home.setdefault("site", {})
    site["north"] = float(site.get("north", 0))
    if "lot" in site: site["lot_poly"] = rect_poly(site["lot"]) if isinstance(site["lot"][0], (int, float)) else [tuple(p) for p in site["lot"]]
    if not home.get("levels"): raise Bad("no levels")
    seen = set()
    for n, lv in enumerate(home["levels"]):
        lv.setdefault("name", "Level %d" % (n + 1)); lv.setdefault("height", 2.8); lv.setdefault("slab", .2); lv.setdefault("id", "L%d" % (n + 1))
        if "z" not in lv: lv["z"] = 0.0 if n == 0 else home["levels"][n - 1]["z"] + home["levels"][n - 1]["height"] + lv["slab"]
        for k in ("rooms", "doors", "windows", "items", "open"): lv.setdefault(k, [])
        for r in lv["rooms"]:
            if "id" not in r: raise Bad("a room on %s has no id" % lv["name"])
            if r["id"] in seen: raise Bad("room id %r is used twice" % r["id"])
            seen.add(r["id"]); r.setdefault("name", r["id"]); r.setdefault("use", "other")
            if "rect" in r: r["poly"] = rect_poly(r["rect"])
            if len(r.get("poly", [])) < 3: raise Bad("room %s needs rect or poly" % r["id"])
            r["poly"] = [r3(p) for p in r["poly"]]
            if signed(r["poly"]) < 0: r["poly"].reverse()
            r["out"] = r["use"] in OUTDOOR; r["void"] = r["use"] == "void"
        build_walls(home, lv)
        for kind in ("doors", "windows"):
            for o in lv[kind]: place_opening(lv, o, kind)
        for it in lv["items"]: place_item(lv, it)
    for kind, letter in (("doors", "D"), ("windows", "W")):
        for i, o in enumerate((o for lv in home["levels"] for o in lv[kind]), 1): o["mark"] = "%s%d" % (letter, i)
    return home


def build_walls(home, lv):
    rooms = [r for r in lv["rooms"] if not r["out"]]; pts = {p for r in rooms for p in r["poly"]}; by = {r["id"]: r for r in lv["rooms"]}
    raw = defaultdict(list)
    for r in rooms:
        for a, b in edges(r["poly"]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if L < .01: raise Bad("room %s has two corners at the same point" % r["id"])
            on = sorted((((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / L, p) for p in pts if seg_dist(p, a, b) < .004)
            cut = [p for _, p in on]
            for p, q in zip(cut, cut[1:]):
                if p != q: raw[tuple(sorted((p, q)))].append(r["id"])
    opened = {frozenset(x) for x in lv["open"]}; lv["walls"] = []
    for (a, b), ids in sorted(raw.items()):
        kind = "ext" if len(ids) == 1 else "int"
        if kind == "int":
            voids = [by[i]["void"] for i in ids]
            if frozenset(ids) in opened or all(voids): kind = "none"
            elif any(voids) and not any(by[i].get("walls") for i in ids if by[i]["void"]): kind = "rail"
        L = math.hypot(b[0] - a[0], b[1] - a[1]); u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L); n = (-u[1], u[0])
        m = ((a[0] + b[0]) / 2 + n[0] * .03, (a[1] + b[1]) / 2 + n[1] * .03)
        pos = next((i for i in ids if inside(m, by[i]["poly"])), None); neg = next((i for i in ids if i != pos), None)
        th = {"ext": home["walls"]["ext"], "int": home["walls"]["int"], "rail": .05, "none": 0}[kind]
        lv["walls"].append({"a": a, "b": b, "len": L, "u": u, "n": n, "kind": kind, "th": th, "rooms": ids, "pos": pos, "neg": neg, "holes": []})
    for r in lv["rooms"]:
        if r["out"]: r["clear"] = r["poly"]; continue
        d = []
        for a, b in edges(r["poly"]):
            d.append(max([0] + [s["th"] / 2 for s in lv["walls"] if r["id"] in s["rooms"] and s["kind"] in ("ext", "int") and seg_dist(s["a"], a, b) < .01 and seg_dist(s["b"], a, b) < .01]))
        r["clear"] = inset(r["poly"], d)


def place_opening(lv, o, kind):
    if "at" not in o: raise Bad("a %s on %s has no at" % (kind[:-1], lv["name"]))
    o["kind"] = kind[:-1]; door = kind == "doors"
    o.setdefault("type", "swing" if door else "casement"); o.setdefault("w", .8 if door else 1.2)
    o.setdefault("h", 2.1 if door else 1.3); o.setdefault("sill", 0 if door else .9)
    best = min(((seg_dist(o["at"], s["a"], s["b"]), i) for i, s in enumerate(lv["walls"]) if s["kind"] in ("ext", "int", "rail")), default=(9, -1))
    if best[0] > .16:
        o["wall"] = None; return
    s = lv["walls"][best[1]]; o["wall"] = best[1]
    t = (o["at"][0] - s["a"][0]) * s["u"][0] + (o["at"][1] - s["a"][1]) * s["u"][1]; o["t"] = t
    o["c"] = (s["a"][0] + s["u"][0] * t, s["a"][1] + s["u"][1] * t)
    o["fits"] = t - o["w"] / 2 >= -.001 and t + o["w"] / 2 <= s["len"] + .001
    s["holes"].append(o)
    out = None
    if s["kind"] == "ext":
        side = 1 if s["pos"] is None else -1; p = (o["c"][0] + s["n"][0] * side * .3, o["c"][1] + s["n"][1] * side * .3)
        out = next((r["id"] for r in lv["rooms"] if r["out"] and inside(p, r["poly"])), "outside")
    o["rooms"] = [x for x in (s["pos"], s["neg"]) if x] + ([out] if out else [])
    if door and o["type"] in ("swing", "double"):
        into = o.get("into") or next((x for x in o["rooms"] if x not in ("outside",)), None); o["into"] = into
        o["side"] = 1 if into == s["pos"] or (into != s["neg"] and s["pos"] is None) else -1
        key = 0 if abs(s["u"][0]) > abs(s["u"][1]) else 1; low = s["u"][key] > 0
        want = o.get("hinge") or ("left" if key == 0 else "top"); o["hinge"] = want
        first = want in ("left", "top"); o["hinge_sign"] = (-1 if first else 1) * (1 if low else -1)


def place_item(lv, it):
    if it.get("type") not in ITEMS: raise Bad("unknown item type %r (home.py items lists them; use box for anything else)" % it.get("type"))
    W, D, H, zones, tags = ITEMS[it["type"]]
    it.setdefault("w", W); it.setdefault("d", D); it.setdefault("h", H); it["tags"] = tags.split()
    if "room" in it and "wall" in it and "at" not in it:
        r = next((r for r in lv["rooms"] if r["id"] == it["room"]), None)
        if not r: raise Bad("item %s names room %r, which is not on %s" % (it["type"], it["room"], lv["name"]))
        x0, y0, x1, y1 = bbox(r["clear"]); wall = it["wall"]; gap = it.get("gap", 0); hor = wall in ("top", "bottom")
        if wall not in ("top", "bottom", "left", "right"): raise Bad("item %s: wall must be top, bottom, left or right" % it["type"])
        span = (x1 - x0) if hor else (y1 - y0); al = it.get("along", "center"); half = it["w"] / 2
        t = {"start": half, "center": span / 2, "end": span - half}.get(al) if isinstance(al, str) else (al if al >= 0 else span + al)
        if t is None: raise Bad("item %s: along must be start, center, end or a number" % it["type"])
        back = it["d"] / 2 + gap
        it["at"] = {"top": (x0 + t, y0 + back), "bottom": (x0 + t, y1 - back), "left": (x0 + back, y0 + t), "right": (x1 - back, y0 + t)}[wall]
        it["rot"] = {"top": 0, "bottom": 180, "left": 270, "right": 90}[wall]
    if "at" not in it: raise Bad("item %s on %s needs at, or room and wall" % (it["type"], lv["name"]))
    it["at"] = r3(it["at"])
    if "rot" not in it: it["rot"] = FACE.get(it.get("face", "down"), 0)
    if it["type"] == "stairs":
        steps = it.setdefault("steps", max(3, math.ceil((lv["height"] + .2) / .18))); it.setdefault("rise", lv["height"] + .2)
        it["riser"] = it["rise"] / steps; it["going"] = it["d"] / max(1, steps - 1); it["h"] = it["rise"]
    z = it.get("z")
    if z is None:
        z = Z_UP.get(it["type"], 0.0)
        if z is None: z = lv["height"] - it["h"] - ({"pendant": .9, "ac": .25}.get(it["type"], 0))
    it["z"] = z; it["floor"] = not ({"flat", "up", "on"} & set(it["tags"])) and z < 1.9 and it["h"] > .1
    it["zones"] = zones; it["host"] = next((r["id"] for r in lv["rooms"] if inside(it["at"], r["poly"])), None)


def sun(lat, lon, tz, day, hour):
    """Azimuth (clockwise from north) and height of the sun in degrees. day = day of year."""
    g = 2 * math.pi / 365 * (day - 1 + (hour - 12) / 24)
    eq = 229.18 * (.000075 + .001868 * math.cos(g) - .032077 * math.sin(g) - .014615 * math.cos(2 * g) - .040849 * math.sin(2 * g))
    dec = .006918 - .399912 * math.cos(g) + .070257 * math.sin(g) - .006758 * math.cos(2 * g) + .000907 * math.sin(2 * g) - .002697 * math.cos(3 * g) + .00148 * math.sin(3 * g)
    ha = math.radians((hour * 60 + eq + 4 * lon - 60 * tz) / 4 - 180); la = math.radians(lat)
    sh = math.sin(la) * math.sin(dec) + math.cos(la) * math.cos(dec) * math.cos(ha); el = math.asin(max(-1, min(1, sh)))
    az = math.atan2(-math.cos(dec) * math.sin(ha), math.sin(dec) * math.cos(la) - math.cos(dec) * math.sin(la) * math.cos(ha))
    return math.degrees(az) % 360, math.degrees(el)


def bearing(home, v):
    """Compass bearing of a plan direction; plan up points to site.north."""
    return (math.degrees(math.atan2(v[0], -v[1])) + home["site"]["north"]) % 360


def outward(s): return s["n"] if s["pos"] is None else (-s["n"][0], -s["n"][1])


def compass(b): return ("N", "NE", "E", "SE", "S", "SW", "W", "NW")[int((b + 22.5) // 45) % 8]


def roof_list(home):
    """The roofs with their outer rectangle (overhangs included) and eaves height."""
    top = home["levels"][-1]; res = []
    for r in home.get("roofs") or []:
        x, y, w, d = r["rect"]; o = r.get("overhang", .6); o = {k: o for k in ("top", "bottom", "left", "right")} if not isinstance(o, dict) else o
        res.append((r, (x - o.get("left", 0), y - o.get("top", 0), x + w + o.get("right", 0), y + d + o.get("bottom", 0)), r.get("z", top["z"] + top["height"])))
    return res


def sun_hours(home, lv, s, o):
    """Hours of direct sun on the middle of an opening between 08:00 and 16:00: (Mar, Jun, Dec). The home's own walls, roof edges
    and the given neighbours block it; trees and curtains do not."""
    st = home["site"]
    if "lat" not in st: return None
    tz = st.get("tz", round(st.get("lon", 0) / 15)); d = outward(s); z0 = lv["z"] + o["sill"] + o["h"] / 2; res = []
    solid = [(r["poly"], bbox(r["poly"]), l["z"] - l["slab"], l["z"] + l["height"]) for l in home["levels"] for r in l["rooms"] if not r["out"]] + [(rect_poly(n["rect"]), bbox(rect_poly(n["rect"])), 0, n["h"]) for n in st.get("neighbours", [])]
    top = max(q[3] for q in solid); roofs = roof_list(home); start = (o["c"][0] + d[0] * (s["th"] / 2 + .05), o["c"][1] + d[1] * (s["th"] / 2 + .05))
    for day in (80, 172, 355):
        h = 0
        for k in range(32):
            az, el = sun(st["lat"], st.get("lon", 0), tz, day, 8.125 + k / 4); b = math.radians(az - st["north"]); v = (math.sin(b), -math.cos(b))
            if el < 3 or (v[0] * d[0] + v[1] * d[1]) * math.cos(math.radians(el)) < .09: continue  # below the horizon, or sliding along the glass
            t, rise = .1, math.tan(math.radians(el)); free = True
            if o.get("shade") and o["h"] / 2 + .14 < rise * o["shade"] / max(.05, v[0] * d[0] + v[1] * d[1]): free = False
            while free and t < 30 and z0 + t * rise < top + .5:
                q = (start[0] + v[0] * t, start[1] + v[1] * t); z = z0 + t * rise
                if any(lo <= z <= hi and bb[0] <= q[0] <= bb[2] and bb[1] <= q[1] <= bb[3] and inside(q, poly) for poly, bb, lo, hi in solid): free = False
                if any(z - .2 * rise - .02 <= ez <= z and x0 <= q[0] <= x1 and y0 <= q[1] <= y1 for _, (x0, y0, x1, y1), ez in roofs): free = False
                t += .2
            h += .25 if free else 0
        res.append(h)
    return res


def groups(lv):
    ids = {r["id"] for r in lv["rooms"] if not r["out"] and not r["void"]}; left = set(ids); res = []
    while left:
        g, q = set(), [left.pop()]
        while q:
            c = q.pop(); g.add(c)
            for a, b in (p for p in lv["open"] if len(p) == 2):
                for x, y in ((a, b), (b, a)):
                    if x == c and y in left: left.discard(y); q.append(y)
        res.append(sorted(g))
    return sorted(res)


def swing_polys(lv, o):
    s = lv["walls"][o["wall"]]; hs = [(o["hinge_sign"], o["w"])] if o["type"] == "swing" else [(-1, o["w"] / 2), (1, o["w"] / 2)]; res = []
    for sign, w in hs:
        h = (o["c"][0] + s["u"][0] * sign * o["w"] / 2, o["c"][1] + s["u"][1] * sign * o["w"] / 2); base = (-s["u"][0] * sign, -s["u"][1] * sign); side = (s["n"][0] * o["side"], s["n"][1] * o["side"])
        res.append([h] + [(h[0] + (base[0] * math.cos(t) + side[0] * math.sin(t)) * w, h[1] + (base[1] * math.cos(t) + side[1] * math.sin(t)) * w) for t in [k * math.pi / 16 for k in range(9)]])
    return res


def esc(s): return html.escape(str(s), quote=True)


def wall_pieces(s, lv):
    """Solid parts of a wall along its length: (t0, t1, z0, z1) with the openings taken out."""
    H = lv["height"]; res = []; cur = 0.0
    for o in sorted(s["holes"], key=lambda o: o["t"]):
        a, b = max(0, o["t"] - o["w"] / 2), min(s["len"], o["t"] + o["w"] / 2)
        if a > cur + .001: res.append((cur, a, 0, H))
        if o["sill"] > .001: res.append((a, b, 0, o["sill"]))
        if o["sill"] + o["h"] < H - .001: res.append((a, b, o["sill"] + o["h"], H))
        cur = max(cur, b)
    if cur < s["len"] - .001: res.append((cur, s["len"], 0, H))
    return res


def symbol(it):
    """Plan symbol in the item's own frame (front is +y), metres."""
    w, d, t = it["w"], it["d"], it["type"]; R = lambda x, y, a, b, r=0: '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="%.3f"/>' % (x, y, a, b, r)
    E = lambda x, y, a, b: '<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f"/>' % (x, y, a, b); P = lambda *p: '<path d="%s" fill="none"/>' % " ".join(p)
    M = lambda x, y: "M%.3f %.3f" % (x, y); T = lambda x, y: "L%.3f %.3f" % (x, y); o = R(-w / 2, -d / 2, w, d, .02)
    if t.startswith("bed"):
        n = 1 if w < 1.3 else 2; pw = (w - .12 * (n + 1)) / n
        return o + "".join(R(-w / 2 + .12 + i * (pw + .12), -d / 2 + .12, pw, .36, .06) for i in range(n)) + P(M(-w / 2, -d / 2 + .62), T(w / 2, -d / 2 + .62))
    if t == "screen": return "".join(E(-w / 2 + (k + .5) * w / max(1, round(w / .1)), 0, .02, .02) for k in range(max(1, round(w / .1))))
    if t in ("dishwasher", "oven"): return '<g stroke-dasharray=".08 .06" fill="none">%s</g>' % R(-w / 2, -d / 2, w, d)
    if t == "bunk": return o + R(-w / 2 + .1, -d / 2 + .12, w - .2, .36, .06) + P(M(-w / 2, -d / 2), T(w / 2, d / 2))
    if t == "crib": return o + P(*[x for k in range(1, 6) for x in (M(-w / 2 + w * k / 6, -d / 2), T(-w / 2 + w * k / 6, d / 2))])
    if t in ("sofa2", "sofa3"):
        n = 2 if t == "sofa2" else 3; a = .18; sw = (w - 2 * a) / n
        return R(-w / 2, -d / 2, w, d, .08) + R(-w / 2, -d / 2, w, .22, .06) + "".join(R(-w / 2 + a + i * sw, -d / 2 + .22, sw, d - .22, .05) for i in range(n))
    if t == "sofa_l": return '<path d="M%.3f %.3fH%.3fV%.3fH%.3fV%.3fH%.3fZ"/>' % (-w / 2, -d / 2, w / 2, d / 2, w / 2 - .9, d / 2 - .7, -w / 2) + R(-w / 2, -d / 2, w, .22, .06)
    if t == "armchair": return R(-w / 2, -d / 2, w, d, .1) + R(-w / 2 + .14, -d / 2 + .2, w - .28, d - .2, .06)
    if t.startswith("dining"):
        s = "".join(R(x - .21, y - .21, .42, .42, .06) for x, y, _ in chairs(it))
        return s + (E(0, 0, w / 2, d / 2) if t == "dining_round" else o)
    if t == "desk": return o + R(-.22, d / 2 + .02, .44, .42, .08)
    if t == "wardrobe": return o + P(M(-w / 2, 0), T(w / 2, 0)) + P(*[x for k in range(1, int(w / .14)) for x in (M(-w / 2 + k * .14, -d * .3), T(-w / 2 + k * .14, d * .3))])
    if t in ("bookshelf", "tall_cabinet", "oven_tall"): return o + P(M(-w / 2, -d / 2), T(w / 2, d / 2))
    if t == "fridge": return o + P(M(-w / 2, -d / 2), T(w / 2, d / 2), M(w / 2, -d / 2), T(-w / 2, d / 2))
    if t == "sink": return R(-w / 2 + .06, -d / 2 + .1, w * .52, d - .18, .05) + P(M(w * .1, -d / 2 + .12), T(w * .1, -d / 2 + .2)) + P(*[x for k in range(4) for x in (M(w * .12 + k * .07, -d / 2 + .16), T(w * .12 + k * .07, d / 2 - .12))])
    if t == "hob": return R(-w / 2 + .03, -d / 2 + .06, w - .06, d - .12, .03) + "".join(E(x * w * .23, y * d * .19, .085, .085) for x in (-1, 1) for y in (-1, 1))
    if t == "toilet": return R(-w / 2, -d / 2, w, .18, .03) + E(0, .06, w / 2 - .01, d / 2 - .11)
    if t == "squat": return R(-w / 2, -d / 2, w, d, .05) + E(0, 0, w * .22, d * .34)
    if t in ("basin", "vanity", "vanity2"): return o + "".join(E(x, .02, min(.2, w * .36), d * .3) for x in ((-w / 4, w / 4) if t == "vanity2" else (0,)))
    if t == "shower": return o + P(M(-w / 2, -d / 2), T(w / 2, d / 2), M(w / 2, -d / 2), T(-w / 2, d / 2)) + E(0, 0, .05, .05)
    if t == "bathtub": return o + R(-w / 2 + .07, -d / 2 + .07, w - .14, d - .14, .2)
    if t in ("washer", "laundry"): return (o if t == "laundry" else R(-w / 2 + .02, -d / 2 + .02, w - .04, d - .04, .02)) + "".join(E(x, 0, .2, .2) for x in ((-w / 4, w / 4) if t == "laundry" else (0,)))
    if t == "car": return R(-w / 2, -d / 2, w, d, .35) + R(-w / 2 + .15, -d / 2 + 1.1, w - .3, .6, .12) + R(-w / 2 + .15, d / 2 - 1.5, w - .3, .55, .12)
    if t in ("motorbike", "bicycle"): return E(0, -d / 2 + .3, .07, .3) + E(0, d / 2 - .3, .07, .3) + R(-.12, -.35, .24, .7, .1) + P(M(-w / 2, -d / 2 + .6), T(w / 2, -d / 2 + .6))
    if t in ("tree", "palm", "shrub"): return E(0, 0, w / 2, d / 2) + P(*[x for k in range(8) for x in (M(0, 0), T(w * .42 * math.cos(k * math.pi / 4 + .2), w * .42 * math.sin(k * math.pi / 4 + .2)))])
    if t in ("plant", "plant_tall", "floor_lamp", "side_table", "stool", "water_tank"): return E(0, 0, w / 2, d / 2) + E(0, 0, w * .2, d * .2)
    if t == "pond": return R(-w / 2, -d / 2, w, d, min(w, d) * .45)
    if t == "stairs":
        n = it["steps"] - 1; s = o + P(*[x for k in range(1, n) for x in (M(-w / 2, d / 2 - d * k / n), T(w / 2, d / 2 - d * k / n))])
        return s + P(M(0, d / 2 - .1), T(0, -d / 2 + .15)) + P(M(-.1, -d / 2 + .3), T(0, -d / 2 + .12), T(.1, -d / 2 + .3))
    if t in ("pendant", "ceiling_light"): return '<g stroke-dasharray=".06 .05">%s</g>' % E(0, 0, w / 2, d / 2) + P(M(-w / 2, 0), T(w / 2, 0), M(0, -d / 2), T(0, d / 2))
    if t in ("wall_cabinet", "hood", "shelf_wall", "curtain"): return '<g stroke-dasharray=".08 .06" fill="none">%s</g>' % R(-w / 2, -d / 2, w, d)
    if t == "piano": return o + R(-w / 2 + .1, d / 2 - .18, w - .2, .16)
    return o


def chairs(it):
    """Chair positions of a dining set: (x, y, facing degrees) in the item's frame."""
    w, d, t = it["w"], it["d"], it["type"]; res = []
    for s in it.get("seats", {"dining2": ["left", "right"], "dining_round": ["front", "back", "left", "right"]}.get(t, ["front", "back"])):
        L = w if s in ("front", "back") else d; n = max(1, int(L / .6 + .05)) if t != "dining_round" else 1
        for k in range(n):
            x = (k + .5) * L / n - L / 2
            res.append({"front": (x, d / 2 + .12, 180), "back": (x, -d / 2 - .12, 0), "left": (-w / 2 - .12, x, 270), "right": (w / 2 + .12, x, 90)}[s])
    return res


FLOOR_TINT = {"garden": "#e9eee2", "terrace": "#efece6", "carport": "#efefed", "balcony": "#efece6", "yard": "#f0efeb", "paving": "#efefed", "service_yard": "#f0efeb", "driveway": "#efefed"}


def plan_svg(home, lv, today, fit=None):
    site = home["site"]; polys = [r["poly"] for r in lv["rooms"]] + ([site["lot_poly"]] if "lot_poly" in site and lv is home["levels"][0] else [])
    bs = [bbox(p) for p in polys]; x0, y0, x1, y1 = min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs)
    W, H = x1 - x0, y1 - y0; pw, ph = (420, 297) if W >= H * .95 else (297, 420); room_w, room_h = pw - 84, ph - 100
    scale = next((s for s in (20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250, 500) if W * 1000 / s <= room_w and H * 1000 / s <= room_h), 500); k = 1000 / scale
    ox, oy = 52 + (room_w - W * k) / 2 - x0 * k, 44 + (room_h - H * k) / 2 - y0 * k
    X, Y = lambda v: ox + v * k, lambda v: oy + v * k; pts = lambda poly: " ".join("%.2f,%.2f" % (X(p[0]), Y(p[1])) for p in poly)
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%dmm" height="%dmm" font-family="Helvetica Neue,Arial,sans-serif">' % (pw, ph, pw, ph), '<rect width="100%" height="100%" fill="#fff"/>']
    if "lot_poly" in site and lv is home["levels"][0]:
        o.append('<polygon points="%s" fill="#fbfaf7" stroke="#888" stroke-width=".35" stroke-dasharray="6 1.5 1 1.5"/>' % pts(site["lot_poly"]))
        sb = site.get("setback", {}); a, b, c, d = bbox(site["lot_poly"])
        if sb: o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="none" stroke="#b9a" stroke-width=".2" stroke-dasharray="1.6 1.2"/>' % (X(a + sb.get("left", 0)), Y(b + sb.get("top", 0)), (c - a - sb.get("left", 0) - sb.get("right", 0)) * k, (d - b - sb.get("top", 0) - sb.get("bottom", 0)) * k))
    for r in lv["rooms"]: o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width=".18"/>' % (pts(r["poly"]), FLOOR_TINT.get(r["use"], "#f4f4f2" if r["void"] else "#fff"), "#aaa" if r["out"] else "none"))
    for r in lv["rooms"]:
        if r["void"]:
            a, b, c, d = bbox(r["poly"]); o.append('<path d="M%.2f %.2fL%.2f %.2fM%.2f %.2fL%.2f %.2f" stroke="#bbb" stroke-width=".15" stroke-dasharray="1.5 1"/>' % (X(a), Y(b), X(c), Y(d), X(c), Y(b), X(a), Y(d)))
    if fit:
        for flag, col in ((fit["cov60"], "#f4d58a"), (fit["cov75"], "#c3e2c6")):
            g = fit["g"]
            for j in range(g.H):
                i = 0
                while i < g.W:
                    if not flag[j * g.W + i]: i += 1; continue
                    e = i
                    while e < g.W and flag[j * g.W + e]: e += 1
                    o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>' % (X(g.x0 + i * CELL), Y(g.y0 + j * CELL), (e - i) * CELL * k, CELL * k + .03, col)); i = e
    lay = lambda it: 0 if "flat" in it["tags"] else 3 if "up" in it["tags"] else 2 if {"on", "under"} & set(it["tags"]) else 1
    for it in sorted(lv["items"], key=lay):
        if it["type"] in ("art", "ac", "mirror"): continue
        o.append('<g transform="translate(%.3f %.3f) rotate(%g) scale(%.4f)" fill="%s" stroke="%s" stroke-width="%.4f">%s</g>' % (X(it["at"][0]), Y(it["at"][1]), it["rot"], k, "none" if lay(it) in (0, 2, 3) else "#fff", "#c4c0b8" if lay(it) == 0 else "#8d8a85", .16 / k, symbol(it)))
    for s in lv["walls"]:
        if s["kind"] == "none": continue
        for t0, t1, z0, z1 in wall_pieces(s, lv):
            if z0 > 1.2 or z1 < 1.0 or (z0 == 0 and z1 < 1.2): continue
            e = s["th"] / 2; a0, a1 = (t0 - (e if t0 < .002 else 0)), (t1 + (e if t1 > s["len"] - .002 else 0))
            q = [(s["a"][0] + s["u"][0] * t + s["n"][0] * v, s["a"][1] + s["u"][1] * t + s["n"][1] * v) for t, v in ((a0, -e), (a1, -e), (a1, e), (a0, e))]
            o.append('<polygon points="%s" fill="%s"/>' % (pts(q), "#1d1c1b" if s["kind"] != "rail" else "#777"))
        for h in s["holes"]:
            o.append(opening_svg(lv, s, h, pts, X, Y, k)); d = outward(s) if s["kind"] == "ext" else (s["n"] if h.get("side", 1) < 0 else (-s["n"][0], -s["n"][1])); q = (h["c"][0] + d[0] * (s["th"] / 2 + 2.6 / k), h["c"][1] + d[1] * (s["th"] / 2 + 2.6 / k))
            o.append('<text x="%.2f" y="%.2f" font-size="1.9" text-anchor="middle" fill="#8a5a3a" stroke="#fff" stroke-width=".5" paint-order="stroke">%s</text>' % (X(q[0]), Y(q[1]) + .7, h["mark"]))
    if fit:
        for x0_, y0_, x1_, y1_, txt, bad in fit["lines"]:
            col = "#b3261e" if bad else "#7a3d1c"; o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width=".25"/><text x="%.2f" y="%.2f" font-size="2" font-weight="600" text-anchor="middle" fill="%s" stroke="#fff" stroke-width=".7" paint-order="stroke">%s</text>' % (X(x0_), Y(y0_), X(x1_), Y(y1_), col, (X(x0_) + X(x1_)) / 2, (Y(y0_) + Y(y1_)) / 2 + .7, col, txt))
        for it in lv["items"]:
            if it["floor"] and it["w"] * it["d"] > .13 and not it["type"] in ("screen", "stairs"): o.append('<text x="%.2f" y="%.2f" font-size="1.9" text-anchor="middle" fill="#333" stroke="#fff" stroke-width=".5" paint-order="stroke">%s</text>' % (X(it["at"][0]), Y(it["at"][1]) + .6, esc((it.get("name") or it["type"].replace("_", " "))[:22])))
        o.append('<g font-size="2.6" fill="#333"><rect x="16" y="%d" width="5" height="2.6" fill="#c3e2c6"/><text x="23" y="%d">floor reached from the front door by a path 0.75 m wide, chairs pushed in</text><rect x="16" y="%d" width="5" height="2.6" fill="#f4d58a"/><text x="23" y="%d">reached by a path 0.60 m wide</text><text x="16" y="%d" fill="#7a3d1c">lines: free space measured at each item, in metres (5 cm grid)</text></g>' % (ph - 36, ph - 33.8, ph - 31, ph - 28.8, ph - 24))
    for r in lv["rooms"] if not fit else []:
        if r["void"]: continue
        a, b, c, d = bbox(r["clear"]); cx, cy = label_point(r, lv); sq = len(r["clear"]) == 4; fs = max(2.0, min(3.2, (c - a) * k / max(6, len(r["name"])) * 1.5))
        lines = [(r["name"], fs, "600"), (("%.2f x %.2f, " % (c - a, d - b) if sq else "") + "%.1f m²" % area(r["clear"]), fs * .72, "400")]
        for i, (txt, f, wt) in enumerate(lines): o.append('<text x="%.2f" y="%.2f" font-size="%.2f" font-weight="%s" text-anchor="middle" fill="#222" stroke="#fff" stroke-width=".9" paint-order="stroke" stroke-linejoin="round">%s</text>' % (X(cx), Y(cy) + i * fs * 1.05, f, wt, esc(txt)))
    o += dims(lv, X, Y, k, (x0, y0, x1, y1))
    nx, ny = pw - 24, 24; ang = -site["north"]
    o.append('<g transform="translate(%d %d) rotate(%g)"><circle r="8" fill="none" stroke="#222" stroke-width=".3"/><path d="M0 -8L3 5L0 2.6L-3 5Z" fill="#222"/><text y="-9.4" font-size="4" text-anchor="middle" fill="#222">N</text></g>' % (nx, ny, ang))
    seg = .5 if scale <= 40 else 1 if scale <= 75 else 2; bx, by_ = 16, ph - 13
    for i in range(5): o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="1.6" fill="%s" stroke="#222" stroke-width=".2"/>' % (bx + i * seg * k, by_, seg * k, "#222" if i % 2 == 0 else "#fff"))
    o.append('<text x="%.2f" y="%.2f" font-size="2.6" fill="#222">0</text><text x="%.2f" y="%.2f" font-size="2.6" fill="#222">%g m</text>' % (bx, by_ - 1.4, bx + 5 * seg * k - 2, by_ - 1.4, 5 * seg))
    o.append('<g text-anchor="end" fill="#222"><text x="%d" y="%d" font-size="5.2" font-weight="600">%s</text><text x="%d" y="%d" font-size="3.4">%s, scale 1:%d on A3</text><text x="%d" y="%d" font-size="2.5" fill="#666">Concept drawing of %s, not for construction. Dimensions to wall centre lines; room sizes are clear inside.</text></g>' % (pw - 16, ph - 20, esc(home.get("name", "Home")), pw - 16, ph - 14, esc(lv["name"]) + (", fit check" if fit else ""), scale, pw - 16, ph - 9, today))
    return "\n".join(o) + "</svg>", (pw, ph)


def label_point(r, lv):
    """A spot for the room name that covers as little furniture as possible."""
    a, b, c, d = bbox(r["clear"]); its = [footprint(i) for i in lv["items"] if i["host"] == r["id"] and not {"up", "flat"} & set(i["tags"])]; best = None; cen = ((a + c) / 2, (b + d) / 2)
    for i in range(1, 12):
        for j in range(1, 12):
            p = (a + (c - a) * i / 12, b + (d - b) * j / 12)
            if not all(inside(q, r["clear"]) for q in ((p[0] - .5, p[1]), (p[0] + .5, p[1]), (p[0], p[1] + .2), (p[0], p[1] - .2))): continue
            hit = sum(1 for f in its for dx in (-.6, -.3, 0, .3, .6) for dy in (-.15, .1, .3) if inside((p[0] + dx, p[1] + dy), f)); sc = hit * 3 + math.dist(p, cen)
            if best is None or sc < best[0]: best = (sc, p)
    return best[1] if best else cen


def opening_svg(lv, s, o, pts, X, Y, k):
    w, e, c, u, n = o["w"] / 2, s["th"] / 2, o["c"], s["u"], s["n"]; P = lambda a, b: (c[0] + u[0] * a + n[0] * b, c[1] + u[1] * a + n[1] * b)
    ln = lambda p, q, sw=.2, col="#222": '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="%s" stroke-width="%.2f"/>' % (X(p[0]), Y(p[1]), X(q[0]), Y(q[1]), col, sw)
    if o["kind"] == "window": return "".join(ln(P(-w, b), P(w, b)) for b in (-e, -.012, .012, e)) + ln(P(-w, -e), P(-w, e)) + ln(P(w, -e), P(w, e))
    r = '<polygon points="%s" fill="#fff"/>' % pts([P(-w, -e), P(w, -e), P(w, e), P(-w, e)])
    if o["type"] in ("slide", "glass_slide", "pocket"): return r + ln(P(-w, .02), P(.04, .02), .35) + ln(P(-.04, -.02), P(w, -.02), .35) + ln(P(-w, -e), P(w, -e), .12) + ln(P(-w, e), P(w, e), .12)
    if o["type"] in ("open",): return r + ln(P(-w, -e), P(w, -e), .12, "#999") + ln(P(-w, e), P(w, e), .12, "#999")
    if o["type"] == "garage": return r + ln(P(-w, 0), P(w, 0), .3)
    for poly in swing_polys(lv, o):
        r += '<polyline points="%s" fill="none" stroke="#777" stroke-width=".16"/>' % pts(poly[1:]) + ln(poly[0], poly[-1], .4)
    return r + ln(P(-w, -e), P(w, -e), .1, "#bbb") + ln(P(-w, e), P(w, e), .1, "#bbb")


def dims(lv, X, Y, k, box):
    rooms = [r for r in lv["rooms"] if not r["out"]]; o = []
    if not rooms: return o
    xs, ys = sorted({p[0] for r in rooms for p in r["poly"]}), sorted({p[1] for r in rooms for p in r["poly"]})
    def merge(v):
        res = [v[0]]
        for a in v[1:]:
            if a - res[-1] >= .28: res.append(a)
        if res[-1] != v[-1]: res[-1] = v[-1]
        return res
    xs, ys = merge(xs), merge(ys); top, left = Y(box[1]), X(box[0])
    def chain(v, pos, hor):
        for a, b in zip(v, v[1:]):
            m = ((X(a) + X(b)) / 2 if hor else (Y(a) + Y(b)) / 2); t = "%.2f" % (b - a)
            if hor: o.append('<path d="M%.2f %.2fH%.2fM%.2f %.2fl1.4 -1.4M%.2f %.2fl1.4 -1.4" stroke="#333" stroke-width=".16"/><text x="%.2f" y="%.2f" font-size="2.3" text-anchor="middle" fill="#333">%s</text>' % (X(a), pos, X(b), X(a) - .7, pos + .7, X(b) - .7, pos + .7, m, pos - 1, t))
            else: o.append('<path d="M%.2f %.2fV%.2fM%.2f %.2fl1.4 -1.4M%.2f %.2fl1.4 -1.4" stroke="#333" stroke-width=".16"/><text transform="translate(%.2f %.2f) rotate(-90)" font-size="2.3" text-anchor="middle" fill="#333">%s</text>' % (pos, Y(a), Y(b), pos - .7, Y(a) + .7, pos - .7, Y(b) + .7, pos - 1, m, t))
        for a in v:
            o.append('<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" stroke="#999" stroke-width=".12"/>' % ((X(a), pos - 1.5, X(a), pos + 4) if hor else (pos - 1.5, Y(a), pos + 4, Y(a))))
    chain(xs, top - 8, True); chain(ys, left - 8, False)
    if len(xs) > 2: chain([xs[0], xs[-1]], top - 15, True)
    if len(ys) > 2: chain([ys[0], ys[-1]], left - 15, False)
    return o


def schedule(home):
    o = ["# %s: schedule" % home.get("name", "Home"), "", "Concept quantities taken from the plan. No prices: ask a local supplier or look up dated ones. Sun hours are for the best window of the room, with the home's own walls, roof edges and the given neighbours in the way; trees are not counted.", ""]
    fin, paint = defaultdict(float), defaultdict(float)
    for lv in home["levels"]:
        o += ["## %s (ceiling %.2f m)" % (lv["name"], lv["height"]), "", "| Room | Use | Clear size (m) | Area (m2) | Floor | Direct sun, hours between 08 and 16, Mar / Jun / Dec |", "|---|---|---|---|---|---|"]
        for r in lv["rooms"]:
            if r["void"]: continue
            a, b, c, d = bbox(r["clear"]); A = area(r["clear"]); fin[r.get("floor", "unset")] += A
            best = [0, 0, 0]
            for s in lv["walls"]:
                for q in s["holes"] if s["kind"] == "ext" and r["id"] in s["rooms"] else []:
                    if q["kind"] == "window" or q["type"] in ("glass", "glass_slide"):
                        h = sun_hours(home, lv, s, q); best = [max(x, y) for x, y in zip(best, h)] if h else best
            sun_t = "outside" if r["out"] else "%g / %g / %g" % tuple(best) if "lat" in home["site"] else "no location"
            o.append("| %s | %s | %s | %.1f | %s | %s |" % (r["name"], r["use"], "%.2f x %.2f" % (c - a, d - b) if len(r["clear"]) == 4 else "irregular", A, r.get("floor", "unset"), sun_t))
        o.append(""); rows = []
        for q in lv["doors"]:
            rows.append("| %s | door, %s | %.2f x %.2f | %s |" % (q["mark"], q["type"], q["w"], q["h"], " / ".join(q.get("rooms", []))))
        for q in lv["windows"]:
            s = lv["walls"][q["wall"]] if q["wall"] is not None else None
            rows.append("| %s | window, %s | %.2f x %.2f, sill %.2f | %s%s |" % (q["mark"], q["type"], q["w"], q["h"], q["sill"], " / ".join(x for x in q.get("rooms", []) if x != "outside"), ", faces " + compass(bearing(home, outward(s))) if s and s["kind"] == "ext" else ""))
        if rows: o += ["| Mark | Type | Size (m) | Where |", "|---|---|---|---|"] + rows + [""]
        for s in lv["walls"]:
            if s["kind"] in ("ext", "int"):
                A = s["len"] * lv["height"] - sum(h["w"] * h["h"] for h in s["holes"]); paint["inside wall faces"] += A * (2 if s["kind"] == "int" else 1); paint["outside wall faces"] += A if s["kind"] == "ext" else 0
    o += ["## Quantities", "", "| What | m2 |", "|---|---|"] + ["| floor: %s | %.1f |" % x for x in sorted(fin.items())] + ["| %s, openings taken out | %.1f |" % x for x in sorted(paint.items())]
    o += ["", "## Furniture and fittings", "", "| Room | Item | Width x depth x height (m) |", "|---|---|---|"]
    for lv in home["levels"]:
        nm = {r["id"]: r["name"] for r in lv["rooms"]}
        for it in sorted(lv["items"], key=lambda i: (nm.get(i["host"], "outside"), i["type"])): o.append("| %s | %s | %.2f x %.2f x %.2f |" % (nm.get(it["host"], "outside"), it.get("name") or it["type"].replace("_", " "), it["w"], it["d"], it["h"]))
    return "\n".join(o) + "\n"


def scene(home):
    """Everything the viewer needs, already in metres: x right, y down the plan, z up."""
    S = home["style"]; out = {"name": home.get("name", "Home"), "style": S, "levels": [], "site": {k: v for k, v in home["site"].items() if k != "lot"}, "roofs": [], "when": home.get("when", {})}
    st = home["site"]; w = home.get("when", {}); day, hour = w.get("day", 80), w.get("hour", 10)
    az, el = sun(st["lat"], st.get("lon", 0), st.get("tz", round(st.get("lon", 0) / 15)), day, hour) if "lat" in st else (120, 45)
    b = math.radians(az - st["north"]); out["sun"] = {"x": math.sin(b), "y": -math.cos(b), "el": el}
    for lv in home["levels"]:
        L = {"id": lv["id"], "name": lv["name"], "z": lv["z"], "height": lv["height"], "slab": lv["slab"], "rooms": [], "walls": [], "openings": [], "items": []}
        by = {r["id"]: r for r in lv["rooms"]}; fac = lv.get("facade") or S["facade"]; col = lambda i: (by[i].get("wall") or S["wall"]) if i in by else fac
        for r in lv["rooms"]: L["rooms"].append({"id": r["id"], "name": r["name"], "use": r["use"], "poly": r["poly"], "clear": r["clear"], "out": r["out"], "void": r["void"], "floor": r.get("floor"), "cover": r.get("cover"), "rail": r.get("rail"), "area": area(r["clear"])})
        for s in lv["walls"]:
            if s["kind"] == "none": continue
            base = {"a": s["a"], "u": s["u"], "n": s["n"], "th": s["th"], "len": s["len"], "kind": s["kind"], "pos": col(s["pos"]) if s["pos"] else fac, "neg": col(s["neg"]) if s["neg"] else fac, "fac": fac, "out": 0 if s["kind"] != "ext" else (1 if s["pos"] is None else -1)}
            for key, p, k in (("capA", s["a"], -1), ("capB", (s["a"][0] + s["u"][0] * s["len"], s["a"][1] + s["u"][1] * s["len"]), 1)):  # the end of a wall shows the room it looks into
                q = (p[0] + s["u"][0] * k * (s["th"] / 2 + .03), p[1] + s["u"][1] * k * (s["th"] / 2 + .03)); base[key] = next((col(r["id"]) for r in lv["rooms"] if not r["out"] and not r["void"] and inside(q, r["poly"])), fac if s["kind"] == "ext" else base["pos"])
            L["walls"].append({**base, "pieces": wall_pieces(s, lv)})
            for o in s["holes"]: L["openings"].append({"kind": o["kind"], "type": o["type"], "c": o["c"], "u": s["u"], "n": s["n"], "th": s["th"], "w": o["w"], "h": o["h"], "sill": o["sill"], "ext": s["kind"] == "ext", "glass": bool(o.get("glass")), "side": o.get("side", 1), "hinge": o.get("hinge_sign", -1), "color": o.get("color"), "out": base["out"], "shade": o.get("shade"), "panes": o.get("panes"), "rail": bool(o.get("rail"))})
        for it in lv["items"]: L["items"].append({"type": it["type"], "at": it["at"], "rot": it["rot"], "w": it["w"], "d": it["d"], "h": it["h"], "z": it["z"], "color": it.get("color"), "host": it["host"], "steps": it.get("steps"), "riser": it.get("riser"), "going": it.get("going"), "chairs": chairs(it) if it["type"].startswith("dining") else None, "name": it.get("name"), **{k: it[k] for k in ("splash", "head", "side") if k in it}})
        out["levels"].append(L)
    top = home["levels"][-1]; rf = home.get("roofs"); one = home.get("roof", {})
    if rf is None and one.get("type") != "none":
        bs = [bbox(r["poly"]) for r in top["rooms"] if not r["out"]]
        e = home["walls"]["ext"] / 2; a, b, c, d = min(k[0] for k in bs) - e, min(k[1] for k in bs) - e, max(k[2] for k in bs) + e, max(k[3] for k in bs) + e; rf = [{**one, "rect": [a, b, c - a, d - b]}]
    for r in rf or []: out["roofs"].append({"type": "gable", "pitch": 30, "overhang": .6, "ridge": "auto", "z": top["z"] + top["height"], **r})
    out["views"] = views(home); out["ext"] = home["walls"]["ext"]
    return out


def views(home):
    """Automatic cameras plus the file's own views."""
    res = []; L0 = home["levels"][0]; pts = home["site"].get("lot_poly") or [p for r in L0["rooms"] for p in r["poly"]]; x0, y0, x1, y1 = bbox(pts); cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; R = math.hypot(x1 - x0, y1 - y0)
    top = home["levels"][-1]; H = top["z"] + top["height"]; f = {"top": (0, -1), "bottom": (0, 1), "left": (-1, 0), "right": (1, 0)}.get(home["site"].get("street", "bottom"), (0, 1)); side = (f[1], -f[0])
    for lv in home["levels"]:
        bs = [bbox(r["poly"]) for r in lv["rooms"]]; a, b, c, d = min(k[0] for k in bs), min(k[1] for k in bs), max(k[2] for k in bs), max(k[3] for k in bs); m = ((a + c) / 2, (b + d) / 2); r = max(c - a, d - b)
        res.append({"name": "cut-" + lv["id"], "cut": lv["id"], "from": [m[0] + r * .16, m[1] + r * .75, lv["z"] + r * 1.5], "to": [m[0], m[1], lv["z"] + .5], "fov": 30, "fit": [a, b, lv["z"], c, d, lv["z"] + 1.6], "portrait": d - b > (c - a) * 1.15})
    if home["site"].get("lot_poly") or any(r["out"] for r in L0["rooms"]):
        W = abs(side[0]) * (x1 - x0) + abs(side[1]) * (y1 - y0); far = max(W, H) * 1.15 + 3; ex = (x1 if f[0] > 0 else x0) if f[0] else cx; ey = (y1 if f[1] > 0 else y0) if f[1] else cy
        res.append({"name": "street", "from": [ex + f[0] * far + side[0] * W * .55, ey + f[1] * far + side[1] * W * .55, 1.6], "to": [ex - f[0] * 2 + side[0] * W * .02, ey - f[1] * 2 + side[1] * W * .02, 1.6], "fov": 38, "shift": .11})
        res.append({"name": "aerial", "from": [cx + f[0] * R - side[0] * R * .75, cy + f[1] * R - side[1] * R * .75, H + R * .75], "to": [cx, cy, H * .3], "fov": 32, "fit": [x0, y0, 0, x1, y1, H + 1.2]})
    for lv in home["levels"]:
        for r in lv["rooms"]:
            if r["out"] or r["void"] or r["use"] in ("storage", "corridor", "shaft", "stairs"): continue
            v = room_view(lv, r)
            if v: res.append(v)
    own = home.get("views", []); names = {v.get("name") for v in own}
    return [v for v in res if v["name"] not in names] + [{"fov": 62, **v} for v in own]


def room_view(lv, r):
    """Level eye-height camera at the spot and angle that show most of the room, its furniture and its windows."""
    x0, y0, x1, y1 = bbox(r["clear"]); g = next((g for g in groups(lv) if r["id"] in g), [r["id"]]); polys = [k["clear"] for k in lv["rooms"] if k["id"] in g]
    block = [footprint(i) for i in lv["items"] if i["host"] in g and i["z"] < 1.35 < i["z"] + i["h"] and "soft" not in i["tags"]]; low = [footprint(i) for i in lv["items"] if i["host"] in g and i["floor"] and "soft" not in i["tags"]]
    high = [footprint(i) for i in lv["items"] if i["host"] in g and i["z"] < .9 and i["z"] + i["h"] > .7 and i["type"] != "shower"]
    mine = [i["at"] for i in lv["items"] if i["host"] == r["id"] and not {"up", "flat"} & set(i["tags"])]; glass = [o["c"] for o in lv["windows"] + lv["doors"] if o["wall"] is not None and r["id"] in o["rooms"] and (o["kind"] == "window" or o["type"] == "glass_slide")]
    free = lambda p: any(inside(p, q) for q in polys) or any(s["kind"] == "none" and seg_dist(p, s["a"], s["b"]) < .12 for s in lv["walls"])
    fov = 56 if r["use"] not in ("bath", "wc") and min(x1 - x0, y1 - y0) > 2 else 70; half = math.atan(math.tan(math.radians(fov / 2)) * 1.6); best = None
    for fx in (.06, .3, .5, .7, .94):
        for fy in (.06, .3, .5, .7, .94):
            p = (min(max(x0 + (x1 - x0) * fx, x0 + .22), x1 - .22), min(max(y0 + (y1 - y0) * fy, y0 + .22), y1 - .22))
            if not inside(p, r["clear"]) or any(inside(p, t) for t in block): continue
            ray = []
            for k in range(72):
                a = k * math.pi / 36; t = .1
                while t < 7 and free((p[0] + math.cos(a) * t, p[1] + math.sin(a) * t)) and not any(inside((p[0] + math.cos(a) * t, p[1] + math.sin(a) * t), q) for q in block): t += .15
                ray.append(t)
            for k in range(0, 72, 2):
                a = k * math.pi / 36; fan = [ray[(k + j) % 72] for j in range(-int(half * 36 / math.pi), int(half * 36 / math.pi) + 1)]
                def seen(q):
                    dd = math.dist(p, q); b = math.atan2(q[1] - p[1], q[0] - p[0]); return dd > .8 and abs((b - a + math.pi) % (2 * math.pi) - math.pi) < half * .88 and ray[int(round(b * 36 / math.pi)) % 72] > dd - .7
                sc = sum(min(t, 5) for t in fan) / len(fan) * 1.2 + 1.0 * sum(map(seen, mine)) / max(1, len(mine)) * 3 + (2.0 if any(map(seen, glass)) else 0) - (2 if min(fan) < .6 else 0) - (1.2 if any(inside(p, t) for t in low) else 0) - (1.5 if any(inside((p[0] + math.cos(b) * t, p[1] + math.sin(b) * t), q) for q in high for b in (a - half * .8, a - half * .4, a, a + half * .4, a + half * .8) for t in (.25, .5, .75)) else 0) - (.8 if a % (math.pi / 2) < .02 else 0)
                if best is None or sc > best[0]: best = (sc, p, a)
    if not best: return None
    _, p, a = best; z = lv["z"] + 1.35; return {"name": "room-" + r["id"], "room": r["id"], "level": lv["id"], "from": [p[0], p[1], z], "to": [p[0] + math.cos(a), p[1] + math.sin(a), z], "fov": fov, "shift": -.24 if fov > 60 else -.1}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=pathlib.Path)
    parser.add_argument("output", type=pathlib.Path, help="a new directory for the drawings")
    args = parser.parse_args()
    try:
        model = load(args.model)
        plans = [plan_svg(model, level, "Concept drawing") for level in model["levels"]]
        documents = {"scene.json": json.dumps(scene(model), indent=2), "schedule.md": schedule(model)}
        for index, plan in enumerate(plans, 1):
            documents[f"level-{index}.svg"] = plan[0] if isinstance(plan, tuple) else plan
        args.output.mkdir()
        for name, content in documents.items():
            (args.output / name).write_text(content, encoding="utf-8")
    except (KeyError, TypeError, ValueError, OSError, Bad) as error:
        parser.exit(2, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
