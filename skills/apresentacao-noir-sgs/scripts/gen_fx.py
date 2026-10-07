import numpy as np, colorsys
from PIL import Image
import os
A=os.path.join(os.path.dirname(__file__),"..","assets"); I=os.path.join(os.path.dirname(__file__),"..","images")
def hsv2rgb(h,s,v):
    h=h%1.0; i=(h*6).astype(int)%6; f=h*6-np.floor(h*6)
    p=v*(1-s); q=v*(1-s*f); t=v*(1-s*(1-f))
    r=np.choose(i,[v,q,p,p,t,v]); g=np.choose(i,[t,v,v,q,p,p]); b=np.choose(i,[p,p,t,v,v,q])
    return r,g,b
for k in ("tower","trafo","breaker","insul","hat"):
    im=Image.open(f"{A}/hero_{k}.png").convert("RGBA"); a=np.asarray(im).astype(float)/255
    rgb=a[...,:3]; al=a[...,3]; L=rgb.mean(-1)
    h,w=L.shape; yy,xx=np.mgrid[0:h,0:w]
    hue=(xx/w*0.85+yy/h*0.55+L*0.6)%1.0
    sat=np.clip(0.15+0.95*np.clip((L-0.12)/0.5,0,1),0,0.85)
    val=np.clip(L*1.55+0.06,0,1)
    r,g,b=hsv2rgb(hue,sat,val)
    # chromatic split
    sh=max(2,w//160)
    r=np.roll(r,sh,axis=1); b=np.roll(b,-sh,axis=1)
    out=np.dstack([r,g,b,al]); out[...,3]=np.clip(al*1.0,0,1)
    img=Image.fromarray((out*255).astype(np.uint8),"RGBA")
    img.save(f"{A}/hero_{k}_fx.png"); img.save(f"{I}/hero_{k}_fx.png"); print(k,"fx")
