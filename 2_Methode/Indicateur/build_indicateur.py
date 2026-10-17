#!/usr/bin/env python3
"""Construit l'indicateur d'avancement du Programme Riemann à partir de indicateur_avancement.json.

    python 2_Methode/Indicateur/build_indicateur.py                 -> 1_Presentation/31_INDICATEUR_D_AVANCEMENT.html (liens actifs)
    python 2_Methode/Indicateur/build_indicateur.py --artefact F    -> F : variante sans liens, pour une page publiée hors du corpus

Vérifie que chaque document cité existe. À chaque version : compléter le JSON, relancer ce script.
"""
from __future__ import annotations
import html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRES = ROOT / "1_Presentation"
OUT = PRES / "31_INDICATEUR_D_AVANCEMENT.html"

def load():
    return json.loads((HERE / "indicateur_avancement.json").read_text(encoding="utf-8-sig"))

def txt(s: str) -> str:
    """Échappe, puis convertit la notation ^...^ en exposant."""
    return re.sub(r"\^([^^\s]+)\^", r"<sup>\1</sup>", html.escape(s, quote=False))

def check_links(d) -> list[str]:
    missing = []
    for e in d["etapes"]:
        for _, rel in e["documents"]:
            if not (PRES / rel).resolve().exists(): missing.append(f"{e['id']}: {rel}")
    for x in d.get("croisements", []):
        if x.get("document") and not (PRES / x["document"]).resolve().exists(): missing.append(f"croisement {x['id']}: {x['document']}")
    return missing

def topnav(current: str, prefix: str = "") -> str:
    """Common menu; four main views plus Bellman and grouped references/figures."""
    import importlib.util
    path=ROOT/'2_Methode/Pilotage/navigation.py'
    spec=importlib.util.spec_from_file_location('common_research_navigation',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.render_nav(current,prefix)


def current_research_state():
    path = ROOT / "3_Preuves_et_calculs/data/etat_recherche_courant.json"
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}

def current_status_banner(prefix: str = "") -> str:
    state = current_research_state()
    if not state: return ""
    return ('<aside data-current="v655" style="margin:14px 0;padding:10px;border:1px solid #c0d0da;font-size:.9rem">'
            'Outils de recherche réévalués en V6.55 : '
            '<a href="' + prefix + '1_Presentation/31_INDICATEUR_D_AVANCEMENT.html">évaluations</a> · '
            '<a href="' + prefix + '1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#bellman">Bellman actuel</a> · '
            '<a href="' + prefix + '00_Carte_des_idees.html">graphe relié au but</a>. '
            'Cette pièce garde le domaine et la date de ses résultats.</aside>')


def since(d, dim):
    """Première étape à partir de laquelle le niveau actuel est atteint sans interruption."""
    et = d["etapes"]; cur = et[-1]["niveaux"][dim]; k = len(et) - 1
    while k > 0 and et[k - 1]["niveaux"][dim] == cur: k -= 1
    return et[k]

