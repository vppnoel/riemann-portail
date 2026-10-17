#!/usr/bin/env python3
"""P2.2 : analogue "corps de fonctions" du pipeline G->c->C->Q, et ce que Q voit (ou non) de la positivité de Weil.

L-polynôme d'une courbe elliptique sur F_p : P(T)=1 - a T + p T^2, racines inverses alpha_{1,2}, s_n = alpha_1^n+alpha_2^n.
Analogue de q=-L'/L : q_n = -s_n (u=p^{-s}, log p = 1 ; q = u P'/P = -sum s_n u^n, résidu -1 aux zéros comme pour -zeta'/zeta) ;
c_n=(q*q)_n - n q_n = (s*s)_n + n s_n (pas de pôle : L est entière).
C_N = sum_{n<=N} c_n ; Q_M = (1-1/p) sum_{N<M} C_N^2 p^{-N}   (analogue de int |C|^2 x^-2 dx).
(1) Q ne dépend que du spectre de Frobenius : croissance cubique si |alpha|=sqrt p, exponentielle sinon.
(2) La borne |a| <= 2 sqrt p n'est PAS produite par Q : elle vient de la géométrie (Hasse-Weil). On énumère toutes
    les courbes y^2=x^3+Ax+B sur F_p pour le vérifier.
"""
from pathlib import Path
import sys, math
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]

def Q_curve(a, p, M):
    s = [2, a]                                   # s_0, s_1
    for n in range(2, M + 2): s.append(a * s[-1] - p * s[-2])
    q = {n: -s[n] for n in range(1, M + 1)}
    c = {}
    for n in range(1, M + 1):
        conv = sum(q[i] * q[n - i] for i in range(1, n))
        c[n] = conv - n * q[n]
    C, acc, out = {}, 0, []
    for n in range(1, M + 1):
        acc += c[n]; C[n] = acc
    Q = 0.0
    for N in range(1, M + 1):
        Q += float(C[N] ** 2) / float(p ** N) * (1 - 1 / p) if N < 700 else float("inf")
        out.append((N, Q))
    return out

p = 101
rows = []
for label, a in [("a=10 (|a|<=2sqrt p, RH vraie)", 10), ("a=20 (bord)", 20), ("a=25 (viole Hasse, FAUX)", 25)]:
    disc = a * a - 4 * p
    rad = (abs(a) + math.sqrt(disc)) / 2 if disc > 0 else math.sqrt(p)
    res = dict(Q_curve(a, p, 60))
    for M in (10, 20, 40, 60):
        rows.append(dict(cas=label, rayon_alpha_max=round(rad, 3), sqrt_p=round(math.sqrt(p), 3), M=M, Q_M=res[M], Q_M_sur_M3=res[M] / M ** 3))
df = pd.DataFrame(rows); df.to_csv(ROOT / "data" / "function_field_analog.csv", index=False)
print(df.round(4).to_string(index=False))

# (2) énumération exhaustive des courbes y^2 = x^3 + A x + B sur F_p
x = np.arange(p); sq = np.zeros(p, dtype=int)
for y in range(p): sq[(y * y) % p] += 1
amax = 0; count = 0
for A in range(p):
    for B in range(p):
        if (4 * A ** 3 + 27 * B ** 2) % p == 0: continue
        rhs = (x ** 3 + A * x + B) % p
        N1 = 1 + int(np.sum(sq[rhs]))            # points affines + infini
        a = p + 1 - N1
        amax = max(amax, abs(a)); count += 1
print(f"p={p} : {count} courbes lisses y^2=x^3+Ax+B ; max|a| = {amax} ; 2 sqrt p = {2*math.sqrt(p):.3f} ; a=25 jamais atteint")
