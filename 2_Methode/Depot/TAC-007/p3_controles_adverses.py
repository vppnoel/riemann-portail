#!/usr/bin/env python3
"""TAC-007, reprise : contrôles adverses demandés par la vérification (fil #3). Prévision enregistrée avant calcul (commit d777652).

C0  La forme générale ci-dessous reproduit exactement weil_matrix() du document 81 pour ζ.
C1  Davenport–Heilbronn (DH) à L = 0,8. Forme de Weil en variable x pour une fonction de degré 1, conducteur q, facteur Γ((s+κ)/2) :
      Q(f) = [pôle] + g(0)·C₀(L) + ∫₀^{2L} (g(0) − g(x)) w(x)/x dx − Σ_{log n < 2L} 2 Re b(n) n^{−1/2} g(log n),
      a = (1 + 2κ)/4, w(x) = 2x e^{−2ax}/(1 − e^{−2x}), C₀(L) = log(q/π) + E₁(4L) + ∫₀^{2L} (e^{−2x} − w(x))/x dx,
    b(n) coefficients de −F'/F (src/rejection.py). Pour ζ : a = 1/4, q = 1, pôle, b = Λ. Pour L(s,χ₅) et DH : a = 3/4, q = 5, sans pôle.
    Validation sur L(s,χ₅) contre ses zéros (data/L_chi5_zeros_600.csv), avec f = cos⁴(πx/2L).
C2  Analogue des corps de fonctions : même chaîne (côté arithmétique, nombres de points comptés) pour y² = x³ + x + 1 sur F₅,
    comparée au côté spectral ; fausses courbes (genre 1 avec a = 5 > 2√5 ; genre 2 à quatuor hors du cercle).
C3  Témoins négatifs pour ζ à 0,8 : (a) quatuor fictif de zéros hors droite ; (b) Λ(2) multiplié par 1 + ε.
Aucun zéro de ζ n'est utilisé dans les formes ; les zéros de L(s,χ₅) servent seulement à la validation C1.
python -B 2_Methode/Depot/TAC-007/p3_controles_adverses.py  →  p3_resultats.json (même dossier)
Auteur et titulaire des droits : Vincent NOËL. Producteur : ia:claude.
"""
from pathlib import Path
import importlib.util, itertools, json, math, sys, time
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
def charger(nom, rel):
    s = importlib.util.spec_from_file_location(nom, ROOT / rel); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
z = charger('zhu', '3_Preuves_et_calculs/scripts/run_zhu_reproduction.py'); mp = z.mp
rj = charger('rejection', '3_Preuves_et_calculs/src/rejection.py')
mp.mp.dps = 60
OUT = HERE / 'p3_resultats.json'; R = {}; t0 = time.time()
def note(k, v):
    R[k] = v; OUT.write_text(json.dumps(R, indent=1, ensure_ascii=False) + '\n'); print(k, json.dumps(v, ensure_ascii=False)[:300], f'{time.time() - t0:.0f} s', flush=True)
s = lambda x, d=12: mp.nstr(x, d)


# ------------------------------------------------------------------ forme générale en variable x
def w_a(x, a):
    return mp.mpf(1) if x == 0 else 2 * x * mp.exp(-2 * a * x) / (1 - mp.exp(-2 * x))

def C0_a(L, a, q):
    return mp.log(mp.mpf(q) / mp.pi) + mp.e1(4 * L) + mp.quad(lambda x: (mp.exp(-2 * x) - w_a(x, a)) / x, [0, 2 * L])

def poids(kind, L):
    """2 Re b(n) n^{−1/2} pour log n < 2L."""
    nmax = int(math.exp(2 * L)) + 1
    b = rj.log_derivative_coeffs(rj.coeffs(kind, nmax + 1))
    return {n: 2 * mp.mpf(float(b[n].real)) / mp.sqrt(n) for n in range(2, nmax + 1) if math.log(n) < 2 * L and abs(b[n].real) > 1e-15}

