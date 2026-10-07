import sys,os
from nl import *
import example_data as A
D=A.D; PER=A.PER; TI_=A.TI_; TDEV=A.TD; TA=A.TA; TF=A.TF; TIT=A.TIT; IDX=A.IDX; dates=A.dates; dvals=A.dvals; cons=A.cons; att=A.att
def pct0(a,b): return round(100*a/b)
def sort_desc(cats,vals):
    pairs=list(zip(cats,vals)); out=[p for p in pairs if p[0]!="Outras"]; out.sort(key=lambda p:-p[1]); out+=[p for p in pairs if p[0]=="Outras"]
    return [p[0] for p in out],[p[1] for p in out]
def cut(s,n): return s if len(s)<=n else s[:n-1]+"…"
def wrap(s,n):
    ln=[];cur=""
    for w in s.split():
        if len(cur)+len(w)+1>n: ln.append(cur); cur=w
        else: cur=(cur+" "+w).strip()
    ln.append(cur); return ln

# ---------- shared hero pages ----------
def title_block(id,y0,y1,cy,big,size,overlay,subline=None,kicker=None):
    cx=640; w=tw(big,size); pf=220; ov_sp=14
    xl=cx-w/2-16; xr=cx+w/2+16
    ty=cy+size*0.35; pb=cy+0.30*pf
    ow=len(overlay)*(18*0.6+ov_sp)+30
    below=ow>0.8*w
    oy=(ty+size*0.2+26) if below else (ty-size*0.16)
    b=[f'<text x="{f1(xl)}" y="{f1(pb)}" font-size="{pf}" fill="{C["txt"]}" text-anchor="end" font-family="{LIGHT}">(</text>',
       f'<text x="{f1(xr)}" y="{f1(pb)}" font-size="{pf}" fill="{C["txt"]}" font-family="{LIGHT}">)</text>',
       TD(cx,ty,big,size,None,"middle")]
    if not below: b.append(R(cx-ow/2,oy-22,ow,32,C["bg"]))
    b.append(f'<text x="{f1(cx+ov_sp/2)}" y="{f1(oy)}" font-size="18" fill="{C["txt"]}" text-anchor="middle" letter-spacing="{ov_sp}">{esc(overlay.upper())}</text>')
    if kicker: b.append(TM(cx,y0+34,kicker,14,C["orange"],"middle"))
    if subline: b.append(TM(cx,y1+28,subline,13,C["txt2"],"middle"))
    bx0=max(4,min(xl-pf*0.62-8,cx-ow/2-24)); bx1=min(1276,max(xr+pf*0.62+8,cx+ow/2+36))
    return G(id,(bx0,y0,bx1-bx0,y1-y0+(40 if subline else 0)),b)

def cover(deck,total):
    it=[hero_img("hero","tower",640,40,540,0.62,64,100),hero_img("hero-fx","tower_fx",640,40,540,0.18,520,36)]
    it+=chrome(1,total,"FISCALIZAÇÃO DE OBRAS ELÉTRICAS · ISA ENERGIA BRASIL","SGS ENGER ENGENHARIA · RELATÓRIO SEMANAL")
    if deck=="A":
        ov="Semanal consolidado"; sub="Relatório semanal consolidado de qualidade · inspeções e desvios"
    else:
        ov="Semanal de qualidade"; sub="Gestão de Inspeções e Desvios · todas as regionais do período"
    it.append(title_block("cover-title",170,470,320,"RELATÓRIO",140,ov,sub))
    cols=[("PERÍODO","28/09/2026 a 04/10/2026"),("REGIONAIS","06"),("INSPEÇÕES CONCLUÍDAS","537"),("DESVIOS REGISTRADOS","45")]
    xs=[M,440,640,920]
    for i,(l,v) in enumerate(cols):
        x=xs[i]
        it.append(G(f"cover-meta-{i+1}",(x,560,[360,170,250,300][i],96),[L(x,560,x+230,560,C["line"],1),TM(x,584,l,12,C["txt2"]),TD(x,636,v,26,C["orange"] if i==2 else C["txt"])]))
    return svg_page(it,"cover")

