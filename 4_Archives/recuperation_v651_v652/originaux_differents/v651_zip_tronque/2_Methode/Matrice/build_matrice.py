#!/usr/bin/env python3
"""V6.19 — Matrice d'équivalence et de force des théories : matrice_theories.json → 1_Presentation/44_MATRICE_DES_THEORIES.html.

Chaque théorie (ligne et colonne) est décrite selon la méthode du corpus : symbolique → opérateur → fonctions → identification.
Une case porte la relation de la ligne vers la colonne. Les relations écrites dans le fichier sont « directes » ; le générateur
en déduit d'autres par transitivité (⇔ et ⇒), marquées « déduites ». Les cases restantes sont « à compléter » : ce sont les zones
d'ombre de la matrice, que le plan de recherche (document 43) et les lectures doivent remplir.

    python 2_Methode/Matrice/build_matrice.py
"""
from __future__ import annotations
import html, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; PRES = ROOT / "1_Presentation"
OUT = PRES / "44_MATRICE_DES_THEORIES.html"
INV = {"⇒": "⇐", "(⇒)": "(⇐)", "↗": "↙", "✗": "✗", "⇔": "⇔", "∥": "∥", "≈": "≈", "?": "?"}

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def esc(s) -> str:
    return html.escape(str(s or ""), quote=True)

def load():
    M = json.loads((HERE / "matrice_theories.json").read_text(encoding="utf-8-sig"))
    S = {s["cle"]: s for s in json.loads((ROOT / "2_Methode" / "Sources" / "sources.json").read_text(encoding="utf-8-sig"))}
    return M, S

def check(M, S) -> list[str]:
    ids = [n["id"] for n in M["noeuds"]]; errs = []
    if len(set(ids)) != len(ids): errs.append("identifiants en double")
    for n in M["noeuds"]:
        errs += [f"{n['id']} : clé inconnue {k}" for k in n["sources"] if k not in S]
        errs += [f"{n['id']} : document {d} absent" for d in n["docs"] if not doc_path(d)]
        if n["force"] not in M["forces"]: errs.append(f"{n['id']} : force inconnue {n['force']}")
        if n.get("apport") not in M.get("apports", {}): errs.append(f"{n['id']} : provenance inconnue {n.get('apport')}")
    for x in M.get("redecouvertes", []):
        errs += [f"redécouverte : clé inconnue {k}" for k in x["sources"] if k not in S]
        errs += [f"redécouverte : document {d} absent" for d in x["corpus"] if not doc_path(d)]
    for r in M["relations"]:
        if r["de"] not in ids or r["vers"] not in ids: errs.append(f"relation {r['de']}→{r['vers']} : nœud inconnu")
        if r.get("apport") not in M.get("apports", {}): errs.append(f"relation {r['de']}→{r['vers']} : provenance {r.get('apport')}")
        if r["type"] not in M["legende"]: errs.append(f"relation {r['de']}→{r['vers']} : type {r['type']}")
        errs += [f"relation {r['de']}→{r['vers']} : clé inconnue {k}" for k in r["sources"] if k not in S]
    return errs

def doc_path(num: str):
    for ext in (".pdf", ".html", ".md"):
        c = sorted(PRES.glob(f"{num}_*{ext}"))
        if c: return c[0].name
    return None

def cells(M) -> dict:
    """{(ligne, colonne): (symbole, relation, déduite)} ; relations directes, inverses, puis fermeture transitive de ⇔ et ⇒."""
    C = {}
    for r in M["relations"]:
        C[(r["de"], r["vers"])] = (r["type"], r, False)
        C.setdefault((r["vers"], r["de"]), (INV[r["type"]], r, False))
    ids = [n["id"] for n in M["noeuds"]]
    imp = {(a, b) for (a, b), (t, _, _) in C.items() if t in ("⇒", "⇔")}
    changed = True
    while changed:
        changed = False
        for a, b in list(imp):
            for c in ids:
                if (b, c) in imp and a != c and (a, c) not in imp: imp.add((a, c)); changed = True
    for a, c in imp:
        if (a, c) in C: continue
        sym = "⇔" if (c, a) in imp else "⇒"
        C[(a, c)] = (sym, None, True)
        if sym == "⇒" and (c, a) not in C: C[(c, a)] = ("⇐", None, True)
    return C