CSS = r"""
/* Mise en page : feuille d'ingénieur sur papier quadrillé ; une échelle de maturité 0–9 sert de règle commune à toutes les sections */
:root {
  --paper: #f3f6f8; --sheet: #fbfcfd; --ink: #14243a; --muted: #56677a; --grid: #d8e1e8; --rule: #b9c7d3;
  --band: #eef3f7; --line: #1d5d8c; --accent: #b8650f; --ok: #2b7a57; --void: #8c96a4;
  --display: "Literata", Georgia, "Times New Roman", serif;
  --body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --paper: #0e151e; --sheet: #131c27; --ink: #e2e9f1; --muted: #98a8ba; --grid: #223142; --rule: #34485e;
    --band: #182331; --line: #6cb0e0; --accent: #e59a4a; --ok: #5ec496; --void: #6d7888; color-scheme: dark; }
}
:root[data-theme="dark"] { --paper: #0e151e; --sheet: #131c27; --ink: #e2e9f1; --muted: #98a8ba; --grid: #223142; --rule: #34485e;
  --band: #182331; --line: #6cb0e0; --accent: #e59a4a; --ok: #5ec496; --void: #6d7888; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper);
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 24px 24px; background-position: -1px -1px; color: var(--ink); font-family: var(--body); font-size: 15px; line-height: 1.55; }
.wrap { max-width: 1080px; margin: 0 auto; padding-inline: 16px; padding-block: 28px 48px; display: grid; gap: 22px; }
.topnav { display: flex; flex-wrap: wrap; gap: 4px 18px; padding-bottom: 10px; border-bottom: 1px solid var(--rule); font-size: 14px; }
.topnav a { color: var(--muted); text-decoration: none; }
.topnav a:hover, .topnav a:focus-visible { color: var(--ink); text-decoration: underline; text-underline-offset: 3px; }
.topnav a[aria-current="page"] { color: var(--ink); font-weight: 600; }
.sheet { background: var(--sheet); border: 1px solid var(--rule); border-radius: 4px; padding: 22px; min-width: 0; display: grid; gap: 14px; }
h1, h2 { font-family: var(--display); font-weight: 650; text-wrap: balance; margin: 0; letter-spacing: -0.01em; }
h1 { font-size: clamp(26px, 4.2vw, 38px); line-height: 1.15; } h2 { font-size: 22px; line-height: 1.25; }
p { margin: 0; max-width: 72ch; }
a { color: var(--line); text-underline-offset: 2px; } a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.eyebrow { font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }
.lede { color: var(--muted); font-size: 16px; }
.head { display: grid; gap: 10px; position: relative; padding-left: 18px; }
.head::before { content: ""; position: absolute; left: 0; top: 4px; bottom: 4px; width: 2px; background: var(--line); }
.mono { font-family: var(--mono); font-variant-numeric: tabular-nums; }
.foot { color: var(--muted); font-size: 12.5px; }
/* verdict */
.verdict { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }
.v { border: 1px solid var(--rule); border-radius: 4px; padding: 12px 14px; display: grid; gap: 6px; align-content: start; background: var(--paper); min-width: 0; }
.v .tag { font-family: var(--mono); font-size: 12px; letter-spacing: 0.06em; text-transform: uppercase; }
.v.up .tag { color: var(--accent); } .v.same .tag { color: var(--muted); } .v.open .tag { color: var(--void); }
.v ul { margin: 0; padding-left: 18px; display: grid; gap: 3px; }
/* petits multiples */
.multiples { display: grid; grid-template-columns: repeat(auto-fit, minmax(330px, 1fr)); gap: 14px 22px; }
.panel { min-width: 0; display: grid; gap: 2px; }
.panel h3 { margin: 0; font-family: var(--body); font-size: 14.5px; font-weight: 600; display: flex; gap: 8px; align-items: baseline; flex-wrap: wrap; }
.panel h3 .mono { color: var(--line); }
.panel .q { color: var(--muted); font-size: 12.5px; line-height: 1.35; }
.panel svg { width: 100%; height: auto; display: block; overflow: visible; }
.panel svg text { font-family: var(--mono); font-size: 10px; fill: var(--muted); }
.panel svg .day { font-size: 9px; }
.tip { position: absolute; z-index: 5; max-width: 300px; pointer-events: none; background: var(--sheet); color: var(--ink); border: 1px solid var(--rule);
  border-radius: 4px; padding: 8px 10px; font-size: 13px; line-height: 1.4; box-shadow: 0 4px 14px rgba(0,0,0,0.12); }
.tip b { font-weight: 600; }
/* tableau des versions */
.tablewrap { overflow-x: auto; }
table.hist { border-collapse: collapse; width: 100%; min-width: 760px; font-size: 13.5px; }
table.hist th { text-align: left; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; padding: 6px 8px; border-bottom: 1px solid var(--rule); }
table.hist td { padding: 9px 8px; border-bottom: 1px solid var(--grid); vertical-align: top; }
table.hist td.ver { white-space: nowrap; } table.hist td.ver b { display: block; font-weight: 600; }
table.hist td.ver span { color: var(--muted); font-size: 12.5px; }
.chg { display: flex; flex-wrap: wrap; gap: 4px; }
.chip { display: inline-block; font-family: var(--mono); font-size: 11.5px; line-height: 1.35; padding: 2px 7px; border-radius: 3px; border: 1px solid currentColor; overflow-wrap: anywhere; max-width: 100%; }
.chip.up { color: var(--accent); } .chip.ok { color: var(--ok); } .chip.open { color: var(--void); } .chip.here { color: var(--accent); } .chip.next { color: var(--line); }
.docs { display: flex; flex-wrap: wrap; gap: 3px 12px; } .docs a, .docs .doc { white-space: nowrap; } .docs .doc { font-family: var(--mono); font-size: 12px; color: var(--muted); }
table.hist col.c1 { width: 120px; } table.hist col.c2 { width: 36%; } table.hist col.c3 { width: 20%; }
/* instantané */
.legend { display: flex; flex-wrap: wrap; gap: 16px; font-size: 13px; color: var(--muted); align-items: center; }
.sw { position: relative; display: inline-block; width: 16px; height: 16px; vertical-align: -3px; margin-right: 6px; }
.dims { display: grid; gap: 4px; }
.axis, .dim { display: grid; grid-template-columns: minmax(170px, 230px) minmax(0, 1fr); gap: 14px; align-items: center; }
.axis .scale { display: grid; grid-template-columns: repeat(10, 1fr); font-family: var(--mono); font-size: 12px; color: var(--muted); } .axis .scale span { text-align: center; }
.dim { padding: 10px 0; border-top: 1px solid var(--rule); }
.dim .name b { display: block; font-weight: 600; } .dim .name small { display: block; color: var(--muted); font-size: 12.5px; line-height: 1.4; }
.track { position: relative; height: 34px; background: repeating-linear-gradient(90deg, var(--grid) 0 1px, transparent 1px 10%); border-left: 1px solid var(--rule); border-right: 1px solid var(--rule); }
.lane { position: absolute; left: 0; right: 0; top: 50%; height: 1px; background: var(--rule); }
.mk { position: absolute; top: 50%; width: 16px; height: 16px; margin-left: -8px; margin-top: -8px; border-radius: 50%; }
.mk.then { border: 2px solid var(--void); background: var(--sheet); }
.mk.now { background: var(--line); border: 2px solid var(--sheet); box-shadow: 0 0 0 1px var(--line); }
.mk.target { border: 2px dashed var(--void); background: transparent; }
.sw .mk { left: 8px; }
.mv { position: absolute; top: 50%; height: 3px; margin-top: -1.5px; background: var(--accent); }
.mv::after, .arr::after { content: ""; position: absolute; right: -2px; top: -4px; border-left: 8px solid var(--accent); border-top: 5.5px solid transparent; border-bottom: 5.5px solid transparent; }
.arr { display: inline-block; width: 26px; height: 3px; background: var(--accent); vertical-align: 4px; margin-right: 6px; position: relative; }
.note { grid-column: 2; color: var(--muted); font-size: 13px; margin-top: -2px; } .note .mono { color: var(--ink); }
/* degrés */
.degrees { overflow-x: auto; }
.deg-row { display: grid; grid-template-columns: 0.9fr 0.55fr 1.35fr 0.55fr 1.35fr 1.25fr; min-width: 920px; border: 1px solid var(--rule); border-radius: 4px; }
.deg { padding: 12px 12px 14px; border-right: 1px solid var(--rule); display: grid; gap: 7px; align-content: start; min-width: 0; }
.deg:last-child { border-right: 0; }
.deg.gap { background: repeating-linear-gradient(135deg, transparent 0 7px, var(--grid) 7px 8px); } .deg.side { background: var(--paper); }
.deg .n { font-family: var(--display); font-size: 28px; line-height: 1; } .deg .k { font-family: var(--mono); font-size: 11px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
.deg .ex { font-size: 13.5px; } .deg .chip { justify-self: start; }
.voices { display: flex; gap: 3px; height: 22px; align-items: flex-end; } .voices i { display: block; width: 6px; border-radius: 1px; background: var(--line); }
/* croisements */
table.xmat { border-collapse: collapse; min-width: 760px; width: 100%; font-size: 13px; table-layout: fixed; }
table.xmat th { font-family: var(--mono); font-size: 11.5px; font-weight: 500; color: var(--muted); text-align: left; padding: 6px; border-bottom: 1px solid var(--rule); }
table.xmat td { border: 1px solid var(--grid); padding: 6px; vertical-align: top; height: 54px; }
table.xmat td.diag { background: var(--paper); font-family: var(--mono); font-size: 11.5px; color: var(--muted); }
table.xmat td.void { background: transparent; border-color: transparent; }
table.xmat td.shade { background: repeating-linear-gradient(135deg, transparent 0 7px, var(--grid) 7px 8px); color: var(--muted); font-size: 12px; }
.xchips { display: flex; flex-wrap: wrap; gap: 3px; }
.chip.lit { color: var(--void); border-style: dashed; }
.sdots { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 5px; }
.sdot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; vertical-align: middle; }
a.chip { text-decoration: none; } a.chip:hover { text-decoration: underline; }
table.xmat td.mr:not(.shade) { background: color-mix(in srgb, var(--paper) 60%, transparent); }
table.xlist { border-collapse: collapse; width: 100%; min-width: 860px; font-size: 13px; }
table.xlist th { text-align: left; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; padding: 6px 8px; border-bottom: 1px solid var(--rule); }
table.xlist td { padding: 8px; border-bottom: 1px solid var(--grid); vertical-align: top; }
table.xlist td.lv { font-family: var(--mono); color: var(--line); white-space: nowrap; }
.zones { display: grid; gap: 4px; } .zones li { color: var(--muted); }
/* échelle */
.ladder { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 8px 18px; }
.rung { display: grid; grid-template-columns: 34px 1fr; gap: 10px; align-items: baseline; padding: 6px 0; border-bottom: 1px dashed var(--rule); }
.rung .lv { font-family: var(--mono); font-size: 18px; font-weight: 500; color: var(--line); text-align: right; } .rung b { font-weight: 600; } .rung span { color: var(--muted); font-size: 13.5px; }
/* marches */
.next { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }
.step { border-top: 2px solid var(--line); padding-top: 10px; display: grid; gap: 6px; align-content: start; min-width: 0; } .step .gain { font-family: var(--mono); font-size: 12.5px; color: var(--accent); }
@media (max-width: 640px) { .axis, .dim { grid-template-columns: 1fr; gap: 6px; } .axis .lbl { display: none; } .note { grid-column: 1; } .sheet { padding: 16px; } .multiples { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: no-preference) { .mv { animation: grow 900ms ease-out both; transform-origin: left center; } @keyframes grow { from { transform: scaleX(0.15); } to { transform: scaleX(1); } } }
"""

