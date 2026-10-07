import sys,subprocess,os,glob,re
src=os.path.abspath(sys.argv[1]); dst=os.path.abspath(sys.argv[2]); os.makedirs(dst,exist_ok=True)
FD=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","assets","fonts")).replace("\\","/")
css=f"""@font-face{{font-family:'Open Sauce';src:url('file:///{FD}/OpenSauce-Regular.ttf')}}
@font-face{{font-family:'Open Sauce Light';src:url('file:///{FD}/OpenSauce-Light.ttf')}}
@font-face{{font-family:'Space Mono';src:url('file:///{FD}/SpaceMono-Regular.ttf')}}
html,body{{margin:0;background:#000}} svg{{display:block;width:1280px;height:720px}}"""
edge=r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
sel=sys.argv[3:]
for f in sorted(glob.glob(os.path.join(src,"*.svg"))):
    b=os.path.basename(f)
    if sel and not any(b.startswith(s) for s in sel): continue
    t=open(f,encoding="utf-8").read(); t=re.sub(r"^<\?xml.*?\?>","",t)
    html=os.path.join(src,"_p_"+b.replace(".svg",".html"))
    open(html,"w",encoding="utf-8").write(f"<!doctype html><meta charset='utf-8'><style>{css}</style>{t}")
    out=os.path.join(dst,b.replace(".svg",".png")); ud=os.path.abspath("../.edge_ud_"+b)
    try: subprocess.run([edge,"--user-data-dir="+ud,"--headless","--disable-gpu","--hide-scrollbars","--window-size=1280,720","--virtual-time-budget=3000",f"--screenshot={out}","file:///"+html.replace("\\","/")],capture_output=True,timeout=45)
    except Exception as e: print("timeout",b)
    print(out,os.path.exists(out))
