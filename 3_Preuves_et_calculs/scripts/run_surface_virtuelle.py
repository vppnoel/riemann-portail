"""V6.21 — Axe J : la surface virtuelle.

Prévisions écrites avant le calcul : data/prevision_v621_surface.md (19 h 10 UTC).

Dans le Modèle réduit, la surface C × C existe. Ses courbes : les fibres f1 = pt × C, f2 = C × pt, et les graphes de Frobenius
Γ_n = {(x, F^n x)}. Intersections (N_d = q^d + 1 − S_d, S_d = Σ α_i^d) :
    f1·f1 = f2·f2 = 0, f1·f2 = 1, Γ_n·f1 = 1, Γ_n·f2 = q^n, Γ_n·Γ_n = q^n (2 − 2g), Γ_m·Γ_n = q^min(m,n) N_|m−n| (m ≠ n).
Indice de Hodge : sur toute famille de courbes, la forme d'intersection a au plus une direction positive. C'est la positivité
de Castelnuovo, d'où Weil tire RH.
Orthogonalement aux fibres, avec D_n = q^−n/2 Γ_n : D_m·D_n = −q^−|m−n|/2 S_|m−n|, diagonale −2g, c'est-à-dire
−Σ_i e^{i(m−n)θ_i} quand |α_i| = √q : l'opposé de la forme de Toeplitz du corpus (doc. 29), qui est la métrique des zéros.

Pour ζ, la surface n'existe pas. On construit sa forme d'intersection « virtuelle » par le même dictionnaire, depuis les seuls
nombres premiers (formule explicite, doc. 33) : fibres ↔ pôle, Γ_m·Γ_n ↔ puissances de premiers, Γ·Γ ↔ terme archimédien.
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
from function_field import power_sums, roots_alpha

TOL = 1e-9

def intersection_gram(c, q, g, K):
    """Forme d'intersection normalisée sur {f1, f2, D_0, …, D_K}, D_n = q^−n/2 Γ_n (calcul en flottants à partir des S_d exacts)."""
    S = [2 * g] + power_sums(c, K + 1)                   # S_0 = 2g
    n = K + 1; M = np.zeros((n + 2, n + 2))
    M[0, 1] = M[1, 0] = 1.0
    for i in range(n):
        M[0, 2 + i] = M[2 + i, 0] = q ** (-i / 2)        # D_i · f1
        M[1, 2 + i] = M[2 + i, 1] = q ** (i / 2)         # D_i · f2
        for j in range(n):
            d = abs(i - j)
            M[2 + i, 2 + j] = (2 - 2 * g) if d == 0 else (q ** (d / 2) + q ** (-d / 2) - S[d] * q ** (-d / 2))
    return M

def perp_block(c, q, g, K):
    """Bloc orthogonal aux fibres : −q^−|d|/2 S_|d| (diagonale −2g)."""
    S = [2 * g] + power_sums(c, K + 1); n = K + 1
    d = np.abs(np.subtract.outer(np.arange(n), np.arange(n)))
    return -np.array([[S[x] * q ** (-x / 2) for x in row] for row in d], dtype=float)

def inertia(M, tol=TOL):
    ev = np.linalg.eigvalsh(0.5 * (M + M.T)); s = tol * max(1.0, np.max(np.abs(ev)))
    return int(np.sum(ev > s)), int(np.sum(ev < -s)), int(np.sum(np.abs(ev) <= s))

def off_circle(c, q, tol=1e-6):
    return int(np.sum(np.abs(np.abs(roots_alpha(c)) / math.sqrt(q) - 1) > tol))

