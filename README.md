# Leituras θ

Toda segunda, uma seleção curta de papers novos do arXiv sobre teoria de resposta ao item, psicometria para ML e avaliação de LLMs, com o resumo e o porquê de cada um. Sai por e-mail e fica arquivada no site.

Site estático, sem build e sem dependências.

| Arquivo | Conteúdo |
|---|---|
| `data/issues.json` | **Dados**: todas as edições, da mais nova para a mais antiga |
| `CURADORIA.md` | Perfil, buscas e critérios usados pela rotina semanal. Edite para mudar o foco |
| `scripts/arxiv_candidates.py` | Lista os candidatos recentes do arXiv |
| `scripts/render_email.py` | Gera o e-mail (HTML com estilos inline + texto) de uma edição em `out/` |
| `index.html`, `styles.css`, `app.js` | Site: edição atual, arquivo, busca e filtro por tag |

## Rodar localmente

```bash
python3 -m http.server 8000      # site em http://localhost:8000
python3 scripts/render_email.py  # gera out/email.html da edição mais nova
```
