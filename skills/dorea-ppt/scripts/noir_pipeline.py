"""Pipeline completo: deck.json -> PPTX noir (fontes embutidas, animações, validação).
Uso: python noir_pipeline.py <deck.json> <pasta_de_trabalho> [--name nome]
Requer a skill ppt-master em ~/.claude/skills/ppt-master. Saída: <pasta>/entrega/<nome>.pptx"""
import sys, os, re, json, glob, shutil, subprocess, argparse
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import noir_build, noir_specs
from embed_fonts import embed

PM = os.path.expanduser("~/.claude/skills/ppt-master/scripts")


def run(args, check=True):
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    if check and r.returncode != 0: raise SystemExit(f"FALHOU: {' '.join(args[:2])}\n{r.stdout[-1500:]}\n{r.stderr[-800:]}")
    return r


def gen_anim(project):
    """animations.json: tempos medidos do modelo Canva (tudo aparece em ~1,3 s)."""
    def row(eff, order, dur, delay, first=False, opts=None):
        r = {"effect": eff, "order": order, "duration": dur, "trigger": "after-previous" if first else "with-previous", "delay": round(delay, 2)}
        if opts: r["effect_options"] = opts
        return r
    slides = {}
    for f in sorted(glob.glob(os.path.join(project, "svg_output", "*.svg"))):
        stem = os.path.basename(f)[:-4]; t = open(f, encoding="utf-8").read()
        ids = re.findall(r'^<g id="([^"]+)" data-pptx-bounds', t, re.M); groups = {}; k = 0
        for gid in ids:
            if gid in ("topbar", "footer", "legend"): continue
            k += 1; first = (k == 1)
            if gid in ("logo", "logo-sgs"): r = row("entrance_fade", k, 0.2, 0.0, first)
            elif gid == "hero": r = row("entrance_faded_zoom", k, 0.5, 0.35, first)
            elif gid == "hero-fx":
                groups[gid] = {"effects": [row("entrance_faded_zoom", k, 0.5, 0.35, first), row("exit_fade", k + 100, 0.4, 0.9, False)]}; continue
            elif gid.endswith("-title"): r = row("entrance_split", k, 0.3, 0.3, first)
            elif gid == "header": r = row("entrance_fade", k, 0.2, 0.05, first)
            elif gid.startswith(("cover-meta", "divider-meta", "divider-index", "closing-meta")): r = row("entrance_fade", k, 0.2, 0.5 + 0.08 * k, first)
            elif gid.startswith("kpi"): r = row("entrance_fade", k, 0.2, 0.15 + 0.04 * k, first)
            else: r = row("entrance_wipe", k, 0.25, 0.3 + 0.05 * k, first, {"direction": "right"})
            groups[gid] = {"effects": [r]}
        slides[stem] = {"groups": groups, "transition": {"effect": "fade", "duration": 0.35}}
    json.dump({"version": 1, "slides": slides}, open(os.path.join(project, "animations.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("deck"); ap.add_argument("work"); ap.add_argument("--name"); a = ap.parse_args()
    deck = json.load(open(a.deck, encoding="utf-8")); work = os.path.abspath(a.work); os.makedirs(work, exist_ok=True)
    name = a.name or re.sub(r"\W+", "_", deck.get("meta", {}).get("name") or deck.get("meta", {}).get("title", "apresentacao")).strip("_").lower()
    print("1/8 gerando SVGs..."); roster, c = noir_build.build(deck, work)
    meta = deck.get("meta", {}); accent = noir_build.N.C["acc"]
    print("2/8 criando projeto ppt-master...")
    out = run([os.path.join(PM, "project_manager.py"), "init", name]).stdout
    m = re.search(r"Project created: (.+)", out); project = m.group(1).strip()
    print("   projeto:", project)
    print("3/8 spec, lock, imagens...")
    images = []
    for fn in sorted(c.used):
        kind = "Photograph" if fn.startswith(("logo", "img_")) else "Illustration"
        purpose = "Brand logo" if fn.startswith("logo") else ("User image" if fn.startswith("img_") else ("Iridescent entrance layer" if fn.endswith("_fx.png") else "3D object behind the title"))
        images.append((fn, purpose, kind))
    open(os.path.join(project, "design_spec.md"), "w", encoding="utf-8").write(noir_specs.design_spec(meta, roster, images, accent))
    open(os.path.join(project, "spec_lock.md"), "w", encoding="utf-8").write(noir_specs.spec_lock(meta, len(roster), images, accent))
    os.makedirs(os.path.join(project, "images"), exist_ok=True)
    for f in glob.glob(os.path.join(project, "images", "*")): os.remove(f)
    for fn in c.used: shutil.copy(os.path.join(work, "images", fn), os.path.join(project, "images", fn))
    so = os.path.join(project, "svg_output"); os.makedirs(so, exist_ok=True)
    for f in glob.glob(os.path.join(so, "*.svg")): os.remove(f)
    for f in glob.glob(os.path.join(work, "svg", "*.svg")): shutil.copy(f, so)
    print("4/8 animações..."); gen_anim(project)
    print("5/8 validações ppt-master...")
    run([os.path.join(PM, "animation_config.py"), "validate", project]); run([os.path.join(PM, "project_manager.py"), "validate", project])
    run([os.path.join(PM, "analyze_images.py"), os.path.join(project, "images")], check=False)
    r = run([os.path.join(PM, "svg_quality_checker.py"), project, "--canonical-authoring", "--stage", "final", "--json"], check=False)
    rep = json.load(open(os.path.join(project, "validation", "svg_quality_report.json"), encoding="utf-8"))
    blocking = rep["categories"]["blocking"]["issues"]
    if r.returncode != 0 or blocking:
        print("CHECKER REPROVOU:"); [print("  -", i.get("file", ""), i.get("message", "")[:220]) for i in blocking[:20]]
        raise SystemExit("Corrija o deck.json (textos longos demais, muitos itens) e rode de novo.")
    print("6/8 exportando PPTX...")
    run([os.path.join(PM, "finalize_svg.py"), project]); run([os.path.join(PM, "svg_to_pptx.py"), project, "--no-notes"])
    pptx = sorted(glob.glob(os.path.join(project, "exports", "*.pptx")), key=os.path.getmtime)[-1]
    print("7/8 embutindo fontes Open Sauce / Space Mono...")
    os.makedirs(os.path.join(work, "entrega"), exist_ok=True); final = os.path.join(work, "entrega", name + ".pptx")
    try: embed(pptx, final)
    except PermissionError:
        final = os.path.join(work, "entrega", name + "_v2.pptx"); embed(pptx, final)
    print("8/8 conferindo o arquivo...")
    from pptx import Presentation
    p = Presentation(final); print("   abre no python-pptx:", len(p.slides._sldIdLst), "slides")
    val = glob.glob(os.path.expanduser("~/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/*/*/skills/pptx/scripts/office/validate.py"))
    if val: print("   validate:", run([val[0], final], check=False).stdout.strip().splitlines()[-1])
    print("PRONTO:", final)


if __name__ == "__main__": main()
