#!/usr/bin/env python3
"""V6.58 — intègre les documents 80 et 81 au pilotage et réorganise l'entrée du corpus.

python -B 2_Methode/Outils/integrate_v658.py            # données de pilotage + README + plan du corpus
puis : python -B 2_Methode/Outils/integrate_v655.py --rebuild

Auteur et titulaire des droits : Vincent NOËL.
Le script est idempotent : relancé, il ne duplique rien. Il ne modifie aucun niveau de l'indicateur,
aucun statut d'idée, aucun original reçu ou archivé. Il suit le protocole du pilotage (README de
2_Methode/Pilotage) : prévision conservée, preuve et portée enregistrées, bilan rapproché, indicateur
réexaminé, dépendances et contrats.
"""
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[2]
PRES = ROOT / '1_Presentation'
V, DATE_ISO, DATE_FR = 'V6.58', '2026-10-17', '17 octobre 2026'
D80, D81 = '1_Presentation/80_D_OU_VIENT_LE_SIGNE.md', '1_Presentation/81_ZHU_REPRODUIT.md'
MARK = 'V6.58 :'


def rd(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8-sig'))


def wr(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


# ---------------------------------------------------------------- registre des identifiants
def registre():
    rel = '2_Methode/Pilotage/registre_identifiants.json'; r = rd(rel)
    pos = {d['number']: i for i, d in enumerate(r['documents'])}
    for n, stem, extra in ((80, '80_D_OU_VIENT_LE_SIGNE', ['80_Trois_niveaux_du_signe.png', 'english/80_WHERE_THE_SIGN_COMES_FROM.md',
                                                          'english/80_WHERE_THE_SIGN_COMES_FROM.pdf', 'english/80_three_levels_EN.png']),
                           (81, '81_ZHU_REPRODUIT', ['81_Zhu_reproduit.png', 'english/81_ZHU_REPRODUCED.md', 'english/81_ZHU_REPRODUCED.pdf',
                                                     'english/81_zhu_reproduced_EN.png'])):
        doc = dict(id=f'DOC-{n:03d}', number=n, paths=[f'1_Presentation/{stem}.md', f'1_Presentation/{stem}.pdf'] +
                   ['1_Presentation/' + e for e in extra], renumbered=False)
        if n in pos: r['documents'][pos[n]] = doc
        else: r['documents'].append(doc)
    for doc in r['documents']:                                   # versions anglaises des documents 01 et 07
        extra = {1: ['1_Presentation/english/01_SYNTHESIS_EN.md', '1_Presentation/english/01_SYNTHESIS_EN.pdf'],
                 7: ['1_Presentation/english/07_READING_GUIDE_EN.md', '1_Presentation/english/07_READING_GUIDE_EN.pdf']}.get(doc['number'], [])
        doc['paths'] += [x for x in extra if x not in doc['paths']]
    r['revision'] = 'v658-documents-80-81'
    wr(rel, r)


# ---------------------------------------------------------------- navigateur : trois coups et un bilan
COUPS = [
    dict(id='v658_trois_niveaux', titre="D'où vient le signe dans le Modèle réduit : comptage, degré ou carré", statut='fait',
         type='preuve auxiliaire', question="La réalisation de Gram Q = ‖Af‖² existe-t-elle dans le Modèle réduit, et quelle structure y impose le signe ?",
         these="Séparer trois niveaux de positivité calculables depuis les comptages : comptage, degré d'isogénie, trace d'un carré.",
         cout=1, version=V, temoin="Prévisions G1–G4 écrites avant (data/prevision_v658_gram.md) ; calcul exact sur 425 courbes et 220 faux jumeaux ; pivots rationnels.",
         document='80_D_OU_VIENT_LE_SIGNE.pdf', gains={}, probabilite=0, probabilite_scope='Aucune estimation de probabilité ; étude déjà exécutée.',
         prerequis=[], debloque=[], operateurs=[], croise=['RH'], repond_a=[],
         appris="Comptages et degrés restent positifs pour 119 faux jumeaux qui violent RH ; seule la trace de u·ι(u) (Rosati, polarisation) les exclut. ζ passe les niveaux 1 et 2 ; ce qui manque est un carré.",
         prevision=dict(gains={}, probabilite=None, texte='G1–G4, data/prevision_v658_gram.md, 8 h 50 UTC : quatre justes.'),
         refutation_tenue='Aucun gain global annoncé ; proposition élémentaire, résultats de géométrie cités.',
         evaluation_courante=dict(date=DATE_ISO, statut_avant='nouveau', statut='fait', raison='Résultat de V6.58 enregistré dans son périmètre (Modèle réduit) ; transfert à ζ non revendiqué.',
                                  groupe='secondaire', source=D80, calcul_rejoue=True)),
    dict(id='v658_zhu_reproduit', titre='Reproduire les fenêtres de Zhu par une méthode indépendante', statut='fait',
         type='mesure', question='Les valeurs λ*(L) de Zhu (L = 0,5 à 0,8) sont-elles retrouvées par une forme de Weil en variable x, contrôlée par les zéros ?',
         these='Une forme en x, à intégrales bornées, reproduit les majorants de Zhu et situe les certificats du corpus.',
         cout=1, version=V, temoin='Prévisions Z1–Z5 écrites avant (data/prevision_v658_zhu.md) ; contrôle par 1 070 zéros à 1,9·10⁻¹³ ; 60 chiffres, non certifié.',
         document='81_ZHU_REPRODUIT.pdf', gains={}, probabilite=0, probabilite_scope='Aucune estimation de probabilité ; étude déjà exécutée.',
         prerequis=[], debloque=['v658_certificat_noyau_S08'], operateurs=[], croise=['RH'], repond_a=[],
         appris='Valeurs de Zhu retrouvées à 0,1–8 % près ; la direction presque nulle est celle du pôle ; sur le noyau des moments la marge à 0,8 est d’environ 5·10⁻¹².',
         prevision=dict(gains={}, probabilite=None, texte='Z1–Z4 (9 h 10 UTC) et Z5 (9 h 47 UTC), data/prevision_v658_zhu.md.'),
         refutation_tenue='Aucune certification revendiquée ; valeurs majorantes.',
         evaluation_courante=dict(date=DATE_ISO, statut_avant='nouveau', statut='fait', raison='Mesure enregistrée comme mesure ; la certification de Zhu est citée, non reproduite.',
                                  groupe='noyau_S08', source=D81, calcul_rejoue=True)),
    dict(id='v658_certificat_noyau_S08', titre='Certifier la marge du noyau des moments à S = 0,8', statut='route à construire',
         type='certificat', question='Prolonger les certificats des documents 71, 73 et 75 (S ≤ 11/20) jusqu’à S = 0,8, où agissent les premiers 2, 3 et 4, avec une marge visée d’environ 10⁻¹². Portée corrigée le 17 octobre : la positivité à 0,8 suit déjà du minorant certifié de Zhu ; l’apport serait une marge indépendante environ 10⁵ fois plus forte sur le noyau, pas une fenêtre nouvelle.',
         temoin='Marge mesurée sur le noyau (doc. 81) ; certificat existant à 11/20 (doc. 75, 3/10000).',
         document='81_ZHU_REPRODUIT.pdf', gains={}, cout=None, probabilite=None, prerequis=['v658_zhu_reproduit'], debloque=[], operateurs=[], croise=['RH'], repond_a=[],
         probabilite_scope='Hors du classement numérique ; aucune probabilité attribuée.',
         prevision=dict(gains={}, probabilite=None,
                        texte='Écrite le 17 octobre 2026 avant tout essai de certification : (P1) la marge mesurée se stabilise entre 3·10⁻¹² et 6·10⁻¹² avec 40 modes ou plus ; (P2) un minorant certifié d’au moins 10⁻¹² demande une tête de dimension au moins 100 dans l’architecture du document 73. Critère de rejet : marge mesurée sous 10⁻¹³, ou tête irréalisable en intervalles.'),
         evaluation_courante=dict(date=DATE_ISO, statut_avant='nouveau', statut='route à construire', raison='Pré-enregistré en V6.58 avec sa prévision ; non exécuté ; hors du classement numérique (aucune probabilité attribuée).',
                                  groupe='noyau_S08', source=D81, calcul_rejoue=False)),
]


def navigateur():
    rel = '2_Methode/Navigateur/carte_navigation.json'; n = rd(rel)
    pos = {c['id']: i for i, c in enumerate(n['coups'])}
    for c in COUPS:
        if c['id'] in pos: n['coups'][pos[c['id']]] = c
        else: n['coups'].append(c)
    n['bilan_v658'] = dict(version=V, document='80_D_OU_VIENT_LE_SIGNE.pdf',
        resultat="Doc. 80 : dans le Modèle réduit, le signe ne vient ni des comptages ni des degrés, mais d'un carré (Rosati). Doc. 81 : fenêtres de Zhu reproduites sans certification ; marge du noyau des moments ≈ 5·10⁻¹² à 0,8 (positivité déjà couverte par Zhu). Aucune preuve de RH ; niveaux inchangés.",
        next_action=dict(titre='Certifier la marge du noyau des moments à S = 0,8', document='81_ZHU_REPRODUIT.pdf', statut='route à construire',
                         probabilite_estimee=None, action_ids=['v658_certificat_noyau_S08']),
        probability_estimate=None, current_decision_model='2_Methode/Pilotage/pilotage_recherche.json')
    wr(rel, n)


# ---------------------------------------------------------------- pilotage : évaluations, fiches, investigation
def pilotage():
    rel = '2_Methode/Pilotage/pilotage_recherche.json'; p = rd(rel)
    p['version'], p['revision'], p['date'] = V, 'v658-signe-carre-zhu-20261017', DATE_ISO
    add = {'comprendre': ([D80], "V6.58 : le Modèle réduit localise la source du signe dans un carré (Rosati), ni comptage ni degré (doc. 80). Niveau inchangé."),
           'croiser': ([D80], "V6.58 : trois niveaux de positivité transposés exactement entre courbes et ζ (doc. 80). Niveau inchangé."),
           'voir': ([D81], "V6.58 : fenêtres de Zhu reproduites par une méthode indépendante, contrôlée par les zéros (doc. 81, non certifié). Niveau inchangé."),
           'case': ([D81], "V6.58 : la marge du noyau des moments à S = 0,8 est mesurée (≈ 5·10⁻¹²) ; la positivité à 0,8 suit déjà du minorant certifié de Zhu, qui domine en portée les certificats 71–75. Niveau inchangé.")}
    for k, (ev, txt) in add.items():
        r = p['reviews'][k]
        for e in ev:
            if e not in r['evidence']: r['evidence'].append(e)
        if MARK not in r['reason']: r['reason'] = r['reason'].rstrip() + ' ' + txt
        r['reviewed_on'] = DATE_ISO
    node_ev = {'modred': [D80], 'objet': [D80], 'pos': [D80, D81], 'local': [D81]}
    for nd in p['nodes']:
        for e in node_ev.get(nd['id'], []):
            if e not in nd['evidence']: nd['evidence'].append(e)
    if not any(i['id'] == 'noyau_S08' for i in p['investigations']):
        p['investigations'].append(dict(
            id='noyau_S08', label='Certificat du noyau des moments à S = 0,8', requires=[], nodes=['local', 'pos'],
            question='Certifier un minorant de Q_W sur les tests à moments nuls de support [−0,8 ; 0,8], où agissent 2, 3 et 4.',
            witness='Marge mesurée ≈ 5·10⁻¹² (doc. 81), non certifiée ; certificat existant jusqu’à 11/20 (doc. 75).',
            refutation='Marge mesurée sous 10⁻¹³ avec plus de modes, ou tête irréalisable en intervalles : la voie par fenêtres s’arrête à 11/20.',
            output='Certificat local ou obstacle documenté. Renforce une marge déjà positive (Zhu) ; aucune fenêtre nouvelle ni conséquence globale : la positivité sur toutes les fenêtres est RH.',
            source=D81, status='ouvert', probability=None, pre_registered_on=DATE_ISO, not_executed=True,
            dimensions=['case', 'demontrer']))
    wr(rel, p)


# ---------------------------------------------------------------- indicateur : étape V6.58, niveaux inchangés
def indicateur():
    rel = '2_Methode/Indicateur/indicateur_avancement.json'; d = rd(rel)
    if not any(e['id'] == 'v658' for e in d['etapes']):
        last = d['etapes'][-1]
        d['etapes'].append(dict(id='v658', court=V, versions=V, jour='17 oct.', niveaux=dict(last['niveaux']),
            franchi="V6.58 : le signe vient d'un carré. Dans le Modèle réduit, comptages et degrés d'isogénie restent positifs pour 119 faux jumeaux ; seule la trace d'un carré (Rosati) les exclut. Fenêtres de Zhu reproduites sans certification ; marge du noyau des moments ≈ 5·10⁻¹² à 0,8 (positivité déjà couverte par Zhu). Aucune preuve de RH ; niveaux inchangés.",
            pourquoi={'comprendre': "Le mécanisme du signe est localisé dans le Modèle réduit ; son analogue pour ζ manque.",
                      'case': "Aucune fenêtre nouvelle certifiée ; une cible chiffrée."},
            documents=[["D'où vient le signe", '80_D_OU_VIENT_LE_SIGNE.pdf'], ['Zhu reproduit', '81_ZHU_REPRODUIT.pdf'],
                       ['Programmes', '../3_Preuves_et_calculs/scripts/run_gram_modele_reduit.py']]))
    d['comparaison']['apres'] = 'v658'; d['comparaison']['apres_libelle'] = 'État V6.58, réévalué le 17 octobre'
    wr(rel, d)


# ---------------------------------------------------------------- plan du corpus
THEMES = [
    ("I. Point de départ : l'énergie Q et les premiers textes",
     "Le programme part d'une énergie construite avec les nombres premiers, dont la croissance lit la position des zéros. Théorèmes A et B, attaques reçues et leur audit, leçon de 2026.",
     ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']),
    ("II. Les instruments V6 et leur audit",
     "Bascule vers un atlas de mécanismes : détecteurs, verrous local et global, audits de conventions, classement de ce que chaque instrument voit.",
     ['14', '15', '16', '17', '18', '19', '21', '22', '23', '24', '25', '26']),
    ("III. Ce que RH exige : familles, Modèle réduit, Archipel d'Euler",
     "Là où RH est un théorème (courbes sur 𝔽_q) et parmi les fonctions qui partagent l'équation fonctionnelle : la nécessité se voit, et elle tient au produit d'Euler.",
     ['27', '28', '29', '30', '56', '57', '58', '61', '63', '64']),
    ("IV. Des premiers au continu : opérateurs, seuils, rencontres",
     "L'opérateur de ζ reconstruit depuis les premiers, la base comme pas de temps, la loi de seuil, le degré 2, la Rencontre à n.",
     ['32', '33', '35', '38', '39', '40', '41', '43', '45', '53', '54']),
    ("V. La surface virtuelle et le carré",
     "Ce que serait l'objet géométrique pour ζ : surface et Riemann–Roch virtuels, Frobenius, le carré en continu, et la localisation du signe dans un carré.",
     ['46', '47', '48', '49', '50', '51', '52', '80']),
    ("VI. La positivité de Weil : certificats, ponts et obligations",
     "Le front actuel : certificats sur des fenêtres, ponts arithmétiques, compensation, transport, et les obligations globales restantes.",
     ['59', '60', '65', '66', '67', '68', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '81', 'ESSAI', 'CORRELATIONS', 'PARCOURS']),
    ("VII. Outils, gouvernance et relectures",
     "Registre des métaphores et des sources, indicateur, navigateur et Bellman, matrice des théories, pré-relecture, articles.",
     ['20', '31', '34', '36', '37', '42', '44', '55', '62', '69']),
]
TITRES = {'02': 'Article court (EN)', '03': 'Dossier de relecture (EN, remplacé par relecture/)', '04': 'Brief pour spécialistes (EN)',
          '05': 'Message au relecteur', '09': 'Attaques reçues : audit et amélioration', '10': 'Attaque 2 : résultats jusqu’à N = 1000',
          '11': 'Estimation sous RH', '12': 'Annulation du pôle', '13': 'Leçon 2026', '25': 'Atlas des métaphores physique–mathématique',
          '31': "Indicateur d'avancement", '34': 'Navigateur de recherche', '44': 'Matrice des théories'}
ESSENTIELS = {'28', '30', '37', '58', '60', '71', '73', '75', '76', '79', '80', '81', 'ESSAI', 'CORRELATIONS'}
SPECIAUX = {'ESSAI': 'ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55', 'CORRELATIONS': 'CORRELATIONS_IDENTITE_ET_ENERGIE', 'PARCOURS': 'PARCOURS_ET_PROPRIETES'}


def titre_md(p):
    t = p.read_text(encoding='utf-8-sig')
    m = re.search(r'^title:\s*"([^"]+)"', t, re.M)
    if m: return m.group(1)
    m = re.search(r'^#\s+(.+)$', t, re.M)
    s = m.group(1).strip() if m else p.stem
    return re.sub(r'^V6[.\d]*[a-z/.]*\s*[—–-]\s*', '', s)


def pieces(key):
    """Liste (stem, titre, liens) pour un numéro ou une clé spéciale. Les pages-ateliers HTML d'un même numéro
    (graphes, langue, ponts…) sont rattachées au document comme liens « atelier »."""
    if key in SPECIAUX: stems = [SPECIAUX[key]]; ateliers = []
    else:
        files = [f for f in PRES.glob(key + '_*') if f.is_file() and not f.name.endswith('_nav.html')]
        docs = sorted({f.stem for f in files if f.suffix in ('.md', '.pdf', '.docx')})
        pages = sorted({f.stem for f in files if f.suffix == '.html'})
        stems = docs or pages; ateliers = [x for x in pages if x not in stems]
    out = []
    for i, st in enumerate(stems):
        files = {ext: PRES / (st + ext) for ext in ('.pdf', '.md', '.html', '.docx') if (PRES / (st + ext)).exists()}
        if not files: continue
        titre = titre_md(files['.md']) if '.md' in files else TITRES.get(key, st.replace('_', ' ').capitalize())
        liens = [f'[{lab}](1_Presentation/{st}{ext})' for ext, lab in (('.pdf', 'PDF'), ('.html', 'page'), ('.md', 'texte'), ('.docx', 'Word')) if ext in files]
        if i == 0: liens += [f'[atelier](1_Presentation/{x}.html)' for x in ateliers]
        out.append((st, titre, ' · '.join(liens)))
    return out


def plan():
    L = ['# Plan du corpus — Programme Riemann ' + V, '',
         f'**{DATE_FR}.** Les documents gardent leur numéro, leur date et la version de leur rédaction ; ce plan les range par question plutôt que par ordre chronologique. ★ marque les pièces signalées dans « À lire d’abord » ([README](README.md)). Auteur : Vincent NOËL.', '']
    seen = set()
    for titre, intro, keys in THEMES:
        L += ['## ' + titre, '', intro, '', '| N° | Document | Fichiers |', '|---|---|---|']
        for k in keys:
            for st, t, liens in pieces(k):
                if st in seen: continue
                seen.add(st)
                num = st[:2] if st[:2].isdigit() else '—'
                star = '★ ' if (k in ESSENTIELS) else ''
                L.append(f'| {num} | {star}{t.replace("|", "∣")} | {liens} |')
        L.append('')
    L += ['## Hors numérotation', '',
          '- [Articles au format standard (PDF et LaTeX)](1_Presentation/articles/) · [Dossier pour un spécialiste](1_Presentation/relecture/00_READ_ME_FIRST_EN.md)',
          '- [Reconstruction V6.51 intégrée](1_Presentation/RECONSTRUCTION_V651_INTEGREE.html) · [Récupération historique](RECUPERATION.html)',
          '- [Liste des figures](1_Presentation/LISTE_DES_FIGURES.md) · [Preuves et calculs : mode d’emploi](3_Preuves_et_calculs/README.md)',
          '- [Table logique](TABLE_LOGIQUE.md) · [Références hiérarchisées](REFERENCES_HIERARCHISEES.md) · [Guide pour une IA](GUIDE_POUR_UNE_IA.md)',
          '- En anglais : [README_EN](README_EN.md) · [Logical table](LOGICAL_TABLE.md) · [Ranked references](REFERENCES_RANKED.md) · [Guide for an AI](GUIDE_FOR_AN_AI.md) · [document 80](1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.pdf) · [document 81](1_Presentation/english/81_ZHU_REPRODUCED.pdf)',
          '- [Historique des livraisons](HISTORIQUE_DES_LIVRAISONS.md)', '']
    missing = sorted({f.name[:2] for f in PRES.glob('[0-9][0-9]_*') if f.suffix in ('.md', '.pdf', '.html', '.docx')} - {s[:2] for s in seen})
    if missing: raise SystemExit('Plan incomplet, numéros non rangés : ' + ', '.join(missing))
    (ROOT / 'PLAN_DU_CORPUS.md').write_text('\n'.join(L), encoding='utf-8-sig')


# ---------------------------------------------------------------- README et historique
CHANGES = [
          '- **Résultats.** [Document 80](1_Presentation/80_D_OU_VIENT_LE_SIGNE.pdf) (le signe vient d’un carré) et [document 81](1_Presentation/81_ZHU_REPRODUIT.pdf) (Zhu reproduit, noyau des moments), avec prévisions écrites avant, scripts, données et tests.',
          '- **Intégration au pilotage.** Documents 80 et 81 au registre des identifiants ; trois actions au navigateur (deux faites, une ouverte et pré-enregistrée : certifier la marge à S = 0,8) ; étape V6.58 de l’indicateur, niveaux inchangés et motivés ; fiches d’idées et investigation reliées ; références Zhu26, Wei48 et Mum70 au registre des sources.',
          '- **Réorganisation.** Ce README ne garde que l’entrée du corpus ; le [plan du corpus](PLAN_DU_CORPUS.md) range les 81 documents par question ; l’[historique des livraisons](HISTORIQUE_DES_LIVRAISONS.md) conserve tous les anciens README. Le portail affiche le même bloc « À lire d’abord ».',
          '- **Outils de lecture.** [Table logique](TABLE_LOGIQUE.md) : les énoncés en forme logique sur cinq routes vers RH, leur statut lu dans le pilotage, les témoins contraires, les obstructions et ce qui manque au plus court. [Références hiérarchisées](REFERENCES_HIERARCHISEES.md) : les 177 fiches rangées par rôle logique, avec celles à vérifier en priorité. [Guide pour une IA](GUIDE_POUR_UNE_IA.md) : un prompt qui explique à une autre IA comment utiliser le corpus et proposer les prochaines étapes. Les trois documents sont générés depuis les données par `2_Methode/Outils/build_outils_de_lecture.py`.',
          '- **Synthèse et guide de lecture à jour.** [Synthèse](1_Presentation/01_SYNTHESE_FR.pdf) (doc. 01) et [guide de lecture intuitif](1_Presentation/07_GUIDE_DE_LECTURE_INTUITIF.pdf) (doc. 07) décrivent l’état V6.58, avec leurs versions anglaises ; les versions V6.24 sont conservées dans `4_Archives/historique/`.',
          '- **Registres V6.44–V6.50 déclarés historiques** (décision de l’auteur) : ils ne sont plus comparés au corpus courant, que le pilotage suit depuis V6.55 ; voir `3_Preuves_et_calculs/data/registres_historiques_v650.json`.',
          '- **Réparations.** Pages générées resynchronisées avec leurs données ; tests hérités corrigés lorsque l’écart venait d’un test périmé, et non d’un résultat. Détail : [note de livraison](2_Methode/Pilotage/LIVRAISON_V658.md).']

CHANGES_EN = [
          '- **Results.** [Document 80](1_Presentation/english/80_WHERE_THE_SIGN_COMES_FROM.pdf) (the sign comes from a square) and [document 81](1_Presentation/english/81_ZHU_REPRODUCED.pdf) (Zhu reproduced; the moment kernel), with predictions written in advance, scripts, data and tests.',
          '- **Reading tools.** [Logical table](LOGICAL_TABLE.md): statements in logical form on five routes towards RH, with live statuses, counter-witnesses, obstructions and the open cut. [Ranked references](REFERENCES_RANKED.md): 177 records ranked by logical role. [Guide for an AI](GUIDE_FOR_AN_AI.md): a prompt explaining how to use the corpus and propose next steps. French versions are generated from the same data.',
          '- **Synthesis and reading guide.** Both are up to date at V6.58, in [French](1_Presentation/01_SYNTHESE_FR.pdf) and [English](1_Presentation/english/01_SYNTHESIS_EN.pdf) for the synthesis, and in [French](1_Presentation/07_GUIDE_DE_LECTURE_INTUITIF.pdf) and [English](1_Presentation/english/07_READING_GUIDE_EN.pdf) for the guide.',
          '- **V6.44–V6.50 registries declared historical** (author\'s decision): they are no longer compared with the current corpus, which the steering data has tracked since V6.55.',
          '- **Reorganization.** The French README keeps only the entry; the [corpus map](PLAN_DU_CORPUS.md) groups the 81 documents by question; the [release history](HISTORIQUE_DES_LIVRAISONS.md) keeps every earlier README (in French).']

REPRO = 'integrate_v658.py'
EN_DOCS = 'documents 80–81'

def readme():
    pts = rd('2_Methode/Pilotage/points_d_attention.json')
    hist = ROOT / 'HISTORIQUE_DES_LIVRAISONS.md'
    if not hist.exists():
        old = (ROOT / 'README.md').read_text(encoding='utf-8-sig')
        hist.write_text('# Historique des livraisons — Programme Riemann\n\n*Texte des README successifs, conservé tel quel (de la plus récente à la plus ancienne). Chaque section décrit l’état de sa date. Le README courant ne garde que l’entrée du corpus.*\n\n---\n\n' + old, encoding='utf-8-sig')
    L = [f'# Programme Riemann — {V}', '',
         f'*{DATE_FR}. Un programme de recherche personnel sur l’hypothèse de Riemann (RH), conservé comme un corpus versionné : documents, preuves, code, données et tests. Auteur : Vincent P. P. NOËL (Strasbourg). Travail mené avec l’aide de ChatGPT (OpenAI) et de Claude (Anthropic) ; l’auteur assume la responsabilité finale du contenu.*', '',
         '*English: [README_EN.md](README_EN.md).*', '',
         '## À lire d’abord', '', '**' + pts['etat'] + '**', '']
    for i, pt in enumerate(pts['points'], 1):
        liens = ' · '.join(f'[{a}]({b})' for a, b in pt['liens'])
        L += [f'**{i}. {pt["titre"]}** — *{pt["statut"]}*', '', pt['texte'], '', '→ ' + liens, '']
    L += ['**Précautions de lecture**', ''] + ['- ' + x for x in pts['precautions']] + ['']
    L += [f'## Ce qui change en {V}', ''] + CHANGES + ['', '## Où aller', '']
    L += ['- [' + a + '](' + b + ')' for a, b in pts['outils']] + ['']
    L += ['## Organisation', '',
          '| Dossier | Contenu |', '|---|---|',
          '| `1_Presentation/` | les documents numérotés (texte, PDF, pages), les articles, le dossier de relecture |',
          '| `2_Methode/` | pilotage (indicateur, navigateur, graphe, Bellman), sources, figures, matrice, outils de construction |',
          '| `3_Preuves_et_calculs/` | preuves, programmes, données, prévisions, tests (`python tests/run_all_tests.py`) |',
          '| `4_Archives/` | originaux reçus et archivés, états antérieurs ; jamais modifiés |',
          '| `4_Exports/` | compléments ZIP livrés séparément |',
          '| racine | portail, graphe des idées, liste des figures, inventaires de récupération et d’intégrité, licences |', '',
          '## Reproduire et vérifier', '',
          'Python 3.12 ou plus récent, avec `numpy`, `scipy`, `pandas`, `matplotlib`, `mpmath`, `sympy` et `python-docx` (voir `requirements.txt`).', '',
          '```bash', 'pip install -r requirements.txt', 'cd 3_Preuves_et_calculs && python tests/run_all_tests.py && cd ..',
          'python -B 2_Methode/Outils/' + REPRO, 'python -B 2_Methode/Outils/integrate_v655.py --rebuild',
          'python -B 2_Methode/Pilotage/verify_contracts.py', 'python -B 2_Methode/Pilotage/verify_pilotage.py',
          'sha256sum -c CHECKSUMS.sha256', '```', '',
          'Les fichiers `.md` du corpus portent la marque UTF-8 (BOM), sauf les originaux reçus ou archivés, conservés à l’octet près. La méthode de recherche reste celle du protocole convenu ; toute modification de méthode exige une proposition et l’accord préalable de l’auteur.', '',
          '## Licences', '',
          '- **Code** (`*.py`, `*.js`, scripts de construction) : licence MIT, voir `LICENSE`.',
          '- **Textes, figures et données** : Creative Commons Attribution 4.0 International (CC BY 4.0), voir `LICENSE-CC-BY-4.0.md`.',
          '- © 2026 Vincent P. P. NOËL. Pour citer ce travail, voir `CITATION.cff`.', '',
          '## English summary', '',
          'A personal research programme on the Riemann Hypothesis, kept as a versioned corpus (mostly in French). **No proof of RH is claimed.** The main proved statements are written up in English in `1_Presentation/articles/`: (A) the growth exponent of a mean square Q(X) built from c = Λ∗Λ − Λ·log + 2γΛ equals 2(Θ − ½); (B) under RH, Q(X) ∼ (S/3)(log X)³, and the constant equals 4κ/3 if and only if all zeros are simple. Weil positivity is certified on all admissible test functions for supports up to 11/20 (documents 71–75). In the function-field model, the sign comes neither from point counts nor from isogeny degrees but from a square (Rosati positivity); ζ already satisfies the first two levels (document 80). None of this has been refereed yet. Code: MIT. Texts, figures and data: CC BY 4.0.', '']
    (ROOT / 'README.md').write_text('\n'.join(L), encoding='utf-8-sig')


def NDOCS():
    return len({f.name[:2] for f in PRES.glob('[0-9][0-9]_*') if f.suffix in ('.md', '.pdf', '.html', '.docx')})


THEMES_EN = ["I. Starting point: the energy Q and the first texts", "II. The V6 instruments and their audit",
             "III. What RH requires: families, reduced model, Euler archipelago", "IV. From primes to the continuum: operators, thresholds, encounters",
             "V. The virtual surface and the square", "VI. Weil positivity: certificates, bridges and obligations", "VII. Tools, governance and reviews"]


def readme_en():
    E = rd('2_Methode/Pilotage/points_d_attention.json'); pts = E['en']; order = [p['id'] for p in E['points']]
    L = [f'# Riemann Programme — {V} (English entry)', '',
         '*17 October 2026. A personal research programme on the Riemann Hypothesis (RH), kept as a versioned corpus of documents, proofs, code, data and tests. Author: Vincent P. P. NOËL (Strasbourg). The work was carried out with the help of ChatGPT (OpenAI) and Claude (Anthropic); the author takes final responsibility for the content. Most research documents are in French ([README.md](README.md)); this entry layer, the three papers, the specialist review file and ' + EN_DOCS + ' are in English.*', '',
         '## Read first', '', '**' + pts['etat'] + '**', '']
    for i, k in enumerate(order, 1):
        pt = pts['points'][k]
        L += [f'**{i}. {pt["titre"]}** — *{pt["statut"]}*', '', pt['texte'], '', '→ ' + ' · '.join(f'[{a}]({b})' for a, b in pt['liens']), '']
    L += ['**Reading precautions**', ''] + ['- ' + x for x in pts['precautions']] + ['']
    L += [f'## What changed in {V}', ''] + CHANGES_EN + ['', '## Where to go', ''] + [f'- [{a}]({b})' for a, b in pts['outils']] + ['']
    L += ['## The corpus at a glance', '', f'The {NDOCS()} numbered documents (in French) are grouped in seven questions in [PLAN_DU_CORPUS.md](PLAN_DU_CORPUS.md):', '']
    for (titre, _, keys), en in zip(THEMES, THEMES_EN):
        nums = [k for k in keys if k.isdigit()]
        extra = [k for k in keys if not k.isdigit()]
        L.append(f'- **{en}**: documents ' + ', '.join(str(int(k)) for k in nums) + (' and the essays on amplification, correlations and paths' if extra else '') + '.')
    L += ['', '## Reproduce and verify', '',
          'Python 3.12 or later with `numpy`, `scipy`, `pandas`, `matplotlib`, `mpmath`, `sympy` and `python-docx` (see `requirements.txt`).', '',
          '```bash', 'pip install -r requirements.txt', 'cd 3_Preuves_et_calculs && python tests/run_all_tests.py && cd ..',
          'python -B 2_Methode/Outils/' + REPRO, 'python -B 2_Methode/Outils/integrate_v655.py --rebuild',
          'python -B 2_Methode/Pilotage/verify_contracts.py', 'python -B 2_Methode/Pilotage/verify_pilotage.py',
          'sha256sum -c CHECKSUMS.sha256', '```', '',
          '## Licences', '',
          '- **Code**: MIT licence, see `LICENSE`.',
          '- **Texts, figures and data**: Creative Commons Attribution 4.0 International (CC BY 4.0), see `LICENSE-CC-BY-4.0.md`.',
          '- © 2026 Vincent P. P. NOËL. To cite this work, see `CITATION.cff`.', '']
    (ROOT / 'README_EN.md').write_text('\n'.join(L), encoding='utf-8-sig')


def outils_de_lecture():
    import importlib.util
    spec = importlib.util.spec_from_file_location('outils_lecture', ROOT / '2_Methode/Outils/build_outils_de_lecture.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.tout()


if __name__ == '__main__':
    registre(); navigateur(); pilotage(); indicateur(); plan(); readme(); readme_en(); outils_de_lecture()
    print(json.dumps(dict(version=V, documents_ajoutes=[80, 81], coups_ajoutes=[c['id'] for c in COUPS], plan='PLAN_DU_CORPUS.md', readme='README.md'), ensure_ascii=False))
