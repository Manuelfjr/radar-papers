# Guia de curadoria — Leituras θ

Este arquivo é lido pela rotina semanal. Edite-o para mudar o foco, as buscas ou os critérios.

## Para quem é

Pesquisador da Kunumi (mestrado na UFPE) que aplica Teoria de Resposta ao Item (IRT) e Cultural Consensus Theory à avaliação de ML e LLMs: dificuldade e discriminação de itens de benchmark, habilidade latente de modelos, itens suspeitos ou mal rotulados em benchmarks (CLAIRE), sabedoria das multidões. Está entrando mais fundo em LLMs e avaliação de LLMs em geral. Publica em NeurIPS (D&B), ICML, ACL/ARR, IJCAI, AISTATS, IMPS.

## O que procurar (papers submetidos ao arXiv nos últimos 7 dias)

1. **IRT e psicometria para ML** (seção `irt`): IRT, Rasch, testes adaptativos, modelos de medida, CCT, agregação de anotadores e discordância, dificuldade de itens, validade de benchmarks medida com ferramentas psicométricas.
2. **Avaliação de LLMs** (seção `avaliacao`): novos benchmarks e críticas a benchmarks, contaminação, LLM-as-a-judge, saturação, avaliação eficiente (poucos itens), confiabilidade e incerteza das métricas, leaderboards, avaliação de agentes.
3. **LLMs: vale conhecer** (seção `llm`): resultados amplos de LLMs com impacto real (raciocínio, escalonamento, interpretabilidade, alinhamento), de preferência com ligação à avaliação.

Buscas sugeridas na API do arXiv (`http://export.arxiv.org/api/query?search_query=...&sortBy=submittedDate&sortOrder=descending&max_results=50`), ou rode `python3 scripts/arxiv_candidates.py`:
- `all:"item response theory"`, `all:psychometric AND (all:"language model" OR all:"machine learning")`, `all:"adaptive testing"`, `all:"cultural consensus"`, `all:"annotator disagreement"`
- `all:benchmark AND all:"language models" AND all:evaluation`, `all:"LLM-as-a-judge"`, `all:contamination AND all:benchmark`, `all:"efficient evaluation"`
- Para a seção `llm`: Hugging Face Daily Papers (https://huggingface.co/papers) e os mais comentados da semana.

## Critérios de seleção

- **7 a 9 papers.** Cerca de 3 `irt`, 3 `avaliacao`, 2 `llm`, mais 1 `destaque` (o melhor da semana, de qualquer seção).
- Prefira o que é **inovador ou surpreendente**: método novo, resultado que contraria o senso comum, benchmark ou ferramenta útil, crítica bem fundamentada. Evite incrementais e aplicações rotineiras.
- `novelty` de 1 a 5: 5 = muda como se faz algo; 3 = contribuição sólida; 1 = só relevante pelo tema.
- **Nunca invente** papers, IDs, autores ou resultados. Confira cada paper na página `arxiv.org/abs/<id>` e confirme que a data está na janela.
- Não repita papers que já saíram nas edições guardadas em `data/issues.json` (o site guarda só as 4 últimas).
- Se a semana estiver fraca em `irt`, tudo bem incluir menos; não force.

## Texto (português do Brasil)

- `intro`: 2 a 3 frases sobre o tema da semana, direto, sem clichê.
- `tldr`: 1 a 2 frases. O que o paper faz e o principal resultado, com número quando houver.
- `why`: 1 a 2 frases. Por que importa para quem usa IRT para avaliar LLMs, ou como poderia usar no próprio trabalho.
- Títulos ficam no original em inglês. Autores: no máximo 4, depois `"et al."`.

## Formato de cada edição (adicionar no início de `issues` em `data/issues.json`)

```json
{
  "id": "AAAA-MM-DD", "date": "AAAA-MM-DD", "number": N,
  "intro": "...",
  "papers": [
    {"title": "...", "authors": ["..."], "arxiv_id": "2610.01234",
     "url": "https://arxiv.org/abs/2610.01234", "pdf": "https://arxiv.org/pdf/2610.01234",
     "published": "AAAA-MM-DD", "section": "destaque|irt|avaliacao|llm",
     "tags": ["IRT", "benchmarks"], "tldr": "...", "why": "...", "novelty": 4}
  ]
}
```
`id` e `date` = data da segunda-feira do envio. `number` = maior número existente + 1 (a numeração continua mesmo depois que edições antigas são apagadas). Exatamente um paper com `section: "destaque"`.

Depois de adicionar a edição, rode `python3 scripts/prune_issues.py 4`: o site guarda só as 4 edições mais recentes e apaga as anteriores.
