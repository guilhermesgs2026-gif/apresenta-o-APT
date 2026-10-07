# NOIR design system: pure black, thin white lines, Light display type, mono captions, one SGS-orange accent
import math, json, datetime
W,H=1280,720; M=56
C=dict(bg="#000000",txt="#FFFFFF",txt2="#9A9A9A",txt3="#5C5C5C",line="#2A2A2A",line2="#161616",
       orange="#F7941D",green="#34D399",yel="#FACC15",org="#FB923C",red="#F43F5E",cyan="#FFFFFF")
TITLE="Open Sauce"; BODY="Open Sauce"; MONO="Space Mono"; LIGHT="Open Sauce Light"
IMG={k:f"../images/hero_{k}.png" for k in ("tower","trafo","breaker","insul","hat")}
IMG.update({k+"_fx":f"../images/hero_{k}_fx.png" for k in ("tower","trafo","breaker","insul","hat")})
import os
from PIL import ImageFont
_FONTS={}
def tw(text,size,font="OpenSauce-Regular"):
    if font not in _FONTS: _FONTS[font]=ImageFont.truetype(os.path.join(os.path.dirname(__file__),"..","assets","fonts",font+".ttf"),200)
    return _FONTS[font].getlength(text)*size/200
ASP=json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__),"..","assets","aspects.json")))

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def f1(v): return ("%.1f"%v).rstrip("0").rstrip(".")
def num(s): return float(str(s).replace("%","").replace(".","").replace(",","."))
def fmt(n): return f"{int(round(n)):,}".replace(",",".")
def pct(v,d=1): return (f"{v:.{d}f}").replace(".",",")+"%"
def pdate(s):
    d,m=s.split("/"); return datetime.date(2026,int(m),int(d))
WD=["seg","ter","qua","qui","sex","sáb","dom"]
def sem(v):
    if v<=0: return C["green"]
    if v<=15: return C["yel"]
    if v<=30: return C["org"]
    return C["red"]

def T(x,y,s,size,fill=None,weight="normal",anchor="start",fam=None):
    fill=fill or C["txt"]
    a=f' text-anchor="{anchor}"' if anchor!="start" else ""
    fm=f' font-family="{fam}"' if fam else ""
    return f'<text x="{f1(x)}" y="{f1(y)}" font-size="{size}" fill="{fill}"{a}{fm}>{esc(s)}</text>'
def TD(x,y,s,size,fill=None,anchor="start"): return T(x,y,s,size,fill,"normal",anchor,TITLE)
def TM(x,y,s,size,fill=None,anchor="start",weight="normal"): return T(x,y,s,size,fill or C["txt2"],weight,anchor,MONO)
def TL(x,y,lines,size,fill=None,lh=None,fam=None,anchor="start"):
    fill=fill or C["txt"]; lh=lh or round(size*1.3)
    fm=f' font-family="{fam}"' if fam else ""
    an=f' text-anchor="{anchor}"' if anchor!="start" else ""
    sp="".join(f'<tspan x="{f1(x)}" dy="{0 if i==0 else lh}">{esc(l)}</tspan>' for i,l in enumerate(lines))
    return f'<text x="{f1(x)}" y="{f1(y)}" font-size="{size}" fill="{fill}"{an}{fm}>{sp}</text>'
def R(x,y,w,h,fill,rx=0,stroke=None,sw=1,op=None):
    s=f'<rect x="{f1(x)}" y="{f1(y)}" width="{f1(w)}" height="{f1(h)}" fill="{fill}"'
    if rx: s+=f' rx="{rx}"'
    if stroke: s+=f' stroke="{stroke}" stroke-width="{sw}"'
    if op is not None: s+=f' fill-opacity="{op}"'
    return s+"/>"
def L(x1,y1,x2,y2,stroke=None,sw=1):
    return f'<line x1="{f1(x1)}" y1="{f1(y1)}" x2="{f1(x2)}" y2="{f1(y2)}" stroke="{stroke or C["line"]}" stroke-width="{sw}"/>'
