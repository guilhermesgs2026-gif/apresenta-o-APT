"""Transforma os PNG 1920x1080 exportados do Canva (objeto 3D sobre preto) em hero_<nome>.png com alpha,
recortado, com bordas suavizadas, e gera aspects.json. Uso:
  python process_canva_images.py <pasta_com_pngs> <pasta_assets> <pasta_images> tower=tower.png trafo=trafo.png ..."""
import sys,json,os
import numpy as np
from PIL import Image
src,assets,images=sys.argv[1:4]; pairs=[a.split("=") for a in sys.argv[4:]]
asp=json.load(open(os.path.join(assets,"aspects.json"))) if os.path.exists(os.path.join(assets,"aspects.json")) else {}
for key,fn in pairs:
    a=np.asarray(Image.open(os.path.join(src,fn)).convert("RGB")).astype(float); m=a.max(-1)/255
    ys,xs=np.where(m>0.07); H,W=m.shape; pad=40
    x0,x1,y0,y1=max(0,xs.min()-pad),min(W-1,xs.max()+pad),max(0,ys.min()-pad),min(H-1,ys.max()+pad)
    a=a[y0:y1+1,x0:x1+1]; m=m[y0:y1+1,x0:x1+1]; al=np.clip((m-0.02)*1.35,0,1); h,w=al.shape
    fy=np.ones(h); fx=np.ones(w); ey=int(h*0.10); ex=int(w*0.05)
    fy[-ey:]=np.linspace(1,0,ey); fy[:ey]=np.minimum(fy[:ey],np.linspace(0,1,ey)); fx[:ex]=np.linspace(0,1,ex); fx[-ex:]=np.linspace(1,0,ex)
    al=al*fy[:,None]*fx[None,:]
    rgb=np.where(al[...,None]>0.004,np.clip(a/np.maximum(al[...,None],1e-3),0,255),0)
    img=Image.fromarray(np.dstack([rgb,al*255]).astype(np.uint8),"RGBA")
    if img.height>1000: img=img.resize((round(img.width*1000/img.height),1000),Image.LANCZOS)
    img.save(os.path.join(assets,f"hero_{key}.png")); img.save(os.path.join(images,f"hero_{key}.png")); asp[key]=round(img.width/img.height,4); print(key,img.size)
json.dump(asp,open(os.path.join(assets,"aspects.json"),"w"))
print("depois rode gen_fx.py (camada iridescente) e ajuste IMG/ASP em nl.py se criar nomes novos")