CSS = r"""
.mx-pop { position: fixed; z-index: 50; background: var(--sheet); color: var(--ink); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; box-shadow: 0 6px 24px rgba(0,0,0,.18); font-size: 14px; pointer-events: none; }
.mx-pop b { display: block; margin-bottom: 2px; }
.mx-pop math, .fx math { font-size: 1.12em; margin: 6px 0; overflow-x: auto; max-width: 100%; }
math { font-family: 'Latin Modern Math', 'STIX Two Math', 'Cambria Math', math; }
.mx-pop .foot { display: block; }
.fx { overflow-x: auto; padding: 4px 0; }
:root { --p-lit: #5b7b9a; --p-rec: #2b7a57; --p-red: #7a4fb0; --p-new: #c4660a; --p-q: #b8650f; --p-oa: #1d5d8c; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --p-lit: #8fb0cf; --p-rec: #5ec496; --p-red: #b99be6; --p-new: #f0a050; --p-q: #e59a4a; --p-oa: #6cb0e0; } }
:root[data-theme="dark"] { --p-lit: #8fb0cf; --p-rec: #5ec496; --p-red: #b99be6; --p-new: #f0a050; --p-q: #e59a4a; --p-oa: #6cb0e0; }
.mx-tools { display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: center; margin: 4px 0 10px; font-size: 14px; }
.seg { display: inline-flex; border: 1px solid var(--rule); border-radius: 6px; overflow: hidden; }
.seg button { all: unset; cursor: pointer; padding: 5px 12px; font-size: 13px; color: var(--muted); }
.seg button[aria-pressed="true"] { background: var(--ink); color: var(--sheet); }
.seg button:focus-visible { outline: 2px solid var(--line); outline-offset: -2px; }
.mx-wrap { overflow: auto; max-height: 78vh; border: 1px solid var(--grid); border-radius: 6px; background: var(--sheet); }
table.mx { border-collapse: separate; border-spacing: 0; font-size: 13px; }
table.mx th, table.mx td { border-right: 1px solid var(--grid); border-bottom: 1px solid var(--grid); text-align: center; min-width: 34px; height: 32px; padding: 0; }
table.mx thead th { position: sticky; top: 0; z-index: 2; background: var(--band); font-weight: 600; vertical-align: bottom; padding: 6px 2px 4px; font-size: 12px; }
table.mx thead th .vid { writing-mode: vertical-rl; transform: rotate(180deg); display: inline-block; }
table.mx thead th.corner { left: 0; z-index: 3; text-align: left; padding: 6px 10px; font-weight: 500; color: var(--muted); }
table.mx thead th a.art, table.mx tbody th a.art { display: block; font-size: 11px; font-weight: 500; color: var(--line); text-decoration: none; margin-top: 3px; }
table.mx thead th a.art:hover, table.mx tbody th a.art:hover { text-decoration: underline; }
table.mx tbody th { position: sticky; left: 0; z-index: 1; background: var(--band); text-align: left; padding: 3px 10px 3px 8px; white-space: nowrap; font-size: 12px; border-left: 5px solid transparent; }
table.mx tbody th .rowh { display: flex; align-items: baseline; gap: 8px; }
table.mx tbody th a.art { display: inline; margin: 0; }
table.mx td button, table.mx th button { all: unset; cursor: pointer; }
table.mx td button { display: block; width: 100%; height: 100%; min-height: 32px; line-height: 32px; font-size: 15px; }
table.mx th button { font-weight: 600; }
table.mx th button:hover, table.mx th button:focus-visible { text-decoration: underline; }
table.mx td.diag { background: var(--grid); }
table.mx td { position: relative; }
table.mx td.oa::after { content: ""; position: absolute; top: 0; right: 0; border-style: solid; border-width: 0 9px 9px 0; border-color: transparent var(--p-oa) transparent transparent; pointer-events: none; }
table.mx sup.oa { color: var(--p-oa); font-size: 9px; font-weight: 700; margin-left: 2px; }
.redec { width: 100%; border-collapse: collapse; font-size: 13px; }
.redec th, .redec td { text-align: left; vertical-align: top; padding: 6px 8px; border-bottom: 1px solid var(--grid); }
.redec th { font-weight: 600; color: var(--muted); }
.tbl-wrap { overflow-x: auto; }
table.mx .gsep { border-left: 2px solid var(--rule); }
table.mx tr.gsep > * { border-top: 2px solid var(--rule); }
/* provenance */
.mode-prov td.p-litterature { background: color-mix(in srgb, var(--p-lit) 20%, transparent); }
.mode-prov td.p-recalcule { background: color-mix(in srgb, var(--p-rec) 30%, transparent); }
.mode-prov td.p-redecouvert { background: color-mix(in srgb, var(--p-red) 26%, transparent); }
.mode-prov td.p-nouveau { background: color-mix(in srgb, var(--p-new) 34%, transparent); box-shadow: inset 0 0 0 2px var(--p-new); }
.mode-prov td.p-question { background: transparent; box-shadow: inset 0 0 0 2px var(--p-q); }
.mode-prov td.p-deduit button, .mode-type td.ded button { color: var(--muted); font-size: 13px; }
.mode-prov td.p-deduit { background: color-mix(in srgb, var(--p-lit) 6%, transparent); }
th.h-litterature { border-left-color: var(--p-lit) !important; }
th.h-recalcule { border-left-color: var(--p-rec) !important; }
th.h-redecouvert { border-left-color: var(--p-red) !important; }
thead th.h-redecouvert { box-shadow: inset 0 -4px 0 var(--p-red); }
th.h-question { border-left-color: var(--p-q) !important; }
thead th.h-question { box-shadow: inset 0 -4px 0 var(--p-q); }
th.h-nouveau { border-left-color: var(--p-new) !important; }
thead th.h-recalcule { box-shadow: inset 0 -4px 0 var(--p-rec); }
thead th.h-nouveau { box-shadow: inset 0 -4px 0 var(--p-new); }
thead th.h-litterature { box-shadow: inset 0 -4px 0 var(--p-lit); }
/* type de relation */
.mode-type td.k-eq { background: color-mix(in srgb, var(--ok) 24%, transparent); }
.mode-type td.k-imp { background: color-mix(in srgb, var(--line) 20%, transparent); }
.mode-type td.k-part { background: color-mix(in srgb, var(--line) 9%, transparent); }
.mode-type td.k-wit { background: color-mix(in srgb, var(--accent) 26%, transparent); }
.mode-type td.k-ana { background: color-mix(in srgb, var(--ok) 10%, transparent); }
.mode-type td.k-open { box-shadow: inset 0 0 0 2px var(--accent); }
.mode-type td.k-ind { background: color-mix(in srgb, var(--void) 18%, transparent); }
.hide-ded td.p-deduit button { visibility: hidden; }
.hide-ded td.p-deduit { background: transparent !important; }
table.mx td.vide button { color: transparent; }
table.mx td.vide:hover button, table.mx td.vide button:focus-visible { color: var(--void); }
table.mx td.xh { filter: brightness(0.93); }
@media (prefers-color-scheme: dark) { table.mx td.xh { filter: brightness(1.25); } }
table.mx th.xh { color: var(--line); }
table.mx td:focus-within { outline: 2px solid var(--line); outline-offset: -2px; }
.mx-legend { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 10px 0 0; font-size: 13px; color: var(--muted); }
.mx-legend b { color: var(--ink); font-size: 15px; margin-right: 4px; }
.sw { display: inline-block; width: 16px; height: 14px; border-radius: 3px; vertical-align: -2px; margin-right: 6px; }
.sw.litterature { background: color-mix(in srgb, var(--p-lit) 30%, transparent); }
.sw.recalcule { background: color-mix(in srgb, var(--p-rec) 40%, transparent); }
.sw.redecouvert { background: color-mix(in srgb, var(--p-red) 36%, transparent); }
.sw.oa { background: linear-gradient(225deg, var(--p-oa) 0 34%, transparent 34%); border: 1px solid var(--grid); }
.sw.nouveau { background: color-mix(in srgb, var(--p-new) 40%, transparent); box-shadow: inset 0 0 0 2px var(--p-new); }
.sw.question { box-shadow: inset 0 0 0 2px var(--p-q); }
.sw.deduit { background: color-mix(in srgb, var(--p-lit) 8%, transparent); border: 1px solid var(--grid); }
.badge { display: inline-block; font-size: 12px; font-weight: 600; padding: 1px 8px; border-radius: 10px; margin-left: 6px; vertical-align: 2px; }
.badge.litterature { background: color-mix(in srgb, var(--p-lit) 22%, transparent); }
.badge.recalcule { background: color-mix(in srgb, var(--p-rec) 28%, transparent); }
.badge.redecouvert { background: color-mix(in srgb, var(--p-red) 26%, transparent); }
.badge.oa { background: color-mix(in srgb, var(--p-oa) 20%, transparent); }
.badge.nouveau { background: color-mix(in srgb, var(--p-new) 30%, transparent); }
.badge.question { box-shadow: inset 0 0 0 1.5px var(--p-q); }
.badge.deduit { background: var(--band); }
.mx-panel { margin-top: 14px; border: 1px solid var(--rule); border-radius: 6px; padding: 12px 14px; background: var(--sheet); min-height: 70px; }
.mx-panel h3 { margin: 0 0 6px; font-family: var(--display); font-size: 18px; }
.steps4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 8px; margin: 8px 0; }
.steps4 div { border-left: 3px solid var(--line); padding: 4px 8px; background: var(--band); }
.steps4 small { display: block; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; font-size: 11px; }
.ladder { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 10px; }
.ladder div { border: 1px solid var(--grid); border-radius: 6px; padding: 8px 10px; background: var(--sheet); }
.ladder h4 { margin: 0 0 4px; font-size: 13px; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
.ladder button { all: unset; cursor: pointer; display: block; padding: 2px 0 2px 8px; color: var(--ink); border-left: 4px solid transparent; margin: 2px 0; }
.ladder button:hover, .ladder button:focus-visible { text-decoration: underline; }
.counts { display: flex; flex-wrap: wrap; gap: 16px; font-size: 14px; }
.counts span b { font-family: var(--display); font-size: 22px; margin-right: 4px; }
.arts { columns: 2 320px; column-gap: 28px; font-size: 13px; margin: 8px 0 0; padding-left: 18px; }
.arts li { break-inside: avoid; margin: 0 0 4px; }
@media (max-width: 640px) { table.mx .nm, table.mx tbody th a.art { display: none; } }
"""

