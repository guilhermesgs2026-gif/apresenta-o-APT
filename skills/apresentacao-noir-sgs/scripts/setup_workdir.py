"""Cria a pasta de trabalho: <dest>/gen (scripts), <dest>/assets (fontes, objetos 3D, logo), <dest>/images.
Uso: python setup_workdir.py C:/Users/<voce>/Documents/<nome-do-deck>"""
import sys,os,shutil,glob
here=os.path.dirname(os.path.abspath(__file__)); skill=os.path.dirname(here); dest=sys.argv[1]
for sub in ("gen","assets","images"): os.makedirs(os.path.join(dest,sub),exist_ok=True)
for f in glob.glob(os.path.join(here,"*.py"))+glob.glob(os.path.join(here,"*.sh")):
    if os.path.basename(f)!="setup_workdir.py": shutil.copy(f,os.path.join(dest,"gen"))
shutil.copytree(os.path.join(skill,"assets"),os.path.join(dest,"assets"),dirs_exist_ok=True)
for f in glob.glob(os.path.join(skill,"assets","hero_*.png"))+[os.path.join(skill,"assets","sgs_logo.png")]:
    shutil.copy(f,os.path.join(dest,"images"))
shutil.copy(os.path.join(skill,"assets","example_data.json"),os.path.join(dest,"data.json"))
print("pronto:",dest)
