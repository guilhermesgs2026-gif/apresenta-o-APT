# Exports do modelo Canva (não versionados)

Coloque aqui, localmente:
- `canva_ref.mp4`: vídeo das páginas 1, 3 e 4 do modelo;
- `canva_ref.pptx`: export PPTX (traz as fontes embutidas e os tamanhos reais);
- `sheet*.png`: contact sheets de quadros (opcional).

Como gerar (conector Canva do Claude): `copy-design` do modelo → `export-design` com `{"type":"mp4","quality":"horizontal_720p","pages":[1,3,4]}` e com `{"type":"pptx","pages":[1,3,4]}` → baixar com `curl --ssl-no-revoke -A "Mozilla/5.0"`.
Depois: `python ../../scripts/analisar_exemplo.py` mostra os tempos de entrada de cada elemento.
O template original: https://www.canva.com/pt_br/modelos/EAGp1QwF4ko-apresentacao-preta-de-relatorio-de-estrategias-digitais-estilo-moderno-elegante/
