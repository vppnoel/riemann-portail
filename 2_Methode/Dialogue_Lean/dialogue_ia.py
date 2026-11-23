#!/usr/bin/env python3
"""
Programme Riemann — Auteur et titulaire des droits : Vincent NOËL.

Dialogue autonome Claude <-> ChatGPT : rendre lisible la preuve Lean
(leanprover-community/riemann-hypothesis, commit figé dans programme.json).

Unités de travail : programme.json (sur main, modifié par l'auteur seul).
  - « etalonnage » : mêmes fichiers que TAC-017 / TAC-023, SANS donner ces textes aux IA ;
    une comparaison a posteriori mesure ce que le duo rattrape, laisse passer, ajoute.
  - « nouveau » : racine + imports internes sous des préfixes donnés.

Cycle d'une unité :
  draft -> liens -> [sonde] -> review -> (revise -> liens -> review)* -> questions
        -> [comparaison, unités d'étalonnage] -> unité suivante.
  liens : relais/verifier_liens_lean.py (commit, fichier, ligne). Un écart = REVISER
          automatique, sans passer par le critique.
  review : critique en aveugle, avec la liste des huit erreurs connues (CHARTE.md).
  L'auteur ne note jamais sa propre explication.

Lecture du dépôt Lean par `git show` / `git ls-tree` : marche sur un clone partiel
(--filter=blob:none), sans extraire ~150 000 fichiers.

Sorties : 2_Methode/Dialogue_Lean/travail/ sur la branche ia-dialogue uniquement.
Stdlib seulement.
"""
import datetime
import json
import os
import pathlib
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request


def env(name, default=""):
    v = os.environ.get(name, "")
    return v if v.strip() else default


HERE = pathlib.Path(__file__).resolve().parent
OUT = pathlib.Path(env("OUT_DIR", "2_Methode/Dialogue_Lean/travail"))
LEAN_DIR = pathlib.Path(env("LEAN_DIR", "lean-src"))          # clone (partiel) du dépôt Lean
CHARTER_PATH = pathlib.Path(env("CHARTER_PATH", str(HERE / "CHARTE.md")))
PROGRAMME_PATH = pathlib.Path(env("PROGRAMME_PATH", str(HERE / "programme.json")))
VERIF_SCRIPT = pathlib.Path(env("VERIF_SCRIPT", str(HERE / "relais" / "verifier_liens_lean.py")))
REF_ROOT = pathlib.Path(env("REF_ROOT", "."))                  # copie de main pour les références
STOP_PATHS = [OUT / "STOP"] + ([pathlib.Path(env("EXTRA_STOP"))] if env("EXTRA_STOP") else [])

TURNS_PER_RUN = int(env("TURNS_PER_RUN", "4"))
MAX_TURNS_TOTAL = int(env("MAX_TURNS_TOTAL", "200"))
MAX_REVISIONS = int(env("MAX_REVISIONS", "2"))
MAX_OUT = int(env("MAX_OUTPUT_TOKENS", "16000"))
UNIT_CAP = int(env("UNIT_CHARS", "240000"))     # source montrée par unité
FILE_CAP = int(env("FILE_CHARS", "40000"))      # au-delà : index des déclarations + fin du fichier
DRY_RUN = env("DRY_RUN", "0") == "1"
LEAN_ROOT = env("LEAN_ROOT", "Main")    # racine par défaut des unités « descente »

SEED = int(env("EXPERIMENT_SEED", "20261123"))
P_INJECT = float(env("INJECTION_RATE", "0.5"))
P_SELF = float(env("SELF_REVIEW_RATE", "0.3"))
N_QUESTIONS = int(env("N_QUESTIONS", "4"))

AGENTS = {
    "Claude": {"kind": "anthropic", "model": env("ANTHROPIC_MODEL", "claude-opus-5-5")},
    "ChatGPT": {"kind": "openai", "model": env("OPENAI_MODEL", "")},
}

STATE = OUT / "state.json"
JOURNAL = OUT / "JOURNAL.md"
INDEX = OUT / "INDEX.md"
EXPL = OUT / "modules"
EXP = OUT / "experience"
SEALED = EXP / "scelle"
METRICS = EXP / "mesures.jsonl"
BOM = "﻿"
RIGHTS = "Auteur et titulaire des droits : Vincent NOËL."


