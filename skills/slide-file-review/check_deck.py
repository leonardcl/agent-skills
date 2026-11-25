#!/usr/bin/env python3
"""Check a finished .pptx for the faults that break Korean, Chinese, Japanese or mixed-language decks in
PowerPoint, plus off-slide geometry and text left under cover-ups. Reads the file as a zip of XML (standard
library only); never writes to the deck.

  python3 check_deck.py deck.pptx [--margin-px 40]
  python3 check_deck.py --self-test

Codes: ea-missing (error), latin-break (error when the deck has English text), off-slide (error for text,
warning otherwise), off-margin, font-missing, font-variable, near-white-cover, covered-text, hidden-text,
ea-latin-face (warnings). Exit 0 when there are no errors, 1 on any error, 2 when the file cannot be read."""
import argparse, colorsys, math, os, posixpath, re, sys, tempfile, zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"a": A, "p": P, "r": R, "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
      "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006"}
EMU_PX, EMU_IN = 9525, 914400
TOL = 2 * EMU_PX
IDENTITY = (1.0, 0.0, 1.0, 0.0)

HANGUL = "ᄀ-ᇿ㄰-㆏ꥠ-꥿가-힯ힰ-퟿"
KANA = "぀-ヿㇰ-ㇿｦ-ﾟ"
HAN = "㐀-䶿一-鿿豈-﫿"
EA_RE = re.compile("[%s%s%s　-〿！-｠￠-￦]" % (HANGUL, KANA, HAN))
HANGUL_RE, KANA_RE = re.compile("[%s]" % HANGUL), re.compile("[%s]" % KANA)
LATIN_WORD = re.compile(r"[A-Za-z]{2,}")
TITLE_TYPES = {"title", "ctrTitle"}
# Families that carry CJK glyphs, matched as substrings of the lowercased name with spaces removed.
CJK_FACES = ("malgun", "batang", "gulim", "dotum", "gungsuh", "nanum", "applesdgothic", "applegothic",
             "applemyungjo", "pretendard", "suit", "spoqa", "notosanscjk", "notoserifcjk", "notosanskr",
             "notoserifkr", "notosansjp", "notoserifjp", "notosanssc", "notoserifsc", "notosanstc", "notoseriftc",
             "notosanshk", "sourcehan", "hiragino", "meiryo", "yugoth", "yumin", "msgothic", "mspgothic", "msmincho",
             "mspmincho", "msuigothic", "pingfang", "yahei", "jhenghei", "simsun", "simhei", "dengxian", "fangsong",
             "kaiti", "mingliu", "heiti", "songti", "gmarket", "kopub", "plexsanskr", "plexsansjp", "wantedsans",
             "nexon", "paperlogy", "scoredream", "arialunicode", "bizud", "kozuka", "osaka", "lxgw")
# Font file name stems for families whose files are not named after the family.
FILE_HINTS = {"맑은고딕": ["malgun"], "malgungothic": ["malgun"], "바탕": ["batang"], "굴림": ["gulim"],
              "돋움": ["dotum", "gulim"], "궁서": ["gungsuh", "batang"], "宋体": ["simsun"], "新宋体": ["simsun"],
              "黑体": ["simhei"], "等线": ["deng"], "dengxian": ["deng"], "微软雅黑": ["msyh"],
              "microsoftyahei": ["msyh"], "新細明體": ["mingliu"], "pmingliu": ["mingliu"], "微軟正黑體": ["msjh"],
              "microsoftjhenghei": ["msjh"], "ｍｓｐゴシック": ["msgothic"], "ｍｓゴシック": ["msgothic"],
              "mspgothic": ["msgothic"], "ｍｓ明朝": ["msmincho"], "ｍｓｐ明朝": ["msmincho"],
              "游ゴシック": ["yugoth"], "yugothic": ["yugoth"], "游明朝": ["yumin"], "yumincho": ["yumin"],
              "メイリオ": ["meiryo"], "calibrilight": ["calibril"], "arialblack": ["ariblk"], "consolas": ["consola"],
              "constantia": ["constan"]}
FONT_EXT = (".ttf", ".otf", ".ttc", ".otc", ".dfont")
WEIGHT_TAIL = re.compile(r"(\s+(thin|hairline|extra ?light|ultra ?light|light|regular|book|medium|semi ?bold|demi ?bold|"
                         r"bold|extra ?bold|ultra ?bold|black|heavy|italic|oblique))+$", re.I)


def local(tag):
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def norm(name):
    return re.sub(r"[\s\-_]", "", name).lower()


def is_cjk_face(face):
    return bool(re.search("[%s%s%s＀-￯]" % (HANGUL, KANA, HAN), face)) or any(k in norm(face) for k in CJK_FACES)


