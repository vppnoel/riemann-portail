"""V6.17 — Le Contour tourné : L(Δ, s) haut sur la droite critique, en double précision.

Δ(z) = Σ τ(n) e^{2iπnz}, poids 12. Avec F(w) = Δ(iw) = Σ τ(n) e^{-2πnw} (Re w > 0) :
    Λ(s) = (2π)^-s Γ(s) Σ τ(n) n^-s = ∫_0^∞ F(y) y^{s-1} dy,       Λ(s) = Λ(12 - s),  F(1/w) = w^12 F(w).
On tourne la demi-droite d'intégration d'un angle φ < π/2 (Cauchy : F décroît dans tout le secteur), puis on coupe à |w| = 1
et on replie la partie |w| < 1 par la modularité :
    Λ(s) = e^{iφs} [ A(s) + e^{-12iφ} B(s) ],   A(s) = ∫_0^∞ F(e^{x+iφ}) e^{sx} dx,   B(s) = ∫_0^∞ F(e^{x-iφ}) e^{(12-s)x} dx.
Pour s = 6 + it (t réel), B = conj(A) car τ est réel, d'où l'identité exacte, réelle :
    Λ(6 + it) = 2 e^{-φt} Re( e^{6iφ} A(6 + it) ).
Sur l'axe réel (φ = 0), Λ(6+it) ~ e^{-πt/2} naît d'une annulation de termes de taille 1 : il faut des centaines de chiffres
(V6.15, mpmath). Avec φ = π/2 - c/t, le facteur e^{-φt} absorbe cette annulation ; la double précision suffit (c = 6 maximise
c^6 e^{-c}, la taille relative du résultat). L'intégrale en x est calculée par Gauss–Legendre par panneaux.
"""
from __future__ import annotations
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import loggamma

def tau_float(M: int) -> np.ndarray:
    from delta_ramanujan import tau
    return np.array([float(x) for x in tau(M)])

class DeltaBand:
    """Évaluateur de Λ(6 + it) pour t dans une bande [t1, t2] (un angle φ commun)."""
    def __init__(self, taus: np.ndarray, t1: float, t2: float, c: float = 6.0, cut: float = 50.0, nodes: int = 24, osc: float = 3.0):
        self.t1, self.t2 = t1, t2
        tm = 0.5 * (t1 + t2); self.delta = c / tm; self.phi = math.pi / 2 - self.delta
        sd, cd = math.sin(self.delta), math.cos(self.delta)       # w = e^x (sin δ + i cos δ)
        Kmax = cut / (2 * math.pi * sd)                            # n e^x au-delà duquel e^{-2πn e^x sin δ} < e^{-cut}
        if Kmax > len(taus) - 1: raise ValueError(f"tau jusqu'à {Kmax:.0f} nécessaires")
        X = math.log(Kmax) + 0.5
        fmax = 2 * math.pi * Kmax * cd + t2                          # fréquence maximale de l'intégrande en x
        width = osc * 2 * math.pi / fmax; npan = int(math.ceil(X / width)); width = X / npan
        z, w = leggauss(nodes)
        x = (np.arange(npan)[:, None] * width + (z[None, :] + 1) * width / 2).ravel(); wx = np.tile(w * width / 2, npan)
        F = np.zeros(len(x), dtype=complex)
        ex = np.exp(x)
        nmax_x = np.minimum(len(taus) - 1, np.floor(Kmax / ex).astype(int))
        for n in range(1, int(nmax_x.max()) + 1):                  # les petits n servent partout, les grands près de x = 0
            k = nmax_x >= n
            if not k.any(): break
            ph = -2 * math.pi * n * ex[k]
            F[k] += taus[n] * np.exp(ph * sd) * np.exp(1j * ph * cd)
        self.x = x; self.W = wx * F * np.exp(6 * x) * np.exp(6j * self.phi)   # poids incluant e^{6x} et e^{6iφ}
        self.nodes = len(x); self.Kmax = Kmax

    def reA(self, t) -> np.ndarray:
        """Re(e^{6iφ} A(6+it)) pour un tableau de t."""
        t = np.atleast_1d(np.asarray(t, dtype=float)); out = np.empty(len(t))
        for i0 in range(0, len(t), 64):
            out[i0:i0 + 64] = (np.exp(1j * np.outer(t[i0:i0 + 64], self.x)) @ self.W).real
        return out

    def reA_grid(self, t0: float, dt: float, n: int) -> np.ndarray:
        """Même chose sur la grille t0 + k dt, k < n, par récurrence multiplicative."""
        v = self.W * np.exp(1j * t0 * self.x); step = np.exp(1j * dt * self.x); out = np.empty(n)
        for k in range(n):
            out[k] = v.sum().real
            v *= step
            if k % 256 == 255: v = self.W * np.exp(1j * (t0 + (k + 1) * dt) * self.x)   # recalage (erreur d'arrondi)
        return out

    def Z(self, t) -> np.ndarray:
        """Z_Δ(t) = Λ(6+it) / |(2π)^{-s} Γ(s)| = ± |L(Δ, 6 + it)| (normalisation non unitaire, réelle)."""
        t = np.atleast_1d(np.asarray(t, dtype=float))
        return 2 * self.reA(t) * np.exp(-self.phi * t - loggamma(6 + 1j * t).real + 6 * math.log(2 * math.pi))

    def Lambda(self, t) -> np.ndarray:
        t = np.atleast_1d(np.asarray(t, dtype=float)); return 2 * np.exp(-self.phi * t) * self.reA(t)

def theta_delta(t) -> np.ndarray:
    """θ(t) = arg Γ(6 + it) − t log 2π (continu, θ(0) = 0) ; N(T) = θ(T)/π + S(T)."""
    t = np.asarray(t, dtype=float); return loggamma(6 + 1j * t).imag - t * math.log(2 * math.pi)