DEGRES = """
<div class="degrees" role="region" aria-label="Tableau des degrés" tabindex="0"><div class="deg-row">
<div class="deg"><div class="k">degré</div><div class="n mono">0</div><div class="voices" aria-hidden="true"></div><div class="ex">La constante 1, et rien d'autre.</div><span class="chip ok">classé : démontré</span></div>
<div class="deg gap"><div class="k">entre 0 et 1</div><div class="n mono">∅</div><div class="ex">Vide.</div><span class="chip ok">démontré</span></div>
<div class="deg"><div class="k">degré</div><div class="n mono">1</div><div class="voices" aria-hidden="true"><i style="height:22px"></i></div><div class="ex">ζ et les L(s, χ) de Dirichlet. Objet : un caractère (dimension 1).</div><span class="chip ok">classé : démontré (1999)</span><span class="chip open">RH : ouverte</span><span class="chip here">notre travail : v1 à V6.17</span></div>
<div class="deg gap"><div class="k">entre 1 et 2</div><div class="n mono">∅</div><div class="ex">Vide.</div><span class="chip ok">démontré (2011)</span></div>
<div class="deg"><div class="k">degré</div><div class="n mono">2</div><div class="voices" aria-hidden="true"><i style="height:22px"></i><i style="height:15px"></i></div><div class="ex">Formes modulaires (Δ de Ramanujan), courbes elliptiques, ζ d'un corps quadratique. Objet de dimension 2.</div><span class="chip open">classé : conjectural</span><span class="chip open">RH : ouverte</span><span class="chip here">notre travail : V6.15–V6.17 (Δ de Ramanujan, ζ de Q(√5))</span></div>
<div class="deg side"><div class="k">à côté : corps finis</div><div class="n mono">2g</div><div class="voices" aria-hidden="true"><i style="height:22px"></i><i style="height:18px"></i><i style="height:14px"></i><i style="height:10px"></i></div><div class="ex">Courbe de genre g : un polynôme de degré 2g. Le Modèle réduit.</div><span class="chip ok">RH : démontrée (Weil 1948)</span><span class="chip here">notre travail : v3.7, V6.6, V6.7, V6.9, V6.11, V6.17</span></div>
</div></div>
<p class="foot">Classements : Conrey–Ghosh (1993) et Kaczorowski–Perelli (1999) jusqu'au degré 1, Kaczorowski–Perelli (2011) entre 1 et 2. Degré 3 et au-delà : produits de fonctions L et formes de GL(n), RH ouverte.</p>
"""

