#!/usr/bin/env python3
"""Portail du Programme Riemann : la page d'entrée qui reprend tout, générée à partir du corpus.

    python 2_Methode/Portail/build_portail.py                 -> 00_PORTAIL.html (racine du corpus)
    python 2_Methode/Portail/build_portail.py --publication D -> D : copie prête à publier en ligne (portail, carte, indicateur,
                                                                 navigateur, mode d'emploi et documents liés ; .md et .docx convertis en HTML)

Sources : l'indicateur (position, étapes, documents par version), le navigateur (prochain coup, maillon manquant),
le dossier 1_Presentation (tous les documents), VERSION.txt et le dossier des tests.
"""
from __future__ import annotations
import html, importlib.util, json, os, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; PRES = ROOT / "1_Presentation"
OUT = ROOT / "00_PORTAIL.html"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

BI = _load("build_indicateur", ROOT / "2_Methode" / "Indicateur" / "build_indicateur.py")
BN = _load("build_navigateur", ROOT / "2_Methode" / "Navigateur" / "build_navigateur.py")

GROUPS = [(1, 8, "Synthèse, articles et dossier de relecture"), (9, 15, "Attaques, audits et leçons (v3 à V6.0)"),
          (16, 25, "V6 : instruments, métaphores et audits"), (26, 99, "V6.4 et suivantes : la nécessité et le chaînon")]
# Publication en ligne : seuls les fichiers relus pour la publication sont mis en ligne ; les autres liens mènent à une page
# « dans le corpus » qui renvoie au zip. Étendre cette liste après relecture.
ONLINE_ALLOW = ["00_PORTAIL.html", "00_Carte_des_idees.html", "00_Liste_des_figures.html", "README.md", "1_Presentation/31_INDICATEUR_D_AVANCEMENT.html",
                "1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html", "1_Presentation/0[167]_*", "1_Presentation/2[6-9]_*", "1_Presentation/3[0-9]_*", "1_Presentation/4[0-9]_*",
                "1_Presentation/relecture/*"]
DOSSIERS = {37: "relecture", 55: "articles"}   # sous-dossier de 1_Presentation rattaché à un document (lu en entier avant publication)

def dossier_label(stem: str) -> str:
    if stem.startswith("00_"): return "entrée"
    t = stem.replace("RELECTURE_", "").replace("THEOREME_", "Th. ").replace("_RESUME_FR", " (FR)").replace("_EN", "").replace("_", " ")
    return t[0] + t[1:].lower() if not t.startswith("Th.") else t
STUB = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Document dans le corpus</title>{css}</head><body>{nav}<main><h1>Ce document est dans le corpus</h1>
<p>Il n'est pas encore publié en ligne : seuls les documents relus pour la publication le sont. Il se trouve dans le zip du corpus, à l'emplacement indiqué par le lien d'origine.</p>
<p><a href="index.html">Retour au portail</a></p></main></body></html>
"""

def allowed(rel: str) -> bool:
    from fnmatch import fnmatch
    return any(fnmatch(rel, pat) for pat in ONLINE_ALLOW)

FORMATS = {".pdf": "PDF", ".md": "texte", ".docx": "Word", ".html": "page", ".tex": "LaTeX"}

def esc(s: str) -> str:
    return BN.esc(s)

def version_line() -> str:
    return (ROOT / "VERSION.txt").read_text(encoding="utf-8-sig").splitlines()[0].split("—")[-1].strip()

def count_tests() -> int:
    return sum(len(re.findall(r"^def test_", f.read_text(encoding="utf-8-sig"), flags=re.M)) for f in (ROOT / "3_Preuves_et_calculs" / "tests").glob("test_*.py"))

def documents(ind) -> list[dict]:
    """Un document par préfixe « NN_nom » de 1_Presentation, avec ses formats, ses figures et l'étape où il a été produit."""
    label, step = {}, {}
    for e in ind["etapes"]:
        for lab, rel in e["documents"]:
            name = rel.split("/")[-1]; label.setdefault(name, lab); step.setdefault(name, e["court"])
    stems = {}
    for f in sorted(PRES.iterdir()):
        m = re.match(r"(\d\d)_", f.name)
        if not m or f.is_dir(): continue
        stems.setdefault(f.stem, []).append(f)
    docs = []
    for stem, files in stems.items():
        fmts = [f for f in files if f.suffix in FORMATS]
        if not fmts: continue
        num = int(stem[:2]); title = None
        md = next((f for f in fmts if f.suffix == ".md"), None)
        if md:
            for line in md.read_text(encoding="utf-8-sig").splitlines():
                if line.startswith("# "): title = line[2:].strip(); break
        if not title:
            title = next((label[f.name] for f in fmts if f.name in label), None) or stem[3:].replace("_", " ")
        figs = [f for f in sorted(PRES.glob(f"{stem[:2]}_*.png"))]
        docs.append(dict(num=num, stem=stem, title=title, files=sorted(fmts, key=lambda f: list(FORMATS).index(f.suffix)), figures=figs,
                         etape=next((step[f.name] for f in fmts if f.name in step), "")))
    return sorted(docs, key=lambda d: (d["num"], d["stem"]))