KIND = {"⇔": "k-eq", "⇒": "k-imp", "⇐": "k-imp", "(⇒)": "k-part", "(⇐)": "k-part", "✗": "k-wit", "≈": "k-ana", "?": "k-open", "∥": "k-ind", "↗": "k-part", "↙": "k-part"}

def principal(n, S):
    """Premier article de la fiche qui a un lien vers son résumé."""
    for k in n["sources"]:
        if S.get(k, {}).get("lien"): return k, S[k]["lien"]
    return None, None

def build(M, S) -> str:
    bi = _load("build_indicateur", ROOT / "2_Methode" / "Indicateur" / "build_indicateur.py")
    order = {f: k for k, f in enumerate(M["forces"])}
    nodes = sorted(M["noeuds"], key=lambda n: order[n["force"]])
    C = cells(M); ids = [n["id"] for n in nodes]
    gstart = {n["id"] for k, n in enumerate(nodes) if k > 0 and n["force"] != nodes[k - 1]["force"]}
    def prov(v):
        sym, r, ded = v
        return "deduit" if ded else r.get("apport", "litterature")
    n_dir = sum(1 for v in C.values() if not v[2]); n_ded = sum(1 for v in C.values() if v[2])
    total = len(ids) * (len(ids) - 1); n_void = total - len(C)
    cnt = {p: sum(1 for v in C.values() if prov(v) == p) for p in M["apports"]}
    cntn = {p: sum(1 for n in nodes if n["apport"] == p) for p in M["apports"]}
    head = []
    for n in nodes:
        k, l = principal(n, S)
        art = f"<a class='art' href='{esc(l)}' target='_blank' rel='noopener' title='{esc(S[k]['auteurs'])}, {esc(S[k]['titre'])} : résumé'>↗</a>" if l else ""
        head.append(f"<th scope='col' data-c='{n['id']}' class='h-{n['apport']}{' gsep' if n['id'] in gstart else ''}'><button type='button' data-n='{n['id']}' title='{esc(n['nom'])}'><span class='vid'>{esc(n['id'])}</span></button>{"<sup class='oa' title='piste ou proposition d’OpenAI'>OA</sup>" if n.get("origine", "").startswith("OpenAI") else ""}{art}</th>")
    rows = []
    for a in nodes:
        tds = []
        for b in nodes:
            sep = " gsep" if b["id"] in gstart else ""
            if a["id"] == b["id"]: tds.append(f"<td class='diag{sep}' data-c='{b['id']}' aria-label='diagonale'></td>"); continue
            v = C.get((a["id"], b["id"]))
            if not v:
                tds.append(f"<td class='vide{sep}' data-c='{b['id']}'><button type='button' data-a='{a['id']}' data-b='{b['id']}' aria-label='{esc(a['nom'])} et {esc(b['nom'])} : à compléter'>·</button></td>")
            else:
                sym, r, ded = v
                cls = f"{KIND.get(sym, '')} p-{prov(v)}" + (" ded" if ded else " d") + sep + (" oa" if r and r.get("origine", "").startswith("OpenAI") else "")
                tds.append(f"<td class='{cls}' data-c='{b['id']}'><button type='button' data-a='{a['id']}' data-b='{b['id']}' aria-label='{esc(a['nom'])} {sym} {esc(b['nom'])}'>{sym}</button></td>")
        k, l = principal(a, S)
        art = f"<a class='art' href='{esc(l)}' target='_blank' rel='noopener' title='{esc(S[k]['auteurs'])}, {esc(S[k]['titre'])} : résumé'>[{esc(k)}] ↗</a>" if l else ""
        rows.append(f"<tr class='{'gsep' if a['id'] in gstart else ''}' data-r='{a['id']}'><th scope='row' class='h-{a['apport']}'><span class='rowh'><button type='button' data-n='{a['id']}' title='{esc(a['nom'])}'>{esc(a['id'])}<span class='nm'> · {esc(a['nom'])}</span></button>{"<sup class='oa' title='piste ou proposition d’OpenAI'>OA</sup>" if a.get("origine", "").startswith("OpenAI") else ""}{art}</span></th>{''.join(tds)}</tr>")
    legend_p = "".join(f"<span><span class='sw {p}'></span>{esc(v)} ({cnt.get(p, 0)})</span>" for p, v in M["apports"].items()) + "<span><span class='sw oa'></span>coin bleu, ou « OA » sur un nom : vient des pistes d'OpenAI</span>"
    def dl(num):
        h = doc_path(num); return f"<a href='{esc(h)}'>{esc(num)}</a>" if h else esc(num)
    def sl(k):
        s = S[k]; return f"<a href='{esc(s['lien'])}' target='_blank' rel='noopener' title='{esc(s['auteurs'])}, {esc(s['titre'])}'>[{esc(k)}]</a>" if s.get("lien") else f"[{esc(k)}]"
    redec = "".join(f"<tr><td>{esc(x['quoi'])}</td><td>{', '.join(dl(d) for d in x['corpus'])}</td><td>{esc(x['ou'])} {' '.join(sl(k) for k in x['sources'])}</td></tr>" for x in M.get("redecouvertes", []))
    legend_t = "".join(f"<span><b>{esc(k)}</b>{esc(v)}</span>" for k, v in M["legende"].items())
    ladder = "".join(f"<div><h4>{esc(f)}</h4>" + "".join(f"<button type='button' data-n='{n['id']}' class='h-{n['apport']}'>{esc(n['nom'])}</button>" for n in nodes if n["force"] == f) + "</div>"
                     for f in M["forces"] if any(n["force"] == f for n in nodes))
    used = sorted({k for n in nodes for k in n["sources"]} | {k for r in M["relations"] for k in r["sources"]}, key=str.lower)
    arts = "".join(f"<li>[{esc(k)}] {esc(S[k]['auteurs'])}, <i>{esc(S[k]['titre'])}</i> ({esc(S[k].get('annee') or 's. d.')})" + (f" · <a href='{esc(S[k]['lien'])}' target='_blank' rel='noopener'>résumé</a>" if S[k].get("lien") else " · sans lien") + f" <span class='foot'>({esc(S[k]['statut'])})</span></li>" for k in used)
    src = {k: dict(cle=k, ref=f"{s['auteurs']}, {s['titre']} ({s.get('annee') or 's. d.'})", lien=s.get("lien") or "", statut=s["statut"]) for k, s in S.items()}
    data = dict(noeuds={n["id"]: dict(n, docs=[dict(num=d, href=doc_path(d)) for d in n["docs"]]) for n in nodes},
                cases={f"{a}|{b}": dict(sym=v[0], ded=v[2], prov=prov(v), origine=(v[1] or {}).get("origine", ""), note=(v[1] or {}).get("note", ""), sources=(v[1] or {}).get("sources", []),
                                         sens=("direct" if v[1] and v[1]["de"] == a else "inverse") if v[1] else "déduit") for (a, b), v in C.items()},
                sources=src, apports=M["apports"])
    js = r"""
const D = JSON.parse(document.getElementById('mx-data').textContent);
const P = document.getElementById('mx-panel'), T = document.getElementById('mx');
const e = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const tex = n => n.formule_mathml || `<code>${e(n.formule)}</code>`;   // MathML rendu à l'avance (render_formules.js)
const POP = document.getElementById('mx-pop');
function pop(btn){ const n = D.noeuds[btn.dataset.n]; if(!n || !n.formule){ POP.hidden = true; return; }
  POP.innerHTML = `<b>${e(n.nom)}</b>${tex(n)}<span class="foot">${e(n.enonce)}</span>`; POP.hidden = false;
  const r = btn.getBoundingClientRect(), w = Math.min(460, window.innerWidth - 24);
  POP.style.width = w + 'px'; POP.style.left = Math.max(12, Math.min(window.innerWidth - w - 12, r.left)) + 'px';
  const below = r.bottom + 8, h = POP.offsetHeight; POP.style.top = (below + h < window.innerHeight ? below : Math.max(8, r.top - h - 8)) + 'px'; }
document.addEventListener('mouseover', ev => { const b = ev.target.closest('button[data-n]'); if(b) pop(b); else if(!ev.target.closest('#mx-pop')) POP.hidden = true; });
document.addEventListener('focusin', ev => { const b = ev.target.closest('button[data-n]'); if(b) pop(b); else POP.hidden = true; });
document.addEventListener('keydown', ev => { if(ev.key === 'Escape') POP.hidden = true; });
window.addEventListener('scroll', () => { POP.hidden = true; }, {passive:true});
const badge = p => `<span class="badge ${e(p)}">${e(D.apports[p] || p)}</span>`;
function srcs(keys){ if(!keys || !keys.length) return '<p class="foot">Aucune source enregistrée : à compléter dans le registre (document 42).</p>';
  return '<ul>' + keys.map(k => { const s = D.sources[k]; if(!s) return `<li>[${e(k)}]</li>`;
    return `<li>[${e(k)}] ${e(s.ref)} — ${e(s.statut)}${s.lien ? ` · <a href="${e(s.lien)}" target="_blank" rel="noopener">résumé</a>` : ''}</li>`; }).join('') + '</ul>'; }
function showNode(id){ const n = D.noeuds[id];
  P.innerHTML = `<h3>${e(n.nom)}${badge(n.apport)}${(n.origine||'').startsWith('OpenAI') ? '<span class="badge oa">origine : ' + e(n.origine) + '</span>' : ''}</h3><p>${e(n.enonce)}</p>${n.formule ? `<div class="fx">${tex(n)}</div>` : ''}<p class="foot">Force : <b>${e(n.force)}</b> · statut : ${e(n.statut)}</p>
  <p class="foot"><b>Dans ce programme :</b> ${e(n.apport_note)}</p>
  <div class="steps4"><div><small>1. Symbolique</small>${e(n.symbolique)}</div><div><small>2. Opérateur</small>${e(n.operateur)}</div>
  <div><small>3. Fonctions</small>${e(n.fonctions)}</div><div><small>4. Identification</small>${e(n.identification)}</div></div>
  <p class="foot">Documents du corpus : ${n.docs.length ? n.docs.map(d => d.href ? `<a href="${e(d.href)}">${e(d.num)}</a>` : e(d.num)).join(', ') : 'aucun'}</p>${srcs(n.sources)}`; }
function showCell(a, b){ const c = D.cases[a + '|' + b], A = D.noeuds[a], B = D.noeuds[b];
  if(!c){ P.innerHTML = `<h3>${e(A.nom)} · ${e(B.nom)}</h3><p><b>Case à compléter.</b> Quelle relation entre « ${e(A.nom)} » et « ${e(B.nom)} » : équivalence, implication, indépendance, témoin contraire, ou question ouverte ? Une case remplie doit citer une source du registre ou un document du corpus.</p>`; return; }
  P.innerHTML = `<h3>${e(A.nom)} <span style="font-size:22px">${e(c.sym)}</span> ${e(B.nom)}${badge(c.prov)}${c.origine ? '<span class="badge oa">origine : ' + e(c.origine) + '</span>' : ''}</h3>
  <p>${c.ded ? 'Relation <b>déduite</b> par transitivité (⇔ et ⇒) à partir des relations écrites.' : e(c.note)}</p>
  ${c.sens === 'inverse' ? '<p class="foot">Relation écrite dans l’autre sens (de la colonne vers la ligne).</p>' : ''}${c.ded ? '' : srcs(c.sources)}`; }
document.addEventListener('click', ev => { const t = ev.target.closest('button'); if(!t) return;
  if(t.dataset.n){ showNode(t.dataset.n); P.scrollIntoView({block:'nearest'}); }
  else if(t.dataset.a){ showCell(t.dataset.a, t.dataset.b); P.scrollIntoView({block:'nearest'}); }
  else if(t.dataset.mode){ const W = document.getElementById('mx-root'); W.classList.remove('mode-prov','mode-type'); W.classList.add('mode-' + t.dataset.mode);
    document.querySelectorAll('[data-mode]').forEach(x => x.setAttribute('aria-pressed', x === t ? 'true' : 'false'));
    document.getElementById('lg-prov').hidden = t.dataset.mode !== 'prov'; } });
document.getElementById('ded').addEventListener('change', ev => document.getElementById('mx-root').classList.toggle('hide-ded', !ev.target.checked));
let last = [];
function cross(td){ last.forEach(x => x.classList.remove('xh')); last = [];
  if(!td) return; const tr = td.closest('tr'), c = td.dataset.c;
  if(tr && tr.dataset.r){ last.push(...tr.querySelectorAll('td'), tr.querySelector('th')); }
  if(c){ last.push(...T.querySelectorAll(`[data-c="${c}"]`)); }
  last.forEach(x => x.classList.add('xh')); }
T.addEventListener('mouseover', ev => cross(ev.target.closest('td')));
T.addEventListener('focusin', ev => cross(ev.target.closest('td')));
T.addEventListener('mouseleave', () => cross(null));
showNode('RH');
"""
    body = f"""<div class="wrap">
{bi.topnav("matrice", "../")}
<header class="head"><div class="eyebrow">Programme Riemann · {esc(M['version'])} · matrice d'équivalence et de force</div>
<h1>Où se situe chaque théorie par rapport à RH</h1>
<p class="lede">Chaque ligne et chaque colonne est une théorie ou un critère ; la case dit ce que la ligne apporte à la colonne. La couleur dit d'où vient la relation : connue de la littérature, recalculée dans ce programme, retrouvée ici puis reconnue dans la littérature, ou éventuellement nouvelle. Un coin bleu signale ce qui vient des pistes d'OpenAI. Le lien ↗ de chaque en-tête ouvre le résumé de l'article principal. Survoler (ou toucher) le nom d'une théorie affiche sa formule.</p></header>
<section class="sheet" aria-labelledby="t-c"><h2 id="t-c">État de la matrice</h2><div class="counts">
<span><b>{len(nodes)}</b>théories</span><span><b>{n_dir}</b>cases écrites</span><span><b>{n_ded}</b>déduites</span><span><b>{n_void}</b>à compléter</span>
<span><b>{cntn['recalcule']}</b>théories recalculées ici</span><span><b>{cntn['redecouvert']}</b>retrouvées puis reconnues</span><span><b>{cntn['nouveau']}</b>éventuellement nouvelles</span></div>
<details><summary>Les {len(used)} articles de la matrice, avec le lien vers leur résumé</summary><ol class="arts">{arts}</ol></details></section>
<section class="sheet mode-prov" aria-labelledby="t-m" id="mx-root"><h2 id="t-m">La matrice</h2>
<div class="mx-tools"><span>Couleur :</span><span class="seg" role="group" aria-label="Couleur des cases"><button type="button" data-mode="prov" aria-pressed="true">provenance</button><button type="button" data-mode="type" aria-pressed="false">type de relation</button></span>
<label><input type="checkbox" id="ded" checked> montrer les cases déduites</label></div>
<div class="mx-legend" id="lg-prov">{legend_p}</div>
<p class="foot">Lignes et colonnes rangées par force (traits épais entre les groupes), de la plus forte (implique RH) au témoin. La bande de couleur des en-têtes donne la provenance de la théorie elle-même. Survoler une case éclaire sa ligne et sa colonne.</p>
<div class="mx-wrap"><table class="mx" id="mx"><thead><tr><th scope="col" class="corner">ligne → colonne</th>{''.join(head)}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<div class="mx-legend">{legend_t}<span><b>·</b>case à compléter (visible au survol)</span></div>
<div class="mx-panel" id="mx-panel" aria-live="polite"></div></section>
<section class="sheet" aria-labelledby="t-r"><h2 id="t-r">Ce que le programme a retrouvé</h2><p class="foot">Des résultats obtenus ici, ou proposés par OpenAI, puis reconnus dans la littérature. Ils ne sont pas nouveaux, mais ils valident le chemin : le corpus est arrivé par ses propres moyens à des endroits connus. Colonne « Corpus » : documents où cela a été obtenu ; dernière colonne : où la littérature le contient, avec le lien vers le résumé.</p>
<div class="tbl-wrap"><table class="redec"><thead><tr><th>Ce qui a été retrouvé</th><th>Corpus</th><th>Où c'était déjà</th></tr></thead><tbody>{redec}</tbody></table></div></section>
<section class="sheet" aria-labelledby="t-l"><h2 id="t-l">L'échelle de force</h2><p class="foot">Plus forte que RH : l'implique. Équivalente : démontrée équivalente. Plus faible : conséquence de RH. Indépendante : aucune implication connue. Analogue : pendant démontré dans le Modèle réduit. Témoin : contre-exemple qui borne ce qu'un critère peut prouver. Le trait de couleur à gauche de chaque nom donne sa provenance.</p><div class="ladder">{ladder}</div></section>
<p class="foot">Données : <span class="mono">2_Methode/Matrice/matrice_theories.json</span> ; sources : registre (document 42). Mise à jour : <span class="mono">python 2_Methode/Matrice/build_matrice.py</span>. Auteur : Vincent NOËL.</p>
</div>
<div id="mx-pop" class="mx-pop" role="tooltip" hidden></div>
<script type="application/json" id="mx-data">{json.dumps(data, ensure_ascii=False).replace('</', '<\\/')}</script>
<script>{js}</script>"""
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Matrice des théories RH</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,650&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{bi.CSS}{CSS}</style></head><body>{body}</body></html>
"""

if __name__ == "__main__":
    M, S = load(); errs = check(M, S)
    if errs: sys.exit("matrice incohérente :\n  " + "\n  ".join(errs))
    OUT.write_text(build(M, S), encoding="utf-8"); C = cells(M)
    print(f"{len(M['noeuds'])} théories, {sum(1 for v in C.values() if not v[2])} cases écrites, {sum(1 for v in C.values() if v[2])} déduites ; écrit : {OUT}")
