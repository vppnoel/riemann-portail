"""V6.58 — La réalisation de Gram des courbes, certifiée à partir des seuls comptages : LDLᵀ exact (rationnels)
de la forme de Rosati B_jk = q^min(j,k) · S_|j−k| dans la base 1, T, …, T^{2g−1}.

Auteur et titulaire des droits : Vincent NOËL.
B = L·diag(d)·Lᵀ avec d_k > 0 pour tout k ⟺ B définie positive ⟺ RH pour la courbe (racines distinctes).
A = diag(√d)·Lᵀ réalise alors B(u) = ‖A u‖² : une réalisation de Gram construite avec les comptages N_1, …, N_g.
Sortie : data/gram_ldl_exact.json.
"""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
import json, sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from run_gram_modele_reduit import trace_form


def ldl_pivots(M):
    n = len(M); A = [[Fraction(x) for x in row] for row in M]; piv = []
    for k in range(n):
        d = A[k][k]; piv.append(d)
        if d == 0: break
        for i in range(k + 1, n):
            f = A[i][k] / d
            for j in range(k + 1, n): A[i][j] -= f * A[k][j]
    return piv


def main():
    rows = []
    for kind, path in (("courbe", "reduced_model_curves.csv"), ("faux jumeau", "reduced_model_fakes.csv")):
        df = pd.read_csv(D / path)
        if kind == "faux jumeau": df = df[df.euler_positif & ~df.RH]
        for _, x in df.iterrows():
            q, g = int(x.q), int(x.g)
            c = [int(v) for v in str(x.P).split()] if kind == "courbe" else ([1, int(x.c1), q] if g == 1 else [1, int(x.c1), int(x.c2), q * int(x.c1), q * q])
            piv = ldl_pivots(trace_form(c, q))
            first_bad = next((k for k, d in enumerate(piv) if d <= 0), None)
            rows.append(dict(type=kind, q=q, g=g, pivots_positifs=sum(d > 0 for d in piv), premier_pivot_non_positif=first_bad,
                             signe=("nul" if first_bad is not None and piv[first_bad] == 0 else "négatif") if first_bad is not None else "aucun"))
    df = pd.DataFrame(rows); cv, fj = df[df.type == "courbe"], df[df.type == "faux jumeau"]
    rep = dict(courbes=len(cv), courbes_2g_pivots_positifs=int((cv.pivots_positifs == 2 * cv.g).sum()),
               courbes_pivot_nul=cv[cv.signe == "nul"][["q", "g", "premier_pivot_non_positif"]].to_dict("records"),
               faux=len(fj), faux_pivot_negatif=int((fj.signe == "négatif").sum()), faux_pivot_nul=int((fj.signe == "nul").sum()),
               faux_index_du_premier_pivot_non_positif=fj.premier_pivot_non_positif.value_counts().sort_index().to_dict())
    (D / "gram_ldl_exact.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=int), encoding="utf-8")
    print(json.dumps(rep, indent=1, ensure_ascii=False, default=int))


if __name__ == "__main__":
    main()