def write_md(path, text):
    # Règle du dépôt (test_v632_encodage) : tout .md commence par la marque UTF-8.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.startswith(BOM) else BOM + text, encoding="utf-8")


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


# --------------------------------------------------------------------------- API
def http_post(url, headers, body, tries=4):
    data = json.dumps(body).encode()
    for i in range(tries):
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 529) and i < tries - 1:
                time.sleep(30 * (i + 1))
                continue
            raise RuntimeError(f"HTTP {e.code} sur {url} : {msg}")
        except urllib.error.URLError:
            if i < tries - 1:
                time.sleep(30 * (i + 1))
                continue
            raise


def call(agent, system, user):
    a = AGENTS[agent]
    if DRY_RUN:
        return fake_answer(user)
    if a["kind"] == "anthropic":
        r = http_post(
            "https://api.anthropic.com/v1/messages",
            {"x-api-key": os.environ["ANTHROPIC_API_KEY"],
             "anthropic-version": "2023-06-01", "content-type": "application/json"},
            {"model": a["model"], "max_tokens": MAX_OUT, "system": system,
             "messages": [{"role": "user", "content": user}]},
        )
        return "".join(b.get("text", "") for b in r.get("content", []))
    if not a["model"]:
        sys.exit("Variable OPENAI_MODEL non définie (Settings > Secrets and variables > Variables).")
    r = http_post(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
         "content-type": "application/json"},
        {"model": a["model"], "max_completion_tokens": MAX_OUT,
         "messages": [{"role": "system", "content": system},
                      {"role": "user", "content": user}]},
    )
    return r["choices"][0]["message"]["content"] or ""


FAKE_LINK = env("FAKE_LINK", "")


def fake_answer(user):
    if "===ERREUR===" in user:
        return "===VERSION===\n# faux\nTexte altéré.\n===ERREUR===\nInégalité inversée.\n===FIN==="
    if "===DETECTEE===" in user:
        return "===DETECTEE===\nOUI\n===JUSTIFICATION===\nPoint 1.\n===FIN==="
    if "===QUESTIONS===" in user:
        return "===QUESTIONS===\n1. Q ?\n===REPONSES===\n1. R.\n===FIN==="
    if "===BILAN===" in user:
        return "===BILAN===\n| a | b |\n===FIN==="
    if "===VERDICT===" in user:
        v = "OK" if "Révision" in user or "révision" in user else "REVISER"
        return f"===VERDICT===\n{v}\n===REMARQUES===\n1. Remarque factice.\n===FIN==="
    return f"===EXPLICATION===\n# Unité (test)\n\nTexte factice.\n\n## Correspondance\n- {FAKE_LINK}\n===FIN==="


# --------------------------------------------------------------------------- Lean
def git(*args, check=True):
    r = subprocess.run(["git", "-C", str(LEAN_DIR), *args], capture_output=True, text=True, timeout=600)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} : {r.stderr.strip()[:300]}")
    return r.stdout


_cache = {}


def lean_file(commit, path):
    if path not in _cache:
        _cache[path] = git("show", f"{commit}:{path}")
    return _cache[path]


IMPORT_RE = re.compile(r"^\s*(?:public\s+|meta\s+)*import\s+(.+)$")
DECL_RE = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe|public)\s+)*"
    r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|axiom|opaque)\s")


_srcdir = None


def src_dir(commit):
    """srcDir du lakefile (ici « src ») : les noms de modules sont relatifs à ce dossier,
    donc Development.X correspond à src/Development/X.lean."""
    global _srcdir
    if _srcdir is None:
        _srcdir = ""
        for lf in ("lakefile.toml", "lakefile.lean"):
            txt = git("show", f"{commit}:{lf}", check=False)
            m = re.search(r'srcDir\s*:?=\s*"([^"]*)"', txt)
            if m:
                _srcdir = m.group(1).strip("/")
                break
    return _srcdir


def module_to_path(mod, paths, commit):
    d = src_dir(commit)
    cand = (d + "/" if d else "") + mod.replace(".", "/") + ".lean"
    return cand if cand in paths else None


def path_to_module(path, commit):
    d = src_dir(commit)
    rel = path[len(d) + 1:] if d and path.startswith(d + "/") else path
    return rel[:-5].replace("/", ".")


