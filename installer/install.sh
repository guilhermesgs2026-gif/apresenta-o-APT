#!/usr/bin/env bash
# Instalador da skill "apresentacao-noir-sgs" + dependências (macOS / Linux / Git Bash)
# Uso (na raiz do repositório):  bash installer/install.sh [--skip-agent-reach] [--force]
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS="$HOME/.claude/skills"; mkdir -p "$SKILLS"
SKIP_AR=0; FORCE=0
for a in "$@"; do case "$a" in --skip-agent-reach) SKIP_AR=1;; --force) FORCE=1;; esac; done
PY=python3; command -v python3 >/dev/null || PY=python
need(){ command -v "$1" >/dev/null || { echo "Falta '$1'. $2"; exit 1; }; }
echo "==> 1/6 Conferindo programas"; need git "Instale o git"; need "$PY" "Instale o Python 3.10+"
echo "==> 2/6 Bibliotecas Python"
$PY -m pip install --upgrade pip >/dev/null
$PY -m pip install Pillow numpy python-pptx lxml fonttools "markitdown[pptx]"
echo "==> 3/6 Skill ppt-master (hugohe3/ppt-master, MIT)"
PM="$SKILLS/ppt-master"
if [ -d "$PM" ] && [ $FORCE -eq 0 ]; then echo "    já instalada ($PM). Use --force para reinstalar."
else
  TMP="$(mktemp -d)"; git clone --depth 1 https://github.com/hugohe3/ppt-master "$TMP/ppt-master"
  rm -rf "$PM"; cp -r "$TMP/ppt-master/skills/ppt-master" "$PM"; rm -rf "$TMP"
fi
$PY -m pip install -r "$PM/requirements.txt"
$PY "$PM/scripts/attribution_guard.py"
echo "==> 4/6 Pesquisa na web: agent-reach + Exa (Panniantong/agent-reach, MIT)"
if [ $SKIP_AR -eq 1 ]; then echo "    pulado"
else
  [ -d "$HOME/.agent-reach-venv" ] || $PY -m venv "$HOME/.agent-reach-venv"
  "$HOME/.agent-reach-venv/bin/python" -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip
  "$HOME/.agent-reach-venv/bin/agent-reach" install --env=auto || true
  if command -v npm >/dev/null; then npm install -g mcporter && mcporter config add exa https://mcp.exa.ai/mcp --scope home
  else echo "AVISO: instale o Node.js e rode: npm i -g mcporter && mcporter config add exa https://mcp.exa.ai/mcp --scope home"; fi
fi
echo "==> 5/6 Instalando a skill apresentacao-noir-sgs"
rm -rf "$SKILLS/apresentacao-noir-sgs"; cp -r "$REPO/skills/apresentacao-noir-sgs" "$SKILLS/"
echo "==> 6/6 Verificações opcionais"
command -v ffmpeg >/dev/null || echo "AVISO: ffmpeg ausente (só para reanalisar o vídeo do exemplo Canva)."
echo; echo "Pronto. Conecte os conectores Canva e Figma no app do Claude e use:  /apresentacao-noir-sgs"
