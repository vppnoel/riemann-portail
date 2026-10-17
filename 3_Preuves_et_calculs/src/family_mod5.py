"""V6.7 — Trajets d'objets entre L(s, chi_5) et Davenport–Heilbronn, à symétrie de Hardy conservée (conducteur 5).

chi : caractère impair d'ordre 4 modulo 5 (chi(2) = i). L(s, chi) n'est pas autoduale ; sa fonction de Hardy
e^{i vartheta(t)} L(1/2 + it, chi) a une phase constante phi (racine carrée du nombre racine).
A(s) = e^{-i phi} L(s, chi) : fonction de Hardy réelle, produit d'Euler, zéros = ceux de L(s, chi).
DH : fonction de Hardy réelle, pas de produit d'Euler, quatre paires de zéros hors droite pour t <= 200.
Deux trajets d'objets (le signe de la racine carrée n'est pas fixé) :
  F_theta^(+) = (1 - theta) A + theta DH,   F_theta^(-) = (1 - theta) (-A) + theta DH.
Sur la droite : Z_theta = (1 - theta) (+-Z_A) + theta Z_DH, linéaire en theta ; zéros sur la droite à hauteur t
pour theta*(t) = Z_A / (Z_A -+ Z_DH). Deux zéros voisins se rejoignent et quittent la droite à l'extremum de theta*
entre eux (seuil intrinsèque : ni fenêtre, ni base).
"""
from __future__ import annotations
import cmath, math
import numpy as np
from scipy.special import loggamma
try:
    from zero_reconstruction import hurwitz_zeta
    from rejection import KAPPA_DH
except ImportError:
    from .zero_reconstruction import hurwitz_zeta
    from .rejection import KAPPA_DH

_CHI = {1: 1, 2: 1j, 3: -1j, 4: -1}
_GAUSS = sum(_CHI[a] * cmath.exp(2j * math.pi * a / 5) for a in _CHI)
EPS = _GAUSS / (1j * math.sqrt(5))                    # nombre racine de L(s, chi), |EPS| = 1
PHI = (cmath.phase(EPS) / 2) % math.pi               # phase de Hardy (modulo pi)

def vartheta(t: float) -> float:
    """Phase de (5/pi)^((s+1)/2) Gamma((s+1)/2) en s = 1/2 + it."""
    return 0.5 * t * math.log(5 / math.pi) + float(loggamma(0.75 + 0.5j * t).imag)

def L_pair(s: complex) -> tuple[complex, complex]:
    s = complex(s); hz = {a: hurwitz_zeta(s, a / 5.0) for a in _CHI}; f = 5.0 ** (-s)
    return f * sum(_CHI[a] * hz[a] for a in _CHI), f * sum(np.conj(_CHI[a]) * hz[a] for a in _CHI)

def A(s: complex) -> complex:
    return cmath.exp(-1j * PHI) * L_pair(s)[0]

def DH(s: complex) -> complex:
    Lc, Lb = L_pair(s); return 0.5 * (1 - 1j * KAPPA_DH) * Lc + 0.5 * (1 + 1j * KAPPA_DH) * Lb

def hardy(t: float) -> tuple[float, float, float]:
    """(Z_A(t), Z_DH(t), défaut d'imaginaire relatif max)."""
    s = 0.5 + 1j * t; Lc, Lb = L_pair(s); ph = cmath.exp(1j * vartheta(t))
    za = ph * cmath.exp(-1j * PHI) * Lc; zd = ph * (0.5 * (1 - 1j * KAPPA_DH) * Lc + 0.5 * (1 + 1j * KAPPA_DH) * Lb)
    defect = max(abs(za.imag) / max(abs(za), 1e-300), abs(zd.imag) / max(abs(zd), 1e-300))
    return float(za.real), float(zd.real), float(defect)

def F_path(s: complex, theta: float, sign: int = +1) -> complex:
    Lc, Lb = L_pair(s)
    a = sign * cmath.exp(-1j * PHI) * Lc; d = 0.5 * (1 - 1j * KAPPA_DH) * Lc + 0.5 * (1 + 1j * KAPPA_DH) * Lb
    return (1 - theta) * a + theta * d
