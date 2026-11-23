#!/usr/bin/env python3
"""Vérification de TAC-009 (ia:claude) : le Gram de Nyman–Beurling contient-il de l'arithmétique ?

Le rapport affirme que K^NB « ne contient aucun paramètre F » et ne voit donc que la géométrie des dilatations.
Contre-contrôle :
 X  calcul direct en variable x (intégration exacte par morceaux sur [1, Y], queue moyennée) de
    G_ab = ∫₀¹ ρ_a ρ_b dx, ρ_θ(x) = {θ/x} − θ{1/x} ;
 M  même Gram par Plancherel–Mellin : ∫₀^∞ ρ_θ(x) x^{s−1} dx = −ζ(s)(θ^s − θ)/s (0 < Re s < 1), donc
    G_ab = (1/2π) ∫ |ζ(½+it)|² (a^s − a) conj(b^s − b) / |s|² dt, s = ½ + it : |ζ|² y figure explicitement ;
 W  témoin géométrique : |ζ|² remplacé par 1 (fonctions ϕ_θ de transformée −(θ^s − θ)/s, sans arithmétique) ;
 F  même formule avec |F(½+it)|² pour F = L(s, χ₅) et Davenport–Heilbronn (définition du vérificateur, à confronter
    à de Roton ; elle ne prétend pas être la généralisation publiée).
Grille : u = 0,5 ; 1,0 ; … ; 3,0 (θ = e^{−u}), différences C_i = ρ_{θ_{i+1}} − ρ_{θ_i}, Gram K et sa version normalisée R.
python -B 2_Methode/Depot/TAC-009/verification/contre_controle.py  →  contre_controle.json. Auteur et titulaire des droits : Vincent NOËL.
"""
import json, math, sys
from fractions import Fraction
from pathlib import Path
import numpy as np, mpmath as mp
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / '3_Preuves_et_calculs/src')); from rejection import KAPPA_DH
U = np.arange(0.5, 3.0001, 0.5); TH = np.exp(-U); m = len(TH) - 1; out = {'grille_u': U.tolist()}

# ---------------- X : Gram direct en variable x, y = 1/x : ∫₁^∞ ({ay} − a{y})({by} − b{y}) dy / y²
def gram_x(a, b, Y):
    pts = {1.0, float(Y)}
    for c in (1.0, a, b):
        k = np.arange(math.ceil(c), math.floor(c * Y) + 1); pts.update((k / c).tolist())
    P = np.array(sorted(p for p in pts if 1 <= p <= Y)); lo, hi = P[:-1], P[1:]; mid = (lo + hi) / 2
    fa = np.floor(a * mid); fb = np.floor(b * mid); f1 = np.floor(mid)
    # sur un morceau : (α y + β)(γ y + δ)/y², α = a − a = 0 → ({ay} − a{y}) = −fa + a f1 constante
    A = -fa + a * f1; B = -fb + b * f1                     # ρ_a = A, ρ_b = B sur le morceau
    I = np.sum(A * B * (1 / lo - 1 / hi))
    return I
def gram_x_lim(a, b):
    v = [gram_x(a, b, Y) for Y in (2e4, 4e4, 8e4)]          # queue ~ c/Y : extrapolation de Richardson
    return 2 * v[2] - v[1], abs(v[2] - v[1])

# ---------------- M, W, F : formule de Mellin sur la droite critique
mp.mp.dps = 15
T, dt = 400.0, 0.02; t = np.arange(dt / 2, T, dt); s = 0.5 + 1j * t
def _L(args):
    x, conj = args
    chi = [0, 1, 1j, -1j, -1]
    if conj: chi = [complex(c).conjugate() for c in chi]
    return complex(mp.dirichlet(complex(x), chi))