SCRIPT = r"""
(function () {
  const D = JSON.parse(document.getElementById("indic-data").textContent);
  const ET = D.etapes, DIMS = D.dimensions, n = ET.length;
  const W = 600, H = 168, L = 26, R = 10, T = 22, B = 24;
  const xs = i => L + (i + 0.5) * (W - L - R) / n, ys = v => T + (9 - v) * (H - T - B) / 9;
  const tip = document.createElement("div"); tip.className = "tip"; tip.hidden = true; document.body.appendChild(tip);
  const host = document.getElementById("multiples"); const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; };
  // bandes des jours
  const days = []; ET.forEach((e, i) => { if (!days.length || days[days.length - 1].j !== e.jour) days.push({ j: e.jour, a: i, b: i }); else days[days.length - 1].b = i; });
  DIMS.forEach(dm => {
    const p = document.createElement("div"); p.className = "panel";
    const last = ET[n - 1].niveaux[dm.id];
    p.innerHTML = `<h3>${dm.nom} <span class="mono">${last}</span></h3><div class="q">${dm.question}</div>`;
    const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": `${dm.nom} : niveaux par version, de ${ET[0].niveaux[dm.id]} à ${last}` });
    days.forEach((d, k) => {
      const x0 = L + d.a * (W - L - R) / n, x1 = L + (d.b + 1) * (W - L - R) / n;
      if (k % 2 === 0) el("rect", { x: x0, y: T - 14, width: x1 - x0, height: H - B - T + 14, fill: "var(--band)" }, svg);
      const t = el("text", { x: x0 + 3, y: T - 5, class: "day" }, svg); t.textContent = d.j;
    });
    for (let v = 0; v <= 9; v++) {
      el("line", { x1: L, x2: W - R, y1: ys(v), y2: ys(v), stroke: "var(--grid)", "stroke-width": v % 3 === 0 ? 1 : 0.6 }, svg);
      if (v % 3 === 0) { const t = el("text", { x: L - 6, y: ys(v) + 3.5, "text-anchor": "end" }, svg); t.textContent = v; }
    }
    const tgt = D.visees[dm.id];
    if (tgt !== undefined) { el("line", { x1: L, x2: W - R, y1: ys(tgt), y2: ys(tgt), stroke: "var(--void)", "stroke-dasharray": "4 4", "stroke-width": 1.2 }, svg);
      const t = el("text", { x: W - R - 2, y: ys(tgt) - 4, "text-anchor": "end" }, svg); t.textContent = "visé : " + tgt; }
    let d = `M ${xs(0)} ${ys(ET[0].niveaux[dm.id])}`;
    for (let i = 1; i < n; i++) d += ` H ${xs(i)} V ${ys(ET[i].niveaux[dm.id])}`;
    el("path", { d, fill: "none", stroke: "var(--line)", "stroke-width": 2, "stroke-linejoin": "round" }, svg);
    ET.forEach((e, i) => {
      const v = e.niveaux[dm.id], up = i > 0 && v > ET[i - 1].niveaux[dm.id];
      el("circle", { cx: xs(i), cy: ys(v), r: up ? 5.5 : 4, fill: up ? "var(--accent)" : "var(--line)", stroke: "var(--sheet)", "stroke-width": 2 }, svg);
      const t = el("text", { x: xs(i), y: H - 6, "text-anchor": "middle" }, svg); t.textContent = e.court;
      const hit = el("rect", { x: xs(i) - (W - L - R) / n / 2, y: T - 14, width: (W - L - R) / n, height: H - T - B + 14, fill: "transparent" }, svg);
      const why = (e.pourquoi && e.pourquoi[dm.id]) ? e.pourquoi[dm.id] : (up ? "" : "inchangé");
      const prev = i > 0 ? ET[i - 1].niveaux[dm.id] : null;
      hit.addEventListener("mouseenter", () => {
        tip.innerHTML = `<b>${e.versions}</b> · ${e.jour}<br>${dm.nom} : <span class="mono">${prev !== null && prev !== v ? prev + " → " + v : v}</span>${why ? "<br>" + why : ""}`;
        tip.hidden = false; });
      hit.addEventListener("mousemove", ev => { tip.style.left = (ev.pageX + 14) + "px"; tip.style.top = (ev.pageY + 14) + "px"; });
      hit.addEventListener("mouseleave", () => { tip.hidden = true; });
    });
    p.appendChild(svg); host.appendChild(p);
  });
})();
"""

