"""V6.15, coup 1 — Le temps de Heisenberg en degré 2, avec Δ de Ramanujan.

Prévision écrite avant tout calcul (data/prevision_v615.md) : la longueur de détection d'un quadruplet hors droite
est le poids archimédien à sa hauteur, Ω(γ0) = 2π × densité des zéros. Pour L(Δ, s) (degré 2) :
Ω(γ0) = 2 Re ψ(6 + iγ0) - 2 log 2π ≈ 2 log(γ0 / 2π), le double de ζ.

1. tau(n) exacts jusqu'à 25 000 ; contrôles (Hecke, multiplicativité, Deligne).
2. Zéros de L(Δ, s) pour t <= 40 par la série des gamma incomplètes (mpmath), indépendamment des premiers.
3. Formule explicite : traces des premiers contre traces des zéros (fonction test large).
4. L'opérateur reconstruit des seules traces des premiers : zéros, masses 1, comptage contre la loi de Weyl.
5. Quadruplets synthétiques sur le fond de L(Δ, s) et sur celui de ζ, aux mêmes hauteurs ; contrôle supplémentaire
   (non pré-enregistré) : le produit ζ · L(s, χ5), degré 2 non primitif, dont le poids est la somme des poids.
"""
from __future__ import annotations
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); D = ROOT / "data"
from delta_ramanujan import tau, delta_coeffs, traces_delta, omega_delta, Lambda_delta_mp
from prime_generator import traces_from_primes, g_hat, metric_and_generator, first_negative_size, lmin_ratio, heisenberg_length
from rejection import coeffs, log_derivative_coeffs
from zero_reconstruction import nontrivial_zeros
from scipy.special import digamma

TAU = 1e-10
def omega_deg1(r, q, par): return math.log(q / math.pi) + float(np.real(digamma((0.5 + par) / 2 + 0.5j * r)))

def traces(gam, w, N, h):
    k = np.arange(N + 1); return (np.asarray(w)[None, :] * np.exp(1j * np.outer(k * h, np.asarray(gam, dtype=complex)))).sum(1)

def quad(g0, d): return np.array([g0 - 1j * d, g0 + 1j * d, -g0 - 1j * d, -g0 + 1j * d])

