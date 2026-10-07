"""Prepara o logo para fundo preto: remove fundo uniforme (branco/preto/cor) e, com --white, converte as partes
sem cor (cinza/preto) para branco, mantendo cores saturadas (ex.: laranja, vermelho).
Uso: python prepare_logo.py <logo_entrada> <logo_saida.png> [--white]
Imprime a cor de acento sugerida (a cor saturada mais frequente), para usar em meta.accent."""
import sys, colorsys
import numpy as np
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]; white = "--white" in sys.argv
im = Image.open(src).convert("RGBA"); a = np.asarray(im).astype(float)
rgb = a[..., :3]; alpha = a[..., 3]
if alpha.min() > 250:   # sem transparência: remover o fundo (cor dos 4 cantos)
    corners = np.array([rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]]); bg = np.median(corners, axis=0)
    dist = np.linalg.norm(rgb - bg, axis=-1); alpha = np.clip((dist - 18) / 60, 0, 1) * 255
mx = rgb.max(-1); mn = rgb.min(-1); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
if white:
    gray = sat < 0.28
    rgb = np.where(gray[..., None], 255.0, rgb)
out = np.dstack([rgb, alpha]).astype(np.uint8)
ys, xs = np.where(out[..., 3] > 10)
if len(ys): out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
Image.fromarray(out, "RGBA").save(dst)
col = out[..., :3][(out[..., 3] > 200) & (sat[ys.min():ys.max() + 1, xs.min():xs.max() + 1] > 0.5)] if len(ys) else np.zeros((0, 3))
if len(col):
    q = (col // 32).astype(int); keys, cnt = np.unique(q, axis=0, return_counts=True); k = keys[cnt.argmax()] * 32 + 16
    print("acento sugerido: #%02X%02X%02X" % tuple(int(v) for v in k))
print("logo salvo:", dst, Image.open(dst).size)
