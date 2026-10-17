#!/usr/bin/env python3
"""V6.5 — Carte des disparitions de paires dans la famille F_theta = (1 - theta) L(s, chi_3 mod 7) + theta f_7.

Même équation fonctionnelle pour tout theta ; produit d'Euler seulement en theta = 0.
Z_theta(t) = (1 - theta) Z_0(t) + theta Z_1(t) : les zéros sur la droite à hauteur t vérifient
theta = theta*(t) = Z_0 / (Z_0 - Z_1). Entre deux zéros consécutifs de Z_0, theta* garde un signe ; s'il n'y a pas de
pôle (Z_0 = Z_1) dans l'intervalle, theta* y forme une bosse de hauteur h : les deux zéros se rejoignent et quittent
la droite quand theta atteint h. Ces seuils sont intrinsèques (aucune fenêtre, aucune base).
Sorties : data/family_mod7_checks.csv, _intervals.csv, _survival.csv, _proportion.csv, _pair.csv, _imprint.csv,
          _diagram.csv, family_mod7.png.
"""
from pathlib import Path
import sys, math, cmath, time
import numpy as np, pandas as pd
from scipy.optimize import brentq, minimize_scalar
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from family_mod7 import F0, F1, F_theta, completed, hardy, coefficients, vartheta
from zero_reconstruction import hurwitz_zeta

TMAX, DT = 1000.0, 0.01

def theta_star(t):
    z0, z1 = hardy(t); return z0 / (z0 - z1)
def Z(t, theta):
    z0, z1 = hardy(t); return (1 - theta) * z0 + theta * z1
def density(t): return math.log(7 * max(t, 1.0) / (2 * math.pi)) / (2 * math.pi)
def winding_theta(theta, y0, y1, h=0.01, x0=-0.9, x1=4.0):
    pts = []
    for a, b in ((complex(x0, y0), complex(x1, y0)), (complex(x1, y0), complex(x1, y1)), (complex(x1, y1), complex(x0, y1)), (complex(x0, y1), complex(x0, y0))):
        n = max(8, int(abs(b - a) / h)); pts += [a + (b - a) * k / n for k in range(n)]
    v = np.array([F_theta(p, theta) for p in pts]); v = np.append(v, v[0])
    d = np.angle(v[1:] / v[:-1]); return float(np.sum(d) / (2 * math.pi)), float(np.max(np.abs(d)))
def newton(theta, s, it=60, h=1e-5):
    for _ in range(it):
        f = F_theta(s, theta); df = (F_theta(s + h, theta) - F_theta(s - h, theta)) / (2 * h)
        ds = f / df
        if abs(ds) > 0.3: ds *= 0.3 / abs(ds)
        s -= ds
        if abs(ds) < 1e-13: break
    return s

