#!/usr/bin/env python3
"""Page d'état du travail, lisible sur téléphone : 2_Methode/Echanges/ETAT.md.

Lit le registre des fiches (lecture seule) et dit, pour chaque fiche, où elle en est et QUI doit agir.
Régénérée automatiquement sur GitHub après chaque changement du registre (.github/workflows/boites.yml).
python -B 2_Methode/Pilotage/etat.py
Auteur et titulaire des droits : Vincent NOËL.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DEPOT = 'https://github.com/Vppnoel/riemann'
d = json.loads((ROOT / '2_Methode/Pilotage/taches.json').read_text(encoding='utf-8-sig'))
J = json.loads((ROOT / '2_Methode/Pilotage/journal_taches.json').read_text(encoding='utf-8-sig'))['evenements']
AUTEUR = 'auteur:vincent-noel'
NOMS = {'ia:claude': 'Claude', 'ia:chatgpt-sol-6.1-max': 'ChatGPT', AUTEUR: 'toi'}
nom = lambda a: NOMS.get(a, a or '—')
LIBELLE = {'ouverte': 'ouverte', 'assignee': 'en production', 'deposee': 'déposée, à vérifier', 'verifiee': 'vérifiée',
           'a_reprendre': 'à reprendre', 'acceptee': 'acceptée', 'integree': 'intégrée', 'rejetee': 'rejetée',
           'abandonnee': 'abandonnée', 'perimee': 'périmée'}
FORM = f'{DEPOT}/actions/workflows/decision.yml'

def prochaine(t):
    st, prod = t['statut'], t['assigne_a']
    autres = [a for a in NOMS if a not in (prod, AUTEUR)]
    if st == 'ouverte': return 'toi', "l'attribuer à une IA (dis-le dans le fil)"
    if st == 'assignee': return nom(prod), 'produire' if t['previsions'] else 'écrire la prévision, puis produire'
    if st == 'deposee': return nom(autres[0]) if autres else 'un autre acteur', 'vérifier le dépôt'
    if st == 'verifiee': return 'toi', f'décider : [formulaire]({FORM}) (Run workflow → fiche, acceptee / rejetee / a_reprendre)'
    if st == 'a_reprendre': return nom(prod), 'reprendre selon la vérification'
    if st == 'acceptee': return nom(prod), 'intégrer au corpus'
    return '—', '—'

def derniere(t):
    ev = [e for e in J if e['tache'] == t['id']]
    return ev[-1]['le'][:16].replace('T', ' ') + ' UTC' if ev else '—'

T = d['taches']; pour_toi = [t for t in T if prochaine(t)[0] == 'toi']
L = ['﻿# État du travail — Programme Riemann', '',
     f"*Page générée automatiquement depuis le registre des fiches, à chaque changement. Dernier événement : {max(e['le'] for e in J)[:16].replace('T', ' ')} UTC.*", '',
     '## Ce qui t\'attend', '']
L += [f"- **{t['id']}** — {t['titre']} : {prochaine(t)[1]}" for t in pour_toi] or ['- **Rien.** Aucune fiche n\'attend ta décision.']
L += ['', 'Les pull requests marquées « Méthode » attendent aussi ton accord : '
      f'[liste des pull requests ouvertes]({DEPOT}/pulls).', '',
      '## Toutes les fiches', '',
      '| Fiche | Sujet | Statut | Producteur | Vérifications | Qui agit | Quoi | Dernier mouvement | Fil |', '|---|---|---|---|---|---|---|---|---|']
for t in T:
    qui, quoi = prochaine(t)
    ver = ', '.join(f"{nom(v['par'])} : {'conforme' if v['verdict'] == 'conforme' else 'non conforme'}" for v in t['verifications']) or '—'
    st = LIBELLE.get(t['statut'], t['statut'])
    if t.get('decision'): st += f" ({t['decision']['decision']})"
    L.append(f"| {t['id']} | {t['titre']} | {st} | {nom(t['assigne_a'])} | {ver} | {qui} | {quoi} | {derniere(t)} | [fil]({DEPOT}/issues?q={t['id']}) |")
L += ['', '## Liens utiles', '',
      f'- [Pull requests ouvertes]({DEPOT}/pulls) · [Fils de discussion]({DEPOT}/issues) · [Formulaire de décision]({FORM})',
      f'- [Règles de travail](../../GITHUB.md) · [Procédure des fiches](../Pilotage/CIBLAGE.md)', '']
(ROOT / '2_Methode/Echanges/ETAT.md').write_text('\n'.join(L), encoding='utf-8')
print('\n'.join(L[4:12]))
