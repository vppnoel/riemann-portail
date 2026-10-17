"""V6.58 — D'où vient le signe dans le Modèle réduit : comptage, degré, ou carré ?

Auteur et titulaire des droits : Vincent NOËL.
Prévisions écrites avant le calcul : data/prevision_v658_gram.md.

Pour chaque polynôme L du Modèle réduit (425 courbes, 220 faux jumeaux), χ(T) = T^{2g} P(1/T), K = Q[T]/(χ), ι(T) = q/T.
- Niveau 1, le comptage : a_d ≥ 0 (donné).
- Niveau 2, le degré : N(u) = ∏ u(α_i) = Res(χ, u) (degré de l'isogénie u(F) pour une vraie jacobienne).
- Niveau 3, le carré : B(u) = Tr(u·ι(u)) ; dans la base T^j, B_jk = q^min(j,k) · S_|j−k| (entiers), la métrique de Weil.
Tout se calcule à partir des seuls comptages (S_d). Sorties : data/gram_modele_reduit.csv/.json, 1_Presentation/80_Trois_niveaux_du_signe.png.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import product
from pathlib import Path
import json, math, sys
import numpy as np, pandas as pd
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "src"))
from function_field import power_sums

T = sp.Symbol("T")


def chi_coeffs(c):
    """P(u) = Σ c_k u^k (c_0 = 1) → χ(T) = Σ c_k T^{2g−k} (coefficients du degré haut au bas)."""
    return list(c)                                   # χ(T) = T^{2g} P(1/T) : mêmes coefficients, lus dans l'autre sens


def trace_form(c, q):
    m = len(c) - 1; S = [m] + power_sums(c, m)
    return [[q ** min(j, k) * S[abs(j - k)] for k in range(m)] for j in range(m)]


def inertia_exact(M):
    """Signature (n+, n−, n0) d'une matrice symétrique entière : valeurs propres en précision 60 chiffres (mpmath),
    seuil relatif 1e-40 (les entrées sont des entiers exacts)."""
    import mpmath as mp
    mp.mp.dps = 60
    E = mp.eigsy(mp.matrix(M))[0]; vals = [E[i] for i in range(len(M))]; s = max(abs(v) for v in vals) * mp.mpf("1e-40")
    return sum(v > s for v in vals), sum(v < -s for v in vals), sum(abs(v) <= s for v in vals)


def analyse(c, q, g):
    chi = sp.Poly(sum(ck * T ** (len(c) - 1 - k) for k, ck in enumerate(c)), T)
    roots = np.roots(np.array(c, dtype=float))                      # racines de χ = α_i
    r = int(np.sum(np.abs(np.abs(roots) / math.sqrt(q) - 1) > 1e-7))
    # racines réelles de multiplicité impaire (exact)
    odd_real = 0
    for fac, mult in sp.factor_list(chi)[1]:
        nreal = len(sp.real_roots(fac))
        if mult % 2 == 1: odd_real += nreal
    npos, nneg, nz = inertia_exact(trace_form(c, q))
    # niveau 2 : chercher u (coeffs entiers |.| ≤ 3, degré ≤ 2g − 1) avec N(u) < 0
    first = None
    if odd_real:
        best = None
        for co in product(range(-3, 4), repeat=2 * g):
            if not any(co): continue
            val = np.prod([sum(co[k] * a ** k for k in range(2 * g)) for a in roots])
            if val.real < -1e-6:
                h = max(abs(x) for x in co); s = sum(abs(x) for x in co)
                if best is None or (h, s) < best[0]: best = ((h, s), co)
        if best:
            co = best[1]; u = sp.Poly(sum(co[k] * T ** k for k in range(2 * g)), T)
            res = int(sp.resultant(chi.as_expr(), u.as_expr(), T))      # N(u) exact
            first = dict(u=list(co), N=res, hauteur=best[0][0])
    return dict(r=r, racines_reelles_impaires=odd_real, B_pos=npos, B_neg=nneg, B_nul=nz, u_degre_negatif=first)


def main():
    rows = []
    cur = pd.read_csv(D / "reduced_model_curves.csv")
    for _, x in cur.iterrows():
        c = [int(v) for v in str(x.P).split()]; rows.append(dict(type="courbe", q=int(x.q), g=int(x.g), P=x.P, **analyse(c, int(x.q), int(x.g))))
    fk = pd.read_csv(D / "reduced_model_fakes.csv"); fk = fk[fk.euler_positif & ~fk.RH]
    for _, x in fk.iterrows():
        q, g = int(x.q), int(x.g)
        c = [1, int(x.c1), q] if g == 1 else [1, int(x.c1), int(x.c2), q * int(x.c1), q * q]
        rows.append(dict(type="faux jumeau", q=q, g=g, P=" ".join(map(str, c)), **analyse(c, q, g)))
    df = pd.DataFrame(rows)
    df["u_negatif"] = df.u_degre_negatif.apply(lambda v: json.dumps(v) if v else "")
    df.drop(columns=["u_degre_negatif"]).to_csv(D / "gram_modele_reduit.csv", index=False)
    cv, fj = df[df.type == "courbe"], df[df.type == "faux jumeau"]
    f2, f4 = fj[fj.r == 2], fj[fj.r == 4]
    rep = dict(
        G1=dict(courbes=len(cv), sans_racine_reelle_impaire=int((cv.racines_reelles_impaires == 0).sum()), B_sans_negatif=int((cv.B_neg == 0).sum()),
                B_rang_2g=int((cv.B_pos == 2 * cv.g).sum())),
        G2=dict(faux_r4=len(f4), r4_sans_racine_reelle_impaire=int((f4.racines_reelles_impaires == 0).sum()),
                faux_r2=len(f2), r2_avec_racine_reelle_impaire=int((f2.racines_reelles_impaires > 0).sum()),
                genre1_dans_r2=int((f2.g == 1).sum())),
        G3=dict(r2_avec_u_trouve=int(f2.u_degre_negatif.notna().sum()), hauteurs=f2.u_degre_negatif.dropna().apply(lambda v: v["hauteur"]).value_counts().to_dict()),
        G4=dict(faux=len(fj), B_indefinie=int((fj.B_neg > 0).sum()), B_neg_egal_r_sur_2=int((fj.B_neg == fj.r // 2).sum())),
        exemples=dict(r2=f2.u_degre_negatif.dropna().iloc[0] if len(f2) else None, P_r2=f2.P.iloc[0] if len(f2) else None))
    (D / "gram_modele_reduit.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=int), encoding="utf-8")
    figure(df, ROOT.parent / "1_Presentation" / "80_Trois_niveaux_du_signe.png")
    print(json.dumps(rep, indent=1, ensure_ascii=False, default=int))


def figure(df, out, lang="fr"):
    en = lang == "en"
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    groups = [("425 curves" if en else "425 courbes", df[df.type == "courbe"]),
              ("fake twins,\n2 roots off the circle" if en else "faux jumeaux,\n2 racines hors du cercle", df[(df.type != "courbe") & (df.r == 2)]),
              ("fake twins,\n4 roots off the circle" if en else "faux jumeaux,\n4 racines hors du cercle", df[(df.type != "courbe") & (df.r == 4)])]
    levels = (["1. counts\na_d ≥ 0", "2. degree\nN(u) ≥ 0 for all u", "3. square\nB(u) ≥ 0 for all u"] if en else
              ["1. comptage\na_d ≥ 0", "2. degré\nN(u) ≥ 0 pour tout u", "3. carré\nB(u) ≥ 0 pour tout u"])
    M = np.array([[1.0, float((g.racines_reelles_impaires == 0).mean()), float((g.B_neg == 0).mean())] for _, g in groups])
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    ax.imshow(M, cmap="Greens", vmin=0, vmax=1.25, aspect="auto")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{M[i, j] * 100:.0f} %", ha="center", va="center", fontsize=11, color="white" if M[i, j] > 0.5 else "#8b1a1a", fontweight="bold")
    ax.set_xticks(range(3)); ax.set_xticklabels(levels, fontsize=9); ax.set_yticks(range(3)); ax.set_yticklabels([g for g, _ in groups], fontsize=9)
    ax.set_title("Share of polynomials satisfying each positivity level\n(RH ⟺ level 3; everything is computed from point counts)" if en else
                 "Part des polynômes qui satisfont chaque niveau de positivité\n(RH ⟺ niveau 3 ; tout est calculé à partir des comptages)", fontsize=10)
    fig.text(0.01, 0.01, "For ζ (analogue, proved): levels 1 and 2; level 3 is RH." if en else "Pour ζ (analogue, démontré) : niveaux 1 et 2 ; le niveau 3 est RH.", fontsize=8, color="#333")
    fig.text(0.99, 0.01, "Programme Riemann V6.58 — © Vincent NOËL", ha="right", fontsize=7, color="#777")
    fig.tight_layout(rect=(0, 0.04, 1, 1)); fig.savefig(out, dpi=140); plt.close(fig)


if __name__ == "__main__":
    if "--figure-en" in sys.argv:                                   # figure anglaise depuis les données déjà calculées
        figure(pd.read_csv(D / "gram_modele_reduit.csv"), ROOT.parent / "1_Presentation" / "english" / "80_three_levels_EN.png", "en")
    else:
        main()
