"""Biblioteca do estilo noir editorial (modelo Canva): primitivas SVG, gráficos de linha fina, medição de texto.
Tudo genérico: o tema (acento, logo, rodapé) vem do deck.json. Tamanhos de fonte usados (declarados no spec_lock):
title 40, body 18, annotation 13, kpi 64, meta 26, display 120/96/72/56, hero 140, paren 220."""
import math, json, os, datetime
from PIL import ImageFont

W, H, M = 1280, 720, 56
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "assets", "fonts")
C = dict(bg="#000000", txt="#FFFFFF", txt2="#9A9A9A", txt3="#5C5C5C", line="#2A2A2A", line2="#161616",
         acc="#F7941D", green="#34D399", yel="#FACC15", org="#FB923C", red="#F43F5E")
TITLE = "Open Sauce"; BODY = "Open Sauce"; MONO = "Space Mono"; LIGHT = "Open Sauce Light"
LANG = {"dec": ",", "grp": "."}   # pt-BR por padrão; deck.json meta.lang = "en" troca


def set_theme(accent=None, lang=None):
    if accent: C["acc"] = accent
    if lang and lang.lower().startswith("en"): LANG.update(dec=".", grp=",")


# ---------- utilidades ----------
def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def f1(v): return ("%.1f" % v).rstrip("0").rstrip(".")
def fmt(n):
    if isinstance(n, str): return n
    if abs(n - round(n)) < 1e-9: return f"{int(round(n)):,}".replace(",", LANG["grp"])
    return f"{n:,.1f}".replace(",", "§").replace(".", LANG["dec"]).replace("§", LANG["grp"])
def pct(v, d=1): return (f"{v:.{d}f}").replace(".", LANG["dec"]) + "%"
def num(s):
    s = str(s).replace("%", "").replace("R$", "").replace("$", "").strip()
    if LANG["dec"] == ",": s = s.replace(".", "").replace(",", ".")
    else: s = s.replace(",", "")
    try: return float(s)
    except ValueError: return 0.0

_F = {}
def _font(name):
    if name not in _F: _F[name] = ImageFont.truetype(os.path.join(FONT_DIR, name + ".ttf"), 200)
    return _F[name]
def tw(text, size, font="OpenSauce-Regular"):
    return _font(font).getlength(text) * size / 200
def twm(text, size): return tw(text, size, "SpaceMono-Regular")
def wrap_px(text, size, maxw, font="OpenSauce-Regular", maxlines=99):
    lines, cur = [], ""
    for w in str(text).split():
        t = (cur + " " + w).strip()
        if tw(t, size, font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines]; lines[-1] = lines[-1].rstrip(" .,;") + "…"
    return lines
def cut_px(text, size, maxw, font="SpaceMono-Regular"):
    if tw(text, size, font) <= maxw: return text
    while text and tw(text + "…", size, font) > maxw: text = text[:-1]
    return text.rstrip() + "…"
def fit_display(text, maxw=1000, sizes=(120, 96, 72, 56)):
    for s in sizes:
        if tw(text, s) <= maxw: return s
    return sizes[-1]
def sem(v, th=(15, 30)):
    if v <= 0: return C["green"]
    if v <= th[0]: return C["yel"]
    if v <= th[1]: return C["org"]
    return C["red"]


# ---------- primitivas SVG ----------
def T(x, y, s, size, fill=None, anchor="start", fam=None):
    fill = fill or C["txt"]
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    fm = f' font-family="{fam}"' if fam else ""
    return f'<text x="{f1(x)}" y="{f1(y)}" font-size="{size}" fill="{fill}"{a}{fm}>{esc(s)}</text>'
def TD(x, y, s, size, fill=None, anchor="start"): return T(x, y, s, size, fill, anchor, TITLE)
def TM(x, y, s, size, fill=None, anchor="start"): return T(x, y, s, size, fill or C["txt2"], anchor, MONO)
def TL(x, y, lines, size, fill=None, lh=None, fam=None, anchor="start"):
    fill = fill or C["txt"]; lh = lh or round(size * 1.3)
    fm = f' font-family="{fam}"' if fam else ""
    an = f' text-anchor="{anchor}"' if anchor != "start" else ""
    sp = "".join(f'<tspan x="{f1(x)}" dy="{0 if i == 0 else lh}">{esc(l)}</tspan>' for i, l in enumerate(lines))
    return f'<text x="{f1(x)}" y="{f1(y)}" font-size="{size}" fill="{fill}"{an}{fm}>{sp}</text>'