NOMBRES = {5: "cinq", 6: "six", 7: "sept", 8: "huit"}

def load_sources():
    p = ROOT / "2_Methode" / "Sources" / "sources.json"
    return json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else []

def crossings(d, links=True):
    """Carte des croisements : matrice des conjectures, liste, zones d'ombre (cases vides, pendants manquants dans le Modèle réduit)."""
    X = d.get("croisements", []); C = d.get("conjectures", [])
    if not X: return "", []
    nom = {c["id"]: c["nom"] for c in C}; by = {e["id"]: e for e in d["etapes"]}
    corpus = [x for x in X if x["statut"] == "corpus"]
    S = load_sources()
    COUL = {"appui": "#c0392b", "confronter": "#d9822b", "contexte": "#2e6fb5", "outil": "#8a8f98"}
    def chip(x, mr=False):
        tip = html.escape(x["pendant_modele_reduit"] if mr else x["enonce"])
        doc = x.get("document")
        if x["statut"] != "corpus": inner, cls = html.escape(x["titre"]), "chip lit"
        else: inner, cls = f"{html.escape(x['titre'])} · {x['niveau']}", "chip up"
        if links and doc: return f"<a class='{cls}' href=\"{html.escape(doc)}\" title='{tip}'>{inner}</a>"
        return f"<span class='{cls}' title='{tip}'>{inner}</span>"
    def dots(ids):
        src = [z for z in S if all(i in z.get("conjectures", []) for i in ids)]
        if not src: return ""
        def one(z):
            col = COUL.get(z.get("interet"), "#999"); href = html.escape(z.get("lien") or ""); 
            tip = html.escape(f"{z['cle']} · {z['auteurs']} ({z.get('annee') or ''}) · {z.get('interet', '')} · {z['statut']}")
            return f"<a class='sdot' style='background:{col}' href=\"{href}\" title='{tip}' aria-label='{tip}'></a>"
        ds = "".join(one(z) for z in src)
        return f"<div class='sdots' aria-label='Littérature'>{ds}</div>"
    head = "".join(f"<th>{html.escape(c['nom'])}</th>" for c in C) + "<th>Modèle réduit</th>"; rows = []; zones = []
    for i, a in enumerate(C):
        cells = []
        for j, b in enumerate(C):
            if j < i: cells.append("<td class='void'></td>"); continue
            if j == i: cells.append(f"<td class='diag'>{html.escape(a['nom'])}</td>"); continue
            here = [x for x in X if a["id"] in x["conjectures"] and b["id"] in x["conjectures"]]
            if any(x["statut"] == "corpus" for x in here): cells.append(f"<td><div class='xchips'>{''.join(chip(x) for x in here)}</div>{dots([a['id'], b['id']])}</td>")
            else:
                zones.append(f"{a['nom']} × {b['nom']}" + (" (seulement dans la littérature)" if here else ""))
                cells.append(f"<td class='shade'><div class='xchips'>{''.join(chip(x) for x in here)}</div>zone d'ombre{dots([a['id'], b['id']])}</td>")
        mr = [x for x in corpus if a["id"] in x["conjectures"] and x.get("pendant_modele_reduit")]
        if mr: cells.append(f"<td class='mr'><div class='xchips'>{''.join(chip(x, True) for x in mr)}</div>{dots([a['id'], 'MR'])}</td>")
        else:
            zones.append(f"{a['nom']} × Modèle réduit"); cells.append(f"<td class='shade mr'>zone d'ombre{dots([a['id'], 'MR'])}</td>")
        rows.append(f"<tr><th>{html.escape(a['nom'])}</th>{''.join(cells)}</tr>")
    mat = (f"<div class='tablewrap' role='region' aria-label='Matrice des croisements' tabindex='0'><table class='xmat'><thead><tr><th></th>{head}</tr></thead>"
           f"<tbody>{''.join(rows)}</tbody></table></div>"
           "<p class='foot'>Pastilles de littérature (registre des sources, document 42) : <span class='sdot' style='background:#c0392b'></span> appui · <span class='sdot' style='background:#d9822b'></span> à confronter · <span class='sdot' style='background:#2e6fb5'></span> contexte · <span class='sdot' style='background:#8a8f98'></span> outil ; chacune mène au résumé de l'article. Les croisements mènent à leur document. La colonne « Modèle réduit » montre les croisements dont le pendant est établi là où RH est démontrée.</p>")
    for x in corpus:
        if not x.get("pendant_modele_reduit"): zones.append(f"{x['titre']} : pas de pendant dans le Modèle réduit")
    lst = []
    for x in X:
        doc = x.get("document")
        dl = (f"<a href=\"{html.escape(doc)}\">{html.escape(doc.split('_')[0])}</a>" if links else html.escape(doc.split('_')[0])) if doc else "—"
        step = by[x["etape"]]["court"] if x.get("etape") in by else "—"
        lv = x["niveau"] if x["statut"] == "corpus" else "cité"
        mr = html.escape(x["pendant_modele_reduit"]) if x.get("pendant_modele_reduit") else ("<span class='chip open'>zone d'ombre</span>" if x["statut"] == "corpus" else "—")
        lst.append(f"<tr><td><b>{html.escape(x['titre'])}</b><br><span class='foot'>{html.escape(x['lieu'])}</span></td><td>{' × '.join(html.escape(nom[c]) for c in x['conjectures'])}</td>"
                   f"<td>{txt(x['enonce'])}</td><td class='lv'>{lv}</td><td>{step}</td><td>{mr}</td><td>{dl}</td></tr>")
    table = (f"<div class='tablewrap' role='region' aria-label='Liste des croisements' tabindex='0'><table class='xlist'><thead><tr><th>Croisement</th><th>Conjectures</th><th>Énoncé</th>"
             f"<th>Niveau</th><th>Étape</th><th>Pendant dans le Modèle réduit</th><th>Doc.</th></tr></thead><tbody>{''.join(lst)}</tbody></table></div>")
    legend = "".join(f"<li><b>{html.escape(c['nom'])}</b> : {html.escape(c['long'])}</li>" for c in C)
    out = f"""<section class="sheet" aria-labelledby="t-x"><h2 id="t-x">Les croisements</h2>
<p>Un croisement est un endroit du corpus où RH et un problème voisin, aussi difficile qu'elle, se lisent sur le même objet. {html.escape(d.get('regle_croiser', ''))}</p>
<ul class="zones">{legend}</ul>
<h3>La carte</h3><p class="foot">Une case hachurée est une zone d'ombre : aucun croisement produit par le corpus. Les étiquettes en pointillés viennent de la littérature. Le nombre après chaque titre est le niveau sur l'échelle 0–9.</p>{mat}
<h3>La liste</h3><p class="foot">La colonne « Modèle réduit » donne le pendant du croisement là où RH est démontrée (courbes sur les corps finis) : chaque croisement sur ζ devrait en avoir un.</p>{table}
<h3>Les zones d'ombre</h3><ul class="zones">{''.join(f"<li>{html.escape(z)}</li>" for z in zones)}</ul></section>"""
    return out, zones

