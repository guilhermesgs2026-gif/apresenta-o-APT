# Apresentação APT: skill `apresentacao-noir` para o Claude

Skill do Claude Code / Claude Desktop que cria ou **reestiliza apresentações PPTX editáveis** no estilo *noir editorial* do modelo Canva
["Apresentação Preta de Relatório de Estratégias Digitais Estilo Moderno Elegante"](https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/).
Serve para **qualquer assunto**: vendas, marketing, relatórios, projetos, institucional.

## Dois modos
1. **Tema novo**: "faz uma apresentação sobre vendas de carro". O Claude pede o logo, a cor de acento e o conteúdo, gera objetos 3D do tema pelo Canva e monta o PPTX.
2. **Reestilizar**: você envia um PPTX e o Claude preserva o conteúdo (textos, gráficos, tabelas, imagens) e o redesenha nesse estilo.

## O que você ganha
- Fundo preto, títulos entre parênteses (glifos reais), números grandes, gráficos de linha fina, um único acento de cor, sem cartões.
- Fontes **idênticas ao modelo Canva** (Open Sauce, Open Sauce Light, Space Mono), **embutidas** no PPTX.
- Objeto 3D cromado parado atrás do título, com camada iridescente de entrada (como no modelo).
- Animações no ritmo do modelo (tudo aparece em ≈1,3 s) e transições em fade.
- Slides: capa, divisor, conteúdo (até 5 KPIs + até 3 painéis: linha, barras, rosca, tabela, lista, texto, imagem, número) e fechamento.
- Tudo calculado a partir de um `deck.json`; o pipeline valida (checker do ppt-master, validação estrutural do PPTX) e entrega o arquivo.
- Biblioteca de objetos 3D pronta: carro, roda, torre de transmissão, transformador, disjuntor, isoladores, capacete. Novos objetos pelo Canva (passo a passo no `SKILL.md`).

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
5. copia a skill `apresentacao-noir` para `~/.claude/skills/`;
6. avisa o que falta (ffmpeg, Edge).

**Manual (uma vez):** no app do Claude, conecte os conectores **Canva** e **Figma** (Configurações → Conectores). O Canva gera os objetos 3D novos; o Figma só é usado se você autorizar (gasta créditos).

## Uso
Abra uma sessão nova e escreva:
> /apresentacao-noir faz uma apresentação sobre vendas de carro do 3º trimestre

ou
> /apresentacao-noir deixa esta apresentação nesse estilo: C:\...\minha.pptx

O Claude conduz: pede o logo e o que faltar, monta o `deck.json`, gera as prévias, roda o pipeline e entrega em `<pasta>\entrega\<nome>.pptx`.

## Estrutura do repositório
```
installer/                       install.ps1 e install.sh (instalam dependências + skill)
skills/apresentacao-noir/
  SKILL.md                       instruções que o Claude segue (entrevista, esquema, design, animações, QA)
  scripts/
    noir_build.py / noir_lib.py  deck.json -> SVGs no estilo noir (capa, divisor, conteúdo, fechamento)
    noir_pipeline.py             pipeline completo até o PPTX (ppt-master, animações, fontes embutidas, validação)
    noir_specs.py                design_spec.md e spec_lock.md genéricos
    extract_pptx.py              PPTX existente -> rascunho de deck.json (modo reestilizar)
    prepare_logo.py              prepara o logo (fundo transparente, versão clara, cor de acento)
    make_object.py               PNG do Canva -> objeto 3D da biblioteca (alpha + camada iridescente)
    embed_fonts.py, shot2.py     fontes embutidas e prévia fiel dos slides
  assets/fonts/                  Open Sauce, Open Sauce Light, Space Mono (SIL OFL)
  assets/objects/                biblioteca de objetos 3D (PNG com alpha + _fx)
  reference/ESTILO_CANVA.md      análise medida do modelo Canva (fontes, tamanhos, cores, animação)
  reference/canva-exemplo/       onde ficam os exports do modelo (veja o README da pasta)
```

## Exemplo do Canva (base de estilo)
A skill sempre se baseia no modelo do Canva: [link do template](https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/)
e na análise em `skills/apresentacao-noir/reference/ESTILO_CANVA.md` (fontes, tamanhos, opacidade do objeto, tempos de animação medidos quadro a quadro).
Os exports (`.mp4`/`.pptx`) do template **não estão neste repositório público**, por serem conteúdo do Canva; recrie-os com o conector Canva (instruções em `reference/canva-exemplo/README.md`).

## Avisos
- Não testado no PowerPoint real: a validação é estrutural e por prévia dos SVGs. Abra e confira antes de enviar.
- Fontes embutidas: Open Sauce e Space Mono (SIL Open Font License); valem no PowerPoint.
- Terceiros: ppt-master (MIT) e agent-reach (MIT) são baixados dos repositórios originais na instalação.
- Os objetos 3D foram gerados com IA do Canva; confira a licença de uso do Canva para o seu caso.