class Pkg:
    def __init__(self, path):
        self.z = zipfile.ZipFile(path)
        self.names = set(self.z.namelist())
        self.cache = {}

    def xml(self, part):
        if part not in self.cache:
            self.cache[part] = ET.fromstring(self.z.read(part)) if part and part in self.names else None
        return self.cache[part]

    def rels(self, part):
        d, f = posixpath.split(part)
        root = self.xml(posixpath.join(d, "_rels", f + ".rels"))
        out = {}
        for rel in (root.findall("pr:Relationship", NS) if root is not None else []):
            if rel.get("TargetMode") == "External":
                continue
            t = rel.get("Target", "")
            out[rel.get("Id")] = (rel.get("Type", "").rsplit("/", 1)[-1],
                                  t.lstrip("/") if t.startswith("/") else posixpath.normpath(posixpath.join(d, t)))
        return out

    def target(self, part, typ):
        return next((t for k, t in self.rels(part).values() if k == typ), None)


def face(el, slot="ea"):
    e = el.find("a:" + slot, NS) if el is not None else None
    return (e.get("typeface") or None) if e is not None else None


def lvl_rpr(style, lvl):
    return style.find("a:lvl%dpPr/a:defRPr" % lvl, NS) if style is not None else None


def ph_of(el):
    ph = el.find("./*/p:nvPr/p:ph", NS) if el is not None else None
    return (ph.get("type", "obj"), ph.get("idx")) if ph is not None else None


def master_type(t):
    return "title" if t in TITLE_TYPES else (t if t in ("dt", "ftr", "sldNum", "hdr") else "body")


def find_ph(cands, ph, by_type=False):
    if ph is None:
        return None
    typ, idx = ph
    if typ in TITLE_TYPES:
        return next((el for (t, _), el in cands if t in TITLE_TYPES), None)
    if not by_type and idx is not None:
        hit = next((el for (_, i), el in cands if i == idx), None)
        if hit is not None:
            return hit
    if by_type:
        return next((el for (t, _), el in cands if master_type(t) == master_type(typ)), None)
    return next((el for (t, _), el in cands if t == typ), None)


def placeholders(root):
    return [(ph_of(el), el) for el in root.iter("{%s}sp" % P) if ph_of(el)] if root is not None else []