CSS_P = r"""
.cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.card { display: grid; gap: 6px; align-content: start; border: 1px solid var(--rule); border-radius: 4px; background: var(--paper); padding: 14px 16px; color: inherit; text-decoration: none; min-width: 0; }
.card:hover, .card:focus-visible { border-color: var(--line); }
.card b { font-family: var(--display); font-size: 18px; font-weight: 650; color: var(--ink); }
.card span { color: var(--muted); font-size: 14px; }
.state { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; }
.lvl { border-left: 3px solid var(--line); padding: 4px 10px; display: grid; gap: 2px; }
.lvl .n { font-family: var(--mono); font-size: 22px; color: var(--line); font-variant-numeric: tabular-nums; }
.lvl .d { font-size: 13.5px; color: var(--muted); }
.duo { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
.box { border: 1px solid var(--rule); border-radius: 4px; padding: 12px 14px; display: grid; gap: 6px; background: var(--paper); min-width: 0; }
table.docs { border-collapse: collapse; width: 100%; min-width: 640px; font-size: 14px; }
table.docs thead { display: table-header-group; }
table.docs th { text-align: left; font-family: var(--mono); font-size: 11.5px; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted); font-weight: 500; padding: 6px 8px; border-bottom: 1px solid var(--rule); }
table.docs td { padding: 8px; border-bottom: 1px solid var(--grid); vertical-align: top; }
.sheet p .mono, p.foot .mono { overflow-wrap: anywhere; }
table.docs td.num { font-family: var(--mono); color: var(--line); white-space: nowrap; font-variant-numeric: tabular-nums; }
table.docs tr.grp td { font-family: var(--display); font-size: 16px; font-weight: 650; padding-top: 18px; border-bottom: 1px solid var(--rule); }
.fmt a { margin-right: 10px; white-space: nowrap; }
.recent { display: grid; gap: 0; }
"""

