#!/usr/bin/env python3
"""V6.7 — STABILITY-RADIUS dans le Modèle réduit : marge de la forme contre marge de l'objet.

A. Courbes : les 425 de la V6.6, plus 100 nouvelles sur F_3 en genre 9 à 12 (comptées, recomptées à l'étage g + 1).
B. Pour chaque courbe : marge de la forme lambda_min(T_L)/2g pour L = 1..2g+2 ; marge de l'objet (rayon structuré,
   forme close), mécanisme de sortie (rencontre de deux zéros ou bord), vérification de part et d'autre du rayon,
   produit d'Euler au point de sortie.
C. Loi d'inertie : à la fenêtre L = 2g, nombre de valeurs propres négatives de T_L = (zéros hors du cercle)/2,
   contrôlé en 60 chiffres (mpmath) sur des polynômes palindromiques tirés au hasard et sur les 220 faux jumeaux.
D. Trajets vraie courbe -> faux jumeau : seuil de l'objet (interpolation des polynômes) contre seuil de la forme
   (interpolation des matrices, comme au document 26), fenêtre par fenêtre.
Sorties : data/stability_model_*.csv, data/stability_model.png.
"""
from pathlib import Path
import sys, math, random, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from function_field import count_points, random_curve, L_polynomial, power_sums
from stability_radius import (normalized, from_free, H_poly, structured_radius, exit_candidates, perturbed, off_circle, form_margin,
                              toeplitz_form, inertia, form_threshold, object_threshold, euler_counts)
D = ROOT / "data"
NEW_GENERA, NCURVES = range(9, 13), 25

def new_curves():
    path = D / "stability_model_new_curves.csv"
    if path.exists() and "--recount" not in sys.argv: return pd.read_csv(path)
    rng = random.Random(20261009); rows = []; t0 = time.time()
    for g in NEW_GENERA:
        for k in range(NCURVES):
            f = random_curve(3, g, rng); N = [count_points(f, 3, n) for n in range(1, g + 2)]
            c = L_polynomial(N[:g], 3, g); S = power_sums(c, g + 1)
            rows.append(dict(q=3, g=g, courbe=k, f=" ".join(map(str, f)), N=" ".join(map(str, N)), P=" ".join(map(str, c)),
                             recompte_ok=(3 ** (g + 1) + 1 - S[g] == N[g])))
        print(f"genre {g} : {NCURVES} courbes comptées, {time.time() - t0:.0f} s", flush=True)
    df = pd.DataFrame(rows); df.to_csv(path, index=False); return df

