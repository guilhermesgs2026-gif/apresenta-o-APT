---
name: dorea-ppt
description: Cria ou reestiliza apresentações PPTX editáveis no estilo "noir editorial" do modelo Canva do Guilherme (fundo preto, títulos entre parênteses, objetos 3D cromados parados atrás do título, fontes Open Sauce e Space Mono embutidas, gráficos de linha fina, animações rápidas de ~1,3 s). Serve para QUALQUER assunto (vendas, marketing, relatórios, projetos). Use quando o usuário pedir uma apresentação "no estilo Canva preto / noir / igual ao exemplo", disser "/dorea-ppt" ou "usa a skill dorea-ppt", pedir "faz uma apresentação sobre X com esse estilo" ou enviar um PPTX para "deixar nesse estilo". Pede o logo, gera objetos 3D do tema pelo Canva e entrega PPTX nativo validado.
---

# Apresentação Noir (qualquer assunto)

Resultado aprovado pelo usuário: PPTX nativo e editável, fundo **#000000**, títulos `(ENTRE PARÊNTESES)` com glifos reais, números grandes, gráficos de linha fina, um único acento de cor, objeto 3D cromado parado atrás do título e animações no ritmo do modelo Canva.
Referências obrigatórias: `reference/ESTILO_CANVA.md` (fontes, tamanhos, cores, tempos medidos do modelo Canva) e, se existirem localmente, `reference/canva-exemplo/*` (vídeo e PPTX do modelo). Modelo: https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/

## Dois modos
**A. Tema novo** ("faz uma apresentação sobre vendas de carro"): conteúdo vem do pedido/arquivos do usuário.
**B. Reestilizar** (usuário envia um PPTX): preservar todo o conteúdo e redesenhar no estilo.

## 0. Pré-requisitos
`ppt-master` em `~/.claude/skills/ppt-master` (o instalador do repositório instala), Python com Pillow numpy python-pptx lxml fonttools, Edge para prévias (`shot2.py`). Conector Canva para objetos 3D novos (Figma só se o usuário autorizar: gasta créditos).

