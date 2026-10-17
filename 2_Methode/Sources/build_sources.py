"""V6.18 — Registre des sources : sources.json → 1_Presentation/42_REGISTRE_DES_SOURCES.md.

Chaque fiche : clé, bibliographie, lien vers le résumé, statut de vérification (date, ce qui a été vérifié, extrait court),
usage par le corpus, verdict, conjectures touchées, dimensions de l'indicateur, intérêt (couleur).
Priorité de lecture = intérêt × reste à vérifier × usage. Les citations restent dans le texte des documents (« Deligne (1974) ») ;
la clé [Del74] renvoie à la fiche. Les documents qui citent une fiche sont retrouvés par ses motifs et sa clé.
"""
from __future__ import annotations
import json, re, sys, html, importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; PRES = ROOT / "1_Presentation"
COUL = {"appui": "🔴", "confronter": "🟠", "contexte": "🔵", "outil": "⚪"}
POIDS_I = {"appui": 4, "confronter": 3, "contexte": 1, "outil": 1}
RESTE = {"vérifié en ligne": 0.25, "partiellement vérifié": 0.7, "non vérifié": 1.0}
VERD = {"exact": 0.0, "imprécis": 0.5, "faux": 1.0, "non vérifiable": 0.5}
NOMS_C = {"RH": "RH", "SZ": "simplicité", "PC": "répulsion", "dBN": "de Bruijn–Newman", "D2": "degré 2", "MR": "Modèle réduit"}
KEY = re.compile(r"\[([A-Z][A-Za-z]{1,7}[0-9]{2}[a-z]?)\]")

ARTICLE_ALIASES = {'DH36':['DH36a','DH36b'], 'Bom00':['Bom00a'], 'DLMF':['NIS10'], 'Bom74':['Bom73']}