def divider(i,total_regs,name,sub,period,pn,total,keyimg):
    nm=name.upper(); size=int(min(120,900/(tw(nm,100)/100)))
    it=[hero_img("hero",keyimg,640,50,560,0.62,64,100),hero_img("hero-fx",keyimg+"_fx",640,50,560,0.18,530,50)]
    it+=chrome(pn,total,"REGIONAL "+f"{i:02d} / {total_regs:02d}","SGS ENGER ENGENHARIA · RELATÓRIO SEMANAL")
    it.append(title_block("divider-title",200,520,360,nm,size,sub,None,"REGIONAL"))
    it.append(G("divider-meta",(M,590,600,66),[L(M,590,M+230,590,C["line"],1),TM(M,614,"PERÍODO",12,C["txt2"]),TD(M,646,period,26)]))
    it.append(G("divider-index",(W-M-200,590,200,66),[L(W-M-200,590,W-M,590,C["line"],1),TM(W-M,614,"REGIONAL",12,C["txt2"],"end"),TD(W-M,646,f"{i:02d} / {total_regs:02d}",26,C["orange"],"end")]))
    return svg_page(it,"section")

def closing(title,lines,pn,total):
    it=[hero_img("hero","hat",640,50,560,0.62,64,100),hero_img("hero-fx","hat_fx",640,50,560,0.18,524,30)]
    it+=chrome(pn,total,"FISCALIZAÇÃO DE OBRAS ELÉTRICAS · ISA ENERGIA BRASIL","SGS ENGER ENGENHARIA · RELATÓRIO SEMANAL")
    it.append(title_block("closing-title",200,520,360,title,120,"Relatório semanal"))
    it.append(G("closing-meta",(130,560,1020,100),[TM(640,590,lines[0],13,C["txt"],"middle"),TM(640,616,lines[1],13,C["txt2"],"middle"),TM(640,642,lines[2],12,C["txt3"],"middle")]))
    return svg_page(it,"ending")

# ---------- deck B (original structure) ----------
def bchrome(pn,total,reg):
    return chrome(pn,total,f"{PER}  ·  REGIONAL {reg.upper()}","SGS ENGER ENGENHARIA · ISA ENERGIA BRASIL — PAINEL SGI DE GESTÃO DE INSPEÇÕES")

def b_panorama(r,pn,total):
    it=bchrome(pn,total,r["name"]); it.append(page_title("Panorama do período",f"{PER}   ·   Regional: REGIONAL {r['name'].upper()}"))
    k=r["kpi"]; labs=[("INSPEÇÕES","fichas concluídas"),("INSPETORES","com registro no período"),("CONTRATADAS","com inspeção no período"),("PROJETOS","obras e subestações"),("ITENS VERIFICADOS","soma dos checklists")]
    cw=(W-2*M-4*24)/5
    for i,(lab,sub) in enumerate(labs): it.append(kpi(f"kpi-{i+1}",M+i*(cw+24),190,cw,lab,k[lab],sub,hl=(i==0),vs=64))
    lw=560;
    b=section_label(M,360,lw,"Evolução diária das inspeções")+linechart(M,392,lw,256,r["daily"]["cats"],[int(v) for v in r["daily"]["vals"]])
    it.append(G("chart-daily",(M,360,lw,292),b))
    cats,vals=sort_desc(r["part"]["cats"],[int(v) for v in r["part"]["vals"]])
    x2=M+lw+48; w2=W-M-x2
    b=section_label(x2,360,w2,"Participação por contratada","Top 8 no volume de inspeções")+lollipop(x2,392,w2,258,cats,vals,lw=170,fs=14)
    it.append(G("chart-contratadas",(x2,360,w2,292),b))
    return svg_page(it)

def b_projetos(r,pn,total):
    it=bchrome(pn,total,r["name"]); it.append(page_title("Projetos acompanhados",f"{PER}   ·   Regional: REGIONAL {r['name'].upper()}"))
    cats,vals=sort_desc(r["proj"]["cats"],[int(v) for v in r["proj"]["vals"]])
    b=section_label(M,190,W-2*M,"Inspeções por projeto","Top 16 no período")+lollipop(M,222,W-2*M,430,cats,vals,lw=340,fs=14)
    it.append(G("chart-projetos",(M,190,W-2*M,466),b)); return svg_page(it)

