"""Banc de rejet (v3.2) : le pipeline G -> c -> C -> Q appliqué à trois objets.

  zeta      : produit d'Euler + pôle en s=1  (G = q^2 + q' + 2 gamma q)
  L_chi5    : produit d'Euler, entière        (G = q^2 + q'),  chi(2)=i mod 5
  DH        : Davenport-Heilbronn, équation fonctionnelle SANS produit d'Euler
              f = (1-i k)/2 L(s,chi) + (1+i k)/2 L(s,conj chi)

Générique : Lambda_f est défini par f * Lambda_f = a log, donc -f'/f = sum Lambda_f n^-s,
et c_f = Lambda_f*Lambda_f - Lambda_f log (+ 2 gamma Lambda_f si pôle simple de résidu 1 en s=1).
Ce sont des diagnostics : ils ne prouvent rien sur RH.
"""
from __future__ import annotations
import math
import numpy as np

EULER_GAMMA = 0.5772156649015329
KAPPA_DH = (math.sqrt(10 - 2 * math.sqrt(5)) - 2) / (math.sqrt(5) - 1)


def chi5(N: int) -> np.ndarray:
    """Caractère complexe mod 5 avec chi(2)=i (impair : chi(4)=-1)."""
    tab = {0: 0, 1: 1, 2: 1j, 3: -1j, 4: -1}
    n = np.arange(N + 1)
    return np.array([tab[int(r)] for r in n % 5], dtype=complex)


def coeffs(kind: str, N: int) -> np.ndarray:
    a = np.zeros(N + 1, dtype=complex)
    if kind == "zeta":
        a[1:] = 1.0
    elif kind == "L_chi5":
        a = chi5(N)
    elif kind == "DH":
        x = chi5(N)
        a = 0.5 * (1 - 1j * KAPPA_DH) * x + 0.5 * (1 + 1j * KAPPA_DH) * np.conj(x)
    else:
        raise ValueError(kind)
    return a


def log_derivative_coeffs(a: np.ndarray) -> np.ndarray:
    """Lambda_f(n) avec -f'/f = sum Lambda_f n^-s ; a[1] doit valoir 1."""
    N = len(a) - 1
    logn = np.log(np.maximum(np.arange(N + 1), 1))
    lam = np.zeros(N + 1, dtype=complex)
    acc = np.zeros(N + 1, dtype=complex)
    for m in range(1, N + 1):
        lam[m] = a[m] * logn[m] - acc[m]
        if 2 * m <= N:
            acc[2 * m : N + 1 : m] += a[2 : N // m + 1] * lam[m]
    return lam


def c_from_lambda(lam: np.ndarray, pole: bool) -> np.ndarray:
    N = len(lam) - 1
    conv = np.zeros(N + 1, dtype=complex)
    for m in range(1, N + 1):
        k = N // m
        if lam[m] != 0:
            conv[m : m * k + 1 : m] += lam[m] * lam[1 : k + 1]
    logn = np.log(np.maximum(np.arange(N + 1), 1))
    c = conv - lam * logn
    if pole:
        c = c + 2 * EULER_GAMMA * lam
    c[0] = 0
    return c


def build(kind: str, N: int):
    a = coeffs(kind, N)
    lam = log_derivative_coeffs(a)
    c = c_from_lambda(lam, pole=(kind == "zeta"))
    return a, lam, c


def Q_curve(c: np.ndarray):
    """Q(X)=int_1^X |C|^2 x^-2 dx pour X entier (C constante entre entiers)."""
    N = len(c) - 1
    C = np.cumsum(c)
    m = np.arange(1, N, dtype=float)
    Q = np.concatenate([[0.0], np.cumsum(np.abs(C[1:N]) ** 2 * (1 / m - 1 / (m + 1)))])
    return C, Q   # Q(X) = Q[X-1]


def dh_zeros(tmax=200.0, step=2.0, sigmas=(0.6, 0.8, 1.0, 1.2, 1.4)):
    """Zéros de DH par Newton (mpmath, Hurwitz) : (sigma, t) distincts, t>0."""
    import mpmath as mp
    mp.mp.dps = 20
    k = mp.mpf(KAPPA_DH)
    c1, c2 = (1 - 1j * k) / 2, (1 + 1j * k) / 2
    ch = {1: 1, 2: 1j, 3: -1j, 4: -1}

    def L(s, conj):
        return sum((ch[a].conjugate() if conj else ch[a]) * mp.zeta(s, mp.mpf(a) / 5) for a in ch) * mp.mpf(5) ** (-s)

    f = lambda s: c1 * L(s, False) + c2 * L(s, True)
    found = []
    t0 = 10.0
    while t0 < tmax:
        for s0 in sigmas:
            try:
                z = mp.findroot(f, mp.mpc(s0, t0), tol=1e-10, maxsteps=30)
            except Exception:
                continue
            if abs(f(z)) < 1e-8 and 0 < z.imag < tmax + 20 and -0.5 < z.real < 2.0:
                zz = (float(z.real), float(z.imag))
                if all(abs(zz[0] - w[0]) + abs(zz[1] - w[1]) > 1e-5 for w in found):
                    found.append(zz)
        t0 += step
    return sorted(found, key=lambda w: w[1])


def dh_functional_equation_defect(s_list=((0.3, 7.0), (0.7, 12.0), (0.5, 20.0))):
    """|Lam(s) - Lam(1-s)| / |Lam(s)| pour Lam(s)=(5/pi)^{(s+1)/2} Gamma((s+1)/2) f(s)."""
    import mpmath as mp
    mp.mp.dps = 25
    k = mp.mpf(KAPPA_DH)
    c1, c2 = (1 - 1j * k) / 2, (1 + 1j * k) / 2
    ch = {1: 1, 2: 1j, 3: -1j, 4: -1}
    def f(s):
        Lc = sum(ch[a] * mp.zeta(s, mp.mpf(a) / 5) for a in ch) * mp.mpf(5) ** (-s)
        Lb = sum(ch[a].conjugate() * mp.zeta(s, mp.mpf(a) / 5) for a in ch) * mp.mpf(5) ** (-s)
        return c1 * Lc + c2 * Lb
    Lam = lambda s: (mp.mpf(5) / mp.pi) ** ((s + 1) / 2) * mp.gamma((s + 1) / 2) * f(s)
    out = []
    for (x, y) in s_list:
        s = mp.mpc(x, y)
        out.append(float(abs(Lam(s) - Lam(1 - s)) / abs(Lam(s))))
    return out
