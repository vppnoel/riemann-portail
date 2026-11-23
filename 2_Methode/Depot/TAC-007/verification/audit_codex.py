#!/usr/bin/env python3
"""Audit complémentaire TAC-007, Codex (ia:chatgpt-sol-6.1-max).

python -B 2_Methode/Depot/TAC-007/verification/audit_codex.py --rejeu /copie/du/corpus
Les scripts p1, p2, p3 sont exécutés dans cette copie, p1_resultats.json
supprimé avant p1 pour désactiver la reprise depuis les résultats enregistrés.
Les sources du producteur ne sont pas modifiées par cet audit.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import platform
import sys
import numpy as np
import mpmath as mp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKS = []


def check(label, ok, **details):
    CHECKS.append(dict(controle=label, ok=bool(ok), **details))


def numeric_string(value):
    try: return mp.mpf(value)
    except (ValueError, TypeError): return None


def compare(a, b, path=''):
    if isinstance(a, dict):
        keys = [k for k in a if k not in ('secondes', 'duree_secondes')]
        check(path+':cles', all(k in b for k in keys))
        for k in keys: compare(a[k], b[k], path+'/'+k)
    elif isinstance(a, list):
        check(path+':taille', len(a) == len(b))
        for i, (x, y) in enumerate(zip(a, b)): compare(x, y, path+'/'+str(i))
    elif isinstance(a, (int, float, str)):
        x, y = numeric_string(a), numeric_string(b)
        if x is None:
            check(path, a == b)
        else:
            # Les résidus ~10^-50 sont des bruits, pas des bornes certifiées.
            absolute = mp.mpf('1e-25') if path.endswith('ecart_max') else mp.mpf('1e-40')
            check(path, abs(x-y) <= max(absolute, abs(x)*mp.mpf('5e-9')),
                  original=a, rejeu=b)


def det(matrix):
    if not matrix: return F(1)
    return sum(((-1)**j * matrix[0][j] * det([row[:j]+row[j+1:] for row in matrix[1:]])
                for j in range(len(matrix))), F(0))


def cf_restriction_exacte(counts, genus, M, parity):
    """Congruence rationnelle, différente du Householder multiprécision.

    Base q^(k/2)(delta_k +/- delta_-k) ; la contrainte du pôle a pour
    coefficients q^k +/- 1. Après élimination d'une coordonnée, tous les
    mineurs principaux sont rationnels. La positivité est donc décidée
    exactement, y compris quand la plus petite valeur est zéro.
    """
    q = 5
    ks = list(range(parity, M+1)); sg = 1 if parity == 0 else -1
    size = len(ks)
    if size <= 1: return dict(dimension=0, psd=True, mineurs=[])
    A = [[F(0) for _ in ks] for _ in ks]
    pole = [F(1 if k == 0 else q**k+sg) for k in ks]
    for i, k in enumerate(ks):
        for j, l in enumerate(ks):
            if k == l == 0: value = 2*genus-2
            elif k == 0 or l == 0: value = -2*counts[max(k, l)]
            elif k == l: value = 2*q**k*(2*genus-2)-2*sg*counts[2*k]
            else: value = -2*q**min(k, l)*counts[abs(k-l)]-2*sg*counts[k+l]
            A[i][j] = F(value)
    E = [[-pole[j+1]/pole[0] for j in range(size-1)]]
    E += [[F(i == j) for j in range(size-1)] for i in range(size-1)]
    R = [[sum((E[i][r]*A[i][j]*E[j][c] for i in range(size) for j in range(size)), F(0))
          for c in range(size-1)] for r in range(size-1)]
    minors = []
    for n in range(1, size):
        for selection in itertools.combinations(range(size-1), n):
            minors.append(det([[R[i][j] for j in selection] for i in selection]))
    return dict(dimension=size-1, psd=all(v >= 0 for v in minors),
                mineurs=[str(v) for v in minors], matrice=[[str(v) for v in row] for row in R])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rejeu', type=Path)
    parser.add_argument('--sortie', type=Path, default=HERE/'resultats_audit_codex.json')
    args = parser.parse_args()
    mp.mp.dps = 70
    deposit = ROOT/'2_Methode/Depot/TAC-007'
    registry = json.loads((ROOT/'2_Methode/Pilotage/taches.json').read_text())
    task = next(t for t in registry['taches'] if t['id'] == 'TAC-007')
    for rel, expected_hash in {**task['entrees'], **task['depots'][-1]['fichiers']}.items():
        check('integrite/'+rel, hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() == expected_hash)
    p1 = json.loads((deposit/'p1_resultats.json').read_text())
    p2 = json.loads((deposit/'p2_resultats.json').read_text())
    p3 = json.loads((deposit/'p3_resultats.json').read_text())
    if args.rejeu:
        for name in ('p1_resultats.json', 'p2_resultats.json', 'p3_resultats.json'):
            compare(json.loads((deposit/name).read_text()),
                    json.loads((args.rejeu/'2_Methode/Depot/TAC-007'/name).read_text()), 'rejeu/'+name)
    vals = [mp.mpf(p1[f'N={n} K=48 dps=60 pair']['marge']) for n in (40, 48, 56, 64)]
    check('P1_fourchette', all(mp.mpf('3e-12') <= v <= mp.mpf('6e-12') for v in vals))
    check('P1_decroissance_mesuree', all(a > b for a, b in zip(vals, vals[1:])))
    check('P1_variation_56_64', abs(vals[-1]-vals[-2])/vals[-2] < mp.mpf('.1'))
    cells = mp.mpf(700000)*mp.sqrt(mp.mpf(str(p2['budgets']['quadrature en fréquence (trapèzes)']['valeur']))/mp.mpf('5e-12'))
    check('P2_echelle_cellules', abs(cells/mp.mpf(str(p2['cellules_necessaires_quadrature_seule']))-1) < mp.mpf('1e-14'))
    # Contrôle indépendant de la projection : élimination puis problème
    # généralisé, comparé à la base Householder du programme du corpus.
    spec = importlib.util.spec_from_file_location('zhu_audit', ROOT/'3_Preuves_et_calculs/scripts/run_zhu_reproduction.py')
    z = importlib.util.module_from_spec(spec); spec.loader.exec_module(z)
    mp.mp.dps = 70; N = 12; L = mp.mpf('0.8')
    matrix = mp.matrix(z.weil_matrix(L, 0, N, 64))
    xs, weights = z.nodes(-L, L, 2*N+20)
    a = mp.matrix([mp.fsum(w*z.basis_vals(x, L, list(range(0, 2*N, 2)))[i]*mp.exp(-x/2)
                           for x, w in zip(xs, weights)) for i in range(N)])
    E = mp.matrix(N, N-1)
    for j in range(N-1): E[0, j] = -a[j+1]/a[0]; E[j+1, j] = 1
    gram = E.T*E; chol = mp.cholesky(gram); inv = chol**-1
    reduced = inv*(E.T*matrix*E)*inv.T
    eigenvalues, vectors = mp.eigsy(reduced)
    direct = eigenvalues[0]
    householder = z.noyau_des_moments(L, N, 64, 0)
    residual = mp.norm(reduced*vectors[:, 0]-direct*vectors[:, 0])
    check('projection_elimination_vs_Householder', abs(direct-householder) < mp.mpf('1e-55'),
          ecart=mp.nstr(abs(direct-householder), 8))
    check('moment_annule', mp.norm(a.T*E) < mp.mpf('1e-60'))
    check('residu_spectral_70_chiffres', residual < mp.mpf('1e-60'), valeur=mp.nstr(residual, 8))
    # Le cache de Gauss est indexé seulement par n, pas par la précision.
    z._GL.clear(); mp.mp.dps = 60; nodes60 = list(z.gauss(48)[0])
    mp.mp.dps = 80; cached80 = list(z.gauss(48)[0])
    check('cache_gauss_reutilise_noeuds_60', nodes60 == cached80)
    z._GL.clear(); fresh80 = z.gauss(48)[0]
    cache_error = max(abs(a-b) for a, b in zip(cached80, fresh80))
    check('cache_ecart_loin_sous_marge', cache_error < mp.mpf('1e-55'), ecart=mp.nstr(cache_error, 8))
    # Corps de fonctions : preuve exacte du signe des formes des trois cas.
    counts = {int(k):v for k, v in p3['C2']['courbe']['N_m'].items()}
    direct_n1 = 1+sum((y*y-x*x*x-x-1) % 5 == 0 for x in range(5) for y in range(5))
    check('CF_N1_compte_direct', direct_n1 == counts[1] == 9)
    def genus1(a):
        traces = [2, a]
        for m in range(2, 7): traces.append(a*traces[-1]-5*traces[-2])
        return {m:5**m+1-traces[m] for m in range(1, 7)}
    check('CF_comptes_vs_recurrence', counts == genus1(-3))
    traces4 = [4, 0, -22, 0]
    for m in range(4, 7): traces4.append(-11*traces4[m-2]-25*traces4[m-4])
    fake2 = {m:5**m+1-traces4[m] for m in range(1, 7)}
    cf = {}
    for case, ns, genus in (('vraie', counts, 1), ('faux_genre1', genus1(5), 1), ('faux_genre2', fake2, 2)):
        cf[case] = {}
        for M in (1, 2, 3):
            for parity in (0, 1):
                answer = cf_restriction_exacte(ns, genus, M, parity)
                label = f'M={M} '+('pair' if parity == 0 else 'impair')
                cf[case][label] = answer
                expected = case == 'vraie' or M == 1 or (case == 'faux_genre1' and parity == 0) or (case == 'faux_genre2' and M == 2 and parity == 1)
                check('CF_signe_exact_'+case+'_'+label, answer['psd'] == expected)
    check('C1_validation_chi5', all(mp.mpf(v['ecart_relatif']) < mp.mpf('1e-6') for v in p3['C1_validation_chi5'].values()))
    check('C1_DH_matrices_finies_positives', all(mp.mpf(p3['C1_DH'][f'N={N}']['lambda_min_secteur_pair']) > 0 for N in (32, 48)))
    check('C3_seuil_Lambda2_prevu', mp.mpf(p3['C3']['b_Lambda2']['ecart_relatif']) < mp.mpf('.05'))
    out = dict(acteur='ia:chatgpt-sol-6.1-max', python=platform.python_version(), numpy=np.__version__, mpmath=mp.__version__,
               controles=CHECKS, bilan=dict(reussis=sum(c['ok'] for c in CHECKS), total=len(CHECKS)),
               empreintes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in deposit.iterdir() if p.is_file()},
               projection_independante=dict(N=N, L='0.8', marge=mp.nstr(direct, 20), residu=mp.nstr(residual, 8)),
               cache_gauss=dict(ecart_noeuds_60_contre_80_frais=mp.nstr(cache_error, 8), indexe_par_precision=False),
               corps_fonctions_signes_rationnels=cf,
               limite='P1 et DH : matrices finies et quadratures non certifiées. P2 : modèle de budgets fixé. Aucun minorant sur tout espace.')
    args.sortie.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(out['bilan']), flush=True)
    print(json.dumps(dict(projection=out['projection_independante'], cache=out['cache_gauss'])), flush=True)
    return 0 if all(c['ok'] for c in CHECKS) else 1


if __name__ == '__main__':
    sys.exit(main())
