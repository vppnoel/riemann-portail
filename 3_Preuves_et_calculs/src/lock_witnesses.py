"""V6.3d — deux témoins pour séparer le verrou local (PRIME-LOCK) du signe global (DUAL-LOCK).

Les deux sont de la forme  F(s) = P(s) * zeta(s)  où P est un polynôme de Dirichlet
auto-réciproque (élément de degré 0 de la classe de Selberg étendue) :

  F6 : P(s) = 1 + 6^(1/2 - s)
       - équation fonctionnelle de type zeta, conducteur 6 ;
       - zéros de P : s = 1/2 + i (2k+1) pi / log 6, tous SUR la droite critique ;
       - pas de produit d'Euler : a(2) a(3) = 1 mais a(6) = 1 + sqrt(6) ;
       - Lambda_F(6^k) = (-1)^(k+1) 6^(k/2) log 6  ->  fuite hors puissances de premiers.

  E2 : P(s) = (1 - 2^(a - s)) (1 - 2^(1 - a - s)),  a = 0,8
       - équation fonctionnelle de type zeta, conducteur 4 ;
       - coefficients multiplicatifs (produit d'Euler ; seul le facteur local en 2 est modifié),
         donc Lambda_F est portée par les puissances de premiers : fuite nulle ;
       - zéros de P : s = a + 2 pi i k / log 2 et s = 1 - a + 2 pi i k / log 2, HORS de la droite ;
       - le facteur local en 2 viole la borne de type Ramanujan (|Lambda_F(2^k)| ~ 2^(a k) log 2).

Ce module est un diagnostic. Il ne prouve rien sur RH : la positivité de F6 aux hauteurs
testées repose sur les zéros connus de zeta.
"""
from __future__ import annotations

import math
import numpy as np

try:
    from rejection import log_derivative_coeffs
    from dual_lock import _arch_matrix, _pole_vector, correlation_direct, tent_fourier
except ImportError:  # usage en paquet
    from .rejection import log_derivative_coeffs
    from .dual_lock import _arch_matrix, _pole_vector, correlation_direct, tent_fourier

A_E2 = 0.8
SPECS = {
    # q : conducteur ; parity : Gamma((s + parity)/2) ; pole : pôle simple en s = 1
    "zeta": dict(q=1, parity=0, pole=True),
    "F6": dict(q=6, parity=0, pole=True),
    "E2": dict(q=4, parity=0, pole=True),
}


def coeffs_witness(kind: str, N: int, a: float = A_E2) -> np.ndarray:
    """Coefficients de Dirichlet a(0..N) (a(0) = 0, a(1) = 1)."""
    c = np.zeros(N + 1, dtype=complex)
    c[1:] = 1.0
    if kind == "zeta":
        return c
    if kind == "F6":
        c[6::6] += math.sqrt(6.0)
        return c
    if kind == "E2":
        c[2::2] -= 2.0 ** a + 2.0 ** (1.0 - a)
        c[4::4] += 2.0
        return c
    raise ValueError(kind)


def lambda_witness(kind: str, N: int, a: float = A_E2) -> np.ndarray:
    """Coefficients de -F'/F, calculés par la récurrence générique (aucune formule fermée injectée)."""
    return log_derivative_coeffs(coeffs_witness(kind, N, a))


def lambda_closed_form(kind: str, N: int, a: float = A_E2) -> np.ndarray:
    """Formule fermée de Lambda_F, pour contrôle indépendant de la récurrence."""
    lam = np.zeros(N + 1, dtype=float)
    for p in range(2, N + 1):
        if all(p % d for d in range(2, int(math.isqrt(p)) + 1)):
            pk = p
            while pk <= N:
                lam[pk] = math.log(p)
                pk *= p
    if kind == "F6":
        k, n = 1, 6
        while n <= N:
            lam[n] += (-1) ** (k + 1) * 6.0 ** (k / 2.0) * math.log(6.0)
            k, n = k + 1, n * 6
    elif kind == "E2":
        k, n = 1, 2
        while n <= N:
            lam[n] -= math.log(2.0) * (2.0 ** (a * k) + 2.0 ** ((1.0 - a) * k))
            k, n = k + 1, n * 2
    elif kind != "zeta":
        raise ValueError(kind)
    return lam


def compression_from_lambda(center: float, lam: np.ndarray, *, q: float, parity: int, pole: bool,
                            half_width: float = 2.5, dimension: int = 5, frequency_step: float = 0.6,
                            arch_dt: float = 0.02, correlation_eps: float = 2e-8):
    """Compression de la forme de Weil, côté premiers, pour des coefficients Lambda_F quelconques.

    Même construction que dual_lock.compression_accurate (mêmes briques), mais Lambda_F, le
    conducteur, la parité et le pôle sont fournis par l'appelant. Aucun zéro n'entre ici.
    """
    m, w = int(dimension), float(half_width)
    freqs = float(center) + frequency_step * (np.arange(m, dtype=float) - (m - 1) / 2.0)
    nmax = int(math.floor(math.exp(2.0 * w))) + 2
    if len(lam) <= nmax:
        raise ValueError("Lambda_F doit couvrir n <= exp(2 w) + 2")
    b = np.real(lam)
    M = _arch_matrix(freqs, w, parity, dt=arch_dt)
    F0 = np.zeros((m, m))
    for i in range(m):
        for j in range(i + 1):
            F0[i, j] = F0[j, i] = correlation_direct(0.0, w, freqs[i], freqs[j], eps=correlation_eps)
    M += math.log(q / math.pi) * F0
    if pole:
        pv = _pole_vector(freqs, w)
        M += 2.0 * np.outer(pv, pv)
    terms = [(math.log(n), float(b[n]) / math.sqrt(n)) for n in range(2, nmax + 1)
             if abs(b[n]) > 1e-14 and math.log(n) <= 2.0 * w + 1e-12]
    for i in range(m):
        for j in range(i + 1):
            loc = sum(wt * correlation_direct(lx, w, freqs[i], freqs[j], eps=correlation_eps) for lx, wt in terms)
            M[i, j] -= 2.0 * loc
            M[j, i] = M[i, j]
    return freqs, 0.5 * (M + M.T)


def polynomial_zero_gammas(kind: str, gamma_max: float, a: float = A_E2) -> dict[str, np.ndarray]:
    """gamma = -i (rho - 1/2) pour les zéros de P, |Re gamma| <= gamma_max.

    Retourne {'on': réels (zéros sur la droite), 'off': complexes (zéros hors droite)}.
    """
    if kind == "zeta":
        return {"on": np.zeros(0), "off": np.zeros(0, dtype=complex)}
    if kind == "F6":
        step = math.pi / math.log(6.0)
        K = int(gamma_max / step) + 1
        k = np.arange(-K, K + 1)
        g = (2 * k + 1) * step
        return {"on": g[np.abs(g) <= gamma_max], "off": np.zeros(0, dtype=complex)}
    if kind == "E2":
        step = 2.0 * math.pi / math.log(2.0)
        K = int(gamma_max / step)
        k = np.arange(-K, K + 1)
        d = a - 0.5
        return {"on": np.zeros(0), "off": np.concatenate([k * step - 1j * d, k * step + 1j * d])}
    raise ValueError(kind)


def zero_side(freqs: np.ndarray, w: float, gammas: np.ndarray) -> np.ndarray:
    """Z_ij = somme_rho H_i(gamma_rho) H_j(gamma_rho) (sans conjugaison)."""
    H = np.array([tent_fourier(np.asarray(gammas, dtype=complex), w, xi) for xi in freqs])
    return np.real(H @ H.T)
