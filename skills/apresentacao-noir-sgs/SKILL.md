---
name: apresentacao-noir-sgs
description: Cria apresentações PPTX de nível topo no estilo "noir editorial" do modelo Canva do Guilherme (fundo preto, títulos entre parênteses, objetos 3D cromados atrás do título, fontes Open Sauce e Space Mono embutidas, animações rápidas) para relatórios da SGS Enger / ISA Energia (fiscalização de obras elétricas, inspeções, desvios, subestações). Use quando o usuário pedir "apresentação/relatório no estilo Canva preto", "igual ao exemplo", "versão consolidada" ou "modelo original" de relatório semanal SGI, ou mencionar apresentacao-noir-sgs. Entrega 2 PPTX nativos e editáveis (consolidado + estrutura original).
---

# Apresentação Noir SGS (resultado final aprovado)

Esta skill reproduz o resultado aprovado pelo usuário: dois PPTX editáveis, fundo preto, com objetos 3D de subestação, fontes do modelo Canva embutidas e animações no ritmo do exemplo.

**Modelo de referência (Canva):** https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/
**Cópia do usuário no Canva (leitura/export):** design `DAHXWAxsUzs`. Existe também uma cópia de rascunho `DAHXWV3qObk` com os 5 objetos 3D.

## Referência de estilo (consultar sempre)
Antes de criar ou revisar qualquer slide, ler `reference/ESTILO_CANVA.md` (fontes, tamanhos, cores, layout e animação medidos do modelo Canva). Se existirem localmente, comparar com `reference/canva-exemplo/canva_ref.mp4`, `canva_ref.pptx` e `sheet*.png` (não vão no repositório público; ver `reference/canva-exemplo/README.md` para recriar). Reanálise de tempos: `python scripts/analisar_exemplo.py`.

## Instalação (repositório https://github.com/guilhermesgs2026-gif/apresenta-o-APT)
`installer/install.ps1` (Windows) ou `installer/install.sh` instalam esta skill + ppt-master + agent-reach/Exa + bibliotecas Python. Conectores Canva e Figma são ligados manualmente no app do Claude.

