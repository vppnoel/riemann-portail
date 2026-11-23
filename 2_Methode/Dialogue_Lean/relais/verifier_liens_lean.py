#!/usr/bin/env python3
"""Contrôle des liens Lean d'un texte Markdown.

Usage : python3 -I verifier_liens_lean.py TEXTE.md CHEMIN_CLONE_LEAN [COMMIT]

Pour chaque lien de la forme
  [`nom`](https://github.com/leanprover-community/riemann-hypothesis/blob/<commit>/<chemin>#L<n>)
le script vérifie trois choses :
  1. le commit du lien est le commit attendu ;
  2. le fichier existe à ce commit (via `git show`, donc il marche sur un clone partiel) ;
  3. la ligne n contient le dernier composant du nom cité (par ex. `core_gm` pour
     `UpperTheory.Comparison₂.core_gm`), comme identifiant entier et non comme
     préfixe d'un autre nom (`landau_pole_asym` ≠ `landau_pole_asym_deriv`).

Il signale les écarts sans rien corriger. Code de sortie 1 s'il y en a.
Bibliothèque standard seulement.
"""
import re
import subprocess
import sys

DEPOT = "https://github.com/leanprover-community/riemann-hypothesis/blob/"
COMMIT_DEFAUT = "51d9b1a28026d458aef9c9af3df8b083276e3d2d"


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    texte, clone = sys.argv[1], sys.argv[2]
    commit = sys.argv[3] if len(sys.argv) > 3 else COMMIT_DEFAUT
    s = open(texte, encoding="utf-8-sig").read()
    motif = re.compile(r"\[([^\]]*)\]\(" + re.escape(DEPOT) + r"([0-9a-f]{7,40})/([^)#]+)(?:#L(\d+))?\)")
    liens = motif.findall(s)
    cache, ecarts = {}, 0
    for etiquette, c, chemin, ligne in liens:
        if c != commit:
            print(f"COMMIT  {etiquette} : {c} au lieu de {commit}")
            ecarts += 1
        if chemin not in cache:
            r = subprocess.run(["git", "-C", clone, "show", f"{commit}:{chemin}"],
                               capture_output=True, text=True, timeout=120)
            cache[chemin] = r.stdout.splitlines() if r.returncode == 0 else None
        lignes = cache[chemin]
        if lignes is None:
            print(f"FICHIER {etiquette} : {chemin} introuvable au commit")
            ecarts += 1
            continue
        if not ligne:
            continue
        n = int(ligne)
        contenu = lignes[n - 1] if 0 < n <= len(lignes) else ""
        # Le nom cité est le dernier passage entre accents graves de l'étiquette s'il y en a
        # (l'étiquette peut englober du texte qui précède le lien), sinon son premier mot.
        cites = re.findall(r"`([^`]+)`", etiquette)
        mots = (cites[-1] if cites else re.sub(r"[`\[\]]", "", etiquette)).split()
        nom = mots[0].split(".")[-1] if mots else ""
        # Le nom doit apparaître comme identifiant entier : `landau_pole_asym` ne doit pas
        # être accepté sur la ligne de `landau_pole_asym_deriv` (défaut relevé dans la
        # vérification de TAC-023). Un point peut précéder (espace de noms), pas un caractère
        # d'identifiant ; rien d'identifiant ne doit suivre.
        entier = re.compile(r"(?<![\w'])" + re.escape(nom) + r"(?![\w'!?])") if nom else None
        if nom and nom.lower() not in ("definition", "définition") and not entier.search(contenu):
            print(f"LIGNE   {etiquette} : {chemin.split('/')[-1]}#L{n} → {contenu.strip()[:100]}")
            ecarts += 1
    print(f"{len(liens)} liens, {len(cache)} fichiers, {ecarts} écart(s)")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
