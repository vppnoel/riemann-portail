#!/usr/bin/env python3
"""Relecture TAC-008 par Codex (ia:chatgpt-sol-6.1-max).

Depuis la racine : python -B 2_Methode/Depot/TAC-008/verification/audit_codex.py
Option --rejeu : copie du corpus dans laquelle les deux scripts du producteur
ont été exécutés, sans reprendre les JSON préexistants.
Ce programme contrôle un calcul fini ; il ne fournit aucun certificat RH.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import platform
import sys
import numpy as np
from scipy.integrate import quad_vec

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKS = []


def check(label, ok, **details):
    CHECKS.append(dict(controle=label, ok=bool(ok), **details))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compare_json(a, b, prefix=''):
    """Tolérance de rejeu binary64, distincte d'une borne mathématique."""
    if isinstance(a, dict):
        check(prefix + ':cles', a.keys() == b.keys())
        for key in a:
            compare_json(a[key], b[key], prefix + '/' + key)
    elif isinstance(a, list):
        check(prefix + ':liste', len(a) == len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            compare_json(x, y, prefix + '/' + str(i))
    elif isinstance(a, (int, float)):
        # Pas d'atol qui masquerait les composantes de taille 10^-14.
        check(prefix, abs(a-b) <= 5e-8 * abs(a) if a else b == 0,
              original=a, rejeu=b)
    else:
        check(prefix, a == b)


def points_independants(p, m):
    """Compte y²=x³+x+1 par histogramme des carrés, sans Euler ni Frobenius.

    Coefficients ascendants et réduction en ordre décroissant : chemin
    indépendant de l'implémentation du producteur de TAC-007.
    """
    import sympy as sp
    x = sp.symbols('x')
    for lower in itertools.product(range(p), repeat=m):
        polynomial = x**m + sum(c*x**i for i, c in enumerate(lower))
        if sp.Poly(polynomial, x, modulus=p).is_irreducible:
            break
    def mul(a, b):
        out = [0]*(2*m-1)
        for i, u in enumerate(a):
            for j, v in enumerate(b):
                out[i+j] = (out[i+j]+u*v) % p
        for degree in range(2*m-2, m-1, -1):
            c = out[degree]
            for i, u in enumerate(lower):
                out[degree-m+i] = (out[degree-m+i]-c*u) % p
        return out[:m]
    def encode(v):
        return sum(c*p**i for i, c in enumerate(v))
    elements = list(itertools.product(range(p), repeat=m))
    squares = np.bincount([encode(mul(v, v)) for v in elements], minlength=p**m)
    count = 1  # point à l'infini
    for v in elements:
        cube = mul(mul(v, v), v)
        rhs = [(a+b) % p for a, b in zip(cube, v)]
        rhs[0] = (rhs[0]+1) % p
        count += int(squares[encode(rhs)])
    return count


def analogue_cf(counts):
    """Euler des points fermés de la courbe sur F5, degrés <= 6.

    B_d points fermés de degré d, coefficient d log q à chaque puissance
    P^k de norme q^(dk). Les normes coïncident pour tous les points d'un
    même degré ; on les agrège pour K total, pas pour sa diagonale.
    """
    q, limit = 5, 6
    closed = {}
    for m in range(1, limit+1):
        value = counts[m]-sum(d*closed[d] for d in closed if m % d == 0)
        check(f'CF:points_fermes_entiers_deg{m}', value % m == 0 and value >= 0)
        closed[m] = value//m
    us = np.arange(2., 8.0001, .25)
    ls = np.arange(1, limit+1)*math.log(q)
    w = np.exp(-.5*((ls[:, None]-us)/.5)**2)
    def parts(T, defect=None):
        aggregate = np.zeros(limit)
        diagonal = np.zeros((len(us), len(us)))
        chain = diagonal.copy()
        psi = T*math.sqrt(2*math.pi)*np.exp(-.5*(T*(ls[:, None]-ls))**2)
        for d, count in closed.items():
            degrees = np.arange(d, limit+1, d)
            exponents = degrees//d
            c = d*math.log(q)*q**(-degrees.astype(float)/2)
            if defect == 'eta1': c[exponents >= 2] *= 2
            if defect == 'phase': c[exponents == 2] *= -1
            aggregate[degrees-1] += count*c
            A = w[degrees-1]*c[:, None]
            diagonal += count*T*math.sqrt(2*math.pi)*(A.T @ A)
            pc = psi[np.ix_(degrees-1, degrees-1)].copy()
            np.fill_diagonal(pc, 0)
            chain += count*A.T @ pc @ A
        A = w*aggregate[:, None]
        total = A.T @ psi @ A
        return total, diagonal, chain, total-diagonal-chain
    result = dict(q=q, degre_max=limit, nombres_points=counts, points_fermes=closed)
    for T in (1., 10.):
        baseline = parts(T)
        norms = [float(np.linalg.norm(v)) for v in baseline[1:]]
        row = dict(parts_normes=[v/sum(norms) for v in norms], defauts={})
        for name in ('eta1', 'phase'):
            changed = parts(T, name)
            distances = [float(np.linalg.norm(a-b)/np.trace(baseline[0]))
                         for a, b in zip(changed[1:], baseline[1:])]
            row['defauts'][name] = dict(distances=distances,
                                      part_croisee=distances[2]/sum(distances))
        result[str(T)] = row
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rejeu', type=Path)
    parser.add_argument('--sortie', type=Path, default=HERE/'resultats_audit_codex.json')
    args = parser.parse_args()
    deposit = ROOT/'2_Methode/Depot/TAC-008'
    registry = json.loads((ROOT/'2_Methode/Pilotage/taches.json').read_text())
    task = next(t for t in registry['taches'] if t['id'] == 'TAC-008')
    for rel, expected_hash in {**task['entrees'], **task['depots'][-1]['fichiers']}.items():
        check('integrite/'+rel, hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() == expected_hash)
    original = json.loads((deposit/'resultats.json').read_text())
    witness = json.loads((deposit/'temoin_negatif.json').read_text())
    if args.rejeu:
        for name in ('resultats.json', 'temoin_negatif.json'):
            a = json.loads((deposit/name).read_text())
            b = json.loads((args.rejeu/'2_Methode/Depot/TAC-008'/name).read_text())
            compare_json(a, b, 'rejeu/'+name)
    dk = load_module('decomposition_verifiee', deposit/'decomposition_K.py')
    zeta, chi = dk.b_of('zeta'), dk.b_of('L_chi5')
    check('coefficients_zeta_Lambda', np.max(np.abs(zeta-dk.Lam)) < 1e-12,
          erreur=float(np.max(np.abs(zeta-dk.Lam))))
    from rejection import chi5
    expected = chi5(dk.NMAX)*dk.Lam
    check('coefficients_chi5', np.max(np.abs(chi-expected)) < 1e-12,
          erreur=float(np.max(np.abs(chi-expected))))
    # Micro-cas : boucle double indépendante et quadrature en t.
    ns = np.array([2, 3, 4, 5, 6, 8, 9, 10])
    bs = np.array([2, 3, 2, 5, 0, 2, 3, 0])
    us = np.array([.7, 1.2, 2.3])
    logs = np.log(ns)
    win = np.exp(-.5*((logs[:, None]-us)/.5)**2)
    c = np.array([1+.2j, -.6j, -.7, .4+.8j, .1, .3j, -.9j, .2])/np.sqrt(ns)
    A = win*c[:, None]
    T = 1.3
    direct = [np.zeros((3, 3), complex) for _ in range(3)]
    for i, n in enumerate(ns):
        for j, m in enumerate(ns):
            component = 0 if i == j else 1 if bs[i] and bs[i] == bs[j] else 2
            weight = T*math.sqrt(2*math.pi)*math.exp(-.5*(T*math.log(n/m))**2)
            direct[component] += weight*np.outer(A[i], A[j].conj())
    # Seules les variables du module chargé en mémoire changent, pas son fichier.
    saved = {k: getattr(dk, k) for k in ('keep', 'Wk', 'lk', 'bk', 'US', 'n')}
    dk.keep, dk.Wk, dk.lk, dk.bk, dk.US, dk.n = ns, win, logs, bs, us, np.arange(11)
    b = np.zeros(11, complex); b[ns] = c*np.sqrt(ns)
    measured = dk.K_parts(b, T)
    for key, value in saved.items(): setattr(dk, key, value)
    for label, a, b in zip(('diag', 'chaine', 'croise'), direct, measured[1:]):
        check('decomposition_double_'+label, np.linalg.norm(a-b) < 1e-12)
    def integrand(t):
        channel = np.exp(-1j*t*logs) @ A
        return np.outer(channel, channel.conj())*math.exp(-.5*(t/T)**2)
    quadrature, error = quad_vec(integrand, -10*T, 10*T, epsabs=1e-11, epsrel=1e-11)
    check('gaussienne_formule_vs_integrale_t', np.linalg.norm(quadrature-measured[0]) < 1e-10,
          erreur=float(np.linalg.norm(quadrature-measured[0])), estimation_quad=float(error))
    check('K_hermitienne', np.linalg.norm(measured[0]-measured[0].conj().T) < 1e-12)
    check('K_positive_micro_cas', np.linalg.eigvalsh(measured[0]).min() > -1e-12)
    # Deux puissances d'un seul premier : la phase de b(p²) change K_chaine
    # avec toute gaussienne de largeur finie. Ce n'est pas une impossibilité d'ordre deux.
    w2 = np.exp(-.5*((np.log([2, 4])[:, None]-np.arange(2, 8.01, .25))/.5)**2)
    a2 = w2*(math.log(2)/np.sqrt([2, 4]))[:, None]
    chain2 = math.sqrt(2*math.pi)*math.exp(-.5*math.log(2)**2)*(np.outer(a2[0], a2[1])+np.outer(a2[1], a2[0]))
    phase_signal = float(2*np.linalg.norm(chain2))
    check('contre_exemple_phase_visible_ordre_deux', phase_signal > 0,
          distance_chaine=phase_signal)
    row = original['T=1']; mean = row['W2_moyenne_chaine_sur_trace']; sd = row['W2_ecart_type_chaine_sur_trace']
    scalar_z = {k:(row[k]['chaine_sur_trace']-mean)/sd for k in ('zeta', 'L_chi5', 'DH')}
    for label, value in scalar_z.items():
        check('ecart_reduit_fini_'+label, math.isfinite(value))
    fractions = {}
    for label, roww in witness['defauts'].items():
        fraction = roww['d_croise']/(roww['d_diag']+roww['d_chaine']+roww['d_croise'])
        fractions[label] = fraction
        if label.startswith('T=1.0'):
            check('temoin_localise_croise_'+label, fraction > .98)
        if label.endswith('phase'):
            check('phase_diag_invariante_'+label, roww['d_diag'] == 0)
    counts = {m:points_independants(5, m) for m in range(1, 7)}
    check('CF_comptes_independants', list(counts.values()) == [9, 27, 108, 675, 3069, 15552])
    cf = analogue_cf(counts)
    out = dict(acteur='ia:chatgpt-sol-6.1-max', python=platform.python_version(), numpy=np.__version__,
               controles=CHECKS, bilan=dict(reussis=sum(c['ok'] for c in CHECKS), total=len(CHECKS)),
               empreintes={f.name:hashlib.sha256(f.read_bytes()).hexdigest()
                           for f in deposit.iterdir() if f.is_file()},
               ecarts_reduits_chaine_sur_trace_contre_W2=scalar_z,
               separation_DH_L_chi5_en_ecarts_types_W2=abs(row['DH']['chaine_sur_trace']-row['L_chi5']['chaine_sur_trace'])/sd,
               W1_W2_T10=dict(ecart_reduit_moyennes=original['T=10']['separations']['z_chaine_W1_contre_W2'],
                              ecart_reduit_tirages=original['T=10']['separations']['z_chaine_W1_contre_W2_tirage_unique']),
               fractions_croisees_somme_des_normes_des_differences=fractions,
               analogue_corps_fonctions=cf,
               limite='Contrôles numériques finis, sans reste certifié ni test universel de multiplicativité.')
    args.sortie.write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(out['bilan']), flush=True)
    print(json.dumps(dict(ecarts_reduits=scalar_z, fractions=fractions), ensure_ascii=False), flush=True)
    return 0 if all(c['ok'] for c in CHECKS) else 1


if __name__ == '__main__':
    sys.exit(main())
