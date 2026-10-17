"""V6.19 — La Rencontre à n : la marge d'un n-uplet de zéros est la corrélation à n points.

Prévisions écrites avant le calcul : data/prevision_v619.md (18 h 18 UTC).

Identité (§1 du document 43) : n atomes aux angles θ_l, fenêtre de N échantillons x_l(j) = e^{ijθ_l}, Gram G = V V*.
G_lm = e^{i(N−1)(θ_l−θ_m)/2} · sin(NΔ/2)/sin(Δ/2) ; donc G/N = U K U* avec U diagonale unitaire et K_lm = D_N(θ_l − θ_m),
D_N(Δ) = sin(NΔ/2)/(N sin(Δ/2)). D'où det(G/N) = det K = (2π/N)^n R_n^CUE(N)(θ_1, …, θ_n) : la marge normalisée d'un n-uplet
est la corrélation à n points du CUE(N), normalisée. Limite de Heisenberg : det[sinc(π(s_l − s_m))] (noyau sinus).

Mesures : densité à trois points des zéros de ζ (1 070 zéros, t ≤ 1 500), dépliés par la formule de Riemann–von Mangoldt,
comparée au noyau sinus R3, à Poisson (1) et au produit des paires R2(x)R2(y) ; même mesure pour ζ·L(χ5) (t ≤ 600).
"""
from __future__ import annotations
from pathlib import Path
import json, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"

def DN(d, N):
    d = np.asarray(d, float); s = np.sin(d / 2)
    return np.where(np.abs(s) < 1e-15, 1.0, np.sin(N * d / 2) / (N * np.where(np.abs(s) < 1e-15, 1.0, s)))

def sinc(x):
    x = np.asarray(x, float); return np.where(np.abs(x) < 1e-12, 1.0, np.sin(x) / np.where(np.abs(x) < 1e-12, 1.0, x))

def gram_margin(theta, N):
    V = np.exp(1j * np.outer(theta, np.arange(N))); G = V @ V.conj().T
    return float(np.linalg.det(G / N).real)

def kernel_det(theta, N):
    return float(np.linalg.det(DN(np.subtract.outer(theta, theta), N)))

def R3(x, y):
    """Noyau sinus, trois points 0, x, x + y (densité normalisée)."""
    a, b, c = sinc(np.pi * x), sinc(np.pi * y), sinc(np.pi * (x + y))
    return 1 - a * a - b * b - c * c + 2 * a * b * c

def R2(x): return 1 - sinc(np.pi * x) ** 2

def R3_melange(f1):
    """Superposition de deux familles indépendantes de fractions f1, 1 − f1 (chacune suit le noyau sinus à sa propre échelle)."""
    f2 = 1 - f1
    def R(x, y):
        out = f1 ** 3 * R3(f1 * x, f1 * y) + f2 ** 3 * R3(f2 * x, f2 * y)
        for fa, fb in ((f1, f2), (f2, f1)):
            out = out + fa ** 2 * fb * (R2(fa * x) + R2(fa * y) + R2(fa * (x + y)))
        return out
    return R

def unfold_zeta(t): return t / (2 * np.pi) * np.log(t / (2 * np.pi * np.e)) + 7 / 8
def unfold_L(t, q): return t / (2 * np.pi) * np.log(q * t / (2 * np.pi * np.e))

def triple_hist(u, edges):
    """Triplets ordonnés i < j < k : x = u_j − u_i, y = u_k − u_j, dans le carré des bords."""
    u = np.sort(u); top = edges[-1]; H = np.zeros((len(edges) - 1, len(edges) - 1)); n0 = 0
    for i in range(len(u)):
        if u[i] + 2 * top > u[-1]: break           # i doit laisser la place à x, y ≤ top
        n0 += 1
        js = np.arange(i + 1, np.searchsorted(u, u[i] + top, "right"))
        for j in js:
            x = u[j] - u[i]; ks = np.arange(j + 1, np.searchsorted(u, u[j] + top, "right"))
            if len(ks): H += np.histogram2d(np.full(len(ks), x), u[ks] - u[j], bins=[edges, edges])[0]
    return H, n0

def expected(fun, edges, n0, sub=8):
    h = edges[1] - edges[0]; k = len(edges) - 1; E = np.zeros((k, k))
    off = (np.arange(sub) + 0.5) / sub * h
    for a in range(k):
        for b in range(k):
            X, Y = np.meshgrid(edges[a] + off, edges[b] + off, indexing="ij"); E[a, b] = fun(X, Y).mean() * h * h * n0
    return E

def chi2(H, E):
    m = E > 5
    return float(((H[m] - E[m]) ** 2 / E[m]).sum() / m.sum()), int(m.sum())

