"""V6.20 — Le Palier 4/3, recalculé et décomposé.

Prévisions écrites avant le calcul : data/prevision_v620_palier.md (18 h 49 UTC).
Famille qui annule le pôle (V5.6) : w = μ + β a, a(n) = μ(n)(log²n − 2γ log n), β = −S_N/A_N, d'où W_N(1) = 0 et
  e_N² = β² Q(N) + T_N,  Q(N) = ∫_1^N C(t)² t^−2 dt,  T_N = Σ_{m ≥ N} E(m)²/(m(m+1)),  E(m) = 1 − Σ_{n ≤ N} w_n ⌊m/n⌋.
On écrit e_N² log N/κ = b_N² · r_Q(N) · 4/3 + τ_N, avec b_N = β log²N, r_Q = Q/((4κ/3) log³N), τ_N = T_N log N/κ.
Sous RH (Théorème B, zéros simples), b_N → −1 en moyenne, r_Q → 1 et τ_N → 0 : la limite est 4/3. La question est la vitesse.
Cribles en numpy (μ, Λ, c = Λ*Λ − Λ log + 2γΛ), indépendants des fonctions de src/ ; contrôle contre la V5.6 jusqu'à 10⁵.
"""
from __future__ import annotations
from pathlib import Path
import json, math, sys, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; D = ROOT / "data"
G = 0.5772156649015329
KAPPA = 2 + G - math.log(4 * math.pi)

def sieves(N):
    """μ et Λ jusqu'à N (crible d'Ératosthène vectorisé)."""
    isp = np.ones(N + 1, bool); isp[:2] = False
    for p in range(2, int(N ** 0.5) + 1):
        if isp[p]: isp[p * p::p] = False
    primes = np.nonzero(isp)[0]
    mu = np.ones(N + 1, np.int8); mu[0] = 0
    lam = np.zeros(N + 1)
    for p in primes:
        mu[p::p] *= -1
        if p <= N // p: mu[p * p::p * p] = 0
        q = p; lp = math.log(p)
        while q <= N:
            lam[q] = lp
            if q > N // p: break
            q *= p
    return mu, lam

def c_arith(lam, N):
    conv = np.zeros(N + 1)
    for d in np.nonzero(lam)[0]:
        k = N // d
        conv[d::d][:k] += lam[d] * lam[1:k + 1]
    n = np.arange(N + 1, dtype=float)
    c = conv - lam * np.log(np.maximum(n, 1.0)) + 2 * G * lam; c[0] = 0
    return c