def article_citations():
    """Link the existing article bibliography keys without rewriting the articles."""
    out=[]; known={s['cle'] for s in load()}
    for p in sorted((PRES/'articles').glob('article*.tex')):
        text=p.read_text(encoding='utf-8-sig')
        cited={k.strip() for group in re.findall(r'\\cite\w*(?:\[[^\]]*\])*\{([^}]+)\}',text) for k in group.split(',')}
        bibliog=set(re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',text))
        refs=[]
        for key in sorted(cited|bibliog):
            targets=ARTICLE_ALIASES.get(key,[key])
            if not set(targets)<=known:raise ValueError(f'Article {p.name}: référence non reliée {key}')
            refs.append(dict(article_key=key,registry_keys=targets,cited=key in cited))
        out.append(dict(id='ARTICLE-'+re.search(r'article(\d+)',p.name)[1],
                        title=re.search(r'\\title\{(.*?)\}',text,re.S)[1] if re.search(r'\\title\{(.*?)\}',text,re.S) else p.stem,
                        tex='articles/'+p.name,pdf='articles/'+p.with_suffix('.pdf').name,references=refs))
    return out

def load() -> list[dict]:
    return json.loads((HERE / "sources.json").read_text(encoding="utf-8-sig"))

def docx_text(p) -> str:
    """Texte d'un document Word (paragraphes et tableaux) ; vide si python-docx manque."""
    try:
        import docx
    except ImportError:
        return ""
    d = docx.Document(str(p))
    return "\n".join([x.text for x in d.paragraphs] + [c.text for tb in d.tables for r in tb.rows for c in r.cells])

def textes() -> dict:
    """Textes des documents numérotés de 1_Presentation : Markdown, et Word quand le document n'existe qu'en .docx (02–05, 09–13)."""
    docs = {p.name: p.read_text(encoding="utf-8-sig") for p in sorted(PRES.glob("[0-9][0-9]_*.md")) if not p.name.startswith("42_")}
    for p in sorted(PRES.glob("[0-9][0-9]_*.docx")):
        if not p.with_suffix(".md").exists() and not any(n[:2] == p.name[:2] for n in docs): docs[p.name] = docx_text(p)
    return docs

def citations(S) -> dict:
    """Documents de 1_Presentation (Markdown, ou Word seul) où chaque fiche est citée, par clé ou par motif."""
    docs = textes()
    out = {}
    for s in S:
        hits = set()
        for n, t in docs.items():
            if f"[{s['cle']}]" in t or any(m and m in t for m in s.get("motifs", [])): hits.add(n[:2])
        out[s["cle"]] = sorted(hits | {d[:2] for d in s.get("docs", []) + s.get("cite_aussi", []) if d[:2].isdigit()})
        for a in article_citations():
            if any(s['cle'] in r['registry_keys'] for r in a['references']):
                out[s['cle']].append(f"[{a['id']}]({a['pdf']})")
    return out

def priorite(s, n_docs) -> float:
    return round(POIDS_I.get(s.get("interet"), 1) * (RESTE.get(s["statut"], 1) + VERD.get(s.get("verdict"), 0.5)) * (1 + min(n_docs, 5) / 5), 2)

def check(S) -> list[str]:
    errs, keys = [], set()
    for s in S:
        if not re.fullmatch(r"[A-Z][A-Za-z]{1,7}[0-9]{2}[a-z]?", s["cle"]): errs.append(f"clé mal formée {s['cle']}")
        if s["cle"] in keys: errs.append(f"clé en double {s['cle']}")
        keys.add(s["cle"])
        if s["statut"] not in RESTE: errs.append(f"{s['cle']} : statut inconnu {s['statut']}")
        if s.get("interet") not in COUL: errs.append(f"{s['cle']} : intérêt inconnu {s.get('interet')}")
        if s.get("verdict") in ("imprécis", "faux") and not s.get("correction"): errs.append(f"{s['cle']} : verdict sans correction")
    for p in PRES.glob("[0-9][0-9]_*.md"):
        for k in KEY.findall(p.read_text(encoding="utf-8-sig")):
            if k not in keys: errs.append(f"{p.name} : clé inconnue [{k}]")
    return errs

def lectures(S, n=3) -> list[dict]:
    """Les lectures prioritaires (coups « lecture » du navigateur) : appuis et résultats à confronter pas encore vérifiés en entier."""
    cit = citations(S)
    c = [s for s in S if s.get("interet") in ("appui", "confronter") and (s["statut"] != "vérifié en ligne" or s.get("verdict") != "exact")]
    return sorted(c, key=lambda s: -priorite(s, len(cit[s["cle"]])))[:n]

def fmt(s) -> str:
    """Format bibliographique uniforme : [Clé] Auteurs. *Titre*. Publication. Lien."""
    pub = (s.get("publication") or "").strip().rstrip(".")
    yr = str(s.get("annee") or "s. d.")
    if yr not in pub: pub = f"{pub} ({yr})" if pub else yr
    out = f"[{s['cle']}] {s['auteurs'].strip().rstrip('.')}. *{s['titre'].strip().rstrip('.')}*. {pub}."
    if s.get("lien"): out += f" <{s['lien']}>"
    return out

REF0, REF1 = "<!-- references:debut -->", "<!-- references:fin -->"

def doc_refs(text, S) -> str:
    """Section « Références » d'un document : toutes les fiches dont la clé figure dans le texte (hors section)."""
    body = text.split(REF0)[0]
    by = {s["cle"]: s for s in S}
    keys = sorted({k for k in KEY.findall(body) if k in by}, key=str.lower)
    if not keys: return ""
    L = [REF0, "", "## Références", "", "Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).", ""]
    for k in keys:
        s = by[k]; line = "- " + fmt(s) + f" — {s['statut']}"
        if s.get("verdict") in ("imprécis", "faux"): line += f". **Correctif V6.18 :** {s['correction']}"
        L.append(line)
    L += ["", REF1]
    return "\n".join(L)

def sync_docs(S, write=True) -> list[str]:
    """Ajoute ou met à jour la section « Références » de chaque document numéroté (sauf 20 et 42). Renvoie les documents à jour."""
    changed = []
    # V6.59 : les originaux figés (2_Methode/Pilotage/originaux_figes.json) restent à l'octet près.
    figes = {f["path"] for f in json.loads((PRES.parent / "2_Methode/Pilotage/originaux_figes.json").read_text(encoding="utf-8-sig"))["fichiers"]}
    for p in sorted(PRES.glob("[0-9][0-9]_*.md")):
        if p.name[:2] in ("20", "42") or str(p.relative_to(PRES.parent)) in figes: continue
        t = p.read_text(encoding="utf-8-sig"); base = t.split(REF0)[0].rstrip() + "\n"
        sec = doc_refs(base, S); new = base + ("\n" + sec + "\n" if sec else "")
        if new != t:
            changed.append(p.name)
            if write: p.write_text(new, encoding="utf-8-sig")
    return changed

def md_escape(t) -> str:
    return str(t or "").replace("|", "\\|").replace("\n", " ")

def build() -> str:
    S = load(); cit = citations(S)
    for s in S: s["_p"] = priorite(s, len(cit[s["cle"]])); s["_docs"] = cit[s["cle"]]
    n = len(S); st = {k: sum(1 for s in S if s["statut"] == k) for k in RESTE}
    it = {k: sum(1 for s in S if s.get("interet") == k) for k in COUL}
    vd = {k: sum(1 for s in S if s.get("verdict") == k) for k in VERD}
    L = [f"# Registre des sources\n",
         "**État éditorial :** 14 octobre 2026 (V6.55). Les dates de vérification propres aux fiches sont conservées.  ",
         "**Statut :** registre généré par `2_Methode/Sources/build_sources.py` à partir de `2_Methode/Sources/sources.json`. Ne pas modifier ce fichier à la main.  ",
         "**Demande de l'auteur :** savoir où sont les sources et où elles sont citées ; garder la référence dans le texte ; situer chaque article dans les grilles de lecture, par couleur d'intérêt, avec un lien vers le résumé et des priorités.\n",
         "## 1. Comment lire ce registre\n",
         "- **Dans les documents**, la citation reste écrite en clair (« Deligne (1974) »). Une clé entre crochets, par exemple [Del74], renvoie à la fiche de ce registre. Les documents antérieurs gardent leurs citations d'origine ; la colonne « Cité dans » les retrouve par le nom des auteurs. Les documents qui n'existent qu'en Word (02 à 05, 09 à 13, dont les audits des réponses d'OpenAI) sont lus aussi.",
         "- **Couleur d'intérêt** : 🔴 appui (un énoncé démontré du corpus repose dessus) ; 🟠 à confronter (résultat proche qui pourrait contenir ou contredire un énoncé du corpus) ; 🔵 contexte ; ⚪ outil (méthode).",
         "- **Statut** : vérifié en ligne (bibliographie et énoncé contrôlés, date indiquée), partiellement vérifié (bibliographie, ou énoncé par une source secondaire), non vérifié (cité de mémoire).",
         "- **Verdict** sur l'usage qu'en fait le corpus : exact, imprécis ou faux (avec la correction), non vérifiable.",
         "- **Conjectures** : RH, simplicité (SZ), répulsion (PC), de Bruijn–Newman (dBN), degré 2 (D2), Modèle réduit (MR). Ce sont les lignes et colonnes de la carte des croisements (document 31), où chaque fiche apparaît en pastille de sa couleur.",
         "- **Priorité de lecture** = intérêt × (reste à vérifier + doute sur le verdict) × usage dans le corpus. Les trois premières deviennent des coups « lecture » du navigateur (document 34).",
         "- Les anciennes bibliographies sont conservées et intégrées ici : `4_Archives/REFERENCES.md`, `3_Preuves_et_calculs/preuves/BIBLIO_POSITIONNEMENT.md`, `4_Archives/docs_techniques/SOURCES_RH_PROGRAMME.md`, et les notes de `1_Presentation/relecture/`.\n",
         "## 2. Bilan\n",
         f"| Fiches | Vérifiées en ligne | Partiellement | Non vérifiées | 🔴 appui | 🟠 à confronter | 🔵 contexte | ⚪ outil |",
         "|---|---|---|---|---|---|---|---|",
         f"| {n} | {st['vérifié en ligne']} | {st['partiellement vérifié']} | {st['non vérifié']} | {it['appui']} | {it['confronter']} | {it['contexte']} | {it['outil']} |\n",
         f"Verdicts : {vd['exact']} exacts, {vd['imprécis']} imprécis, {vd['faux']} faux, {vd['non vérifiable']} non vérifiables. Les vérifications de cette version ont été faites le 10 octobre 2026 ; celles des bibliographies antérieures gardent leur date.\n",
         "## 3. Les citations à corriger\n",
         "| Clé | Usage par le corpus | Correction |", "|---|---|---|"]
    for s in sorted(S, key=lambda s: s["cle"].lower()):
        if s.get("verdict") in ("imprécis", "faux"):
            L.append(f"| [{s['cle']}] | {md_escape(s.get('usage_corpus'))} | {md_escape(s.get('correction'))} |")
    L += ["", "## 4. Lectures prioritaires\n", "| Priorité | Clé | Intérêt | Statut | Référence | Pourquoi la lire |", "|---|---|---|---|---|---|"]
    for s in sorted([s for s in S if s.get("interet") in ("appui", "confronter")], key=lambda s: -s["_p"])[:12]:
        L.append(f"| {s['_p']:.2f} | [{s['cle']}] | {COUL[s['interet']]} | {s['statut']} | {md_escape(s['auteurs'])}, *{md_escape(s['titre'])}* ({s.get('annee') or 's. d.'}) | {md_escape(s.get('correction') or s.get('usage_corpus'))} |")
    L += ["", "## 5. Les fiches\n", "| Clé | | Référence | Lien | Statut | Verdict | Conjectures | Cité dans |", "|---|---|---|---|---|---|---|---|"]
    for s in sorted(S, key=lambda s: s["cle"].lower()):
        lien = f"[résumé]({s['lien']})" if s.get("lien") else "—"
        conj = ", ".join(NOMS_C.get(c, c) for c in s.get("conjectures", [])) or "—"
        L.append(f"| **[{s['cle']}]** | {COUL.get(s.get('interet'), '')} | {md_escape(s['auteurs'])}, *{md_escape(s['titre'])}*, {md_escape(s.get('publication'))} | {lien} | {s['statut']} ({s.get('verifie_le') or '—'}) | {s.get('verdict')} | {conj} | {', '.join(s['_docs']) or '—'} |")
    L += ["", "## 6. Bibliographie (format uniforme)\n"]
    for s in sorted(S, key=lambda s: s["cle"].lower()): L.append("- " + fmt(s))
    L += ["", "## 7. Ce qui a été vérifié, fiche par fiche\n"]
    for s in sorted(S, key=lambda s: s["cle"].lower()):
        L.append(f"- **[{s['cle']}]** {COUL.get(s.get('interet'), '')} {md_escape(s.get('ce_qui_a_ete_verifie'))}" + (f" Extrait : « {md_escape(s['extrait'])} »" if s.get("extrait") else "") + f" Usage : {md_escape(s.get('usage_corpus'))}")
    L += ["", "## 8. Références des articles LaTeX et PDF", "",
          "Les articles sont conservés. Les correspondances ci-dessous relient leurs clés bibliographiques aux fiches globales ; elles ne valent pas nouvelle vérification des énoncés cités.", "",
          "Alias : DH36 renvoie aux deux parties DH36a/DH36b ; Bom00 à Bom00a ; DLMF à NIS10 ; Bom74 à Bom73 (exposé de 1973 publié dans le volume de 1974).", "",
          "| Article | Versions | Clé de l’article → fiche globale |", "|---|---|---|"]
    for a in article_citations():
        L.append(f"| {a['id']} | [PDF]({a['pdf']}) · [LaTeX]({a['tex']}) | "+'; '.join(r['article_key']+' → '+', '.join(r['registry_keys']) for r in a['references'])+' |')
    return "\n".join(L) + "\n"


def write_article_links():
    obj={'version':'V6.55','scope':'Raccordement bibliographique, sans modification des articles ni nouvelle vérification des références.',
         'aliases':ARTICLE_ALIASES,'articles':article_citations()}
    (HERE/'references_articles.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def build_html():
    spec=importlib.util.spec_from_file_location('ind_style',ROOT/'2_Methode/Indicateur/build_indicateur.py')
    bi=importlib.util.module_from_spec(spec);spec.loader.exec_module(bi)
    esc=lambda x:html.escape(str(x),quote=True)
    S=load();cit=citations(S)
    rows=[]
    for s in sorted(S,key=lambda x:x['cle'].lower()):
        articles=[a for a in article_citations() if any(s['cle'] in r['registry_keys'] for r in a['references'])]
        links=', '.join(f'<a href="{esc(a["pdf"])}">{a["id"]}</a> (<a href="{esc(a["tex"])}">LaTeX</a>)' for a in articles)
        doc_links=[]
        for number in [x for x in cit[s['cle']] if not x.startswith('[')]:
            files=sorted(p for p in PRES.glob(number+'_*') if p.suffix in {'.pdf','.html','.md','.docx'} and not p.stem.endswith('_nav') and '_COMPLEMENT_' not in p.name)
            preferred=next((p for ext in ['.pdf','.html','.md','.docx'] for p in files if p.suffix==ext),None)
            if preferred:doc_links.append(f'<a href="{esc(preferred.name)}">Document {esc(number)}</a>')
        docs=', '.join(doc_links)
        if s['cle']=='SuzSig23':docs='<a href="79_SIGNAL_COUPLAGES_ET_RESOLUTION.html">Complément79 : signal et résolution</a> · <a href="79_SIGNAL_COUPLAGES_ET_RESOLUTION.pdf">PDF</a>'
        if s['cle']=='SuzH23':docs='<a href="76_COMPLEMENT_COUP_DOUBLE.html">Complément 76</a> · <a href="76_COMPLEMENT_COUP_DOUBLE.pdf">PDF</a> · <a href="76_COMPLEMENT_COUP_DOUBLE.tex">LaTeX</a>'
        rows.append(f'<tr id="ref-{esc(s["cle"])}"><th>{esc(s["cle"])}</th><td>{esc(s["auteurs"])}. <i>{esc(s["titre"])}</i>. {esc(s.get("publication",""))}<br><a href="{esc(s.get("lien", ""))}">Source</a></td><td>{esc(s["statut"])} · {esc(s.get("verifie_le", ""))}<br>{esc(s.get("verdict",""))}</td><td>{docs}<br>{links}</td></tr>')
    body=bi.topnav('sources','../')+'<header class="head"><div class="eyebrow">Document 42 · références globales</div><h1>Registre des sources</h1><p class="lede">'+str(len(S))+' fiches conservées ; renvois aux trois articles LaTeX et PDF. Les dates de vérification restent celles des fiches.</p></header><section class="sheet"><p><a href="42_REGISTRE_DES_SOURCES.pdf">PDF existant du registre</a> · <a href="42_REGISTRE_DES_SOURCES.md">Registre complet, usages et correctifs</a> · <a href="../00_PORTAIL.html?type=references#documents">Catalogue filtré sur les références</a></p><label style="display:grid;gap:8px">Rechercher une clé, un auteur, un titre ou un document<input id="reference-search" type="search" placeholder="Weil, Wei52, Document 16…" style="width:100%;max-width:100%"></label><p>Alias des articles : DH36 → DH36a et DH36b ; Bom00 → Bom00a ; DLMF → NIS10 ; Bom74 → Bom73.</p><div style="overflow:auto"><table><thead><tr><th>Clé</th><th>Référence</th><th>Vérification</th><th>Documents et articles</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div></section><script>document.getElementById("reference-search").addEventListener("input",e=>{const q=e.target.value.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase();document.querySelectorAll("tr[id^=ref-]").forEach(r=>r.hidden=!r.textContent.normalize("NFD").replace(/[\\u0300-\\u036f]/g,"").toLowerCase().includes(q))})</script>'
    return '<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>42 · Registre des sources</title><style>'+bi.CSS+'</style><body><main class="wrap">'+body+'</main></body></html>'

if __name__ == "__main__":
    errs = check(load())
    if errs: raise SystemExit("\n".join(errs))
    if "--registry-only" not in sys.argv:
        print("documents mis à jour :", ", ".join(sync_docs(load())) or "aucun")
    (PRES / "42_REGISTRE_DES_SOURCES.md").write_text(build(), encoding="utf-8-sig")
    write_article_links()
    (PRES / "42_REGISTRE_DES_SOURCES.html").write_text(build_html(),encoding='utf-8')
    print("écrit :", PRES / "42_REGISTRE_DES_SOURCES.md")
