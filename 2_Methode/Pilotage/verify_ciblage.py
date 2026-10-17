"""Contrôles adverses du ciblage et des fiches de tâche ; aucun calcul mathématique n'est rejoué.

python -B 2_Methode/Pilotage/verify_ciblage.py
Repris de la branche ciblage du 16 octobre 2026 et étendu en V6.59 aux fiches de tâche (taches.py).
Les contrôles valident le raccord logique et les règles de répartition, pas la loi de signe de Weil.
"""
from pathlib import Path
from copy import deepcopy
import importlib.util, json, tempfile, shutil, sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


m = load('ciblage_test', 'ciblage.py')
T = load('taches_test', 'taches.py')

LECTURE = ['2_Methode/Pilotage/pilotage_recherche.json', '2_Methode/Pilotage/ciblage_contrats.json', '2_Methode/Pilotage/engine.py',
           '2_Methode/Pilotage/ciblage.py', '2_Methode/Pilotage/taches.py', '2_Methode/Pilotage/bellman_contrats_v643.json']


def copie_minimale(dest, avec_resultats=True):
    fichiers = list(LECTURE)
    if avec_resultats:
        c = m.read(ROOT / m.CONTRATS)
        fichiers += [p for e in c['evidence'].values() for p in e['lire']]
        inv = m.read(ROOT / m.CONFIG)['investigations']
        fichiers += [a['source'] for a in inv]
    for rel in dict.fromkeys(fichiers):
        d = dest / rel; d.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / rel, d)
    (dest / '2_Methode/Pilotage/taches.json').write_text(json.dumps(dict(schema='taches_v1', version='test', auteurs=['auteur:a'], taches=[])), encoding='utf-8')