def tail_T(N, w, factor):
    M = N * factor
    dd = np.zeros(M + 1)
    for k in np.nonzero(w)[0]:
        dd[k + 1::k + 1] += w[k]
    E = 1.0 - np.cumsum(dd)
    m = np.arange(N, M, dtype=float)
    body = float(np.sum(E[N:M] ** 2 / (m * (m + 1))))
    meanE2 = float(np.mean(E[M // 2:M] ** 2))
    return body + meanE2 / M, meanE2

def main():
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    t0 = time.time(); mu, lam = sieves(Nmax); c = c_arith(lam, Nmax); C = np.cumsum(c)
    k = np.arange(1, Nmax, dtype=float); Qcum = np.r_[0.0, np.cumsum(C[1:Nmax] ** 2 * (1 / k - 1 / (k + 1)))]   # Qcum[j] = Q(j+1)
    n = np.arange(1, Nmax + 1, dtype=float); m = mu[1:].astype(float); L_ = np.log(n)
    a = m * (L_ ** 2 - 2 * G * L_); cS = np.cumsum(m / n); cA = np.cumsum(a / n)
    print(f"cribles et Q jusqu'à {Nmax} : {time.time() - t0:.0f} s", flush=True)
    rows = []
    Ns = [998, 2000, 5000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000, 2_000_000, 5_000_000]
    for N in [x for x in Ns if x <= Nmax]:
        t1 = time.time(); S, A = cS[N - 1], cA[N - 1]; beta = -S / A; L = math.log(N)
        w = m[:N] + beta * a[:N]
        fac = 400 if N <= 20_000 else (60 if N <= 200_000 else (20 if N <= 500_000 else (10 if N <= 2_000_000 else 6)))
        T, meanE2 = tail_T(N, w, fac)
        Q = Qcum[N - 1]; bN = beta * L * L; rQ = Q / (4 * KAPPA / 3 * L ** 3)
        e2 = beta ** 2 * Q + T
        rows.append(dict(N=N, L=L, b_N=bN, r_Q=rQ, r_Q_modele=1 - 4.99 / L + 10.3 / L ** 2, part_beta2Q=beta ** 2 * Q * L / KAPPA,
                         tau=T * L / KAPPA, T_L2_sur_kappa=T * L * L / KAPPA, total=e2 * L / KAPPA, rapport_a_4_3=e2 * L / KAPPA / (4 / 3),
                         Q=Q, T_N=T, meanE2=meanE2, facteur_M=fac, secondes=round(time.time() - t1, 1)))
        print({k_: (round(v, 5) if isinstance(v, float) else v) for k_, v in rows[-1].items()}, flush=True)
    df = pd.DataFrame(rows); df.to_csv(D / "palier_quatre_tiers.csv", index=False)
    # contrôle de la queue : facteur double à N = 100 000
    N = 100_000; S, A = cS[N - 1], cA[N - 1]; beta = -S / A; w = m[:N] + beta * a[:N]
    T40, _ = tail_T(N, w, 120)
    ctrl = dict(N=N, T_facteur_60=float(df.loc[df.N == N, "T_N"].iloc[0]), T_facteur_120=T40)
    if Nmax >= 1_000_000:
        N = 1_000_000; S, A = cS[N - 1], cA[N - 1]; beta = -S / A; w = m[:N] + beta * a[:N]
        ctrl.update(N2=N, T_facteur_10=float(df.loc[df.N == N, "T_N"].iloc[0]), T_facteur_20=tail_T(N, w, 20)[0])
    # V5.6
    old = pd.read_csv(D / "pole_cancellation_extension.csv"); j = old.merge(df, on="N", suffixes=("_v56", ""))
    rep = dict(controle_queue=ctrl, ecart_rel_max_v56_e2=float((abs(j.e2_pc - (j.T_N + j.part_beta2Q * KAPPA / j.L)) / j.e2_pc).max()),
               ecart_rel_max_v56_Q=float((abs(j.Q_v56 - j.Q) / j.Q).max()))
    # ajustements en 1/L sur N ≥ 10⁴
    s = df[df.N >= 10_000]; x = 1 / s.L.values
    for col in ("rapport_a_4_3", "T_L2_sur_kappa"):
        X = np.c_[np.ones_like(x), x, x * x]; coef = np.linalg.lstsq(X, s[col].values, rcond=None)[0]
        rep[f"ajustement_{col}"] = dict(c0=float(coef[0]), c1=float(coef[1]), c2=float(coef[2]))
        X1 = np.c_[np.ones_like(x), x]; coef1 = np.linalg.lstsq(X1, s[col].values, rcond=None)[0]
        rep[f"ajustement_lineaire_{col}"] = dict(c0=float(coef1[0]), c1=float(coef1[1]))
    # même ajustement en lissant b_N : b_N remplacé par sa moyenne attendue −(1 + 2γ/L)
    s2 = df[df.N >= 10_000].copy(); s2["lisse"] = ((1 + 2 * G / s2.L) ** 2 * s2.r_Q + 0.75 * s2.tau) 
    X = np.c_[np.ones_like(x), x, x * x]; coef = np.linalg.lstsq(X, s2.lisse.values, rcond=None)[0]
    rep["ajustement_b_lisse"] = dict(c0=float(coef[0]), c1=float(coef[1]), c2=float(coef[2]))
    rep["kappa"] = KAPPA
    # ---- balayage dense : b_N et r_Q pour tous les N (peu coûteux), T_N pour 64 valeurs log-régulières
    NN = np.arange(10_000, Nmax + 1); LL = np.log(NN); bb = -cS[NN - 1] / cA[NN - 1] * LL ** 2; rq = Qcum[NN - 1] / (4 * KAPPA / 3 * LL ** 3)
    part = bb ** 2 * rq                                     # part β²Q rapportée à 4/3
    rep["balayage_bQ"] = dict(n=int(len(NN)), mediane_b=float(np.median(bb)), part_b2rQ_mediane=float(np.median(part)),
                              fraction_b_hors_m2_m05=float(np.mean((bb < -2) | (bb > -0.5))), max_abs_b=float(np.abs(bb).max()),
                              N_max_abs_b=int(NN[np.argmax(np.abs(bb))]))
    grid = np.unique(np.round(np.logspace(4, math.log10(Nmax), 64)).astype(int)); rowsS = []
    for N in grid:
        S, A = cS[N - 1], cA[N - 1]; beta = -S / A; L = math.log(N); w = m[:N] + beta * a[:N]
        T, meanE2 = tail_T(N, w, 20 if N <= 500_000 else (10 if N <= 2_000_000 else 6))
        Q = Qcum[N - 1]; tot = (beta ** 2 * Q + T) * L / KAPPA
        rowsS.append(dict(N=int(N), L=L, b_N=beta * L * L, r_Q=Q / (4 * KAPPA / 3 * L ** 3), tau=T * L / KAPPA, T_L2_sur_kappa=T * L * L / KAPPA,
                          total=tot, rapport_a_4_3=tot / (4 / 3), A_N=A, S_N=S))
    sc = pd.DataFrame(rowsS); sc.to_csv(D / "palier_balayage.csv", index=False)
    r = sc.rapport_a_4_3.values
    rep["balayage"] = dict(n=int(len(sc)), mediane_rapport=float(np.median(r)), q10=float(np.quantile(r, 0.1)), q90=float(np.quantile(r, 0.9)),
                           fraction_sous_4_3=float(np.mean(r < 1)), max_rapport=float(r.max()), N_max=int(sc.N[np.argmax(r)]),
                           mediane_T_L2_sur_kappa=float(np.median(sc.T_L2_sur_kappa)))
    # médianes par tranches de L et ajustement 1 + c1/L sur les médianes
    sc["tranche"] = pd.cut(sc.L, 6); med = sc.groupby("tranche", observed=True).agg(L=("L", "median"), r=("rapport_a_4_3", "median"), tl=("T_L2_sur_kappa", "median")).reset_index(drop=True)
    X = np.c_[np.ones(len(med)), 1 / med.L.values]; co = np.linalg.lstsq(X, med.r.values, rcond=None)[0]
    rep["medianes_par_tranche"] = med.to_dict("records"); rep["ajustement_medianes"] = dict(c0=float(co[0]), c1=float(co[1]))
    # développement théorique au premier ordre (b moyen, r_Q du doc. 37, T ≈ t κ/L²)
    tq = float(np.median(sc.T_L2_sur_kappa)); rep["developpement_premier_ordre"] = dict(coef_b=4 * G, coef_rQ=-4.99, coef_T=0.75 * tq, c1=4 * G - 4.99 + 0.75 * tq)
    figure(sc, D.parent.parent / "1_Presentation" / "45_Le_palier_recalcule.png", rep["developpement_premier_ordre"]["c1"])
    (D / "palier_quatre_tiers.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rep, indent=1, ensure_ascii=False))

def figure(sc, out, c1):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
    ax[0].semilogx(sc.N, sc.rapport_a_4_3, "o-", ms=3, lw=1, color="crimson", label="e²·log N / (4κ/3)")
    ax[0].semilogx(sc.N, sc.b_N ** 2 * sc.r_Q, "s", ms=3, color="#1d5d8c", label="part β²Q : b²·r_Q")
    ax[0].semilogx(sc.N, 0.75 * sc.tau, "^", ms=3, color="#2b7a57", label="part de la queue : ¾·τ")
    Ls = np.log(sc.N.values); ax[0].semilogx(sc.N, 1 + c1 / Ls, "k--", lw=1, label=f"1 − {-c1:.2f}/log N (premier ordre)".replace(".", ","))
    ax[0].axhline(1, color="grey", lw=0.8); ax[0].set_ylim(0, 2.2); ax[0].set_xlabel("N"); ax[0].set_ylabel("rapport à 4/3")
    ax[0].set_title("Le Palier : un palier par endroits, des pics là où A_N s'annule"); ax[0].legend(fontsize=8)
    ax[1].semilogx(sc.N, sc.b_N, "o", ms=3, color="#b8650f"); ax[1].semilogx(sc.N, -(1 + 2 * G / Ls), "k--", lw=1, label="−(1 + 2γ/log N)")
    ax[1].set_ylim(-3, 0); ax[1].set_xlabel("N"); ax[1].set_ylabel("b_N = β log² N"); ax[1].set_title("Le coefficient b_N = −S_N log²N / A_N"); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=130); plt.close(fig)

if __name__ == "__main__":
    main()