def lean_modules(commit, paths, root=None, depth=2, prefixes=(), max_files=10**9):
    """Descente en largeur depuis un module racine (par défaut LEAN_ROOT = Main), par les
    imports internes au dépôt (Mathlib exclu), jusqu'à `depth` niveaux. Renvoie la liste
    des chemins et le niveau de chacun."""
    root = root or LEAN_ROOT
    start = root if root.endswith(".lean") else module_to_path(root, paths, commit)
    if not start:
        sys.exit(f"Module racine « {root} » introuvable sous {src_dir(commit) or '.'}/")
    level, queue = {start: 0}, [start]
    while queue and len(level) < max_files:
        p = queue.pop(0)
        if level[p] >= depth:
            continue
        for line in lean_file(commit, p).splitlines():
            m = IMPORT_RE.match(line)
            if not m:
                continue
            for mod in m.group(1).split():
                q = module_to_path(mod, paths, commit)
                if q and q not in level and (not prefixes or any(q.startswith(x) for x in prefixes)):
                    level[q] = level[p] + 1
                    queue.append(q)
    return list(level), level


def unit_files(unit, commit, all_paths):
    if "fichiers" in unit:
        missing = [p for p in unit["fichiers"] if p not in all_paths]
        if missing:
            sys.exit(f"{unit['id']} : fichiers absents au commit {commit} : {missing[:3]}")
        return list(unit["fichiers"])
    files, _ = lean_modules(commit, all_paths, unit.get("racine"), unit.get("profondeur", 2),
                            unit.get("prefixes", ()), unit.get("max_fichiers", 25))
    return files


def file_view(commit, path):
    """Source avec numéros de ligne d'origine ; imports résumés ; gros fichiers réduits."""
    lines = lean_file(commit, path).splitlines()
    n_imp = sum(1 for l in lines if IMPORT_RE.match(l))
    body = [(i + 1, l) for i, l in enumerate(lines) if not IMPORT_RE.match(l)]
    text = "\n".join(f"{n:>5}| {l}" for n, l in body)
    note = f"({len(lines)} lignes, dont {n_imp} imports non reproduits)"
    if len(text) > FILE_CAP:
        heads = [f"{n:>5}| {l}" for n, l in body if DECL_RE.match(l)]
        tail = [f"{n:>5}| {l}" for n, l in body[-150:]]
        text = ("-- [FICHIER TROP LONG : index des déclarations, puis les 150 dernières lignes]\n"
                + "\n".join(heads) + "\n  ...\n" + "\n".join(tail))
    return f"### FICHIER {path} {note}\n{text}\n"


def unit_view(commit, files):
    parts, size = [], 0
    for p in files:
        v = file_view(commit, p)
        if size + len(v) > UNIT_CAP:
            parts.append(f"-- [PLAFOND ATTEINT : {len(files) - len(parts)} fichier(s) non montrés]\n")
            break
        parts.append(v)
        size += len(v)
    return "\n".join(parts)


def check_links(chapter_path, commit):
    if not VERIF_SCRIPT.exists():
        return 0, 0, "(script de contrôle des liens absent)"
    r = subprocess.run([sys.executable, "-I", str(VERIF_SCRIPT), str(chapter_path), str(LEAN_DIR), commit],
                       capture_output=True, text=True, timeout=1800)
    out = (r.stdout + r.stderr).strip()
    m = re.search(r"(\d+) liens, (\d+) fichiers, (\d+) écart", out)
    n_links, n_gaps = (int(m.group(1)), int(m.group(3))) if m else (0, 1)
    return n_links, n_gaps, out


# --------------------------------------------------------------------------- état
def load_state():
    if STATE.exists():
        return json.loads(read(STATE))
    return {"turns": 0, "unit_idx": 0, "phase": "draft", "revisions": 0,
            "author": "Claude", "done": []}


def save_state(s):
    STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False), encoding="utf-8")


def other(a):
    return "ChatGPT" if a == "Claude" else "Claude"


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def journal(entry):
    if not JOURNAL.exists():
        write_md(JOURNAL, f"# Journal du dialogue\n\n*{RIGHTS}*\n\n")
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(entry.rstrip() + "\n\n")


def measure(**kw):
    kw["t"] = now()
    METRICS.parent.mkdir(parents=True, exist_ok=True)
    with METRICS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(kw, ensure_ascii=False) + "\n")


def between(txt, start, end="===FIN==="):
    m = re.search(re.escape(start) + r"\s*(.*?)\s*(?:" + re.escape(end) + r"|\Z)", txt, re.S)
    return m.group(1).strip() if m else ""


