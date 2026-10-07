"""Transforma um PNG exportado do Canva (objeto 3D sobre preto, ex.: 1920x1080) em objeto da biblioteca:
 assets/objects/<nome>.png     (recortado, alpha pela luminância, bordas suavizadas)
 assets/objects/<nome>_fx.png  (camada iridescente de entrada: matiz + separação cromática)
 assets/objects/aspects.json   (largura/altura)
Uso: python make_object.py <png> <nome>   (pode repetir: <png1> <nome1> <png2> <nome2> ...)"""
import sys, os, json
import numpy as np
from PIL import Image

OBJ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "objects")


def hsv2rgb(h, s, v):
    h = h % 1.0; i = (h * 6).astype(int) % 6; f = h * 6 - np.floor(h * 6)
    p = v * (1 - s); q = v * (1 - s * f); t = v * (1 - s * (1 - f))
    return (np.choose(i, [v, q, p, p, t, v]), np.choose(i, [t, v, v, q, p, p]), np.choose(i, [p, p, t, v, v, q]))


def process(src, name):
    os.makedirs(OBJ, exist_ok=True)
    a = np.asarray(Image.open(src).convert("RGB")).astype(float); m = a.max(-1) / 255
    ys, xs = np.where(m > 0.07); H, W = m.shape; pad = 40
    x0, x1, y0, y1 = max(0, xs.min() - pad), min(W - 1, xs.max() + pad), max(0, ys.min() - pad), min(H - 1, ys.max() + pad)
    a = a[y0:y1 + 1, x0:x1 + 1]; m = m[y0:y1 + 1, x0:x1 + 1]
    al = np.clip((m - 0.02) * 1.35, 0, 1); h, w = al.shape
    fy = np.ones(h); fx = np.ones(w); ey = int(h * 0.10); ex = int(w * 0.05)
    fy[-ey:] = np.linspace(1, 0, ey); fy[:ey] = np.minimum(fy[:ey], np.linspace(0, 1, ey))
    fx[:ex] = np.linspace(0, 1, ex); fx[-ex:] = np.linspace(1, 0, ex)
    al = al * fy[:, None] * fx[None, :]
    rgb = np.where(al[..., None] > 0.004, np.clip(a / np.maximum(al[..., None], 1e-3), 0, 255), 0)
    img = Image.fromarray(np.dstack([rgb, al * 255]).astype(np.uint8), "RGBA")
    if img.height > 1000: img = img.resize((round(img.width * 1000 / img.height), 1000), Image.LANCZOS)
    if img.width > 1400: img = img.resize((1400, round(img.height * 1400 / img.width)), Image.LANCZOS)
    img.save(os.path.join(OBJ, name + ".png"))
    # camada iridescente
    f = np.asarray(img).astype(float) / 255; rgb = f[..., :3]; alp = f[..., 3]; L = rgb.mean(-1)
    hh, ww = L.shape; yy, xx = np.mgrid[0:hh, 0:ww]
    hue = (xx / ww * 0.85 + yy / hh * 0.55 + L * 0.6) % 1.0
    sat = np.clip(0.15 + 0.95 * np.clip((L - 0.12) / 0.5, 0, 1), 0, 0.85); val = np.clip(L * 1.55 + 0.06, 0, 1)
    r, g, b = hsv2rgb(hue, sat, val); sh = max(2, ww // 160); r = np.roll(r, sh, 1); b = np.roll(b, -sh, 1)
    Image.fromarray((np.dstack([r, g, b, alp]) * 255).astype(np.uint8), "RGBA").save(os.path.join(OBJ, name + "_fx.png"))
    p = os.path.join(OBJ, "aspects.json"); asp = json.load(open(p)) if os.path.exists(p) else {}
    asp[name] = round(img.width / img.height, 4); json.dump(asp, open(p, "w"), indent=1)
    print(name, img.size, "aspect", asp[name])


if __name__ == "__main__":
    args = sys.argv[1:]
    for i in range(0, len(args), 2): process(args[i], args[i + 1])
