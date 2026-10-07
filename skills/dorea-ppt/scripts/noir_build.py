"""deck.json -> SVGs (1280x720) no estilo noir editorial. Uso:
   python noir_build.py <deck.json> <pasta_de_trabalho>
Gera <pasta>/svg/*.svg, copia imagens usadas para <pasta>/images e grava <pasta>/roster.json.
Tipos de slide: cover, divider, content (kpis + painéis), closing. Veja SKILL.md para o esquema."""
import sys, os, json, shutil
from PIL import Image
import noir_lib as N
from noir_lib import *

SK = os.path.join(HERE, "..")
OBJ_DIR = os.path.join(SK, "assets", "objects")


def load_objects():
    p = os.path.join(OBJ_DIR, "aspects.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


class Ctx:
    def __init__(s, deck, work):
        s.deck = deck; s.meta = deck.get("meta", {}); s.work = work
        s.images = os.path.join(work, "images"); os.makedirs(s.images, exist_ok=True)
        s.objects = load_objects(); s.used = set(); s.theme = {}
        N.set_theme(s.meta.get("accent"), s.meta.get("lang"))
        s.theme.update(org=s.meta.get("org", ""), topbar=s.meta.get("topbar", s.meta.get("org", "")), footer=s.meta.get("footer", ""))
        lg = s.meta.get("logo")
        if lg and os.path.exists(lg):
            ext = os.path.splitext(lg)[1].lower() or ".png"; name = "logo" + ext
            shutil.copy(lg, os.path.join(s.images, name)); im = Image.open(lg)
            s.theme.update(logo_file=name, logo_aspect=im.width / im.height); s.used.add(name)
        s.cycle = s.meta.get("objects") or list(s.objects)[:1]
        s.ci = 0

    def obj_pair(s, key, h=560, op=0.62, fx_bounds=(530, 50), top=50):
        """Grupos hero + hero-fx (camada iridescente que some na animação). key=None -> sem objeto."""
        if not key or key not in s.objects: return []
        for suf in ("", "_fx"):
            fn = f"obj_{key}{suf}.png"
            shutil.copy(os.path.join(OBJ_DIR, f"{key}{suf}.png"), os.path.join(s.images, fn)); s.used.add(fn)
        a = s.objects[key]
        return [N.hero("hero", f"obj_{key}.png", a, 640, top, h, op, 64, 100),
                N.hero("hero-fx", f"obj_{key}_fx.png", a, 640, top, h, 0.18, fx_bounds[0], fx_bounds[1])]

    def next_obj(s, key):
        if key == "auto":
            if not s.cycle: return None
            k = s.cycle[s.ci % len(s.cycle)]; s.ci += 1; return k
        return key


def cover(c, sl, pn, total):
    title = sl["title"].upper(); size = fit_display(title, 900, (140, 120, 96, 72, 56))
    it = c.obj_pair(c.next_obj(sl.get("object", "auto")), 540, 0.62, (520, 36), 40)
    it += N.chrome(c.theme, pn, total)
    it.append(N.title_block("cover-title", 170, 470, 320, title, size, sl.get("overlay", ""), sl.get("subtitle")))
    items = sl.get("meta", [])[:4]; n = max(len(items), 1); cw = (W - 2 * M) / n
    for i, (lab, val) in enumerate(items):
        x = M + i * cw; w = cw - 30
        it.append(N.G(f"cover-meta-{i + 1}", (x, 560, w, 96), [L(x, 560, x + min(w, 230), 560, C["line"], 1), TM(x, 584, cut_px(lab.upper(), 12, w), 12, C["txt2"]),
                     TD(x, 636, cut_px(str(val), 26, w, "OpenSauce-Regular"), 26, C["acc"] if i == 2 else C["txt"])]))
    return svg_page(it, "cover")


def divider(c, sl, pn, total, idx, count):
    title = sl["title"].upper(); size = fit_display(title, 900, (120, 96, 72, 56))
    it = c.obj_pair(c.next_obj(sl.get("object", "auto")), 560, 0.62, (530, 50), 50)
    it += N.chrome(c.theme, pn, total, sl.get("topbar"))
    it.append(N.title_block("divider-title", 200, 520, 360, title, size, sl.get("overlay", ""), None, sl.get("kicker")))
    left = sl.get("meta_left", [])
    if left: it.append(N.G("divider-meta", (M, 590, 600, 66), [L(M, 590, M + 230, 590, C["line"], 1), TM(M, 614, left[0].upper(), 12, C["txt2"]), TD(M, 646, cut_px(str(left[1]), 26, 560, "OpenSauce-Regular"), 26)]))
    r = sl.get("meta_right", [sl.get("index_label", "SEÇÃO"), f"{idx:02d} / {count:02d}"])
    it.append(N.G("divider-index", (W - M - 200, 590, 200, 66), [L(W - M - 200, 590, W - M, 590, C["line"], 1), TM(W - M, 614, r[0].upper(), 12, C["txt2"], "end"), TD(W - M, 646, str(r[1]), 26, C["acc"], "end")]))
    return svg_page(it, "section")


def closing(c, sl, pn, total):
    title = sl.get("title", "OBRIGADO").upper(); size = fit_display(title, 900, (120, 96, 72, 56))
    it = c.obj_pair(c.next_obj(sl.get("object", "auto")), 560, 0.62, (524, 30), 50)
    it += N.chrome(c.theme, pn, total)
    it.append(N.title_block("closing-title", 200, 520, 360, title, size, sl.get("overlay", "")))
    ls = (sl.get("lines", []) + ["", "", ""])[:3]
    it.append(N.G("closing-meta", (130, 560, 1020, 100), [TM(640, 590, cut_px(ls[0], 13, 1000), 13, C["txt"], "middle"), TM(640, 616, cut_px(ls[1], 13, 1000), 13, C["txt2"], "middle"), TM(640, 642, cut_px(ls[2], 12, 1000), 12, C["txt3"], "middle")]))
    return svg_page(it, "ending")


# ---------- painéis ----------
def panel(c, p, i, x, y, w, h):
    t = p.get("type"); body = N.section_label(x, y, w, p.get("title", ""), p.get("right"))
    cy = y + 34; ch = h - 40
    if t == "line":
        body += N.linechart(x, y + 30, w, h - 30, p["cats"], [num(v) for v in p["vals"]], p.get("hi", True), p.get("color"), sub_labels=p.get("sub_labels"))
    elif t == "bars":
        n = len(p["cats"]); mx = max(n, 1)
        body += N.lollipop(x, cy, w, min(ch, 34 * mx), p["cats"], [num(v) for v in p["vals"]], p.get("leader", True), p.get("color"))
    elif t == "donut":
        parts = p["parts"]; pal = [C["acc"], C["txt"], "#8A8A8A", "#555555", "#B5B5B5", "#3A3A3A"]
        parts = [(a[0], num(a[1]), a[2] if len(a) > 2 else pal[k % len(pal)]) for k, a in enumerate(parts)]
        r = max(50, min(110, (ch - 20) / 2.2)); cx = x + r + 20; cyy = cy + ch / 2
        body += N.donut(cx, cyy, r, parts, 10); tot = sum(a[1] for a in parts) or 1
        body += [TD(cx, cyy + 14, fmt(tot), 40, None, "middle")]
        lx = cx + r + 40; ly = cyy - (len(parts) * 40) / 2 + 24
        for lab, v, col in parts:
            body += [DOT(lx, ly - 5, 5, col), TM(lx + 14, ly, cut_px(str(lab).upper(), 13, w - (lx - x) - 20), 13, C["txt"]), TM(lx + 14, ly + 20, f"{fmt(v)} · {pct(100 * v / tot, 0)}", 12, C["txt2"])]
            ly += 40
    elif t == "table":
        body += N.table(x, cy - 4, w, ch + 4, p["headers"], p["rows"], p.get("colw"), p.get("status"))
    elif t == "bullets":
        items = p["items"]; avail = ch
        per = min(76, avail / max(len(items), 1)); yy = cy + 34
        for k, it_ in enumerate(items):
            lines = wrap_px(it_, 18, w - 56, maxlines=max(1, int((per - 16) // 24)))
            body += [L(x, yy - 24, x + w, yy - 24, C["line2"], 1), TM(x, yy + 2, f"{k + 1:02d}", 13, C["acc"]), TL(x + 44, yy, lines, 18, C["txt"], 24, BODY)]
            yy += per
    elif t == "text":
        lines = wrap_px(p["body"], 18, w, maxlines=max(1, int((ch - 10) // 26)))
        body.append(TL(x, cy + 26, lines, 18, C["txt"], 26, BODY))
    elif t == "stat":
        body += [TD(x, cy + 80, str(p["value"]), 64, C["acc"] if p.get("hl", True) else C["txt"]), TM(x, cy + 112, cut_px(p.get("label", "").upper(), 13, w), 13, C["txt2"])]
        if p.get("sub"): body.append(TM(x, cy + 136, cut_px(p["sub"], 12, w), 12, C["txt3"]))
    elif t == "image":
        src = p["src"]; name = f"img_{i}_{os.path.basename(src)}"
        shutil.copy(src, os.path.join(c.images, name)); c.used.add(name); im = Image.open(src)
        a = im.width / im.height; iw = min(w, ch * a); ih = iw / a
        body.append(f'<image href="../images/{name}" x="{f1(x + (w - iw) / 2)}" y="{f1(cy + (ch - ih) / 2)}" width="{f1(iw)}" height="{f1(ih)}" preserveAspectRatio="xMidYMid meet"/>')
        if p.get("caption"): body.append(TM(x, y + h - 2, cut_px(p["caption"].upper(), 12, w), 12, C["txt3"]))
    return N.G(f"panel-{i}", (x, y, w, h), body)


def content(c, sl, pn, total):
    it = N.chrome(c.theme, pn, total, sl.get("topbar"))
    hd, yh = N.header(sl["title"], sl.get("kicker"), sl.get("subtitle")); it.append(hd)
    y = yh + 12
    k = sl.get("kpis", [])[:5]
    if k:
        n = len(k); cw = (W - 2 * M - (n - 1) * 24) / n
        for i, d in enumerate(k):
            it.append(N.kpi(f"kpi-{i + 1}", M + i * (cw + 24), y, cw, d["label"], d["value"], d.get("sub", ""), d.get("hl", i == 0), 64, 140))
        y += 156
    ps = sl.get("panels", [])[:3]
    if ps:
        n = len(ps); gap = 40; ws = [p.get("weight", 1) for p in ps]; tot = sum(ws)
        avail = W - 2 * M - gap * (n - 1); x = M; ph = 650 - y
        for i, p in enumerate(ps):
            w = avail * ws[i] / tot
            it.append(panel(c, p, i + 1, x, y, w, ph)); x += w + gap
    return svg_page(it, "content")


def build(deck, work, outsvg=None):
    c = Ctx(deck, work); outsvg = outsvg or os.path.join(work, "svg"); os.makedirs(outsvg, exist_ok=True)
    for f in os.listdir(outsvg):
        if f.endswith(".svg"): os.remove(os.path.join(outsvg, f))
    sl = deck["slides"]; total = len(sl); roster = []
    divs = [s for s in sl if s["type"] == "divider"]; di = 0
    for n, s in enumerate(sl, 1):
        t = s["type"]
        if t == "cover": svg = cover(c, s, n, total)
        elif t == "divider": di += 1; svg = divider(c, s, n, total, di, len(divs))
        elif t == "closing": svg = closing(c, s, n, total)
        else: svg = content(c, s, n, total)
        fn = f"{n:02d}_{t}.svg"; open(os.path.join(outsvg, fn), "w", encoding="utf-8").write(svg)
        roster.append([n, fn, s.get("title", t)])
    json.dump(dict(roster=roster, used=sorted(c.used), theme=c.theme, accent=N.C["acc"], objects=sorted(c.used)), open(os.path.join(work, "roster.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return roster, c


if __name__ == "__main__":
    deck = json.load(open(sys.argv[1], encoding="utf-8")); work = sys.argv[2]
    r, c = build(deck, work); print(len(r), "slides ->", os.path.join(work, "svg"))
