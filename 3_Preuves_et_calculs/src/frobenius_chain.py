"""V6.9 — Le chaînon : du Frobenius discret au flot continu.

1. Reconstruction depuis les seuls comptages (Modèle réduit). Les traces normalisées p_n = S_n / q^(n/2)
   (S_n = q^n + 1 - N_n) forment la suite t_n = <U^n v, v> d'un opérateur U = F / sqrt(q) et d'un vecteur v.
   Gram de Krylov G_mn = t_|n-m|, matrice décalée S_mn = t_|n+1-m| ; le faisceau S x = lambda G x redonne
   les valeurs propres de U sur le sous-espace cyclique (construction de type GNS / Naimark).
   Sa dimension est le rang de G : le nombre de zéros DISTINCTS. G >= 0 <=> U unitaire pour une métrique
   positive <=> RH (loi d'inertie, document 29).
2. Spectre des longueurs lu dans les zéros. Avec un poids gaussien w(gamma) = exp(-(gamma/s)^2/2),
       S(u) = -(sqrt(2 pi)/s) * somme_gamma w(gamma) e^{i gamma u}
   a des pics en u = log n de hauteur c(n)/sqrt(n), c(n) coefficient de -F'/F (formule explicite).
   Produit d'Euler <=> c(n) porté par les puissances de nombres premiers <=> pics seulement en log p^k.
   Modèle réduit (une seule base q) : pics seulement en u = n log q, hauteur -(log q) p_n.
"""
from __future__ import annotations
import math
import numpy as np

# ---------------------------------------------------------------- 1. reconstruction GNS / Krylov
def traces_from_b(b: np.ndarray, L: int) -> np.ndarray:
    """p_0..p_{L-1} (sommes de puissances des beta_j), réelles, depuis le polynôme normalisé b."""
    m = len(b) - 1; e = [(-1) ** k * b[k] for k in range(m + 1)]; S = [float(m)]
    for n in range(1, L):
        s = sum((-1) ** (i - 1) * e[i] * S[n - i] for i in range(1, min(n - 1, m) + 1))
        if n <= m: s += (-1) ** (n - 1) * n * e[n]
        S.append(s)
    return np.array(S)

def gns_frobenius(b: np.ndarray, tol: float = 1e-9):
    """Renvoie (rang, valeurs propres reconstruites, valeurs propres du Gram de taille 2g + 4)."""
    g = (len(b) - 1) // 2; L = 2 * g + 4; p = traces_from_b(b, L + 2)
    idx = np.arange(L); G = p[np.abs(idx[None, :] - idx[:, None])]
    ev = np.linalg.eigvalsh(G); r = int(np.sum(np.abs(ev) > tol * np.max(np.abs(ev))))
    i = np.arange(r); G0 = G[:r, :r]; S = p[np.abs(i[None, :] + 1 - i[:, None])]
    lam = np.linalg.eigvals(np.linalg.solve(G0, S))
    return r, lam, ev

def spectral_masses(b: np.ndarray, lam: np.ndarray) -> np.ndarray:
    """Masses w_j de la mesure spectrale : p_n = somme w_j lam_j^n (Vandermonde, n < nombre de lam).
    La multiplicité d'un zéro, invisible comme dimension de l'espace reconstruit, y reparaît comme masse."""
    r = len(lam); p = traces_from_b(b, r); V = np.vander(lam, r, increasing=True).T
    return np.linalg.solve(V, p.astype(complex))

def distinct(z: np.ndarray, tol: float = 1e-6) -> np.ndarray:
    out = []
    for x in z:
        if all(abs(x - y) > tol for y in out): out.append(x)
    return np.array(out)

def match_error(lam: np.ndarray, beta: np.ndarray) -> float:
    """max sur lambda de la distance à la valeur propre vraie la plus proche, et réciproquement."""
    if len(lam) == 0: return float("nan")
    a = max(min(abs(l - b) for b in beta) for l in lam); c = max(min(abs(b - l) for l in lam) for b in beta)
    return float(max(a, c))

def inverse_closure(lam: np.ndarray) -> float:
    """Équation fonctionnelle vue sur le spectre : l'ensemble est stable par lambda -> 1/lambda."""
    return float(max(min(abs(1 / l - m) for m in lam) for l in lam))

# ---------------------------------------------------------------- 2. spectre des longueurs
def length_spectrum(gam: np.ndarray, u: np.ndarray, s: float, chunk: int = 512) -> np.ndarray:
    """S(u) = -(sqrt(2 pi)/s) somme w(Re gamma) e^{i gamma u}, gamma complexes (zéros hors droite inclus)."""
    gam = np.asarray(gam, dtype=complex); w = np.exp(-0.5 * (gam.real / s) ** 2); out = np.zeros(len(u), dtype=complex)
    for i0 in range(0, len(u), chunk):
        uu = u[i0: i0 + chunk]; out[i0: i0 + chunk] = (w[None, :] * np.exp(1j * np.outer(uu, gam))).sum(axis=1)
    return -math.sqrt(2 * math.pi) / s * out

def log_derivative_coefficients(a: np.ndarray) -> np.ndarray:
    """c(n) avec -F'/F = somme c(n) n^-s, pour F = somme a(n) n^-s, a(1) = 1 (récurrence de Dirichlet)."""
    N = len(a) - 1; c = np.zeros(N + 1, dtype=complex)
    for n in range(2, N + 1):
        s = a[n] * math.log(n)
        for d in range(2, n + 1):
            if n % d == 0 and n // d >= 2: s -= a[d] * c[n // d]
        c[n] = s
    return c

def is_prime_power(n: int) -> bool:
    if n < 2: return False
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0: n //= p
            return n == 1
        p += 1
    return True

def curve_gammas(b: np.ndarray, q: int, T: float) -> np.ndarray:
    """Zéros (gamma = -i(s - 1/2)) de P(q^-s), périodiques de période 2 pi / log q, |Re gamma| <= T."""
    beta = 1 / np.roots(b[::-1]); lq = math.log(q); out = []
    K = int(T * lq / (2 * math.pi)) + 2
    for be in beta:
        for k in range(-K, K + 1):
            gm = (np.angle(be) + 2 * math.pi * k) / lq - 1j * math.log(abs(be)) / lq
            if abs(gm.real) <= T: out.append(gm)
    return np.array(out)