def build(d, links=True, standalone=True) -> str:
    if links and standalone:
        import importlib.util
        spec = importlib.util.spec_from_file_location('pilotage_courant', ROOT/'2_Methode/Pilotage/build_pilotage.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        return module.render(module.load_state(), 'indicateur')
    et = d["etapes"]; dims = d["dimensions"]; by = {e["id"]: e for e in et}
    a, b = by[d["comparaison"]["avant"]], by[d["comparaison"]["apres"]]
    up = [(dm, a["niveaux"][dm["id"]], b["niveaux"][dm["id"]]) for dm in dims if b["niveaux"][dm["id"]] > a["niveaux"][dm["id"]]]
    same = [(dm, b["niveaux"][dm["id"]], since(d, dm["id"])) for dm in dims if b["niveaux"][dm["id"]] == a["niveaux"][dm["id"]]]
    crossings_html, zones = crossings(d, links)
    # ---- verdict
    li_up = "".join(f"<li><b>{dm['nom']}</b> <span class='mono'>{x} → {y}</span></li>" for dm, x, y in up)
    li_same = "".join(f"<li><b>{dm['nom']}</b> <span class='mono'>{y}</span>, depuis {s['court']} ({s['jour']})</li>" for dm, y, s in same)
    verdict = f"""<div class="verdict">
<div class="v up"><span class="tag">A bougé depuis le 7 octobre</span><ul>{li_up}</ul></div>
<div class="v same"><span class="tag">Stable</span><ul>{li_same}</ul></div>
<div class="v open"><span class="tag">Pas encore</span><ul><li><b>Relecture</b> : niveau 7 jamais atteint ; dossier envoyable depuis V6.13</li><li><b>Degré 2</b> : niveau {b['niveaux'].get('degre2', 0)} sur 9</li><li><b>La case vide</b> : niveau {b['niveaux']['case']} sur 9</li>{f"<li><b>Croiser</b> : {len(zones)} zones d'ombre sur la carte des croisements</li>" if zones else ""}</ul></div></div>"""
    # ---- tableau des versions
    rows = []
    for i, e in enumerate(et):
        chg = []
        for dm in dims:
            v = e["niveaux"][dm["id"]]; p = et[i - 1]["niveaux"][dm["id"]] if i else None
            if p is None: chg.append(f"<span class='chip ok'>{dm['nom']} {v}</span>")
            elif v != p: chg.append(f"<span class='chip up'>{dm['nom']} {p} → {v}</span>")
        if i and not chg: chg = ["<span class='chip open'>aucun niveau ne change</span>"]
        docs = "".join((f"<a href=\"{html.escape(rel)}\">{html.escape(lab)}</a>" if links else f"<span class='doc'>{html.escape(rel.split('/')[-1])}</span>") for lab, rel in e["documents"])
        rows.append(f"<tr><td class='ver'><b>{html.escape(e['versions'])}</b><span>{e['jour']}</span></td><td>{txt(e['franchi'])}</td><td><div class='chg'>{''.join(chg)}</div></td><td><div class='docs'>{docs}</div></td></tr>")
    table = f"""<div class="tablewrap" role="region" aria-label="Étapes par version" tabindex="0"><table class="hist"><colgroup><col class="c1"><col class="c2"><col class="c3"><col></colgroup>
<thead><tr><th>Versions</th><th>Étape franchie</th><th>Niveaux qui changent</th><th>Documents</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>"""
    # ---- instantané avant / après
    pct = lambda l: (l + 0.5) * 10
    snap = []
    for dm in dims:
        x, y = a["niveaux"][dm["id"]], b["niveaux"][dm["id"]]; t = d["visees"].get(dm["id"])
        marks = "<span class='lane'></span>"
        if t is not None: marks += f"<span class='mk target' style='left:{pct(t)}%'></span>"
        if y != x: marks += f"<span class='mv' style='left:{pct(x)}%; width:calc({pct(y) - pct(x)}% - 10px)'></span>"
        marks += f"<span class='mk then' style='left:{pct(x)}%'></span><span class='mk now' style='left:{pct(y)}%'></span>"
        # raison la plus récente donnée pour cette dimension, jusqu'à l'étape « après » incluse
        why = next((e["pourquoi"][dm["id"]] for e in reversed(et[:et.index(b) + 1]) if e.get("pourquoi", {}).get(dm["id"])), "")
        snap.append(f"""<div class="dim"><div class="name"><b>{dm['nom']} <span class="mono" style="color:var(--line)">{y}</span></b><small>{dm['question']}</small></div>
<div class="track" role="img" aria-label="{dm['nom']} : {x} ({html.escape(d['comparaison']['avant_libelle'])}), {y} ({html.escape(d['comparaison']['apres_libelle'])})">{marks}</div>
<p class="note"><span class="mono">{f'{x} → {y}' if y != x else y}</span>{(' · ' + html.escape(why)) if why else ''}</p></div>""")
    snapshot = f"""<div class="legend"><span><span class="sw"><span class="mk then"></span></span>{d['comparaison']['avant_libelle']}</span><span><span class="arr"></span>mouvement</span>
<span><span class="sw"><span class="mk now"></span></span>{d['comparaison']['apres_libelle']}</span><span><span class="sw"><span class="mk target"></span></span>prochaine marche visée</span></div>
<div class="dims"><div class="axis"><span class="lbl"></span><div class="scale" aria-hidden="true">{''.join(f'<span>{k}</span>' for k in range(10))}</div></div>{''.join(snap)}</div>"""
    ladder = "".join(f"<div class='rung'><span class='lv'>{i}</span><div><b>{n}</b><br><span>{s}</span></div></div>" for i, (n, s) in enumerate(d["echelle"]))
    steps = "".join(f"<div class='step'><b>{t}</b><p>{txt(p)}</p><span class='gain'>{g}</span></div>" for t, p, g in d["prochaines_marches"])
    data = json.dumps({"etapes": [{k: e[k] for k in ("id", "court", "jour", "versions", "niveaux", "pourquoi")} for e in et],
                       "dimensions": dims, "visees": d["visees"]}, ensure_ascii=False)
    note_links = ("Chaque nom de document est un lien vers le fichier du corpus." if links else
                  "Dans le corpus (document 31), chaque nom de document est un lien vers le fichier.")
    body = f"""
<div class="wrap">
{topnav("indicateur", "../") if links else ""}
<header class="head"><div class="eyebrow">Programme Riemann · indicateur d'avancement · {et[-1]['versions']} · {et[-1]['jour']} 2026</div>
<h1>Les étapes franchies, version par version</h1>
<p class="lede">Une échelle de maturité de 0 à 9, inspirée des niveaux de maturité technologique, et {NOMBRES.get(len(dims), len(dims))} dimensions. Chaque version du corpus y est placée, avec les documents qu'elle a produits. La comparaison de niveaux ci-dessous conserve ses deux étapes sélectionnées. Les croisements entre RH et les problèmes voisins ont leur propre carte.</p></header>
<section class="sheet" aria-labelledby="t-v"><h2 id="t-v">Est-ce qu'on avance ?</h2>{verdict}</section>
<section class="sheet" aria-labelledby="t-p"><h2 id="t-p">Le parcours, dimension par dimension</h2>
<p class="foot">Une étape par groupe de versions, du premier au dernier jour du corpus ; les points orange marquent une marche franchie. Survoler un point donne la raison.</p>
<div class="multiples" id="multiples"></div></section>
<section class="sheet" aria-labelledby="t-h"><h2 id="t-h">Version par version</h2><p class="foot">{note_links}</p>{table}</section>
<section class="sheet" aria-labelledby="t-s"><h2 id="t-s">Où en est-on : {d['comparaison']['avant_libelle']} et {d['comparaison']['apres_libelle']}</h2>{snapshot}</section>
<section class="sheet" aria-labelledby="t-d"><h2 id="t-d">Le degré, en une image</h2>
<p>Le <strong>degré</strong> d'une fonction L est le nombre de facteurs Γ dans son équation fonctionnelle. C'est aussi la dimension de l'objet qui se tient derrière elle, et la vitesse à laquelle ses zéros s'empilent : jusqu'à la hauteur T, il y en a environ d·(T/2π)·log T. Image : le nombre de voix dans un accord. ζ chante seule ; une forme modulaire est un accord à deux voix.</p>{DEGRES}</section>
{crossings_html}
<section class="sheet" aria-labelledby="t-e"><h2 id="t-e">L'échelle : niveaux de maturité 0 à 9</h2><div class="ladder">{ladder}</div></section>
<section class="sheet" aria-labelledby="t-n"><h2 id="t-n">Les prochaines marches</h2><div class="next">{steps}</div></section>
<p class="foot">Niveaux attribués d'après les documents du corpus : c'est une grille de lecture, pas une mesure. Mise à jour à chaque version : <span class="mono">2_Methode/Indicateur/indicateur_avancement.json</span>, puis <span class="mono">python 2_Methode/Indicateur/build_indicateur.py</span>.</p>
</div>
<script type="application/json" id="indic-data">{data.replace('</', '<\\/')}</script>
<script>{SCRIPT}</script>
"""
    head = f"""<title>Indicateur d'avancement RH</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,650&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{CSS}</style>"""
    if standalone:
        return f"<!doctype html>\n<html lang=\"fr\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n{head}\n</head><body>{body}</body></html>\n"
    return head + body

if __name__ == "__main__":
    d = load(); miss = check_links(d)
    if miss:
        print("documents introuvables :\n  " + "\n  ".join(miss)); sys.exit(1)
    if "--artefact" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--artefact") + 1]); out.write_text(build(d, links=False, standalone=False), encoding="utf-8")
    else:
        out = OUT; out.write_text(build(d, links=True, standalone=True), encoding="utf-8")
    print("écrit :", out)
