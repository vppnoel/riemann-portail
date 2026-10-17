"""V6.58 — Reproduire Zhu (2026) : positivité de Weil sur la fenêtre [−L, L], phase A (non certifiée).

Auteur et titulaire des droits : Vincent NOËL.
Prévisions écrites avant le calcul : data/prevision_v658_zhu.md.

Forme de Weil (Zhu, arXiv:2608.24827 v2, conventions F(t) = ∫ f(x) e^{itx} dx) :
  Q(f) = 2 F(i/2) F(−i/2) + (1/2π) ∫ |F(t)|² [Re ψ(1/4 + it/2) − log π − Σ_{log n < 2L} 2Λ(n) n^{−1/2} cos(t log n)] dt.
Écriture en variable x, avec g = f ⋆ f̃ (g(x) = ∫ f(y) f(y − x) dy, paire, support [−2L, 2L]) et w(x) = x e^{x/2} / sinh x :
  Q(f) = 2F(i/2)F(−i/2) + g(0)·C₀(L) + ∫₀^{2L} (g(0) − g(x)) w(x)/x dx − Σ_{log n < 2L} 2Λ(n) n^{−1/2} g(log n),
  C₀(L) = −log π + E₁(4L) + ∫₀^{2L} (e^{−2x} − w(x))/x dx.
(Représentation de Gauss ψ(z) = ∫₀^∞ (e^{−u}/u − e^{−zu}/(1 − e^{−u})) du, puis échange des intégrales.)
Base : Legendre normalisée sur [−L, L], secteur pair ou impair. Les valeurs propres de la matrice de Galerkin sont des
majorants variationnels de λ*(L) dans chaque secteur. Sorties : data/zhu_reproduction.json, data/zhu_controle_zeros.json.
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys, time
import mpmath as mp
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"
mp.mp.dps = 60


# ---------------------------------------------------------------- quadrature de Gauss–Legendre en précision multiple
_GL = {}
def gauss(n):
    if n in _GL: return _GL[n]
    x0, _ = np.polynomial.legendre.leggauss(n); xs, ws = [], []
    for x in x0:
        x = mp.mpf(x)
        for _ in range(60):
            p0, p1 = mp.mpf(1), x
            for k in range(2, n + 1): p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp; x -= dx
            if abs(dx) < mp.mpf(10) ** (-mp.mp.dps + 5): break
        p0, p1 = mp.mpf(1), x
        for k in range(2, n + 1): p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1)
        xs.append(x); ws.append(2 / ((1 - x * x) * dp * dp))
    _GL[n] = (xs, ws); return xs, ws


def nodes(a, b, n):
    xs, ws = gauss(n); h = (b - a) / 2; c = (a + b) / 2
    return [c + h * x for x in xs], [h * w for w in ws]


def legendre_vals(u, nmax):
    """P̄_0..P̄_nmax (normalisées sur [−1,1]) en u ; nul hors de [−1, 1]."""
    if u < -1 or u > 1: return [mp.mpf(0)] * (nmax + 1)
    P = [mp.mpf(1), u]
    for k in range(2, nmax + 1): P.append(((2 * k - 1) * u * P[-1] - (k - 1) * P[-2]) / k)
    return [mp.sqrt(mp.mpf(2 * k + 1) / 2) * P[k] for k in range(nmax + 1)]


def basis_vals(x, L, degs):
    v = legendre_vals(x / L, max(degs)); s = 1 / mp.sqrt(L)
    return [v[d] * s for d in degs]


def vonmangoldt(n):
    for p in range(2, n + 1):
        if n % p == 0:
            m = n
            while m % p == 0: m //= p
            return math.log(p) if m == 1 else 0.0
    return 0.0


def w(x):
    return x * mp.exp(x / 2) / mp.sinh(x) if x != 0 else mp.mpf(1)


def C0(L):
    I = mp.quad(lambda x: (mp.exp(-2 * x) - w(x)) / x, [0, 2 * L])
    return -mp.log(mp.pi) + mp.e1(4 * L) + I


def gram_corr(L, degs, x, J):
    """G_mn(x) = ∫ T_m(y) T_n(y − x) dy, y ∈ [−L + x, L], pour x ≥ 0 (exact si J > max degré)."""
    ys, wy = nodes(-L + x, L, J); n = len(degs)
    A = [basis_vals(y, L, degs) for y in ys]; B = [basis_vals(y - x, L, degs) for y in ys]
    G = [[mp.mpf(0)] * n for _ in range(n)]
    for k in range(len(ys)):
        wk = wy[k]; a = A[k]; b = B[k]
        for i in range(n):
            ai = a[i] * wk
            if ai == 0: continue
            row = G[i]
            for j in range(n): row[j] += ai * b[j]
    return [[(G[i][j] + G[j][i]) / 2 for j in range(n)] for i in range(n)]


def weil_matrix(L, parity, N, K=48):
    L = mp.mpf(L); degs = [parity + 2 * k for k in range(N)]; n = N; J = max(degs) + 4
    # pôle
    xs, wx = nodes(-L, L, J + 8)
    BV = [basis_vals(x, L, degs) for x in xs]
    a = [mp.fsum(wx[k] * BV[k][i] * mp.exp(-xs[k] / 2) for k in range(len(xs))) for i in range(n)]
    b = [mp.fsum(wx[k] * BV[k][i] * mp.exp(xs[k] / 2) for k in range(len(xs))) for i in range(n)]
    M = [[a[i] * b[j] + a[j] * b[i] for j in range(n)] for i in range(n)]
    c0 = C0(L)
    for i in range(n): M[i][i] += c0
    # archimédien : ∫₀^{2L} (δ − G(x)) w(x)/x dx
    xk, wk = nodes(mp.mpf(0), 2 * L, K)
    for k in range(K):
        G = gram_corr(L, degs, xk[k], J); f = wk[k] * w(xk[k]) / xk[k]
        for i in range(n):
            for j in range(n): M[i][j] += f * ((1 if i == j else 0) - G[i][j])
    # premiers
    for m in range(2, int(math.exp(2 * float(L))) + 1):
        lam = vonmangoldt(m)
        if lam == 0 or math.log(m) >= 2 * float(L): continue
        G = gram_corr(L, degs, mp.log(m), J); coef = 2 * mp.mpf(lam) / mp.sqrt(m)
        for i in range(n):
            for j in range(n): M[i][j] -= coef * G[i][j]
    return M


def lam_min(M, N):
    E = mp.eigsy(mp.matrix([row[:N] for row in M[:N]]))[0]
    return min(E[i] for i in range(N))


def controle_zeros(L=0.8):
    """Z1 : Q(f) en variable x contre Σ_{γ ≤ 1500} 2|F(γ)|², f = cos⁴(πx/2L) (paire, lisse)."""
    mp.mp.dps = 30; L = mp.mpf(L)
    f = lambda x: mp.cos(mp.pi * x / (2 * L)) ** 4 if abs(x) <= L else mp.mpf(0)
    def g(x):
        ys, wy = nodes(-L + x, L, 60); return mp.fsum(wy[k] * f(ys[k]) * f(ys[k] - x) for k in range(len(ys)))
    xs, wx = nodes(-L, L, 60)
    Fa = mp.fsum(wx[k] * f(xs[k]) * mp.cosh(xs[k] / 2) for k in range(60))
    g0 = g(mp.mpf(0)); xk, wk = nodes(mp.mpf(0), 2 * L, 60)
    Q = 2 * Fa ** 2 + g0 * C0(L) + mp.fsum(wk[k] * (g0 - g(xk[k])) * w(xk[k]) / xk[k] for k in range(60))
    for m in (2, 3, 4):
        if math.log(m) < 2 * float(L): Q -= 2 * mp.mpf(vonmangoldt(m)) / mp.sqrt(m) * g(mp.log(m))
    gam = pd.read_csv(D / "zeta_zeros_1500.csv").t.values; gam = gam[gam > 0]
    def Fhat(t):                                   # transformée exacte de cos⁴(πx/2L) : cos⁴ = 3/8 + cos(2θ)/2 + cos(4θ)/8
        t = mp.mpf(float(t)); tot = mp.mpf(0)
        for k, wk_ in enumerate((mp.mpf(3) / 8, mp.mpf(1) / 2, mp.mpf(1) / 8)):
            for sgn in ((1,) if k == 0 else (1, -1)):
                r = t + sgn * k * mp.pi / L
                tot += wk_ * (2 * L if r == 0 else 2 * mp.sin(r * L) / r) * (1 if k == 0 else mp.mpf(1) / 2)
        return tot
    Z = mp.fsum(2 * Fhat(t) ** 2 for t in gam)
    mp.mp.dps = 60
    return dict(L=float(L), Q_formule_x=float(Q), somme_zeros=float(Z), ecart_relatif=float(abs(Q - Z) / abs(Z)), zeros=int(len(gam)))


def main():
    t0 = time.time(); out = {}
    ctrl = controle_zeros(); print("Z1", ctrl, flush=True)
    (D / "zhu_controle_zeros.json").write_text(json.dumps(ctrl, indent=1, ensure_ascii=False), encoding="utf-8")
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    for L in (0.5, 0.6, 0.7, 0.8):
        for parity in ((0, 1) if L == 0.8 else (0,)):
            M = weil_matrix(L, parity, Nmax)
            vals = {str(N): mp.nstr(lam_min(M, N), 8) for N in (8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64) if N <= Nmax}
            out[f"L={L} {'pair' if parity == 0 else 'impair'}"] = vals
            print(L, parity, vals, f"{time.time() - t0:.0f} s", flush=True)
            (D / "zhu_reproduction.json").write_text(json.dumps(dict(valeurs=out, controle=ctrl, Nmax=Nmax, dps=60), indent=1, ensure_ascii=False), encoding="utf-8")



def noyau_des_moments(L, N, K=48, parity=0):
    """Plus petite valeur de Q sur {F(i/2) = F(−i/2) = 0}, secteur de parité donnée, N modes (cadre des docs 71–75).
    Pour f paire, les deux moments exponentiels sont égaux ; pour f impaire, opposés. Dans les deux cas une seule
    contrainte a·c = 0, et le terme du pôle (a·bᵀ + b·aᵀ, b = ±a) s'annule sur ce sous-espace.
    Base orthonormée exacte de a⊥ : colonnes 2 à N du réflecteur de Householder qui envoie a/|a| sur ±e₁.
    (Une orthogonalisation de Gram–Schmidt des P·eᵢ est instable ici : les composantes de a décroissent
    sur-exponentiellement et la famille est presque liée au-delà de la précision de travail.)"""
    M = weil_matrix(L, parity, N, K)
    L_ = mp.mpf(L); degs = [parity + 2 * k for k in range(N)]; xs, wx = nodes(-L_, L_, max(degs) + 12)
    BV = [basis_vals(x, L_, degs) for x in xs]
    a = [mp.fsum(wx[k] * BV[k][i] * mp.exp(-xs[k] / 2) for k in range(len(xs))) for i in range(N)]
    na = mp.sqrt(mp.fsum(x * x for x in a)); u = [x / na for x in a]
    sgn = 1 if u[0] >= 0 else -1
    wv = list(u); wv[0] += sgn                              # H = I − 2wwᵀ/wᵀw envoie u sur −sgn·e₁
    ww = mp.fsum(x * x for x in wv)
    H = mp.matrix(N, N)
    for i in range(N):
        for j in range(N): H[i, j] = (1 if i == j else 0) - 2 * wv[i] * wv[j] / ww
    B = H[:, 1:N]                                            # N × (N−1), colonnes orthonormées, orthogonales à a
    R = B.T * mp.matrix(M) * B
    E = mp.eigsy(R)[0]
    return min(E[i] for i in range(N - 1))


def noyau_main():
    """Recalcule toute la table du noyau des moments (doc. 81, §4) avec la fonction ci-dessus ; remplace le fichier."""
    out = {}
    for L, N in ((0.347, 24), (0.347, 32), (0.5, 24), (0.5, 32), (0.55, 24), (0.55, 32), (0.6, 24), (0.6, 32),
                 (0.7, 24), (0.7, 32), (0.8, 24), (0.8, 32), (0.8, 40)):
        v = noyau_des_moments(L, N); out[f"{L}|{N}"] = mp.nstr(v, 8); print(L, N, out[f"{L}|{N}"], flush=True)
    for L, N in ((0.347, 24), (0.5, 24), (0.5, 32), (0.55, 24), (0.55, 32), (0.8, 24)):
        v = noyau_des_moments(L, N, parity=1); out[f"{L}|{N}|impair"] = mp.nstr(v, 8); print(L, N, "impair", out[f"{L}|{N}|impair"], flush=True)
    (D / "zhu_noyau_des_moments.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")


FIG_TXT = {
    "fr": ["ce corpus (40 modes, 60 chiffres)", "Zhu, planchers (200 modes)", "Zhu, majorants certifiés", "Zhu, minorant certifié (0,8)",
           "demi-largeur L de la fenêtre (support de f dans [−L, L])", "λ*(L), plus petite valeur de Q(f)/‖f‖²",
           "La marge de positivité de Weil s'effondre avec la fenêtre", "secteur pair", "secteur impair",
           "encadrement certifié de Zhu (pair)", "plancher de Zhu (200 modes)", "nombre de modes de Legendre",
           "plus petite valeur propre (majorant de λ*)", "L = 0,8 : convergence vers l'encadrement de Zhu"],
    "en": ["this corpus (40 modes, 60 digits)", "Zhu, floors (200 modes)", "Zhu, certified upper bounds", "Zhu, certified lower bound (0.8)",
           "half-width L of the window (supp f in [−L, L])", "λ*(L), smallest value of Q(f)/‖f‖²",
           "The Weil positivity margin collapses with the window", "even sector", "odd sector",
           "Zhu's certified bracket (even)", "Zhu's floor (200 modes)", "number of Legendre modes",
           "smallest eigenvalue (upper bound for λ*)", "L = 0.8: convergence to Zhu's bracket"]}

def figure(out, lang="fr"):
    T = FIG_TXT[lang]
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    d = json.loads((D / "zhu_reproduction.json").read_text(encoding="utf-8"))
    Ls = [0.5, 0.6, 0.7, 0.8]; ours = [float(d["valeurs"][f"L={L} pair"]["40"]) for L in Ls]
    zf = [d["zhu_planchers_tableau1"][str(L)] for L in Ls]; zc = [d["zhu_majorants_certifies_tableau3"][str(L)] for L in Ls]
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.3))
    ax[0].semilogy(Ls, ours, "o-", color="#1d5d8c", label=T[0])
    ax[0].semilogy(Ls, zf, "s", mfc="none", color="#c0392b", ms=9, label=T[1])
    ax[0].semilogy(Ls, zc, "_", color="#555", ms=14, mew=2, label=T[2])
    ax[0].semilogy([0.8], [d["zhu_minorant_certifie_0.8"]], "^", color="#2b7a57", ms=9, label=T[3])
    ax[0].set_xlabel(T[4]); ax[0].set_ylabel(T[5])
    ax[0].set_title(T[6], fontsize=10); ax[0].legend(fontsize=8)
    N = [8, 12, 16, 20, 24, 28, 32, 36, 40]; v = [float(d["valeurs"]["L=0.8 pair"][str(n)]) for n in N]
    N64 = [48, 56, 64]; v64 = [float(d["valeurs_L08_pair_N64"][str(n)]) for n in N64]
    ax[1].semilogy(N + N64, v + v64, "o-", color="#1d5d8c", label=T[7])
    vo = [float(d["valeurs"]["L=0.8 impair"][str(n)]) for n in N]; ax[1].semilogy(N, vo, "s-", color="#7a4fb0", label=T[8])
    ax[1].axhspan(d["zhu_minorant_certifie_0.8"], 2.27e-17, color="#2b7a57", alpha=0.15, label=T[9])
    ax[1].axhline(1.65e-17, color="#c0392b", ls="--", lw=1, label=T[10])
    ax[1].set_xlabel(T[11]); ax[1].set_ylabel(T[12])
    ax[1].set_title(T[13], fontsize=10); ax[1].legend(fontsize=8)
    fig.text(0.99, 0.01, "Programme Riemann V6.58 — © Vincent NOËL", ha="right", fontsize=7, color="#777")
    fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(out, dpi=140); plt.close(fig)


if __name__ == "__main__":
    if "--figure-en" in sys.argv: figure(ROOT.parent / "1_Presentation" / "english" / "81_zhu_reproduced_EN.png", "en")
    elif "--figure" in sys.argv: figure(ROOT.parent / "1_Presentation" / "81_Zhu_reproduit.png")
    elif "--noyau" in sys.argv: noyau_main()
    else: main()