def R(x, y, w, h, fill, rx=0, stroke=None, sw=1, op=None):
    s = f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" fill="{fill}"'
    if rx: s += f' rx="{rx}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None: s += f' fill-opacity="{op}"'
    return s + "/>"
def L(x1, y1, x2, y2, stroke=None, sw=1):
    return f'<line x1="{f1(x1)}" y1="{f1(y1)}" x2="{f1(x2)}" y2="{f1(y2)}" stroke="{stroke or C["line"]}" stroke-width="{sw}"/>'
def DOT(x, y, r, fill): return f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="{fill}"/>'
def G(id, bounds, body, extra=""):
    x, y, w, h = bounds
    return f'<g id="{id}" data-pptx-bounds="{f1(x)} {f1(y)} {f1(w)} {f1(h)}"{extra}>\n' + "\n".join(body if isinstance(body, list) else [body]) + "\n</g>"
def svg_page(items, role="content"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{BODY}" data-pptx-page-role="{role}">\n'
            f'<rect id="bg" x="0" y="0" width="{W}" height="{H}" fill="{C["bg"]}" data-pptx-role="background"/>\n' + "\n".join(items) + "\n</svg>\n")


# ---------- elementos de página ----------
def hero(id, image, aspect, cx=640, top=50, h=560, op=0.62, by=64, bh=100):
    """Objeto 3D parado atrás do título (grupo com bounds só na faixa superior, para não colidir com o título)."""
    if aspect > 1.5: w = 860; hh = w / aspect; t = top + (h - hh) / 2   # objeto largo (carro)
    elif aspect > 1: w = h; hh = h / aspect; t = top + (h - hh) / 2
    else: w = h * aspect; hh = h; t = top
    img = f'<image href="../images/{image}" x="{f1(cx - w / 2)}" y="{f1(t)}" width="{f1(w)}" height="{f1(hh)}" opacity="{op}" preserveAspectRatio="xMidYMid meet"/>'
    return G(id, (cx - w / 2, by, w, bh), [img])

def logo(theme, x=M, y=24, h=40):
    """Logo (PNG sem fundo, versão clara) ou, sem logo, o nome da organização em texto."""
    if theme.get("logo_file"):
        pw = min(240, h * theme.get("logo_aspect", 2.0)); ph = h
        if theme.get("logo_aspect", 2.0) < 1.2: pw = h * theme["logo_aspect"]
        body = [f'<image href="../images/{theme["logo_file"]}" x="{f1(x)}" y="{f1(y)}" width="{f1(pw)}" height="{f1(ph)}" preserveAspectRatio="xMidYMid meet"/>']
        return G("logo", (x, y, pw, ph), body, ' data-pptx-role="logo"'), pw
    name = theme.get("org", "")
    pw = max(60, twm(name.upper(), 14) + 6)
    return G("logo", (x, y + 6, pw, 26), [TM(x, y + 26, name.upper(), 14, C["txt"])], ' data-pptx-role="logo"'), pw

def chrome(theme, pn, total, toptext=None):
    lg, pw = logo(theme)
    top_txt = toptext if toptext is not None else theme.get("topbar", "")
    top = G("topbar", (M + pw + 20, 28, W - 2 * M - pw - 20, 30), [TM(W - M, 48, cut_px(top_txt.upper(), 12, W - 2 * M - pw - 40), 12, C["txt2"], "end")], ' data-pptx-role="header"')
    foot = G("footer", (M, H - 44, W - 2 * M, 30), [TM(M, H - 24, cut_px(theme.get("footer", "").upper(), 12, 900), 12, C["txt3"]), TM(W - M, H - 24, f"{pn:02d} / {total:02d}", 12, C["txt2"], "end")], ' data-pptx-role="footer"')
    return [lg, top, foot]

