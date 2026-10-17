#!/usr/bin/env python3
"""V6.6 — Le Modèle réduit : là où RH est un théorème, à quoi ressemble ce qui la rend nécessaire ?

A. Courbes hyperelliptiques y^2 = f(x) sur F_3, F_5, F_7, genre 1 à 8 : N_1..N_g comptés, P(u) reconstruit,
   N_{g+1} recompté directement (double comptage), RH vérifiée.
B. Positivité de Castelnuovo le long de la tour F_{q^n} : rho_n = |S_n| / (2 g q^(n/2)) <= 1 ; marge 1 - max rho_n.
C. Fausses courbes : polynômes entiers avec l'équation fonctionnelle et un produit d'Euler à comptages entiers >= 0,
   mais RH fausse ; à quel étage n la positivité de Castelnuovo les démasque-t-elle ?
D. Plage de survie : perturbation qui conserve l'équation fonctionnelle ; marge selon le genre.
Sorties : data/reduced_model_*.csv, data/reduced_model.png.
"""
from pathlib import Path
import sys, math, random, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from function_field import (count_points, random_curve, L_polynomial, power_sums, closed_points, roots_alpha,
                            castelnuovo_ratio, angles, survival_margin, squarefree)

PLAN = {3: range(1, 9), 5: range(1, 6), 7: range(1, 5)}
NCURVES, DMAX = 25, 200

def tower_max(phi, g, N):
    n = np.arange(1, N + 1)[:, None]
    rho = np.abs(np.cos(n * phi[None, :]).sum(axis=1)) / g
    return np.maximum.accumulate(rho)

def classify(c, q, g, D=DMAX):
    S = power_sums(c, D); a = closed_points(S, q)
    al = roots_alpha(c)
    if g == 1:                                         # RH exacte en arithmétique entière : x = alpha + q/alpha réel dans [-2 sqrt q, 2 sqrt q]
        rh = c[1] ** 2 <= 4 * q
    else:                                              # h(x) = x^2 + c1 x + (c2 - 2q) : deux racines réelles dans [-2 sqrt q, 2 sqrt q]
        c1, c2 = c[1], c[2]
        rh = (c1 * c1 - 4 * (c2 - 2 * q) >= 0) and (c1 * c1 <= 16 * q) and (c2 + 2 * q >= 0) and ((c2 + 2 * q) ** 2 >= 4 * q * c1 * c1)
    rho = [abs(s) / (2 * g * q ** (n / 2)) for n, s in enumerate(S[:80], start=1)]
    first = next((n for n, r in enumerate(rho, start=1) if r > 1 + 1e-12), None)
    return dict(RH=rh, euler_positif=bool(min(a) >= 0), alpha_max_sur_q=float(np.max(np.abs(al)) / q),
                N1=q + 1 - S[0], rho_1=rho[0], premier_etage_castelnuovo_faux=first)

EXAMPLE = (5, [1, 1, -8, 5, 25])                      # un faux jumeau de genre 2 sur F_5 (c1 = 1, c2 = -8)