def DOT(x,y,r,fill): return f'<circle cx="{f1(x)}" cy="{f1(y)}" r="{r}" fill="{fill}"/>'
def G(id,bounds,body,extra=""):
    x,y,w,h=bounds
    return f'<g id="{id}" data-pptx-bounds="{f1(x)} {f1(y)} {f1(w)} {f1(h)}"{extra}>\n'+"\n".join(body if isinstance(body,list) else [body])+"\n</g>"
def paren(x,y0,y1,side,w=None,sw=2.5,col=None):
    w=w or (y1-y0)*0.11; mid=(y0+y1)/2; col=col or C["txt"]
    if side=="l": d=f"M{f1(x+w)} {f1(y0)} Q{f1(x-w*0.9)} {f1(mid)} {f1(x+w)} {f1(y1)}"
    else: d=f"M{f1(x-w)} {f1(y0)} Q{f1(x+w*0.9)} {f1(mid)} {f1(x-w)} {f1(y1)}"
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
def svg_page(items,role="content"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{BODY}" data-pptx-page-role="{role}">\n'
            f'<rect id="bg" x="0" y="0" width="{W}" height="{H}" fill="{C["bg"]}" data-pptx-role="background"/>\n'+"\n".join(items)+"\n</svg>\n")
def hero_img(id,key,cx=640,top=60,h=560,op=0.62,by=64,bh=100):
    base=key.replace("_fx","")
    a=ASP[base]
    if a>1: w=h; hh=h/a; t=top+(h-hh)/2
    else: w=h*a; hh=h; t=top
    img=f'<image href="{IMG[key]}" x="{f1(cx-w/2)}" y="{f1(t)}" width="{f1(w)}" height="{f1(hh)}" opacity="{op}" preserveAspectRatio="xMidYMid meet"/>'
    return G(id,(cx-w/2,by,w,bh),[img])

def paren_pair(y0,y1,w=46,sw=3):
    return [G("paren-l",(12,y0,100,y1-y0),[paren(60,y0,y1,"l",w=w,sw=sw)]),G("paren-r",(1168,y0,100,y1-y0),[paren(1220,y0,y1,"r",w=w,sw=sw)])]

def logo(x=M,y=24,h=40,img="../images/sgs_logo.png"):
    pw=h*2.035
    b=[f'<image href="{img}" x="{f1(x)}" y="{f1(y)}" width="{f1(pw)}" height="{f1(h)}" preserveAspectRatio="xMidYMid meet"/>']
    return G("logo-sgs",(x,y,pw,h),b,' data-pptx-role="logo"'),pw

def chrome(pn,total,toptext,footleft):
    lg,pw=logo()
    top=G("topbar",(M+pw+20,28,W-2*M-pw-20,30),[TM(W-M,48,toptext,12,C["txt2"],"end")],' data-pptx-role="header"')
    foot=G("footer",(M,H-44,W-2*M,30),[TM(M,H-24,footleft,12,C["txt3"]),TM(W-M,H-24,f"{pn:02d} / {total:02d}",12,C["txt2"],"end")],' data-pptx-role="footer"')
    return [lg,top,foot]

def page_title(title,sub=None,paren_title=True):
    t=f"({title.upper()})" if paren_title else title
    b=[TD(M,128,t,40)]
    if sub: b.append(TM(M,156,sub,13,C["txt2"]))
    return G("header",(M,84,W-2*M,86),b)

def section_label(x,y,w,label,right=None):
    b=[L(x,y,x+w,y,C["line"],1),TM(x,y+22,label.upper(),12,C["txt2"])]
    if right: b.append(TM(x+w,y+22,right.upper(),12,C["txt3"],"end"))
    return b

def kpi(id,x,y,w,label,value,sub,hl=False,vs=64,h=150):
    b=[L(x,y,x+w,y,C["line"],1),TM(x,y+24,label.upper(),12,C["txt2"]),TD(x,y+104,value,vs,C["orange"] if hl else C["txt"]),TM(x,y+130,sub,12,C["txt3"])]
    return G(id,(x,y,w,h),b)

