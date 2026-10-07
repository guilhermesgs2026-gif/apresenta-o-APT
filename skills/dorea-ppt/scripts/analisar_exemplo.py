"""Reanalisa o vídeo do modelo Canva: quando cada região da tela aparece (início e 90%).
Uso: python analisar_exemplo.py [inicio_s] [duracao_s]   (padrão 0 e 5 = capa)
Requer ffmpeg no PATH e Pillow/numpy."""
import os,sys,subprocess,glob,tempfile
import numpy as np
from PIL import Image
here=os.path.dirname(os.path.abspath(__file__))
mp4=os.path.join(here,"..","reference","canva-exemplo","canva_ref.mp4")
ini=sys.argv[1] if len(sys.argv)>1 else "0"; dur=sys.argv[2] if len(sys.argv)>2 else "5"
tmp=tempfile.mkdtemp()
subprocess.run(["ffmpeg","-v","error","-y","-ss",ini,"-t",dur,"-i",mp4,"-vf","fps=20,scale=480:270",os.path.join(tmp,"f_%03d.png")],check=True)
R=dict(logo=(0.02,0.08,0.18,0.2),parenteses_esq=(0.06,0.3,0.2,0.75),parenteses_dir=(0.78,0.3,0.94,0.75),titulo=(0.22,0.35,0.78,0.6),textos=(0.2,0.62,0.85,0.72),objeto=(0.36,0.05,0.64,0.95))
fs=sorted(glob.glob(os.path.join(tmp,"f_*.png")))
def reg(a,x0,y0,x1,y1): return a[int(y0*270):int(y1*270),int(x0*480):int(x1*480)]
rows=[[i/20]+[reg(np.asarray(Image.open(f).convert("L")).astype(float),*R[k]).mean() for k in R] for i,f in enumerate(fs)]
final=np.array(rows[int(len(rows)*0.5):int(len(rows)*0.8)]).mean(0)
for k,name in enumerate(R,1):
    t10=next((r[0] for r in rows if r[k]>=0.1*final[k]),None); t90=next((r[0] for r in rows if r[k]>=0.9*final[k]),None)
    print(f"{name:15s} começa {t10}s | 90% em {t90}s")
