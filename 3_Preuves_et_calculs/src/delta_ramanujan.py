"""V6.15 — Δ de Ramanujan : L(Δ, s), premier objet de degré 2 du corpus.

Δ(z) = q prod (1 - q^n)^24 = somme tau(n) q^n (poids 12, niveau 1). Normalisation : lambda(n) = tau(n) / n^(11/2),
L(Δ, s) = somme lambda(n) n^-s = prod_p (1 - lambda(p) p^-s + p^-2s)^-1, droite critique Re s = 1/2,
Λ(s) = (2π)^(-s) Γ(s + 11/2) L(Δ, s) = Λ(1 - s) (signe i^12 = +1).

- tau(n) exacts : prod (1 - q^n)^3 = somme (-1)^k (2k+1) q^(k(k+1)/2) (Jacobi), puissance 8 modulo plusieurs
  nombres premiers, puis restes chinois (|tau(n)| <= d(n) n^(11/2)).
- traces t_n = somme_γ g^(γ) e^{iγnh} par la formule explicite, SANS AUCUN ZÉRO : terme archimédien
  Ω(r) = 2 Re ψ(6 + i r) - 2 log 2π (c'est 2π fois la densité moyenne des zéros à la hauteur r), et termes premiers.
- contrôle indépendant : Λ(6 + it) (normalisation non unitaire, s ↦ 12 - s) par la série des fonctions gamma incomplètes,
  en précision étendue (mpmath) ; ses changements de signe sont les zéros.
"""
from __future__ import annotations
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import digamma
from prime_generator import g_hat, prime_traces

MODULI = (2097143, 2097133, 2097131, 2097097, 2097091, 2097083)   # premiers < 2^21 (vérifiés dans les tests)

def tau(M: int) -> list[int]:
    """[tau(0)=0, tau(1), ..., tau(M)] exacts (entiers Python)."""
    L = M                                   # P^8 jusqu'au degré M-1 donne tau(1..M)
    P = np.zeros(L, dtype=np.int64); k = 0
    while k * (k + 1) // 2 < L:
        P[k * (k + 1) // 2] = (-1) ** k * (2 * k + 1); k += 1
    res = []
    for m in MODULI:
        x = P % m
        for _ in range(3): x = np.convolve(x, x)[:L] % m
        res.append(x)
    Mprod = 1
    for m in MODULI: Mprod *= m
    out = [0]
    for n in range(L):
        r = 0
        for m, x in zip(MODULI, res):
            Mi = Mprod // m; r += int(x[n]) * Mi * pow(Mi, -1, m)
        r %= Mprod
        if r > Mprod // 2: r -= Mprod
        out.append(r)
    return out

def delta_coeffs(M: int) -> np.ndarray:
    """a[n] = lambda(n) = tau(n) / n^(11/2), a[0] = 0, a[1] = 1."""
    t = tau(M); n = np.arange(M + 1, dtype=float); a = np.zeros(M + 1)
    a[1:] = np.array([float(x) for x in t[1:]]) / n[1:] ** 5.5
    return a.astype(complex)

def omega_delta(r) -> np.ndarray:
    """Poids archimédien de L(Δ, s) : 2 Re ψ(6 + i r) - 2 log 2π (pair en r)."""
    return 2 * np.real(digamma(6 + 1j * np.asarray(r, dtype=float))) - 2 * math.log(2 * math.pi)

def arch_traces_general(n: np.ndarray, h: float, a: float, omega, R: float | None = None, block: float = 0.25, order: int = 16) -> np.ndarray:
    """(1/π) ∫_0^∞ g^(r) cos(r n h) Ω(r) dr, pour un poids Ω pair."""
    if R is None: R = 260.0 / a
    z, wz = leggauss(order); nb = int(math.ceil(R / block))
    starts = np.arange(nb) * block; r = (starts[:, None] + block * (z[None, :] + 1) / 2).ravel(); wr = np.tile(wz * block / 2, nb)
    base = (g_hat(r, a).real * omega(r) * wr) / math.pi
    out = np.empty(len(n))
    for i0 in range(0, len(n), 64):
        nn = np.asarray(n[i0:i0 + 64], dtype=float); out[i0:i0 + 64] = np.cos(np.outer(nn * h, r)) @ base
    return out

def traces_delta(c: np.ndarray, N: int, h: float, a: float) -> np.ndarray:
    """t_0..t_N pour L(Δ, s), sans aucun zéro ; c : coefficients de -L'/L (log_derivative_coeffs(delta_coeffs(M)))."""
    need = math.exp(N * h + 2 * a)
    if len(c) - 1 < need: raise ValueError(f"coefficients jusqu'à {need:.0f} nécessaires")
    n = np.arange(N + 1)
    return prime_traces(c, n, h, a) + arch_traces_general(n, h, a, omega_delta)

def Lambda_delta_mp(t, taus, dps: int = 40):
    """Λ(6 + it) = somme_n tau(n) [ (2πn)^-s Γ(s, 2πn) + (2πn)^-(12-s) Γ(12-s, 2πn) ], s = 6 + it (réel pour t réel)."""
    import mpmath as mp
    with mp.workdps(dps):
        s = mp.mpc(6, t); tot = mp.mpf(0)
        for n in range(1, len(taus)):
            x = 2 * mp.pi * n
            term = taus[n] * (x ** (-s) * mp.gammainc(s, x) + x ** (-(12 - s)) * mp.gammainc(12 - s, x))
            tot += term
            if n > 8 and abs(term) < abs(tot) * mp.mpf(10) ** (-dps + 5): break
        return mp.re(tot)