def measure(u, edges, small=0.5):
    H, n0 = triple_hist(u, edges)
    E3, E1, E22 = expected(R3, edges, n0), expected(lambda x, y: np.ones_like(x), edges, n0), expected(lambda x, y: R2(x) * R2(y), edges, n0)
    c3, k3 = chi2(H, E3); c1, k1 = chi2(H, E1)
    zone = (edges[:-1] + 1e-9) < small
    Z = np.outer(zone, zone)
    return dict(n_origines=n0, chi2_reduit_R3=c3, cases_R3=k3, chi2_reduit_Poisson=c1, cases_Poisson=k1,
                masse_zone_obs=float(H[Z].sum()), masse_zone_R3=float(E3[Z].sum()), masse_zone_R2R2=float(E22[Z].sum()),
                masse_zone_Poisson=float(E1[Z].sum())), H, E3

def main():
    rng = np.random.default_rng(619)
    # ---- P1 : identité
    err = 0.0
    for n in range(2, 6):
        for _ in range(250):
            N = int(rng.integers(n, 40)); th = rng.uniform(0, 2 * np.pi, n)
            err = max(err, abs(gram_margin(th, N) - kernel_det(th, N)))
    rep = dict(P1_ecart_max_identite=err)
    edges = np.linspace(0, 3, 13)
    # ---- P2, P3 : ζ
    g = np.sort(pd.read_csv(D / "zeta_zeros_1500.csv").t.values); g = g[g > 0]
    rz, Hz, Ez = measure(unfold_zeta(g), edges); rep["zeta"] = rz
    # ---- P4 : ζ·L(χ5), t ≤ 600, dépliage par la somme des fonctions de comptage
    L = np.sort(pd.read_csv(D / "L_chi5_zeros_600.csv").t.values); L = L[(L > 0) & (L <= 600)]
    gz = g[g <= 600]
    tt = np.sort(np.r_[gz, L]); u = unfold_zeta(tt) + unfold_L(tt, 5)
    rm, Hm, Em = measure(u, edges); rep["zeta_L_chi5"] = rm
    dz, dl = np.log(tt / (2 * np.pi)), np.log(5 * tt / (2 * np.pi)); f1 = float(np.mean(dz / (dz + dl)))
    Emix = expected(R3_melange(f1), edges, rm["n_origines"]); cm, km = chi2(Hm, Emix)
    Z = np.outer(edges[:-1] < 0.5, edges[:-1] < 0.5)
    rm.update(fraction_zeta=f1, chi2_reduit_melange=cm, cases_melange=km, masse_zone_melange=float(Emix[Z].sum()))
    rz6, _, _ = measure(unfold_zeta(gz), edges); rep["zeta_t_le_600"] = rz6
    rep["n_zeros"] = dict(zeta=len(g), zeta_600=len(gz), L_chi5_600=len(L))
    (D / "rencontre_a_n.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    c = (edges[:-1] + edges[1:]) / 2
    pd.DataFrame([dict(x=c[a], y=c[b], obs=Hz[a, b], attendu_R3=Ez[a, b]) for a in range(len(c)) for b in range(len(c))]).to_csv(D / "rencontre_a_n_zeta.csv", index=False)
    figure(edges, Hz, Ez, rz["n_origines"], ROOT.parent / "1_Presentation" / "43_La_rencontre_a_n.png")
    print(json.dumps(rep, indent=1, ensure_ascii=False))

def figure(edges, H, E, n0, out):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    h = edges[1] - edges[0]; c = (edges[:-1] + edges[1:]) / 2
    fig = plt.figure(figsize=(12, 5.2))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    xs = np.linspace(0, 3, 61); X, Y = np.meshgrid(xs, xs, indexing="ij")
    ax.plot_surface(X, Y, R3(X, Y), cmap="viridis", alpha=0.55, linewidth=0)
    CX, CY = np.meshgrid(c, c, indexing="ij")
    ax.scatter(CX, CY, H / (n0 * h * h), color="crimson", s=14, depthshade=False, label="zéros de ζ (t ≤ 1 500)")
    ax.set_xlabel("x (1er écart)"); ax.set_ylabel("y (2e écart)"); ax.set_zlabel("densité à 3 points")
    ax.set_title("La Rencontre à trois en 3D : noyau sinus R3 et zéros de ζ"); ax.legend(loc="upper left", fontsize=8)
    ax2 = fig.add_subplot(1, 2, 2)
    im = ax2.imshow(((H - E) / np.sqrt(np.maximum(E, 1))).T, origin="lower", extent=[0, 3, 0, 3], cmap="RdBu_r", vmin=-3, vmax=3)
    fig.colorbar(im, ax=ax2, label="(observé − R3) / √R3")
    ax2.set_xlabel("x"); ax2.set_ylabel("y"); ax2.set_title("Écarts normalisés au noyau sinus")
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)

if __name__ == "__main__":
    main()
