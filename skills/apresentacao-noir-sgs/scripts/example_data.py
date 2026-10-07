"""Dados do exemplo (relatório semanal SGI SGS Enger x ISA Energia). Troque este módulo ao usar outro relatório:
precisa expor D (lista de regionais), PER, TI_, TD, TA, TF, TIT, IDX, dates, dvals, cons, att."""
import json,os
from nl import num,pdate
D=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","example_data.json"),encoding="utf-8"))
for r in D:
    if r["name"].startswith("Linhas"): r["name"]="Linhas de Transmissão"
PER="28/09/2026 a 04/10/2026"
for r in D:
    r["ins"]=int(num(r["kpi"]["INSPEÇÕES"])); r["dev"]=int(num(r["dkpi"]["TOTAL DE DESVIOS"]))
    r["idx"]=100*r["dev"]/r["ins"]; r["itens"]=int(num(r["kpi"]["ITENS VERIFICADOS"]))
    cl=dict(zip(r["classif"]["cats"],[int(v) for v in r["classif"]["vals"]]))
    r["aberto"]=cl.get("Aberto",0); r["fechado"]=cl.get("Fechado",0)
TI_=sum(r["ins"] for r in D); TD=sum(r["dev"] for r in D); TIT=sum(r["itens"] for r in D)
TA=sum(r["aberto"] for r in D); TF=sum(r["fechado"] for r in D)
assert TI_==537 and TD==45 and TA+TF==45
IDX=100*TD/TI_
daily={}
for r in D:
    for c,v in zip(r["daily"]["cats"],r["daily"]["vals"]): daily[c]=daily.get(c,0)+int(v)
dates=sorted(daily,key=pdate); dvals=[daily[d] for d in dates]
# contratadas consolidadas (a partir das matrizes: >=3 inspecoes por regional)
cons={}
for r in D:
    for row in r["matriz"][1:]:
        nm=row[0]; ins=int(num(row[2])); itn=int(num(row[3])); dv=int(num(row[4])); cr=int(num(row[5]))
        c=cons.setdefault(nm,dict(nm=nm,reg=[],ins=0,itens=0,dev=0,crit=0))
        c["reg"].append(r["name"]); c["ins"]+=ins; c["itens"]+=itn; c["dev"]+=dv; c["crit"]+=cr
for c in cons.values(): c["idx"]=100*c["dev"]/c["ins"] if c["ins"] else 0
att=[]  # linhas regional x contratada > 30%
for r in D:
    for row in r["matriz"][1:]:
        v=num(row[6])
        if v>30: att.append(dict(nm=row[0],reg=r["name"],ins=int(num(row[2])),dev=int(num(row[4])),idx=v,idxs=row[6]))
att.sort(key=lambda a:-a["idx"])

