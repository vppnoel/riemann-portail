"""V6.8 — L'Archipel d'Euler : dans l'espace des fonctions qui ont l'équation fonctionnelle, où RH tient-elle ?

Espace V_q^kappa (q premier, parité kappa = 0 paire, 1 impaire) : combinaisons réelles
    F_c(s) = somme_chi c_chi A_chi(s),   A_chi(s) = e^{-i phi_chi} L(s, chi),
sur les caractères primitifs chi modulo q de parité kappa ; phi_chi = arg(epsilon_chi)/2, epsilon_chi le nombre racine.
Chaque A_chi a une fonction de Hardy réelle Z_chi(t) = e^{i vartheta(t)} A_chi(1/2 + it), avec le même vartheta ;
donc tout F_c aussi : Z_c = somme c_chi Z_chi. Les zéros de F_c sont symétriques par rapport à la droite critique ;
une paire ne peut quitter la droite qu'en passant par un zéro double de Z_c.
Points d'Euler : les axes c = e_chi (une seule L(s, chi)). Ailleurs, pas de produit d'Euler.

Distance (projective) d'un point d'Euler e_i au premier zéro double à la hauteur t :
    zéro double en t  <=>  A(t) c = 0,  A(t) = [[Z_chi(t)], [Z'_chi(t)]] (2 x d) ;
    dist(e_i, ker A(t)) = sqrt(r^T (A A^T)^{-1} r),  r = A e_i   (sinus de l'angle ; d >= 3).
    Pour d = 2, ker A(t) n'est non nul qu'aux zéros du wronskien W = Z_1 Z_2' - Z_2 Z_1'.
Rayon de l'île jusqu'à la hauteur T : r(T) = min sur |t| <= T de cette distance.
"""
from __future__ import annotations
import cmath, math
import numpy as np
from scipy.special import loggamma

_B2K = [1 / 6, -1 / 30, 1 / 42, -1 / 30, 5 / 66, -691 / 2730, 7 / 6, -3617 / 510, 43867 / 798,
        -174611 / 330, 854513 / 138, -236364091 / 2730, 8553103 / 6, -23749461029 / 870, 8615841276005 / 14322]

def hurwitz_vec(s: np.ndarray, a: float, chunk: int = 4096) -> np.ndarray:
    """zeta(s, a) pour un tableau de s (Euler–Maclaurin, mêmes paramètres que zero_reconstruction.hurwitz_zeta)."""
    s = np.asarray(s, dtype=complex); out = np.empty_like(s)
    for i0 in range(0, len(s), chunk):
        ss = s[i0: i0 + chunk]; M = int(np.max(np.abs(ss))) + 25
        n = np.arange(M, dtype=float) + a; x = M + a
        tot = np.exp(-np.outer(ss, np.log(n))).sum(axis=1) + x ** (1 - ss) / (ss - 1) + 0.5 * x ** (-ss)
        term = ss * x ** (-ss - 1); fact = 2.0
        for k, b in enumerate(_B2K, start=1):
            tot = tot + b / fact * term
            term = term * (ss + 2 * k - 1) * (ss + 2 * k) / (x * x); fact *= (2 * k + 1) * (2 * k + 2)
        out[i0: i0 + chunk] = tot
    return out

def primitive_root(q: int) -> int:
    for g in range(2, q):
        if len({pow(g, k, q) for k in range(1, q)}) == q - 1: return g
    raise ValueError(q)

def characters(q: int, parity: int) -> list[dict]:
    """Caractères non principaux modulo q premier, de parité donnée : dict(k, table {a: chi(a)}, eps, phi, reel)."""
    g = primitive_root(q); log = {pow(g, j, q): j for j in range(q - 1)}; out = []
    for k in range(1, q - 1):
        if k % 2 != parity: continue                      # chi_k(-1) = (-1)^k
        tab = {a: cmath.exp(2j * math.pi * log[a] * k / (q - 1)) for a in range(1, q)}
        tau = sum(tab[a] * cmath.exp(2j * math.pi * a / q) for a in tab)
        eps = tau / ((1j ** parity) * math.sqrt(q))
        out.append(dict(k=k, table=tab, eps=eps, phi=cmath.phase(eps) / 2, reel=(2 * k == q - 1)))
    return out