def part_A():
    rows = []
    cur = pd.read_csv(D / "reduced_model_curves.csv")
    for _, r in cur.iterrows():
        q, g = int(r.q), int(r.g); c = [int(x) for x in str(r.P).split()]
        Kf = 2 * g + 1
        pf, nf, zf = inertia(intersection_gram(c, q, g, Kf))
        pp, npp, zp = inertia(perp_block(c, q, g, 4 * g))
        rows.append(dict(type="courbe", q=q, g=g, P=r.P, positives_forme_complete=pf, positives_perp_4g=pp, rang_perp_4g=pp + npp, hors_cercle=off_circle(c, q)))
    tw = pd.read_csv(D / "reduced_model_fakes.csv"); tw = tw[tw.euler_positif & ~tw.RH]
    for _, r in tw.iterrows():
        q, g = int(r.q), int(r.g); c = [1, int(r.c1), q] if g == 1 else [1, int(r.c1), int(r.c2), q * int(r.c1), q * q]
        pf, nf, zf = inertia(intersection_gram(c, q, g, 2 * g + 1))
        pp, npp, zp = inertia(perp_block(c, q, g, 4 * g))
        rows.append(dict(type="faux jumeau", q=q, g=g, P=" ".join(map(str, c)), positives_forme_complete=pf, positives_perp_4g=pp, rang_perp_4g=pp + npp, hors_cercle=off_circle(c, q)))
    df = pd.DataFrame(rows); df.to_csv(D / "surface_virtuelle_modele_reduit.csv", index=False)
    cv, fj = df[df.type == "courbe"], df[df.type == "faux jumeau"]
    return dict(courbes=int(len(cv)), courbes_une_seule_positive=int((cv.positives_forme_complete == 1).sum()),
                courbes_perp_sans_positive=int((cv.positives_perp_4g == 0).sum()), courbes_rang_perp_egal_2g=int((cv.rang_perp_4g == 2 * cv.g).sum()),
                faux_jumeaux=int(len(fj)), jumeaux_au_moins_deux_positives=int((fj.positives_forme_complete >= 2).sum()),
                jumeaux_surplus_egal_hors_cercle_sur_2=int((fj.positives_forme_complete - 1 == fj.hors_cercle // 2).sum()),
                jumeaux_rang_perp_egal_2g=int((fj.rang_perp_4g == 2 * fj.g).sum()),
                repartition_jumeaux=fj.groupby(["hors_cercle", "positives_forme_complete"]).size().reset_index(name="n").to_dict("records"))

def part_B():
    """ζ, L(χ5), DH : forme d'intersection virtuelle depuis les premiers (paramètres du doc. 33)."""
    import run_prime_generator as RPG
    from prime_generator import traces_from_primes, g_hat, toeplitz_pencil
    a, h = RPG.MAIN["a"], RPG.MAIN["h"]; out = {}
    for kind in ("zeta", "L_chi5", "DH"):
        rows = []
        for L in (100, 200, 300, 400, 600):
            M = int(math.exp(L * h + 2 * a)) + 2
            t = traces_from_primes(kind, RPG.coeff_cache(kind, M), L, h, a)
            G, _ = toeplitz_pencil(t, L); G = 0.5 * (G + G.conj().T)           # métrique des zéros, calculée sans zéro
            pole = kind == "zeta"
            n = np.arange(L)
            if pole:
                c2 = g_hat(0.5j, a).real; av = math.sqrt(c2) * np.exp(-n * h / 2); bv = math.sqrt(c2) * np.exp(n * h / 2)
                P = np.outer(av, bv) + np.outer(bv, av)                    # contribution des fibres (le pôle)
                Mfull = np.zeros((L + 2, L + 2), dtype=complex); Mfull[0, 1] = Mfull[1, 0] = 1
                Mfull[0, 2:] = Mfull[2:, 0] = av; Mfull[1, 2:] = Mfull[2:, 1] = bv; Mfull[2:, 2:] = P - G
            else:
                Mfull = -G
            ev = np.linalg.eigvalsh(Mfull); s = 1e-11 * np.max(np.abs(ev))
            evG = np.linalg.eigvalsh(G); sG = 1e-11 * np.max(np.abs(evG))
            rows.append(dict(L=L, X=M, positives=int(np.sum(ev > s)), negatives_metrique=int(np.sum(evG < -sG)), rang_metrique=int(np.sum(np.abs(evG) > sG)),
                             autointersection_diag=float(np.real(Mfull[2, 2] if pole else Mfull[0, 0]))))
        out[kind] = rows
    pd.DataFrame([dict(objet=k, **r) for k, v in out.items() for r in v]).to_csv(D / "surface_virtuelle_premiers.csv", index=False)
    return out

def figure(out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    A = pd.read_csv(D / "surface_virtuelle_modele_reduit.csv"); B = pd.read_csv(D / "surface_virtuelle_premiers.csv")
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.2))
    cv = A[A.type == "courbe"]; fj = A[A.type == "faux jumeau"]
    lab = ["courbes\n(425)", "jumeaux, 2 racines\nhors du cercle", "jumeaux, 4 racines\nhors du cercle"]
    vals = [cv.positives_forme_complete.mean(), fj[fj.hors_cercle == 2].positives_forme_complete.mean(), fj[fj.hors_cercle == 4].positives_forme_complete.mean()]
    ax[0].bar(lab, vals, color=["#2b7a57", "#b8650f", "#c0392b"]); ax[0].axhline(1, color="k", lw=0.8, ls="--")
    ax[0].set_ylabel("directions positives"); ax[0].set_title("Modèle réduit : la vraie surface C × C (indice de Hodge = 1)")
    for kind, col, nm in (("zeta", "#1d5d8c", "ζ"), ("L_chi5", "#7a4fb0", "L(χ5)"), ("DH", "#c0392b", "Davenport–Heilbronn")):
        s = B[B.objet == kind]; ax[1].plot(s.X, s.positives, "o-", color=col, label=nm)
    ax[1].set_xscale("log"); ax[1].axhline(1, color="k", lw=0.8, ls="--"); ax[1].set_xlabel("nombres premiers utilisés (jusqu'à X)")
    ax[1].set_ylabel("directions positives"); ax[1].set_title("La surface virtuelle, calculée depuis les premiers"); ax[1].legend()
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)

if __name__ == "__main__" and "--figure" in sys.argv:
    figure(ROOT.parent / "1_Presentation" / "46_La_surface_virtuelle.png"); sys.exit()

if __name__ == "__main__":
    rep = dict(A=part_A()); print(json.dumps(rep, indent=1, ensure_ascii=False), flush=True)
    rep["B"] = part_B(); print(json.dumps(rep["B"], indent=1, ensure_ascii=False))
    (D / "surface_virtuelle.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