## 0. Pré-requisitos (verificar antes de começar)
- Skill `ppt-master` em `~/.claude/skills/ppt-master` (origem: https://github.com/hugohe3/ppt-master). Se faltar: clonar e copiar `skills/ppt-master` para lá, rodar `python scripts/attribution_guard.py` (deve sair 0).
- Conectores: **Canva** (imagens 3D) e **Figma** (opcional; gera imagem mas gasta créditos, perguntar antes). Pesquisa web: `agent-reach` (venv em `~/.agent-reach-venv`, Exa via `mcporter`).
- Python com `Pillow numpy python-pptx lxml fontTools`. Edge instalado (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`) para prévia.
- Logo: usar **somente o logo da SGS** (sem fundo, versão branca em `assets/sgs_logo.png`; cinza vira branco, laranja fica). Nunca recriar logo da ISA.

## 1. O que entregar (sempre os dois)
1. **Consolidado** (≈16 slides): capa, resumo executivo, volume por regional, ritmo diário, desvios por regional, status aberto×fechado, matriz de risco consolidada, contratadas em atenção (>30%), 1 slide por regional, foco da próxima semana, obrigado. Títulos são frases-conclusão (action titles).
2. **Modelo original** (mesma estrutura do PPTX fonte, ex.: 32 slides = capa + 6 regionais × 5 [divisor, panorama, projetos, desvios, matriz] + obrigado). Textos, títulos, rótulos e números **verbatim** da fonte.
Dados de exemplo em `assets/example_data.json` estão **anonimizados** (versão pública); com o PPTX real do painel, gerar os dados reais com `scripts/parse.py` + `scripts/build_data.py` (gera `data.json`) e nunca commitar dados reais no repositório público. Conferir somas (ex.: 537 inspeções, 45 desvios). Textos de "próximos passos" são deduções dos dados: avisar o usuário.

## 2. Fluxo (executar em ordem)
1. `python ~/.claude/skills/apresentacao-noir-sgs/scripts/setup_workdir.py <pasta>` cria `<pasta>/gen`, `assets`, `images` (copia scripts, fontes, objetos 3D, logo, dados de exemplo).
2. Dados novos: `python gen/parse.py` (ajustar caminho do PPTX) e `python gen/build_data.py`; trocar `gen/example_data.py` se a estrutura mudar (precisa expor `D, PER, TI_, TD, TA, TF, TIT, IDX, dates, dvals, cons, att`).
3. **Objetos 3D (só se precisar de novos)** — ver seção 4. Os 5 prontos já estão em `assets/` (torre, transformador, disjuntor, cadeia de isoladores, capacete) com camada `_fx`.
4. Gerar SVGs: `cd gen && python deckN.py A ../out_NA` (consolidado) e `python deckN.py B ../out_NB` (original). Prévia fiel com fontes: `python shot2.py ../out_NA ../shots_NA 01 02 ...` e abrir os PNG (Read). Sempre olhar capa, 1 divisor, 1 slide de dados, matriz, fechamento.
5. Projetos ppt-master (um por deck): `python ~/.claude/skills/ppt-master/scripts/project_manager.py init <nome>` (cria em `~/.claude/projects/<nome>_<data>`).
6. `python install.py A <projetoA>` e `python install.py B <projetoB>` (escreve design_spec.md, spec_lock.md, copia SVGs e imagens usadas). Depois `python gen_anim.py <projeto>` (animations.json) e:
   - `python <ppt-master>/scripts/animation_config.py validate <projeto>`
   - `python <ppt-master>/scripts/project_manager.py validate <projeto>`
   - `python <ppt-master>/scripts/analyze_images.py <projeto>/images`
   - `python chk.py <projeto>` (checker final; precisa `exit 0`)
   - `python <ppt-master>/scripts/finalize_svg.py <projeto>` e `python <ppt-master>/scripts/svg_to_pptx.py <projeto> --no-notes`
7. **Fontes embutidas (obrigatório)**: `python embed_fonts.py <exports/arquivo.pptx> <saida>.pptx` (Open Sauce, Open Sauce Light, Space Mono, extraídas do export do modelo Canva; licenças livres).
8. Validar: `python <skills pptx>/scripts/office/validate.py <saida>.pptx` ("All validations PASSED"). Copiar para `Documents/<deck>/entrega/` com sufixo de versão. Se o arquivo estiver aberto no PowerPoint (erro "Device or resource busy"), salvar com novo sufixo `_vN`.

## 3. Sistema de design (não mudar sem o usuário pedir)
- Canvas 1280×720 (PPT 16:9). Fundo **#000000** (a versão azul-noite #060B14 foi descartada pelo usuário; preto "igual ao original"). Texto #FFFFFF; secundário #9A9A9A; terciário #5C5C5C; linhas #2A2A2A/#161616. **Um único acento: laranja SGS #F7941D** (líder do gráfico, número-herói). Semáforo só como bolinhas: verde #34D399, amarelo #FACC15, laranja #FB923C, vermelho #F43F5E (≤15% amarelo, ≤30% laranja, >30% vermelho).
- Fontes **idênticas ao modelo**: títulos e números grandes = **Open Sauce**; parênteses = **Open Sauce Light** (glifo de texto "(" e ")"); legendas, rótulos, tabelas, números pequenos = **Space Mono** MAIÚSCULO. Sem negrito (só Regular está embutida). Tema do PPTX deve sair com Open Sauce (major/minor).
- Tamanhos (px em 1280): título de slide 40; KPI 64; título-herói da capa 140; divisor/fechamento até 120 (ajustar pela largura real com `tw()`); parênteses 220; legenda sobreposta 18 com espaçamento 14; mono 12–14; rodapé 12. Declarar todos no spec_lock (`title, body, annotation, kpi, meta, display, hero, paren`).
- Sem cards: linhas finas, rótulos mono, números gigantes, gráficos de linha fina (lollipop horizontal, linha com pontos, rosca fina). Margens 56. Cabeçalho: logo SGS (sem fundo) à esquerda + texto mono à direita; rodapé mono + "NN / TT".
- Capa/divisor/fechamento ("title block"): parênteses colados ao título (medir título com PIL e as TTF), legenda espaçada sobre o título com faixa preta atrás (se a legenda for >80% da largura do título, vai abaixo, sem faixa), objeto 3D atrás a **opacidade 0,62** (a camada iridescente `_fx` em 0,18 em repouso). Objetos: capa = torre; divisores = transformador, disjuntor, cadeia de isoladores, torre (Linhas de Transmissão), transformador, disjuntor; fechamento = capacete.
- Cada bloco = `<g id data-pptx-bounds>`; grupos de nível raiz **sem sobreposição de bounds** (o checker reprova). Bounds não recortam. Hero em grupo com bounds só na faixa superior; `hero-fx` em faixa inferior livre (mesma imagem, bounds disjuntos).

## 4. Objetos 3D (estilo do modelo: preto brilhante, monocromático)
1. Gerar no Canva (`generate-image`) com prompt-modelo: "Photorealistic 3D render of <objeto>, glossy black chrome and dark smoked metal, monochrome black and gray, soft studio reflections, dramatic rim light, deep blacks, high-end editorial product render, pure black seamless background, no text, no color accents". Aspect 3:4 para altos, 1:1 para largos. Verificar miniaturas (cortados? contorno fino demais? regenerar).
2. O Canva só devolve miniatura de 149 px. Para resolução cheia: `copy-design` (DAHXWAxsUzs, página 1) → `read-design` com `open_transaction` → `edit-design`: apagar elementos e `insert_fill` de cada asset (1080×1080 ou 810×1080 centrado), `add_page` (1920×1080, fundo #000000) → `commit` (pedir autorização do usuário; a cópia é rascunho) → `export-design` PNG 1920×1080 `lossless` → baixar com `curl --ssl-no-revoke -A "Mozilla/5.0"` (URLs expiram;).
3. `python process_canva_images.py <pasta> assets images tower=tower.png ...` (recorta, alpha pela luminância, suaviza bordas, grava `aspects.json`), depois `python gen_fx.py` (camada iridescente: mapa de matiz + separação cromática). Novos nomes: incluir em `IMG`/`ASP` de `nl.py`, no `used` de `install.py` e em `HR` de `specs.py`.
4. Não usar GIF/vídeo girando: o usuário quer objeto **parado** como no modelo (o movimento está nos parênteses, título e legendas). Fallback sem Canva: `render3d.py` ray-marcher (não incluído; só se pedido).

## 5. Animações (medidas do vídeo do modelo; `gen_anim.py`)
O modelo faz tudo em ~1,3 s e depois fica parado. Tempos gravados:
- Capa/divisor: logo fade 0,2 s @0; título+parênteses `entrance_split` 0,3 s @0,3; objeto `entrance_faded_zoom` 0,5 s @0,35; `hero-fx` mesmo efeito + `exit_fade` 0,4 s @0,9; legendas fade 0,2 s @0,5 + 0,08·k.
- Slides de dados: header fade 0,2 @0,05; KPIs/cartões fade 0,2 com +0,04·k; gráficos `entrance_wipe` (direction right) 0,25 @0,3+0,05·k. Transição entre slides: fade 0,35 s. Meta: tudo aparece em ≤ ~1,3 s (média ~0,9 s). O usuário achou 0,5 s/rise-up lento: não voltar a isso.
- No Spec §I: Custom Animations = enabled. Sem animações de saída (avanço por clique).

## 6. QA final (sempre antes de entregar)
- Checker `chk.py` exit 0; `validate.py` PASSED; todas as 16/32 páginas com `<p:transition>` e `<p:timing>`; fontes no XML = Space Mono, Open Sauce Light e tema Open Sauce; 3 fontes embutidas; fundo `#000000`.
- Conferir totais contra a fonte (ex.: 537/45), nomes das regionais (Cabreúva, São Paulo, Bauru, Linhas de Transmissão, Taubaté, Baixada Santista), semáforo e legenda verbatim no modelo original.
- Olhar prévias: sem sobreposição título/overlay, parênteses alinhados, rótulos não cortados (Space Mono é largo: rótulo máx ~21 caracteres em 13 px).
- Avisar o usuário: não abri no PowerPoint; camada `_fx` aparece levemente na edição; fontes embutidas só valem no PowerPoint Windows; Segoe/Arial como fallback.

## 7. Armadilhas conhecidas
- `rm -rf` com glob relativo é bloqueado: use caminho absoluto ou não apague (avisar o usuário).
- Heredoc com aspas/`'` quebra no Bash da sessão: criar arquivos com a ferramenta Write.
- `curl` precisa de `--ssl-no-revoke` e `-A "Mozilla/5.0"` (Canva exige UA/Referer); URLs de export expiram em horas.
- Edge headless trava às vezes: usar `--user-data-dir` único por captura (já em `shot2.py`) e `--virtual-time-budget`.
- SVG: sem `<style>`, `class`, entidades HTML; `letter-spacing` como atributo funciona; `opacity` em `<image>` funciona; texto multilinha = um `<text>` com `<tspan x dy>`; nada de acento sublinhado/linha sob título.
- `data-pptx-page-role` obrigatório na raiz (cover/section/content/ending). Logo e rodapé com `data-pptx-role`.
- Nome da variável `TD` em `deckN.py` conflita com a função `TD()` do `nl.py`: dados usam `TDEV`.
- O arquivo original do usuário **não tem animações**; as animações vêm do modelo Canva.
- Não mudar a estrutura do "modelo original"; consolidar só no deck consolidado.
