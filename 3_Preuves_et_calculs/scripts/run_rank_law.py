#!/usr/bin/env python3
"""V6.7 — Loi de rang des compressions de Weil (côté zéros) pour zeta, L(s, chi_5), DH et les témoins F6, E2.

Dans le Modèle réduit, la forme de Weil fenêtrée est positive tant que la fenêtre ne dépasse pas le nombre de zéros
(2g), puis exactement singulière. Ici : compression de dimension m (fonctions tentes modulées autour de T, pas 0,6,
demi-largeur W), Z_ij = somme_rho H_i(gamma) H_j(gamma), problème Z v = lambda G v.
N_bande = nombre de zéros atteints (gamma identifié à -gamma, fonctions de test paires) dont |Re gamma| est dans
[T - (m-1) 0,3 - 2 pi/W ; T + (m-1) 0,3 + 2 pi/W] (lobe principal des tentes).
Question : lambda_min s'effondre-t-il quand m dépasse N_bande, de la même façon pour tous les objets ?
Sorties : data/rank_law.csv, data/rank_law.png.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
from scipy.linalg import eigh
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from dual_lock import tent_fourier
from dual_lock_audit import gram_matrix_closed as gram_matrix
from zero_reconstruction import nontrivial_zeros
from lock_witnesses import polynomial_zero_gammas

STEP, MMAX = 0.6, 25
D = ROOT / "data"

def gammas(kind):
    if kind in ("zeta", "F6", "E2"):
        gz = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; g = np.concatenate([gz, -gz]).astype(complex)
        if kind == "zeta": return g
        pz = polynomial_zero_gammas(kind, 1600.0); return np.concatenate([g, pz["on"].astype(complex), pz["off"]])
    z = nontrivial_zeros(kind); return -1j * (z - 0.5)

def classes(g):
    """Représentants de gamma modulo +-gamma (fonctions de test paires)."""
    rep = np.where((g.real > 1e-12) | ((np.abs(g.real) <= 1e-12) & (g.imag >= 0)), g, -g)
    key = np.round(rep.real, 7) + 1j * np.round(rep.imag, 7); _, idx = np.unique(key, return_index=True)
    return rep[np.sort(idx)]

PLAN = {"zeta": (100.0, 300.0, 600.0, 1000.0, 1400.0), "L_chi5": (85.7, 100.0, 114.2, 166.5, 176.7, 300.0, 500.0), "DH": (85.7, 100.0, 114.2, 166.5, 176.7, 300.0, 500.0),
        "F6": (100.0, 300.0, 600.0), "E2": (100.0, 300.0, 600.0)}
WIDTHS = (2.5, 5.0, 10.0)

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    df = pd.read_csv(D / "rank_law.csv")
    cols = {"zeta": "#1f4e79", "L_chi5": "#2e8b57", "F6": "#e67e22", "DH": "#c0392b", "E2": "#8e44ad"}
    labs = {"zeta": "ζ", "L_chi5": "L(s, χ₅)", "F6": "F6 (sans produit d'Euler, zéros sur la droite)", "DH": "DH", "E2": "E2 (produit d'Euler, zéros hors droite)"}
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
    ax = axs[0]
    for k in ("zeta", "L_chi5", "F6"):
        d = df[(df.objet == k)]; ax.semilogy(d.m - d.N_bande, np.maximum(d.lam_rel, 1e-16), "o", ms=2.6, alpha=0.55, color=cols[k], label=labs[k])
    ax.axvline(0.5, color="0.3", ls="--", lw=0.9); ax.set_xlabel("dimension m − nombre de zéros atteints N_bande")
    ax.set_ylabel("λ_min relatif (λ_min / moyenne des |valeurs propres|)"); ax.set_ylim(1e-16, 3)
    ax.set_title("Zéros sur la droite : λ_min chute dès que m dépasse les zéros atteints", fontsize=9.5); ax.legend(frameon=False, fontsize=7.5, loc="lower left")
    ax = axs[1]
    for k in ("L_chi5", "DH", "E2"):
        d = df[df.objet == k]; s = np.sign(d.lam_rel) * np.log10(1 + np.abs(d.lam_rel) / 1e-12)
        ax.plot(d.m - d.N_bande, s, "o", ms=2.6, alpha=0.55, color=cols[k], label=labs[k])
    ax.axhline(0, color="0.3", lw=0.8); ax.set_xlabel("dimension m − nombre de zéros atteints N_bande")
    ax.set_ylabel("signe × log₁₀(1 + |λ_min relatif| / 10⁻¹²)")
    ax.set_title("Les faux jumeaux passent sous zéro ; les vrais s'arrêtent à zéro", fontsize=10); ax.legend(frameon=False, fontsize=7.5, loc="lower left")
    fig.tight_layout(); fig.savefig(D / "rank_law.png"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    t0 = time.time(); G_cache = {}; rows = []
    for kind, Ts in PLAN.items():
        g_all = gammas(kind); reps = classes(g_all)
        for T in Ts:
            for W in WIDTHS:
                key = (T, W)
                fr_max = T + STEP * (np.arange(MMAX) - (MMAX - 1) / 2)
                if key not in G_cache: G_cache[key] = gram_matrix(fr_max, W)
                Gm = G_cache[key]
                sel = np.abs(np.abs(g_all.real) - T) < 60.0 + 3 * (MMAX * STEP)           # zéros lointains : contribution négligeable (tentes en 1/t^2)
                Hm = np.array([tent_fourier(g_all[sel], W, xi) for xi in fr_max])
                Zm = np.real(Hm @ Hm.T)
                tail = np.array([tent_fourier(g_all[~sel], W, xi) for xi in fr_max]); Ztail = np.real(tail @ tail.T)
                for m in range(3, MMAX + 1, 2):
                    i0 = (MMAX - m) // 2; ix = slice(i0, i0 + m)
                    Z = Zm[ix, ix] + Ztail[ix, ix]; G = Gm[ix, ix]
                    if np.linalg.cond(G) > 1e10: continue                                    # base trop mal conditionnée : non mesuré
                    ev = eigh(Z, G, eigvals_only=True)
                    half = (m - 1) * STEP / 2 + 2 * math.pi / W
                    nb = int(np.sum(np.abs(np.abs(reps.real) - T) <= half))
                    off = int(np.sum((np.abs(np.abs(reps.real) - T) <= half) & (np.abs(reps.imag) > 1e-6)))
                    rows.append(dict(objet=kind, T=T, W=W, m=m, N_bande=nb, hors_droite_dans_la_bande=off, lam_min=float(ev[0]),
                                     lam_rel=float(ev[0] / np.mean(np.abs(ev))), negatives=int(np.sum(ev < -1e-9 * np.max(np.abs(ev)))),
                                     cond_G=float(np.linalg.cond(G)), part_lointaine=float(np.linalg.norm(Ztail[ix, ix]) / np.linalg.norm(Z))))
                print(f"{kind} T={T} W={W} ({time.time() - t0:.0f} s)", flush=True)
    df = pd.DataFrame(rows); df.to_csv(D / "rank_law.csv", index=False)
    fits = []
    for (k, W), d in df[df.objet.isin(["zeta", "L_chi5", "F6"])].groupby(["objet", "W"]):
        e = d[(d.m - d.N_bande >= 1) & (d.lam_rel > 1e-15)]
        if len(e) >= 4:
            p = np.polyfit(e.m - e.N_bande, np.log10(e.lam_rel), 1)
            fits.append(dict(objet=k, W=W, points=len(e), pente_log10_par_dimension=p[0], ordonnee=p[1],
                             dispersion=float(np.std(np.log10(e.lam_rel) - np.polyval(p, e.m - e.N_bande)))))
    pd.DataFrame(fits).to_csv(D / "rank_law_fits.csv", index=False); print(pd.DataFrame(fits).to_string(index=False))
    for k in ("DH", "E2"):
        d = df[df.objet == k]; print(k, ": fenêtres avec une valeur négative :", int((d.lam_rel < 0).sum()), "/", len(d),
                                    "; première dimension négative par fenêtre :", d[d.lam_rel < 0].groupby(["T", "W"]).m.min().to_dict())
    print("objets à zéros sur la droite : valeurs négatives :", int((df[df.objet.isin(["zeta", "L_chi5", "F6"])].lam_rel < -1e-13).sum()))
    # portée : distance de la fenêtre au zéro hors droite de DH le plus proche, et première dimension où la forme devient négative
    gd = gammas("DH"); offt = np.unique(np.round(np.abs(gd.real[np.abs(gd.imag) > 1e-6]), 4)); por = []
    for (T, W), d in df[df.objet == "DH"].groupby(["T", "W"]):
        neg = d[d.lam_rel < 0].sort_values("m"); dist = float(np.min(np.abs(offt - T)))
        first = neg.iloc[0] if len(neg) else None
        por.append(dict(T=T, W=W, distance_au_zero_hors_droite=dist, m_max_mesure=int(d.m.max()),
                        premiere_dimension_negative=(int(first.m) if first is not None else None),
                        demi_bande_a_ce_m=((int(first.m) - 1) * STEP / 2 + 2 * math.pi / W) if first is not None else None,
                        zeros_atteints_a_ce_m=(int(first.N_bande) if first is not None else None)))
    pd.DataFrame(por).to_csv(D / "rank_law_reach.csv", index=False); print(pd.DataFrame(por).to_string(index=False))
    figure(); print(f"total {time.time() - t0:.0f} s")
