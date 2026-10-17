"""Ciblage en lecture seule : recommandations motivées et fiches de tâche proposées.

python -B 2_Methode/Pilotage/ciblage.py                    # rapport JSON, aucun fichier modifié
python -B 2_Methode/Pilotage/ciblage.py --actualiser-vues  # reconstruit les quatre vues et data/ciblage_courant.json

Aucun calcul mathématique n'est lancé ; aucun fait, niveau, statut ou coût n'est écrit.
Les empreintes de référence sont celles du registre unique du pilotage
(`reviewed_source_hashes` dans pilotage_recherche.json) ; ciblage_contrats.json ne déclare que
les chemins lus. La procédure complète (fiches, rôles, dépôt, vérification, décision) est dans
CIBLAGE.md ; les fiches sont gérées par taches.py.

Origine : couche « ciblage automatique » du 16 octobre 2026 (branche V6.58-ciblage), fusionnée en
V6.59 dans la méthode unique du corpus. Auteur : Vincent NOËL.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, importlib.util, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CONFIG = '2_Methode/Pilotage/pilotage_recherche.json'
CONTRATS = '2_Methode/Pilotage/ciblage_contrats.json'
STATUTS_CLOS = {'cloture_documentaire', 'clos', 'refute', 'demontre', 'certifie', 'abandonne'}


def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def module(name, p):
    s = importlib.util.spec_from_file_location(name, p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def dependencies(root, paths, reviewed):
    """Compare les fichiers lus au registre unique des empreintes revues.
    Un fichier absent, non revu ou modifié rend la pièce « à revérifier » ; CSS et menus ne sont pas déclarés."""
    changed, missing, unreviewed = [], [], []
    for path in paths:
        p = Path(root) / path
        if not p.is_file(): missing.append(path)
        elif path not in reviewed: unreviewed.append(path)
        elif sha(p) != reviewed[path]: changed.append(path)
    return dict(changed=changed, missing=missing, unreviewed=unreviewed, unchanged=not (changed or missing or unreviewed))


def scalar_targets(data):
    """Portée scalaire finie seulement ; une borne suffisante négative reste une indécision."""
    leaves = sorted(data.get('leaves', []), key=lambda x: F(x['u_a']))
    contiguous = bool(leaves) and F(leaves[0]['u_a']) == 0 and F(leaves[-1]['u_b']) == 1
    contiguous = contiguous and all(F(a['u_b']) == F(b['u_a']) for a, b in zip(leaves, leaves[1:]))
    valid = []
    for row in leaves:
        margin = F(row['endpoint_margin_exact']); B = F(row['B_upper_exact']); w = F(row['width_upper_exact']); g = F(row['lower_bound_exact'])
        valid.append(B >= 0 and w > 0 and g == margin - B * w * w / 8 and g > 0)
    actions = []
    for n, pair in enumerate(data.get('unresolved', [])):
        actions.append(dict(id='cellule-' + str(n), type='preciser_cellule', cell=pair,
                            reason='Cellule non conclue ; fournir ses marges de bord, leur incertitude et la dette de courbure avant de choisir précision ou subdivision.'))
    for pair in data.get('negative_witnesses', []):
        actions.append(dict(id='temoin-' + str(len(actions)), type='verifier_temoin', cell=pair,
                            reason='Rejouer indépendamment le témoin négatif déclaré ; aucune conclusion globale automatique.'))
    closed = contiguous and all(valid) and not actions and data.get('finite_scalar_window_certified') is True
    return dict(object_type='signal_scalaire', domain=data.get('window', 'non renseigné'), closed_in_declared_window=closed,
                cells=len(leaves), actions=actions, finite_only=True,
                reason='Fenêtre déjà certifiée : ne pas ajouter de subdivisions comme nouvelle portée.' if closed else 'Couverture ou gardes à compléter ; aucune fermeture du signe global.',
                proof_promotions=[])


def local_choice(lower, upper, debt):
    """Contrat d'un adaptateur qui fournit des bornes de bord scalaires, dans les mêmes unités que la dette."""
    lower, upper, debt = map(F, (lower, upper, debt))
    if lower > upper or debt < 0: raise ValueError('bornes ordonnées et dette non négative requises')
    if upper < 0: return 'verifier_temoin'
    if lower - debt > 0: return 'conserver_cellule'
    if upper - debt > 0: return 'raffiner_precision'
    return 'subdiviser_ou_ameliorer_garde'