def forme(L, parity, N, K, a, q, wts, pole):
    L = mp.mpf(L); degs = [parity + 2 * k for k in range(N)]; J = max(degs) + 4; n = N
    M = [[mp.mpf(0)] * n for _ in range(n)]
    if pole:
        xs, wx = z.nodes(-L, L, J + 8); BV = [z.basis_vals(x, L, degs) for x in xs]
        A = [mp.fsum(wx[k] * BV[k][i] * mp.exp(-xs[k] / 2) for k in range(len(xs))) for i in range(n)]
        B = [mp.fsum(wx[k] * BV[k][i] * mp.exp(xs[k] / 2) for k in range(len(xs))) for i in range(n)]
        M = [[A[i] * B[j] + A[j] * B[i] for j in range(n)] for i in range(n)]
    c0 = C0_a(L, a, q)
    for i in range(n): M[i][i] += c0
    xk, wk = z.nodes(mp.mpf(0), 2 * L, K)
    for k in range(K):
        G = z.gram_corr(L, degs, xk[k], J); f = wk[k] * w_a(xk[k], a) / xk[k]
        for i in range(n):
            for j in range(n): M[i][j] += f * ((1 if i == j else 0) - G[i][j])
    for m, c in wts.items():
        G = z.gram_corr(L, degs, mp.log(m), J)
        for i in range(n):
            for j in range(n): M[i][j] -= c * G[i][j]
    return M

def base_noyau(L, N, parity):
    """Colonnes orthonormées de a⊥ (moment exponentiel nul), comme noyau_des_moments() du document 81."""
    L_ = mp.mpf(L); degs = [parity + 2 * k for k in range(N)]; xs, wx = z.nodes(-L_, L_, max(degs) + 12)
    BV = [z.basis_vals(x, L_, degs) for x in xs]
    a = [mp.fsum(wx[k] * BV[k][i] * mp.exp(-xs[k] / 2) for k in range(len(xs))) for i in range(N)]
    na = mp.sqrt(mp.fsum(x * x for x in a)); u = [x / na for x in a]; sg = 1 if u[0] >= 0 else -1
    wv = list(u); wv[0] += sg; ww = mp.fsum(x * x for x in wv)
    H = mp.matrix(N, N)
    for i in range(N):
        for j in range(N): H[i, j] = (1 if i == j else 0) - 2 * wv[i] * wv[j] / ww
    return H[:, 1:N]

def vp(Mx):
    E, V = mp.eigsy(Mx); i = min(range(Mx.rows), key=lambda k: E[k]); return E[i], V[:, i]

def transformees(L, N, parity, zc):
    """φ̂_i(z) = ∫ φ_i(x) e^{izx} dx, z complexe."""
    L_ = mp.mpf(L); degs = [parity + 2 * k for k in range(N)]; xs, wx = z.nodes(-L_, L_, max(degs) + 60)
    BV = [z.basis_vals(x, L_, degs) for x in xs]; e = [mp.exp(1j * zc * x) for x in xs]
    return [mp.fsum(wx[k] * BV[k][i] * e[k] for k in range(len(xs))) for i in range(N)]


L = 0.8; N = 48; K = 48

# ------------------------------------------------------------------ C0 : la forme générale reproduit le document 81
if 'C0' not in R:
    Nt = 12
    Mg = forme(L, 0, Nt, K, mp.mpf(1) / 4, 1, {m: 2 * mp.mpf(z.vonmangoldt(m)) / mp.sqrt(m) for m in range(2, 5) if z.vonmangoldt(m)}, True)
    Mz = z.weil_matrix(L, 0, Nt, K)
    note('C0', dict(N=Nt, ecart_max=s(max(abs(Mg[i][j] - Mz[i][j]) for i in range(Nt) for j in range(Nt)), 3)))

# ------------------------------------------------------------------ C1 : validation sur L(s, χ₅), puis DH
def Q_test(L, a, q, wts, pole):
    """Q(f) en variable x pour f = cos⁴(πx/2L) (même chemin que controle_zeros du document 81)."""
    mp.mp.dps = 30; L = mp.mpf(L)
    f = lambda x: mp.cos(mp.pi * x / (2 * L)) ** 4 if abs(x) <= L else mp.mpf(0)
    def g(x):
        ys, wy = z.nodes(-L + x, L, 60); return mp.fsum(wy[k] * f(ys[k]) * f(ys[k] - x) for k in range(len(ys)))
    xs, wx = z.nodes(-L, L, 60); g0 = g(mp.mpf(0)); xk, wk = z.nodes(mp.mpf(0), 2 * L, 60)
    Q = g0 * C0_a(L, a, q) + mp.fsum(wk[k] * (g0 - g(xk[k])) * w_a(xk[k], a) / xk[k] for k in range(60))
    if pole: Q += 2 * mp.fsum(wx[k] * f(xs[k]) * mp.cosh(xs[k] / 2) for k in range(60)) ** 2
    Q -= mp.fsum(c * g(mp.log(m)) for m, c in wts.items())
    return Q