def assign(idx, unit):
    r = random.Random(SEED * 1000 + idx)
    cond = "auto" if r.random() < P_SELF else "croisee"
    sonde = r.random() < P_INJECT
    if unit["phase"] == "etalonnage":   # l'étalonnage se fait toujours en relecture croisée
        cond = "croisee"
    return {"condition": cond, "sonde": sonde}


def chapter_path(idx, unit):
    return EXPL / f"{idx+1:02d}-{unit['id']}.md"


def summary():
    if not METRICS.exists():
        return ""
    rows = [json.loads(l) for l in METRICS.read_text(encoding="utf-8").splitlines() if l.strip()]
    out = ["\n## Mesures (provisoires)\n",
           "| Condition | Sondes | Erreurs détectées | Taux | 1re relecture « OK » | Écarts de liens (1er jet) |",
           "|---|---|---|---|---|---|"]
    for c in ("croisee", "auto"):
        pr = [r for r in rows if r["evt"] == "sonde" and r["condition"] == c]
        hit = sum(1 for r in pr if r["detectee"])
        rv = [r for r in rows if r["evt"] == "relecture" and r["condition"] == c and r["revision"] == 0]
        ok = sum(1 for r in rv if r["verdict"] == "OK")
        lk = [r for r in rows if r["evt"] == "liens" and r["condition"] == c and r["revision"] == 0]
        gaps = sum(1 for r in lk if r["ecarts"])
        taux = f"{hit/len(pr):.0%}" if pr else "–"
        out.append(f"| {c} | {len(pr)} | {hit} | {taux} | {ok}/{len(rv)} | {gaps}/{len(lk)} |")
    return "\n".join(out) + "\n"


def write_index(units, s, prog):
    lines = ["# Preuve Lean rendue lisible — index\n",
             f"*{RIGHTS} Produit par Claude et ChatGPT, non accepté par l'auteur.*\n",
             f"Source : {prog['lean_repo']} @ `{prog['lean_commit']}`\n",
             "| # | Unité | Phase | Statut |", "|---|---|---|---|"]
    for i, u in enumerate(units):
        f = chapter_path(i, u)
        if u["id"] in s["done"]:
            st = "relue par les deux IA" if assign(i, u)["condition"] == "croisee" else "auto-relue (contrôle)"
        elif i == s["unit_idx"]:
            st = f"en cours ({s['phase']})"
        else:
            st = "à faire"
        link = f"[{u['titre']}](modules/{f.name})" if f.exists() else u["titre"]
        lines.append(f"| {i+1} | {link} | {u['phase']} | {st} |")
    write_md(INDEX, "\n".join(lines) + "\n" + summary())


# --------------------------------------------------------------------------- tours
def fmt_author(commit, repo):
    base = repo.rstrip("/") + f"/blob/{commit}/"
    return f"""Réponds UNIQUEMENT dans ce format :
===EXPLICATION===
(markdown complet du chapitre ; LaTeX entre $...$ autorisé.
Chaque déclaration Lean citée porte un lien exact, étiquette = son nom entre accents graves :
[`nom_de_la_declaration`]({base}CHEMIN/DU/FICHIER.lean#Lnn)
où nn est le numéro de la ligne où la déclaration est introduite, lu dans la marge du source.
Termine par « ## Correspondance » : une ligne par déclaration expliquée, avec son lien.
N'évalue pas ta propre explication : pas de note, pas de « fidèle », pas de « vérifié ».)
===FIN==="""


FMT_CRITIC = """Réponds UNIQUEMENT dans ce format :
===VERDICT===
OK ou REVISER
===REMARQUES===
## Liste de contrôle
(les huit points de la charte, numérotés 1 à 8, chacun : « non applicable », « vérifié : <ce que
tu as confronté> » ou « PROBLÈME : <où, quelle déclaration, pourquoi> »)
## Autres remarques
(liste numérotée : erreurs de fidélité, omissions importantes, passages obscurs)
===FIN==="""

FMT_INJECT = """Réponds UNIQUEMENT dans ce format :
===VERSION===
(le chapitre complet, identique sauf UNE erreur mathématique subtile mais réelle, de l'un des
huit types de la charte : hypothèse omise, quantificateur ou paramètre généralisé, cas limite,
inclusion géométrique relâchée… Aucune trace visible de la modification ; liens inchangés.)
===ERREUR===
(description précise de l'erreur introduite, de son type (1 à 8) et de l'endroit)
===FIN==="""