def vartheta(t, q: int, parity: int):
    t = np.asarray(t, dtype=float)
    return 0.5 * t * math.log(q / math.pi) + np.imag(loggamma(0.25 + 0.5 * parity + 0.5j * t))

def hardy_grid(q: int, parity: int, t: np.ndarray):
    """Z (d x len(t)) : fonctions de Hardy des A_chi ; défaut d'imaginaire relatif max ; liste des caractères."""
    chars = characters(q, parity); s = 0.5 + 1j * np.asarray(t, dtype=float)
    Hz = {a: hurwitz_vec(s, a / q) for a in range(1, q)}
    pref = np.exp(-s * math.log(q)) * np.exp(1j * vartheta(t, q, parity))
    Z = np.empty((len(chars), len(t))); defect = 0.0
    for i, ch in enumerate(chars):
        w = cmath.exp(-1j * ch["phi"]) * pref * sum(ch["table"][a] * Hz[a] for a in Hz)
        Z[i] = w.real; defect = max(defect, float(np.max(np.abs(w.imag) / np.maximum(np.abs(w), 1e-300))))
    return Z, defect, chars

def F_values(q: int, parity: int, c: np.ndarray, s: np.ndarray) -> np.ndarray:
    """F_c(s) = somme c_chi e^{-i phi} L(s, chi) en des points complexes quelconques."""
    chars = characters(q, parity); s = np.asarray(s, dtype=complex)
    Hz = {a: hurwitz_vec(s, a / q) for a in range(1, q)}; pref = np.exp(-s * math.log(q))
    return sum(ci * cmath.exp(-1j * ch["phi"]) * pref * sum(ch["table"][a] * Hz[a] for a in Hz) for ci, ch in zip(c, chars))

def dirichlet_coefficients(q: int, parity: int, c: np.ndarray, N: int) -> np.ndarray:
    chars = characters(q, parity); a = np.zeros(N + 1, dtype=complex)
    for n in range(1, N + 1):
        if n % q: a[n] = sum(ci * cmath.exp(-1j * ch["phi"]) * ch["table"][n % q] for ci, ch in zip(c, chars))
    return a

# ---------------------------------------------------------------- distance au premier zéro double
def double_zero_distance(Z: np.ndarray, Zp: np.ndarray, i0: int) -> np.ndarray:
    """d >= 3 : distance projective (sinus) de e_{i0} au sous-espace ker A(t), pour chaque t de la grille."""
    m11 = np.sum(Z * Z, axis=0); m12 = np.sum(Z * Zp, axis=0); m22 = np.sum(Zp * Zp, axis=0)
    r1, r2 = Z[i0], Zp[i0]; det = m11 * m22 - m12 ** 2
    cost = (m22 * r1 * r1 - 2 * m12 * r1 * r2 + m11 * r2 * r2) / np.where(det > 0, det, np.nan)
    return np.sqrt(np.clip(cost, 0.0, 1.0))

def kernel_point(Zt: np.ndarray, Zpt: np.ndarray, i0: int) -> np.ndarray:
    """Point de ker A(t) le plus proche de e_{i0} (projection orthogonale), normalisé."""
    A = np.vstack([Zt, Zpt]); e = np.zeros(A.shape[1]); e[i0] = 1.0
    P = A.T @ np.linalg.solve(A @ A.T, A); c = e - P @ e; return c / np.linalg.norm(c)