def Fhat(t, L):
    t = mp.mpf(float(t)); L = mp.mpf(L); tot = mp.mpf(0)
    for k, wk_ in enumerate((mp.mpf(3) / 8, mp.mpf(1) / 2, mp.mpf(1) / 8)):
        for sgn in ((1,) if k == 0 else (1, -1)):
            r = t + sgn * k * mp.pi / L
            tot += wk_ * (2 * L if r == 0 else 2 * mp.sin(r * L) / r) * (1 if k == 0 else mp.mpf(1) / 2)
    return tot

if 'C1_validation_chi5' not in R:
    out = {}
    for Lv in (0.8, 1.5):
        wts = poids('L_chi5', Lv)
        Q = Q_test(Lv, mp.mpf(3) / 4, 5, wts, False)
        gam = pd.read_csv(ROOT / '3_Preuves_et_calculs/data/L_chi5_zeros_600.csv').t.values
        Z = mp.fsum(Fhat(t, Lv) ** 2 for t in gam)
        # contre-épreuve : avec le facteur de ζ (a = 1/4, q = 1), la validation doit échouer
        Qfaux = Q_test(Lv, mp.mpf(1) / 4, 1, wts, False)
        out[f'L={Lv}'] = dict(Q_formule_x=s(Q), somme_zeros=s(Z), ecart_relatif=s(abs(Q - Z) / abs(Z), 3), zeros=len(gam),
                              poids={str(k): s(v, 8) for k, v in wts.items()}, contre_epreuve_facteur_zeta_ecart=s(abs(Qfaux - Z) / abs(Z), 3))
    mp.mp.dps = 60
    note('C1_validation_chi5', out)

if 'C1_DH' not in R:
    out = {}
    wDH = poids('DH', L)
    for Nn in (32, 48):
        M = forme(L, 0, Nn, K, mp.mpf(3) / 4, 5, wDH, False); Mx = mp.matrix(M)
        lam_plein = vp(Mx)[0]
        B = base_noyau(L, Nn, 0); lam_noyau = vp(B.T * Mx * B)[0]
        out[f'N={Nn}'] = dict(lambda_min_secteur_pair=s(lam_plein), lambda_min_noyau=s(lam_noyau))
    out['poids_2Re_b_sur_racine_n'] = {str(k): s(v, 8) for k, v in wDH.items()}
    note('C1_DH', out)

# ------------------------------------------------------------------ C3 : témoins négatifs pour ζ à 0,8
if 'C3' not in R:
    wZ = {m: 2 * mp.mpf(z.vonmangoldt(m)) / mp.sqrt(m) for m in range(2, 5) if z.vonmangoldt(m)}
    M = mp.matrix(forme(L, 0, N, K, mp.mpf(1) / 4, 1, wZ, True)); B = base_noyau(L, N, 0); Rk = B.T * M * B
    lam0, u = vp(Rk); out = dict(N=N, lambda0=s(lam0))
    gam1 = mp.mpf('14.134725141734693790457251983562')
    def avec_quatuor(d):
        v = mp.matrix(transformees(L, N, 0, gam1 - 1j * d)); Bv = B.T * v
        D = mp.matrix(N - 1, N - 1)
        for i in range(N - 1):
            for j in range(N - 1): D[i, j] = 4 * mp.re(Bv[i] * Bv[j])
        return vp(Rk + D)[0]
    qa = {str(d): s(avec_quatuor(mp.mpf(d))) for d in ('0', '0.1', '0.01', '0.001')}
    lo, hi = mp.mpf(0), mp.mpf('0.1')
    if avec_quatuor(hi) < 0:
        for _ in range(40):
            mid = (lo + hi) / 2
            if avec_quatuor(mid) < 0: hi = mid
            else: lo = mid
    out['a_quatuor_fictif'] = dict(hauteur=s(gam1, 10), lambda_min=qa, seuil_delta=s(hi, 6))
    G2 = B.T * mp.matrix(z.gram_corr(mp.mpf(L), [2 * k for k in range(N)], mp.log(2), max(2 * k for k in range(N)) + 4)) * B
    c2 = 2 * mp.log(2) / mp.sqrt(2); d1 = c2 * (u.T * G2 * u)[0]          # dλ/dε = −c2·uᵀG₂u
    eps_pred = lam0 / d1
    lam_eps = lambda e: vp(Rk - e * c2 * G2)[0]
    lo, hi = mp.mpf(0), 4 * eps_pred
    for _ in range(60):
        mid = (lo + hi) / 2
        if lam_eps(mid) < 0: hi = mid
        else: lo = mid
    out['b_Lambda2'] = dict(derivee_premier_ordre=s(-d1), epsilon_predit=s(eps_pred, 8), epsilon_observe=s(hi, 8),
                            ecart_relatif=s(abs(hi - eps_pred) / abs(eps_pred), 3), lambda_a_moins_eps_observe=s(lam_eps(-hi)))
    note('C3', out)