_cache = {}
def L_pair():
    """L(s, χ) et L(s, χ̄) sur la grille, calculés une seule fois (en parallèle)."""
    if 'L' not in _cache:
        from multiprocessing import Pool
        with Pool() as P:
            L1 = np.array(P.map(_L, [(x, False) for x in s], chunksize=200))
            L2 = np.array(P.map(_L, [(x, True) for x in s], chunksize=200))
        _cache['L'] = (L1, L2)
    return _cache['L']
def absF2(kind):
    if kind == 'W': return np.ones_like(t)
    if kind == 'zeta': return np.array([float(abs(mp.zeta(complex(x))) ** 2) for x in s])
    L1, L2 = L_pair()
    if kind == 'L_chi5': return 0.5 * (np.abs(L1) ** 2 + np.abs(L2) ** 2)   # t > 0 pour χ et t < 0 via χ̄
    D = 0.5 * (1 - 1j * KAPPA_DH) * L1 + 0.5 * (1 + 1j * KAPPA_DH) * L2
    return np.abs(D) ** 2                                   # DH à coefficients réels : |D(½−it)| = |D(½+it)|
def gram_mellin(w):
    M = np.array([TH[i + 1] ** s - TH[i + 1] - TH[i] ** s + TH[i] for i in range(m)])   # transformées des C_i (au signe près)
    G = (M * (w / np.abs(s) ** 2)) @ M.conj().T * dt / (2 * np.pi)
    return 2 * G.real                                       # t et −t
def spectre(K):
    d = np.sqrt(np.diag(K)); Rn = K / np.outer(d, d); e = np.linalg.eigvalsh(Rn)
    return e, float(np.exp(-np.sum((e / e.sum()) * np.log(e / e.sum()))))        # rang effectif (entropie)

Kx = np.zeros((m, m)); Ex = np.zeros((m, m))
rho = lambda i, j: gram_x_lim(TH[i], TH[j])
G = {}; 
for i in range(m + 1):
    for j in range(i, m + 1):
        G[i, j] = G[j, i] = rho(i, j)
for i in range(m):
    for j in range(m):
        Kx[i, j] = G[i + 1, j + 1][0] - G[i + 1, j][0] - G[i, j + 1][0] + G[i, j][0]
        Ex[i, j] = G[i + 1, j + 1][1] + G[i + 1, j][1] + G[i, j + 1][1] + G[i, j][1]
res = {}
for kind in ('zeta', 'W', 'L_chi5', 'DH'):
    K = gram_mellin(absF2(kind)); e, r = spectre(K)
    res[kind] = dict(K=K.tolist(), valeurs_propres_R=e.tolist(), rang_effectif=r)
    print(kind, np.round(e, 5), round(r, 4), flush=True)
ex, rx = spectre(Kx)
res['zeta_x'] = dict(K=Kx.tolist(), erreur_extrapolation_max=float(Ex.max()), valeurs_propres_R=ex.tolist(), rang_effectif=rx)
res['accord_x_mellin_zeta'] = dict(ecart_max=float(np.abs(Kx - np.array(res['zeta']['K'])).max()), norme_K=float(np.abs(Kx).max()))
dist = lambda a, b: float(np.linalg.norm(np.array(res[a]['valeurs_propres_R']) - np.array(res[b]['valeurs_propres_R'])))
res['distances_spectrales'] = {f'{a}-{b}': dist(a, b) for a, b in (('zeta', 'W'), ('zeta', 'DH'), ('zeta', 'L_chi5'), ('DH', 'W'), ('L_chi5', 'W'))}
res['troncature'] = dict(T=T, pas=dt, remarque="intégrale tronquée à |t| ≤ T ; la queue est d'ordre ∫_T^∞ |F|² 16/t² dt ≈ 16 log(T)/T pour ζ (≈ 0,24 en absolu au pire), à comparer aux entrées de K ; voir accord_x_mellin_zeta")
out.update(res)
(HERE / 'contre_controle.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({k: out[k] for k in ('accord_x_mellin_zeta', 'distances_spectrales')}, indent=1))