def exact_inertia(b, L, dps=60):
    import mpmath as mp
    mp.mp.dps = dps; bb = [mp.mpf(repr(float(x))) for x in b]; m = len(bb) - 1
    e = [(-1) ** k * bb[k] for k in range(m + 1)]; S = [mp.mpf(m)]
    for n in range(1, L):
        s = sum((-1) ** (i - 1) * e[i] * S[n - i] for i in range(1, min(n - 1, m) + 1))
        if n <= m: s += (-1) ** (n - 1) * n * e[n]
        S.append(s)
    T = mp.matrix(L, L)
    for i in range(L):
        for j in range(L): T[i, j] = S[abs(i - j)]
    ev = mp.eigsy(T)[0]; scale = max(abs(x) for x in ev)
    return sum(1 for x in ev if x < -mp.mpf(10) ** (-dps // 2) * scale)

def exact_off_circle(b, dps=60):
    import mpmath as mp
    mp.mp.dps = dps; r = mp.polyroots([mp.mpf(repr(float(x))) for x in b[::-1]], maxsteps=200, extraprec=200)
    return sum(1 for z in r if abs(abs(z) - 1) > mp.mpf(10) ** -12)

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fm = pd.read_csv(D / "stability_model_form_margin.csv"); dc = pd.read_csv(D / "stability_model_curves.csv")
    pf = pd.read_csv(D / "stability_model_paths.csv"); fk = pd.read_csv(D / "stability_model_fakes.csv")
    blue, green, red, grey = "#1f4e79", "#2e8b57", "#c0392b", "0.55"
    fig, axs = plt.subplots(2, 2, figsize=(11, 7.8), dpi=150)
    ax = axs[0, 0]
    for g, col in ((2, "#9ecae1"), (4, "#4292c6"), (8, "#2171b5"), (12, "#08306b")):
        d = fm[(fm.q == 3) & (fm.g == g)].groupby("L").marge_forme.median()
        ax.plot(d.index / (2 * g), np.maximum(d.values, 1e-17), "o-", color=col, ms=3.5, lw=1.3, label=f"vraies courbes, genre {g}")
    ax.axvline(1, color="0.3", ls="--", lw=0.9); ax.set_yscale("log"); ax.set_ylim(1e-17, 2)
    ax.text(1.06, 1e-11, "fenêtre > 2g :\nforme exactement\nsingulière", fontsize=7.5, color="0.25")
    ax.set_xlabel("fenêtre L / 2g (nombre d'étages / nombre de zéros)"); ax.set_ylabel("marge de la forme λ_min(T_L)/2g (médiane)")
    ax.set_title("Marge de la forme : nulle dès que la fenêtre dépasse les zéros", fontsize=10); ax.legend(frameon=False, fontsize=7.5, loc="lower left")
    ax = axs[0, 1]
    for q, col, mk in ((3, blue, "o"), (5, green, "s"), (7, red, "^")):
        d = dc[dc.q == q].groupby("g").rayon_objet.median(); ax.loglog(2 * d.index, d.values, mk + "-", color=col, ms=5, lw=1.3, label=f"F_{q}")
    ax.set_xlabel("nombre de zéros 2g"); ax.set_ylabel("marge de l'objet (rayon structuré, médiane)")
    ax.set_title("Marge de l'objet : positive, décroît avec le nombre de zéros", fontsize=10); ax.legend(frameon=False, fontsize=9)
    ax = axs[1, 0]
    for g, off, col, mk in ((1, -0.08, "#6baed6", "o"), (2, 0.08, blue, "s")):
        d = pf[pf.g == g].copy(); d["s"] = np.minimum(d.seuil_forme.fillna(9.0), 1.08)
        st = d.groupby("L").s.quantile([0.25, 0.5, 0.75]).unstack()
        ax.errorbar(st.index + off, st[0.5], yerr=[st[0.5] - st[0.25], st[0.75] - st[0.5]], fmt=mk + "-", color=col, ms=5, lw=1.3, capsize=3)
        so = d.groupby(["c1", "c2"], dropna=False).seuil_objet.first()
        ax.axhspan(so.quantile(0.25), so.quantile(0.75), color=col, alpha=0.15)
        ax.axhline(so.median(), color=col, lw=1.0, ls="--")
        ax.text(5.35, so.median() + 0.015, f"objet, genre {g}", color=col, fontsize=7.5, ha="right", va="bottom")
    ax.axhline(1.0, color="0.4", lw=0.8, ls=":"); ax.text(5.3, 1.02, "≥ 1 : la forme du faux jumeau est encore positive", fontsize=7, ha="right", color="0.3")
    ax.set_xticks(range(1, 6)); ax.set_ylim(-0.05, 1.15); ax.set_xlim(0.6, 5.4)
    ax.set_xlabel("fenêtre L (genre 1 : 2g = 2 ; genre 2 : 2g = 4)"); ax.set_ylabel("seuil sur le trajet vraie courbe → faux jumeau")
    ax.text(1.55, 0.78, "forme, genre 1", color="#6baed6", fontsize=7.5); ax.text(3.3, 0.62, "forme, genre 2", color=blue, fontsize=7.5)
    ax.set_title("Le seuil de la forme tombe à 0 en L = 2g + 1 ; celui de l'objet, non", fontsize=10)
    ax = axs[1, 1]
    d = dc[~dc.zeros_confondus]
    e = d[d.mecanisme == "rencontre"]; ax.loglog(e.plus_petit_ecart ** 2, e.rayon_objet, "o", color=blue, ms=2.5, alpha=0.6, label="rencontre : en abscisse, (écart minimal)²")
    e = d[d.mecanisme == "bord"]; ax.loglog(e.distance_au_bord, e.rayon_objet, "^", color=red, ms=2.8, alpha=0.6, label="bord : en abscisse, distance au bord")
    ax.set_xlabel("ce qu'il faut franchir (en 2 cos φ)"); ax.set_ylabel("marge de l'objet")
    ax.set_title("La marge de l'objet suit la paire la plus serrée", fontsize=10); ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    fig.tight_layout(); fig.savefig(D / "stability_model.png"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    t0 = time.time()
    old = pd.read_csv(D / "reduced_model_curves.csv")[["q", "g", "courbe", "f", "N", "P", "recompte_ok"]]
    allc = pd.concat([old, new_curves()], ignore_index=True)
    print("courbes :", len(allc), "; recomptes corrects :", int(allc.recompte_ok.sum()), flush=True)
    # ---------------- B : deux marges par courbe
    rows, fm = [], []
    for _, r in allc.iterrows():
        q, g = int(r.q), int(r.g); c = list(map(int, r.P.split())); b = normalized(c, q)
        for L in range(1, 2 * g + 3):
            fm.append(dict(q=q, g=g, courbe=int(r.courbe), L=L, marge_forme=form_margin(b, L)))
        cands = exit_candidates(b); sr = cands[0]; bin_, bout = perturbed(b, sr["delta"], 0.999), perturbed(b, sr["delta"], 1.001)
        y = np.sort(np.real(np.roots(H_poly(b)[::-1]))) if g > 1 else np.real(np.roots(H_poly(b)[::-1]))
        def beyond(cand):                                  # juste au-delà du point de sortie (pas relatif, ou absolu si le rayon est nul)
            d = cand["delta"]; n = np.linalg.norm(d)
            return perturbed(b, d, 1.000001) if cand["rayon"] > 1e-6 else perturbed(b, d / max(n, 1e-300), 1e-6)
        a = euler_counts(beyond(sr), q, 200)
        r_euler = next((cd["rayon"] for cd in cands if np.min(euler_counts(beyond(cd), q, 60)) >= 0), float("nan"))
        rows.append(dict(q=q, g=g, courbe=int(r.courbe), P=r.P, rayon_objet=sr["rayon"], mecanisme=sr["mecanisme"], x_sortie=sr["x"],
                         rh_a_0999=off_circle(bin_) == 0, hors_cercle_a_1001=off_circle(bout),
                         marge_forme_a_1001_L4g=form_margin(bout, 4 * g),
                         euler_positif_a_la_sortie=bool(np.min(a) >= 0), a1_a_la_sortie=float(a[0]), rayon_objet_euler=r_euler,
                         zeros_confondus=bool(sr["rayon"] < 1e-6),
                         plus_petit_ecart=float(np.min(np.diff(y))) if g > 1 else float("nan"), distance_au_bord=float(2 - np.max(np.abs(y))),
                         marge_forme_L2g=form_margin(b, 2 * g), marge_forme_L2g1=form_margin(b, 2 * g + 1)))
    dc = pd.DataFrame(rows); dc.to_csv(D / "stability_model_curves.csv", index=False)
    pd.DataFrame(fm).to_csv(D / "stability_model_form_margin.csv", index=False)
    print(f"B : {len(dc)} courbes ; rayon nul (zéros confondus) : {int(dc.zeros_confondus.sum())} ; RH juste avant le rayon : {int(dc.rh_a_0999.sum())} ;"
          f" hors du cercle juste après (rayon > 0) : {int((dc[~dc.zeros_confondus].hors_cercle_a_1001 > 0).sum())} / {int((~dc.zeros_confondus).sum())} ;"
          f" rayon avec Euler = rayon sans Euler : {int((np.abs(dc.rayon_objet_euler - dc.rayon_objet) < 1e-9).sum())} ;"
          f" Euler positif au point de sortie : {int(dc.euler_positif_a_la_sortie.sum())} ; |marge forme| max à L = 2g+1 : {dc.marge_forme_L2g1.abs().max():.1e}"
          f" ; {time.time() - t0:.0f} s", flush=True)
    # ---------------- C : loi d'inertie sur des polynômes palindromiques au hasard (contrôle en 60 chiffres)
    rng = np.random.default_rng(20261009); irows = []
    for g in range(1, 7):
        for _ in range(150):
            nq = rng.integers(0, g // 2 + 1); nr = rng.integers(0, g - 2 * nq + 1); roots = []
            for _ in range(nq):
                z = rng.uniform(1.02, 2) * np.exp(1j * rng.uniform(0.05, 3.09)); roots += [z, np.conj(z), 1 / z, 1 / np.conj(z)]
            for _ in range(nr):
                x = rng.uniform(1.02, 2) * rng.choice([-1, 1]); roots += [x, 1 / x]
            for y in rng.uniform(-2, 2, size=g - 2 * nq - nr):
                ph = math.acos(y / 2); roots += [np.exp(1j * ph), np.exp(-1j * ph)]
            P = np.real(np.poly(roots)); b = P[::-1] / P[-1]; off = 4 * nq + 2 * nr
            irows.append(dict(g=g, hors_cercle=off, negatives_L2g_60chiffres=exact_inertia(b, 2 * g),
                              negatives_L2g_double=inertia(b, 2 * g), rh_decide_L2gm1=(inertia(b, 2 * g - 1) == 0) == (off == 0)))
    di = pd.DataFrame(irows); di.to_csv(D / "stability_model_inertia.csv", index=False)
    print("C : loi d'inertie (60 chiffres) :", int((di.negatives_L2g_60chiffres == di.hors_cercle // 2).sum()), "/", len(di),
          "; en double précision :", int((di.negatives_L2g_double == di.hors_cercle // 2).sum()),
          "; la fenêtre 2g - 1 décide RH :", int(di.rh_decide_L2gm1.sum()), f"; {time.time() - t0:.0f} s", flush=True)
    # ---------------- D : faux jumeaux et trajets
    fake = pd.read_csv(D / "reduced_model_fakes.csv"); fkr = fake[fake.euler_positif & ~fake.RH]
    real = fake[fake.realise]; frows, prows = [], []
    for _, r in fkr.iterrows():
        q, g = int(r.q), int(r.g)
        cf = [1, int(r.c1), q] if g == 1 else [1, int(r.c1), int(r.c2), q * int(r.c1), q * q]; bf = normalized(cf, q)
        cands = real[(real.q == q) & (real.g == g)]
        best = None
        for _, t in cands.iterrows():
            ct = [1, int(t.c1), q] if g == 1 else [1, int(t.c1), int(t.c2), q * int(t.c1), q * q]; bt = normalized(ct, q)
            dist = float(np.linalg.norm(bt - bf))
            if best is None or dist < best[0]: best = (dist, bt, ct)
        dist, bt, ct = best
        off = exact_off_circle(bf); neg = exact_inertia(bf, 2 * g)
        tobj = object_threshold(bt, bf)
        for L in range(1, 2 * g + 2):
            prows.append(dict(q=q, g=g, c1=int(r.c1), c2=(int(r.c2) if g == 2 else None), L=L,
                              seuil_forme=form_threshold(toeplitz_form(bt, L), toeplitz_form(bf, L)), seuil_objet=tobj))
        frows.append(dict(q=q, g=g, c1=int(r.c1), c2=(int(r.c2) if g == 2 else None), hors_cercle=off, negatives_L2g=neg,
                          marge_forme_L2g=form_margin(bf, 2 * g), marge_forme_L8=form_margin(bf, 8), marge_forme_L16=form_margin(bf, 16),
                          vraie_courbe_la_plus_proche=" ".join(map(str, ct)), distance=dist, seuil_objet=tobj,
                          rayon_objet_de_la_vraie=structured_radius(bt)["rayon"]))
    dfk = pd.DataFrame(frows); dfk.to_csv(D / "stability_model_fakes.csv", index=False)
    dp = pd.DataFrame(prows); dp.to_csv(D / "stability_model_paths.csv", index=False)
    print("D : faux jumeaux :", len(dfk), "; inertie = hors cercle / 2 :", int((dfk.negatives_L2g == dfk.hors_cercle // 2).sum()),
          "; marge de la forme négative à L = 2g :", int((dfk.marge_forme_L2g < 0).sum()), flush=True)
    piv = dp.groupby(["g", "L"]).seuil_forme.median(); print("seuil de la forme (médiane) :\n" + piv.to_string())
    print("seuil de l'objet (médiane) :", dp.groupby("g").seuil_objet.median().to_dict())
    figure(); print(f"total {time.time() - t0:.0f} s")