class Master:
    def __init__(self, pkg, part):
        self.root = pkg.xml(part)
        self.phs = placeholders(self.root)
        ts = self.root.find("p:txStyles", NS) if self.root is not None else None
        self.styles = {k: (ts.find("p:%sStyle" % k, NS) if ts is not None else None) for k in ("title", "body", "other")}
        cm = self.root.find("p:clrMap", NS) if self.root is not None else None
        self.clrmap = dict(cm.attrib) if cm is not None else {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2"}
        theme = pkg.xml(pkg.target(part, "theme")) if part else None
        self.fonts, self.colors = {}, {}
        for kind in ("major", "minor"):
            f = theme.find(".//a:fontScheme/a:%sFont" % kind, NS) if theme is not None else None
            self.fonts[kind] = {"ea": face(f, "ea") or "", "latin": face(f, "latin") or "", "cs": face(f, "cs") or "",
                                "scripts": {e.get("script"): e.get("typeface") or ""
                                            for e in (f.findall("a:font", NS) if f is not None else [])}}
        cs = theme.find(".//a:clrScheme", NS) if theme is not None else None
        for c in (cs if cs is not None else []):
            if len(c):
                self.colors[local(c.tag)] = c[0].get("val") if local(c[0].tag) == "srgbClr" else c[0].get("lastClr")


def scripts_for(text, lang):
    if HANGUL_RE.search(text):
        return ["Hang"]
    if KANA_RE.search(text):
        return ["Jpan"]
    lang = (lang or "").lower()
    for pre, s in (("ko", "Hang"), ("ja", "Jpan"), ("zh-tw", "Hant"), ("zh-hk", "Hant"), ("zh-mo", "Hant"), ("zh", "Hans")):
        if lang.startswith(pre):
            return [s]
    return ["Hans", "Hant", "Jpan", "Hang"]


def theme_ea(master, kind, text, lang, via):
    t = master.fonts[kind]
    tail = " (via %s)" % via if via else ""
    if t["ea"]:
        return t["ea"], "theme %s ea%s" % (kind, tail)
    scripts = scripts_for(text, lang)
    for s in scripts:
        if t["scripts"].get(s):
            return t["scripts"][s], "theme %s %s script font%s" % (kind, s, tail)
    return None, "theme %s%s: ea empty and no %s script font" % (kind, tail, "/".join(scripts))


def resolve_ea(chain, master, default_kind, text, lang):
    for label, tf in chain:
        if tf and tf.startswith(("+mj", "+mn")):
            return theme_ea(master, "major" if tf.startswith("+mj") else "minor", text, lang, label)
        if tf:
            return tf, label
    return theme_ea(master, default_kind, text, lang, None)


def adjust(rgb, col):
    mod, off = col.find("a:lumMod", NS), col.find("a:lumOff", NS)
    if mod is None and off is None:
        return rgb
    h, l, s = colorsys.rgb_to_hls(*[int(rgb[i:i + 2], 16) / 255.0 for i in (0, 2, 4)])
    l = l * (int(mod.get("val")) / 100000.0 if mod is not None else 1) + (int(off.get("val")) / 100000.0 if off is not None else 0)
    return "%02X%02X%02X" % tuple(int(round(v * 255)) for v in colorsys.hls_to_rgb(h, min(1.0, max(0.0, l)), s))


def color(col, master):
    """(opaque, RRGGBB or None) of a colour element."""
    t = local(col.tag)
    rgb = None
    if t == "srgbClr":
        rgb = col.get("val")
    elif t == "schemeClr":
        rgb = master.colors.get(master.clrmap.get(col.get("val"), col.get("val")))
    elif t == "sysClr":
        rgb = col.get("lastClr")
    elif t == "prstClr":
        rgb = {"white": "FFFFFF", "black": "000000"}.get(col.get("val"))
    alpha = col.find("a:alpha", NS)
    opaque = alpha is None or int(alpha.get("val", "100000")) >= 95000
    return opaque, (adjust(rgb, col).upper() if rgb and len(rgb) == 6 else None)


def fill_of(el, master):
    sppr = el.find("p:spPr", NS)
    for c in (sppr if sppr is not None else []):
        t = local(c.tag)
        if t == "noFill" or t in ("gradFill", "blipFill", "pattFill", "grpFill"):
            return False, None
        if t == "solidFill":
            return color(c[0], master) if len(c) else (True, None)
    ref = el.find("p:style/a:fillRef", NS)
    if ref is not None and ref.get("idx", "0") != "0" and len(ref):
        return color(ref[0], master)
    return False, None


def near_white(rgb):
    return bool(rgb) and all(int(rgb[i:i + 2], 16) >= 0xF5 for i in (0, 2, 4))


def xfrm_box(xfrm, xf):
    off, ext = xfrm.find("a:off", NS), xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return None
    sx, ox, sy, oy = xf
    x, y = int(off.get("x", 0)) * sx + ox, int(off.get("y", 0)) * sy + oy
    w, h = int(ext.get("cx", 0)) * sx, int(ext.get("cy", 0)) * sy
    rot = int(xfrm.get("rot", 0)) / 60000.0
    if rot % 180:
        c, s = abs(math.cos(math.radians(rot))), abs(math.sin(math.radians(rot)))
        cx, cy = x + w / 2, y + h / 2
        w, h = w * c + h * s, w * s + h * c
        x, y = cx - w / 2, cy - h / 2
    return (x, y, x + w, y + h)


def group_xf(xfrm, xf):
    if xfrm is None:
        return xf
    g = {k: xfrm.find("a:" + k, NS) for k in ("off", "ext", "chOff", "chExt")}
    if any(v is None for v in g.values()):
        return xf
    sx, ox, sy, oy = xf
    kx = int(g["ext"].get("cx")) / float(int(g["chExt"].get("cx")) or int(g["ext"].get("cx")) or 1)
    ky = int(g["ext"].get("cy")) / float(int(g["chExt"].get("cy")) or int(g["ext"].get("cy")) or 1)
    return (sx * kx, sx * (int(g["off"].get("x")) - int(g["chOff"].get("x")) * kx) + ox,
            sy * ky, sy * (int(g["off"].get("y")) - int(g["chOff"].get("y")) * ky) + oy)


def area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def overlap(a, b):
    return area((max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])))


def contains(outer, inner):
    return (outer[0] - TOL <= inner[0] and outer[1] - TOL <= inner[1]
            and outer[2] + TOL >= inner[2] and outer[3] + TOL >= inner[3])


def snip(text, n=40):
    text = " ".join(text.split())
    return '"%s"' % (text if len(text) <= n else text[:n - 3] + "...")