def main():
    checks = []

    def ck(name, ok):
        assert ok, name
        checks.append(dict(name=name, passed=True))

    def refuse(name, fn):
        try: fn()
        except T.Refus: checks.append(dict(name=name, passed=True)); return
        raise AssertionError(name)

    # ------------------------------------------------------------ ciblage (contrôles de la branche du 16 octobre)
    c = m.read(HERE / 'pilotage_recherche.json'); before = json.dumps(c, sort_keys=True)
    r = m.analyse(ROOT)
    ck('44 cellules closes : pas de raffinement automatique', r['scalar']['closed_in_declared_window'] and not r['calculation_requests'] and r['scalar']['cells'] == 44)
    ck('demande de calcul distincte de programme exécutable', r['executable_actions'] == [])
    ck('aucune promotion scientifique', not r['proof_promotions'] and not r['scientific_state_modified'] and not r['indicator_levels_modified'])
    ck('borne négative seule : indécision, pas témoin', m.local_choice('1', '1', '2') == 'subdiviser_ou_ameliorer_garde')
    ck('incertitude de bord décisive : précision', m.local_choice('0', '2', '1') == 'raffiner_precision')
    ck('valeur négative : vérification indépendante', m.local_choice('-2', '-1', '0') == 'verifier_temoin')
    ck('contact nul : aucune certification forcée', m.local_choice('0', '0', '0') != 'conserver_cellule')
    targets = m.investigation_targets(c); t = next(x for x in targets if x['id'] == 'test_paquets')
    ck('sous-tâches exécutées ne ferment pas ET', set(t['missing_prerequisites']) == {'signe_paquets', 'duale_schur'})
    cc = deepcopy(c)
    a = next(a for a in cc['investigations'] if a['id'] == 'signe_paquets'); a['status'] = 'clos'; a['outcome'] = 'refute'
    t = next(x for x in m.investigation_targets(cc) if x['id'] == 'test_paquets')
    ck('piste close par réfutation ne prouve pas un prérequis', 'signe_paquets' in t['missing_prerequisites'])
    a['status'] = 'demontre'
    t = next(x for x in m.investigation_targets(cc) if x['id'] == 'test_paquets')
    ck('statut sans portée positive reste bloquant', 'signe_paquets' in t['missing_prerequisites'])
    a['validated_outcome'] = dict(established=True, object_type='fixture', domain='fixture', norm='fixture', quantifiers='fixture', source='fixture')
    t = next(x for x in m.investigation_targets(cc) if x['id'] == 'test_paquets')
    ck('un seul prérequis fermé : ET encore bloqué', t['missing_prerequisites'] == ['duale_schur'])
    ck('coût absent reste absent', all(x['cost'] is None for x in targets))
    ck('liens graphiques ne deviennent pas faits', r['graph_links_are_proofs'] is False)
    ck('front = investigations ouvertes sans prérequis manquant', {x['id'] for x in r['theoretical_front']} == {x['id'] for x in targets if x['status'] == 'ouvert' and not x['missing_prerequisites']})
    with tempfile.TemporaryDirectory() as d:
        p = Path(d); (p / 'science.py').write_text('a=1'); (p / 'style.css').write_text('x')
        reviewed = {'science.py': m.sha(p / 'science.py')}
        (p / 'style.css').write_text('y'); ck('CSS changé : résultat scientifique intact', m.dependencies(p, ['science.py'], reviewed)['unchanged'])
        (p / 'science.py').write_text('a=2'); ck('code mathématique changé : à revérifier', not m.dependencies(p, ['science.py'], reviewed)['unchanged'])
        ck('fichier hors registre unique : à revérifier', m.dependencies(p, ['style.css'], reviewed)['unreviewed'] == ['style.css'])
    ck('registre unique : toutes les dépendances lues ont une empreinte revue', all(a['unchanged'] for a in r['dependency_audits'].values()))
    ck('lecture seule de l’état', json.dumps(c, sort_keys=True) == before)
    ck('Bellman courant : noyaux sans autolancement', [x['id'] for x in r['bellman']['choices']] == ['noyaux'] and all(not x['machine_ready'] for x in r['bellman']['choices']))
    with tempfile.TemporaryDirectory() as d:
        p = Path(d); copie_minimale(p, avec_resultats=False)
        missing = m.analyse(p)
        ck('résultats absents : blocage expliqué sans exception', not missing['scalar']['closed_in_declared_window'] and missing['calculation_requests'][0]['type'] == 'reverifier_dependances' and not missing['matrix']['certified'])
    cc = deepcopy(c); cc['bellman']['default_budget'] = 0
    stop = m.analyse(ROOT, cc)
    ck('STOP budgétaire ne ferme pas la recherche', all(a['id'] == 'STOP' for a in stop['bellman']['choices']) and bool(stop['theoretical_front']) and not stop['proof_promotions'])
    ck('fiches proposées complètes', all(all(f.get(k) for k in T.OBLIGATOIRES) for f in r['fiches_proposees']))

    # ------------------------------------------------------------ fiches de tâche : cycle complet dans une copie
    with tempfile.TemporaryDirectory() as d:
        p = Path(d); copie_minimale(p)
        R = T.Registre(p)
        crees = R.ouvrir('ia:coordination')
        ck('ouvrir crée une fiche par proposition', len(crees) == len(r['fiches_proposees']))
        ck('ouvrir est idempotent', T.Registre(p).ouvrir('ia:coordination') == [])
        R = T.Registre(p); ident = next(t['id'] for t in R.data['taches'] if t['genre'] == 'investigation')
        refuse('acteur sans type refusé', lambda: R.assigner(ident, 'claude', 'ia:coordination'))
        R.assigner(ident, 'ia:explorateur-1', 'ia:coordination')
        refuse('dépôt sans prévision refusé', lambda: R.deposer(ident, 'ia:explorateur-1', 'mesure'))
        refuse('prévision par un autre acteur refusée', lambda: R.prevoir(ident, 'ia:autre', 'Je prévois un résultat mesurable et réfutable ici.'))
        R.prevoir(ident, 'ia:explorateur-1', 'Prévision : obstacle documenté ; réfutée si une borne positive apparaît.')
        refuse('dépôt sans RAPPORT.md refusé', lambda: R.deposer(ident, 'ia:explorateur-1', 'obstacle'))
        dep = p / T.DEPOT / ident; dep.mkdir(parents=True)
        (dep / 'RAPPORT.md').write_text('## Prévision\n## Méthode\n## Résultat\n', encoding='utf-8')
        refuse('RAPPORT.md incomplet refusé', lambda: R.deposer(ident, 'ia:explorateur-1', 'obstacle'))
        (dep / 'RAPPORT.md').write_text('\n'.join(T.TITRES_RAPPORT) + '\n', encoding='utf-8')
        refuse('statut hors vocabulaire refusé', lambda: R.deposer(ident, 'ia:explorateur-1', 'prouve'))
        refuse('dépôt par un acteur non assigné refusé', lambda: R.deposer(ident, 'agent:x', 'obstacle'))
        R.deposer(ident, 'ia:explorateur-1', 'obstacle')
        (dep / 'verification').mkdir(); (dep / 'verification' / 'VERIFICATION.md').write_text('contrôles', encoding='utf-8')
        refuse('producteur ne vérifie pas son propre dépôt', lambda: R.verifier(ident, 'ia:explorateur-1', 'conforme', 'Rejoué et confronté au critère de rejet.'))
        (dep / 'ajout.txt').write_text('modifié après dépôt', encoding='utf-8')
        refuse('dépôt modifié après enregistrement refusé', lambda: R.verifier(ident, 'agent:audit', 'conforme', 'Rejoué et confronté au critère de rejet.'))
        (dep / 'ajout.txt').unlink()
        refuse('acceptation avant vérification refusée', lambda: R.decider(ident, 'auteur:a', 'acceptee', ''))
        R.verifier(ident, 'agent:audit', 'conforme', 'Rejoué et confronté au critère de rejet écrit avant.')
        refuse('décision par un non-auteur refusée', lambda: R.decider(ident, 'ia:explorateur-1', 'acceptee', ''))
        refuse('auteur non déclaré refusé', lambda: R.decider(ident, 'auteur:inconnu', 'acceptee', ''))
        R.decider(ident, 'auteur:a', 'acceptee', 'Accepté dans sa portée.')
        refuse('intégration d’une pièce restée dans le dépôt refusée', lambda: R.integrer(ident, 'ia:rapporteur', [str((dep / 'RAPPORT.md').relative_to(p))]))
        R.integrer(ident, 'ia:rapporteur', ['2_Methode/Pilotage/ciblage.py'])
        ck('cycle complet : intégrée', R.tache(ident)['statut'] == 'integree')
        ck('contrôle de cohérence sans erreur', T.Registre(p).controler() == [])
        R = T.Registre(p); R.ouvrir('ia:coordination'); R = T.Registre(p)
        cle = R.tache(ident)['cle']
        ck('nouveau cycle après intégration', any(t['cle'] == cle and t['cycle'] == 2 for t in R.data['taches']))
        # une entrée modifiée rend la fiche périmée
        autre = next(t for t in R.data['taches'] if t['statut'] == 'ouverte' and t['genre'] == 'investigation')
        R.assigner(autre['id'], 'ia:explorateur-2', 'ia:coordination')
        R.prevoir(autre['id'], 'ia:explorateur-2', 'Prévision écrite avant : borne candidate ou obstacle documenté.')
        src = p / next(c for c in autre['entrees'] if c.startswith('1_Presentation'))
        src.write_bytes(src.read_bytes() + b'\n')
        d2 = p / T.DEPOT / autre['id']; d2.mkdir(parents=True); (d2 / 'RAPPORT.md').write_text('\n'.join(T.TITRES_RAPPORT), encoding='utf-8')
        refuse('entrée modifiée : fiche périmée', lambda: R.deposer(autre['id'], 'ia:explorateur-2', 'mesure'))
        ck('statut périmée enregistré', T.Registre(p).tache(autre['id'])['statut'] == 'perimee')
        # journal chaîné : une altération est détectée
        J = json.loads((p / T.JOURNAL).read_text(encoding='utf-8'))
        J['evenements'][1]['par'] = 'ia:falsifie'; (p / T.JOURNAL).write_text(json.dumps(J, ensure_ascii=False), encoding='utf-8')
        ck('journal altéré : chaîne rompue détectée', any('chaîne rompue' in e for e in T.Registre(p).controler()))
        brief = T.Registre(p).fiche(ident, verification=True)
        ck('consigne de vérification à l’aveugle', 'ia:explorateur-1' not in brief and 'Critère de rejet' in brief)
    # le registre réel du corpus est cohérent
    ck('registre du corpus cohérent', T.Registre(ROOT).controler() == [])
    print(json.dumps(dict(checks=checks, passed=len(checks), RH_proved=False), ensure_ascii=False, indent=2))
    return checks


if __name__ == '__main__':
    main()