def example_table():
    q, c = EXAMPLE; S = power_sums(c, 12); a = closed_points(S, q)
    rho = castelnuovo_ratio(S, q, 2)
    return pd.DataFrame(dict(n=range(1, 13), N_n=[q ** n + 1 - S[n - 1] for n in range(1, 13)], a_n=a, rho_n=rho))

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    tw = pd.read_csv(ROOT / "data" / "reduced_model_tower.csv"); dc = pd.read_csv(ROOT / "data" / "reduced_model_curves.csv")
    df = pd.read_csv(ROOT / "data" / "reduced_model_fakes.csv"); ex = pd.read_csv(ROOT / "data" / "reduced_model_example.csv")
    blue, green, red, grey = "#1f4e79", "#2e8b57", "#c0392b", "0.6"
    fig, axs = plt.subplots(2, 2, figsize=(11, 7.8), dpi=150)
    ax = axs[0, 0]
    for g, col, lab in ((1, "#9ecae1", "genre 1"), (2, "#4292c6", "genre 2 (courbe maximale sur F₈₁)"), (4, "#2171b5", "genre 4"), (8, "#08306b", "genre 8")):
        d = tw[(tw.q == 3) & (tw.g == g)]; ax.plot(d.n, d.max_rho, color=col, lw=1.5, drawstyle="steps-post", label=f"vraie courbe, {lab}")
    exm = np.maximum.accumulate(ex.rho_n)
    ax.plot(ex.n, np.minimum(exm, 1.28), "o", color=red, ms=3.5, label="faux jumeau (genre 2, F₅)")
    ax.plot(ex.n, np.minimum(exm, 1.28), color=red, lw=1.2, drawstyle="steps-post")
    ax.annotate(f"ρ₅ = {ex.rho_n.iloc[4]:.2f}".replace(".", ","), (5, 1.28), xytext=(9, 1.2), fontsize=8, color=red, arrowprops=dict(arrowstyle="-", color=red, lw=0.8))
    ax.axhline(1, color="0.3", lw=0.9, ls="--"); ax.set_xscale("log"); ax.set_ylim(0, 1.3)
    ax.set_xlabel("étage n de la tour (corps à qⁿ éléments)"); ax.set_ylabel("max ρ_k pour k ≤ n  (positivité : ≤ 1)")
    ax.set_title("Positivité de Castelnuovo : tenue sans marge", fontsize=10); ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    ax = axs[0, 1]; d = df[(df.q == 5) & (df.g == 2)]; q = 5
    c1 = np.linspace(-14, 14, 400)
    ax.plot(c1, c1 ** 2 / 4 + 2 * q, color=blue, lw=1); ax.plot(c1, 2 * math.sqrt(q) * np.abs(c1) - 2 * q, color=blue, lw=1)
    m = d[~d.euler_positif]; ax.scatter(m.c1, m.c2, s=4, color="0.85", label="pas de produit d'Euler positif")
    m = d[d.RH & ~d.realise & d.euler_positif]; ax.scatter(m.c1, m.c2, s=10, facecolors="none", edgecolors=blue, lw=0.7, label="RH, non réalisé ici")
    m = d[d.realise]; ax.scatter(m.c1, m.c2, s=12, color=blue, label="vraie courbe (comptée)")
    m = d[d.euler_positif & ~d.RH]; ax.scatter(m.c1, m.c2, s=12, marker="x", color=red, lw=0.9, label="faux jumeau : Euler positif, RH fausse")
    ax.set_xlim(-8, 14); ax.set_ylim(-20, 55); ax.set_xlabel("c₁"); ax.set_ylabel("c₂")
    ax.set_title("Genre 2 sur F₅ : P(u) = 1 + c₁u + c₂u² + 5c₁u³ + 25u⁴", fontsize=10); ax.legend(frameon=False, fontsize=7, loc="upper left")
    ax = axs[1, 0]
    for q, col, mk in ((3, blue, "o"), (5, green, "s"), (7, red, "^")):
        g = dc[dc.q == q].groupby("g").survie_relative.median(); ax.semilogy(g.index, g.values, mk + "-", color=col, ms=5, lw=1.3, label=f"F_{q}")
    ax.set_xlabel("genre (nombre de paires de zéros)"); ax.set_ylabel("plage de survie relative (médiane)")
    ax.set_title("La marge diminue quand les zéros sont plus nombreux", fontsize=10); ax.legend(frameon=False, fontsize=9)
    ax = axs[1, 1]
    for N, col in (("marge_tour_n10", "#9ecae1"), ("marge_tour_n1000", "#4292c6"), ("marge_tour_n100000", "#08306b")):
        g = dc[dc.q == 3].groupby("g")[N].median(); ax.plot(g.index, g.values, "o-", color=col, ms=4, lw=1.3, label=f"étages jusqu'à {N.split('_n')[1].replace('100000', '100 000').replace('1000', '1 000')}")
    ax.set_xlabel("genre (courbes sur F₃)"); ax.set_ylabel("marge 1 − max ρ (médiane)")
    ax.set_title("Plus on monte dans la tour, plus la marge s'annule", fontsize=10); ax.legend(frameon=False, fontsize=9)
    fig.tight_layout(); fig.savefig(ROOT / "data" / "reduced_model.png"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" in sys.argv:
        figure(); sys.exit(0)
    t0 = time.time(); rng = random.Random(20261008)
    # ---------------- A, B, D : vraies courbes
    rows, tower_rows = [], []
    for q, gs in PLAN.items():
        for g in gs:
            for k in range(NCURVES):
                f = random_curve(q, g, rng)
                N = [count_points(f, q, n) for n in range(1, g + 2)]
                c = L_polynomial(N[:g], q, g); S = power_sums(c, g + 1)
                al = roots_alpha(c); phi = angles(c, q)
                em, ep, scale = survival_margin(phi)
                tm = tower_max(phi, g, 100000)
                y = np.sort(2 * np.cos(phi)); gaps = np.diff(y) if g > 1 else np.array([np.nan])
                Sx = power_sums(c, 60); cas = castelnuovo_ratio(Sx, q, g)
                rows.append(dict(q=q, g=g, courbe=k, f=" ".join(map(str, f)), N=" ".join(map(str, N)), P=" ".join(map(str, c)),
                                 recompte_ok=(q ** (g + 1) + 1 - S[g] == N[g]), ecart_RH=float(np.max(np.abs(np.abs(al) / math.sqrt(q) - 1))),
                                 castelnuovo_exact_ok_n60=bool(np.all(cas <= 1 + 1e-12)),
                                 marge_tour_n10=1 - tm[9], marge_tour_n100=1 - tm[99], marge_tour_n1000=1 - tm[999], marge_tour_n100000=1 - tm[-1],
                                 survie_moins=em, survie_plus=ep, survie_relative=min(-em, ep) / scale,
                                 bord_le_plus_proche=float(2 - np.max(np.abs(y))), plus_petit_ecart=float(np.nanmin(gaps)) if g > 1 else float("nan")))
                if k == 0:
                    for n in np.unique(np.round(np.logspace(0, 5, 60)).astype(int)):
                        tower_rows.append(dict(q=q, g=g, n=int(n), max_rho=float(tm[n - 1])))
            print(f"q={q} g={g} : {NCURVES} courbes, {time.time() - t0:.0f} s", flush=True)
    dc = pd.DataFrame(rows); dc.to_csv(ROOT / "data" / "reduced_model_curves.csv", index=False)
    pd.DataFrame(tower_rows).to_csv(ROOT / "data" / "reduced_model_tower.csv", index=False)
    print("recomptes corrects :", int(dc.recompte_ok.sum()), "/", len(dc), " ; écart RH max :", f"{dc.ecart_RH.max():.1e}",
          " ; Castelnuovo exact (n <= 60) :", int(dc.castelnuovo_exact_ok_n60.sum()), "/", len(dc), flush=True)
    # ---------------- C : fausses courbes, genre 1 et 2, q = 5 et q = 3
    fakes = []
    for q in (3, 5):
        realized1 = set(); realized2 = set()
        for f in [[1, a, b, c] for a in range(q) for b in range(q) for c in range(q)]:
            if squarefree(f, q): realized1.add(L_polynomial([count_points(f, q, 1)], q, 1)[1])
        for coeffs in np.ndindex(*(q,) * 5):
            f = [1] + list(coeffs)
            if squarefree(f, q):
                c = L_polynomial([count_points(f, q, 1), count_points(f, q, 2)], q, 2); realized2.add((c[1], c[2]))
        for c1 in range(-(q + 1), 3 * q):
            c = [1, c1, q]; r = classify(c, q, 1); r.update(q=q, g=1, c1=c1, c2=None, realise=(c1 in realized1)); fakes.append(r)
        B = 2 * q + 4
        for c1 in range(-B, B + 1):
            for c2 in range(-2 * B, 4 * B + 1):
                c = [1, c1, c2, q * c1, q * q]
                if q + 1 + c1 < 0: continue                    # N_1 < 0 : pas de produit d'Euler
                r = classify(c, q, 2); r.update(q=q, g=2, c1=c1, c2=c2, realise=((c1, c2) in realized2)); fakes.append(r)
        print(f"q={q} : polynômes de genre 1 et 2 classés, {time.time() - t0:.0f} s", flush=True)
    df = pd.DataFrame(fakes); df.to_csv(ROOT / "data" / "reduced_model_fakes.csv", index=False)
    s = df.groupby(["q", "g"]).apply(lambda d: pd.Series(dict(
        polynomes=len(d), euler_positifs=int(d.euler_positif.sum()), RH=int(d.RH.sum()), realises=int(d.realise.sum()),
        faux_jumeaux=int((d.euler_positif & ~d.RH).sum()), faux_jumeaux_qui_passent_n1=int((d.euler_positif & ~d.RH & (d.rho_1 <= 1)).sum()),
        realises_hors_RH=int((d.realise & ~d.RH).sum()))))
    print(s.to_string(), flush=True)
    ex = example_table(); ex.to_csv(ROOT / "data" / "reduced_model_example.csv", index=False); print(ex.to_string(index=False))
    figure()
    print(f"total {time.time() - t0:.0f} s")