class Slide:
    def __init__(self, pkg, part, num, masters, pres_default):
        self.pkg, self.part, self.num = pkg, part, num
        self.root = pkg.xml(part)
        self.hidden = self.root.get("show") == "0"
        self.rels = pkg.rels(part)
        lay_part = pkg.target(part, "slideLayout")
        self.layout_phs = placeholders(pkg.xml(lay_part))
        mpart = pkg.target(lay_part, "slideMaster") if lay_part else None
        if mpart not in masters:
            masters[mpart] = Master(pkg, mpart)
        self.master = masters[mpart]
        self.pres_default = pres_default
        self.shapes = []
        tree = self.root.find("p:cSld/p:spTree", NS)
        self.walk(tree if tree is not None else [], IDENTITY)

    def walk(self, tree, xf):
        for el in tree:
            t = local(el.tag)
            if t == "AlternateContent":
                pick = el.find("mc:Choice", NS)
                pick = pick if pick is not None else el.find("mc:Fallback", NS)
                self.walk(pick if pick is not None else [], xf)
            elif t == "grpSp":
                self.walk(el, group_xf(el.find("p:grpSpPr/a:xfrm", NS), xf))
            elif t in ("sp", "pic", "graphicFrame", "cxnSp"):
                self.shapes.append(self.shape(el, t, xf))

    def shape(self, el, kind, xf):
        nv = el.find("./*/p:cNvPr", NS)
        s = {"name": nv.get("name", "?") if nv is not None else "?", "kind": kind,
             "hidden": nv is not None and nv.get("hidden") in ("1", "true"), "breaks": 0,
             "opaque": False, "rgb": None, "rectish": False, "text": "", "ea_missing": [], "ea_latin": []}
        ph = ph_of(el)
        lay = find_ph(self.layout_phs, ph)
        mas = find_ph(self.master.phs, ph_of(lay) or ph, by_type=True)
        xfrm = el.find("p:xfrm", NS) if kind == "graphicFrame" else el.find("p:spPr/a:xfrm", NS)
        if xfrm is None and ph:
            for src in (lay, mas):
                x = src.find("p:spPr/a:xfrm", NS) if src is not None else None
                if x is not None:
                    xfrm, xf = x, IDENTITY
                    break
        s["box"] = xfrm_box(xfrm, xf) if xfrm is not None else None
        s["breaks"] = sum(1 for e in el.iter() if e.get("latinLnBrk") in ("1", "true"))
        if kind == "sp":
            s["opaque"], s["rgb"] = fill_of(el, self.master)
            geom = el.find("p:spPr/a:prstGeom", NS)
            s["rectish"] = geom is not None and geom.get("prst") in ("rect", "roundRect")
        elif kind == "pic":
            blip = el.find("p:blipFill/a:blip", NS)
            tgt = self.rels.get(blip.get("{%s}embed" % R), ("", ""))[1] if blip is not None else ""
            s["opaque"] = tgt.lower().endswith((".jpg", ".jpeg")) and blip.find("a:alphaModFix", NS) is None
            s["rectish"] = True
        bp = el.find("p:txBody/a:bodyPr", NS)
        s["inset"] = [int(bp.get(k, d)) if bp is not None else d
                      for k, d in (("lIns", 91440), ("tIns", 45720), ("rIns", 91440), ("bIns", 45720))]
        if kind == "sp":
            bodies = [(el.find("p:txBody", NS), "shape")]
        elif kind == "graphicFrame":
            bodies = [(tc.find("a:txBody", NS), "table cell") for tc in el.iter("{%s}tc" % A)]
        else:
            bodies = []
        style = None
        if ph:
            style = "title" if ph[0] in TITLE_TYPES else ("other" if ph[0] in ("dt", "ftr", "sldNum", "hdr") else "body")
        ref = el.find("p:style/a:fontRef", NS)
        fontref = {"minor": "+mn-ea", "major": "+mj-ea"}.get(ref.get("idx")) if ref is not None else None
        texts = []
        for body, where in bodies:
            if body is None:
                continue
            lst = body.find("a:lstStyle", NS)
            for p in body.findall("a:p", NS):
                ppr = p.find("a:pPr", NS)
                lvl = int(ppr.get("lvl", 0)) + 1 if ppr is not None else 1
                for r in p:
                    if local(r.tag) not in ("r", "fld"):
                        continue
                    text = r.findtext("a:t", "", NS)
                    texts.append(text)
                    if EA_RE.search(text):
                        self.east_asian(s, r.find("a:rPr", NS), ppr, lst, lvl, where, ph, lay, mas, style, fontref, text)
                texts.append("\n")
        s["text"] = "".join(texts).strip()
        return s

    def east_asian(self, s, rpr, ppr, lst, lvl, where, ph, lay, mas, style, fontref, text):
        chain = [("run", face(rpr)), ("paragraph default", face(ppr.find("a:defRPr", NS) if ppr is not None else None)),
                 ("%s list style" % where, face(lvl_rpr(lst, lvl)))]
        if ph:
            chain += [("layout placeholder", face(lvl_rpr(lay.find("p:txBody/a:lstStyle", NS) if lay is not None else None, lvl))),
                      ("master placeholder", face(lvl_rpr(mas.find("p:txBody/a:lstStyle", NS) if mas is not None else None, lvl))),
                      ("master %sStyle" % style, face(lvl_rpr(self.master.styles[style], lvl)))]
        else:
            if where == "shape":
                chain.append(("shape style fontRef", fontref))
            chain.append(("presentation default", face(lvl_rpr(self.pres_default, lvl))))
        lang = None
        if rpr is not None:
            alt = rpr.get("altLang", "")
            lang = alt if alt[:2].lower() in ("ko", "ja", "zh") else rpr.get("lang")
        kind = "major" if ph and ph[0] in TITLE_TYPES else "minor"
        found, stop = resolve_ea(chain, self.master, kind, text, lang)
        if found is None:
            s["ea_missing"].append((text, " > ".join(lbl for lbl, _ in chain) + " > theme", stop))
        else:
            s.setdefault("ea_ok", []).append((found, stop))
            if not is_cjk_face(found):
                s["ea_latin"].append(found)


