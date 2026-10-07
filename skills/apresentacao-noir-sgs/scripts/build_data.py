import json,re
raw=json.load(open("data_raw.json",encoding="utf-8"))
def num(s): return int(re.sub(r"\D","",s))
FIX={"Cabreuva":"Cabreúva","Taubate":"Taubaté","Sao Paulo":"São Paulo","Linhas De Transmissao":"Linhas de Transmissão","Linhas de Transmissao":"Linhas de Transmissão"}
def smart_title(s):
    t=" ".join(w.lower() if w.lower() in ("de","da","do","dos","das","e") else w.capitalize() for w in s.title().split())
    return FIX.get(t,t)
regs=[]
NREG=(len(raw)-2)//5
for k in range(NREG):
    b=1+k*5
    div,pan,proj,dev,mat=raw[b:b+5]
    name=smart_title(div["texts"][0].replace("REGIONAL ",""))
    t=pan["texts"]
    def after(lst,label): return lst[lst.index(label)-0+1] if False else None
    # KPI order: label,value,sub repeated
    kv={}
    for i,x in enumerate(t):
        if x in("INSPEÇÕES","INSPETORES","CONTRATADAS","PROJETOS","ITENS VERIFICADOS"): kv[x]=t[i+1]
    d=dev["texts"]; dk={}
    for i,x in enumerate(d):
        if x in("TOTAL DE DESVIOS","CRÍTICOS (RAC)","ÍNDICE DESV/INSP","CONTRATADAS","PROJETOS"): dk[x]=d[i+1]
    regs.append(dict(name=name,kpi=kv,part=pan["charts"][1],daily=pan["charts"][0],proj=proj["charts"][0],
      dkpi=dk,classif=dev["charts"][0],ddaily=dev["charts"][1],matriz=mat["tables"][0],
      slides=[b+1,b+2,b+3,b+4,b+5]))
json.dump(regs,open("data.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print(raw[0]["texts"][:12])
ti=td=0
for r in regs:
    i=num(r["kpi"]["INSPEÇÕES"]); dd=num(r["dkpi"]["TOTAL DE DESVIOS"]); ti+=i; td+=dd
    print(r["name"],r["kpi"],r["dkpi"], sum(r["daily"]["vals"]),sum(r["part"]["vals"]),sum(r["proj"]["vals"]),sum(r["classif"]["vals"]),sum(r["ddaily"]["vals"]), r["daily"]["cats"][0],r["daily"]["cats"][-1])
print(ti,td)

# meta.json (período, geração, números da capa) lido do primeiro slide e do último
cov=raw[0]["texts"]; end=raw[-1]["texts"]
import re as _re
gen=_re.search(r"gerado em (\d\d/\d\d/\d{4}) às (\d\d:\d\d)"," ".join(cov+end))
period=cov[2]; short=_re.sub(r"/20\d\d","",period)
meta=dict(period=period,period_short=short,gen_date=gen.group(1) if gen else "",gen_time=gen.group(2) if gen else "",
          n_regionais=int(cov[3]),inspecoes=int(cov[5].replace(".","")),desvios=int(cov[7].replace(".","")),contratadas=int(cov[9].replace(".","")))
json.dump(meta,open("meta.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("meta:",meta)
