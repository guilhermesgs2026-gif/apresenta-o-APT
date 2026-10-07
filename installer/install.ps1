# Instalador da skill "apresentacao-noir" + todas as dependências (Windows / PowerShell)
# Uso (na raiz do repositório):  powershell -ExecutionPolicy Bypass -File installer\install.ps1
# Opções: -SkipAgentReach (não instala pesquisa web) | -Force (reinstala ppt-master mesmo se já existir)
param([switch]$SkipAgentReach,[switch]$Force)
$ErrorActionPreference = "Stop"
$repo   = Split-Path -Parent $PSScriptRoot
$claude = Join-Path $env:USERPROFILE ".claude"
$skills = Join-Path $claude "skills"
New-Item -ItemType Directory -Force -Path $skills | Out-Null

function Need($cmd,$hint){ if(-not (Get-Command $cmd -ErrorAction SilentlyContinue)){ throw "Falta '$cmd'. $hint" } }
Write-Host "==> 1/6 Conferindo programas" -ForegroundColor Cyan
Need git    "Instale em https://git-scm.com"
Need python "Instale o Python 3.10+ em https://python.org (marque 'Add to PATH')"

Write-Host "==> 2/6 Bibliotecas Python" -ForegroundColor Cyan
python -m pip install --upgrade pip | Out-Null
python -m pip install Pillow numpy python-pptx lxml fonttools "markitdown[pptx]"

Write-Host "==> 3/6 Skill ppt-master (hugohe3/ppt-master, MIT)" -ForegroundColor Cyan
$pm = Join-Path $skills "ppt-master"
if((Test-Path $pm) -and -not $Force){ Write-Host "    já instalada ($pm). Use -Force para reinstalar." }
else {
  $tmp = Join-Path $env:TEMP "apresentacao-apt-ppt-master"
  if(Test-Path $tmp){ Remove-Item -Recurse -Force $tmp }
  git clone --depth 1 https://github.com/hugohe3/ppt-master $tmp
  if(Test-Path $pm){ Remove-Item -Recurse -Force $pm }
  Copy-Item -Recurse (Join-Path $tmp "skills\ppt-master") $pm
  Remove-Item -Recurse -Force $tmp
}
python -m pip install -r (Join-Path $pm "requirements.txt")
python (Join-Path $pm "scripts\attribution_guard.py")
if($LASTEXITCODE -ne 0){ throw "ppt-master falhou na checagem de integridade (attribution_guard)." }

Write-Host "==> 4/6 Pesquisa na web: agent-reach + Exa (Panniantong/agent-reach, MIT)" -ForegroundColor Cyan
if($SkipAgentReach){ Write-Host "    pulado (-SkipAgentReach)" }
else {
  $venv = Join-Path $env:USERPROFILE ".agent-reach-venv"
  if(-not (Test-Path $venv)){ python -m venv $venv }
  & (Join-Path $venv "Scripts\python.exe") -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip
  & (Join-Path $venv "Scripts\agent-reach.exe") install --env=auto
  if(Get-Command npm -ErrorAction SilentlyContinue){
    npm install -g mcporter
    mcporter config add exa https://mcp.exa.ai/mcp --scope home
  } else { Write-Warning "npm não encontrado: instale o Node.js e rode 'npm i -g mcporter' + 'mcporter config add exa https://mcp.exa.ai/mcp --scope home' para a busca semântica." }
}

Write-Host "==> 5/6 Instalando a skill apresentacao-noir" -ForegroundColor Cyan
$dst = Join-Path $skills "apresentacao-noir"
if(Test-Path $dst){ Remove-Item -Recurse -Force $dst }
Copy-Item -Recurse (Join-Path $repo "skills\apresentacao-noir") $dst

Write-Host "==> 6/6 Verificações opcionais" -ForegroundColor Cyan
if(-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)){ Write-Warning "ffmpeg não encontrado (só necessário para reanalisar o vídeo do exemplo Canva): winget install Gyan.FFmpeg" }
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if(-not (Test-Path $edge)){ Write-Warning "Microsoft Edge não encontrado em $edge (usado para as prévias dos slides)." }

Write-Host ""
Write-Host "Pronto. Falta só conectar, no app do Claude, os conectores Canva e Figma (Configurações > Conectores)." -ForegroundColor Green
Write-Host "Depois abra uma nova sessão e use:  /apresentacao-noir"