def part_contexts(root):
    """Count latinLnBrk=1 per nearest named context (shape name or text style) in a layout, master or presentation part."""
    parent = {c: p for p in root.iter() for c in p}
    out = Counter()
    for e in root.iter():
        if e.get("latinLnBrk") not in ("1", "true"):
            continue
        ctx, cur = local(root.tag), e
        while cur in parent:
            cur = parent[cur]
            t = local(cur.tag)
            if t in ("sp", "graphicFrame"):
                nv = cur.find("./*/p:cNvPr", NS)
                ctx = 'shape "%s"' % (nv.get("name") if nv is not None else "?")
                break
            if t in ("defaultTextStyle", "titleStyle", "bodyStyle", "otherStyle", "notesStyle"):
                ctx = t
                break
        out[ctx] += 1
    return out


def font_files():
    configured = os.environ.get("DECK_FONT_DIRS")
    dirs = [os.path.expanduser(p) for p in (configured or "").split(os.pathsep) if p]
    dirs = [p for p in dirs if os.path.isdir(p)]
    files = []
    for d in dirs:
        for dp, _, fns in os.walk(d):
            files += [fn for fn in fns if fn.lower().endswith(FONT_EXT)]
    return dirs, files


def match_font(family, files):
    hints = FILE_HINTS.get(norm(family), []) + [norm(family)]
    return [f for f in files if any(norm(os.path.splitext(f)[0]).startswith(h) for h in hints if h)]


def is_variable(fn):
    return "[" in fn or "variable" in fn.lower()


def pages(nums):
    nums = sorted(n for n in nums if isinstance(n, int))
    return ", ".join(str(n) for n in nums[:12]) + (" ..." if len(nums) > 12 else "")


