#!/usr/bin/env python3
"""V6.3d — Le verrou local (PRIME-LOCK) et le signe global (DUAL-LOCK) sont-ils indépendants ?

Deux témoins F(s) = P(s) zeta(s) (voir src/lock_witnesses.py) :
  F6 : pas de produit d'Euler, zéros de P sur la droite ;
  E2 : produit d'Euler (fuite nulle), zéros de P hors de la droite.
Pour chacun :
  1. côté premiers (compression_from_lambda) contre côté zéros (zéros de zeta + zéros de P) ;
  2. plus petite valeur propre généralisée lambda_G ; pour E2, attribution par quadruplet ;
  3. mesures PRIME-LOCK (fuite, défaut de tour) et défaut multiplicatif.
Sorties : data/lock_independence_audit.csv, _attribution.csv, _table.csv.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
from scipy.linalg import eigh
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from lock_witnesses import (SPECS, A_E2, coeffs_witness, lambda_witness, compression_from_lambda,
                            polynomial_zero_gammas, zero_side)
from dual_lock import tent_fourier
from dual_lock_audit import gram_matrix
from explicit_formula import load_zeros
from prime_lock import support_leakage, degree1_tower_defect
from dark_zeta import multiplicative_defect
from rejection import build

W, DIM, STEP, GMAX, N = 2.5, 5, 0.6, 20000.0, 32768
gam, _ = load_zeros()
gz = np.concatenate([gam, -gam]).astype(complex)
WINDOWS = {"F6": (20.0, 31.0, 50.0), "E2": (18.0, 27.0, 45.0, 50.0)}
rows, attrib = [], []
for kind, Ts in WINDOWS.items():
    sp = SPECS[kind]; lam = lambda_witness(kind, 400); pz = polynomial_zero_gammas(kind, GMAX)
    allg = np.concatenate([gz, pz["on"].astype(complex), pz["off"]])
    for T in Ts:
        fr, M = compression_from_lambda(T, lam, q=sp["q"], parity=sp["parity"], pole=sp["pole"],
                                        half_width=W, dimension=DIM, frequency_step=STEP)
        G = gram_matrix(fr, W); Z = zero_side(fr, W, allg)
        lz, V = eigh(Z, G); v = V[:, 0]
        rows.append(dict(objet=kind, T=T, demi_largeur=W, dim=DIM,
                         ecart_rel=float(np.linalg.norm(M - Z) / np.linalg.norm(Z)),
                         lamG_premiers=float(eigh(M, G, eigvals_only=True)[0]), lamG_zeros=float(lz[0])))
        if kind == "E2":
            part = lambda g: float(np.real(np.sum((v @ np.array([tent_fourier(g, W, xi) for xi in fr])) ** 2)))
            step, d = 2 * math.pi / math.log(2.0), A_E2 - 0.5
            r = dict(T=T, lamG=float(lz[0]), part_zeros_zeta=part(gz)); tot = r["part_zeros_zeta"]; best = (0.0, None)
            for k in range(0, int(GMAX / step) + 1):
                q4 = np.array([s * k * step + e * 1j * d for s in ((1, -1) if k else (1,)) for e in (1, -1)])
                p = part(q4); tot += p
                if p < best[0]: best = (p, k)
            r.update(quadruplet_dominant_k=best[1], hauteur=best[1] * step, part_quadruplet_dominant=best[0],
                     part_autres_zeros_P=tot - r["part_zeros_zeta"] - best[0], somme_controle=tot)
            attrib.append(r)
pd.DataFrame(rows).to_csv(ROOT / "data" / "lock_independence_audit.csv", index=False)
pd.DataFrame(attrib).to_csv(ROOT / "data" / "lock_independence_attribution.csv", index=False)

# ---- tableau des quatre coins
def local_metrics(a, lam):
    return dict(defaut_multiplicatif=multiplicative_defect(a, P=48)["defect_normalized"],
                fuite_hors_pk=support_leakage(lam), defaut_de_tour=degree1_tower_defect(lam))
table = []
for kind in ("zeta", "L_chi5", "DH"):
    a, lam, _ = build(kind, N); table.append(dict(objet=kind, **local_metrics(a, lam)))
for kind in ("F6", "E2"):
    a = coeffs_witness(kind, N); table.append(dict(objet=kind, **local_metrics(a, lambda_witness(kind, N))))
df = pd.DataFrame(rows)
old = pd.read_csv(ROOT / "data" / "explicit_formula_audit.csv")
sign = {k: float(g.lamG_premiers.min()) for k, g in pd.concat([df, old]).groupby("objet")}
names = {"zeta": "zeta", "L_chi5": "L_pair_chi5", "DH": "DH", "F6": "F6", "E2": "E2"}
for r in table:
    r["lamG_min_fenetres_testees"] = sign[names[r["objet"]]]
    r["zeros_hors_droite_connus"] = r["objet"] in ("DH", "E2")
dt = pd.DataFrame(table); dt.to_csv(ROOT / "data" / "lock_independence_table.csv", index=False)
pd.set_option("display.width", 250)
print(df.to_string(index=False, float_format=lambda x: f"{x:.6g}")); print()
print(pd.DataFrame(attrib).to_string(index=False, float_format=lambda x: f"{x:.5g}")); print()
print(dt.to_string(index=False, float_format=lambda x: f"{x:.4g}"))