def b_desvios(r,pn,total):
    it=bchrome(pn,total,r["name"]); it.append(page_title("Desvios — visão geral",f"{PER}   ·   Regional: REGIONAL {r['name'].upper()}"))
    k=r["dkpi"]; keys=["TOTAL DE DESVIOS","CRÍTICOS (RAC)","ÍNDICE DESV/INSP","CONTRATADAS","PROJETOS"]
    subs=["no período filtrado","0% do total","desvios por inspeção","com desvio registrado","com ocorrência"]
    cw=(W-2*M-4*24)/5
    for i,lab in enumerate(keys): it.append(kpi(f"kpi-{i+1}",M+i*(cw+24),190,cw,lab,k[lab],subs[i],hl=(i==0),vs=64))
    cl=dict(zip(r["classif"]["cats"],[int(v) for v in r["classif"]["vals"]]))
    parts=[("Aberto",cl.get("Aberto",0),C["orange"]),("Fechado",cl.get("Fechado",0),C["txt"])]; tot=sum(p[1] for p in parts)
    lw=500
    b=section_label(M,360,lw,"Classificação dos desvios")
    cx,cy=M+130,360+140; b+=donut(cx,cy,92,parts,sw=10)
    b+=[TD(cx,cy+22,str(tot),64,None,"middle"),TM(cx,cy+46,"DESVIOS",12,C["txt2"],"middle")]
    ly=360+96
    for lab,v,col in parts:
        b+=[DOT(M+300,ly-5,5,col),T(M+316,ly,lab,18,C["txt"]),TD(M+316,ly+48,str(v),40,col),TM(M+420,ly+44,pct(100*v/tot,0) if tot else "0%",14,C["txt2"])]
        ly+=96
    it.append(G("chart-classificacao",(M,360,lw,292),b))
    x2=M+lw+48; w2=W-M-x2
    b=section_label(x2,360,w2,"Desvios por data de registro")+linechart(x2,392,w2,256,r["ddaily"]["cats"],[int(v) for v in r["ddaily"]["vals"]],hi=False,col=C["orange"])
    it.append(G("chart-desvios-data",(x2,360,w2,292),b)); return svg_page(it)

def b_matriz(r,pn,total):
    it=bchrome(pn,total,r["name"]); it.append(page_title("Matriz de risco das contratadas",f"{PER}   ·   Regional: REGIONAL {r['name'].upper()}"))
    b=section_label(M,190,W-2*M,"Índice de desvios por inspeção")+table(M,222,W-2*M,380,r["matriz"][0],r["matriz"][1:],[3.2,1,1.1,1,1,1,1.4],idx_col=6)
    it.append(G("matriz",(M,190,W-2*M,420),b))
    it.append(G("legend",(M,612,W-2*M,26),[TM(M,630,"Verde: sem desvio · Amarelo: até 15% · Laranja: até 30% · Vermelho: acima de 30%   |   contratadas com pelo menos 3 inspeções",12,C["txt2"])]))
    return svg_page(it)

def build_B(out):
    os.makedirs(out,exist_ok=True); total=32; n=0; roster=[]
    def put(name,svg,title):
        nonlocal n; n+=1; fn=f"{n:02d}_{name}.svg"; open(os.path.join(out,fn),"w",encoding="utf-8").write(svg); roster.append((n,fn,title))
    put("capa",cover("B",total),"Capa")
    keys=["trafo","breaker","insul","tower","trafo","breaker"]
    for k,r in enumerate(D):
        base=n
        put(f"r{k+1}_divisor",divider(k+1,6,r["name"],"Gestão de Inspeções · Qualidade",PER,n+1,total,keys[k]),f"Regional {r['name']}")
        put(f"r{k+1}_panorama",b_panorama(r,n+1,total),f"Panorama do período — {r['name']}")
        put(f"r{k+1}_projetos",b_projetos(r,n+1,total),f"Projetos acompanhados — {r['name']}")
        put(f"r{k+1}_desvios",b_desvios(r,n+1,total),f"Desvios — visão geral — {r['name']}")
        put(f"r{k+1}_matriz",b_matriz(r,n+1,total),f"Matriz de risco das contratadas — {r['name']}")
    put("obrigado",closing("OBRIGADO",["RELATÓRIO SEMANAL DE QUALIDADE  —  SGS ENGER ENGENHARIA · ISA ENERGIA BRASIL","6 REGIONAIS  ·  537 INSPEÇÕES  ·  45 DESVIOS  ·  28/09/2026 A 04/10/2026","GERADO AUTOMATICAMENTE EM 06/10/2026 ÀS 10:37"],n+1,total),"Obrigado")
    return roster

