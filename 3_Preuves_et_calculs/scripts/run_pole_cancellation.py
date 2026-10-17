#!/usr/bin/env python3
"""v5.6 — Vérification et extension de l'« annulation du pôle » (document reçu) :
 w_n = mu(n) + beta a(n),  beta_pc = -S_N/A_N  (S_N = sum mu(n)/n, A_N = sum a(n)/n)  =>  W_N(1) = sum w_n/n = 0.
Identités exactes (t = 1/x) : e_N = -beta C(t) pour 1 <= t <= N, 0 pour t < 1, d'où
 ||e_N||^2 = beta^2 Q(N) + T_N,   T_N = sum_{m>=N} E(m)^2 / (m(m+1)),  E(m) = 1 - sum_{n<=N} w_n floor(m/n).
 A. contrôle contre la Gram exacte (N = 100, 500, 998) ; H_N, H_N^2/(N Q(N)) ; W_N(0), W_N'(1).
 B. extension sans Gram : e_pc^2 jusqu'à N = 10^5.
 C. b_N = beta_pc log^2 N jusqu'à N = 10^7 (prédiction par résidus sous RH : b_N -> -1).
"""
from pathlib import Path
import sys, math, time
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import nyman_beurling as nb
from rh_core import KAPPA, EULER_GAMMA as g, mobius_sieve, arithmetic_c_via_lambda
out = {}
def weights(N, mu):
    n = np.arange(1, N + 1, dtype=float); m = mu[1:N + 1].astype(float); L = np.log(n)
    a = m * (L ** 2 - 2 * g * L); S = float((m / n).sum()); A = float((a / n).sum()); beta = -S / A
    return n, m, a, S, A, beta, m + beta * a
def tail_T(N, w, M_factor=400):
    M = max(N * M_factor, 2_000_000)
    d = np.zeros(M + 1)
    for k in range(1, N + 1):
        if w[k - 1] != 0: d[k::k] += w[k - 1]
    E = 1.0 - np.cumsum(d)                      # E(m) = 1 - sum_{n<=N} w_n floor(m/n)
    m = np.arange(N, M, dtype=float)
    body = float(np.sum(E[N:M] ** 2 / (m * (m + 1))))
    meanE2 = float(np.mean(E[M // 2:M] ** 2)); tail = meanE2 / M
    return body + tail, meanE2, M
CN = 120_000
c = arithmetic_c_via_lambda(CN); C = np.cumsum(c)
def Qint(N):           # Q(N) = int_1^N C(t)^2 t^-2 dt (C constante sur [k,k+1))
    k = np.arange(1, N, dtype=float); return float(np.sum(C[1:N] ** 2 * (1 / k - 1 / (k + 1))))
def Hint(N):
    k = np.arange(1, N, dtype=float); return float(np.sum(C[1:N] * np.log((k + 1) / k)))
mu = mobius_sieve(10_000_000)
# ---------------- A
M1 = np.load(ROOT / "data" / "nb_gram_sqfree1000.npy"); sf = [n for n in range(1, 1001) if mu[n] != 0]
rowsA = []
for N in (100, 500, 998):
    n, m, a, S, A, beta, w = weights(N, mu)
    ns = [x for x in sf if x <= N]; k = len(ns); Gm = M1[:k, :k]
    ww = np.array([w[x - 1] for x in ns]); b = np.array([nb.chi_rho(x) for x in ns])
    e2_gram = float(1 + 2 * ww @ b + ww @ Gm @ ww)
    T, meanE2, M = tail_T(N, w)
    Q = Qint(N); H = Hint(N)
    rowsA.append(dict(N=N, beta_pc_log2N=beta * math.log(N) ** 2, e2_gram=e2_gram, beta2Q=beta ** 2 * Q, T_N=T, e2_identite=beta ** 2 * Q + T,
                      ecart_rel=abs(beta ** 2 * Q + T - e2_gram) / e2_gram, Q=Q, H=H, H2_sur_NQ=H * H / (N * Q),
                      W0=float(w.sum()), W1prime=float(-(w * np.log(n) / n).sum()), rk=e2_gram * math.log(N) / KAPPA))
dfA = pd.DataFrame(rowsA); dfA.to_csv(ROOT / "data" / "pole_cancellation_check.csv", index=False)
print("A. contrôle :"); print(dfA.round(6).to_string(index=False))
# ---------------- B
rowsB = []
for N in (998, 2000, 5000, 10_000, 20_000, 50_000, 100_000):
    t0 = time.time(); n, m, a, S, A, beta, w = weights(N, mu); T, meanE2, M = tail_T(N, w, M_factor=200 if N > 20000 else 400)
    Q = Qint(N); L = math.log(N); e2 = beta ** 2 * Q + T
    rowsB.append(dict(N=N, b_N=beta * L ** 2, Q=Q, Q_sur_4k3L3=Q / (4 * KAPPA / 3 * L ** 3), part_beta2Q_rk=beta ** 2 * Q * L / KAPPA, part_T_rk=T * L / KAPPA,
                      e2_pc=e2, e2_pc_rk=e2 * L / KAPPA, NT_N=N * T, meanE2=meanE2, W0=float(w.sum()), secondes=round(time.time() - t0, 1)))
    print(rowsB[-1], flush=True)
dfB = pd.DataFrame(rowsB); dfB.to_csv(ROOT / "data" / "pole_cancellation_extension.csv", index=False)
# ---------------- C
Nmax = 10_000_000
nn = np.arange(1, Nmax + 1, dtype=float); mm = mu[1:Nmax + 1].astype(float); LL = np.log(nn)
cS = np.cumsum(mm / nn); cA = np.cumsum(mm * (LL ** 2 - 2 * g * LL) / nn)
rowsC = []
for e in np.arange(2.0, 7.01, 0.25):
    N = int(round(10 ** e)); S, A = cS[N - 1], cA[N - 1]
    rowsC.append(dict(N=N, S_N=S, A_N=A, b_N=-S / A * math.log(N) ** 2))
dfC = pd.DataFrame(rowsC); dfC.to_csv(ROOT / "data" / "pole_cancellation_bN.csv", index=False)
print("\nC. b_N = -S_N log^2 N / A_N :"); print(dfC.round(4).to_string(index=False))
