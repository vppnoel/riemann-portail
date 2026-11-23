#!/usr/bin/env python3
"""TAC-008 : décomposition de la cohérence inter-échelles K = K_diag + K_chaîne + K_croisé.

K_ij = ∫ C_F(u_i,t) conj C_F(u_j,t) ψ(t/T) dt, C_F(u,t) = Σ b_F(n) n^{-1/2} w((log n − u)/h) e^{−it log n}
(critique « tomographie de phase », § 7–8 ; 4_Archives/recus/2026-10-17/). Avec ψ(y) = exp(−y²/2) :
K_ij = Σ_{n,m} c_n conj(c_m) w_i(n) w_j(m) Ψ(log n − log m), Ψ(x) = T√(2π) exp(−(Tx)²/2), c_n = b_F(n)/√n.
Diagonale : n = m. Chaîne : n ≠ m puissances d'un même premier. Croisé : le reste.
Réglages fixés dans la prévision (journal des tâches) avant tout calcul.
python -B 2_Methode/Depot/TAC-008/decomposition_K.py  →  resultats.json
Auteur et titulaire des droits : Vincent NOËL. Producteur : ia:claude.
"""
from pathlib import Path
import json, sys
import numpy as np
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / '3_Preuves_et_calculs/src'))
from rejection import coeffs, log_derivative_coeffs

NMAX, H, US, TS, DRAWS, SEED = 20000, 0.5, np.arange(2.0, 8.0001, 0.25), (10.0, 1.0), 20, 20261018
n = np.arange(NMAX + 1); logn = np.log(np.maximum(n, 1))

# plus petit facteur premier et « base » p de n quand n est une puissance de premier
spf = np.zeros(NMAX + 1, dtype=np.int64)
for p in range(2, NMAX + 1):
    if spf[p] == 0: spf[p::p] = np.where(spf[p::p] == 0, p, spf[p::p])
base = np.zeros(NMAX + 1, dtype=np.int64); expo = np.zeros(NMAX + 1, dtype=np.int64)
for k in range(2, NMAX + 1):
    p = spf[k]; m, e = k, 0
    while m % p == 0: m //= p; e += 1
    if m == 1: base[k] = p; expo[k] = e
Lam = np.where(base > 0, np.log(np.maximum(base, 1)), 0.0)

def b_of(kind, rng=None):
    if kind in ('zeta', 'L_chi5', 'DH'): return log_derivative_coeffs(coeffs(kind, NMAX))
    b = np.zeros(NMAX + 1, dtype=complex); pp = base > 0
    if kind == 'W1':                                    # multiplicatif aléatoire : α_p^k log p
        alpha = np.exp(2j * np.pi * rng.random(NMAX + 1))
        b[pp] = alpha[base[pp]] ** expo[pp] * Lam[pp]
    elif kind == 'W2':                                  # phases indépendantes pour chaque p^k
        b[pp] = Lam[pp] * np.exp(2j * np.pi * rng.random(pp.sum()))
    return b

W = np.exp(-0.5 * ((logn[:, None] - US[None, :]) / H) ** 2); W[:2] = 0.0
keep = np.where(W.max(axis=1) > 1e-12)[0]; Wk = W[keep]; lk = logn[keep]; bk = base[keep]

def K_parts(b, T):
    c = (b / np.sqrt(np.maximum(n, 1)))[keep]
    A = Wk * c[:, None]                                  # (n, échelles)
    tot = np.zeros((len(US), len(US)), complex)
    for s in range(0, len(keep), 2000):
        Psi = T * np.sqrt(2 * np.pi) * np.exp(-0.5 * (T * (lk[s:s + 2000, None] - lk[None, :])) ** 2)
        tot += A[s:s + 2000].T @ Psi @ A.conj()
    diag = (A * (T * np.sqrt(2 * np.pi))).T @ A.conj()
    chain = np.zeros_like(tot)
    for p in np.unique(bk[bk > 0]):
        idx = np.where(bk == p)[0]
        if len(idx) < 2: continue
        Psi = T * np.sqrt(2 * np.pi) * np.exp(-0.5 * (T * (lk[idx, None] - lk[None, idx])) ** 2); np.fill_diagonal(Psi, 0)
        chain += A[idx].T @ Psi @ A[idx].conj()
    return tot, diag, chain, tot - diag - chain

def stats(b, T):
    tot, d, ch, cr = K_parts(b, T); tr = np.real(np.trace(tot))
    dg = np.sqrt(np.real(np.diag(tot))); R = tot / np.outer(dg, dg)
    fro = lambda M: float(np.linalg.norm(M))
    s = fro(d) + fro(ch) + fro(cr)
    return dict(part_diag=fro(d) / s, part_chaine=fro(ch) / s, part_croise=fro(cr) / s,
                chaine_sur_trace=fro(ch) / tr, croise_sur_trace=fro(cr) / tr, R=R, Kn={'diag': d / tr, 'chaine': ch / tr, 'croise': cr / tr})

def main():
    rng = np.random.default_rng(SEED); out = dict(reglages=dict(NMAX=NMAX, h=H, u=[float(u) for u in US], T=list(TS), tirages=DRAWS, graine=SEED))
    for T in TS:
        S = {k: stats(b_of(k), T) for k in ('zeta', 'L_chi5', 'DH')}
        Wd = {k: [stats(b_of(k, rng), T) for _ in range(DRAWS)] for k in ('W1', 'W2')}
        res = {}
        for k, v in S.items(): res[k] = {x: v[x] for x in ('part_diag', 'part_chaine', 'part_croise', 'chaine_sur_trace', 'croise_sur_trace')}
        for k, L in Wd.items():
            for x in ('part_diag', 'part_chaine', 'part_croise', 'chaine_sur_trace', 'croise_sur_trace'):
                a = np.array([d[x] for d in L]); res[k + '_moyenne_' + x] = float(a.mean()); res[k + '_ecart_type_' + x] = float(a.std(ddof=1))
        # séparations : distance de R totale et des composantes normalisées, comparées à la dispersion des témoins
        dist = lambda A, B: float(np.linalg.norm(A - B))
        sep = {}
        for a_, b_ in (('zeta', 'DH'), ('zeta', 'L_chi5'), ('L_chi5', 'DH')):
            sep[f'{a_}-{b_}'] = dict(R=dist(S[a_]['R'], S[b_]['R']), **{x: dist(S[a_]['Kn'][x], S[b_]['Kn'][x]) for x in ('diag', 'chaine', 'croise')})
        w2 = np.array([d['chaine_sur_trace'] for d in Wd['W2']]); w1 = np.array([d['chaine_sur_trace'] for d in Wd['W1']])
        sep['z_chaine_zeta_contre_W2'] = float((S['zeta']['chaine_sur_trace'] - w2.mean()) / w2.std(ddof=1))
        sep['z_chaine_W1_contre_W2'] = float((w1.mean() - w2.mean()) / np.sqrt(w1.var(ddof=1) / DRAWS + w2.var(ddof=1) / DRAWS))
        sep['z_chaine_W1_contre_W2_tirage_unique'] = float((w1.mean() - w2.mean()) / np.sqrt(w1.var(ddof=1) + w2.var(ddof=1)))
        res['separations'] = sep
        out[f'T={T:g}'] = res
        print(json.dumps({f'T={T:g}': res}, ensure_ascii=False, indent=1), flush=True)
    (HERE / 'resultats.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')

if __name__ == '__main__': main()
