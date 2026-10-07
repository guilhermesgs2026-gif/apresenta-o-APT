# Estilo do exemplo Canva (fonte da verdade visual)

Modelo: "Apresentação Preta de Relatório de Estratégias Digitais Estilo Moderno Elegante" (Canva Creative Studio)
Link: https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/

Arquivos locais (NÃO versionados no repositório público, por serem conteúdo do template do Canva): `canva_ref.mp4`, `canva_ref.pptx` e `sheet*.png`. Para recriá-los: com o conector Canva, faça `copy-design` do modelo, depois `export-design` em `mp4` e `pptx` e salve nesta pasta (`reference/canva-exemplo/`).
- `canva_ref.mp4`: export em vídeo das páginas 1, 3 e 4 do modelo (15 s, 1280×720, 30 fps; 5 s por página).
- `canva_ref.pptx`: export PPTX do modelo (mostra fontes, tamanhos e posições reais; as fontes vão embutidas).
- `sheet_entry.png`: 12 quadros da entrada da capa (0,10 s a 1,20 s).
- `sheet1.png` / `sheet2.png`: quadros da capa e do slide "Desempenho".

Sempre que for criar ou revisar uma apresentação, **comparar com estes arquivos**. Para reanalisar: `python scripts/analisar_exemplo.py`.

## Fontes (lidas do PPTX do Canva)
| Uso | Fonte | Tamanho no Canva (1920 px) | Equivalente em 1280 px |
|---|---|---|---|
| Título grande (RELATÓRIO, DESEMPENHO) | Open Sauce Regular | 152,8 pt (≈204 px) | ≈136 px |
| Parênteses "(" e ")" | Open Sauce Light, espaçamento −0,02 em | 254,5 pt (≈339 px) | ≈226 px |
| Legenda sobre o título (REDES SOCIAIS) | Open Sauce, espaçamento ≈0,8 em | 20,9 pt | ≈18 px |
| Título de slide de dados "(VISÃO GERAL)" | Open Sauce | 68,2 pt | ≈45 px |
| Textos pequenos, parágrafos, rótulos, dados | Space Mono, MAIÚSCULO | 13,9 pt | ≈12 px |
| Logo do exemplo | Helios Extended | 26,4 pt | (não usado: use o logo do cliente) |

## Cores
Fundo preto puro `#000000`; texto `#E8ECEC` / `#FFFFFF`; objeto 3D com **opacidade 0,62** atrás do título; gráficos em linhas brancas finas com pontos; sem cartões nem caixas.

## Layout (capa, slide 1)
Logo no canto superior esquerdo; título enorme centralizado com parênteses colados; legenda espaçada sobreposta ao título com faixa preta atrás; 4 blocos de texto mono na base; objeto 3D cromado e escuro atrás do título.

## Animação (medida quadro a quadro)
Capa: logo 0,0–0,3 s; parênteses 0,4–0,6 s abrem do centro para fora; título 0,3–0,7 s revelado de dentro para fora; objeto 3D 0,4–1,0 s cresce com fade e brilho iridescente (verde/roxo/rosa) que depois assenta no cromado; textos pequenos em sequência 0,3–1,2 s. Depois tudo fica parado até o fim da página; saída em 4,1–4,6 s (fade) e a próxima página entra a partir do preto.
Slide de dados: logo 0,05–0,45 s; gráfico 0,45–0,65 s; título 0,7–0,85 s; parágrafo 1,05–1,85 s. Ritmo total ≈1,3 s.

## Objetos 3D
Renders fotorrealistas escuros, brilhantes, monocromáticos (peça de xadrez, óculos, mão robótica) sobre preto, com reflexos suaves. São imagens paradas; o movimento vem das animações de entrada, não de rotação.
