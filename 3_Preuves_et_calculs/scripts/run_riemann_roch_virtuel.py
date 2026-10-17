"""V6.22 — Axe J2 : le Riemann–Roch virtuel, dans le Modèle réduit.

Prévisions écrites avant le calcul : data/prevision_v622_riemann_roch.md (22 h 01 UTC).
Trois contraintes vraies pour toute courbe lisse de genre g sur F_q, démontrées sans RH, testées le long de la tour F_{q^m} :
 (E) existence : h_m = #Pic⁰(F_{q^m}) = Π(1 − α_i^m) ≥ 1 ;
 (C) dimension (Clifford) : A_n ≤ h_m (Q^{⌊n/2⌋+1} − 1)/(Q − 1) pour 1 ≤ n ≤ 2g − 2, Q = q^m, A_n = nombre de diviseurs effectifs ;
 (S) Stepanov–Bombieri : si Q est un carré et Q > (g + 1)⁴, N_m ≤ Q + (2g + 1)√Q + 1.
Castelnuovo (doc. 28) : |S_m| ≤ 2g q^{m/2}. Tout est calculé en entiers exacts à partir des comptages.
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys
from math import isqrt
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "src"))
from function_field import power_sums

M = 80

def elem_from_power(p, k):
    """e_1..e_k des racines à partir des sommes de puissances p[1..k] (Newton, entiers exacts)."""
    e = [1]
    for j in range(1, k + 1):
        s = sum((-1) ** (i - 1) * e[j - i] * p[i] for i in range(1, j + 1))
        assert s % j == 0; e.append(s // j)
    return e

def floors(c, q, g):
    S = power_sums(c, 2 * g * M + 2); S = [2 * g] + S             # S[k] = Σ α^k
    out = dict(E=None, C=None, S=None, castelnuovo=None, E_tordu=None, S_tordu=None)
    for m in range(1, M + 1):
        Q = q ** m
        p = [None] + [S[k * m] for k in range(1, 2 * g + 1)]
        e = elem_from_power(p, 2 * g)
        Pm = [(-1) ** j * e[j] for j in range(2 * g + 1)]          # P_m(T) = Π(1 − α^m T)
        h = sum(Pm)
        Nm = Q + 1 - S[m]
        if out["E"] is None and h < 1: out["E"] = m
        if out["C"] is None and g >= 2 and h >= 1:
            # Z_m(T) = P_m(T) / ((1 − T)(1 − Q T)) : coefficients A_0..A_{2g−2}
            inv = [(Q ** (j + 1) - 1) // (Q - 1) for j in range(2 * g - 1)]   # 1/((1−T)(1−QT))
            A = [sum(Pm[i] * inv[n - i] for i in range(0, min(n, 2 * g) + 1)) for n in range(2 * g - 1)]
            for n in range(1, 2 * g - 1):
                if A[n] > h * (Q ** (n // 2 + 1) - 1) // (Q - 1): out["C"] = m; break
        r = isqrt(Q)
        if out["S"] is None and r * r == Q and Q > (g + 1) ** 4 and Nm > Q + (2 * g + 1) * r + 1: out["S"] = m
        # tordu quadratique sur F_{q^m} (involution hyperelliptique) : racines −α^m, Q + 1 + S_m points, Pic⁰ d'ordre Π(1 + α^m)
        ht = sum(Pm[j] * (-1) ** j for j in range(2 * g + 1))
        if out["E_tordu"] is None and ht < 1: out["E_tordu"] = m
        if out["S_tordu"] is None and r * r == Q and Q > (g + 1) ** 4 and Q + 1 + S[m] > Q + (2 * g + 1) * r + 1: out["S_tordu"] = m
        if out["castelnuovo"] is None and S[m] * S[m] > 4 * g * g * Q: out["castelnuovo"] = m
    return out

def main():
    rows = []
    cur = pd.read_csv(D / "reduced_model_curves.csv")
    for _, r in cur.iterrows():
        q, g = int(r.q), int(r.g); c = [int(x) for x in str(r.P).split()]
        rows.append(dict(type="courbe", q=q, g=g, P=r.P, **floors(c, q, g)))
    tw = pd.read_csv(D / "reduced_model_fakes.csv"); tw = tw[tw.euler_positif & ~tw.RH]
    for _, r in tw.iterrows():
        q, g = int(r.q), int(r.g); c = [1, int(r.c1), q] if g == 1 else [1, int(r.c1), int(r.c2), q * int(r.c1), q * q]
        rows.append(dict(type="faux jumeau", q=q, g=g, P=" ".join(map(str, c)), **floors(c, q, g)))
    df = pd.DataFrame(rows); df.to_csv(D / "riemann_roch_virtuel.csv", index=False)
    cv, fj = df[df.type == "courbe"], df[df.type == "faux jumeau"]
    first_EC = fj[["E", "C"]].min(axis=1)
    allc = fj[["E", "C", "S"]].min(axis=1)
    alltw = fj[["E", "C", "S", "E_tordu", "S_tordu"]].min(axis=1)
    rep = dict(
        courbes=int(len(cv)), courbes_violant_E=int(cv.E.notna().sum()), courbes_violant_C=int(cv.C.notna().sum()), courbes_violant_S=int(cv.S.notna().sum()),
        courbes_violant_castelnuovo=int(cv.castelnuovo.notna().sum()),
        jumeaux=int(len(fj)), jumeaux_attrapes_E=int(fj.E.notna().sum()), jumeaux_attrapes_C=int(fj.C.notna().sum()), jumeaux_attrapes_S=int(fj.S.notna().sum()),
        jumeaux_attrapes_E_ou_C=int(first_EC.notna().sum()), jumeaux_attrapes_au_moins_un=int(allc.notna().sum()),
        jumeaux_attrapes_castelnuovo=int(fj.castelnuovo.notna().sum()),
        E_ou_C_avant_castelnuovo=int((first_EC < fj.castelnuovo).sum()), E_ou_C_meme_etage=int((first_EC == fj.castelnuovo).sum()),
        courbes_violant_tordu=int((cv.E_tordu.notna() | cv.S_tordu.notna()).sum()),
        jumeaux_attrapes_avec_tordu=int(alltw.notna().sum()), mediane_etage_avec_tordu=float(alltw.median()),
        mediane_rapport_avec_tordu_sur_castelnuovo=float((alltw / fj.castelnuovo).median()),
        avec_tordu_avant_castelnuovo=int((alltw < fj.castelnuovo).sum()), avec_tordu_meme_etage=int((alltw == fj.castelnuovo).sum()),
        etage_max_avec_tordu=float(alltw.max()),
        mediane_rapport_S_sur_castelnuovo=float((fj.S / fj.castelnuovo).median()),
        S_avant_castelnuovo=int((fj.S < fj.castelnuovo).sum()),
        par_genre={int(g): dict(n=int(len(s)), E=int(s.E.notna().sum()), C=int(s.C.notna().sum()), S=int(s.S.notna().sum()),
                                mediane_etage_castelnuovo=float(s.castelnuovo.median()), mediane_etage_S=float(s.S.median()) if s.S.notna().any() else None)
                   for g, s in fj.groupby("g")})
    (D / "riemann_roch_virtuel.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rep, indent=1, ensure_ascii=False))

def figure(out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
    d = pd.read_csv(D / "riemann_roch_virtuel.csv"); f = d[d.type == "faux jumeau"]
    tw = f[["E", "C", "S", "E_tordu", "S_tordu"]].min(axis=1)
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.2))
    lab = ["(E) existence", "(C) Clifford", "(S) Stepanov", "(S)+(S′) avec\nle tordu", "Castelnuovo\n(la surface)"]
    val = [f.E.notna().sum(), f.C.notna().sum(), f.S.notna().sum(), tw.notna().sum(), f.castelnuovo.notna().sum()]
    ax[0].bar(lab, val, color=["#8c96a4", "#8c96a4", "#b8650f", "#2b7a57", "#1d5d8c"]); ax[0].axhline(len(f), color="k", lw=0.8, ls="--")
    ax[0].set_ylabel("faux jumeaux démasqués (sur 220)"); ax[0].set_title("Quelle propriété, démontrée sans RH, démasque les faux jumeaux ?")
    for i, v in enumerate(val): ax[0].text(i, v + 3, str(int(v)), ha="center")
    m = np.arange(1, 11); w = 0.4
    ax[1].bar(m - w / 2, [(f.castelnuovo == k).sum() for k in m], w, color="#1d5d8c", label="Castelnuovo (surface)")
    ax[1].bar(m + w / 2, [(tw == k).sum() for k in m], w, color="#2b7a57", label="Stepanov + tordu (courbe)")
    ax[1].set_xlabel("étage m de la tour F_{q^m} où le jumeau tombe"); ax[1].set_ylabel("nombre de jumeaux"); ax[1].legend()
    ax[1].set_title("La courbe seule suffit, un peu plus tard que la surface")
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)

if __name__ == "__main__":
    main(); figure(ROOT.parent / "1_Presentation" / "47_Le_riemann_roch_virtuel.png")