def check(path, margin_px=None):
    """Return (findings, info, meta). A finding is (slide number or 0 for the deck, severity, shape name, code, message)."""
    pkg = Pkg(path)
    pres_part = pkg.target("", "officeDocument") or "ppt/presentation.xml"
    pres = pkg.xml(pres_part)
    if pres is None:
        raise ValueError("no presentation part in %s" % path)
    sz = pres.find("p:sldSz", NS)
    W, H = (int(sz.get("cx")), int(sz.get("cy"))) if sz is not None else (12192000, 6858000)
    pres_default = pres.find("p:defaultTextStyle", NS)
    prels = pkg.rels(pres_part)
    order = [prels[s.get("{%s}id" % R)][1] for s in pres.findall("p:sldIdLst/p:sldId", NS) if s.get("{%s}id" % R) in prels]
    masters, slides = {}, []
    for i, part in enumerate(order, 1):
        slides.append(Slide(pkg, part, i, masters, pres_default))
    F, info = [], []
    english = any(LATIN_WORD.search(s["text"]) for sl in slides for s in sl.shapes)

    # 2. latinLnBrk on slides, layouts, masters and presentation defaults.
    brk_sev = "ERROR" if english else "WARN"
    for sl in slides:
        for s in sl.shapes:
            if s["breaks"]:
                F.append((sl.num, brk_sev, s["name"], "latin-break",
                          "latinLnBrk=1 on %d paragraph style(s): PowerPoint breaks English words mid-word; set it to 0" % s["breaks"]))
    other_parts = [pres_part] + sorted(n for n in pkg.names if re.match(r"ppt/(slideLayouts|slideMasters)/[^/]+\.xml$", n))
    for part in other_parts:
        for ctx, n in sorted(part_contexts(pkg.xml(part)).items()):
            F.append((0, brk_sev, "", "latin-break", "%s %s: latinLnBrk=1 on %d level(s); every slide using it inherits mid-word "
                                                      "breaks; set it to 0" % (part, ctx, n)))

    # 1 and 6. East Asian font resolution.
    resolved = Counter()
    for sl in slides:
        latin = Counter()
        latin_shapes = []
        for s in sl.shapes:
            if s["ea_missing"]:
                text, chain, stop = s["ea_missing"][0]
                F.append((sl.num, "ERROR", s["name"], "ea-missing",
                          "%d CJK run(s) with no East Asian font, e.g. %s; looked at %s; stopped at %s. PowerPoint picks the OS "
                          "default font" % (len(s["ea_missing"]), snip(text), chain, stop)))
            for found, stop in s.get("ea_ok", []):
                resolved[(stop.split(" (via")[0], found)] += 1
            if s["ea_latin"]:
                latin.update(s["ea_latin"])
                latin_shapes.append(s["name"])
        if latin:
            F.append((sl.num, "WARN", "", "ea-latin-face",
                      "%d CJK run(s) whose East Asian font is a Latin face (%s) in %s: PowerPoint substitutes a system font per glyph"
                      % (sum(latin.values()), ", ".join("%s x%d" % kv for kv in latin.most_common()),
                         ", ".join('"%s"' % n for n in latin_shapes[:3]) + (" ..." if len(latin_shapes) > 3 else ""))))
    if resolved:
        info.append("CJK runs with an East Asian font: " + "; ".join(
            "%d at %s (%s)" % (n, where, f) for (where, f), n in resolved.most_common(6)))

    # 4. Geometry against the slide and the margin.
    m = (margin_px or 0) * EMU_PX
    for sl in slides:
        for s in sl.shapes:
            b = s["box"]
            if b is None:
                continue
            over = [(k, lbl, d) for k, (lbl, d) in enumerate((("left", -b[0]), ("top", -b[1]), ("right", b[2] - W),
                                                              ("bottom", b[3] - H))) if d > TOL]
            if over:
                where = ", ".join("%s by %d px" % (lbl, round(d / EMU_PX)) for _, lbl, d in over)
                if b[2] <= 0 or b[3] <= 0 or b[0] >= W or b[1] >= H:
                    F.append((sl.num, "WARN", s["name"], "off-slide", "box lies entirely off the slide (%s); nothing of it shows, "
                              "delete it at the source" % where))
                elif s["text"] and any(d > s["inset"][k] + TOL for k, _, d in over):
                    F.append((sl.num, "ERROR", s["name"], "off-slide", "text box crosses the slide edge past its inner padding "
                              "(%s), so text can be cut off: %s" % (where, snip(s["text"]))))
                elif s["text"]:
                    F.append((sl.num, "WARN", s["name"], "off-slide", "text box crosses the slide edge (%s), within its inner "
                              "padding: %s" % (where, snip(s["text"]))))
                else:
                    F.append((sl.num, "WARN", s["name"], "off-slide", "%s crosses the slide edge (%s)" % (s["kind"], where)))
            elif m and s["text"]:
                inside = [(lbl, d) for lbl, d in (("left", m - b[0]), ("top", m - b[1]), ("right", b[2] - (W - m)),
                                                  ("bottom", b[3] - (H - m))) if d > TOL]
                if inside:
                    F.append((sl.num, "WARN", s["name"], "off-margin", "text box crosses the %g px margin (%s)" % (
                        margin_px, ", ".join("%s by %d px" % (lbl, round(d / EMU_PX)) for lbl, d in inside))))

    # 5. Text left under cover-ups, raster under near-white patches, hidden shapes holding text.
    for sl in slides:
        sh = sl.shapes
        for i, t in enumerate(sh):
            if t["hidden"] and t["text"]:
                F.append((sl.num, "WARN", t["name"], "hidden-text", "hidden shape still holds text %s" % snip(t["text"])))
            if not t["text"] or t["hidden"] or not t["box"] or not area(t["box"]):
                continue
            for c in sh[i + 1:]:
                if c["hidden"] or not c["opaque"] or not c["rectish"] or not c["box"]:
                    continue
                share = overlap(t["box"], c["box"]) / area(t["box"])
                if near_white(c["rgb"]) and share >= 0.5:
                    F.append((sl.num, "WARN", t["name"], "near-white-cover", "text %s sits %d%% under near-white #%s shape \"%s\"; "
                              "delete the stale text at the source" % (snip(t["text"]), round(share * 100), c["rgb"], c["name"])))
                    break
                if contains(c["box"], t["box"]):
                    F.append((sl.num, "WARN", t["name"], "covered-text", "text %s is fully covered by later opaque %s \"%s\""
                              % (snip(t["text"]), c["kind"], c["name"])))
                    break
        for j, c in enumerate(sh):
            if (c["kind"] == "sp" and c["opaque"] and c["rectish"] and not c["text"] and not c["hidden"] and c["box"]
                    and area(c["box"]) and near_white(c["rgb"]) and c["rgb"] != "FFFFFF"):
                pic = next((p for p in sh[:j] if p["kind"] == "pic" and p["box"]
                            and overlap(c["box"], p["box"]) / area(c["box"]) >= 0.9), None)
                if pic:
                    F.append((sl.num, "WARN", c["name"], "near-white-cover", "near-white #%s patch on picture \"%s\": a cover-up over "
                              "raster content; crop or replace the image at the source" % (c["rgb"], pic["name"])))

    # 3. Fonts named in the deck against font files on this machine.
    named = defaultdict(set)
    for sl in slides:
        for e in sl.root.iter():
            if e.tag in ("{%s}latin" % A, "{%s}ea" % A, "{%s}cs" % A) and e.get("typeface", "")[:1] not in ("", "+"):
                named[e.get("typeface")].add(sl.num)
    for part in other_parts:
        label = "presentation defaults" if part == pres_part else part.split("/")[1]
        for e in pkg.xml(part).iter():
            if e.tag in ("{%s}latin" % A, "{%s}ea" % A, "{%s}cs" % A) and e.get("typeface", "")[:1] not in ("", "+"):
                named[e.get("typeface")].add(label)
    for ms in masters.values():
        for kind, d in ms.fonts.items():
            for slot in ("latin", "ea", "cs"):
                if d[slot]:
                    named[d[slot]].add("theme %s %s" % (kind, slot))
    for (where, f) in resolved:
        if where.startswith("theme"):
            named[f].add(where)
    dirs, files = font_files()
    if not dirs:
        info.append("font check skipped: no readable font directories selected; set DECK_FONT_DIRS to check installed font files")
    else:
        ok = []
        for fam in sorted(named):
            where = sorted(w for w in named[fam] if not isinstance(w, int))
            used = "; ".join(filter(None, ["slides " + pages(named[fam]) if any(isinstance(w, int) for w in named[fam]) else ""] + where))
            hits = match_font(fam, files)
            base = WEIGHT_TAIL.sub("", fam)
            base_hits = match_font(base, files) if not hits and base and base != fam else []
            if base_hits:
                F.append((0, "WARN", "", "font-missing", "'%s' (%s): a weight named as a family; files exist only for '%s' (%s). "
                          "PowerPoint may substitute: name the base family and set the weight, or install static weights "
                          "(match is by file name)" % (fam, used, base, ", ".join(sorted(set(base_hits))[:3]))))
            elif not hits:
                F.append((0, "WARN", "", "font-missing", "'%s' (%s): no font file whose name matches it in %d font folder(s); "
                          "PowerPoint will substitute (match is by file name)" % (fam, used, len(dirs))))
            elif all(is_variable(h) for h in hits):
                F.append((0, "WARN", "", "font-variable", "'%s' (%s): only variable-font file(s) found (%s); PowerPoint may "
                          "silently replace it, install the static weights" % (fam, used, ", ".join(sorted(set(hits))[:3]))))
            else:
                ok.append(fam)
        if ok:
            info.append("fonts with a matching file (by file name): " + ", ".join(ok))
    meta = {"slides": len(slides), "W": W, "H": H, "hidden": {sl.num for sl in slides if sl.hidden}}
    return F, info, meta