def title_block(id, y0, y1, cy, big, size, overlay, subline=None, kicker=None):
    """Parênteses de texto (Open Sauce Light) colados ao título + legenda espaçada sobreposta com faixa preta."""
    cx = 640; w = tw(big, size); pf = 220; ov_sp = 14
    xl = cx - w / 2 - 16; xr = cx + w / 2 + 16
    ty = cy + size * 0.35; pb = cy + 0.30 * pf
    overlay = (overlay or "").upper()
    ow = len(overlay) * (18 * 0.6 + ov_sp) + 30
    below = ow > 0.8 * w or size < 96 or len(big) > 16   # título longo/2+ palavras: legenda vai abaixo, sem faixa
    oy = (ty + size * 0.2 + 26) if below else (ty - size * 0.16)
    b = [f'<text x="{f1(xl)}" y="{f1(pb)}" font-size="{pf}" fill="{C["txt"]}" text-anchor="end" font-family="{LIGHT}">(</text>',
         f'<text x="{f1(xr)}" y="{f1(pb)}" font-size="{pf}" fill="{C["txt"]}" font-family="{LIGHT}">)</text>',
         TD(cx, ty, big, size, None, "middle")]
    if overlay:
        if not below: b.append(R(cx - ow / 2, oy - 22, ow, 32, C["bg"]))
        b.append(f'<text x="{f1(cx + ov_sp / 2)}" y="{f1(oy)}" font-size="18" fill="{C["txt"]}" text-anchor="middle" letter-spacing="{ov_sp}">{esc(overlay)}</text>')
    if kicker: b.append(TM(cx, y0 + 34, kicker.upper(), 14, C["acc"], "middle"))
    if subline: b.append(TM(cx, y1 + 28, cut_px(subline, 13, 1000), 13, C["txt2"], "middle"))
    bx0 = max(4, min(xl - pf * 0.62 - 8, cx - ow / 2 - 24)); bx1 = min(1276, max(xr + pf * 0.62 + 8, cx + ow / 2 + 36))
    return G(id, (bx0, y0, bx1 - bx0, y1 - y0 + (40 if subline else 0)), b)

def header(title, kicker=None, sub=None):
    """Título de slide (2 linhas no máximo, Open Sauce 40). Retorna (grupo, y_final_do_cabeçalho)."""
    lines = wrap_px(title, 40, 1000, maxlines=2)
    b = []
    if kicker: b.append(TM(M, 96, kicker.upper(), 12, C["acc"]))
    b.append(TL(M, 134, lines, 40, C["txt"], 46, TITLE))
    h = 44 + 46 * len(lines)
    if sub: b.append(TM(M, 134 + 46 * (len(lines) - 1) + 28, cut_px(sub, 13, 1000), 13, C["txt2"])); h += 26
    return G("header", (M, 84, W - 2 * M, h), b), 84 + h

def section_label(x, y, w, label, right=None):
    b = [L(x, y, x + w, y, C["line"], 1), TM(x, y + 22, cut_px(label.upper(), 12, w * 0.7), 12, C["txt2"])]
    if right: b.append(TM(x + w, y + 22, cut_px(right.upper(), 12, w * 0.45), 12, C["txt3"], "end"))
    return b

def kpi(id, x, y, w, label, value, sub="", hl=False, vs=64, h=150):
    value = str(value)
    while tw(value, vs) > w - 8 and vs > 40: vs -= 8
    b = [L(x, y, x + w, y, C["line"], 1), TM(x, y + 24, cut_px(label.upper(), 12, w), 12, C["txt2"]),
         TD(x, y + 104, value, vs, C["acc"] if hl else C["txt"]), TM(x, y + 130, cut_px(sub, 12, w), 12, C["txt3"])]
    return G(id, (x, y, w, h), b)


# ---------- gráficos de linha fina ----------
def lollipop(x, y, w, h, cats, vals, leader=True, color=None, vfmt=fmt):
    n = len(cats); mx = max(vals) if vals else 1; rh = h / max(n, 1); out = []
    lw = min(240, max(70, max(twm(str(c).upper(), 13) for c in cats) + 14)); bx = x + lw + 18; bw = w - lw - 18 - 70
    for i, (c, v) in enumerate(zip(cats, vals)):
        cy = y + i * rh + rh / 2
        out.append(TM(x + lw, cy + 4.5, cut_px(str(c).upper(), 13, lw), 13, "#D0D0D0", "end"))
        Ln = max(4, bw * v / mx) if mx else 4; col = C["acc"] if (leader and i == 0) else (color or C["txt"])
        out += [L(bx, cy, bx + Ln, cy, col, 2), DOT(bx + Ln, cy, 5, col), TM(bx + Ln + 14, cy + 5, vfmt(v), 14, col if (leader and i == 0) else C["txt"])]
    return out