# ------------------------------------------------------------------ C2 : corps de fonctions
def compte_points(p, m, coeffs=(1, 1, 0, 1)):
    """N_m = #E(F_{p^m}) pour y² = x³ + x + 1, par énumération (arithmétique de F_{p^m} écrite ici)."""
    import sympy
    X = sympy.symbols('X')
    for c in itertools.product(range(p), repeat=m):
        P = sympy.Poly([1, *c], X, modulus=p)
        if P.is_irreducible: mod = [int(v) % p for v in P.all_coeffs()]; break
    def mul(u, v):                                                  # coefficients du degré m − 1 au degré 0
        r = [0] * (2 * m - 1)
        for i, a in enumerate(u):
            if a:
                for j, b in enumerate(v): r[i + j] = (r[i + j] + a * b) % p
        for k in range(m - 1):                                      # r[k] porte X^(2m−2−k), avec 2m−2−k ≥ m
            c = r[k]
            if c:
                for t in range(1, m + 1): r[k + t] = (r[k + t] - c * mod[t]) % p   # X^m = −Σ mod[t] X^(m−t)
                r[k] = 0
        return r[m - 1:]
    def puis(u, e):
        r = [0] * m; r[-1] = 1
        while e:
            if e & 1: r = mul(r, u)
            u = mul(u, u); e >>= 1
        return r
    Q = p ** m; un = [0] * (m - 1) + [1]; e = (Q - 1) // 2; Nm = 1
    for x in itertools.product(range(p), repeat=m):
        x = list(x); x3 = mul(mul(x, x), x)
        v = [(a + b) % p for a, b in zip(x3, x)]; v[-1] = (v[-1] + 1) % p
        if not any(v): Nm += 1
        else: Nm += 2 if puis(v, e) == un else 0
    return Nm

def forme_cf(q, Nm, M, parity, genre):
    """Côté arithmétique : Q(f) = (2g − 2) g(0) − Σ_{m≠0} g(m) N_|m| q^{−|m|/2}, restreint à F̃(√q) = 0."""
    ks = list(range(-M, M + 1)); idx = {k: i for i, k in enumerate(ks)}
    cols = []
    for k in range(parity, M + 1):
        v = [mp.mpf(0)] * len(ks)
        if k == 0: v[idx[0]] = mp.mpf(1)
        else: v[idx[k]] = 1 / mp.sqrt(2); v[idx[-k]] = (1 if parity == 0 else -1) / mp.sqrt(2)
        cols.append(v)
    P = mp.matrix(cols).T                                                       # (2M+1) × dim
    A = mp.matrix(len(ks), len(ks))
    for i, k in enumerate(ks):
        for j, l in enumerate(ks):
            m = k - l                                                           # g(m) = Σ_k f_k f_{k−m}
            A[i, j] = (2 * genre - 2) if m == 0 else -mp.mpf(Nm[abs(m)]) * mp.mpf(q) ** (-mp.mpf(abs(m)) / 2)
    return P, A, ks

def restreint(P, A, ks, q):
    r = mp.sqrt(q); a = mp.matrix([[r ** k for k in ks]]) * P                 # F̃(√q) sur la base (ligne)
    n = P.cols
    if n == 1: return None
    u = [a[0, i] / mp.norm(a) for i in range(n)]; sg = 1 if u[0] >= 0 else -1
    wv = list(u); wv[0] += sg; ww = mp.fsum(x * x for x in wv)
    Hm = mp.matrix(n, n)
    for i in range(n):
        for j in range(n): Hm[i, j] = (1 if i == j else 0) - 2 * wv[i] * wv[j] / ww
    Bk = P * Hm[:, 1:n]; return Bk.T * A * Bk

