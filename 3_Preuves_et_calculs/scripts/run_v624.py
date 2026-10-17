"""V6.24 — A. J3 simplifié : additivité ou dérivée nulle ? B. « Le même calcul » que les deux tiers, sur nos zéros.

Prévisions écrites avant le calcul : data/prevision_v624.md.
A. Construction de Stepanov (V6.23) avec φ = x^p, x^p + 1, x^{2p} (dérivée nulle) et x^p + x (additif, dérivée 1).
B. Inégalité rang–trace (Alpöge–Furman) sur la métrique des zéros : G_{ρρ'} = noyau de Fejér de support [−A, A] en α
   (ĥ(u) = sinc²(π A u) en ordonnées dépliées). Distincts ≥ (tr G)²/tr G² = N²/Σ_{ρ,ρ'} sinc²(π A Δx) ;
   simples ≥ 2·distincts/N − 1. Valeur théorique (noyau sinus) : 1/(1 + ∫(1 − sinc²(πu)) sinc²(πAu) du ... ) calculée numériquement.
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"; sys.path.insert(0, str(ROOT / "scripts"))

def part_A():
    import run_frobenius_non_geometrique as F
    out = []
    for p in (61, 101):
        z = lambda n: np.zeros(n, dtype=np.int64)
        def mono(k, extra=None):
            v = z(k + 1); v[k] = 1
            if extra is not None:
                for i, c in extra.items(): v[i] = (v[i] + c) % p
            return v
        phis = {"x^p (additif, dérivée nulle)": mono(p), "x^p + 1 (dérivée nulle)": mono(p, {0: 1}),
                "x^{2p} (dérivée nulle)": mono(2 * p), "x^p + x (additif, dérivée 1)": mono(p, {1: 1})}
        for M, J in ((2, 3), (3, 3), (4, 3)):
            K = max(2, int(math.ceil(M * (p // 2) / (2 * J) * 0.8)))
            r = F.experiment(p, [1, 1, 0, 1], J, K, M, phis); out.append(r)
            print({k: (v["fonctions_auxiliaires"] if isinstance(v, dict) else v) for k, v in r.items()}, flush=True)
    return out

def unfold(t, q=1):
    return t / (2 * np.pi) * np.log(q * t / (2 * np.pi * np.e))

def sinc2(x):
    x = np.asarray(x, float); s = np.ones_like(x); m = np.abs(x) > 1e-12; s[m] = (np.sin(x[m]) / x[m]) ** 2; return s

def rank_trace(u, A):
    u = np.sort(u); N = len(u); tot = 0.0
    for i in range(N):
        d = u - u[i]; tot += float(np.sum(sinc2(np.pi * A * d)))
    D_ = N * N / tot
    return D_ / N, 2 * D_ / N - 1

def theory(A):
    """Noyau sinus : tr G²/N = 1 + ∫ R2(u) sinc²(πAu) du − (terme de densité retiré par la diagonale, déjà compté)."""
    u = np.linspace(-60, 60, 600001); du = u[1] - u[0]
    R2 = 1 - sinc2(np.pi * u)
    s = 1 + float(np.sum(R2 * sinc2(np.pi * A * u)) * du)
    return 1 / s, 2 / s - 1

def part_B():
    g = np.sort(pd.read_csv(D / "zeta_zeros_1500.csv").t.values); g = g[g > 0]
    L = np.sort(pd.read_csv(D / "L_chi5_zeros_600.csv").t.values); L = L[(L > 0) & (L <= 600)]
    gz = g[g <= 600]; tt = np.sort(np.r_[gz, L]); umix = unfold(tt) + unfold(tt, 5)
    rows = []
    for A in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0):
        dz, sz = rank_trace(unfold(g), A); dm, sm = rank_trace(umix, A); dt, st = theory(A)
        rows.append(dict(A=A, zeta_distincts=dz, zeta_simples=sz, melange_distincts=dm, melange_simples=sm, theorie_distincts=dt, theorie_simples=st))
        print(rows[-1], flush=True)
    return rows

def figure(out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    B = pd.DataFrame(json.loads((D / "v624.json").read_text(encoding="utf-8-sig"))["B"])
    fig, ax = plt.subplots(figsize=(9, 4.4))
    ax.plot(B.A, B.zeta_simples, "o-", color="#1d5d8c", label="nos 1 070 zéros de ζ (mesuré)")
    ax.plot(B.A, B.theorie_simples, "k--", label="noyau sinus (théorie, même noyau de Fejér)")
    ax.plot(B.A, B.melange_simples, "s-", color="#7a4fb0", label="ζ·L(χ5), familles étrangères")
    ax.axvline(1, color="grey", lw=0.8); ax.text(1.03, 0.05, "portée démontrée\n(Montgomery)", fontsize=8, color="grey")
    ax.axhline(0.6725, color="#2b7a57", lw=1); ax.text(2.1, 0.645, "0,6725 (Alpöge–Furman, noyau optimisé, sans hypothèse)", fontsize=8, color="#2b7a57")
    ax.set_xlabel("fenêtre A (support de Fourier de la corrélation de paires utilisée)"); ax.set_ylabel("borne : proportion de zéros simples")
    ax.set_ylim(0, 1.02); ax.set_title("Le même calcul (rang–trace) sur nos zéros"); ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)

if __name__ == "__main__" and "--figure" in sys.argv:
    figure(ROOT.parent / "1_Presentation" / "49_Le_meme_calcul.png"); sys.exit()

if __name__ == "__main__":
    rep = dict(A=part_A(), B=part_B())
    (D / "v624.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    figure(ROOT.parent / "1_Presentation" / "49_Le_meme_calcul.png")