# ---------- deck A (consolidated) ----------
def achrome(pn,total,sec): return chrome(pn,total,"FISCALIZAÇÃO DE OBRAS ELÉTRICAS · "+sec.upper(),"SGS ENGER ENGENHARIA PARA ISA ENERGIA BRASIL · "+PER)
def atitle(title_lines,kicker=None):
    b=[]
    if kicker: b.append(TM(M,96,kicker.upper(),12,C["orange"]))
    b.append(TL(M,134,title_lines,40,C["txt"],46,TITLE))
    return G("header",(M,84,W-2*M,44+46*len(title_lines)),b)

def a_resumo(pn,total):
    it=achrome(pn,total,"Resumo executivo"); it.append(atitle(["537 inspeções, 45 desvios e nenhum crítico:","o risco se concentra em poucas contratadas"],"Resumo executivo"))
    cw=(W-2*M-3*24)/4
    vals=[("INSPEÇÕES CONCLUÍDAS",fmt(TI_),f"{fmt(TIT)} itens verificados",True),("DESVIOS REGISTRADOS",str(TDEV),f"{pct(IDX)} desvios por inspeção",False),("DESVIOS CRÍTICOS (RAC)","0","nenhum no período",False),("DESVIOS EM ABERTO",str(TA),f"{pct0(TA,TDEV)}% do total · {TF} fechados",False)]
    for i,(l,v,s,hl) in enumerate(vals): it.append(kpi(f"kpi-{i+1}",M+i*(cw+24),232,cw,l,v,s,hl))
    top=max(D,key=lambda r:r["dev"]); hi=max(D,key=lambda r:r["idx"]); lead=max(D,key=lambda r:r["ins"])
    pts=[("Volume",f"{lead['name']} lidera o volume de inspeções",f"{pct0(lead['ins'],TI_)}%",f"{lead['ins']} de {TI_} inspeções",C["txt"]),
         ("Desvios",f"{top['name']} concentra a maior parte dos desvios",f"{pct0(top['dev'],TDEV)}%",f"{top['dev']} de {TDEV} desvios",C["orange"]),
         ("Intensidade",f"{hi['name']} tem o maior índice de desvios por inspeção",f"{round(hi['idx'])}%",f"{hi['ins']} inspeções · {hi['dev']} desvios",C["red"]),
         ("Atenção","Combinações regional × contratada acima de 30%: "+", ".join(a['nm'] for a in att),str(len(att)),"exigem plano de ação",C["yel"])]
    cw2=(W-2*M-24)/2
    for i,(t,s,hv,hs,col) in enumerate(pts):
        x=M+(i%2)*(cw2+24); y=414+(i//2)*128
        b=[L(x,y,x+cw2,y,C["line"],1),DOT(x+5,y+26,4,col),TM(x+18,y+30,t.upper(),12,C["txt2"]),TL(x,y+62,wrap(s,36)[:3],18,C["txt"],24),
           TD(x+cw2,y+70,hv,64,col,"end"),TM(x+cw2,y+96,hs.upper(),12,C["txt3"],"end")]
        it.append(G(f"insight-{i+1}",(x,y,cw2,122),b))
    return svg_page(it)

def a_regionais(pn,total):
    s=sorted(D,key=lambda r:-r["ins"]); a,b2=s[0],s[1]
    it=achrome(pn,total,"Volume por regional"); it.append(atitle([f"{a['name']} e {b2['name']} respondem por {pct0(a['ins']+b2['ins'],TI_)}%","das 537 inspeções da semana"],"Panorama consolidado"))
    b=section_label(M,226,720,"Inspeções por regional","Semana 28/09 a 04/10")+lollipop(M,258,720,380,[r["name"] for r in s],[r["ins"] for r in s],lw=200,fs=18)
    it.append(G("chart-regionais",(M,226,720,420),b))
    x2=M+720+60; w2=W-M-x2; big=max(D,key=lambda r:r["itens"])
    it.append(kpi("kpi-itens",x2,226,w2,"ITENS VERIFICADOS",fmt(TIT),"soma dos checklists · 6 regionais",False,vs=64,h=150))
    it.append(kpi("kpi-sp",x2,420,w2,"MAIOR VOLUME DE ITENS",fmt(big["itens"]),f"{big['name']} · {pct0(big['itens'],TIT)}% do total",True,vs=64,h=150))
    return svg_page(it)

def a_ritmo(pn,total):
    wk=[v for d,v in zip(dates,dvals) if pdate(d).weekday()<5]
    it=achrome(pn,total,"Ritmo diário"); it.append(atitle([f"Ritmo estável de {min(wk)} a {max(wk)} inspeções por dia útil,","com queda esperada no fim de semana"],"Ritmo operacional"))
    b=section_label(M,226,W-2*M,"Inspeções por dia · todas as regionais","Total da semana: 537")+linechart(M+10,260,W-2*M-20,380,dates,dvals,fs=16)
    it.append(G("chart-daily",(M,226,W-2*M,420),b)); return svg_page(it)

def a_desvios(pn,total):
    s=sorted(D,key=lambda r:-r["dev"]); hi=max(D,key=lambda r:r["idx"])
    it=achrome(pn,total,"Desvios"); it.append(atitle([f"{s[0]['name']} concentra {s[0]['dev']} dos {TDEV} desvios;",f"{hi['name']} tem o maior índice ({pct(hi['idx'],0)})"],"Qualidade"))
    b=section_label(M,226,640,"Desvios por regional","Total: 45 · críticos (RAC): 0")+lollipop(M,258,640,380,[r["name"] for r in s],[r["dev"] for r in s],lw=200,fs=18,col=C["txt"])
    it.append(G("chart-desvios",(M,226,640,420),b))
    x2=M+640+60; w2=W-M-x2; rows=sorted(D,key=lambda r:-r["idx"]); rh=380/6
    b=section_label(x2,226,w2,"Índice desvios por inspeção")
    for i,r in enumerate(rows):
        cy=258+i*rh+rh/2; col=sem(r["idx"])
        b+=[L(x2,258+(i+1)*rh,x2+w2,258+(i+1)*rh,C["line2"],1),T(x2,cy+6,r["name"],18,"#CFCFCF"),DOT(x2+w2-90,cy,5,col),TM(x2+w2,cy+5,pct(r["idx"]),14,col,"end","bold")]
    it.append(G("indice-regional",(x2,226,w2,420),b)); return svg_page(it)

def a_status(pn,total):
    s=sorted(D,key=lambda r:-r["dev"])
    it=achrome(pn,total,"Tratamento de desvios"); it.append(atitle([f"{TA} dos {TDEV} desvios seguem abertos ({pct0(TA,TDEV)}%)","e nenhum é crítico"],"Tratamento de desvios"))
    b=section_label(M,226,440,"Status geral"); cx,cy=M+220,226+215; b+=donut(cx,cy,120,[("A",TA,C["orange"]),("F",TF,C["txt"])],sw=10)
    b+=[TD(cx,cy+24,str(TDEV),64,None,"middle"),TM(cx,cy+52,"DESVIOS",12,C["txt2"],"middle"),DOT(M+110,226+400,5,C["orange"]),T(M+124,226+406,f"Aberto {TA}",16,C["txt"]),DOT(M+260,226+400,5,C["txt"]),T(M+274,226+406,f"Fechado {TF}",16,C["txt"])]
    it.append(G("donut-status",(M,226,440,420),b))
    x2=M+440+60; w2=W-M-x2; mx=max(r["dev"] for r in D); rh=380/6; bw=w2-200-90
    b=section_label(x2,226,w2,"Aberto × fechado por regional")
    for i,r in enumerate(s):
        cy=258+i*rh+rh/2; bx=x2+200
        b.append(T(x2+180,cy+6,r["name"],16,"#CFCFCF","normal","end"))
        wa=bw*r["aberto"]/mx; wf=bw*r["fechado"]/mx
        if r["aberto"]: b+= [L(bx,cy-6,bx+wa,cy-6,C["orange"],3)]
        if r["fechado"]: b+= [L(bx,cy+6,bx+wf,cy+6,C["txt"],3)]
        b.append(TM(bx+max(wa,wf)+14,cy+5,f"{r['aberto']} / {r['fechado']}",14,C["txt"],"start","bold"))
    it.append(G("stack-regional",(x2,226,w2,420),b)); return svg_page(it)

def a_matriz(pn,total):
    rows=sorted([c for c in cons.values() if c["dev"]>0],key=lambda c:-c["idx"])
    it=achrome(pn,total,"Risco"); it.append(atitle([f"Matriz consolidada: {len(rows)} contratadas com desvio,","ÁREA 19 e TECCEN lideram o índice"],"Risco"))
    rr=[[c["nm"],str(len(c["reg"])),str(c["ins"]),fmt(c["itens"]),str(c["dev"]),str(c["crit"]),pct(c["idx"])] for c in rows[:12]]
    b=section_label(M,226,W-2*M,"Índice de desvios por inspeção · todas as regionais")+table(M,258,W-2*M,360,["CONTRATADA","REGIONAIS","INSPEÇÕES","ITENS","DESVIOS","CRÍTICOS","DESV/INSP"],rr,[3.2,1,1.1,1,1,1,1.4],idx_col=6,fs=15)
    it.append(G("matriz",(M,226,W-2*M,396),b))
    it.append(G("legend",(M,624,W-2*M,24),[TM(M,640,"Verde: sem desvio · Amarelo: até 15% · Laranja: até 30% · Vermelho: acima de 30%   |   contratadas com ≥ 3 inspeções por regional",12,C["txt2"])]))
    return svg_page(it)

def a_atencao(pn,total):
    it=achrome(pn,total,"Contratadas em atenção"); it.append(atitle([f"{len(att)} combinações acima de 30% de desvios por inspeção","exigem plano de ação já na próxima semana"],"Contratadas em atenção"))
    n=len(att); cw=(W-2*M-(n-1)*40)/n
    for i,a in enumerate(att):
        x=M+i*(cw+40); y=232; col=sem(a["idx"])
        nm=a["nm"]; sz=40
        b=[L(x,y,x+cw,y,C["line"],1),TM(x,y+24,"REGIONAL "+a["reg"].upper(),12,C["orange"]),TD(x,y+84,nm.upper(),sz),
           TD(x,y+250,a["idxs"],150 if len(a["idxs"])<=3 else 130,col),TM(x,y+282,"DESVIOS POR INSPEÇÃO",12,C["txt2"]),L(x,y+312,x+cw,y+312,C["line"],1),
           TD(x,y+372,str(a["ins"]),64),TM(x,y+398,"INSPEÇÕES",12,C["txt2"]),TD(x+cw/2,y+372,str(a["dev"]),64,col),TM(x+cw/2,y+398,"DESVIOS",12,C["txt2"])]
        it.append(G(f"card-{i+1}",(x,y,cw,410),b))
    return svg_page(it)

def a_regional(r,pn,total):
    rows=r["matriz"][1:]; worst=sorted(rows,key=lambda x:-num(x[6]))[0]
    l2=f"{worst[0]} lidera o índice ({worst[6]})" if num(worst[6])>0 else "sem desvios nas contratadas monitoradas"
    it=achrome(pn,total,"Regional "+r["name"]); it.append(atitle([f"{r['name']}: {r['ins']} inspeções e {r['dev']} desvio"+("s" if r['dev']!=1 else ""),f"índice de {pct(r['idx'],1 if r['idx']<10 else 0)} · "+l2],"Regional "+r["name"]))
    cw=(W-2*M-3*24)/4
    vals=[("INSPEÇÕES",str(r["ins"]),f"{pct0(r['ins'],TI_)}% do total",True),("DESVIOS",str(r["dev"]),f"{r['aberto']} abertos · {r['fechado']} fechados",False),("ÍNDICE DESV/INSP",r["dkpi"]["ÍNDICE DESV/INSP"],"desvios por inspeção",False),("ITENS VERIFICADOS",r["kpi"]["ITENS VERIFICADOS"],f"{r['kpi']['CONTRATADAS']} contratadas · {r['kpi']['PROJETOS']} projetos",False)]
    for i,(l,v,s_,hl) in enumerate(vals): it.append(kpi(f"kpi-{i+1}",M+i*(cw+24),232,cw,l,v,s_,hl,vs=64,h=140))
    y0=396; hh=250
    w1=380
    b=section_label(M,y0,w1,"Inspeções por dia")+linechart(M,y0+30,w1,hh-34,r["daily"]["cats"],[int(v) for v in r["daily"]["vals"]],wd=False,fs=12)
    it.append(G("chart-daily",(M,y0,w1,hh),b))
    pc,vc=sort_desc(r["proj"]["cats"],[int(v) for v in r["proj"]["vals"]]); k=min(5,len(pc))
    x2=M+w1+40; w2=380
    b=section_label(x2,y0,w2,"Top projetos","inspeções"); rh=(hh-40)/k
    mx=max(vc[:k])
    for i in range(k):
        yy=y0+36+i*rh
        b.append(T(x2,yy+14,cut(pc[i],36),13,"#CFCFCF"))
        L_=max(4,(w2-50)*vc[i]/mx); col=C["orange"] if i==0 else C["txt"]
        b+=[L(x2,yy+28,x2+L_,yy+28,col,2),DOT(x2+L_,yy+28,4,col),TM(x2+L_+10,yy+32,str(vc[i]),12,C["txt"],"start","bold")]
    it.append(G("chart-projetos",(x2,y0,w2,hh),b))
    x3=x2+w2+40; w3=W-M-x3
    rr=sorted(rows,key=lambda x:-num(x[6]))[:5]; rh=min(40,(hh-40)/max(len(rr),1))
    b=section_label(x3,y0,w3,"Contratadas · desv/insp")
    for i,x in enumerate(rr):
        yy=y0+36+i*rh; col=sem(num(x[6]))
        b+=[L(x3,yy+rh,x3+w3,yy+rh,C["line2"],1),T(x3,yy+rh*0.62,cut(x[0],20),14,"#CFCFCF"),DOT(x3+w3-62,yy+rh*0.5,4,col),TM(x3+w3,yy+rh*0.5+5,x[6],13,col,"end","bold")]
    it.append(G("risco",(x3,y0,w3,hh),b))
    return svg_page(it)

def a_foco(pn,total):
    it=achrome(pn,total,"Foco da próxima semana"); it.append(atitle(["Três frentes para manter zero crítico","e reduzir o índice de desvios"],"Foco da próxima semana"))
    items=[("01","Contratadas acima de 30%","; ".join(f"{a['nm']} ({a['reg']}, {a['idxs']})" for a in att)+". Plano de ação e reinspeção dirigida.",C["red"]),
           ("02","Fechar os desvios abertos",f"{TA} desvios em aberto, concentrados em "+", ".join(f"{r['name']} ({r['aberto']})" for r in sorted(D,key=lambda r:-r["aberto"])[:2])+". Acompanhar prazo de tratamento.",C["orange"]),
           ("03","Padronizar o cadastro",f"{cons['NÃO INFORMADO']['ins']} inspeções sem contratada informada ({pct0(cons['NÃO INFORMADO']['ins'],TI_)}% do total). Tornar o campo obrigatório no registro.",C["txt"])]
    cw=(W-2*M-2*40)/3
    for i,(n,t,s,col) in enumerate(items):
        x=M+i*(cw+40); y=232
        b=[L(x,y,x+cw,y,C["line"],1),TD(x,y+110,n,64,col),T(x,y+166,t,18,C["txt"],"bold"),TL(x,y+204,wrap(s,32)[:8],16,C["txt2"],26)]
        it.append(G(f"foco-{i+1}",(x,y,cw,400),b))
    return svg_page(it)

def build_A(out):
    os.makedirs(out,exist_ok=True); total=16; n=0; roster=[]
    def put(name,svg,title):
        nonlocal n; n+=1; fn=f"{n:02d}_{name}.svg"; open(os.path.join(out,fn),"w",encoding="utf-8").write(svg); roster.append((n,fn,title))
    put("capa",cover("A",total),"Capa")
    put("resumo",a_resumo(2,total),"Resumo executivo"); put("regionais",a_regionais(3,total),"Volume por regional"); put("ritmo",a_ritmo(4,total),"Ritmo diário")
    put("desvios",a_desvios(5,total),"Desvios por regional"); put("status",a_status(6,total),"Status dos desvios"); put("matriz",a_matriz(7,total),"Matriz de risco consolidada"); put("atencao",a_atencao(8,total),"Contratadas em atenção")
    for i,r in enumerate(D): put(f"reg{i+1}",a_regional(r,9+i,total),f"Regional {r['name']}")
    put("foco",a_foco(15,total),"Foco da próxima semana")
    put("obrigado",closing("OBRIGADO",["FISCALIZAÇÃO DE OBRAS ELÉTRICAS  —  SGS ENGER ENGENHARIA · ISA ENERGIA BRASIL","6 REGIONAIS  ·  537 INSPEÇÕES  ·  45 DESVIOS  ·  28/09/2026 A 04/10/2026","GERADO AUTOMATICAMENTE EM 06/10/2026 ÀS 10:37"],16,total),"Obrigado")
    return roster

if __name__=="__main__":
    which=sys.argv[1]; out=sys.argv[2]
    print((build_A if which=="A" else build_B)(out))
