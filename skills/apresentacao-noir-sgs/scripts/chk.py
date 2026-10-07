import sys,json,subprocess,collections
import os
S=os.path.expanduser("~/.claude/skills/ppt-master")
P=sys.argv[1]
r=subprocess.run(["python",S+"/scripts/svg_quality_checker.py",P,"--canonical-authoring","--stage","final","--json"],capture_output=True,text=True,encoding="utf-8",errors="replace")
rep=json.load(open(P+"/validation/svg_quality_report.json",encoding="utf-8"))
print("exit",r.returncode, rep["summary"] if "summary" in rep else "")
c=collections.Counter()
for k in ("blocking","introduced"):
    for i in rep["categories"][k]["issues"]:
        c[(k,i.get("message","")[:170])]+=1
for (k,m),v in c.most_common(25): print(k,v,m)
