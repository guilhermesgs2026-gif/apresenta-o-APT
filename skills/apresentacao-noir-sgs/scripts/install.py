import sys,os,shutil,subprocess,glob,importlib
sys.path.insert(0,os.path.dirname(__file__))
import specs
S=os.path.expanduser("~/.claude/skills/ppt-master")
which=sys.argv[1]; proj=sys.argv[2]
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
if which=="A":
    import deckN as d; out=os.path.join(ROOT,"out_NA"); roster=d.build_A(out)
    name="Fiscalização de Obras Elétricas - Relatório Consolidado"
    core="537 inspeções, 45 desvios e zero críticos; o risco se concentra em poucas contratadas e regionais."
    intent="Resumir a semana de fiscalização das 6 regionais, expor onde está o risco e orientar o foco da próxima semana."
    outcome="A gestão identifica em minutos as contratadas e regionais que exigem ação."
    afterlife="Enviado por e-mail como pré-leitura e arquivado no relatório semanal."
    deliv="Reunião semanal de gestão (tela) e leitura offline em PPTX"
    aud="Gestão da ISA Energia Brasil e liderança da SGS Enger Engenharia"
    mode_name="pyramid"
    mode_beh="Open with the conclusion (executive summary), then support it with one action-titled page per finding, drill down to one page per regional, close with next-week focus."
    pages=[]
    for n,fn,t in roster:
        pages.append((fn,t,t,"Chart, KPI cards and callouts from the weekly SGI data for: "+t,"KPI cards, chart panels and the action title belong to one page job; no cross-page dependency"))
else:
    import deckN as d; out=os.path.join(ROOT,"out_NB"); roster=d.build_B(out)
    name="Relatório Semanal de Qualidade - Modelo Original"
    core="Mesma estrutura do painel SGI (32 páginas, 6 regionais × 5 páginas) com visual de alto nível."
    intent="Entregar o relatório semanal no formato original do painel SGI, com texto e ordem preservados."
    outcome="Quem já conhece o relatório encontra cada dado no mesmo lugar, agora com leitura muito mais rápida."
    afterlife="Substitui o PPTX gerado automaticamente pelo painel; reutilizado semana a semana."
    deliv="Reunião semanal de gestão (tela) e leitura offline em PPTX"
    aud="Gestão da ISA Energia Brasil e liderança da SGS Enger Engenharia"
    mode_name="briefing"
    mode_beh="Preserve the original dashboard order verbatim: cover, then per regional a divider, panorama, projects, deviations and risk matrix, then thank-you."
    pages=[(fn,t,t,"All labels, titles and figures verbatim from the original SGI export for: "+t,"Page titles and labels are verbatim from source; order is source order") for n,fn,t in roster]
P=proj
used=set()
for f in glob.glob(os.path.join(out,"*.svg")):
    t=open(f,encoding="utf-8").read()
    for h in ("hero_tower","hero_trafo","hero_breaker","hero_insul","hero_hat","hero_tower_fx","hero_trafo_fx","hero_breaker_fx","hero_insul_fx","hero_hat_fx"):
        if "images/"+h+".png" in t: used.add(h)
sp=specs.design_spec(name,pages,core,intent,outcome,"Editorial noir: pure black, hairline charts, chrome 3D hero objects, SGS orange accent",afterlife,deliv,aud,mode_name,mode_beh,used)
open(os.path.join(P,"design_spec.md"),"w",encoding="utf-8").write(sp)
lk=specs.spec_lock(len(pages),core,aud,intent,mode_beh,used)
open(os.path.join(P,"spec_lock.md"),"w",encoding="utf-8").write(lk)
os.makedirs(os.path.join(P,"images"),exist_ok=True)
for f in glob.glob(os.path.join(P,"images","hero_*")): os.remove(f)
for h in used: shutil.copy(os.path.join(ROOT,"assets",h+".png"),os.path.join(P,"images",h+".png"))
shutil.copy(os.path.join(ROOT,"images","sgs_logo.png"),os.path.join(P,"images","sgs_logo.png"))
pass
so=os.path.join(P,"svg_output")
os.makedirs(so,exist_ok=True)
for f in glob.glob(os.path.join(so,"*.svg")): os.remove(f)
for f in glob.glob(os.path.join(out,"*.svg")): shutil.copy(f,so)
print("installed",len(roster),"pages into",P)
