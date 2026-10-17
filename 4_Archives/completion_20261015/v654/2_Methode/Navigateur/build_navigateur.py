#!/usr/bin/env python3
"""Navigateur de recherche du Programme Riemann : la démonstration comme itinéraire.

    python 2_Methode/Navigateur/build_navigateur.py                -> 1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html, classement imprimé
    python 2_Methode/Navigateur/build_navigateur.py --artefact F   -> F : variante sans liens, pour une page publiée hors du corpus

Position : l'indicateur d'avancement (dernière étape). Opérateurs : les métaphores du registre, lues dans
1_Presentation/20_Registre_metaphores_V6.md avec leur garde. Coups : carte_navigation.json (estimations écrites à la main).
Le script vérifie que chaque opérateur cité existe dans le registre, que chaque prérequis existe et que chaque document cité existe.
"""
from __future__ import annotations
import html, importlib.util, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; PRES = ROOT / "1_Presentation"
OUT = PRES / "34_NAVIGATEUR_DE_RECHERCHE.html"
REG = PRES / "20_Registre_metaphores_V6.md"

def _indicateur():
    spec = importlib.util.spec_from_file_location("build_indicateur", ROOT / "2_Methode" / "Indicateur" / "build_indicateur.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def source(sec: str) -> str:
    """Étiquette courte de la section du registre d'où vient un opérateur."""
    m = re.search(r"V6\.[\d]+[a-z/]*", sec)
    if m: return "registre · " + m.group(0)
    if sec.startswith("Annexe B"): return "registre · annexe B"
    return "registre · tableau canonique"

def esc(s: str) -> str:
    return re.sub(r"\^([^^\s]+)\^", r"<sup>\1</sup>", html.escape(s, quote=False))

def clean(s: str) -> str:
    """Retire le gras markdown et la notation LaTeX \\( \\) du registre."""
    return re.sub(r"\\\(|\\\)", "", s.replace("**", "")).strip()

# ------------------------------------------------------------------ les opérateurs : le registre des métaphores
def operators() -> dict:
    ops, hdr, sec = {}, None, ""
    for line in REG.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("## "): sec = line[3:].strip()
        if line.startswith("| Nom"): hdr = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if line.startswith("| **") and hdr:
            cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
            if len(cells) != len(hdr): raise ValueError(f"ligne du registre mal formée : {cells[0]}")
            row = dict(zip(hdr, cells)); name = clean(cells[0])
            ops[name] = dict(nom=name, section=sec,
                             image=clean(row.get("Image", row.get("Image mentale", ""))),
                             enonce=clean(row.get("Énoncé exact", row.get("Objet exact / ancrage", ""))),
                             autorise=clean(row.get("Correspondance autorisée", "")),
                             garde=clean(row.get("Où l'image casse", row.get("Où l’image casse", row.get("Correspondance interdite", "")))),
                             question=clean(row.get("Question divergente", "")), statut=clean(row.get("Statut V6.3", "")))
    return ops

def load():
    carte = json.loads((HERE / "carte_navigation.json").read_text(encoding="utf-8-sig"))
    ind = json.loads((ROOT / "2_Methode" / "Indicateur" / "indicateur_avancement.json").read_text(encoding="utf-8-sig"))
    return carte, ind, operators()

def check(carte, ops, ind=None) -> list[str]:
    errs, ids = [], {c["id"] for c in carte["coups"]}
    conj = {x["id"] for x in (ind or {}).get("conjectures", [])}
    for c in carte["coups"]:
        errs += [f"{c['id']} : conjecture inconnue « {x} »" for x in c.get("croise", []) if conj and x not in conj]
    for c in carte["coups"]:
        errs += [f"{c['id']} : opérateur inconnu « {o} »" for o in c.get("operateurs", []) if o not in ops]
        errs += [f"{c['id']} : prérequis inconnu « {p} »" for p in c.get("prerequis", []) if p not in ids]
        if c.get("document") and not (PRES / c["document"]).exists(): errs.append(f"{c['id']} : document introuvable {c['document']}")
        if c.get("maillon") and c["maillon"] not in {m["id"] for m in carte.get("chaine", [])}: errs.append(f"{c['id']} : maillon inconnu {c['maillon']}")
    return errs

# ------------------------------------------------------------------ le score et l'itinéraire
def missing_links(carte) -> list[dict]:
    """Les maillons du chaînon (document 32) encore manquants pour ζ : la distance au but."""
    return [m for m in carte.get("chaine", []) if m["etat"] == "manquant"]

def score(c, carte, open_ids) -> dict:
    w = carte["poids"]
    valeur = sum(w[d] * g * c.get("probabilite", 0) for d, g in c.get("gains", {}).items())
    if not c.get("temoin"): valeur *= 0.5                                   # règle du témoin
    expl = len(c.get("repond_a", [])) + 0.5 * sum(1 for x in c.get("debloque", []) if x in open_ids)
    prox = carte.get("poids_maillon", 0.0) if c.get("maillon") in {m["id"] for m in missing_links(carte)} else 0.0   # distance au but
    pont = carte.get("poids_croisement", 0.0) * max(0, len(set(c.get("croise", []))) - 1)                         # règle du croisement
    return dict(valeur=valeur, explicatif=expl, proximite=prox, croisement=pont, cout=c["cout"], score=(valeur + expl + prox + pont) / c["cout"])

def _vtuple(txt: str) -> tuple:
    m = re.search(r"V(\d+)\.(\d+)", txt or ""); return (int(m.group(1)), int(m.group(2))) if m else (6, 0)

def veille(carte, ops) -> list[dict]:
    """Veille rétrospective : pour chaque piste écartée, les opérateurs entrés au registre depuis sa dernière lecture."""
    out = []
    for p in carte.get("pistes_ecartees", []):
        last = max(_vtuple(p["rejet"]), _vtuple(p.get("relue") or p["rejet"]))
        new = [o for o in ops.values() if _vtuple(o["section"]) > last]
        out.append(dict(p, depuis=f"V{last[0]}.{last[1]}", nouveaux=[o["nom"] for o in new], a_relire=len(new) >= carte.get("seuil_veille", 3)))
    return out

def realized(c, ind) -> dict | None:
    """Gains de niveau obtenus à la version du coup, lus dans l'indicateur (étape précédente -> étape du coup)."""
    et = ind["etapes"]; k = next((i for i, e in enumerate(et) if e["versions"] == c.get("version")), None)
    if k is None or k == 0: return None
    return {d: et[k]["niveaux"][d] - et[k - 1]["niveaux"][d] for d in et[k]["niveaux"] if et[k]["niveaux"][d] != et[k - 1]["niveaux"][d]}

def itinerary(carte):
    done = {c["id"] for c in carte["coups"] if c["statut"] == "fait"}
    todo = [c for c in carte["coups"] if c["statut"] == "ouvert"]; route = []
    while todo:
        open_ids = {c["id"] for c in todo}
        ready = [c for c in todo if all(p in done for p in c.get("prerequis", []))]
        if not ready: break
        best = max(ready, key=lambda c: (score(c, carte, open_ids)["score"], -c["cout"]))
        route.append((best, score(best, carte, open_ids))); done.add(best["id"]); todo.remove(best)
    return route

# ------------------------------------------------------------------ la page
CSS_NAV = r"""
.move { border: 1px solid var(--rule); border-radius: 4px; background: var(--paper); padding: 16px 18px; display: grid; gap: 12px; min-width: 0; }
.move h3 { margin: 0; font-family: var(--display); font-size: 20px; font-weight: 650; text-wrap: balance; }
.dial { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px 18px; }
.dial > div { display: grid; gap: 4px; align-content: start; min-width: 0; }
.dial .k, .opk { font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
.dial .k.th { color: var(--line); } .dial .k.an { color: var(--accent); } .dial .k.re { color: var(--void); }
.opl { display: grid; gap: 8px; }
.op { display: grid; grid-template-columns: minmax(150px, 210px) minmax(0, 1fr); gap: 4px 14px; padding-top: 8px; border-top: 1px dashed var(--rule); }
.op b { font-weight: 600; } .op .g { color: var(--muted); font-size: 13.5px; } .op .g::before { content: "garde : "; font-family: var(--mono); font-size: 11.5px; color: var(--accent); }
.sc { display: flex; flex-wrap: wrap; gap: 6px; } .chip.ex { color: var(--line); }
table.route { border-collapse: collapse; width: 100%; min-width: 760px; font-size: 13.5px; }
table.route th { text-align: left; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; padding: 6px 8px; border-bottom: 1px solid var(--rule); }
table.route td { padding: 9px 8px; border-bottom: 1px solid var(--grid); vertical-align: top; }
table.route td.num { font-family: var(--mono); font-variant-numeric: tabular-nums; white-space: nowrap; }
table.route td.rk { font-family: var(--mono); font-size: 18px; color: var(--line); width: 34px; }
.bar { display: inline-block; height: 8px; background: var(--line); border-radius: 0 2px 2px 0; vertical-align: 1px; margin-right: 6px; }
.trail { display: grid; gap: 0; }
.leg { display: grid; grid-template-columns: 74px minmax(0, 1fr); gap: 14px; padding: 10px 0; border-top: 1px solid var(--grid); }
.leg .lv2 { font-family: var(--mono); color: var(--line); font-size: 13px; } .leg p { font-size: 14px; } .leg .ap { color: var(--muted); font-size: 13.5px; }
.side { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
details.ops summary { cursor: pointer; font-weight: 600; } details.ops[open] summary { margin-bottom: 10px; }
table.opt { border-collapse: collapse; width: 100%; min-width: 820px; font-size: 13px; }
table.opt td, table.opt th { padding: 6px 8px; border-bottom: 1px solid var(--grid); vertical-align: top; text-align: left; }
table.opt th { font-family: var(--mono); font-size: 11px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; }
.rules { display: grid; gap: 8px; } .rules div { display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 12px; } .rules b { font-weight: 600; }
@media (max-width: 640px) { .op, .leg, .rules div { grid-template-columns: minmax(0, 1fr); } }
.leg, .op, .move { overflow-wrap: break-word; }
"""

def build(carte, ind, ops, links=True, standalone=True) -> str:
    bi = _indicateur(); dims = {d["id"]: d for d in ind["dimensions"]}; cur = ind["etapes"][-1]
    conj = {x["id"]: x["nom"] for x in ind.get("conjectures", [])}
    route = itinerary(carte); open_ids = {c["id"] for c in carte["coups"] if c["statut"] == "ouvert"}
    use = {}
    for c in carte["coups"]:
        for o in c.get("operateurs", []): use[o] = use.get(o, 0) + 1
    # position
    goal = carte["but"]; vis = dict(ind.get("visees", {})); vis[goal["dimension"]] = goal["niveau"]
    pct = lambda l: (l + 0.5) * 10; rows = []
    for d in ind["dimensions"]:
        y = cur["niveaux"][d["id"]]; t = vis.get(d["id"])
        marks = "<span class='lane'></span>" + (f"<span class='mk target' style='left:{pct(t)}%'></span>" if t is not None else "") + f"<span class='mk now' style='left:{pct(y)}%'></span>"
        rows.append(f"<div class='dim'><div class='name'><b>{d['nom']} <span class='mono' style='color:var(--line)'>{y}</span></b><small>poids {carte['poids'][d['id']]:g}"
                    f"{' · but : ' + str(t) if t is not None else ''}</small></div><div class='track' role='img' aria-label='{d['nom']} : niveau {y}'>{marks}</div></div>")
    position = (f"<div class='legend'><span><span class='sw'><span class='mk now'></span></span>position ({cur['versions']})</span><span><span class='sw'><span class='mk target'></span></span>but ou marche visée</span></div>"
                f"<div class='dims'><div class='axis'><span class='lbl'></span><div class='scale' aria-hidden='true'>{''.join(f'<span>{k}</span>' for k in range(10))}</div></div>{''.join(rows)}</div>")
    # prochain coup
    def opblock(names):
        return "".join(f"<div class='op'><div><b>{esc(o)}</b><div class='opk'>{esc(source(ops[o]['section']))}</div></div><div><div>{esc(ops[o]['image'] or ops[o]['enonce'])}</div>"
                       f"<div class='g'>{esc(ops[o]['garde'])}</div></div></div>" for o in names)
    def chips(c, s):
        g = " ".join(f"<span class='chip up'>{dims[d]['nom']} +{v}</span>" for d, v in c.get("gains", {}).items()) or "<span class='chip open'>aucun niveau visé</span>"
        px = f"<span class='chip up'>maillon manquant +{s['proximite']:g}</span>" if s["proximite"] else ""
        px += f"<span class='chip up'>croisement {' × '.join(esc(conj.get(x, x)) for x in c.get('croise', []))} +{s['croisement']:g}</span>" if s.get("croisement") else ""
        return (f"<div class='sc'>{g}<span class='chip ex'>explicatif {s['explicatif']:g}</span>{px}<span class='chip open'>coût {c['cout']}</span>"
                f"<span class='chip ok'>score {s['score']:.2f}</span></div>")
    if route:
        c, s = route[0]
        nxt = (f"<div class='move'><div class='eyebrow'>Prochain coup · {esc(c['id'])}</div><h3>{esc(c['titre'])}</h3><p>{esc(c['question'])}</p>{chips(c, s)}"
               f"<div class='dial'><div><span class='k th'>Thèse</span><p>{esc(c['these'])}</p></div><div><span class='k an'>Antithèse : le témoin</span><p>{esc(c['temoin'])}</p></div>"
               f"<div><span class='k re'>Ce qui la réfuterait</span><p>{esc(c.get('refutation', '—'))}</p></div>"
               f"<div><span class='k'>Répond à</span><ul style='margin:0;padding-left:18px'>{''.join(f'<li>{esc(q)}</li>' for q in c.get('repond_a', []))}</ul></div></div>"
               f"<div class='opl'><div class='opk'>Opérateurs, avec leur garde (lue dans le registre)</div>{opblock(c.get('operateurs', []))}</div></div>")
    else:
        nxt = "<p>Aucun coup ouvert dont les prérequis sont remplis.</p>"
    # itinéraire
    links_by_id = {m["id"]: m["nom"] for m in carte.get("chaine", [])}
    mx = max([s["score"] for _, s in route] + [1e-9]); tr = []
    for k, (c, s) in enumerate(route, 1):
        tr.append(f"<tr><td class='rk'>{k}</td><td><b>{esc(c['titre'])}</b><br><span class='foot'>{esc(', '.join(c.get('operateurs', [])))}</span></td>"
                  f"<td>{esc(links_by_id.get(c.get('maillon'), '—'))}</td><td class='num'>{s['valeur']:.2f}</td><td class='num'>{s['explicatif']:g}</td><td class='num'>{s['proximite']:g}</td><td class='num'>{s['croisement']:g}</td><td class='num'>{c['cout']}</td>"
                  f"<td class='num'><span class='bar' style='width:{60 * s['score'] / mx:.0f}px'></span>{s['score']:.2f}</td></tr>")
    table = (f"<div class='tablewrap' role='region' aria-label='Itinéraire proposé' tabindex='0'><table class='route'><thead><tr><th></th><th>Coup et opérateurs</th><th>Maillon</th><th>Valeur</th><th>Explicatif</th><th>Proximité</th><th>Croisement</th><th>Coût</th><th>Score</th></tr></thead>"
             f"<tbody>{''.join(tr)}</tbody></table></div>")
    # distance au but : le chaînon
    ETAT = {"acquis": "ok", "non nécessaire": "open", "manquant": "up"}
    chain = "".join(f"<div class='leg' style='grid-template-columns:132px minmax(0,1fr)'><div class='lv2'><span class='chip {ETAT.get(m['etat'], 'open')}'>{esc(m['etat'])}</span></div><div><p><b>{esc(m['nom'])}</b></p><p class='ap'>{esc(m['preuve'])}</p></div></div>"
                    for m in carte.get("chaine", []))
    miss = missing_links(carte)
    distance = (f"<p>Catégories encore ouvertes : <b>{len(miss)} maillon{'s' if len(miss) > 1 else ''} manquant{'s' if len(miss) > 1 else ''}</b>"
                f"{' (' + esc(', '.join(m['nom'] for m in miss)) + ')' if miss else ''}. Ce compte n’est pas une distance à RH. Un coup qui porte sur un maillon manquant reçoit +{carte.get('poids_maillon', 0):g} au score.</p><div class='trail'>{chain}</div>")
    # bilan : prévu contre obtenu
    def gtxt(g):
        return ", ".join(f"{dims[d]['nom']} {v:+d}" for d, v in g.items()) if g else "aucun niveau"
    bl = []
    for c in carte["coups"]:
        if c["statut"] != "fait": continue
        pv = c.get("prevision"); ob = realized(c, ind)
        ptxt = ("non enregistré (avant le navigateur)" if pv is None else
                (", ".join(f"{dims[d]['nom']} +{v} (p = {pv.get('probabilite', 0):g})" for d, v in pv.get("gains", {}).items()) or f"aucun niveau (p = {pv.get('probabilite', 0):g})"))
        bl.append(f"<tr><td class='num'>{esc(c.get('version', ''))}</td><td><b>{esc(c['titre'])}</b></td><td>{esc(ptxt)}</td><td>{esc(gtxt(ob) if ob is not None else '—')}</td>"
                  f"<td>{esc(c.get('refutation_tenue', '—'))}</td></tr>")
    bilan = (f"<div class='tablewrap' role='region' aria-label='Bilan des coups' tabindex='0'><table class='route'><thead><tr><th>Version</th><th>Coup</th><th>Prévu (pré-enregistré)</th><th>Obtenu (indicateur)</th><th>Réfutation annoncée</th></tr></thead>"
             f"<tbody>{''.join(bl)}</tbody></table></div>")
    # hors navigation autonome
    side = []
    for c in carte["coups"]:
        if c["statut"] in ("humain", "route à construire"):
            tag = "un relecteur humain" if c["statut"] == "humain" else "une route à construire"
            side.append(f"<div class='move'><div class='eyebrow'>{esc(c['statut'])}</div><h3>{esc(c['titre'])}</h3><p>{esc(c['question'])}</p>"
                        f"<p class='foot'>Hors de la navigation autonome : il y faut {tag}. Témoin : {esc(c['temoin'])}</p></div>")
    # route parcourue
    legs = []
    for c in carte["coups"]:
        if c["statut"] != "fait": continue
        doc = c.get("document")
        dl = ((f" · <a href=\"{html.escape(doc)}\">{html.escape(doc)}</a>" if links else f" · <span class='mono'>{html.escape(doc)}</span>") if doc else "")
        legs.append(f"<div class='leg'><div class='lv2'>{esc(c['version'])}</div><div><p><b>{esc(c['titre'])}</b> : {esc(c['question'])}</p>"
                    f"<p class='ap'>Témoin : {esc(c['temoin'])} Appris : {esc(c['appris'])}{dl}</p></div></div>")
    # opérateurs
    oprows = "".join(f"<tr><td><b>{esc(o['nom'])}</b>{' <span class=\"chip here\">×' + str(use[o['nom']]) + '</span>' if o['nom'] in use else ''}</td><td>{esc(o['image'] or o['enonce'])}</td><td>{esc(o['garde'])}</td><td>{esc(o['question'])}</td></tr>"
                     for o in ops.values())
    optable = (f"<details class='ops'><summary>Les {len(ops)} opérateurs du registre ({len(use)} utilisés sur la carte)</summary><div class='tablewrap' role='region' aria-label='Opérateurs' tabindex='0'>"
               f"<table class='opt'><thead><tr><th>Opérateur</th><th>Image ou objet</th><th>Garde</th><th>Question qu'il ouvre</th></tr></thead><tbody>{oprows}</tbody></table></div></details>")
    rules = "".join(f"<div><b>{esc(a)}</b><span>{esc(b)}</span></div>" for a, b in carte["regles"])
    vv = veille(carte, ops)
    vrows = "".join(f"<tr><td><b>{esc(v['titre'])}</b><br><span class='foot'>{esc(v['raison'])}</span></td><td class='num'>{esc(v['rejet'])}</td><td class='num'>{esc(v.get('relue') or '—')}</td>"
                    f"<td class='num'>{len(v['nouveaux'])}</td><td>{'<span class="chip up">à relire</span>' if v['a_relire'] else '<span class="chip open">à jour</span>'}"
                    f"<br><span class='foot'>{esc(', '.join(v['nouveaux'][:6]) + (' …' if len(v['nouveaux']) > 6 else ''))}</span></td></tr>" for v in vv)
    veille_html = (f"<p class='foot'>À chaque nouvel opérateur, les pistes écartées sont reconsidérées : une piste est signalée « à relire » quand au moins {carte.get('seuil_veille', 3)} opérateurs sont entrés au registre depuis sa dernière lecture.</p>"
                   f"<div class='tablewrap' role='region' aria-label='Veille rétrospective' tabindex='0'><table class='route'><thead><tr><th>Piste écartée</th><th>Écartée</th><th>Relue</th><th>Opérateurs nouveaux</th><th>État</th></tr></thead><tbody>{vrows}</tbody></table></div>") if vv else ""
    body = f"""
<div class="wrap">
{bi.topnav("navigateur", "../") if links else ""}
<header class="head"><div class="eyebrow">Programme Riemann · navigateur de recherche · position {cur['versions']}</div>
<h1>La démonstration comme itinéraire</h1>
<p class="lede">La destination mathématique est RH. L'indicateur situe le travail ; les cases vides désignent les mécanismes encore à construire. Les métaphores du registre proposent des opérateurs avec leurs conditions. Un pas compte lorsqu'il produit une preuve, une mesure contrôlée ou un obstacle explicite.</p></header>
<section class="sheet" aria-labelledby="t-pos"><h2 id="t-pos">Position et destination</h2><p class="foot">{esc(goal['libelle'])}</p>{position}</section>
<section class="sheet" aria-labelledby="t-dist"><h2 id="t-dist">Maillons ouverts du chaînon</h2>{distance}</section>
<section class="sheet" aria-labelledby="t-next"><h2 id="t-next">Le prochain coup</h2>{nxt}</section>
<section class="sheet" aria-labelledby="t-route"><h2 id="t-route">L'itinéraire proposé</h2><p class="foot">Choix glouton : à chaque pas, le coup ouvert de meilleur score dont les prérequis sont remplis. Les gains, probabilités et coûts sont des estimations écrites dans la carte, à discuter.</p>{table}</section>
<section class="sheet" aria-labelledby="t-side"><h2 id="t-side">Ce que le navigateur ne fait pas seul</h2><div class="side">{''.join(side)}</div></section>
<section class="sheet" aria-labelledby="t-trail"><h2 id="t-trail">La route parcourue</h2><div class="trail">{''.join(legs)}</div></section>
<section class="sheet" aria-labelledby="t-bilan"><h2 id="t-bilan">Bilan : prévu contre obtenu</h2><p class="foot">Chaque coup ouvert garde la prévision écrite avant le calcul ; une fois fait, on la compare à ce que l'indicateur a enregistré et l'on note si la réfutation annoncée a eu lieu. C'est ainsi que les estimations se calibrent.</p>{bilan}</section>
<section class="sheet" aria-labelledby="t-veille"><h2 id="t-veille">Veille rétrospective : les pistes écartées</h2>{veille_html}</section>
<section class="sheet" aria-labelledby="t-ops"><h2 id="t-ops">Les opérateurs</h2>{optable}</section>
<section class="sheet" aria-labelledby="t-rules"><h2 id="t-rules">Règles de navigation</h2><div class="rules">{rules}</div></section>
<p class="foot">Données : <span class="mono">2_Methode/Navigateur/carte_navigation.json</span>, l'indicateur et le registre des métaphores. Mise à jour : <span class="mono">python 2_Methode/Navigateur/build_navigateur.py</span>.</p>
</div>
"""
    head = f"""<title>Navigateur de recherche RH</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,650&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{bi.CSS}{CSS_NAV}</style>"""
    if carte.get('bilan_parcours'):
        phase='<section class="sheet"><h2>Parcours et propriétés — 14 octobre 2026</h2><p>'+esc(carte['bilan_parcours']['resultat'])+'</p><p><a href="PARCOURS_ET_PROPRIETES.html">Carte transversale</a> · <a href="CORRELATIONS_IDENTITE_ET_ENERGIE.html">Complément finalisé</a></p></section>'
        body=body.replace('</header>','</header>'+phase,1)
    elif carte.get('bilan_v649'):
        phase='<section class="sheet"><h2>V6.49 : compensation multi-premiers</h2><p>'+carte['bilan_v649']['resultat']+'</p><p><a href="'+carte['bilan_v649']['graphe']+'">Paiement conjoint</a> · <a href="'+carte['bilan_v649']['document']+'">Preuves et limites</a></p></section>'
    elif carte.get('bilan_v648'):
        phase='<section class="sheet"><h2>V6.48 : opérateur commun certifié</h2><p>'+carte['bilan_v648']['resultat']+'</p><p><a href="73_OPERATEUR_COMMUN.html">Tête, sources et queue</a> · <a href="'+carte['bilan_v648']['document']+'">Huit lemmes et budgets</a></p></section>'
    elif carte.get('bilan_v647'):
        phase='<section class="sheet"><h2>V6.47 : concentration et opérateur commun</h2><p>'+carte['bilan_v647']['resultat']+'</p><p><a href="72_CONCENTRATION_PROJETEE.html">Lego des concentrations</a> · <a href="'+carte['bilan_v647']['document']+'">Huit lemmes et certificat</a></p></section>'
    elif carte.get('bilan_v646'):
        phase='<section class="sheet"><h2>V6.46 : Lego et certificat borné complet</h2><p>'+carte['bilan_v646']['resultat']+'</p><p><a href="71_LEGO_REUTILISABLE.html">Atelier de raccords</a> · <a href="'+carte['bilan_v646']['document']+'">K1–K7 et encadrements</a></p></section>'
    elif carte.get('bilan_v645'):
        phase='<section class="sheet"><h2>V6.45 : pont arithmétique et dette des sources</h2><p>'+carte['bilan_v645']['resultat']+'</p><p><a href="70_PONT_ARITHMETIQUE.html">Atelier et contrats</a> · <a href="'+carte['bilan_v645']['document']+'">C1–C5 et exécution</a></p></section>'
    elif carte.get('bilan_v644'):
        phase='<section class="sheet"><h2>V6.44 : langue des domaines et queue effective</h2><p>'+carte['bilan_v644']['resultat']+'</p><p><a href="69_LANGUE_DES_PASSAGES.html">Dictionnaire et atelier</a> · <a href="'+carte['bilan_v644']['document']+'">Preuves et calculs</a></p></section>'
    elif carte.get('bilan_v643'):
        phase='<section class="sheet"><h2>Phase V6.43 : construire des ponts</h2><p>Transport opératoire, domaine H¹, cœur admissible, régularisation décalée et Schur sont démontrés. La priorité est un invariant arithmétique sur une famille, avec contrôle des noyaux et du défaut. Le classement général reste documentaire et conventionnel.</p><p><a href="67_GRAPHE_DES_PONTS.html">Carte et pilote courant</a> · <a href="67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf">Lemmes et preuves</a></p></section>'
    elif carte.get('bilan_v642'):
        phase='''<section class="sheet"><h2>Suite de la phase V6.42</h2><p>Un pli choisi, le contour continu de sa paire et quatre boîtes de racines sont validés. La suite locale est le déploiement sur une fibre à A constant ; la suite globale est le contrôle de la compensation archimédienne et des corrélations signées, sur tous les tests. Le classement général conserve ses poids conventionnels.</p><p><a href="66_GRAPHE_DES_CERTIFICATS.html">Graphe courant : certificat et contrats</a> · <a href="66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf">Dossier et preuves</a></p></section>'''
        if not links:phase=re.sub(r'<a[^>]*>(.*?)</a>',r'\1',phase)
        body=body.replace('</header>','</header>'+phase,1)
    elif carte.get('bilan_v641'):
        phase='''<section class="sheet"><h2>Suite de la phase V6.41</h2><p>La phase de passages est exécutée : fibres, jets, plis et blocs locaux. Le dossier retient ensuite la certification d’un pli et d’un contour de deux zéros, puis l’audit du contrat arithmétique uniforme. Le classement général ci-dessous conserve ses coûts et poids conventionnels ; il ne remplace pas ces dépendances de phase.</p><p><a href="65_GRAPHE_DES_PASSAGES.html">Graphe : acquis, hypothèses et pont manquant</a> · <a href="65_FIBRES_PLIS_ET_POSITIVITE.pdf">Dossier et démonstrations</a></p></section>'''
        if not links:phase=re.sub(r'<a[^>]*>(.*?)</a>',r'\1',phase)
        body=body.replace('</header>','</header>'+phase,1)
    if standalone:
        return f"<!doctype html>\n<html lang=\"fr\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n{head}\n</head><body>{body}</body></html>\n"
    return head + body

if __name__ == "__main__":
    carte, ind, ops = load(); errs = check(carte, ops, ind)
    if errs:
        print("carte incohérente :\n  " + "\n  ".join(errs)); sys.exit(1)
    for k, (c, s) in enumerate(itinerary(carte), 1):
        print(f"{k}. {c['titre']:45s} score {s['score']:.2f}  (valeur {s['valeur']:.2f}, explicatif {s['explicatif']:g}, maillon {s['proximite']:g}, croisement {s['croisement']:g}, coût {c['cout']})")
    if "--artefact" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--artefact") + 1]); out.write_text(build(carte, ind, ops, links=False, standalone=False), encoding="utf-8")
    else:
        out = OUT; out.write_text(build(carte, ind, ops), encoding="utf-8")
    print(f"opérateurs lus dans le registre : {len(ops)} ; écrit : {out}")