def main():
    t0 = time.time()
    # ---- 1. tau(n)
    T = tau(25000); from sympy import primerange
    chk = dict(tau_1_a_11=str(T[1:12]), hecke_p2=all(T[p * p] == T[p] ** 2 - p ** 11 for p in primerange(2, 158)),
               multiplicatif=all(T[m * n] == T[m] * T[n] for m in range(2, 120) for n in range(2, 120) if math.gcd(m, n) == 1),
               deligne_max=max(abs(T[p]) / p ** 5.5 for p in primerange(2, 25000)))
    print("tau :", chk, flush=True)
    # ---- 2. zéros de L(Δ, s), t <= 40, sans les premiers
    ts = np.arange(1.0, 40.01, 0.1); v = [Lambda_delta_mp(t, T[:80], 40) for t in ts]; zm = []
    for i in range(len(ts) - 1):
        if v[i] * v[i + 1] < 0:
            lo, hi, flo = ts[i], ts[i + 1], v[i]
            for _ in range(32):
                m = (lo + hi) / 2; fm = Lambda_delta_mp(m, T[:80], 40)
                if (fm < 0) == (flo < 0): lo, flo = m, fm
                else: hi = m
            zm.append((lo + hi) / 2)
    zm = np.array(zm); print(f"zéros (gamma incomplètes, t <= 40) : {len(zm)} ; premier {zm[0]:.7f}", flush=True)
    # ---- 3. formule explicite : premiers contre zéros
    c = log_derivative_coeffs(delta_coeffs(25000)); ex = []
    for a, h, N in ((0.5, 0.05, 40), (0.3, 0.05, 40)):
        tp = traces_delta(c, N, h, a); zz = np.concatenate([zm, -zm]); tz = traces(zz, g_hat(zz, a), N, h)
        ex.append(dict(a=a, h=h, N=N, ecart_relatif=float(np.max(np.abs(tp - tz)) / abs(tz[0])), poids_au_dela_de_40=float(g_hat(40.0, a).real / g_hat(0.0, a).real)))
    pd.DataFrame(ex).to_csv(D / "delta_formule_explicite.csv", index=False); print("formule explicite :", ex, flush=True)
    # ---- 4. l'opérateur des premiers
    a, h, N = 0.04, 0.01, 1000; tD = traces_delta(c, N, h, a)
    r = metric_and_generator(tD, N, h); mass = r["weight"] / g_hat(r["gamma"], a); ok = np.abs(mass - 1) < 1e-3
    gp = np.sort(r["gamma"][ok].real[r["gamma"][ok].real > 0])
    pd.DataFrame(dict(gamma=gp)).to_csv(D / "delta_zeros_premiers.csv", index=False)
    pd.DataFrame(dict(gamma=zm, ecart_au_generateur=gp[:len(zm)] - zm)).to_csv(D / "delta_zeros_mpmath.csv", index=False)
    weyl = []
    for TT in (50, 100, 150, 200):
        rr = np.linspace(0, TT, 20001); weyl.append(dict(T=TT, comptes=int((gp <= TT).sum()), weyl=float(np.trapezoid(omega_delta(rr), rr) / (2 * math.pi))))
    pd.DataFrame(weyl).to_csv(D / "delta_weyl.csv", index=False)
    print(f"générateur : {ok.sum()} valeurs propres de masse 1 ; max |Im| {np.max(np.abs(r['gamma'][ok].imag)):.1e} ; écart aux zéros mpmath {np.max(np.abs(gp[:len(zm)] - zm)):.1e} ;"
          f" Weyl {[(w['T'], w['comptes'], round(w['weyl'], 1)) for w in weyl]} ; positivité : {first_negative_size(tD, TAU, N + 1)}", flush=True)
    # ---- 5. le temps de Heisenberg en degré 2
    Nq = 850; tD = tD[:Nq + 1]
    tZ = traces_from_primes("zeta", log_derivative_coeffs(coeffs("zeta", 20000)), Nq, h, a)
    tL = traces_from_primes("L_chi5", log_derivative_coeffs(coeffs("L_chi5", 20000)), Nq, h, a)
    zz = -1j * (nontrivial_zeros("zeta") - 0.5); posZ = np.sort(zz.real[zz.real > 0])
    zl = -1j * (nontrivial_zeros("L_chi5") - 0.5); posZL = np.sort(np.concatenate([posZ, zl.real[zl.real > 0]]))
    mid = lambda pos, x: float(0.5 * (pos[np.searchsorted(pos, x) - 1] + pos[np.searchsorted(pos, x)]))
    rows = []
    for H in (30, 50, 100, 150, 200):
        for obj, bg, pos, om in (("L(Δ, s)", tD, gp, lambda g: float(omega_delta(g))),
                                 ("ζ", tZ, posZ, lambda g: omega_deg1(g, 1, 0)),
                                 ("ζ · L(s, χ5)", tZ + tL, posZL, lambda g: omega_deg1(g, 1, 0) + omega_deg1(g, 5, 1))):
            g0 = mid(pos, H); q = quad(g0, 0.2); n = first_negative_size(bg + traces(q, g_hat(q, a), Nq, h), TAU, Nq + 1)
            Lc = None if n is None else (n - 1) * h
            rows.append(dict(objet=obj, hauteur_visee=H, hauteur=g0, L_c=Lc, Omega=om(g0), rapport=None if Lc is None else Lc / om(g0),
                             pre_enregistre=obj != "ζ · L(s, χ5)"))
            print(rows[-1], flush=True)
    for d in (0.05, 0.4):
        g0 = mid(gp, 100); q = quad(g0, d); n = first_negative_size(tD + traces(q, g_hat(q, a), Nq, h), TAU, Nq + 1)
        rows.append(dict(objet="L(Δ, s)", hauteur_visee=100, hauteur=g0, delta=d, L_c=(n - 1) * h, Omega=float(omega_delta(g0)), rapport=(n - 1) * h / float(omega_delta(g0)), pre_enregistre=False))
    hd = pd.DataFrame(rows); hd.to_csv(D / "delta_heisenberg.csv", index=False)
    print(f"total {time.time() - t0:.0f} s")