def build(standalone: bool = True) -> str:
    ind = BI.load(); carte, ind2, ops = BN.load(); cur = ind["etapes"][-1]; dims = ind["dimensions"]
    route = BN.itinerary(carte); miss = BN.missing_links(carte); docs = documents(ind)
    a = lambda href, text: f"<a href=\"{html.escape(href)}\">{text}</a>"
    nav = BI.topnav("portail", "")
    cards = "".join(f"<a class='card' href='{h}'><b>{t}</b><span>{d}</span></a>" for t, h, d in (
        ("Compensation multi-premiers", "1_Presentation/74_COMPENSATION_MULTI_PREMIERS.html", "Paiement joint certifié ; saut L² et petite dette en R ; extension positive ouverte."),
        ("Compensation et preuves", "1_Presentation/74_COMPENSATION_MULTI_PREMIERS.pdf", "Document74 : huit lemmes, comparaisons exécutées et prochain raccord."),
        ("Opérateur commun certifié", "1_Presentation/73_OPERATEUR_COMMUN.html", "Tête, sources et queue du minorant ; tous tests jusqu’à1/2 ; double raccord exécuté."),
        ("Opérateur, tête et sources", "1_Presentation/73_OPERATEUR_COMMUN_TETE_SOURCES_ET_QUEUE.pdf", "Document73 : huit lemmes, Gauss, erreurs, Bareiss et Schur certifié."),
        ("Lego des concentrations", "1_Presentation/72_CONCENTRATION_PROJETEE.html", "Tous tests jusqu’à3/8 ; opérateur commun ; tête et sources à construire."),
        ("Concentration et opérateur commun", "1_Presentation/72_CONCENTRATION_PROJETEE_ET_OPERATEUR_COMMUN.pdf", "Document72 : huit lemmes, intervalles, erreurs, certificat et diagnostic séparé."),
        ("Le Lego réutilisable", "1_Presentation/71_LEGO_REUTILISABLE.html", "Premier certificat complet : tous tests, premier2 présent, 0<S≤0,347 ; atelier de raccords."),
        ("Certificat local complet", "1_Presentation/71_LEGO_REUTILISABLE_ET_PREMIER_CERTIFICAT_COMPLET.pdf", "Document71 : K1–K7, intervalles, constantes rationnelles, modèles perturbés et gardes."),
        ("Le pont arithmétique", "1_Presentation/70_PONT_ARITHMETIQUE.html", "Annulation du pôle, fluctuation de Chebyshev, dette par résidus et budgets encadrés."),
        ("Pont arithmétique et dette", "1_Presentation/70_PONT_ARITHMETIQUE_ET_DETTE_DE_COUPLAGE.pdf", "Document 70 : C1–C5, obstruction uniforme du modèle continu et contrats suffisants."),
        ("La langue des passages", "1_Presentation/69_LANGUE_DES_PASSAGES.html", "Dictionnaire progressif, arithmétique des jets et atelier de traduction typée."),
        ("Arithmétique et queue effective", "1_Presentation/68_ARITHMETIQUE_DES_PASSAGES_ET_QUEUE_EFFECTIVE.pdf", "Document 68 : huit preuves auxiliaires, I−compact et réduction Schur avec budget."),
        ("Dictionnaire des domaines", "1_Presentation/69_DICTIONNAIRE_PROGRESSIF_DES_DOMAINES.pdf", "Document 69 : objets, fonctions, opérateurs, images et gardes."),
        ("Construire des ponts avec Bellman", "1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf", "Document 67 : transports, domaine H¹, cœur dense, régularisation et dette de Schur."),
        ("Ponts et contrats", "1_Presentation/67_GRAPHE_DES_PONTS.html", "Carte des implications et pilote adaptatif de constructions complémentaires."),
        ("Un pli certifié et sa paire", "1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf", "Document 66 : existence, unicité et quatre racines validées ; Rouché continu ; inégalité arithmétique globale explicitée."),
        ("Graphe des certificats", "1_Presentation/66_GRAPHE_DES_CERTIFICATS.html", "Ce qui est maintenant certifié, les deux nouvelles voies fermées sous hypothèses et le pont global restant."),
        ("Graphe des passages", "1_Presentation/65_GRAPHE_DES_PASSAGES.html", "Idées, lemmes et preuves : paire sans étiquette, deux portes vers RH, pont arithmétique manquant et voies fermées."),
        ("Fibres, plis et positivité", "1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.pdf", "Document 65 : géométrie de A, jets, 20 candidats de collisions, 18 blocs et contrats du passage au global."),
        ("Comparaison exacte V13", "1_Presentation/64_COMPARAISON_EXACTE_V13.pdf", "12 couples : 8 détections plus précoces, 4 plus tardives à D élevé ; 24 racines recoupées. Suite : suivre les branches."),
        ("Contraintes exactes V13", "1_Presentation/63_CONTRAINTES_EXACTES_V13.pdf", "Étape 1 démontrée : D varie sous contraintes exactes ; preuve et témoins."),
        ("Atlas des décisions", "1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html", "Les 74 documents ; paiement multi-premiers V6.49 ; certificat positif toujours jusqu’à1/2 ;43fiches et19outils avec usages."),
        ("Le cheminement intellectuel", "1_Presentation/06_CHEMINEMENT_INTELLECTUEL.md", "D'où viennent les intuitions, ce qui les a testées, ce qui en est resté : le récit, de la v1 à la V6.17."),
        ("Synthèse historique", "1_Presentation/01_SYNTHESE_FR.md", "Synthèse conservée à son état d’origine ; bilan courant dans l’atlas des décisions."),
        ("Guide de lecture intuitif", "1_Presentation/07_GUIDE_DE_LECTURE_INTUITIF.md", "Les images du programme, de la plus simple à la plus fine, et l'endroit où chacune casse."),
        ("Plan de recherche V6.19", "1_Presentation/43_PLAN_DE_RECHERCHE_LA_RENCONTRE_A_N.pdf", "La Rencontre à n en 3D, sept axes selon la méthode symbolique → opérateur → fonctions → identification, avec prévisions."),
        ("Matrice des théories", "1_Presentation/44_MATRICE_DES_THEORIES.html", "Où se situe chaque théorie par rapport à RH : équivalences, implications, témoins ; cases à compléter."),
        ("Registre des sources", "1_Presentation/42_REGISTRE_DES_SOURCES.md", "Chaque article cité : couleur d'intérêt, état de vérification, lien vers le résumé, priorités de lecture."),
        ("Carte des idées", "00_Carte_des_idees.html", "Les idées par thème, avec leur statut (démontré, mesuré, obstacle) et leurs documents. Cliquez un nœud pour son détail."),
        ("Indicateur d'avancement", "1_Presentation/31_INDICATEUR_D_AVANCEMENT.html", "Chaque version depuis le 3 octobre : ce qui a été franchi, les niveaux qui ont bougé, les documents produits."),
        ("Navigateur de recherche", "1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html", "Où on en est, le maillon manquant, le prochain coup et la route parcourue."),
        ("Liste des figures", "00_Liste_des_figures.html", "Toutes les figures du programme, en miniatures, avec leur légende et le document qui les explique."),
        ("Mode d'emploi", "README.md", "Le README du corpus : organisation des dossiers, ordre de lecture, journal des versions.")))
    lv = "".join(f"<div class='lvl'><span class='n'>{cur['niveaux'][d['id']]}</span><b>{d['nom']}</b><span class='d'>{BI.txt(ind['echelle'][cur['niveaux'][d['id']]][0])}</span></div>" for d in dims)
    nxt = route[0][0] if route else None
    current_path = ROOT / '3_Preuves_et_calculs/data/v649_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v648_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v647_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v646_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v645_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v644_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v643_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v642_etat_recherche.json'
    if not current_path.exists():current_path=ROOT/'3_Preuves_et_calculs/data/v641_etat_recherche.json'
    if current_path.exists():
        current_state=json.loads(current_path.read_text(encoding='utf-8-sig'))
        phase_next=current_state.get('next_actions',[])
        nxt=next((c for key in phase_next for c in carte['coups'] if c['id']==key and c['statut']=='ouvert'),nxt)
    state = (f"<div class='state'>{lv}</div><div class='duo'>"
             f"<div class='box'><span class='eyebrow'>Maillon manquant</span><b>{esc(', '.join(m['nom'] for m in miss) or 'aucun')}</b><span class='foot'>{esc(miss[0]['preuve']) if miss else ''}</span></div>"
             + (f"<div class='box'><span class='eyebrow'>Prochain coup de la phase courante</span><b>{esc(nxt['titre'])}</b><span class='foot'>{esc(nxt['question'])}</span></div>" if nxt else "")
             + "</div>")
    rec = "".join(f"<div class='leg'><div class='lv2'>{esc(e['court'])}<br><span class='foot'>{esc(e['jour'])}</span></div><div><p>{BI.txt(e['franchi'])}</p>"
                  f"<p class='ap'>{' · '.join(a('1_Presentation/' + rel, esc(lab)) for lab, rel in e['documents'])}</p></div></div>" for e in ind["etapes"][-5:][::-1])
    rows, g = [], None
    for d in docs:
        grp = next(t for lo, hi, t in GROUPS if lo <= d["num"] <= hi)
        if grp != g: rows.append(f"<tr class='grp'><td colspan='4'>{esc(grp)}</td></tr>"); g = grp
        fm = "".join(a("1_Presentation/" + f.name, FORMATS[f.suffix]) for f in d["files"])
        fg = (" · figures : " + ", ".join(a("1_Presentation/" + f.name, str(k)) for k, f in enumerate(d["figures"], 1))) if d["figures"] else ""
        sub = DOSSIERS.get(d["num"])
        if sub and (PRES / sub).is_dir():
            fg += " · dossier : " + ", ".join(a(f"1_Presentation/{sub}/{f.name}", esc(dossier_label(f.stem))) for f in sorted(g for g in [*(PRES / sub).glob("*.md"), *(PRES / sub).glob("*.pdf"), *(PRES / sub).glob("*.txt")] if "_fig" not in g.name))
        rows.append(f"<tr><td class='num'>{d['num']:02d}</td><td>{esc(d['title'])}</td><td class='fmt'>{fm}<span class='foot'>{fg}</span></td><td class='num'>{esc(d['etape'])}</td></tr>")
    table = (f"<div class='tablewrap' role='region' aria-label='Tous les documents' tabindex='0'><table class='docs'><thead><tr><th>N°</th><th>Document</th><th>Formats</th><th>Étape</th></tr></thead>"
             f"<tbody>{''.join(rows)}</tbody></table></div>")
    body = f"""
<div class="wrap">
{nav}
<header class="head"><div class="eyebrow">Programme Riemann · portail · {esc(version_line())} · {esc(cur['jour'])} 2026</div>
<h1>Portail du Programme Riemann</h1>
<p class="lede">Étude d'une quantité construite avec les nombres premiers, dont la croissance reflète la position des zéros de ζ, puis recherche de ce qui rend l'hypothèse de Riemann nécessaire. Hypothèse de travail de l'auteur : RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand qui la rend nécessaire. Aucune preuve de RH n'est revendiquée ; les énoncés démontrés n'ont pas encore été relus par un spécialiste.</p></header>
<section class="sheet" aria-labelledby="t-start"><h2 id="t-start">Par où commencer</h2><div class="cards">{cards}</div></section>
<section class="sheet" aria-labelledby="t-state"><h2 id="t-state">Où on en est ({esc(cur['versions'])})</h2><p class="foot">Niveaux de maturité de 0 à 9 sur les {len(dims)} dimensions de l'indicateur.</p>{state}</section>
<section class="sheet" aria-labelledby="t-recent"><h2 id="t-recent">Les dernières étapes</h2><div class="recent">{rec}</div><p class="foot">Toutes les étapes depuis le 3 octobre : {a('1_Presentation/31_INDICATEUR_D_AVANCEMENT.html', "l'indicateur d'avancement")}.</p></section>
<section class="sheet" aria-labelledby="t-docs"><h2 id="t-docs">Tous les documents</h2><p class="foot">{len(docs)} documents de présentation, du plus ancien au plus récent ; la colonne « étape » renvoie à l'indicateur.</p>{table}</section>
<section class="sheet" aria-labelledby="t-code"><h2 id="t-code">Code, données et tests</h2><p>Les calculs sont dans {a('3_Preuves_et_calculs/README.md', '3_Preuves_et_calculs')} : code source, scripts, données et {count_tests()} tests, lancés par <span class="mono">python 3_Preuves_et_calculs/tests/run_all_tests.py</span>. Chaque version est reproduite à l'identique sur une copie neuve avant d'être livrée.</p></section>
<p class="foot">Page générée par <span class="mono">python 2_Methode/Portail/build_portail.py</span> à partir de l'indicateur, du navigateur et du dossier 1_Presentation.</p>
</div>
"""
    head = f"""<title>Portail du Programme Riemann</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,650&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{BI.CSS}{BN.CSS_NAV}{CSS_P}</style>"""
    if standalone:
        return f"<!doctype html>\n<html lang=\"fr\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n{head}\n</head><body>{body}</body></html>\n"
    return head + body

