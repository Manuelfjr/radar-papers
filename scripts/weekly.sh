#!/bin/zsh
# Weekly run of Leituras θ on this Mac (launchd: ~/Library/LaunchAgents/com.manuelfjr.leituras-theta.plist).
# Builds this week's edition with Claude, keeps the last 4, pushes to GitHub Pages and shows a macOS notification.
# Usage: scripts/weekly.sh          normal run
#        scripts/weekly.sh --check  only checks auth, git and notification (no edition)
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
REPO="$HOME/Documents/projects/radar-papers"
SITE="https://manuelfjr.github.io/radar-papers/"
cd "$REPO" || exit 1
mkdir -p logs
LOG="logs/$(date +%F).log"
exec >>"$LOG" 2>&1
echo "=== $(date) ==="

notify() {  # title, message, url
  osascript -e "display notification \"$2\" with title \"$1\" sound name \"Glass\""
  [[ -n "$3" ]] && osascript -e "set r to button returned of (display dialog \"$2\" with title \"$1\" buttons {\"Depois\", \"Abrir site\"} default button 2 giving up after 14400)" -e "if r is \"Abrir site\" then open location \"$3\"" &
}

MONDAY=$(python3 -c "import datetime as d;t=d.date.today();print(t-d.timedelta(days=t.weekday()))")

if [[ "$1" == "--check" ]]; then
  git fetch -q origin && echo "git ok"
  claude -p "Responda só: ok" --model claude-sonnet-5-5 && echo "claude ok"
  notify "Leituras θ" "Teste: as notificações estão funcionando." "$SITE"
  exit 0
fi

git pull -q --rebase origin main || { notify "Leituras θ" "Falhou o git pull. Veja $REPO/$LOG"; exit 1; }
if python3 -c "import json,sys;sys.exit(0 if any(i['id']=='$MONDAY' for i in json.load(open('data/issues.json'))['issues']) else 1)"; then
  echo "edição $MONDAY já existe; nada a fazer"; exit 0
fi

PROMPT="Você produz a edição semanal da newsletter \"Leituras θ\" neste repositório. A edição desta semana tem id e date = $MONDAY.
1. Leia CURADORIA.md inteiro (leitor, buscas, critérios, tom em português do Brasil, formato JSON) e data/issues.json (maior number e IDs já publicados).
2. Rode python3 scripts/arxiv_candidates.py 8 para os candidatos dos últimos dias. Use WebSearch e WebFetch (inclusive https://huggingface.co/papers) para completar, sobretudo a seção llm.
3. Para cada candidato promissor, leia https://arxiv.org/abs/<id> com WebFetch e confirme título, autores e data. Nunca invente papers, IDs, autores ou números.
4. Escolha de 7 a 9 papers pelos critérios, com exatamente um destaque, sem repetir IDs já publicados. Insira a edição como PRIMEIRO elemento de issues em data/issues.json, com number = maior existente + 1.
5. Rode python3 scripts/prune_issues.py 4 e depois python3 -c \"import json;json.load(open('data/issues.json'))\" para validar.
6. git add data/issues.json && git commit -m \"Edição nº N ($MONDAY)\" && git push origin main
7. Termine com uma linha só: o número da edição e o título do destaque."

claude -p "$PROMPT" --model claude-sonnet-5-5 \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "WebFetch" "WebSearch" \
    "Bash(python3 scripts/*)" "Bash(python3 -c *)" "Bash(git add *)" "Bash(git commit *)" "Bash(git push *)" "Bash(git status*)" "Bash(git diff*)" "Bash(date*)"
STATUS=$?

NUM=$(python3 -c "import json;i=json.load(open('data/issues.json'))['issues'][0];print(i['number'] if i['id']=='$MONDAY' else '')")
if [[ $STATUS -eq 0 && -n "$NUM" ]] && ! git status -sb | head -1 | grep -q ahead; then
  notify "Leituras θ nº $NUM" "A edição da semana saiu: papers novos em IRT e avaliação de LLMs." "$SITE#/$MONDAY"
else
  notify "Leituras θ" "A edição desta semana não foi publicada. Veja $REPO/$LOG"
fi