def critic_prompt(base, text, alert=""):
    return (f"Tu es le CRITIQUE. Tu relis le chapitre d'un auteur anonyme.\n{base}\n"
            f"=== EXPLICATION À VÉRIFIER ===\n{text}\n=== FIN ===\n{alert}\n"
            "Confronte les ÉNONCÉS, pas seulement les noms : hypothèses, quantificateurs, "
            "paramètres, cas limites, conventions de Mathlib, ce qui est admis. Suis les appels "
            "jusqu'au contenu. Rends OK seulement si un humain peut s'y fier.\n" + FMT_CRITIC)


def turn(s, units, prog, charter):
    commit, repo = prog["lean_commit"], prog["lean_repo"]
    idx = s["unit_idx"]
    unit = units[idx]
    cond = assign(idx, unit)
    files = s.setdefault("files", {}).get(unit["id"])
    if files is None:
        files = unit_files(unit, commit, s["_paths"])
        s["files"][unit["id"]] = files
    src = unit_view(commit, files)
    out_file = chapter_path(idx, unit)
    author = s["author"]
    critic = author if cond["condition"] == "auto" else other(author)
    t = now()
    system = charter
    base = (f"Unité : {unit['titre']} ({unit['id']}, {len(files)} fichier(s))\n"
            f"Dépôt : {repo} @ {commit}\n"
            f"=== SOURCE LEAN (numéros de ligne d'origine dans la marge) ===\n{src}\n=== FIN SOURCE ===\n")
    ph = s["phase"]

    if ph in ("draft", "revise"):
        prev = ""
        if ph == "revise":
            prev = (f"\nRévision n°{s['revisions']}. Ta version précédente :\n{read(out_file)}\n"
                    f"\nCritique ou contrôle reçu :\n{s.get('last_review','')}\n"
                    "Corrige chaque point recevable ; si tu en contestes un, dis pourquoi "
                    "dans une section « ## Réponse à la critique ».\n")
        user = (f"Tu es l'AUTEUR.\n{base}{prev}\n"
                "Écris le chapitre qui rend cette unité compréhensible à un humain "
                "mathématicien non spécialiste de Lean.\n" + fmt_author(commit, repo))
        ans = call(author, system, user)
        expl = between(ans, "===EXPLICATION===") or ans.strip()
        write_md(out_file, f"<!-- {RIGHTS} | auteur: {author} ({AGENTS[author]['model']}) | "
                           f"unité: {unit['id']} | lean: {commit} | {t} -->\n" + expl + "\n")
        measure(evt="redaction", unite=unit["id"], phase_unite=unit["phase"], auteur=author,
                revision=s["revisions"], condition=cond["condition"], longueur=len(expl))
        journal(f"## Tour {s['turns']+1} — {author} écrit `{unit['id']}` ({ph}) — {t}")
        s["phase"] = "liens"

    elif ph == "liens":
        n, gaps, report = check_links(out_file, commit)
        measure(evt="liens", unite=unit["id"], condition=cond["condition"],
                revision=s["revisions"], liens=n, ecarts=gaps)
        journal(f"## Contrôle des liens `{unit['id']}` — {t}\n{n} lien(s), {gaps} écart(s)\n\n"
                + "\n".join("    " + l for l in report.splitlines()[-40:]))
        if (gaps or n == 0) and s["revisions"] < MAX_REVISIONS:
            s["revisions"] += 1
            s["last_review"] = ("Contrôle mécanique des liens (REVISER automatique) :\n" + report
                                + ("\nAucun lien Lean trouvé : chaque déclaration citée doit en avoir un."
                                   if n == 0 else ""))
            s["phase"] = "revise"
        else:
            s["link_alert"] = report if gaps or n == 0 else ""
            s["phase"] = "sonde" if (s["revisions"] == 0 and cond["sonde"]) else "review"
        s["turns"] += 1
        return  # pas d'appel d'IA : ne consomme pas de tour payant au-delà du compteur

    elif ph == "sonde":
        injector = other(critic)
        clean = read(out_file)
        inj = call(injector, system, f"{base}\n=== CHAPITRE ===\n{clean}\n=== FIN ===\n"
                   "Exercice de contrôle qualité d'un protocole expérimental.\n" + FMT_INJECT)
        bad = between(inj, "===VERSION===", "===ERREUR===")
        err = between(inj, "===ERREUR===")
        rev = call(critic, system, critic_prompt(base, bad))
        rem = between(rev, "===REMARQUES===") or rev.strip()
        judge = other(critic)
        jd = call(judge, "Tu es juge dans une expérience de détection d'erreurs.",
                  f"Erreur introduite :\n{err}\n\nRemarques du relecteur :\n{rem}\n\n"
                  "Le relecteur a-t-il identifié CETTE erreur (même formulée autrement) ?\n"
                  "Réponds : ===DETECTEE===\nOUI ou NON\n===JUSTIFICATION===\n(1-2 phrases)\n===FIN===")
        hit = between(jd, "===DETECTEE===", "===JUSTIFICATION===").upper().startswith("OUI")
        SEALED.mkdir(parents=True, exist_ok=True)
        (SEALED / f"sonde-{idx+1:02d}-{unit['id']}.json").write_text(json.dumps(
            {"unite": unit["id"], "injecteur": injector, "critique": critic, "juge": judge,
             "erreur": err, "remarques": rem, "detectee": hit,
             "justification": between(jd, "===JUSTIFICATION===")},
            indent=2, ensure_ascii=False), encoding="utf-8")
        measure(evt="sonde", unite=unit["id"], condition=cond["condition"], critique=critic,
                injecteur=injector, juge=judge, detectee=hit)
        journal(f"## Tour {s['turns']+1} — sonde expérimentale sur `{unit['id']}` — {t}\n"
                "(résultat scellé dans experience/scelle/)")
        s["phase"] = "review"

    elif ph == "review":
        la = s.get("link_alert") or ""
        alert = f"\nALERTE : écarts de liens non résolus après {MAX_REVISIONS} révisions :\n{la}\n" if la else ""
        ans = call(critic, system, critic_prompt(base, read(out_file), alert))
        verdict = between(ans, "===VERDICT===", "===REMARQUES===").upper()
        review = between(ans, "===REMARQUES===") or ans.strip()
        ok = verdict.startswith("OK") and not la
        problems = len(re.findall(r"PROBL[ÈE]ME", review, re.I))
        measure(evt="relecture", unite=unit["id"], condition=cond["condition"], critique=critic,
                revision=s["revisions"], verdict="OK" if ok else "REVISER",
                problemes_liste=problems,
                nb_remarques=len(re.findall(r"^\s*\d+[.)]", review, re.M)))
        journal(f"## Tour {s['turns']+1} — {critic} relit `{unit['id']}` "
                f"(condition {cond['condition']}) — {t}\nVerdict : {'OK' if ok else 'REVISER'}\n\n{review}")
        s["last_review"] = review
        if ok or s["revisions"] >= MAX_REVISIONS:
            if not ok:
                with out_file.open("a", encoding="utf-8") as f:
                    f.write(f"\n\n> ⚠️ Désaccord non résolu après {MAX_REVISIONS} révisions. "
                            "Dernière critique :\n\n" +
                            "\n".join("> " + l for l in review.splitlines()) + "\n")
            s["phase"] = "questions"
        else:
            s["revisions"] += 1
            s["phase"] = "revise"

    elif ph == "questions":
        qa = other(author)
        ans = call(qa, system, f"{base}\nRédige {N_QUESTIONS} questions de compréhension sur "
                   "cette unité (ce qu'elle affirme, sous quelles hypothèses, pourquoi c'est utile "
                   "à la suite), avec des réponses vérifiables d'après le source Lean. "
                   "Une question doit pouvoir être notée juste/faux par un tiers.\n"
                   "Réponds : ===QUESTIONS===\n(liste numérotée)\n===REPONSES===\n"
                   "(liste numérotée, mêmes numéros)\n===FIN===")
        write_md(EXP / "questions" / f"{idx+1:02d}-{unit['id']}.md",
                 f"# Questions — {unit['titre']}\n\n*{RIGHTS}*\n\n"
                 + between(ans, "===QUESTIONS===", "===REPONSES===") + "\n")
        write_md(SEALED / f"reponses-{idx+1:02d}-{unit['id']}.md",
                 f"# Réponses — {unit['titre']}\n\n" + between(ans, "===REPONSES===") + "\n")
        measure(evt="questions", unite=unit["id"], redacteur=qa)
        s["phase"] = "comparaison" if unit.get("reference") else "fin"

    elif ph == "comparaison":
        # Étalonnage : le chapitre est figé ; on le compare au dépôt de référence.
        # Deux juges indépendants (les deux modèles) : l'accord entre eux est mesuré aussi.
        ref = read(REF_ROOT / unit["reference"])
        for judge in ("Claude", "ChatGPT"):
            ans = call(judge, "Tu es évaluateur dans une expérience d'étalonnage.",
                       f"Unité : {unit['titre']}\n"
                       f"Texte de référence ({unit['fiche']}, {unit['statut_reference']}) :\n{ref}\n\n"
                       f"=== Texte produit par le dialogue autonome ===\n{read(out_file)}\n=== FIN ===\n\n"
                       f"Huit erreurs connues (charte) :\n{EIGHT}\n\n"
                       "Compare, affirmation mathématique par affirmation mathématique. Donne :\n"
                       "A) ce que le dialogue énonce correctement et que la référence énonce aussi ;\n"
                       "B) ce que la référence établit et que le dialogue omet ou fausse ;\n"
                       "C) ce que le dialogue AJOUTE de faux ou d'invérifiable ;\n"
                       "D) pour chacune des huit erreurs connues : le dialogue la commet-il ? (oui/non/sans objet) ;\n"
                       "E) un tableau final : nombres d'items A, B, C ; nombre d'erreurs connues commises.\n"
                       "Ne juge pas le style. Si la référence elle-même te paraît fausse, dis-le à part.\n"
                       "Réponds : ===BILAN===\n(markdown)\n===FIN===")
            write_md(EXP / "etalonnage" / f"{unit['id']}-{judge}.md",
                     f"# Étalonnage {unit['id']} contre {unit['fiche']} — juge : {judge}\n\n*{RIGHTS}*\n\n"
                     + (between(ans, "===BILAN===") or ans.strip()) + "\n")
            measure(evt="etalonnage", unite=unit["id"], fiche=unit["fiche"], juge=judge)
        journal(f"## Étalonnage `{unit['id']}` contre {unit['fiche']} — {t}\n(experience/etalonnage/)")
        s["phase"] = "fin"

    if s["phase"] == "fin":
        s["done"].append(unit["id"])
        s["unit_idx"] += 1
        s["phase"], s["revisions"], s["link_alert"] = "draft", 0, ""
        s["author"] = other(author)
    s["turns"] += 1


