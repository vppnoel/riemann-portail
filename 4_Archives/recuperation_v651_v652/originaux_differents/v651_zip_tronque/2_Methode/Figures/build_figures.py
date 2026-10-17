"""Liste des figures du corpus : page 00_Liste_des_figures.html (miniatures, légendes, document source) et
1_Presentation/LISTE_DES_FIGURES.md (lisible sur GitHub).

Auteur et titulaire des droits : Vincent NOËL.
Sources : images ![légende](fichier.png) des documents de 1_Presentation ; figures de calcul de 3_Preuves_et_calculs/data
(légende tirée du script qui les produit) ; figures des articles (PDF).
Usage : python 2_Methode/Figures/build_figures.py
"""
from __future__ import annotations
from pathlib import Path
import html, importlib.util, re

ROOT = Path(__file__).resolve().parents[2]; PRES = ROOT / "1_Presentation"; DATA = ROOT / "3_Preuves_et_calculs" / "data"
SCRIPTS = ROOT / "3_Preuves_et_calculs" / "scripts"
esc = lambda s: html.escape(str(s), quote=True)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def title_of(md: Path) -> str:
    for line in md.read_text(encoding="utf-8-sig").splitlines():
        if line.startswith("# "): return line[2:].strip()
    return md.stem


def doc_figures():
    out, seen = [], set()
    for md in sorted(PRES.glob("[0-9][0-9]_*.md")):
        for alt, f in re.findall(r"!\[([^\]]*)\]\(([^)\s]+\.png)\)", md.read_text(encoding="utf-8-sig")):
            p = PRES / f
            if not p.exists(): continue
            pdf = md.with_suffix(".pdf")
            out.append(dict(num=md.name[:2], fichier=f"1_Presentation/{f}", legende=alt, doc_titre=title_of(md),
                            doc=f"1_Presentation/{pdf.name if pdf.exists() else md.name}")); seen.add(f)
    for p in sorted(PRES.glob("*.png")):
        if p.name not in seen:
            out.append(dict(num=p.name[:2], fichier=f"1_Presentation/{p.name}", legende=p.stem[3:].replace("_", " "), doc_titre="(figure sans renvoi dans un document)", doc=""))
    return sorted(out, key=lambda x: (x["num"], x["fichier"]))


def calc_figures():
    texts = {s: s.read_text(encoding="utf-8-sig", errors="replace") for s in SCRIPTS.glob("*.py")}
    out = []
    for p in sorted(DATA.glob("*.png")):
        src = [s for s, t in texts.items() if p.name in t]
        lead = ""
        if src:
            m = re.search(r'"""(.*?)(?:\n|""")', texts[src[0]], flags=re.S); lead = (m.group(1).strip() if m else "")
        out.append(dict(fichier=f"3_Preuves_et_calculs/data/{p.name}", legende=p.stem.replace("_", " "),
                        script=f"3_Preuves_et_calculs/scripts/{src[0].name}" if src else "", contexte=lead))
    return out


def article_figures():
    A = PRES / "articles"
    caps = {"art1_fig1.pdf": "Article 1 : rapport Q(X)/((4κ/3) log³ X) et modèle à deux termes",
            "art1_fig2.pdf": "Article 1 : famille de Nyman–Beurling, e_N² log N/κ",
            "art2_fig1.pdf": "Article 2 : directions positives en trop sur 180 réglages",
            "art2_fig2.pdf": "Article 2 : plus petites valeurs propres de G_L pour ζ, L(χ5) et DH"}
    return [dict(fichier=f"1_Presentation/articles/{k}", legende=v) for k, v in caps.items() if (A / k).exists()]


