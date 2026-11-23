#!/usr/bin/env python3
"""Contrôle d'un ajout au registre des sources hors PR de méthode (GITHUB.md § 4.7).

Usage : python -B 2_Methode/Sources/verifier_ajout_sources.py ANCIEN.json NOUVEAU.json

Sans « [méthode] », une pull request peut seulement AJOUTER des fiches à sources.json :
  1. aucune fiche existante n'est modifiée ni supprimée (comparaison par clé, contenu identique) ;
  2. chaque nouvelle clé est neuve et suit le format des clés ([A-Z][A-Za-z]{1,7}[0-9]{2}[a-z]?) ;
  3. chaque nouvelle fiche a tous les champs obligatoires, un lien https, une date de vérification,
     et des valeurs admises pour statut, verdict et intérêt.
Toute autre modification du registre reste un changement de méthode.
Bibliothèque standard seulement. Code de sortie 1 en cas d'écart.
"""
import json
import re
import sys

OBLIG = ["cle", "auteurs", "annee", "titre", "publication", "type", "lien", "statut",
         "ce_qui_a_ete_verifie", "usage_corpus", "verdict", "motifs", "verifie_le",
         "correction", "conjectures", "interet", "docs", "cite_aussi"]
STATUTS = {"vérifié en ligne", "partiellement vérifié", "non vérifié"}
VERDICTS = {"exact", "imprécis", "faux", "non vérifiable"}
INTERETS = {"appui", "confronter", "contexte", "outil"}
CLE = re.compile(r"^[A-Z][A-Za-z]{1,7}[0-9]{2}[a-z]?$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def charger(p):
    with open(p, encoding="utf-8-sig") as f:
        return {e["cle"]: e for e in json.load(f)}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    avant, apres = charger(sys.argv[1]), charger(sys.argv[2])
    ecarts = []
    for k, e in avant.items():
        if k not in apres:
            ecarts.append(f"{k} : fiche supprimée")
        elif apres[k] != e:
            champs = sorted(c for c in set(e) | set(apres[k]) if e.get(c) != apres[k].get(c))
            ecarts.append(f"{k} : fiche existante modifiée ({', '.join(champs)})")
    nouvelles = [k for k in apres if k not in avant]
    for k in nouvelles:
        e = apres[k]
        if not CLE.match(k):
            ecarts.append(f"{k} : clé hors format")
        manquants = [c for c in OBLIG if c not in e]
        if manquants:
            ecarts.append(f"{k} : champs manquants ({', '.join(manquants)})")
        if not str(e.get("lien", "")).startswith("https://"):
            ecarts.append(f"{k} : lien absent ou non https")
        if not DATE.match(str(e.get("verifie_le", ""))):
            ecarts.append(f"{k} : date de vérification absente ou hors format AAAA-MM-JJ")
        if e.get("statut") not in STATUTS:
            ecarts.append(f"{k} : statut non admis ({e.get('statut')})")
        if e.get("verdict") not in VERDICTS:
            ecarts.append(f"{k} : verdict non admis ({e.get('verdict')})")
        if e.get("interet") not in INTERETS:
            ecarts.append(f"{k} : intérêt non admis ({e.get('interet')})")
        if not str(e.get("ce_qui_a_ete_verifie", "")).strip():
            ecarts.append(f"{k} : « ce_qui_a_ete_verifie » vide")
    for x in ecarts:
        print("ÉCART  " + x)
    print(f"{len(nouvelles)} fiche(s) ajoutée(s) : {', '.join(nouvelles) or '—'} ; {len(ecarts)} écart(s)")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
