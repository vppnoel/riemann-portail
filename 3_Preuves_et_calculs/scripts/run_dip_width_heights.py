#!/usr/bin/env python3
"""V6.3f — La largeur du creux selon la hauteur des paires de zéros.

Même ajustement que run_dip_width_full.py (profil K_w sommé sur tous les zéros de zeta voisins, paramètres
c, A, w), mais les paires (gamma_b, gamma_c) sont prises dans une tranche de hauteur [T1, T2], et les cibles
(zéros de zeta) dans une plage [10, r_max]. Zéros de zeta : data/zeta_zeros_1500.csv (1070 zéros, t <= 1500).
But : savoir si l'écart observé pour zeta (w ~ 0,7 avec 300 zéros) tient aux basses hauteurs.
Sorties : data/zero_difference_width_heights.csv, data/zero_difference_width_heights.png.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from zero_reconstruction import nontrivial_zeros

BW, X = 0.05, 2.5
gz = np.sort(pd.read_csv(ROOT / "data" / "zeta_zeros_1500.csv").t.values); g_all = np.concatenate([gz, -gz])
zl = nontrivial_zeros("L_chi5"); zd = nontrivial_zeros("DH")
SETS = {"zeta": (gz, 1.0), "L_chi5": (np.sort(zl.imag[zl.imag > 0]), 5.0),
        "DH": (np.sort(zd[(np.abs(zd.real - 0.5) < 1e-6) & (zd.imag > 0)].imag), 5.0)}
edges = np.arange(-X, X + BW / 2, BW); xc = 0.5 * (edges[1:] + edges[:-1])

def analyse(name, T1, T2, r_max=None):
    S0, q = SETS[name]; S = S0[(S0 >= T1) & (S0 <= T2)]
    i, j = np.triu_indices(len(S), k=1); order = np.argsort(S[j] - S[i]); D = (S[j] - S[i])[order]; Tm = (0.5 * (S[i] + S[j]))[order]
    top = min(D[-1], gz.max()) - 8.0
    if r_max is not None: top = min(top, r_max)
    Zc = gz[(gz > 10) & (gz < top)]
    h = np.zeros(len(xc)); wts = []
    for z in Zc:
        h += np.histogram(D[np.searchsorted(D, z - X - 1):np.searchsorted(D, z + X + 1)] - z, bins=edges)[0]
        wts.append((np.searchsorted(D, z + 8) - np.searchsorted(D, z - 8)) / 16.0 * BW)
    wts = np.array(wts); y = h / wts.sum(); e = np.sqrt(np.maximum(h, 1.0)) / wts.sum(); wn = wts / wts.sum()
    def kernel(w):
        r = Zc[:, None] + xc[None, :]; K = np.zeros_like(r)
        for g in g_all:
            d = r - g; K -= (w * w - d * d) / (w * w + d * d) ** 2
        return wn @ K
    model = lambda _x, c, A, w: c + A * kernel(w)
    p, cov = curve_fit(model, xc, y, p0=(1.0, 0.05, 0.5), sigma=e, absolute_sigma=True, bounds=([0.5, 0.0, 0.15], [1.5, 1.0, 1.5]))
    chi2 = float(np.sum(((y - model(xc, *p)) / e) ** 2) / (len(xc) - 3))
    m5 = lambda _x, c, A: c + A * kernel(0.5)
    q5, _ = curve_fit(m5, xc, y, p0=(1.0, 0.05), sigma=e, absolute_sigma=True)
    sel = (D > 10) & (D < top + 1)
    row = dict(objet=name, T1=T1, T2=T2, r_max=float(top), zeros=len(S), cibles=len(Zc), paires_utiles=int(h.sum()),
               hauteur_moyenne=float(Tm[sel].mean()), rapport_r_sur_T=float((D[sel] / Tm[sel]).mean()),
               largeur_w=float(p[2]), incertitude_w=float(math.sqrt(cov[2, 2])), amplitude_A=float(p[1]), incertitude_A=float(math.sqrt(cov[1, 1])),
               amplitude_attendue=float(np.mean(2.0 / np.log(q * Tm[sel] / (2 * math.pi)) ** 2)), chi2_par_ddl=chi2,
               chi2_si_w_0_5=float(np.sum(((y - m5(xc, *q5)) / e) ** 2) / (len(xc) - 2)))
    return row, (y, e, model(xc, *p))

# (objet, T1, T2, r_max, rôle) — « tranche » : tranches disjointes de largeur 300 ; les autres lignes sont des variantes.
CASES = [("zeta", 0, 300, None, "tranche"), ("zeta", 300, 600, None, "tranche"), ("zeta", 600, 900, None, "tranche"),
         ("zeta", 900, 1200, None, "tranche"), ("zeta", 1200, 1501, None, "tranche"),
         ("L_chi5", 0, 300, None, "tranche"), ("L_chi5", 300, 601, None, "tranche"),
         ("zeta", 0, 542, None, "liste de 300 zéros (V6.3e)"), ("zeta", 0, 1501, None, "liste entière"),
         ("zeta", 700, 1501, 150.0, "paires hautes, cibles basses"),
         ("L_chi5", 0, 601, None, "liste entière"), ("DH", 0, 601, None, "liste entière")]
if __name__ == "__main__":
    rows = []
    for name, T1, T2, rmax, role in CASES:
        r, _ = analyse(name, T1, T2, rmax); r["role"] = role; rows.append(r)
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
    df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "zero_difference_width_heights.csv", index=False)
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=150)
        for name, lab, col, mk in (("zeta", "zéros de ζ", "#1f4e79", "o"), ("L_chi5", "zéros de L(s, χ₅)", "#2e8b57", "s")):
            d = df[(df.objet == name) & (df.role == "tranche")]
            ax.errorbar(d.hauteur_moyenne, d.largeur_w, yerr=d.incertitude_w, fmt=mk + "-", color=col, ms=5, lw=1.2, capsize=3, label=lab)
        ax.axhline(0.5, color="0.4", lw=0.9, ls="--"); ax.text(30, 0.475, "valeur attendue : 0,5", fontsize=8, color="0.3", ha="left")
        ax.set_xlabel("hauteur moyenne des paires de zéros"); ax.set_ylabel("demi-largeur du creux (w)")
        ax.set_title("La largeur du creux descend vers 0,5 quand la hauteur augmente", fontsize=11)
        ax.set_ylim(0.35, 0.85); ax.set_xlim(0, 1450); ax.legend(frameon=False, fontsize=9)
        fig.tight_layout(); fig.savefig(ROOT / "data" / "zero_difference_width_heights.png"); print("figure écrite")
    except Exception as ex:
        print("figure non produite :", ex)
