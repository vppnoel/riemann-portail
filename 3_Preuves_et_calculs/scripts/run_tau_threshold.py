#!/usr/bin/env python3
"""V6.4 — Test prioritaire de l'Atlas des métaphores : le seuil tau_c entre L(s, chi_5) et Davenport–Heilbronn.

    M_T(tau) = M_inf(T) + M_q(T) + (1 - tau) M_loc^L(T) + tau M_loc^DH(T)   (même conducteur, même facteur gamma)
             = (1 - tau) M^L(T) + tau M^DH(T),
    M_T(tau) v = lambda G v,   tau_c : lambda_min(T, tau_c) = 0.

Trois calculs indépendants de M^L et M^DH :
  A. côté premiers, quadrature adaptative (dual_lock.compression_accurate) ;
  B. côté premiers, Gauss–Legendre (dual_lock_audit.compression_components_independent) ;
  C. côté zéros : Z_ij = somme_rho H_i(gamma_rho) H_j(gamma_rho), listes de zéros jusqu'à |t| = 600.
Compléments (côté zéros) : seuil en fonction de la demi-largeur W du support ; même test entre zeta et
les témoins E2 (produit d'Euler, zéros hors droite) et F6 (pas de produit d'Euler, zéros sur la droite).
Sorties : data/tau_threshold.csv (seuils), data/tau_threshold_curve.csv (lambda_min en fonction de tau),
          data/tau_threshold_2d.csv (carte tau, delta), data/tau_threshold_width.csv, data/tau_threshold_witnesses.csv,
          data/tau_threshold.png.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
from scipy.linalg import eigh
from scipy.optimize import brentq
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from dual_lock import compression_accurate, tent_fourier
from dual_lock_audit import gram_matrix, compression_components_independent
from zero_reconstruction import nontrivial_zeros
from lock_witnesses import polynomial_zero_gammas

STEP = 0.6
WINDOWS = ((86.0, 2.5), (113.0, 2.5), (167.0, 3.5), (176.0, 2.5))
zl = nontrivial_zeros("L_chi5"); zd = nontrivial_zeros("DH")
GL_ = zl.imag.astype(complex)                       # zéros de L(s, chi), tous sur la droite
GD_ = -1j * (zd - 0.5)                              # gamma = -i (rho - 1/2), complexes pour les zéros hors droite
OFF = np.abs(zd.real - 0.5) > 1e-6

def freqs(T, m): return T + STEP * (np.arange(m, dtype=float) - (m - 1) / 2.0)
def zero_side(fr, W, gam):
    H = np.array([tent_fourier(gam, W, xi) for xi in fr]); return np.real(H @ H.T), H
def lam_min(ML, MD, G, tau): return float(eigh((1 - tau) * ML + tau * MD, G, eigvals_only=True)[0])
def threshold(ML, MD, G):
    f = lambda t: lam_min(ML, MD, G, t)
    if f(0.0) <= 0 or f(1.0) >= 0: return float("nan")
    return float(brentq(f, 0.0, 1.0, xtol=1e-12))

def figure():
    """Trace data/tau_threshold.png à partir des fichiers CSV (appel direct : python scripts/run_tau_threshold.py --figure)."""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    dc = pd.read_csv(ROOT / "data" / "tau_threshold_curve.csv"); dw = pd.read_csv(ROOT / "data" / "tau_threshold_width.csv").dropna(subset=["tau_c"])
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.9), dpi=150)
    d86 = dc[dc["T"] == 86.0]
    for m, col in ((5, "#1f4e79"), (9, "#2e8b57"), (13, "#c0392b")):
        d = d86[d86.dimension == m]; axs[0].plot(d.tau, d.lam_min, color=col, lw=1.6, label=f"dimension {m}")
    axs[0].axhline(0, color="0.4", lw=0.8, ls="--"); axs[0].set_xlabel("τ (0 = L(s, χ₅), 1 = Davenport–Heilbronn)")
    axs[0].set_ylabel("plus petite valeur propre λ_min"); axs[0].set_title("Fenêtre T = 86 : λ_min en fonction de τ", fontsize=10); axs[0].legend(frameon=False, fontsize=9)
    axs[1].semilogy(dw.demi_largeur, dw.tau_c, "o-", color="#1f4e79", ms=5, lw=1.4)
    for w, t in zip(dw.demi_largeur, dw.tau_c):
        axs[1].annotate(f"{t:.2g}".replace(".", ","), (w, t), textcoords="offset points", xytext=(7, 4), fontsize=8)
    axs[1].set_xlabel("demi-largeur W du support des fonctions de test"); axs[1].set_ylabel("seuil τ_c (échelle logarithmique)")
    axs[1].set_title("Le seuil τ_c tend vers 0 quand la fenêtre s'élargit", fontsize=10); axs[1].set_xlim(1.5, 12)
    fig.tight_layout(); fig.savefig(ROOT / "data" / "tau_threshold.png"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    rows, curves, map2d = [], [], []
    for T, W in WINDOWS:
        for m in (5, 7, 9, 11, 13):
            fr = freqs(T, m); G = gram_matrix(fr, W); cond = float(np.linalg.cond(G))
            ZL, _ = zero_side(fr, W, GL_); ZD, HD = zero_side(fr, W, GD_)
            row = dict(T=T, demi_largeur=W, dimension=m, cond_G=cond, lam_L=lam_min(ZL, ZD, G, 0.0), lam_DH=lam_min(ZL, ZD, G, 1.0),
                       tau_c_zeros=threshold(ZL, ZD, G))
            # attribution au seuil : lambda = (1 - tau) a + tau b, a = part de L (>= 0), b = part de DH
            tc = row["tau_c_zeros"]
            if tc == tc:
                lam, V = eigh((1 - tc) * ZL + tc * ZD, G); v = V[:, 0]
                a = float(v @ ZL @ v); b = float(v @ ZD @ v)
                b_off = float(np.real(np.sum((v @ HD[:, OFF]) ** 2))); b_on = float(np.real(np.sum((v @ HD[:, ~OFF]) ** 2)))
                row.update(part_L=a, part_DH_sur_droite=b_on, part_DH_hors_droite=b_off, tau_c_par_attribution=a / (a - b))
            # côté premiers : deux quadratures (dimensions où le coût reste raisonnable)
            if m <= 9 and W <= 2.5:
                t0 = time.time()
                _, ML = compression_accurate(T, "L_pair_chi5", half_width=W, dimension=m, frequency_step=STEP)
                _, MD = compression_accurate(T, "DH", half_width=W, dimension=m, frequency_step=STEP)
                row.update(tau_c_premiers_quad=threshold(ML, MD, G), ecart_rel_L=float(np.linalg.norm(ML - ZL) / np.linalg.norm(ZL)),
                           ecart_rel_DH=float(np.linalg.norm(MD - ZD) / np.linalg.norm(ZD)))
                if m <= 7:
                    _, cL, G2 = compression_components_independent(T, "L_pair_chi5", half_width=W, dimension=m, frequency_step=STEP)
                    _, cD, _ = compression_components_independent(T, "DH", half_width=W, dimension=m, frequency_step=STEP)
                    row["tau_c_premiers_gauss"] = threshold(cL["total"], cD["total"], G2)
                row["secondes_cote_premiers"] = time.time() - t0
            rows.append(row); print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
            if m in (5, 9, 13):
                for tau in np.linspace(0, 1, 51):
                    curves.append(dict(T=T, dimension=m, tau=float(tau), lam_min=lam_min(ZL, ZD, G, float(tau))))
            if m == 5:      # carte à deux clés : (1 + delta) M_q ; M_q = log(q/pi) F0 et F0 = G
                c = math.log(5.0 / math.pi)
                for tau in (0.0, 0.25, 0.5, 0.75, 1.0):
                    for delta in (-1.0, -0.5, 0.0, 0.5, 1.0):
                        direct = float(eigh((1 - tau) * ZL + tau * ZD + delta * c * G, G, eigvals_only=True)[0])
                        map2d.append(dict(T=T, tau=tau, delta=delta, lam_min_direct=direct,
                                          lam_min_par_translation=lam_min(ZL, ZD, G, tau) + delta * c))
    # ---- seuil selon la demi-largeur W du support (fenêtre centrée sur le zéro hors droite 0,8085 + 85,699i)
    wrows = []
    for W in (1.5, 2.0, 2.5, 3.5, 5.0, 7.0, 10.0):
        fr = freqs(85.7, 9); G = gram_matrix(fr, W)
        ZL, _ = zero_side(fr, W, GL_); ZD, _ = zero_side(fr, W, GD_)
        wrows.append(dict(T=85.7, dimension=9, demi_largeur=W, n_max_cote_premiers=int(math.exp(2 * W)), cond_G=float(np.linalg.cond(G)),
                          lam_L=lam_min(ZL, ZD, G, 0.0), lam_DH=lam_min(ZL, ZD, G, 1.0), tau_c=threshold(ZL, ZD, G)))
        print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in wrows[-1].items()}, flush=True)
    pd.DataFrame(wrows).to_csv(ROOT / "data" / "tau_threshold_width.csv", index=False)
    # ---- autres témoins : zeta -> E2 et zeta -> F6 (interpolation des formes entières, conducteurs différents)
    gz = pd.read_csv(ROOT / "data" / "zeta_zeros_1500.csv").t.values; gz = np.concatenate([gz, -gz]).astype(complex)
    trows = []
    for kind in ("E2", "F6"):
        pz = polynomial_zero_gammas(kind, 20000.0); gk = np.concatenate([gz, pz["on"].astype(complex), pz["off"]])
        for T in (18.0, 27.0, 45.0):
            fr = freqs(T, 5); G = gram_matrix(fr, 2.5)
            Z0, _ = zero_side(fr, 2.5, gz); Z1, _ = zero_side(fr, 2.5, gk)
            grid = [lam_min(Z0, Z1, G, float(t)) for t in np.linspace(0, 1, 101)]
            trows.append(dict(temoin=kind, T=T, lam_zeta=grid[0], lam_temoin=grid[-1], lam_min_sur_le_trajet=min(grid), tau_c=threshold(Z0, Z1, G)))
            print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in trows[-1].items()}, flush=True)
    pd.DataFrame(trows).to_csv(ROOT / "data" / "tau_threshold_witnesses.csv", index=False)
    df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "tau_threshold.csv", index=False)
    dc = pd.DataFrame(curves); dc.to_csv(ROOT / "data" / "tau_threshold_curve.csv", index=False)
    pd.DataFrame(map2d).to_csv(ROOT / "data" / "tau_threshold_2d.csv", index=False)
    figure()