def attested(a):
    """Un prérequis n'est satisfait que par une issue positive déclarée avec sa portée complète.
    Close par réfutation, ou « démontré » sans portée, il reste bloquant. La preuve elle-même n'est pas vérifiée ici."""
    outcome = a.get('validated_outcome', {})
    return (a.get('status') in ('demontre', 'certifie') and isinstance(outcome, dict) and outcome.get('established') is True
            and all(outcome.get(k) for k in ('object_type', 'domain', 'norm', 'quantifiers', 'source')))


def investigation_targets(config):
    inv = {a['id']: a for a in config['investigations']}
    rows = []
    for a in config['investigations']:
        missing = [k for k in a.get('requires', []) if k not in inv or not attested(inv[k])]
        rows.append(dict(id=a['id'], label=a['label'], question=a['question'], nodes=a['nodes'], source=a['source'],
                         witness=a.get('witness'), output=a.get('output'), requires=a.get('requires', []),
                         missing_prerequisites=missing, status=a['status'], subtasks_executed=a.get('not_executed') is False,
                         kind='investigation', script=None, cost=None, bellman_mapping=None,
                         bellman_status='Hors modèle : aucun coût ni contrat équivalent explicitement lié.',
                         ready_for_formulation=not missing and a['status'] == 'ouvert', refutation=a['refutation']))
    return rows


def fiches_proposees(report, config):
    """Traduit le rapport en fiches de tâche au format commun (voir CIBLAGE.md, § 3).
    La clé `cle` rend la création idempotente ; aucune fiche n'est écrite ici."""
    out = []
    for r in report['calculation_requests']:
        out.append(dict(cle='calcul:' + r['id'], genre='calcul', role='numerique', titre=r['type'].replace('_', ' '),
                        question=r['reason'], objet=report['scalar']['object_type'], domaine=report['scalar']['domain'],
                        entrees=list(read(ROOT / CONTRATS)['evidence']['scalar']['lire']),
                        commande=None, sortie_attendue='Bilan détaillé de la cellule (marges de bord, incertitude, dette de courbure) au format du contrat.',
                        critere_rejet='Bilan incomplet ou unités incohérentes : la cellule reste non conclue.', temoin=None, budget=None, noeuds=[]))
    for c in report['bellman']['choices']:
        if c['id'] == 'STOP': continue
        out.append(dict(cle='bellman:' + c['id'], genre='lier_instance', role='coordinateur', titre=c['label'],
                        question=f"Lier une instance exécutable à l'étude Bellman « {c['label']} » : objet, domaine, entrées avec empreintes, commande bornée, issues possibles et vérificateur.",
                        objet='contrat d’étude', domaine=c.get('scope', ''), entrees=['2_Methode/Pilotage/bellman_contrats_v643.json'], commande=None,
                        sortie_attendue='Contrat d’exécution complet, soumis à l’auteur ; aucun lancement.',
                        critere_rejet=f"Aucune instance réalisable dans la durée déclarée ({c['duration']} lots H) : l'étude reste hors exécution.",
                        temoin=None, budget=c['duration'], noeuds=c.get('nodes', [])))
    for a in report['theoretical_front']:
        out.append(dict(cle='investigation:' + a['id'], genre='investigation', role='explorateur', titre=a['label'],
                        question=a['question'], objet=None, domaine='celui de la question ; à préciser dans la prévision',
                        entrees=[a['source']], commande=None, sortie_attendue=a['output'], critere_rejet=a['refutation'],
                        temoin=a['witness'], budget=None, noeuds=a['nodes']))
    return out