def build_html(D, C, A) -> str:
    bi = _load("build_indicateur", ROOT / "2_Methode" / "Indicateur" / "build_indicateur.py")
    card = lambda f, cap, sub: (f"<figure class='fg'><a href='{esc(f)}'><img src='{esc(f)}' alt='{esc(cap)}' loading='lazy'></a>"
                                f"<figcaption><b>{esc(cap)}</b><span class='foot'>{sub}</span></figcaption></figure>")
    d_cards = "".join(card(x["fichier"], f"Fig. {k}. {x['legende']}",
                           (f"Document {esc(x['num'])} : <a href='{esc(x['doc'])}'>{esc(x['doc_titre'])}</a>" if x["doc"] else esc(x["doc_titre"])))
                      for k, x in enumerate(D, 1))
    c_cards = "".join(card(x["fichier"], f"C{k}. {x['legende']}",
                           (f"Script : <span class='mono'>{esc(x['script'])}</span>" + (f" — {esc(x['contexte'])}" if x["contexte"] else "")) if x["script"] else "script non retrouvé")
                      for k, x in enumerate(C, 1))
    a_rows = "".join(f"<li><a href='{esc(x['fichier'])}'>{esc(x['legende'])}</a> <span class='foot'>(PDF)</span></li>" for x in A)
    css = """.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.fg{margin:0;background:var(--sheet);border:1px solid var(--rule);border-radius:8px;overflow:hidden;display:flex;flex-direction:column}
.fg img{width:100%;height:180px;object-fit:contain;background:#fff;display:block;border-bottom:1px solid var(--rule)}
.fg figcaption{padding:8px 10px;font-size:14px;line-height:1.35}.fg figcaption b{display:block;margin-bottom:3px}
.fg .foot{display:block}.mono{font-family:ui-monospace,monospace;font-size:12px;overflow-wrap:anywhere}"""
    body = f"""<div class="wrap">{bi.topnav("figures", "")}
<header class="head"><div class="eyebrow">Programme Riemann · liste des figures</div><h1>Toutes les figures du programme</h1>
<p class="lede">{len(D)} figures dans les documents, {len(C)} figures de calcul, {len(A)} figures d'articles. Cliquer une miniature ouvre l'image en grand ; le lien sous chaque figure ouvre le document qui l'explique.</p></header>
<section class="sheet" aria-labelledby="t-d"><h2 id="t-d">Figures des documents</h2><div class="grid">{d_cards}</div></section>
<section class="sheet" aria-labelledby="t-c"><h2 id="t-c">Figures de calcul</h2><p class="foot">Produites par les scripts du dossier 3_Preuves_et_calculs ; plusieurs sont les versions de travail des figures des documents.</p><div class="grid">{c_cards}</div></section>
<section class="sheet" aria-labelledby="t-a"><h2 id="t-a">Figures des articles</h2><ul>{a_rows}</ul></section>
<p class="foot">Page produite par <span class="mono">python 2_Methode/Figures/build_figures.py</span>. Auteur : Vincent NOËL.</p></div>"""
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Liste des figures</title>
<style>{bi.CSS}{css}</style></head><body>{body}</body></html>"""


def build_md(D, C, A) -> str:
    L = ["# Liste des figures", "", "Auteur et titulaire des droits : Vincent NOËL. Page produite par `python 2_Methode/Figures/build_figures.py`.", "",
         f"{len(D)} figures dans les documents, {len(C)} figures de calcul, {len(A)} figures d'articles.", "", "## Figures des documents", ""]
    for k, x in enumerate(D, 1):
        doc = f" — document {x['num']} : [{x['doc_titre']}](../{x['doc']})" if x["doc"] else ""
        L += [f"### Fig. {k}. {x['legende']}", "", f"![{x['legende']}](../{x['fichier']}){doc}".replace(")" + doc, ")\n\n" + doc.lstrip(" —")) if doc else f"![{x['legende']}](../{x['fichier']})", ""]
    L += ["## Figures de calcul", "", "| | Figure | Script |", "|---|---|---|"]
    for k, x in enumerate(C, 1):
        L.append(f"| C{k} | [{x['legende']}](../{x['fichier']}) | {('`' + x['script'] + '`') if x['script'] else '—'} |")
    L += ["", "## Figures des articles", ""] + [f"- [{x['legende']}](../{x['fichier']}) (PDF)" for x in A] + [""]
    return "\n".join(L)


def main():
    D, C, A = doc_figures(), calc_figures(), article_figures()
    (ROOT / "00_Liste_des_figures.html").write_text(build_html(D, C, A), encoding="utf-8")
    (PRES / "LISTE_DES_FIGURES.md").write_text(build_md(D, C, A), encoding="utf-8-sig")
    print(f"figures : documents {len(D)}, calcul {len(C)}, articles {len(A)} ; écrit : 00_Liste_des_figures.html, 1_Presentation/LISTE_DES_FIGURES.md")


if __name__ == "__main__":
    main()
