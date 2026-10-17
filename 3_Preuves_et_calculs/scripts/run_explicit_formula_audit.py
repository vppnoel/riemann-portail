#!/usr/bin/env python3
"""V6.3b/c — Audit des conventions de la formule explicite de DUAL-LOCK (priorité fixée par V6.3a).

Test : la compression côté premiers M (compression_accurate : archimédien + conducteur + pôle + coefficients locaux)
doit coïncider avec la somme directe sur les zéros  Z_ij = sum_rho H_i(gamma_rho) H_j(gamma_rho),  gamma_rho = -i(rho - 1/2).
 * zeta : 300 premiers zéros (et leurs opposés) ;
 * Davenport–Heilbronn : zéros de data/dh_zeros.csv (t <= 200), complétés par les partenaires 1 - sigma des zéros hors droite,
   et leurs conjugués.
Puis attribution : lambda_G = v^T Z v (v vecteur propre généralisé, v^T G v = 1) = part des zéros sur la droite (>= 0)
+ part de chaque quadruplet hors droite.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
from scipy.linalg import eigh
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from dual_lock import compression_accurate, tent_fourier
from dual_lock_audit import gram_matrix
from explicit_formula import load_zeros
STEP = 0.6
def Hmat(freqs, W, gams): return np.array([[tent_fourier(g, W, xi) for g in gams] for xi in freqs])
rows, attrib = [], []
gam, _ = load_zeros()
gz = np.concatenate([gam, -gam]).astype(complex)
for T in (20.0, 40.0):
    fr, M = compression_accurate(T, "zeta", half_width=2.5, dimension=5, frequency_step=STEP)
    H = Hmat(fr, 2.5, gz); Z = np.real(H @ H.T); G = gram_matrix(fr, 2.5)
    rows.append(dict(objet="zeta", T=T, demi_largeur=2.5, dim=5, ecart_rel=float(np.linalg.norm(M - Z) / np.linalg.norm(Z)),
                     lamG_premiers=float(eigh(M, G, eigvals_only=True)[0]), lamG_zeros=float(eigh(Z, G, eigvals_only=True)[0])))
d = pd.read_csv(ROOT / "data" / "dh_zeros.csv").drop_duplicates()
full = [(float(s), float(t)) for s, t in zip(d.sigma, d.t)]
for s, t in list(full):
    if abs(s - 0.5) > 1e-6 and not any(abs((1 - s) - s2) < 1e-4 and abs(t - t2) < 1e-4 for s2, t2 in full):
        full.append((1 - s, t))
on = [t for s, t in full if abs(s - 0.5) <= 1e-6]; off = sorted({(round(max(s, 1 - s), 6), round(t, 6)) for s, t in full if abs(s - 0.5) > 1e-6}, key=lambda z: z[1])
def gams_on(): return np.array([g for t in on for g in (t + 0j, -t + 0j)])
def gams_quad(s, t):
    out = []
    for ss in (s, 1 - s):
        g = t - 1j * (ss - 0.5); out += [g, -np.conj(g)]
    return np.array(out)
all_g = np.concatenate([gams_on()] + [gams_quad(s, t) for s, t in off])
for T, W in ((86.0, 2.5), (113.0, 2.5), (167.0, 3.5), (176.0, 2.5)):
    fr, M = compression_accurate(T, "DH", half_width=W, dimension=5, frequency_step=STEP)
    H = Hmat(fr, W, all_g); Z = np.real(H @ H.T); G = gram_matrix(fr, W)
    lam, V = eigh(Z, G); v = V[:, 0]
    rows.append(dict(objet="DH", T=T, demi_largeur=W, dim=5, ecart_rel=float(np.linalg.norm(M - Z) / np.linalg.norm(Z)),
                     lamG_premiers=float(eigh(M, G, eigvals_only=True)[0]), lamG_zeros=float(lam[0])))
    Hon = Hmat(fr, W, gams_on()); part_on = float(np.sum(np.real((v @ Hon) ** 2)))
    r = dict(T=T, lamG=float(lam[0]), part_zeros_sur_la_droite=part_on)
    tot = part_on
    for s, t in off:
        Hq = Hmat(fr, W, gams_quad(s, t)); p = float(np.real(np.sum((v @ Hq) ** 2))); tot += p
        r[f"quadruplet_{s:.4f}+{t:.3f}i"] = p
    r["somme_controle"] = tot
    attrib.append(r)
# ---- V6.3c : contrôle eulérien L(s, chi_5) (moyenne chi / chi-barre) contre ses propres zéros (|t| <= 245)
dl = pd.read_csv(ROOT / "data" / "L_chi5_zeros.csv").drop_duplicates()
gl = np.array([float(t) + 0j for t in dl.t])          # zéros de L(s, chi) sur la droite, t de signe quelconque
for T, W in ((86.0, 2.5), (113.0, 2.5), (167.0, 3.5), (176.0, 2.5)):
    fr, M = compression_accurate(T, "L_pair_chi5", half_width=W, dimension=5, frequency_step=STEP)
    H = Hmat(fr, W, gl); Z = np.real(H @ H.T); G = gram_matrix(fr, W)
    rows.append(dict(objet="L_pair_chi5", T=T, demi_largeur=W, dim=5, ecart_rel=float(np.linalg.norm(M - Z) / np.linalg.norm(Z)),
                     lamG_premiers=float(eigh(M, G, eigvals_only=True)[0]), lamG_zeros=float(eigh(Z, G, eigvals_only=True)[0])))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "explicit_formula_audit.csv", index=False)
da = pd.DataFrame(attrib).fillna(0.0); da.to_csv(ROOT / "data" / "explicit_formula_attribution.csv", index=False)
pd.set_option("display.width", 250)
print(f"zéros DH (t>0) : {len(on)} sur la droite + {2*len(off)} hors droite = {len(on)+2*len(off)}")
print(df.to_string(index=False, float_format=lambda x: f"{x:.6g}")); print()
print(da.T.to_string(float_format=lambda x: f"{x:.4g}"))
