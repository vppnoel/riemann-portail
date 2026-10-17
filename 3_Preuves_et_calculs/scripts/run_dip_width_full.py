#!/usr/bin/env python3
"""V6.3e — La largeur du creux mesure-t-elle la distance des zéros à la droite Re s = 1 ?

Heuristique (terme diagonal de la corrélation de paires) : près d'un zéro de zeta d'ordonnée gamma,
la fréquence des différences de zéros suit  c + A * K_w(r),
    K_w(r) = - somme_rho Re 1 / (w + i (r - gamma_rho))^2,
où w est la distance des zéros de zeta à la droite Re s = 1 : w = 1 - beta = 1/2 sous RH.
On ajuste (c, A, w) sur le profil empilé, K_w étant calculé avec TOUS les zéros voisins, pour trois
fenêtres d'ajustement. (scripts/run_dip_width.py fait le même ajustement avec un seul profil isolé.)
Lecture : w est la « largeur de l'ombre » des zéros de zeta vue par les différences de zéros hauts.
Sorties : data/zero_difference_width.csv, data/zero_difference_width_profile.csv, data/zero_difference_width.png.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
from scipy.optimize import curve_fit
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from explicit_formula import load_zeros
from zero_reconstruction import nontrivial_zeros

BW = 0.05
gz = np.sort(load_zeros()[0]); g_all = np.concatenate([gz, -gz])
zl = nontrivial_zeros("L_chi5"); zd = nontrivial_zeros("DH")
SETS = {"zeta": (gz, 1.0), "L_chi5": (np.sort(zl.imag[zl.imag > 0]), 5.0),
        "DH": (np.sort(zd[(np.abs(zd.real - 0.5) < 1e-6) & (zd.imag > 0)].imag), 5.0)}

def analyse(X):
    edges = np.arange(-X, X + BW / 2, BW); xc = 0.5 * (edges[1:] + edges[:-1])
    def stacked_profile(S):
        """Profil empilé des différences autour des zéros de zeta ; renvoie aussi cibles et poids."""
        i, j = np.triu_indices(len(S), k=1); D = np.sort(S[j] - S[i])
        rmax = min(D[-1], gz.max()) - 8.0; Zc = gz[(gz > 10) & (gz < rmax)]
        h = np.zeros(len(xc)); wts = []
        for z in Zc:
            h += np.histogram(D[np.searchsorted(D, z - X - 1):np.searchsorted(D, z + X + 1)] - z, bins=edges)[0]
            wts.append((np.searchsorted(D, z + 8) - np.searchsorted(D, z - 8)) / 16.0 * BW)
        wts = np.array(wts)
        return h / wts.sum(), np.sqrt(np.maximum(h, 1.0)) / wts.sum(), Zc, wts / wts.sum()
    def kernel(w, Zc, wts):
        """K_w empilé avec les mêmes poids que les données (tous les zéros de zeta, des deux signes)."""
        r = Zc[:, None] + xc[None, :]
        K = np.zeros_like(r)
        for g in g_all:
            d = r - g
            K -= (w * w - d * d) / (w * w + d * d) ** 2
        return wts @ K
    rows, prof = [], {"x": xc}
    for name, (S, q) in SETS.items():
        y, e, Zc, wts = stacked_profile(S)
        model = lambda _x, c, A, w: c + A * kernel(w, Zc, wts)
        p, cov = curve_fit(model, xc, y, p0=(1.0, 0.05, 0.5), sigma=e, absolute_sigma=True, bounds=([0.5, 0.0, 0.15], [1.5, 1.0, 1.5]))
        chi2 = float(np.sum(((y - model(xc, *p)) / e) ** 2) / (len(xc) - 3))
        row = dict(objet=name, fenetre=X, zeros=len(S), cibles=len(Zc), largeur_w=p[2], incertitude_w=math.sqrt(cov[2, 2]),
                   amplitude_A=p[1], incertitude_A=math.sqrt(cov[1, 1]), niveau_c=p[0], chi2_par_ddl=chi2)
        for wf in (0.3, 0.5, 0.7):       # largeur imposée : ce que donneraient des zéros à beta = 0,7 / 0,5 / 0,3
            m2 = lambda _x, c, A: c + A * kernel(wf, Zc, wts)
            q2, _ = curve_fit(m2, xc, y, p0=(1.0, 0.05), sigma=e, absolute_sigma=True)
            row[f"chi2_si_w_{wf}"] = float(np.sum(((y - m2(xc, *q2)) / e) ** 2) / (len(xc) - 2))
        # amplitude attendue (ordre de grandeur) : 2 / log^2(q T / 2 pi), moyennée sur les hauteurs T des paires
        i, j = np.triu_indices(len(S), k=1); sel = (S[j] - S[i] > 10) & (S[j] - S[i] < Zc.max() + 1)
        T = 0.5 * (S[i][sel] + S[j][sel]); row["amplitude_attendue"] = float(np.mean(2.0 / np.log(q * T / (2 * math.pi)) ** 2))
        rows.append(row); prof[name] = y; prof[name + "_erreur"] = e; prof[name + "_modele"] = model(xc, *p)
    return rows, prof

allrows = []
for X in (1.5, 2.5, 3.5):
    rows, prof = analyse(X); allrows += rows
    if X == 2.5: dp = pd.DataFrame(prof)
da = pd.DataFrame(allrows); da.to_csv(ROOT / "data" / "zero_difference_width.csv", index=False)
dp.to_csv(ROOT / "data" / "zero_difference_width_profile.csv", index=False)
df = da[da.fenetre == 2.5]
pd.set_option("display.width", 250); print(da.to_string(index=False, float_format=lambda v: f"{v:.4g}"))
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.4), dpi=150, sharey=True)
    for ax, (name, lab, col) in zip(axs, (("zeta", "zéros de ζ", "#1f4e79"), ("L_chi5", "zéros de L(s, χ₅)", "#2e8b57"), ("DH", "zéros de DH (sur la droite)", "#c0392b"))):
        r = df[df.objet == name].iloc[0]
        ax.errorbar(dp.x, dp[name], yerr=dp[name + "_erreur"], fmt=".", ms=3, lw=0.6, color=col, alpha=0.7, label="mesure")
        ax.plot(dp.x, dp[name + "_modele"], color="k", lw=1.3, label=f"modèle, w = {r.largeur_w:.2f} ± {r.incertitude_w:.2f}".replace(".", ","))
        ax.axhline(1.0, color="0.6", lw=0.7, ls="--"); ax.set_title(lab, fontsize=10); ax.set_xlabel("écart à un zéro de ζ"); ax.legend(frameon=False, fontsize=8, loc="lower right")
    axs[0].set_ylabel("fréquence / fréquence attendue"); fig.tight_layout(); fig.savefig(ROOT / "data" / "zero_difference_width.png"); print("figure écrite")
except Exception as ex:
    print("figure non produite :", ex)