def lollipop(x,y,w,h,cats,vals,lw=190,fs=15,leader=True,col=None,mx=None):
    n=len(cats); mx=mx or (max(vals) if vals else 1); rh=h/n; out=[]
    bx=x+lw+18; bw=w-lw-18-60
    for i,(c,v) in enumerate(zip(cats,vals)):
        cy=y+i*rh+rh/2
        out.append(TM(x+lw,cy+4.5,c.upper(),13,"#D0D0D0","end"))
        L_=max(4,bw*v/mx); colr=C["orange"] if (leader and i==0) else (col or C["txt"])
        out.append(L(bx,cy,bx+L_,cy,colr,2)); out.append(DOT(bx+L_,cy,5,colr))
        out.append(TM(bx+L_+14,cy+5,fmt(v),14,colr if (leader and i==0) else C["txt"],"start","bold"))
    return out

def linechart(x,y,w,h,cats,vals,hi=True,col=None,wd=True,fs=14):
    n=len(cats); mx=max(vals) if vals else 1; base=y+h-(40 if wd else 24); top=y+30; out=[]
    for k in range(4):
        gy=base-(base-top)*k/3
        out.append(L(x,gy,x+w,gy,C["line2"] if k else C["line"],1))
    slot=w/n; pts=[]
    for i,v in enumerate(vals):
        cx=x+slot*i+slot/2; cy=base-(base-top)*v/mx if mx else base; pts.append((cx,cy))
    d="M"+" L".join(f"{f1(a)} {f1(b)}" for a,b in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{col or C["txt"]}" stroke-width="2.5" stroke-linejoin="round"/>')
    mi=vals.index(mx)
    for i,((cx,cy),v,c) in enumerate(zip(pts,vals,cats)):
        colr=C["orange"] if (hi and i==mi) else (col or C["txt"])
        out.append(L(cx,cy,cx,base,C["line"],1)); out.append(DOT(cx,cy,5,colr))
        out.append(TM(cx,cy-14,fmt(v),fs,colr if (hi and i==mi) else C["txt"],"middle","bold"))
        out.append(TM(cx,base+20,c,12,C["txt2"],"middle"))
        if wd: out.append(TM(cx,base+36,WD[pdate(c).weekday()],12,C["txt3"],"middle"))
    return out

def donut(cx,cy,r,parts,sw=10):
    tot=sum(p[1] for p in parts); out=[]
    if tot==0:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["line"]}" stroke-width="{sw}"/>'); return out
    a0=-math.pi/2
    for lab,v,col in parts:
        if v<=0: continue
        a1=a0+2*math.pi*v/tot
        if v==tot: out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        else:
            g=0.03; s,e=a0+g,a1-g
            x0,y0=cx+r*math.cos(s),cy+r*math.sin(s); x1,y1=cx+r*math.cos(e),cy+r*math.sin(e)
            out.append(f'<path d="M{f1(x0)} {f1(y0)} A{r} {r} 0 {1 if (e-s)>math.pi else 0} 1 {f1(x1)} {f1(y1)}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
        a0=a1
    return out

def table(x,y,w,h,headers,rows,colw,idx_col=-1,fs=16):
    n=len(rows); rh=min(44,(h-30)/max(n,1)); out=[]
    tot=sum(colw); cws=[w*c/tot for c in colw]; hx=[]; cx=x
    for c in cws: hx.append(cx); cx+=c
    al=["start"]+["end"]*(len(headers)-1)
    for j,hd in enumerate(headers):
        out.append(TM(hx[j] if al[j]=="start" else hx[j]+cws[j],y+16,hd,12,C["txt2"],al[j]))
    out.append(L(x,y+26,x+w,y+26,C["txt3"],1))
    for i,r in enumerate(rows):
        yy=y+30+i*rh; cy=yy+rh/2
        out.append(L(x,yy+rh,x+w,yy+rh,C["line2"],1))
        for j,v in enumerate(r):
            tx=hx[j] if al[j]=="start" else hx[j]+cws[j]
            if j==idx_col%len(headers):
                col=sem(num(v)); out.append(DOT(tx-82,cy,5,col)); out.append(TM(tx,cy+5,v,15,col,"end","bold"))
            else:
                out.append(TM(tx,cy+5,v.upper(),14,C["txt"] if j==0 else "#B5B5B5",al[j]))
    return out