def report(path, F, info, meta):
    print("deck-qa %s" % os.path.basename(path))
    print("slide size %.3f x %.3f in, %d slide(s)" % (meta["W"] / EMU_IN, meta["H"] / EMU_IN, meta["slides"]))
    for num, sev, name, code, msg in sorted(F, key=lambda f: (f[0], f[1] != "ERROR", f[3])):
        where = "deck" if num == 0 else "slide %d%s" % (num, " (hidden)" if num in meta["hidden"] else "")
        print("%-5s %s%s [%s] %s" % (sev, where, ' "%s"' % name if name else "", code, msg))
    for line in info:
        print("INFO  " + line)
    errors = sum(1 for f in F if f[1] == "ERROR")
    print("result: %d error(s), %d warning(s)" % (errors, len(F) - errors))
    return errors


SELF_TEST_PARTS = {
    "[Content_Types].xml": '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                           '<Default Extension="xml" ContentType="application/xml"/></Types>',
    "_rels/.rels": '<Relationships xmlns="{pr}"><Relationship Id="rId1" Type="{r}/officeDocument" '
                   'Target="ppt/presentation.xml"/></Relationships>',
    "ppt/presentation.xml": '<p:presentation xmlns:a="{a}" xmlns:p="{p}" xmlns:r="{r}"><p:sldIdLst>'
                            '<p:sldId id="256" r:id="rId1"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/>'
                            '<p:defaultTextStyle><a:lvl1pPr latinLnBrk="1"><a:defRPr><a:latin typeface="+mn-lt"/>'
                            '<a:ea typeface="+mn-ea"/></a:defRPr></a:lvl1pPr></p:defaultTextStyle></p:presentation>',
    "ppt/_rels/presentation.xml.rels": '<Relationships xmlns="{pr}"><Relationship Id="rId1" Type="{r}/slide" '
                                       'Target="slides/slide1.xml"/></Relationships>',
    "ppt/slides/_rels/slide1.xml.rels": '<Relationships xmlns="{pr}"><Relationship Id="rId1" Type="{r}/slideLayout" '
                                        'Target="../slideLayouts/slideLayout1.xml"/></Relationships>',
    "ppt/slideLayouts/slideLayout1.xml": '<p:sldLayout xmlns:a="{a}" xmlns:p="{p}"><p:cSld><p:spTree/></p:cSld></p:sldLayout>',
    "ppt/slideLayouts/_rels/slideLayout1.xml.rels": '<Relationships xmlns="{pr}"><Relationship Id="rId1" Type="{r}/slideMaster" '
                                                    'Target="../slideMasters/slideMaster1.xml"/></Relationships>',
    "ppt/slideMasters/slideMaster1.xml": '<p:sldMaster xmlns:a="{a}" xmlns:p="{p}"><p:cSld><p:spTree/></p:cSld>'
                                         '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2"/></p:sldMaster>',
    "ppt/slideMasters/_rels/slideMaster1.xml.rels": '<Relationships xmlns="{pr}"><Relationship Id="rId1" Type="{r}/theme" '
                                                    'Target="../theme/theme1.xml"/></Relationships>',
    "ppt/theme/theme1.xml": '<a:theme xmlns:a="{a}"><a:themeElements><a:fontScheme name="t">'
                            '<a:majorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
                            '<a:minorFont><a:latin typeface="Arial"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
                            '</a:fontScheme></a:themeElements></a:theme>',
}