def check_links(page: str, base: Path) -> list[str]:
    return sorted({h for h in re.findall(r'href="([^"#]+)"', page) if not h.startswith("http") and not (base / h).exists()})

# ------------------------------------------------------------------ publication en ligne
DOC_CSS = """<style>
:root { --bg: #f6f8fa; --fg: #17222f; --muted: #566577; --rule: #c6d1dc; --link: #1d5d8c; --code: #e9eef3; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #0f161f; --fg: #e1e8ef; --muted: #9aa9b9; --rule: #32465b; --link: #8cc0ea; --code: #1a2532; color-scheme: dark } }
:root[data-theme="dark"] { --bg: #0f161f; --fg: #e1e8ef; --muted: #9aa9b9; --rule: #32465b; --link: #8cc0ea; --code: #1a2532; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font: 16px/1.6 "IBM Plex Sans", system-ui, sans-serif; margin: 0; padding-inline: 16px; padding-block: 20px 48px; }
main, nav { max-width: 860px; margin: 0 auto; }
nav { display: flex; flex-wrap: wrap; gap: 4px 18px; padding-bottom: 10px; margin-bottom: 18px; border-bottom: 1px solid var(--rule); font-size: 14px; }
nav a { color: var(--muted); text-decoration: none; } a { color: var(--link); }
h1, h2, h3 { font-family: Literata, Georgia, serif; line-height: 1.25; text-wrap: balance; }
table { border-collapse: collapse; display: block; overflow-x: auto; max-width: 100%; font-size: 14px; }
th, td { border-bottom: 1px solid var(--rule); padding: 5px 8px; text-align: left; vertical-align: top; }
code, pre { background: var(--code); font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 13px; }
pre { padding: 10px; overflow-x: auto; } img { max-width: 100%; height: auto; } main { overflow-wrap: break-word; }
</style>"""

