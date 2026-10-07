import sys,os,re,json,glob
P=sys.argv[1]
slides={}
def row(eff,order,dur,delay,first=False,opts=None):
    r={"effect":eff,"order":order,"duration":dur,"trigger":"after-previous" if first else "with-previous","delay":round(delay,2)}
    if opts: r["effect_options"]=opts
    return r
for f in sorted(glob.glob(os.path.join(P,"svg_output","*.svg"))):
    stem=os.path.basename(f)[:-4]; t=open(f,encoding="utf-8").read()
    ids=re.findall(r'^<g id="([^"]+)" data-pptx-bounds',t,re.M)
    groups={}; k=0
    for gid in ids:
        if gid in ("topbar","footer","legend"): continue
        k+=1; first=(k==1)
        if gid=="logo-sgs": r=row("entrance_fade",k,0.2,0.0,first)
        elif gid=="hero": r=row("entrance_faded_zoom",k,0.5,0.35,first)
        elif gid=="hero-fx":
            groups[gid]={"effects":[row("entrance_faded_zoom",k,0.5,0.35,first),row("exit_fade",k+100,0.4,0.9,False)]}; continue
        elif gid.endswith("-title") and not gid.startswith("header"): r=row("entrance_split",k,0.3,0.3,first)
        elif gid=="header": r=row("entrance_fade",k,0.2,0.05,first)
        elif gid.startswith(("cover-meta","divider-meta","divider-index","closing-meta")): r=row("entrance_fade",k,0.2,0.5+0.08*k,first)
        elif gid.startswith(("kpi","insight","card","foco")): r=row("entrance_fade",k,0.2,0.15+0.04*k,first)
        else: r=row("entrance_wipe",k,0.25,0.3+0.05*k,first,{"direction":"right"})
        groups[gid]={"effects":[r]}
    slides[stem]={"groups":groups,"transition":{"effect":"fade","duration":0.35}}
json.dump({"version":1,"slides":slides},open(os.path.join(P,"animations.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("wrote",len(slides),"slides")
