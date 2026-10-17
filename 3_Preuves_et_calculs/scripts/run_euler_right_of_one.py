#!/usr/bin/env python3
"""V6.8 — La partie démontrée hors des points d'Euler : zéros dans Re s > 1 et Re s > 0,75 (|t| <= 300).

Pour chaque espace V_q de dimension >= 2 : les deux points milieux (e_1 + e_2)/sqrt 2 et (e_1 - e_2)/sqrt 2
et le point d'Euler e_1 (témoin). Comptage par le principe de l'argument sur les rectangles [sigma_0, 3] x [-300, 300] ;
aucun zéro n'est possible pour Re s >= 3 tant que |a(1)| > sqrt 2 (zeta(3) - 1), vérifié ici.
Le pas est divisé par 4 tant que le saut de phase maximal dépasse 1 radian ; si un zéro reste trop près du bord, le bord
est décalé de 0,005 vers la droite (la colonne bord_utilise l'indique).
Sortie : data/archipelago_right_of_1.csv.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from euler_archipelago import characters, F_values, dirichlet_coefficients
D = ROOT / "data"; TMAX = 300.0
SPACES = [(5, 1), (7, 0), (7, 1), (11, 0), (11, 1), (13, 0), (13, 1)]

def winding(q, par, c, sig0, T=TMAX, sig1=3.0, h=0.01):
    while True:
        seg = []
        for A_, B_ in ((complex(sig0, -T), complex(sig1, -T)), (complex(sig1, -T), complex(sig1, T)), (complex(sig1, T), complex(sig0, T)), (complex(sig0, T), complex(sig0, -T))):
            k = max(8, int(abs(B_ - A_) / h)); seg.append(A_ + (B_ - A_) * (np.arange(k) + 0.5) / k)
        pts = np.concatenate(seg); v = F_values(q, par, c, pts); v = np.append(v, v[0]); dphi = np.angle(v[1:] / v[:-1])
        if np.max(np.abs(dphi)) < 1.0 or h < 1e-3: return float(np.sum(dphi) / (2 * math.pi)), float(np.max(np.abs(dphi))), h
        h /= 4

if __name__ == "__main__":
    t0 = time.time(); rows = []
    bound = math.sqrt(2) * (1.2020569031595942 - 1)
    for q, par in SPACES:
        d = len(characters(q, par))
        for nom, c in (("milieu (e_1 + e_2)", np.r_[1.0, 1.0, np.zeros(d - 2)] / math.sqrt(2)), ("milieu (e_1 - e_2)", np.r_[1.0, -1.0, np.zeros(d - 2)] / math.sqrt(2)),
                       ("point d'Euler e_1", np.eye(d)[0])):
            a1 = float(abs(dirichlet_coefficients(q, par, c, 1)[1])); r = dict(q=q, parite=par, point=nom, a1=a1, sans_zero_au_dela_de_3=a1 > bound)
            for sig0 in (1.0, 0.75):
                s0 = sig0
                while True:                                    # un zéro trop près du bord : on décale le bord de 0,005
                    w, mx, h = winding(q, par, c, s0)
                    if mx < 1.0 or s0 > sig0 + 0.03: break
                    s0 += 0.005
                r[f"zeros_Re_s_sup_{sig0}"] = round(w); r[f"bord_utilise_{sig0}"] = s0; r[f"saut_max_{sig0}"] = mx
            rows.append(r); print(r, f"{time.time() - t0:.0f} s", flush=True)
    pd.DataFrame(rows).to_csv(D / "archipelago_right_of_1.csv", index=False)