def figure():
    """Trace data/family_mod7.png à partir des fichiers CSV (appel direct : python scripts/run_family_mod7.py --figure)."""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    dg = pd.read_csv(ROOT / "data" / "family_mod7_diagram.csv"); pr = pd.read_csv(ROOT / "data" / "family_mod7_pair.csv")
    dp = pd.read_csv(ROOT / "data" / "family_mod7_proportion.csv"); im = pd.read_csv(ROOT / "data" / "family_mod7_imprint.csv")
    ds = pd.read_csv(ROOT / "data" / "family_mod7_survival.csv")
    blue, green, red, grey = "#1f4e79", "#2e8b57", "#c0392b", "0.45"
    fig, axs = plt.subplots(2, 2, figsize=(11, 7.6), dpi=150)
    ax = axs[0, 0]; th = dg.Z0 / (dg.Z0 - dg.Z1); th = th.where(th.abs() < 1.6)
    ax.plot(dg.t, th, color=blue, lw=1.3); ax.axhline(0, color=grey, lw=0.8)
    thc = float(pr[pr.etat == "hors droite"].theta.min()); ax.axhline(thc, color=red, lw=0.9, ls="--")
    ax.text(dg.t.min() + 0.2, thc + 0.05, f"θ = {thc:.2f} : la paire se rejoint".replace(".", ","), color=red, fontsize=8)
    ax.set_ylim(-1.5, 1.5); ax.set_xlabel("hauteur t"); ax.set_ylabel("θ pour lequel t est un zéro sur la droite")
    ax.set_title("Carte : où sont les zéros sur la droite, selon θ", fontsize=10)
    ax = axs[0, 1]; on = pr[pr.etat == "sur la droite"]; off = pr[pr.etat == "hors droite"]
    ax.plot(on.theta, on.sigma_1, color=blue, lw=1.6); ax.plot(off.theta, off.sigma_1, color=red, lw=1.6, label="la paire quitte la droite"); ax.plot(off.theta, off.sigma_2, color=red, lw=1.6)
    ax.axvline(thc, color=grey, lw=0.8, ls="--"); ax.set_xlabel("θ"); ax.set_ylabel("partie réelle des deux zéros"); ax.set_ylim(0.2, 0.8)
    ax.set_title("Une disparition de paire (zéros près de t = 113)", fontsize=10); ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax = axs[1, 0]; ax.plot(dp.theta, 100 * dp.sur_la_droite_T1000 / dp.total_theta0_T1000, color=blue, lw=1.5)
    last = ds.iloc[-1]; ax.axvspan(last.theta_moins, last.theta_plus, color=green, alpha=0.25, lw=0)
    ax.annotate("100 % : seulement ici", (0.03, 100), xytext=(0.45, 96.5), fontsize=8, color=green, arrowprops=dict(arrowstyle="-", color=green, lw=0.8))
    ax.set_xlabel("θ (0 = L(s, χ₃), produit d'Euler ; 1 = sosie f₇)"); ax.set_ylabel("zéros sur la droite, t ≤ 1000 (%)"); ax.set_ylim(55, 101)
    ax.set_title("Proportion de zéros sur la droite", fontsize=10)
    ax = axs[1, 1]; ax.errorbar(im.theta, 100 * (1 - im.rapport), yerr=100 * im.incertitude, fmt="o-", color=blue, ms=4, lw=1.3, capsize=3)
    ax.axhline(0, color=grey, lw=0.8); ax.set_xlabel("θ"); ax.set_ylabel("déficit près des zéros de ζ (%)")
    ax.set_title("L'empreinte de ζ dans les écarts entre zéros", fontsize=10)
    fig.tight_layout(); fig.savefig(ROOT / "data" / "family_mod7.png"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    t0 = time.time()
    # ---- 1. contrôles : équation fonctionnelle, multiplicativité
    checks = []
    for name, th in (("L(s, chi_3)", 0.0), ("F_0,5", 0.5), ("f_7", 1.0)):
        F = lambda s, th=th: F_theta(s, th)
        fe = max(abs(completed(F, s) - completed(F, 1 - s)) / abs(completed(F, s)) for s in (0.3 + 7j, 0.7 + 12.5j, 1.4 + 3.1j, 0.2 + 55.5j))
        a = coefficients(th, 2400)
        num = sum((a[m * n] - a[m] * a[n]) ** 2 for m in range(2, 49) for n in range(2, 49) if math.gcd(m, n) == 1)
        den = sum(a[m * n] ** 2 + (a[m] * a[n]) ** 2 for m in range(2, 49) for n in range(2, 49) if math.gcd(m, n) == 1)
        checks.append(dict(objet=name, theta=th, defaut_equation_fonctionnelle=fe, defaut_multiplicatif=num / den))
    pd.DataFrame(checks).to_csv(ROOT / "data" / "family_mod7_checks.csv", index=False); print(pd.DataFrame(checks).to_string(index=False), flush=True)
    # ---- 2. grille des fonctions de Hardy
    tg = np.arange(0.0, TMAX + DT / 2, DT); Zg = np.array([hardy(float(t)) for t in tg]); Z0g, Z1g = Zg[:, 0], Zg[:, 1]
    print(f"grille : {len(tg)} points, {time.time() - t0:.0f} s", flush=True)
    # ---- 3. zéros de Z_0 et intervalles
    idx = np.flatnonzero(np.sign(Z0g[1:]) * np.sign(Z0g[:-1]) < 0)
    zeros0 = np.array([brentq(lambda t: hardy(t)[0], tg[i], tg[i + 1], xtol=1e-12) for i in idx])
    n_arg = round(winding_theta(0.0, 0.0001, 200.0)[0]); n_line = int(np.sum(zeros0 < 200.0))
    print(f"L(s, chi_3) : {len(zeros0)} zéros sur la droite pour t <= {TMAX:.0f} ; contrôle t <= 200 : argument {n_arg}, droite {n_line}", flush=True)
    D = Z0g - Z1g; pole_idx = np.flatnonzero(np.sign(D[1:]) * np.sign(D[:-1]) < 0); poles = tg[pole_idx]
    rows = []
    edges = np.concatenate([[-zeros0[0]], zeros0])                 # première bosse : la paire (-t_1, t_1), symétrique
    for k in range(len(edges) - 1):
        a, b = edges[k], edges[k + 1]; lo = max(a, 0.0)
        has_pole = bool(np.any((poles > lo) & (poles < b)))
        mid = 0.5 * (lo + b) if k else 0.0
        sgn = 1.0 if theta_star(mid if mid > 0 else 1e-6) > 0 else -1.0
        row = dict(t_gauche=a, t_droite=b, ecart=b - a, ecart_normalise=(b - a) * density(0.5 * (abs(a) + b)), signe=sgn, pole=has_pole)
        if not has_pole:
            r = minimize_scalar(lambda t: -sgn * theta_star(t), bounds=(lo + 1e-9, b - 1e-9), method="bounded", options=dict(xatol=1e-10))
            cand = [(float(-r.fun), float(r.x))]
            if k == 0: cand.append((sgn * theta_star(1e-9), 0.0))
            h, tc = max(cand); row.update(seuil=sgn * h, t_rencontre=tc)
            z0c, z1c = hardy(tc if tc > 0 else 1e-9)
            row.update(signe_bosse_Z0=float(np.sign(z0c)), signe_Z1=float(np.sign(z1c)), signe_terme_principal=float(np.sign(math.cos(vartheta(tc)))))
        rows.append(row)
    iv = pd.DataFrame(rows); iv.to_csv(ROOT / "data" / "family_mod7_intervals.csv", index=False)
    ev = iv.dropna(subset=["seuil"])
    print(f"intervalles : {len(iv)} ; avec pôle (paire protégée) : {int(iv.pole.sum())} ; bosses : {len(ev)}", flush=True)
    # ---- 4. plage de survie selon la hauteur
    surv = []
    for T in (25, 50, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000):
        e = ev[ev.t_droite <= T]; pos = e[e.seuil > 0]; neg = e[e.seuil < 0]
        surv.append(dict(T=T, zeros=int(np.sum(zeros0 <= T)), theta_plus=float(pos.seuil.min()), t_plus=float(pos.loc[pos.seuil.idxmin(), "t_rencontre"]),
                         theta_moins=float(neg.seuil.max()), t_moins=float(neg.loc[neg.seuil.idxmax(), "t_rencontre"])))
    ds = pd.DataFrame(surv); ds.to_csv(ROOT / "data" / "family_mod7_survival.csv", index=False); print(ds.to_string(index=False, float_format=lambda v: f"{v:.5g}"), flush=True)
    # ---- 5. proportion de zéros sur la droite selon theta
    prop = []
    for th in np.round(np.concatenate([np.linspace(-1, 2, 121), np.linspace(-0.1, 0.1, 81)]), 6):
        zt = (1 - th) * Z0g + th * Z1g
        row = dict(theta=float(th))
        for T in (200, 1000):
            m = tg <= T; row[f"sur_la_droite_T{T}"] = int(np.sum(np.sign(zt[m][1:]) * np.sign(zt[m][:-1]) < 0)); row[f"total_theta0_T{T}"] = int(np.sum(zeros0 <= T))
        prop.append(row)
    dp = pd.DataFrame(prop).drop_duplicates("theta").sort_values("theta"); dp.to_csv(ROOT / "data" / "family_mod7_proportion.csv", index=False)
    # contrôle du total par le principe de l'argument (t <= 200) pour theta = 0,5 et 1
    for th in (0.5, 1.0):
        w, dmax = winding_theta(th, 0.0001, 200.0); on = int(dp.loc[(dp.theta - th).abs().idxmin(), "sur_la_droite_T200"])
        print(f"theta = {th} : total (argument, t <= 200) = {round(w)} ; sur la droite = {on} ; hors droite = {round(w) - on}", flush=True)
        checks.append(dict(objet=f"comptage theta={th}", theta=th, total_argument_T200=round(w), sur_la_droite_T200=on))
    pd.DataFrame(checks).to_csv(ROOT / "data" / "family_mod7_checks.csv", index=False)
    # ---- 6. trajectoire d'une paire : la première disparition côté theta > 0 sous t = 200
    e = ev[(ev.t_droite <= 200) & (ev.seuil > 0)]; first = e.loc[e.seuil.idxmin()]
    thc, tc, a, b = float(first.seuil), float(first.t_rencontre), float(first.t_gauche), float(first.t_droite)
    pair = []
    for th in np.concatenate([np.linspace(0, thc, 26)[:-1], thc * (1 - np.logspace(-2, -6, 9))]):
        t1 = brentq(lambda t: Z(t, th), a - 0.3 * (b - a) if th else a - 1e-6, tc) if th > 0 else a
        t2 = brentq(lambda t: Z(t, th), tc, b + 0.3 * (b - a)) if th > 0 else b
        pair.append(dict(theta=float(th), etat="sur la droite", sigma_1=0.5, t_1=t1, sigma_2=0.5, t_2=t2))
    s = complex(0.55, tc)
    for th in thc * (1 + np.concatenate([np.logspace(-4, -1, 10), np.linspace(0.15, 1.0, 18)])):
        s = newton(float(th), complex(max(s.real, 0.5 + 1e-4), s.imag))
        pair.append(dict(theta=float(th), etat="hors droite", sigma_1=s.real, t_1=s.imag, sigma_2=1 - s.real, t_2=s.imag, residu=abs(F_theta(s, float(th)))))
    pd.DataFrame(pair).to_csv(ROOT / "data" / "family_mod7_pair.csv", index=False)
    print(f"paire suivie : zéros {a:.4f} et {b:.4f}, rencontre à t = {tc:.4f} pour theta = {thc:.5f} ; total {time.time() - t0:.0f} s", flush=True)
    # ---- 7. l'empreinte en creux le long de la famille : les différences des zéros (sur la droite) de F_theta
    #         évitent-elles les zéros de zeta ? (même statistique que le document 24, §7.3)
    gz = np.sort(pd.read_csv(ROOT / "data" / "zeta_zeros_1500.csv").t.values); rng = np.random.default_rng(20261008)
    def online_zeros(th):
        zt = (1 - th) * Z0g + th * Z1g; i = np.flatnonzero(np.sign(zt[1:]) * np.sign(zt[:-1]) < 0)
        return tg[i] - zt[i] * DT / (zt[i + 1] - zt[i])
    def imprint(S, delta=0.15, ndraw=300):
        i, j = np.triu_indices(len(S), k=1); Dd = np.sort(S[j] - S[i]); top = min(Dd[-1], gz.max()) - 8.0
        Zc = gz[(gz > 10) & (gz < top)]; cnt = lambda Zs: int(np.sum(np.searchsorted(Dd, Zs + delta) - np.searchsorted(Dd, Zs - delta)))
        obs = cnt(Zc); ctl = np.array([cnt(Zc + rng.uniform(-6, 6, len(Zc))) for _ in range(ndraw)])
        return obs / ctl.mean(), ctl.std() / ctl.mean()
    imp = []
    for th in (-1.0, -0.5, -0.25, -0.1, 0.0, 0.1, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0):
        S = online_zeros(th); r, e = imprint(S)
        imp.append(dict(theta=th, zeros_sur_la_droite=len(S), rapport=r, incertitude=e)); print(imp[-1], flush=True)
    pd.DataFrame(imp).to_csv(ROOT / "data" / "family_mod7_imprint.csv", index=False)
    # ---- 8. extrait de la carte theta*(t) autour de la paire suivie (pour la figure)
    m = (tg >= tc - 6) & (tg <= tc + 6)
    pd.DataFrame(dict(t=tg[m], Z0=Z0g[m], Z1=Z1g[m])).to_csv(ROOT / "data" / "family_mod7_diagram.csv", index=False)
    figure()
