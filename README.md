# Apresentação APT: skill `apresentacao-noir-sgs` para o Claude

Skill do Claude Code / Claude Desktop que cria apresentações **PPTX editáveis de nível topo** no estilo *noir editorial* do modelo Canva
["Apresentação Preta de Relatório de Estratégias Digitais Estilo Moderno Elegante"](https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/),
aplicado a relatórios de **fiscalização de obras elétricas** (SGS Enger Engenharia para ISA Energia Brasil).

Cada uso gera **dois arquivos**: o relatório **consolidado** (≈16 slides) e o **modelo com a estrutura original** do painel (≈32 slides).

## O que você ganha
- Fundo preto, títulos entre parênteses, números gigantes, gráficos de linha fina, sem cartões.
- Fontes **idênticas ao modelo Canva** (Open Sauce, Open Sauce Light, Space Mono), **embutidas** no PPTX.
- Objetos 3D cromados de subestação (torre, transformador, disjuntor, isoladores, capacete) com camada iridescente de entrada.
- Animações no mesmo ritmo do modelo (tudo aparece em ≈1,3 s) e transições em fade.
- Logo da SGS sem fundo; semáforo de risco; totais conferidos contra a fonte.
- Fluxo completo e verificado: SVG → ppt-master → PPTX nativo → fontes embutidas → validação.

## Instalação (instala tudo junto)
Windows (PowerShell), na pasta do repositório:
```powershell
git clone https://github.com/guilhermesgs2026-gif/apresenta-o-APT
cd apresenta-o-APT
powershell -ExecutionPolicy Bypass -File installer\install.ps1
```
macOS / Linux:
```bash
git clone https://github.com/guilhermesgs2026-gif/apresenta-o-APT && cd apresenta-o-APT
bash installer/install.sh
```
O instalador:
1. confere `git` e `python` (3.10+);
2. instala as bibliotecas Python (`Pillow numpy python-pptx lxml fonttools markitdown`);
3. instala a skill **ppt-master** ([hugohe3/ppt-master](https://github.com/hugohe3/ppt-master), MIT) e roda a checagem de integridade dela;
4. instala o **agent-reach** + Exa ([Panniantong/agent-reach](https://github.com/Panniantong/agent-reach), MIT) para pesquisa na web (`-SkipAgentReach` / `--skip-agent-reach` pula);
5. copia a skill `apresentacao-noir-sgs` para `~/.claude/skills/`;
6. avisa o que falta (ffmpeg, Edge).

**Manual (uma vez):** no app do Claude, conecte os conectores **Canva** e **Figma** (Configurações → Conectores). O Canva gera os objetos 3D; o Figma só é usado se você autorizar (gasta créditos).

## Uso
Abra uma sessão nova e escreva `/apresentacao-noir-sgs`, por exemplo:
> /apresentacao-noir-sgs monta o relatório da semana de 12/10 a 18/10 com este PPTX do painel: C:\...\apresentacao-semanal-sgi.pptx

A skill lê o PPTX, gera as duas versões, valida e entrega em `Documents\<deck>\entrega\`.

## Estrutura do repositório
```
installer/                       install.ps1 e install.sh (instalam dependências + skill)
skills/apresentacao-noir-sgs/
  SKILL.md                       instruções que o Claude segue (fluxo, design, animações, QA)
  scripts/                       gerador de slides (nl.py, deckN.py), specs, animações, fontes embutidas...
  assets/                        fontes (OFL), objetos 3D, logo SGS, dados de exemplo (anonimizados)
  reference/ESTILO_CANVA.md      análise medida do modelo Canva (fontes, tamanhos, cores, animação)
  reference/canva-exemplo/       onde ficam os exports do modelo (veja o README da pasta)
```

## Exemplo do Canva (base de estilo)
A skill sempre se baseia no modelo do Canva: [link do template](https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/)
e na análise em `skills/apresentacao-noir-sgs/reference/ESTILO_CANVA.md` (fontes, tamanhos, opacidade do objeto, tempos de animação medidos quadro a quadro).
Os exports (`.mp4`/`.pptx`) do template **não estão neste repositório público**, por serem conteúdo do Canva; recrie-os com o conector Canva (instruções em `reference/canva-exemplo/README.md`).

## Avisos
- Os dados em `assets/example_data.json` são **anonimizados** (contratadas e projetos trocados por nomes genéricos). Não suba dados reais de clientes neste repositório público.
- Fontes embutidas: Open Sauce e Space Mono (SIL Open Font License).
- Não testado no PowerPoint real: a validação é estrutural (validate.py) e por prévia dos SVGs. Abra e confira antes de enviar.
- Terceiros: ppt-master (MIT) e agent-reach (MIT) são baixados dos repositórios originais na instalação.
