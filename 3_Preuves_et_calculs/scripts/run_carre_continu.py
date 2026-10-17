"""V6.27 — J6 : le carré, en continu.

Prévisions écrites avant le calcul : data/prevision_v627_carre.md (22 h 57 UTC).
Forme d'intersection virtuelle du doc. 46, depuis les seuls premiers, sur une grille de réglages (a, h, L).
Fiabilité : concordance des traces calculées depuis les premiers et depuis les zéros connus (relatif ≤ 1e-6).
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import run_prime_generator as RPG
from prime_generator import traces_from_primes, traces_from_zeros, g_hat, toeplitz_pencil

XMAX = 3000

def form(kind, t, L, h, a):
    G, _ = toeplitz_pencil(t, L); G = 0.5 * (G + G.conj().T)
    if kind == "zeta":
        n = np.arange(L); c2 = g_hat(0.5j, a).real
        av = math.sqrt(c2) * np.exp(-n * h / 2); bv = math.sqrt(c2) * np.exp(n * h / 2)
        M = np.zeros((L + 2, L + 2), dtype=complex); M[0, 1] = M[1, 0] = 1
        M[0, 2:] = M[2:, 0] = av; M[1, 2:] = M[2:, 1] = bv; M[2:, 2:] = np.outer(av, bv) + np.outer(bv, av) - G
    else:
        M = -G
    ev = np.linalg.eigvalsh(M); s = 1e-11 * np.max(np.abs(ev))
    return int(np.sum(ev > s)) - (1 if kind == "zeta" else 0), int(np.sum(ev > s))

def main():
    Z = {k: RPG.zeros(k) for k in ("zeta", "L_chi5", "DH")}
    rows = []
    for a in (0.02, 0.04, 0.08, 0.16):
        for h in (0.005, 0.01, 0.02):
            Lmax = int((math.log(XMAX) - 2 * a) / h)
            Ls = sorted({int(round(Lmax * f)) for f in (0.35, 0.5, 0.7, 0.85, 1.0)})
            for kind in ("zeta", "L_chi5", "DH"):
                M = int(math.exp(Lmax * h + 2 * a)) + 2
                tP = traces_from_primes(kind, RPG.coeff_cache(kind, M), Lmax, h, a)
                tZ = traces_from_zeros(Z[kind], Lmax, h, a)
                for L in Ls:
                    if L < 10: continue
                    audit = float(np.max(np.abs(tP[:L + 1] - tZ[:L + 1])) / np.max(np.abs(tZ[:L + 1])))
                    extra, pos = form(kind, tP[:L + 1], L, h, a)
                    rows.append(dict(objet=kind, a=a, h=h, L=L, X=round(math.exp(L * h + 2 * a), 1), audit=audit, fiable=audit <= 1e-6, positives=pos, en_trop=extra))
            print(f"a={a} h={h} fait", flush=True)
    df = pd.DataFrame(rows); df.to_csv(D / "carre_continu.csv", index=False)
    f = df[df.fiable]
    z, l, d = f[f.objet == "zeta"], f[f.objet == "L_chi5"], f[f.objet == "DH"]
    rep = dict(reglages=int(len(df)), fiables=int(len(f)),
               zeta_fiables=int(len(z)), zeta_une_seule_positive=int((z.positives == 1).sum()),
               L_fiables=int(len(l)), L_sans_positive=int((l.positives == 0).sum()),
               DH_fiables=int(len(d)), DH_en_trop_des_X61=int((d[d.X >= 61].en_trop > 0).sum()), DH_X_ge_61=int((d.X >= 61).sum()),
               DH_en_trop_pair=int((d.en_trop % 2 == 0).sum()),
               non_fiables_par_objet=df[~df.fiable].groupby("objet").size().to_dict(),
               zeta_non_fiables_avec_positive_en_trop=int(((df.objet == "zeta") & ~df.fiable & (df.en_trop != 0)).sum()))
    # P3 : à X à peu près fixé, dépendance au pas h (a fixé)
    p3 = []
    for a, g in d.groupby("a"):
        for X0 in (100, 400, 1500, 3000):
            sel = g.iloc[(g.X - X0).abs().argsort()].groupby("h").head(1)
            sel = sel[(sel.X / X0).between(0.8, 1.25)]
            if sel.h.nunique() >= 2: p3.append(dict(a=a, X_vise=X0, en_trop_par_h={str(r.h): int(r.en_trop) for r in sel.itertuples()}, X={str(r.h): r.X for r in sel.itertuples()}))
    rep["P3"] = p3
    (D / "carre_continu.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rep, indent=1, ensure_ascii=False))

if __name__ == "__main__" and "--figure" not in sys.argv:
    main()

def figure(out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    df = pd.read_csv(D / "carre_continu.csv")
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    for kind, col, nm, mk in (("zeta", "#1d5d8c", "ζ (positives − 1)", "o"), ("L_chi5", "#7a4fb0", "L(χ5)", "s")):
        s = df[df.objet == kind]; ax[0].scatter(s.X, s.en_trop + (0.08 if kind == "zeta" else -0.08), s=14, color=col, marker=mk, label=nm)
    s = df[df.objet == "DH"]; ax[0].scatter(s.X, s.en_trop, s=14, color="#c0392b", marker="^", label="Davenport–Heilbronn")
    ax[0].set_xscale("log"); ax[0].set_xlabel("nombres premiers utilisés (jusqu'à X)"); ax[0].set_ylabel("directions positives en trop")
    ax[0].set_title("60 réglages (a, h, L) par objet : ζ et L(χ5) toujours à 0"); ax[0].legend(fontsize=8)
    for (h, g), col in zip(s.groupby("h"), ("#c0392b", "#e67e22", "#8e44ad")):
        for a, gg in g.groupby("a"):
            ax[1].plot(gg.X, gg.en_trop, "-", color=col, alpha=0.35 + a * 3, lw=1)
        ax[1].plot([], [], color=col, label=f"pas h = {h}".replace(".", ","))
    ax[1].set_xscale("log"); ax[1].set_xlabel("X"); ax[1].set_ylabel("directions en trop (DH)")
    ax[1].set_title("DH : le nombre dépend du pas h et de la largeur a"); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)

if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--figure":
    figure(ROOT.parent / "1_Presentation" / "52_Le_carre_en_continu.png")