def wronskian_events(t: np.ndarray, Z: np.ndarray, Zp: np.ndarray):
    """d = 2 : zéros du wronskien (interpolation linéaire) et direction du noyau c = (Z_2, -Z_1)."""
    W = Z[0] * Zp[1] - Z[1] * Zp[0]; idx = np.flatnonzero(np.sign(W[1:]) * np.sign(W[:-1]) < 0); ev = []
    for i in idx:
        f = W[i] / (W[i] - W[i + 1]); tt = t[i] + f * (t[i + 1] - t[i])
        z1 = Z[0, i] + f * (Z[0, i + 1] - Z[0, i]); z2 = Z[1, i] + f * (Z[1, i + 1] - Z[1, i])
        c = np.array([z2, -z1]); ev.append((tt, c / np.linalg.norm(c)))
    return ev

def first_order_euler_defect(q: int, parity: int, i0: int, M: int = 60) -> tuple[float, float]:
    """Forme quadratique du défaut de multiplicativité au premier ordre en e_{i0}, sur les directions orthogonales.
    Défaut(m, n) = a(1) b(mn) + b(1) a(mn) - a(m) b(n) - b(m) a(n), (m, n) = 1, mn <= M^2.
    Renvoie (plus petite valeur propre sur les directions orthogonales, valeur pour la direction e_{i0} elle-même)."""
    chars = characters(q, parity); d = len(chars); N = M * M
    def coeffs(j):
        e = np.zeros(d); e[j] = 1.0; return dirichlet_coefficients(q, parity, e, N)
    a = coeffs(i0); rows = []
    pairs = [(m, n) for m in range(1, M + 1) for n in range(m, M + 1) if math.gcd(m, n) == 1 and m * n <= N]
    cols = []
    for j in range(d):
        b = coeffs(j); cols.append(np.array([a[1] * b[m * n] + b[1] * a[m * n] - a[m] * b[n] - b[m] * a[n] for m, n in pairs]))
    Cm = np.array(cols).T                                 # (paires x d)
    Q = np.real(Cm.conj().T @ Cm) / len(pairs)
    others = [j for j in range(d) if j != i0]
    Qo = Q[np.ix_(others, others)]
    return float(np.linalg.eigvalsh(Qo)[0]) if others else float("nan"), float(Q[i0, i0])

# ---------------------------------------------------------------- raffinement (évaluations directes)
def hardy_and_derivative(q: int, parity: int, t: float, h: float = 1e-4):
    """Z_chi(t) et Z'_chi(t) (différences centrées, pas h) pour tous les caractères de l'espace."""
    Zl, _, _ = hardy_grid(q, parity, np.array([t - h, t, t + h]))
    return Zl[:, 1], (Zl[:, 2] - Zl[:, 0]) / (2 * h)

def refine_distance(q: int, parity: int, i0: int, t_lo: float, t_hi: float):
    """d >= 3 : minimum continu de la distance au zéro double sur [t_lo, t_hi] ; renvoie (rayon, t*, c*)."""
    from scipy.optimize import minimize_scalar
    def f(x):
        z, zp = hardy_and_derivative(q, parity, x); return float(double_zero_distance(z[:, None], zp[:, None], i0)[0])
    r = minimize_scalar(f, bounds=(t_lo, t_hi), method="bounded", options=dict(xatol=1e-10))
    z, zp = hardy_and_derivative(q, parity, r.x); return float(r.fun), float(r.x), kernel_point(z, zp, i0)

def refine_wronskian(q: int, parity: int, i0: int, t_lo: float, t_hi: float):
    """d = 2 : zéro du wronskien dans [t_lo, t_hi] (brentq) ; renvoie (rayon, t*, c*)."""
    from scipy.optimize import brentq
    def W(x):
        z, zp = hardy_and_derivative(q, parity, x); return float(z[0] * zp[1] - z[1] * zp[0])
    try: x = brentq(W, t_lo, t_hi, xtol=1e-12)
    except ValueError: x = 0.5 * (t_lo + t_hi)
    z, _ = hardy_and_derivative(q, parity, x); c = np.array([z[1], -z[0]]); c /= np.linalg.norm(c)
    if c[i0] < 0: c = -c
    return float(math.sqrt(max(1 - c[i0] ** 2, 0.0))), float(x), c
