#!/usr/bin/env python3
"""V6.8 — L'Archipel d'Euler.

Espaces V_q (q premier <= 13, parité paire ou impaire) des combinaisons réelles F_c = somme c_chi e^{-i phi_chi} L(s, chi)
qui ont toutes la même équation fonctionnelle (symétrie de Hardy). Points d'Euler : les axes e_chi.
A. Dimensions ; espaces rigides (dimension 1 : aucune voisine qui garde l'équation fonctionnelle).
B. Rigidité au premier ordre : aucune direction tangente (hors l'échelle) ne garde la multiplicativité.
C. Île autour de chaque point d'Euler : rayon r(T) = distance projective au premier zéro double de hauteur |t| <= T
   (forme close), contrôlé de part et d'autre et dans 100 directions au hasard.
D. La paire qui sort : son écart parmi tous les écarts.
E. Carte de V_7 impair (sphère projective, 3 points d'Euler) : fraction des zéros sur la droite.
F. Partie démontrée : zéros dans Re s > 1 (|t| <= 300) pour un point milieu de chaque espace.
Sorties : data/archipelago_*.csv, data/archipelago.png.
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from euler_archipelago import (characters, hardy_grid, double_zero_distance, kernel_point, wronskian_events,
                               first_order_euler_defect, F_values, dirichlet_coefficients, refine_distance, refine_wronskian)
D = ROOT / "data"
SPACES = [(3, 1), (5, 0), (5, 1), (7, 0), (7, 1), (11, 0), (11, 1), (13, 0), (13, 1)]
TMAX, H = 300.0, 0.005
TLIST = (25, 50, 75, 100, 150, 200, 250, 300)

def zeros_on_grid(t, z):
    i = np.flatnonzero(np.sign(z[1:]) * np.sign(z[:-1]) < 0); return t[i] - z[i] * (t[i + 1] - t[i]) / (z[i + 1] - z[i])
def count_on(t, z, lim):
    m = np.abs(t) <= lim; zz = z[m]; return int(np.sum(np.sign(zz[1:]) * np.sign(zz[:-1]) < 0))
def density(t, q): return math.log(q * max(abs(t), 2.0) / (2 * math.pi)) / (2 * math.pi)

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    mp = pd.read_csv(D / "archipelago_map_q7.csv"); rr = pd.read_csv(D / "archipelago_radius.csv"); ex = pd.read_csv(D / "archipelago_exits.csv")
    cmap = LinearSegmentedColormap.from_list("arch", ["#08306b", "#2171b5", "#9ecae1", "#f7fbff"])
    fig, axs = plt.subplots(2, 2, figsize=(11, 9.4), dpi=150)
    e = pd.read_csv(D / "archipelago_map_q7_euler.csv")
    for ax, T in ((axs[0, 0], 50), (axs[0, 1], 300)):
        d = mp[mp["T"] == T]; n = int(round(math.sqrt(len(d))))
        U = d.u.values.reshape(n, n); V = d.v.values.reshape(n, n); Pp = d.paires_hors_droite.values.reshape(n, n)
        im = ax.pcolormesh(U, V, np.log10(1 + Pp), cmap=cmap.reversed(), vmin=0, vmax=2.0, shading="auto")
        ax.contour(U, V, (Pp <= 0).astype(float), levels=[0.5], colors="#c0392b", linewidths=1.0)
        ax.plot(e.u, e.v, "o", color="#c0392b", ms=5, mec="white", mew=1.0)
        for _, r in e.iterrows(): ax.annotate(r.nom, (r.u, r.v), xytext=(6, 6), textcoords="offset points", fontsize=8, color="#c0392b")
        ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title(f"V₇ impair, zéros jusqu'à |t| = {T} : paires hors droite\n(contour rouge : aucune paire hors droite détectée)", fontsize=9.5)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.02); cb.set_label("log₁₀(1 + paires hors droite)")
    ax = axs[1, 0]; cols = {5: "#2e8b57", 7: "#1f4e79", 11: "#e67e22", 13: "#8e44ad"}
    for (q, par, k), d in rr.groupby(["q", "parite", "k"]):
        d = d.sort_values("T"); ax.loglog(d.N_T, d.rayon, "-", color=cols[q], lw=0.9, alpha=0.75)
    for q, c in cols.items(): ax.plot([], [], color=c, label=f"q = {q}")
    xs = np.array([20.0, 520.0]); med = rr[rr["T"] == 300].rayon.median(); n300 = rr[rr["T"] == 300].N_T.median()
    ax.plot(xs, med * (xs / n300) ** -0.77, "k--", lw=1.0, label="pente −0,77 (médiane des ajustements)")
    from matplotlib.ticker import NullFormatter, FixedLocator, FixedFormatter
    ax.xaxis.set_minor_formatter(NullFormatter()); ax.xaxis.set_major_locator(FixedLocator([20, 50, 100, 200, 500])); ax.xaxis.set_major_formatter(FixedFormatter(["20", "50", "100", "200", "500"]))
    ax.set_xlabel("nombre de zéros du point d'Euler jusqu'à |t| = T"); ax.set_ylabel("rayon de l'île r(T) (sinus de l'angle)")
    ax.set_title("Chaque île rétrécit quand on regarde plus haut", fontsize=10); ax.legend(frameon=False, fontsize=8)
    ax = axs[1, 1]
    ax.hist(ex.rang_de_l_ecart, bins=np.linspace(0, 1, 21), color="#1f4e79", alpha=0.85)
    ax.set_xlabel("rang de l'écart de la paire qui sort, parmi tous les écarts jusqu'à T (0 = le plus petit)")
    ax.set_ylabel("nombre de sorties (records de r(T), tous les points d'Euler)")
    ax.set_title("On sort par les paires les plus serrées", fontsize=10)
    fig.tight_layout(); fig.savefig(D / "archipelago.png"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    t0 = time.time()
    # ---------------- A, B
    sp, rig = [], []
    for q, par in SPACES:
        ch = characters(q, par)
        sp.append(dict(q=q, parite=("impaire" if par else "paire"), dimension=len(ch), caracteres=" ".join(str(c["k"]) for c in ch),
                       reels=int(sum(c["reel"] for c in ch)), rigide=(len(ch) == 1)))
        if len(ch) >= 2:
            for i, c in enumerate(ch):
                lo, self_ = first_order_euler_defect(q, par, i, M=40)
                rig.append(dict(q=q, parite=par, k=c["k"], defaut_min_directions_orthogonales=lo, defaut_direction_propre=self_))
    pd.DataFrame(sp).to_csv(D / "archipelago_spaces.csv", index=False); dr = pd.DataFrame(rig); dr.to_csv(D / "archipelago_rigidity.csv", index=False)
    print(pd.DataFrame(sp).to_string(index=False)); print("rigidité au premier ordre : défaut minimal", f"{dr.defaut_min_directions_orthogonales.min():.3f}",
          "; direction propre", f"{dr.defaut_direction_propre.abs().max():.1e}", f"; {time.time() - t0:.0f} s", flush=True)
    # ---------------- C, D : îles
    t = np.arange(-TMAX, TMAX + H / 2, H); rows, exits, valid = [], [], []; grids = {}
    rng = np.random.default_rng(20261009)
    for q, par in SPACES:
        ch = characters(q, par); d = len(ch)
        if d < 2: continue
        Z, defect, _ = hardy_grid(q, par, t); Zp = np.gradient(Z, H, axis=1); grids[(q, par)] = Z
        print(f"q={q} parité={par} : d={d}, défaut d'imaginaire {defect:.1e}, {time.time() - t0:.0f} s", flush=True)
        for i0, c in enumerate(ch):
            z0 = zeros_on_grid(t, Z[i0])
            # candidats : tous les minima locaux de la grille (d >= 3) ou tous les zéros du wronskien (d = 2), raffinés
            cands = []
            if d >= 3:
                dist = double_zero_distance(Z, Zp, i0)
                loc = [j for j in range(1, len(t) - 1) if dist[j] <= dist[j - 1] and dist[j] <= dist[j + 1] and np.isfinite(dist[j])]
                for j in loc: cands.append(refine_distance(q, par, i0, t[j] - 3 * H, t[j] + 3 * H))
            else:
                W = Z[0] * Zp[1] - Z[1] * Zp[0]
                for j in np.flatnonzero(np.sign(W[1:]) * np.sign(W[:-1]) < 0): cands.append(refine_wronskian(q, par, i0, t[j] - H, t[j + 1] + H))
            for T in TLIST:
                inT = [cd for cd in cands if abs(cd[1]) <= T]; r, ts, cstar = min(inT, key=lambda x: x[0])
                comp = np.abs(cstar.copy()); comp[i0] = -1; jp = int(np.argmax(comp))
                zz = z0[np.abs(z0) <= T]; ia = np.searchsorted(zz, ts)
                gap = float(zz[ia] - zz[ia - 1]) if 0 < ia < len(zz) else float("nan")
                gaps = np.diff(zz); ng = gaps * np.array([density(0.5 * (a + b), q) for a, b in zip(zz[:-1], zz[1:])])
                gn = gap * density(ts, q); rank = float(np.mean(ng < gn - 1e-12)) if gap == gap else float("nan")
                rows.append(dict(q=q, parite=par, k=c["k"], T=T, N_T=int(len(zz)), rayon=r, t_sortie=ts, partenaire_k=ch[jp]["k"],
                                 partenaire_conjugue=(ch[jp]["k"] == q - 1 - c["k"]), poids_partenaire=float(abs(cstar[jp])),
                                 ecart_normalise=gn, rang_de_l_ecart=rank, candidats=len(cands)))
            # validation à T = 300 : de part et d'autre du rayon, et 100 directions au hasard
            rT, tsT, cst = min(cands, key=lambda x: x[0])
            e = np.zeros(d); e[i0] = 1.0
            if cst @ e < 0: cst = -cst
            alpha = math.asin(min(rT, 1.0)); u = cst - (cst @ e) * e; u /= np.linalg.norm(u)
            base = count_on(t, Z[i0], TMAX)                   # fenêtre complète |t| <= 300
            def online(cv): return count_on(t, cv @ Z, TMAX)
            loc = lambda cv: count_on(t[np.abs(t - tsT) < 3.0] - tsT, (cv @ Z)[np.abs(t - tsT) < 3.0], 3.0)
            c_in = math.cos(0.95 * alpha) * e + math.sin(0.95 * alpha) * u; c_out = math.cos(1.05 * alpha) * e + math.sin(1.05 * alpha) * u
            ok_rand = ok_exact = 0
            for _ in range(100):
                w = rng.normal(size=d); w -= (w @ e) * e; w /= np.linalg.norm(w)
                n_ = online(math.cos(0.95 * alpha) * e + math.sin(0.95 * alpha) * w)
                ok_rand += n_ >= base - 1; ok_exact += n_ == base     # une paire perdue = -2 ; un zéro qui franchit |t| = 300 = +-1
            Tsm = TMAX; smooth = (Tsm / math.pi) * math.log(q * Tsm / (2 * math.pi * math.e))
            valid.append(dict(q=q, parite=par, k=c["k"], rayon_T300=rT, zeros_sur_la_droite=base, comptage_lisse=smooth, ecart_au_lisse=base - smooth,
                              a_095_meme_compte=(online(c_in) >= base - 1), perte_locale_a_105=loc(c_in) - loc(c_out),
                              directions_au_hasard_ok=ok_rand, directions_au_hasard_compte_identique=ok_exact))
        print(f"   îles : {len(ch)} points d'Euler, {time.time() - t0:.0f} s", flush=True)
    dr = pd.DataFrame(rows); dr.to_csv(D / "archipelago_radius.csv", index=False)
    dv = pd.DataFrame(valid); dv.to_csv(D / "archipelago_validation.csv", index=False)
    rec = dr.sort_values("T").groupby(["q", "parite", "k"], group_keys=False).apply(lambda g: g[g.rayon < g.rayon.shift(1).fillna(9)])
    rec.to_csv(D / "archipelago_exits.csv", index=False)
    fits = []
    for (q, par, k), g in dr.groupby(["q", "parite", "k"]):
        g = g[g["T"] >= 50]; p = np.polyfit(np.log(g.N_T), np.log(g.rayon), 1); fits.append(dict(q=q, parite=par, k=k, pente=p[0]))
    df_fit = pd.DataFrame(fits); df_fit.to_csv(D / "archipelago_scaling.csv", index=False)
    print(dv.to_string(index=False)); print(dr[dr["T"] == 300][["q", "parite", "k", "N_T", "rayon", "t_sortie", "partenaire_k", "partenaire_conjugue", "rang_de_l_ecart"]].to_string(index=False))
    print("pentes log r / log N : médiane", f"{df_fit.pente.median():.2f}", "; quartiles", df_fit.pente.quantile([0.25, 0.75]).round(2).tolist(),
          "; sorties (records) :", len(rec), "; rang médian de l'écart :", f"{rec.rang_de_l_ecart.median():.3f}", flush=True)
    # ---------------- E : carte de V_7 impair
    q, par = 7, 1; Z = grids[(q, par)][:, ::2]; tt = t[::2]; ch = characters(q, par)
    nvec = np.ones(3) / math.sqrt(3); a = np.array([1.0, -1.0, 0.0]) / math.sqrt(2); b = np.cross(nvec, a)
    n = 141; us = np.linspace(-1.75, 1.75, n); UU, VV = np.meshgrid(us, us); P = nvec[None, :] + UU.ravel()[:, None] * a[None, :] + VV.ravel()[:, None] * b[None, :]
    P /= np.linalg.norm(P, axis=1)[:, None]; maprows = []
    near = np.argmax(np.abs(P), axis=1)                    # point d'Euler le plus proche (plus grand cosinus)
    for T in (50, 150, 300):
        m = np.abs(tt) <= T; Zm = Z[:, m]; Nref = np.array([count_on(tt, Z[i], T) for i in range(3)]); cnt = np.empty(len(P))
        for i0 in range(0, len(P), 200):
            Zc = P[i0: i0 + 200] @ Zm; cnt[i0: i0 + 200] = np.sum(np.sign(Zc[:, 1:]) * np.sign(Zc[:, :-1]) < 0, axis=1)
        deficit = Nref[near] - cnt
        maprows += [dict(T=T, u=float(u), v=float(v), zeros_sur_la_droite=int(n_), deficit=int(df_), paires_hors_droite=max(int(df_), 0) / 2)
                    for u, v, n_, df_ in zip(UU.ravel(), VV.ravel(), cnt, deficit)]
        print(f"carte T={T} : part de la carte sans paire hors droite (déficit <= 0) : {np.mean(deficit <= 0):.4f} ; {time.time() - t0:.0f} s", flush=True)
    pd.DataFrame(maprows).to_csv(D / "archipelago_map_q7.csv", index=False)
    eu = []
    for i in range(3):
        e = np.eye(3)[i]; e = e / (e @ nvec); eu.append(dict(nom=f"L(s, χ_{ch[i]['k']})", u=float(e @ a), v=float(e @ b)))
    pd.DataFrame(eu).to_csv(D / "archipelago_map_q7_euler.csv", index=False)
    figure(); print(f"total {time.time() - t0:.0f} s")