def spectral(alphas, q, P, ks):
    """Σ_j F̃(r_j) F̃(1/r_j), r_j = α_j/√q, comme forme quadratique sur la base P."""
    S = mp.matrix(len(ks), len(ks))
    for al in alphas:
        r = mp.mpc(al) / mp.sqrt(q)
        for i, k in enumerate(ks):
            for j, l in enumerate(ks): S[i, j] += mp.re(r ** k * r ** (-l))
    return S

if 'C2' not in R:
    mp.mp.dps = 50; q = 5; out = {}
    Nm = {m: compte_points(q, m) for m in range(1, 7)}
    a = q + 1 - Nm[1]; al = [(a + mp.sqrt(mp.mpc(a * a - 4 * q))) / 2, (a - mp.sqrt(mp.mpc(a * a - 4 * q))) / 2]
    out['courbe'] = dict(equation='y² = x³ + x + 1 sur F₅', N_m=Nm, a=a, borne_de_Hasse=f'|a| = {abs(a)} ≤ 2√5 ≈ 4,47',
                         ecart_rationalite=s(max(abs(q ** m + 1 - (al[0] ** m + al[1] ** m) - Nm[m]) for m in Nm), 3))
    def cas(nom, alphas, genre, comptes=None):
        # vraie courbe : N_m comptés (côté arithmétique indépendant) ; fausses courbes : N_m définis par les α fictifs
        Nf = comptes or {m: mp.re(q ** m + 1 - mp.fsum(x ** m for x in alphas)) for m in range(1, 7)}
        res = {}
        for M in (1, 2, 3):
            for par, lab in ((0, 'pair'), (1, 'impair')):
                P, A, ks = forme_cf(q, Nf, M, par, genre)
                S = spectral(alphas, q, P, ks)
                pole = mp.matrix(len(ks), len(ks)); r = mp.sqrt(q)
                for i, k in enumerate(ks):
                    for j, l in enumerate(ks): pole[i, j] = r ** (k - l) + r ** (l - k)
                ecart = mp.norm(P.T * (A + pole - S) * P)                      # arithmétique + pôle = spectral, sur tout le secteur
                Rk = restreint(P, A, ks, q)
                lam = None if Rk is None else min(mp.eigsy(Rk)[0][i] for i in range(Rk.rows))
                res[f'M={M} {lab}'] = dict(ecart_arith_spectral=s(ecart, 3), lambda_min_noyau='dimension 0' if lam is None else s(lam))
        return res
    out['vraie_courbe'] = cas('vraie', al, 1, comptes=Nm)
    a5 = 5; al5 = [(a5 + mp.sqrt(a5 * a5 - 4 * q)) / 2, (a5 - mp.sqrt(a5 * a5 - 4 * q)) / 2]
    out['faux_genre1_a5'] = dict(alpha=[s(x, 8) for x in al5], **cas('faux1', al5, 1))
    # faux genre 2 : P(T) = 1 − a1 T + a2 T² − q a1 T³ + q² T⁴ à coefficients entiers, quatuor complexe hors du cercle |α| = √q
    trouve = None
    for a1 in range(0, 12):
        for a2 in range(-30, 40):
            rts = np.roots([q * q, -q * a1, a2, -a1, 1]); als = 1 / rts
            if all(abs(x.imag) > 1e-6 for x in als) and all(abs(abs(x) - math.sqrt(q)) > 0.05 for x in als):
                trouve = (a1, a2); break
        if trouve: break
    a1, a2 = trouve
    P4 = mp.polyroots([q * q, -q * a1, a2, -a1, 1], maxsteps=200, extraprec=200); al4 = [1 / x for x in P4]
    out['faux_genre2'] = dict(P_T=f'1 − {a1}T + {a2}T² − {q * a1}T³ + {q * q}T⁴', modules_alpha=[s(abs(x), 8) for x in al4], **cas('faux2', al4, 2))
    mp.mp.dps = 60
    note('C2', out)

R['duree_secondes'] = round(time.time() - t0); OUT.write_text(json.dumps(R, indent=1, ensure_ascii=False) + '\n')
