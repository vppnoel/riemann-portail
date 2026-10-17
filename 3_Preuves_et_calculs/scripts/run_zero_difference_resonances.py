#!/usr/bin/env python3
"""V6.3d — Les différences entre zéros évitent-elles les zéros de zeta ?

Pour un ensemble S d'ordonnées de zéros d'une fonction F et un ensemble de cibles Z, on compte les couples
(gamma_c - gamma_b, z) à distance < delta, et on compare au même comptage pour des cibles décalées au hasard
(décalage uniforme dans [-6, 6], qui conserve la densité lisse). Rapport 1 = aucune structure.
Phénomène connu pour zeta (termes d'ordre inférieur de la corrélation de paires) ; ici on le mesure pour
zeta, L(s, chi_5) et Davenport–Heilbronn (zéros sur la droite, ordonnées positives, mêmes hauteurs).
Sorties : data/zero_difference_resonances.csv, data/zero_difference_profile.csv, data/zero_difference_profile.png.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from explicit_formula import load_zeros
from zero_reconstruction import nontrivial_zeros

rng = np.random.default_rng(20261007)
gz = np.sort(load_zeros()[0])
zl = nontrivial_zeros("L_chi5"); zd = nontrivial_zeros("DH")
L_pos = np.sort(zl.imag[zl.imag > 0]); L_all = np.sort(zl.imag)
D_on = zd[np.abs(zd.real - 0.5) < 1e-6]; D_pos = np.sort(D_on.imag[D_on.imag > 0])

def diffs(S):
    i, j = np.triu_indices(len(S), k=1); return np.sort(S[j] - S[i])
def count(D, Z, delta):
    return int(np.sum(np.searchsorted(D, Z + delta) - np.searchsorted(D, Z - delta)))
def experiment(name, S, Z, delta, rmin=10.0, ndraw=400):
    D = diffs(S); rmax = min(D[-1], Z.max()) - 8.0
    D = D[(D > rmin - 8) & (D < rmax + 8)]; Zc = Z[(Z > rmin) & (Z < rmax)]
    obs = count(D, Zc, delta)
    ctl = np.array([count(D, Zc + rng.uniform(-6, 6, len(Zc)), delta) for _ in range(ndraw)])
    return dict(experience=name, zeros=len(S), cibles=len(Zc), delta=delta, observe=obs, temoin_moyen=float(ctl.mean()),
                rapport=float(obs / ctl.mean()), incertitude=float(ctl.std() / ctl.mean()),
                ecart_en_sigma=float((obs - ctl.mean()) / ctl.std()))
EXPS = [("zeta : différences contre zéros de zeta", gz, gz),
        ("L(chi5), t > 0 : différences contre zéros de zeta", L_pos, gz),
        ("DH sur la droite, t > 0 : différences contre zéros de zeta", D_pos, gz),
        ("L(chi5), tous signes : différences contre zéros de zeta", L_all, gz),
        ("témoin : zeta, différences contre zéros de L(chi5)", gz, L_pos),
        ("témoin : L(chi5), différences contre ses propres zéros", L_pos, L_pos),
        ("témoin : DH, différences contre ses propres zéros", D_pos, D_pos)]
rows = [experiment(n, S, Z, d) for d in (0.05, 0.15) for n, S, Z in EXPS]
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "zero_difference_resonances.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 80)
print(df.to_string(index=False, float_format=lambda v: f"{v:.4g}"))

# ---- profil : rapport en fonction de l'écart x = (gamma_c - gamma_b) - z
edges = np.linspace(-4, 4, 81); xc = 0.5 * (edges[1:] + edges[:-1]); prof = {"x": xc}
for name, S in (("zeta", gz), ("L_chi5", L_pos), ("DH", D_pos)):
    D = diffs(S); rmax = min(D[-1], gz.max()) - 8.0; Zc = gz[(gz > 10) & (gz < rmax)]
    h = np.zeros(len(xc)); bg = 0.0
    for z in Zc:
        h += np.histogram(D[np.searchsorted(D, z - 4.5):np.searchsorted(D, z + 4.5)] - z, bins=edges)[0]
        bg += (np.searchsorted(D, z + 8) - np.searchsorted(D, z - 8)) / 16.0 * (edges[1] - edges[0])
    prof[name] = h / bg
dp = pd.DataFrame(prof); dp.to_csv(ROOT / "data" / "zero_difference_profile.csv", index=False)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(7.5, 4.2), dpi=150)
    for name, lab, col in (("zeta", "zéros de ζ", "#1f4e79"), ("L_chi5", "zéros de L(s, χ₅)", "#2e8b57"), ("DH", "zéros de Davenport–Heilbronn (sur la droite)", "#c0392b")):
        ax.plot(dp.x, dp[name], label=lab, color=col, lw=1.8)
    ax.axhline(1.0, color="0.5", lw=0.8, ls="--"); ax.set_ylim(0.5, 1.3)
    ax.set_xlabel("écart entre une différence de deux zéros et un zéro de ζ"); ax.set_ylabel("fréquence / fréquence attendue")
    ax.set_title("Les différences entre zéros évitent les zéros de ζ", fontsize=11); ax.legend(frameon=False, fontsize=9)
    fig.tight_layout(); fig.savefig(ROOT / "data" / "zero_difference_profile.png"); print("figure écrite")
except Exception as e:
    print("figure non produite :", e)
print(dp.iloc[36:44].to_string(index=False, float_format=lambda v: f"{v:.3f}"))