def figure():
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#52514e",
                         "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.titlesize": 9.5})
    BLUE, ORANGE, VIOLET, GREY = "#2a78d6", "#eb6834", "#4a3aa8", "#52514e"
    hd = pd.read_csv(D / "delta_heisenberg.csv"); hd = hd[hd.delta.isna()] if "delta" in hd else hd
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.0), gridspec_kw=dict(width_ratios=[1.1, 1]))
    A = ax[0]
    for obj, col, mk in (("ζ", BLUE, "o"), ("ζ · L(s, χ5)", ORANGE, "s"), ("L(Δ, s)", VIOLET, "D")):
        x = hd[hd.objet == obj].sort_values("hauteur"); A.plot(x.hauteur, x.L_c, mk + "-", color=col, lw=1.5, ms=5, label=f"{obj} : mesuré" + (" (contrôle non pré-enregistré)" if obj.startswith("ζ ·") else ""))
        rr = np.linspace(25, 205, 200)
        om = omega_delta(rr) if obj == "L(Δ, s)" else (np.array([omega_deg1(g, 1, 0) for g in rr]) + (np.array([omega_deg1(g, 5, 1) for g in rr]) if obj != "ζ" else 0))
        A.plot(rr, om, color=col, lw=0.9, ls=(0, (3, 2)))
    A.set_xlabel("hauteur γ₀ du quadruplet synthétique (δ = 0,2)"); A.set_ylabel("longueur de détection L_c")
    A.text(150, 2.4, "pointillés : poids archimédien Ω(γ₀)\n= 2π × densité des zéros (prévu)", fontsize=7.5, color=GREY)
    A.set_title("Degré 2 : la longueur de détection double", loc="left"); A.legend(frameon=False, fontsize=7.5, loc="upper left")
    B = ax[1]; z = pd.read_csv(D / "delta_zeros_premiers.csv"); w = pd.read_csv(D / "delta_weyl.csv")
    B.step(z.gamma, np.arange(1, len(z) + 1), where="post", color=VIOLET, lw=1.4, label="zéros de L(Δ, s) reconstruits par les premiers (τ(n))")
    rr = np.linspace(0, 232, 400); B.plot(rr, [np.trapezoid(omega_delta(np.linspace(0, x, 2000)), np.linspace(0, x, 2000)) / (2 * math.pi) for x in rr], color=GREY, lw=0.9, ls=(0, (3, 2)), label="loi de Weyl (intégrale de Ω / 2π)")
    zm = pd.read_csv(D / "delta_zeros_mpmath.csv"); B.scatter(zm.gamma, np.arange(1, len(zm) + 1), s=14, color=ORANGE, zorder=3, label=f"contrôle mpmath, t ≤ 40 (écart {np.max(np.abs(zm.ecart_au_generateur)):.0e})")
    B.set_xlabel("t"); B.set_ylabel("nombre de zéros ≤ t"); B.legend(frameon=False, fontsize=7.5, loc="upper left")
    B.set_title("L(Δ, s) depuis les seuls nombres premiers", loc="left")
    fig.tight_layout(w_pad=2.5); fig.savefig(D / "delta_heisenberg.png", dpi=150, bbox_inches="tight"); print("figure écrite")

if __name__ == "__main__":
    if "--figure" not in sys.argv: main()
    figure()