def rewrite(s: str) -> str:
    """Liens relatifs vers des .md ou .docx -> .html (versions converties pour la lecture en ligne)."""
    return re.sub(r'href=(["\'])([^"\'#:]+?)\.(md|docx)(#[^"\']*)?\1', lambda m: f'href={m.group(1)}{m.group(2)}.html{m.group(4) or ""}{m.group(1)}', s)

def _nav_snippet(depth: int) -> str:
    p = "../" * depth
    return BI.topnav("", p).replace("<nav class='topnav'", "<nav")

def publication(dest: Path) -> dict:
    """Copie prête à publier : pages d'entrée, documents qu'elles citent, .md et .docx convertis en HTML, liens réécrits."""
    if dest.exists(): shutil.rmtree(dest)
    dest.mkdir(parents=True)
    entry = {"00_PORTAIL.html": ROOT / "00_PORTAIL.html", "00_Carte_des_idees.html": ROOT / "00_Carte_des_idees.html",
             "1_Presentation/31_INDICATEUR_D_AVANCEMENT.html": PRES / "31_INDICATEUR_D_AVANCEMENT.html",
             "1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html": PRES / "34_NAVIGATEUR_DE_RECHERCHE.html"}
    linked = {"README.md"}
    for rel, src in entry.items():
        base = Path(rel).parent
        for h in re.findall(r'href="([^"#]+)"', src.read_text(encoding="utf-8-sig")):
            if h.startswith("http"): continue
            t = (ROOT / base / h).resolve()
            if t.exists() and t.is_file() and ROOT in t.parents: linked.add(str(t.relative_to(ROOT)))
    for rel in list(linked):                                       # figures citées par les documents en texte
        if rel.endswith(".md"):
            for img in re.findall(r"!\[[^\]]*\]\(([^)\s]+)\)", (ROOT / rel).read_text(encoding="utf-8-sig")):
                t = (ROOT / Path(rel).parent / img).resolve()
                if t.exists(): linked.add(str(t.relative_to(ROOT)))
    linked = {r for r in linked if allowed(r)}
    conv = lambda r: r[:-3] + ".html" if r.endswith(".md") else (r[:-5] + ".html" if r.endswith(".docx") else r)
    files = {}
    for rel in sorted(linked):
        src = ROOT / rel; out = dest / conv(rel); out.parent.mkdir(parents=True, exist_ok=True); depth = len(Path(rel).parts) - 1
        if rel.endswith((".md", ".docx")):
            title = src.stem.replace("_", " ")
            if rel.endswith(".md"):
                m = re.search(r"^# (.+)$", src.read_text(encoding="utf-8-sig"), flags=re.M); title = m.group(1) if m else title
            navf = dest / "_nav.html"; navf.write_text(_nav_snippet(depth), encoding="utf-8")
            cssf = dest / "_css.html"; cssf.write_text(DOC_CSS, encoding="utf-8")
            fmt = "markdown-implicit_figures" if rel.endswith(".md") else "docx"
            subprocess.run(["pandoc", "-f", fmt, "-t", "html5", "-s", "--metadata", f"pagetitle={title}", "-M", "document-css=false",
                            "-H", str(cssf), "-B", str(navf), str(src), "-o", str(out)], check=True, cwd=src.parent)
            s = out.read_text(encoding="utf-8-sig")
            s = s.replace("<body>", "<body><main>", 1).replace("</body>", "</main></body>", 1) if "<main>" not in s else s
            out.write_text(s, encoding="utf-8")
        else:
            shutil.copy2(src, out)
        files[conv(rel)] = out
    for rel, src in entry.items():
        out = dest / rel; out.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, out); files[rel] = out
    for p in [dest / "_nav.html", dest / "_css.html"]:
        if p.exists(): p.unlink()
    (dest / "index.html").write_text(build(standalone=False), encoding="utf-8")
    (dest / "hors_ligne.html").write_text(STUB.format(css=DOC_CSS, nav=_nav_snippet(0)), encoding="utf-8"); files["hors_ligne.html"] = dest / "hors_ligne.html"
    staged = {str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file()}
    def local(out: Path, s: str) -> str:                           # .md/.docx -> .html ; lien vers un fichier non publié -> page « dans le corpus »
        s = rewrite(s); base = out.parent.relative_to(dest)
        def fix(m):
            q, h, frag = m.group(1), m.group(2), m.group(3) or ""
            if h.startswith(("http:", "https:", "mailto:")): return m.group(0)
            norm = os.path.normpath(str(base / h))
            if norm in staged: return m.group(0)
            return f'href={q}{"../" * len(base.parts)}hors_ligne.html{q}'
        return re.sub(r'href=(["\'])([^"\'#]+)(#[^"\']*)?\1', fix, s)
    for out in list(files.values()) + [dest / "index.html"]:
        if out.suffix == ".html": out.write_text(local(out, out.read_text(encoding="utf-8-sig")), encoding="utf-8")
    return files

if __name__ == "__main__":
    page = build(); bad = check_links(page, ROOT)
    if bad:
        print("liens introuvables :", bad); sys.exit(1)
    OUT.write_text(page, encoding="utf-8"); print(f"écrit : {OUT}")
    if "--publication" in sys.argv:
        d = Path(sys.argv[sys.argv.index("--publication") + 1]); f = publication(d)
        size = sum(p.stat().st_size for p in f.values())
        print(f"publication : {len(f)} fichiers, {size / 1e6:.1f} Mo, dans {d}")
