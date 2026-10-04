// Leituras θ — renders data/issues.json: #/ = latest edition, #/AAAA-MM-DD = one edition, search/tags filter across all.
const SECTIONS = [
  ["irt", "IRT e psicometria para ML"],
  ["avaliacao", "Avaliação de LLMs"],
  ["llm", "LLMs: vale conhecer"],
];
const MONTHS = ["jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."];
const $main = document.getElementById("main");
const $q = document.getElementById("q");
let ISSUES = [];
let tagFilter = "";

const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmtDate = iso => { const [y, m, d] = iso.split("-").map(Number); return `${d} ${MONTHS[m - 1]} ${y}`; };

function paperCard(p, opts = {}) {
  const feat = p.section === "destaque" && !opts.plain;
  const s = p.section === "destaque" ? (p.tags || []).some(t => /irt|psicom/i.test(t)) ? "irt" : "avaliacao" : p.section;
  const nov = Array.from({ length: 5 }, (_, i) => `<i class="${i < (p.novelty || 0) ? "on" : ""}"></i>`).join("");
  return `<article class="paper${feat ? " feat" : ""}" data-s="${esc(s)}">
    ${feat ? `<span class="eyebrow">Destaque da semana</span>` : ""}
    <h3><a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.title)}</a></h3>
    <p class="authors">${esc((p.authors || []).join(", "))}</p>
    <p class="tldr">${esc(p.tldr)}</p>
    <p class="why"><b>Por que importa:</b> ${esc(p.why)}</p>
    <div class="meta">
      <div class="tags">${(p.tags || []).map(t => `<button class="tag" type="button" data-tag="${esc(t)}">${esc(t)}</button>`).join("")}</div>
      <div class="links">
        <span class="nov" title="Novidade: ${p.novelty || 0} de 5" aria-label="Novidade ${p.novelty || 0} de 5">${nov}</span>
        <span class="mono">${esc(p.arxiv_id)}</span>
        ${p.pdf ? `<a href="${esc(p.pdf)}" target="_blank" rel="noopener">PDF</a>` : ""}
        <a href="${esc(p.url)}" target="_blank" rel="noopener">arXiv →</a>
      </div>
    </div>
    ${opts.from ? `<span class="from">Edição nº ${opts.from.number} · ${fmtDate(opts.from.date)}</span>` : ""}
  </article>`;
}

function archive(currentId) {
  return `<section class="section"><div class="section-head">Edições</div>
    <nav class="archive">${ISSUES.map(i => `<a href="#/${i.id}"${i.id === currentId ? ' aria-current="page"' : ""}>
      <span class="n mono">nº ${String(i.number).padStart(2, "0")}</span>
      <span class="t">${esc(i.intro)}</span>
      <span class="d mono">${fmtDate(i.date)}</span></a>`).join("")}</nav></section>`;
}

function renderIssue(issue) {
  const idx = ISSUES.indexOf(issue);
  const newer = ISSUES[idx - 1], older = ISSUES[idx + 1];
  const feat = issue.papers.find(p => p.section === "destaque");
  const groups = SECTIONS.map(([k, label]) => {
    const ps = issue.papers.filter(p => p.section === k);
    if (!ps.length) return "";
    return `<section class="section" style="--c:var(--${k === "avaliacao" ? "eval" : k})"><div class="section-head"><span class="dot"></span>${label}</div>${ps.map(p => paperCard(p)).join("")}</section>`;
  }).join("");
  $main.innerHTML = `
    <section class="mast">
      <div class="mast-row"><span><b>Edição nº ${issue.number}</b> · ${fmtDate(issue.date)}</span>
        <span class="pager">${older ? `<a href="#/${older.id}">← anterior</a>` : ""}${newer ? `<a href="#/${newer.id}">próxima →</a>` : ""}</span></div>
      <h2>${esc(issue.intro)}</h2>
      <div class="mast-row"><span>${issue.papers.length} papers</span></div>
    </section>
    ${feat ? paperCard(feat) : ""}
    ${groups}
    ${archive(issue.id)}`;
}

function renderSearch(q) {
  const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
  const hits = [];
  for (const i of ISSUES) for (const p of i.papers) {
    const hay = [p.title, p.tldr, p.why, ...(p.authors || []), ...(p.tags || [])].join(" ").toLowerCase();
    const tagOk = !tagFilter || (p.tags || []).includes(tagFilter);
    if (tagOk && terms.every(t => hay.includes(t))) hits.push(paperCard(p, { plain: true, from: i }));
  }
  const label = [tagFilter && `tag <b>${esc(tagFilter)}</b>`, q && `“${esc(q)}”`].filter(Boolean).join(" + ");
  $main.innerHTML = `<div class="filter-note"><span>${hits.length} resultado${hits.length === 1 ? "" : "s"} para ${label}</span><button type="button" id="clear">Limpar</button></div>
    <section class="section">${hits.join("") || `<p class="empty">Nada encontrado nas edições publicadas.</p>`}</section>`;
}

function route() {
  const q = $q.value.trim();
  if (q || tagFilter) return renderSearch(q);
  const id = location.hash.replace(/^#\/?/, "");
  const issue = ISSUES.find(i => i.id === id) || ISSUES[0];
  if (!issue) { $main.innerHTML = `<p class="empty">A primeira edição sai na próxima segunda.</p>`; return; }
  renderIssue(issue);
}

$main.addEventListener("click", e => {
  const tag = e.target.closest("[data-tag]");
  if (tag) { tagFilter = tag.dataset.tag; route(); window.scrollTo({ top: 0, behavior: "smooth" }); }
  if (e.target.id === "clear") { tagFilter = ""; $q.value = ""; route(); }
});
$q.addEventListener("input", route);
window.addEventListener("hashchange", () => { tagFilter = ""; $q.value = ""; route(); window.scrollTo(0, 0); });

// theme toggle, remembered per browser
const root = document.documentElement;
try { const t = localStorage.getItem("theme"); if (t) root.dataset.theme = t; } catch {}
document.getElementById("theme").addEventListener("click", () => {
  const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = dark ? "light" : "dark";
  try { localStorage.setItem("theme", root.dataset.theme); } catch {}
});

fetch(`data/issues.json?v=${Date.now()}`)
  .then(r => r.json())
  .then(d => { ISSUES = (d.issues || []).sort((a, b) => b.date.localeCompare(a.date)); route(); })
  .catch(() => { $main.innerHTML = `<p class="empty">Não consegui carregar as edições.</p>`; });
