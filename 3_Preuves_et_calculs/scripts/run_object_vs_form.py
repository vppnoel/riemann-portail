#!/usr/bin/env python3
"""V6.7 — Seuil de l'objet contre seuil de la forme, entre L(s, chi_5) et Davenport–Heilbronn.

Seuil de la forme (document 26) : interpolation des matrices (1 - tau) M_L + tau M_DH dans une fenêtre (T, W, m) ;
forme close tau_c = -1/mu_min, (M_DH - M_L) v = mu M_L v.
Seuil de l'objet : interpolation des fonctions F_theta = (1 - theta)(+-A) + theta DH (symétrie de Hardy conservée) ;
theta où la paire de zéros qui devient hors droite dans DH quitte la droite (extremum de theta*, sans fenêtre).
Loi du rayon structuré selon le nombre de zéros : Modèle réduit (rayon de l'objet contre 2g), familles modulo 5
et modulo 7 (plage de survie contre le nombre de zéros jusqu'à T).
Sorties : data/family_mod5_intervals.csv, data/object_vs_form.csv, data/structured_scaling.csv, data/object_vs_form.png.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
from scipy.optimize import brentq, minimize_scalar
from scipy.linalg import eigh
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from family_mod5 import hardy, F_path, PHI
D = ROOT / "data"
TMAX, DT, STEP = 205.0, 0.01, 0.6
WIDTHS = (2.0, 2.5, 3.5, 5.0, 7.0, 10.0)

def density(t): return math.log(5 * max(t, 1.0) / (2 * math.pi)) / (2 * math.pi)

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    of = pd.read_csv(D / "object_vs_form.csv"); sc = pd.read_csv(D / "structured_scaling.csv")
    cols = ["#1f4e79", "#2e8b57", "#c0392b", "#8e44ad", "#e67e22"]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.3), dpi=150)
    ax = axs[0]
    for (t0, d), col in zip(of.groupby("t_zero_DH"), cols):
        d = d.sort_values("W"); ax.semilogy(d.W, d.seuil_forme, "o-", color=col, ms=4, lw=1.3, label=f"forme, t = {t0:.1f}".replace(".", ","))
        ax.axhline(d.seuil_objet_plus.iloc[0], color=col, lw=1.0, ls="--")
    ax.plot([], [], color="0.4", ls="--", label="objet (même couleur) : sans fenêtre")
    ax.set_xlabel("demi-largeur W de la fenêtre"); ax.set_ylabel("seuil τ (forme) ou θ (objet)"); ax.set_ylim(1e-5, 2)
    ax.set_title("L(s, χ₅) → DH : le seuil de la forme dépend de la fenêtre, pas celui de l'objet", fontsize=9.5); ax.legend(frameon=False, fontsize=7, loc="lower left", ncol=1)
    ax = axs[1]
    for (src, d), col, mk in zip(sc.groupby("source", sort=False), cols, ("o", "s", "^", "D", "v")):
        ax.loglog(d.nombre_de_zeros, d.rayon_relatif, mk + "-", color=col, ms=4, lw=1.2, label=src)
    ax.set_xlabel("nombre de zéros (2g pour une courbe ; jusqu'à T pour une famille)"); ax.set_ylabel("rayon de l'objet (normalisé à sa première valeur)")
    ax.set_title("Le rayon de l'objet décroît avec le nombre de zéros", fontsize=9.5); ax.legend(frameon=False, fontsize=7.5)
    fig.tight_layout(); fig.savefig(D / "object_vs_form.png"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    t0 = time.time()
    tg = np.arange(0.3, TMAX + DT / 2, DT); H = np.array([hardy(float(t)) for t in tg]); ZA, ZD, defect = H[:, 0], H[:, 1], H[:, 2]
    print(f"grille : {len(tg)} points ; défaut d'imaginaire max {defect.max():.1e} ; {time.time() - t0:.0f} s", flush=True)
    ref = lambda f, i: brentq(f, tg[i], tg[i + 1], xtol=1e-12)
    za_f = lambda t: hardy(t)[0]; zd_f = lambda t: hardy(t)[1]
    zA = np.array([ref(za_f, i) for i in np.flatnonzero(np.sign(ZA[1:]) * np.sign(ZA[:-1]) < 0)])
    zD = np.array([ref(zd_f, i) for i in np.flatnonzero(np.sign(ZD[1:]) * np.sign(ZD[:-1]) < 0)])
    print(f"zéros sur la droite pour t <= {TMAX:.0f} : A {len(zA)}, DH {len(zD)}", flush=True)
    rows = []
    for sign in (+1, -1):
        th = lambda t, s=sign: (lambda a, d: a / (a - s * d))(*hardy(t)[:2])
        Dd = ZA - sign * ZD; poles = tg[np.flatnonzero(np.sign(Dd[1:]) * np.sign(Dd[:-1]) < 0)]
        for k in range(len(zA) - 1):
            a, b = zA[k], zA[k + 1]; has_pole = bool(np.any((poles > a) & (poles < b)))
            row = dict(trajet="+" if sign > 0 else "-", t_gauche=a, t_droite=b, ecart_normalise=(b - a) * density(0.5 * (a + b)), pole=has_pole)
            if not has_pole:
                sg = 1.0 if th(0.5 * (a + b)) > 0 else -1.0
                r = minimize_scalar(lambda t: -sg * th(t), bounds=(a + 1e-9, b - 1e-9), method="bounded", options=dict(xatol=1e-10))
                row.update(seuil=float(sg * -r.fun), t_rencontre=float(r.x))
            rows.append(row)
    iv = pd.DataFrame(rows); iv.to_csv(D / "family_mod5_intervals.csv", index=False)
    for tr in ("+", "-"):
        e = iv[(iv.trajet == tr)].dropna(subset=["seuil"]); lost = e[(e.seuil > 0) & (e.seuil < 1) & (e.t_droite <= 200)]
        print(f"trajet {tr} : paires qui quittent la droite avant DH (t <= 200) : {len(lost)} ; à t = "
              + ", ".join(f"{x:.2f} (θ = {s:.3f})" for x, s in zip(lost.t_rencontre, lost.seuil)), flush=True)
    # ---------------- seuil de la forme aux hauteurs des zéros hors droite de DH (côté zéros, dimension 9)
    from run_tau_threshold import zero_side, GL_, GD_
    from dual_lock_audit import gram_matrix_closed as gram_matrix
    dh = pd.read_csv(D / "dh_zeros_600.csv"); off_t = sorted({round(float(t), 6) for t, s in zip(dh.t, dh.sigma) if abs(s - 0.5) > 1e-6 and t <= 200})
    out = []
    for t0z in off_t:
        e = iv.dropna(subset=["seuil"])
        def obj(tr):
            c = e[(e.trajet == tr) & (e.seuil > 0) & (e.seuil < 1) & (np.abs(e.t_rencontre - t0z) < 1.5)]
            return float(c.seuil.iloc[0]) if len(c) else float("nan")
        for W in WIDTHS:
            fr = t0z + STEP * (np.arange(9) - 4.0); G = gram_matrix(fr, W)
            ZL, _ = zero_side(fr, W, GL_); ZDm, _ = zero_side(fr, W, GD_)
            mu = eigh(ZDm - ZL, ZL, eigvals_only=True)[0]; lamL = float(eigh(ZL, G, eigvals_only=True)[0])
            out.append(dict(t_zero_DH=t0z, W=W, seuil_forme=(-1 / mu if mu < 0 else float("nan")), lam_min_L=lamL,
                            seuil_objet_plus=obj("+"), seuil_objet_moins=obj("-")))
        print(out[-1], flush=True)
    of = pd.DataFrame(out); of.to_csv(D / "object_vs_form.csv", index=False)
    # ---------------- loi du rayon de l'objet selon le nombre de zéros
    sc = []
    mc = pd.read_csv(D / "stability_model_curves.csv")
    for q in (3, 5, 7):
        g = mc[mc.q == q].groupby("g").rayon_objet.median()
        for gg, v in g.items(): sc.append(dict(source=f"Modèle réduit, F_{q} (rayon médian)", nombre_de_zeros=2 * gg, rayon=v))
    s7 = pd.read_csv(D / "family_mod7_survival.csv")
    for _, r in s7.iterrows(): sc.append(dict(source="famille modulo 7 (plage de survie)", nombre_de_zeros=r.zeros, rayon=min(r.theta_plus, -r.theta_moins)))
    e = iv[iv.trajet == "+"].dropna(subset=["seuil"])
    for T in (25, 50, 75, 100, 125, 150, 175, 200):
        x = e[e.t_droite <= T]; pos = x[x.seuil > 0].seuil; neg = x[x.seuil < 0].seuil
        sc.append(dict(source="famille modulo 5, trajet + (plage de survie)", nombre_de_zeros=int(np.sum(zA <= T)),
                       rayon=min(pos.min() if len(pos) else np.inf, -neg.max() if len(neg) else np.inf)))
    sc = pd.DataFrame(sc); sc["rayon_relatif"] = sc.groupby("source").rayon.transform(lambda v: v / v.iloc[0])
    fits = []
    for src, d in sc.groupby("source", sort=False):
        d = d[np.isfinite(d.rayon) & (d.rayon > 0)]; p = np.polyfit(np.log(d.nombre_de_zeros), np.log(d.rayon), 1); fits.append((src, p[0]))
    sc.to_csv(D / "structured_scaling.csv", index=False)
    print("pente log(rayon) / log(nombre de zéros) :", ", ".join(f"{s} : {p:.2f}" for s, p in fits), flush=True)
    figure(); print(f"total {time.time() - t0:.0f} s")