def self_test():
    def sp(name, x, y, w, h, body="", fill=""):
        return ('<p:sp><p:nvSpPr><p:cNvPr id="2" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/>'
                '<a:ext cx="%d" cy="%d"/></a:xfrm><a:prstGeom prst="rect"/>%s</p:spPr>%s</p:sp>' % (name, x, y, w, h, fill, body))

    def txt(text, ea=None):
        return ('<p:txBody><a:bodyPr/><a:p><a:r><a:rPr lang="ko-KR"><a:latin typeface="Arial"/>%s</a:rPr><a:t>%s</a:t></a:r></a:p>'
                '</p:txBody>' % ('<a:ea typeface="%s"/>' % ea if ea else "", text))
    shapes = (sp("Hangul no ea", 914400, 914400, 4572000, 914400, txt("안녕하세요 world"))
              + sp("Hangul with ea", 914400, 2000000, 4572000, 914400, txt("한국어", "Apple SD Gothic Neo"))
              + sp("Hangul in Arial", 6000000, 2000000, 4572000, 914400, txt("한국어", "Arial"))
              + sp("Off slide", 10000000, 3000000, 4000000, 914400, txt("Overflow text"))
              + sp("Stale text", 914400, 4500000, 3000000, 600000, txt("Old caption"))
              + sp("Cover", 900000, 4400000, 3100000, 800000, "", '<a:solidFill><a:srgbClr val="FEFEFE"/></a:solidFill>'))
    parts = dict(SELF_TEST_PARTS)
    parts["ppt/slides/slide1.xml"] = '<p:sld xmlns:a="{a}" xmlns:p="{p}"><p:cSld><p:spTree>%s</p:spTree></p:cSld></p:sld>' % shapes
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "planted.pptx")
        with zipfile.ZipFile(path, "w") as z:
            for name, xml in parts.items():
                z.writestr(name, xml.replace("{a}", A).replace("{p}", P).replace("{r}", R).replace("{pr}", NS["pr"]))
        F, info, meta = check(path)
    got = {(f[3], f[2], f[1]) for f in F}
    assert ("ea-missing", "Hangul no ea", "ERROR") in got, F
    assert not any(f[3] == "ea-missing" and f[2] == "Hangul with ea" for f in F), F
    assert any(f[3] == "latin-break" and f[1] == "ERROR" and "presentation.xml" in f[4] for f in F), F
    assert ("off-slide", "Off slide", "ERROR") in got, F
    assert ("near-white-cover", "Stale text", "WARN") in got, F
    assert any(f[3] == "ea-latin-face" and '"Hangul in Arial"' in f[4] for f in F), F
    assert meta["slides"] == 1 and any(f[1] == "ERROR" for f in F)
    print("self-test passed: ea-missing, latin-break, off-slide, near-white-cover and ea-latin-face caught on a "
          "planted deck (%d findings)" % len(F))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("deck", nargs="?", help=".pptx file to check (never modified)")
    ap.add_argument("--margin-px", type=float, help="also warn when a text box crosses this inner margin (96 dpi px)")
    ap.add_argument("--self-test", action="store_true", help="build a planted deck in a temp dir and assert the checks catch it")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    if not a.deck:
        ap.error("give a .pptx path or --self-test")
    try:
        F, info, meta = check(a.deck, a.margin_px)
    except (OSError, zipfile.BadZipFile, ET.ParseError, ValueError, KeyError) as e:
        sys.stderr.write("deck-qa: cannot read %s: %s\n" % (a.deck, e))
        return 2
    return 1 if report(a.deck, F, info, meta) else 0


if __name__ == "__main__":
    sys.exit(main())
