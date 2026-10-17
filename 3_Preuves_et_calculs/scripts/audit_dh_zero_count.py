#!/usr/bin/env python3
"""V6.3d — Comptage indépendant des zéros de Davenport–Heilbronn par le principe de l'argument.

Pour chaque bande de hauteur, le nombre de zéros dans le rectangle -0,9 <= Re s <= 4 (qui contient
tous les zéros non triviaux : pas de zéro pour Re s >= 1,9, ni, par l'équation fonctionnelle, pour
Re s <= -0,9 hors zéros triviaux) est comparé à la liste data/dh_zeros.csv complétée par les
partenaires 1 - sigma. Aucune dépendance à mpmath. Sortie : data/dh_zero_count_audit.csv.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from zero_reconstruction import F_eval, nontrivial_zeros

def winding(kind, x0, x1, y0, y1, h=0.005):
    pts = []
    for a, b in ((complex(x0, y0), complex(x1, y0)), (complex(x1, y0), complex(x1, y1)),
                 (complex(x1, y1), complex(x0, y1)), (complex(x0, y1), complex(x0, y0))):
        n = max(8, int(abs(b - a) / h)); pts += [a + (b - a) * k / n for k in range(n)]
    v = np.array([F_eval(kind, p) for p in pts]); v = np.append(v, v[0])
    d = np.angle(v[1:] / v[:-1])
    return float(np.sum(d) / (2 * math.pi)), float(np.max(np.abs(d)))

if __name__ == "__main__":
    z = nontrivial_zeros("DH", extended=False); z = z[z.imag > 0]   # audite la liste historique dh_zeros.csv
    edges = [-0.25, 0.25, 12.5] + [20.5 + 20 * k for k in range(9)] + [200.5]
    rows = []
    for y0, y1 in zip(edges[:-1], edges[1:]):
        w, dmax = winding("DH", -0.9, 4.0, y0, y1)
        rows.append(dict(t_min=y0, t_max=y1, comptage_argument=round(w), ecart_a_l_entier=abs(w - round(w)),
                         pas_de_phase_max=dmax, dans_la_liste=int(np.sum((z.imag > y0) & (z.imag <= y1)))))
        print(rows[-1], flush=True)
    df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "dh_zero_count_audit.csv", index=False)
    print("total argument :", int(df.comptage_argument.sum()), " total liste :", int(df.dans_la_liste.sum()))