## 1. Entrevista rápida (perguntar só o que falta, tudo de uma vez)
1. **Logo** (arquivo). Sempre pedir; nunca recriar logo de terceiros. Sem logo: usar o nome da organização em texto (`meta.org`).
2. **Assunto, público e objetivo**; idioma (padrão pt-BR); **cor de acento** (padrão: a cor saturada do logo, ou laranja #F7941D).
3. **Conteúdo e dados** (números reais; nunca inventar). Se o usuário só deu o tema, propor a estrutura (resumo, seções, dados) e confirmar antes de gerar; marcar dados fictícios como "exemplo".
4. Objetos 3D: biblioteca (`assets/objects`: carro, roda, torre-transmissao, transformador, disjuntor, isoladores, capacete) ou **gerar novos** pelo Canva (seção 4).

## 2. Fluxo (executar na ordem)
```
python scripts/prepare_logo.py <logo> <pasta>/logo.png --white     # fundo transparente; --white deixa partes cinza/pretas brancas; imprime acento sugerido
(modo B)  python scripts/extract_pptx.py <enviada.pptx> <pasta>     # rascunho de deck.json + imagens extraídas
escrever/revisar <pasta>/deck.json                                   # esquema na seção 3
python scripts/noir_build.py <pasta>/deck.json <pasta>               # só SVGs; prévia: python scripts/shot2.py <pasta>/svg <pasta>/shots   (abrir os PNG!)
python scripts/noir_pipeline.py <pasta>/deck.json <pasta> --name <nome>   # tudo: projeto ppt-master, spec/lock, animações, checker, export, fontes embutidas, validação
```
Saída: `<pasta>/entrega/<nome>.pptx`. O pipeline para com a lista de erros se o checker reprovar (texto longo demais, itens demais): encurtar no deck.json e repetir. Se o arquivo estiver aberto no PowerPoint ele salva como `_v2`.
Sempre olhar as prévias (capa, divisor, 1 slide de dados, tabela, fechamento) antes de entregar.

## 3. Esquema do deck.json
```json
{"meta":{"title":"","name":"arquivo","org":"","lang":"pt-BR","accent":"#F7941D","logo":"C:/.../logo.png","topbar":"texto no topo","footer":"rodapé",
         "objects":["carro","roda"],"audience":"","intent":"","core":""},
 "slides":[
  {"type":"cover","title":"VENDAS","overlay":"3º trimestre","subtitle":"...","object":"carro","meta":[["Período","Jul a set"],["Unidades","1.248"]]},
  {"type":"divider","title":"REGIÕES","overlay":"Desempenho","kicker":"Seção 01","object":"auto","meta_left":["Período","Jul a set"]},
  {"type":"content","kicker":"Resumo","title":"Frase-conclusão do slide (até 2 linhas)",
   "kpis":[{"label":"Unidades","value":"1.248","sub":"+12% vs 2T","hl":true}],
   "panels":[{"type":"line","title":"","cats":[],"vals":[],"weight":1},{"type":"bars","cats":[],"vals":[]}]},
  {"type":"closing","title":"OBRIGADO","overlay":"Empresa","lines":["linha 1","linha 2","linha 3"],"object":"auto"}]}
```
- `content`: até **5 KPIs** (value curto; ≤ ~10 caracteres a 64 px) e até **3 painéis** lado a lado (`weight` = largura relativa). Tipos de painel: `line` (cats, vals, hi), `bars` (lollipop horizontal, até ~8 itens), `donut` (parts [[rótulo, valor, cor?]]), `table` (headers, rows, `status:{col,thresholds,good:"high"|"low"}` pinta bolinha verde/amarela/vermelha), `bullets` (items, até ~5), `text` (body), `stat` (value,label,sub), `image` (src, caption).
- `cover.title`/`divider.title`: palavra(s) curta(s) em MAIÚSCULAS (a fonte reduz sozinha: 140/120/96/72/56 px); `overlay` é a legenda espaçada sobre o título (vai abaixo se o título for longo). `object`: nome da biblioteca, `"auto"` (cicla `meta.objects`) ou `null`.
- Números em pt-BR (`1.248`, `18,4%`); `meta.lang:"en"` troca separadores. Títulos de `content` são **frases-conclusão**, não rótulos.
- Excesso: o builder corta com "…"; revise visualmente.

## 4. Objetos 3D novos (estilo do modelo: preto brilhante, monocromático)
1. Canva `generate-image`, prompt-modelo: "Photorealistic 3D render of <objeto>, glossy black chrome and dark smoked metal, monochrome black and gray, soft studio reflections, dramatic rim light, deep blacks, high-end editorial product render, pure black seamless background, no text, no logos, no color accents". 1:1 ou 3:4 (altos); 16:9 (largos). Conferir miniaturas (cortado? fino demais?) e regerar.
2. Resolução cheia (Canva só entrega miniatura de 149 px): `copy-design` do modelo (design `DAHXWAxsUzs`, ou usar o rascunho `DAHXWV3qObk`) → `read-design` com `open_transaction` → `edit-design`: `add_page` (1920×1080, fundo #000000) e `insert_fill` do asset (1080×1080, 810×1080 ou 1920×1080 centrado) → **`commit` (pedir autorização do usuário; é um rascunho)** → `export-design` PNG 1920×1080 `lossless` → baixar com `curl --ssl-no-revoke -A "Mozilla/5.0"` (URLs expiram).
3. `python scripts/make_object.py <png> <nome> [<png2> <nome2> ...]` recorta, cria alpha, suaviza bordas, gera `<nome>_fx.png` (camada iridescente de entrada) e atualiza `assets/objects/aspects.json`. Depois usar `"object":"<nome>"`.
4. Objeto parado, nunca girando (o modelo Canva não gira; o movimento está nas animações de entrada). Copiar objetos úteis para o repositório da skill.

## 5. Sistema de design (não mudar sem o usuário pedir)
- Canvas 1280×720; fundo #000000; texto #FFF; secundário #9A9A9A; terciário #5C5C5C; linhas #2A2A2A. **Um acento** (`meta.accent`). Semáforo só como bolinhas (#34D399 / #FACC15 / #FB923C / #F43F5E).
- Fontes **idênticas ao modelo**: Open Sauce (títulos, números grandes, texto), Open Sauce Light (parênteses), Space Mono MAIÚSCULO (legendas, rótulos, tabelas, números pequenos). Sem negrito (só Regular embutida).
- Tamanhos declarados no spec_lock: title 40, body 18, annotation 13, kpi 64, meta 26, display 120/96/72/56, hero 140, paren 220. **Não usar outros tamanhos** (o checker reprova recorrência de tamanhos não declarados).
- Sem cartões; linhas finas; margens 56; cabeçalho: logo à esquerda + texto mono à direita; rodapé mono + "NN / TT".
- Objeto 3D com opacidade **0,62**; camada `_fx` iridescente em 0,18 em repouso (some com fade na animação).
- Cada bloco é `<g id data-pptx-bounds>`; bounds de grupos raiz **não podem se sobrepor** (checker). Hero fica numa faixa superior; `hero-fx` numa faixa livre.

## 6. Animações (medidas do vídeo do modelo; `noir_pipeline.gen_anim`)
Tudo aparece em ≤ ~1,3 s e fica parado. Capa/divisor/fechamento: logo fade 0,2 s; título+parênteses `entrance_split` 0,3 s @0,3; objeto `entrance_faded_zoom` 0,5 s @0,35; camada `_fx` mesmo efeito + `exit_fade` 0,4 s @0,9; legendas fade 0,2 s. Conteúdo: header fade 0,2; KPIs fade 0,2 (+0,04 s cada); painéis `entrance_wipe` 0,25 s. Transição: fade 0,35 s. Não voltar a efeitos lentos (rise-up de 0,4 s e delays longos foram considerados lentos).

## 7. QA final (sempre)
- `noir_pipeline` chegou a "PRONTO" (checker exit 0, validate "All validations PASSED"); 100% dos slides com `<p:transition>` e `<p:timing>`; 3 fontes embutidas; tema Open Sauce; fundo `#000000`.
- Conferir números e textos com a fonte do usuário; nada inventado; títulos como frases-conclusão.
- Prévias sem sobreposição título/legenda, rótulos cortados, valores estourando o card.
- Avisar: não abri no PowerPoint real; a camada `_fx` aparece levemente na edição; fontes embutidas só valem no PowerPoint (Windows/Mac recente); animações só em modo apresentação.

## 8. Armadilhas
- `rm -rf` com glob relativo é bloqueado: use caminho absoluto ou não apague.
- Criar arquivos com a ferramenta Write (heredoc com aspas/`\'` quebra o Bash).
- `curl` precisa de `--ssl-no-revoke` e `-A "Mozilla/5.0"`; URLs de export expiram em horas.
- Edge headless trava: `shot2.py` já usa `--user-data-dir` único e `--virtual-time-budget`.
- SVG: sem `<style>`/`class`/entidades HTML; `letter-spacing` e `opacity` em `<image>` funcionam; texto multilinha = um `<text>` com `<tspan x dy>`.
- Se `project_manager.py init` rodar com cwd estranho, o projeto vai para `~/.claude/projects/<nome>_<data>` (normal).
- Arquivo PPTX aberto no PowerPoint não pode ser sobrescrito: usar novo sufixo.
