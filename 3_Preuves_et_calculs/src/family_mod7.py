"""V6.5 — Une famille où les zéros bougent vraiment, à équation fonctionnelle constante (conducteur 7).

Caractères de Dirichlet modulo 7 (générateur 3), impairs :
  chi_3 : réel (symbole de Legendre), L(s, chi_3) a un produit d'Euler ;
  chi_1, conj(chi_1) : complexes d'ordre 6.
Sosie de type Davenport–Heilbronn :  f_7 = (L(s, chi_1) + eps L(s, conj chi_1)) / (1 + eps),
  eps = tau(chi_1) / (i sqrt 7)  (nombre racine, |eps| = 1). Coefficients réels, pas de produit d'Euler.
Les deux vérifient la même équation fonctionnelle :
  Lambda(s) = (7/pi)^((s+1)/2) Gamma((s+1)/2) F(s) = Lambda(1 - s).
Famille :  F_theta = (1 - theta) L(s, chi_3) + theta f_7.   Même équation fonctionnelle pour tout theta.

Fonction de Hardy :  Z_theta(t) = Re[e^{i vartheta(t)} F_theta(1/2 + it)] = (1 - theta) Z_0(t) + theta Z_1(t), réelle,
dont les changements de signe sont les zéros de F_theta sur la droite critique. Linéaire en theta : les zéros
sur la droite à hauteur t sont donnés par  theta = theta*(t) = Z_0(t) / (Z_0(t) - Z_1(t)).
"""
from __future__ import annotations
import cmath, math
import numpy as np
from scipy.special import loggamma
try:
    from zero_reconstruction import hurwitz_zeta
except ImportError:
    from .zero_reconstruction import hurwitz_zeta

Q = 7
_OMEGA = cmath.exp(1j * math.pi / 3)
_LOG3 = {1: 0, 3: 1, 2: 2, 6: 3, 4: 4, 5: 5}           # 3^j mod 7
CHI1 = {a: _OMEGA ** j for a, j in _LOG3.items()}        # ordre 6, impair
CHI3 = {a: complex((-1) ** j) for a, j in _LOG3.items()} # réel, impair (symbole de Legendre)
EPS = sum(CHI1[a] * cmath.exp(2j * math.pi * a / 7) for a in CHI1) / (1j * math.sqrt(7))
C1, C2 = 1 / (1 + EPS), EPS / (1 + EPS)                  # f_7 = C1 L(chi_1) + C2 L(conj chi_1)

def coefficients(theta: float, N: int) -> np.ndarray:
    """Coefficients de Dirichlet a(0..N) de F_theta (réels, a(1) = 1)."""
    a = np.zeros(N + 1)
    for n in range(1, N + 1):
        r = n % 7
        if r:
            f7 = (C1 * CHI1[r] + C2 * np.conj(CHI1[r])).real
            a[n] = (1 - theta) * CHI3[r].real + theta * f7
    return a

def L_chi(s: complex, table: dict, conj: bool = False) -> complex:
    s = complex(s)
    return 7.0 ** (-s) * sum((np.conj(table[a]) if conj else table[a]) * hurwitz_zeta(s, a / 7.0) for a in table)

def F0(s: complex) -> complex: return L_chi(s, CHI3)
def F1(s: complex) -> complex: return C1 * L_chi(s, CHI1) + C2 * L_chi(s, CHI1, conj=True)
def F_theta(s: complex, theta: float) -> complex: return (1 - theta) * F0(s) + theta * F1(s)

def completed(F, s: complex) -> complex:
    """Lambda(s) = (7/pi)^((s+1)/2) Gamma((s+1)/2) F(s)."""
    s = complex(s)
    return cmath.exp(((s + 1) / 2) * math.log(7 / math.pi) + loggamma((s + 1) / 2)) * F(s)

def vartheta(t: float) -> float:
    """Phase de (7/pi)^((s+1)/2) Gamma((s+1)/2) en s = 1/2 + it."""
    return 0.5 * t * math.log(7 / math.pi) + float(loggamma(0.75 + 0.5j * t).imag)

def hardy(t: float) -> tuple[float, float]:
    """(Z_0(t), Z_1(t)) : fonctions de Hardy de L(s, chi_3) et de f_7."""
    ph = cmath.exp(1j * vartheta(t)); s = 0.5 + 1j * t
    return float((ph * F0(s)).real), float((ph * F1(s)).real)