EIGHT = ""


def main():
    global EIGHT
    OUT.mkdir(parents=True, exist_ok=True)
    for p in STOP_PATHS:
        if p.exists():
            print(f"Arrêt demandé ({p}).")
            return
    charter = read(CHARTER_PATH)
    m = re.search(r"## Les huit erreurs.*?(?=\n## |\Z)", charter, re.S)
    EIGHT = m.group(0) if m else ""
    prog = json.loads(read(PROGRAMME_PATH))
    units = prog["unites"]
    commit = prog["lean_commit"]
    if git("cat-file", "-t", commit, check=False).strip() != "commit":
        sys.exit(f"Commit Lean {commit} absent du clone {LEAN_DIR}.")
    head = git("rev-parse", "HEAD", check=False).strip()
    if head and head != commit and env("ALLOW_OTHER_HEAD", "0") != "1":
        sys.exit(f"Le clone Lean est extrait à {head}, pas au commit figé {commit}.")
    s = load_state()
    if s.get("lean_commit") and s["lean_commit"] != commit:
        sys.exit(f"Le commit Lean a changé ({s['lean_commit']} → {commit}) : "
                 "ouvrir un nouveau dossier travail/, ne pas mélanger deux versions.")
    s["lean_commit"] = commit
    s["_paths"] = set(git("ls-tree", "-r", "--name-only", commit).splitlines())
    try:
        for _ in range(TURNS_PER_RUN):
            if s["unit_idx"] >= len(units):
                (OUT / "STOP").write_text("fin du programme\n")
                journal("## Fin : toutes les unités du programme ont été traitées.")
                break
            if s["turns"] >= MAX_TURNS_TOTAL:
                (OUT / "STOP").write_text(f"Plafond de {MAX_TURNS_TOTAL} tours atteint.\n")
                journal(f"## Arrêt : plafond de {MAX_TURNS_TOTAL} tours atteint.")
                break
            turn(s, units, prog, charter)
            write_index(units, s, prog)
    finally:
        s.pop("_paths", None)
        save_state(s)
        write_index(units, s, prog)


if __name__ == "__main__":
    main()