def linechart(x, y, w, h, cats, vals, hi=True, color=None, vfmt=fmt, sub_labels=None):
    n = len(cats); mx = max(vals) if vals else 1; sub = bool(sub_labels)
    base = y + h - (40 if sub else 24); top = y + 30; out = []
    for k in range(4):
        gy = base - (base - top) * k / 3
        out.append(L(x, gy, x + w, gy, C["line2"] if k else C["line"], 1))
    slot = w / n; pts = []
    for i, v in enumerate(vals):
        pts.append((x + slot * i + slot / 2, base - (base - top) * v / mx if mx else base))
    out.append(f'<path d="M{" L".join(f"{f1(a)} {f1(b)}" for a, b in pts)}" fill="none" stroke="{color or C["txt"]}" stroke-width="2.5" stroke-linejoin="round"/>')
    mi = vals.index(mx) if hi and vals else -1
    for i, ((cx, cy), v, c) in enumerate(zip(pts, vals, cats)):
        col = C["acc"] if i == mi else (color or C["txt"])
        out += [L(cx, cy, cx, base, C["line"], 1), DOT(cx, cy, 5, col),
                TM(cx, cy - 14, vfmt(v), 14, col if i == mi else C["txt"], "middle"),
                TM(cx, base + 20, cut_px(str(c), 12, slot - 4), 12, C["txt2"], "middle")]
        if sub: out.append(TM(cx, base + 36, sub_labels[i], 12, C["txt3"], "middle"))
    return out

def donut(cx, cy, r, parts, sw=10):
    tot = sum(p[1] for p in parts); out = []
    if tot == 0:
        return [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["line"]}" stroke-width="{sw}"/>']
    a0 = -math.pi / 2
    for lab, v, col in parts:
        if v <= 0: continue
        a1 = a0 + 2 * math.pi * v / tot
        if v == tot: out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        else:
            g = 0.03; s, e = a0 + g, a1 - g
            x0, y0 = cx + r * math.cos(s), cy + r * math.sin(s); x1, y1 = cx + r * math.cos(e), cy + r * math.sin(e)
            out.append(f'<path d="M{f1(x0)} {f1(y0)} A{r} {r} 0 {1 if (e - s) > math.pi else 0} 1 {f1(x1)} {f1(y1)}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        a0 = a1
    return out

def table(x, y, w, h, headers, rows, colw=None, status=None):
    n = len(rows); rh = min(44, (h - 30) / max(n, 1)); out = []
    if not colw:   # larguras pelo conteúdo (Space Mono é monoespaçada)
        colw = [max(twm(str(headers[j]).upper(), 12), *[twm(str(r[j]).upper(), 14) for r in rows]) + 28 for j in range(len(headers))]
    tot = sum(colw); cws = [w * c / tot for c in colw]
    hx = []; cx = x
    for c in cws: hx.append(cx); cx += c
    al = ["start"] + ["end"] * (len(headers) - 1)
    for j, hd in enumerate(headers):
        out.append(TM(hx[j] if al[j] == "start" else hx[j] + cws[j], y + 16, cut_px(str(hd).upper(), 12, cws[j] - 6), 12, C["txt2"], al[j]))
    out.append(L(x, y + 26, x + w, y + 26, C["txt3"], 1))
    sc = status.get("col") if status else None
    for i, r in enumerate(rows):
        yy = y + 30 + i * rh; cy = yy + rh / 2
        out.append(L(x, yy + rh, x + w, yy + rh, C["line2"], 1))
        for j, v in enumerate(r):
            tx = hx[j] if al[j] == "start" else hx[j] + cws[j]
            txt = cut_px(str(v).upper(), 14, cws[j] - 12)
            if sc is not None and j == sc:
                th = status.get("thresholds", (15, 30)); v_ = num(v)
                col = (C["green"] if v_ >= th[1] else C["yel"] if v_ >= th[0] else C["red"]) if status.get("good") == "high" else sem(v_, th)
                out += [DOT(tx - twm(txt, 14) - 14, cy, 5, col), TM(tx, cy + 5, txt, 14, col, "end")]
            else:
                out.append(TM(tx, cy + 5, txt, 14, C["txt"] if j == 0 else "#B5B5B5", al[j]))
    return out