def analyse(root=ROOT, state=None):
    root = Path(root)
    c = state or read(root / CONFIG)
    try: reviewed = read(root / CONFIG)['reviewed_source_hashes']
    except (OSError, ValueError, KeyError): reviewed = {}
    contrats = read(root / CONTRATS)
    audits = {key: dependencies(root, v['lire'], reviewed) for key, v in contrats['evidence'].items()}

    def result(key):
        try: return read(root / contrats['evidence'][key]['resultat'])
        except (OSError, ValueError) as exc:
            audits[key]['read_error'] = type(exc).__name__; audits[key]['unchanged'] = False
            return {}
    scalar = scalar_targets(result('scalar'))
    if not audits['scalar']['unchanged']:
        scalar['closed_in_declared_window'] = False
        scalar['actions'] = [dict(id='relecture-signal', type='reverifier_dependances',
                                  reason='Dépendance absente, non revue, modifiée ou illisible ; conserver les pièces disponibles et réconcilier leur validation.')]
        scalar['reason'] = 'Ciblage bloqué sur cette pièce documentaire ; ne pas réattribuer automatiquement un certificat.'
    matrix = result('matrix')
    diag = dict(object_type='compression_matricielle_finie', certified=audits['matrix']['unchanged'] and matrix.get('certified') is True,
                zero_data_used=matrix.get('zero_data_used'), infinite_tail_certified=False,
                recommendation='Conserver les termes croisés et établir un contrat de dette/erreur sur le complément requis. Le rapport de phases ne mesure pas une proximité de RH.',
                source=contrats['evidence']['matrix']['resultat'])
    if not audits['matrix']['unchanged']: diag['recommendation'] = 'Dépendance absente, non revue, modifiée ou illisible : réévaluer le diagnostic avant réemploi.'
    # Même moteur de scénarios que le navigateur : aucune préférence, coût ou probabilité ajoutés.
    decisions = c.get('decisions')
    if decisions is None:
        e = module('ciblage_engine', root / '2_Methode/Pilotage/engine.py'); decisions = []
        for profile, weights in c['bellman']['profiles'].items():
            for mode in ['lower', 'upper']:
                d = e.solve(e.apply_weight_profile(c['bellman'], weights), c['bellman']['default_budget'], mode,
                            facts=c['bellman_state']['facts'], completed=c['bellman_state']['completed'])
                decisions.append(dict(profile=profile, **d))
    budget = c['bellman']['default_budget']; selected = [d for d in decisions if d['budget'] == budget and d['mode'] == 'lower']
    action_by = {a['id']: a for a in c['bellman']['actions']}; choices = []
    for d in selected:
        for k in d['first_choices']:
            if any(x['id'] == k for x in choices): continue
            if k == 'STOP': choices.append(dict(id=k, label='STOP dans ce scénario', duration=None, machine_ready=False,
                                                reason='La valeur du scénario ne justifie pas une autre étude à ces réglages ; le verrou global reste ouvert.'))
            else:
                a = action_by[k]; choices.append(dict(id=k, label=a['label'], duration=a['duration'], scope=a['scope'], machine_ready=False,
                                                      reason='Étude déclarée par Bellman ; instance et programme non liés. Aucun lancement automatique.', nodes=a['nodes']))
    theoretical = investigation_targets(c)
    relevant_edges = [dict(source=e['source'], target=e['target'], kind=e['kind'], requires=e.get('requires', [])) for e in c['edges'] if e['target'] == 'weil_all']
    observed = {p: sha(root / p) for x in contrats['evidence'].values() for p in x['lire'] if (root / p).is_file()}
    control = {k: c[k] for k in ['bellman', 'bellman_state', 'investigations', 'edges']}
    decision_hash = hashlib.sha256((json.dumps(observed, sort_keys=True) + json.dumps(control, sort_keys=True, ensure_ascii=False)).encode()).hexdigest()
    report = dict(schema='ciblage_v2', decision_snapshot=decision_hash, version=c['version'], mode='recommandations_en_lecture_seule',
                  source_snapshot=hashlib.sha256(json.dumps(observed, sort_keys=True).encode()).hexdigest(),
                  scientific_state_modified=False, indicator_levels_modified=False, proof_promotions=[], automatic_execution=False,
                  provenance_note=contrats['provenance_note'], dependency_audits=audits, scalar=scalar, matrix=diag,
                  bellman=dict(budget=budget, choices=choices, scope='Sept contrats du document 67 ; les investigations restent hors modèle sans raccord explicite.'),
                  theoretical_front=[a for a in theoretical if a['ready_for_formulation']], investigations=theoretical,
                  graph_obligations=relevant_edges, graph_links_are_proofs=False, calculation_requests=scalar['actions'], executable_actions=[],
                  next_theoretical_result='Une inégalité candidate sur les vrais poids premiers, avec bords, norme, dette, dépendance au support et témoin de rejet. Son test global attend les prérequis déclarés.',
                  inputs=observed)
    report['fiches_proposees'] = fiches_proposees(report, c)
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--actualiser-vues', action='store_true', help='Recalculer le ciblage et les vues existantes, sans exécuter de programme scientifique.')
    a = p.parse_args()
    if a.actualiser_vues: module('ciblage_builder', HERE / 'build_pilotage.py').build_all()
    else: print(json.dumps(analyse(), ensure_ascii=False, indent=2))
