"""V6.10 — Le générateur des premiers : l'opérateur de ζ reconstruit depuis les seuls nombres premiers.

Dans le Modèle réduit (document 32), les traces p_n = Tr U^n, lues dans les comptages, donnent l'opérateur U par un
faisceau de Toeplitz. Pour ζ, il n'y a pas de pas naturel : on en choisit un, h > 0, et l'on pose

    t_n = somme sur les zéros rho = 1/2 + i gamma de  g^(gamma) e^{i gamma n h},

où g = phi * phi, phi bosse paire à support [-a, a] (phi(u) = cos^4(pi u / 2a)), g^(r) = phi^(r)^2 >= 0.
Par la formule explicite, t_n se calcule SANS AUCUN ZÉRO : nombres premiers (puissances), terme archimédien,
conducteur, pôle. Le faisceau de Toeplitz (S x = lambda G x, G_jk = t_{j-k}, S_jk = t_{j-k+1}) donne alors
lambda = e^{i gamma h} : l'opérateur de translation de pas h, F_h = e^{h D}, et son générateur D = log(F_h) / h.
G est la métrique : G >= 0 pour toute fenêtre <=> positivité de Weil <=> RH.

Convention de Fourier : f^(r) = int f(u) e^{i r u} du.
Formule explicite (fonction test g_n(u) = g(u - n h), g^_n(r) = g^(r) e^{i r n h}) :
  somme_gamma g^_n(gamma) = [pôle] g^_n(i/2) + g^_n(-i/2)
                           + (1/2 pi) int g^_n(r) [log(q/pi) + Re psi((1/2 + par)/2 + i r/2)] dr
                           - somme_m [c(m) g_n(log m) + conj(c(m)) g_n(-log m)] / sqrt(m),
avec -F'/F = somme c(m) m^-s (c = Lambda pour ζ, Lambda chi pour L(s, chi), coefficients de DH sinon).
"""
from __future__ import annotations
import math
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import digamma

W_COS4 = (3 / 8, 1 / 2, 1 / 8)          # cos^4(x) = 3/8 + cos(2x)/2 + cos(4x)/8

KINDS = {"zeta": dict(q=1, par=0, pole=True), "L_chi5": dict(q=5, par=1, pole=False), "DH": dict(q=5, par=1, pole=False)}

# ------------------------------------------------------------------ fonction test
def _sinc(z):
    z = np.asarray(z, dtype=complex); out = np.ones_like(z); m = np.abs(z) > 1e-8
    out[m] = np.sin(z[m]) / z[m]; out[~m] = 1 - z[~m] ** 2 / 6
    return out

def phi(u: np.ndarray, a: float) -> np.ndarray:
    u = np.asarray(u, dtype=float); out = np.cos(np.pi * u / (2 * a)) ** 4
    return np.where(np.abs(u) <= a, out, 0.0)

def phi_hat(r, a: float) -> np.ndarray:
    """phi^(r) = int phi(u) e^{iru} du, en forme close (r réel ou complexe)."""
    r = np.asarray(r, dtype=complex); out = np.zeros_like(r)
    for k, w in enumerate(W_COS4):
        out += w * a * (_sinc((r + k * np.pi / a) * a) + _sinc((r - k * np.pi / a) * a))
    return out

def g_hat(r, a: float) -> np.ndarray:
    return phi_hat(r, a) ** 2

def g_of(x: np.ndarray, a: float, order: int = 64) -> np.ndarray:
    """g(x) = (phi * phi)(x), support [-2a, 2a], par Gauss-Legendre sur le recouvrement (exact à la machine près)."""
    x = np.abs(np.atleast_1d(np.asarray(x, dtype=float))); out = np.zeros_like(x)
    z, wz = leggauss(order); m = x < 2 * a
    lo = x[m] - a; hi = np.full_like(lo, a)
    mid = 0.5 * (lo + hi); half = 0.5 * (hi - lo)
    y = mid[:, None] + half[:, None] * z[None, :]
    out[m] = half * np.sum(wz[None, :] * phi(y, a) * phi(x[m][:, None] - y, a), axis=1)
    return out

# ------------------------------------------------------------------ côté premiers (aucun zéro)
def arch_traces(n: np.ndarray, h: float, a: float, q: int, par: int, R: float | None = None, block: float = 0.25, order: int = 16) -> np.ndarray:
    """(1/pi) int_0^inf g^(r) cos(r n h) [log(q/pi) + Re psi((1/2+par)/2 + i r/2)] dr (g^ et Omega pairs)."""
    if R is None: R = 260.0 / a
    z, wz = leggauss(order); nb = int(math.ceil(R / block))
    starts = np.arange(nb) * block; r = (starts[:, None] + block * (z[None, :] + 1) / 2).ravel(); wr = np.tile(wz * block / 2, nb)
    om = math.log(q / math.pi) + np.real(digamma((0.5 + par) / 2 + 0.5j * r))
    base = (g_hat(r, a).real * om * wr) / math.pi
    out = np.empty(len(n))
    for i0 in range(0, len(n), 64):
        nn = np.asarray(n[i0:i0 + 64], dtype=float)
        out[i0:i0 + 64] = np.cos(np.outer(nn * h, r)) @ base
    return out

def prime_traces(c: np.ndarray, n: np.ndarray, h: float, a: float) -> np.ndarray:
    """- somme_m [c(m) g(log m - n h) + conj c(m) g(-log m - n h)] / sqrt(m), pour n >= 0."""
    M = len(c) - 1; m = np.arange(2, M + 1); lm = np.log(m); cm = c[2:] / np.sqrt(m)
    keep = np.abs(cm) > 0; m, lm, cm = m[keep], lm[keep], cm[keep]
    out = np.zeros(len(n), dtype=complex)
    for i, k in enumerate(n):
        x1 = lm - k * h; s1 = np.abs(x1) < 2 * a
        x2 = -lm - k * h; s2 = np.abs(x2) < 2 * a
        out[i] = -(np.sum(cm[s1] * g_of(x1[s1], a)) + np.sum(np.conj(cm[s2]) * g_of(x2[s2], a)))
    return out

def traces_from_primes(kind: str, c: np.ndarray, N: int, h: float, a: float) -> np.ndarray:
    """t_0..t_N calculées sans aucun zéro. c : coefficients de -F'/F jusqu'à au moins exp(N h + 2a)."""
    spec = KINDS[kind]; n = np.arange(N + 1)
    need = math.exp(N * h + 2 * a)
    if len(c) - 1 < need: raise ValueError(f"coefficients jusqu'à {need:.0f} nécessaires")
    t = prime_traces(c, n, h, a) + arch_traces(n, h, a, spec["q"], spec["par"])
    if spec["pole"]:
        t = t + g_hat(0.5j, a).real * 2 * np.cosh(n * h / 2)
    return t

def traces_from_zeros(gammas: np.ndarray, N: int, h: float, a: float) -> np.ndarray:
    """Contrôle : t_n = somme g^(gamma) e^{i gamma n h} sur une liste de zéros (gamma complexes)."""
    gam = np.asarray(gammas, dtype=complex); w = g_hat(gam, a)
    return np.array([np.sum(w * np.exp(1j * gam * k * h)) for k in range(N + 1)])

# ------------------------------------------------------------------ faisceau : l'opérateur de translation et son générateur
def toeplitz_pencil(t: np.ndarray, L: int):
    """G_jk = t_{j-k}, S_jk = t_{j-k+1} (t_{-n} = conj t_n), taille L x L ; il faut t_0..t_L."""
    def T(off):
        j = np.arange(L)[:, None]; k = np.arange(L)[None, :]; d = j - k + off
        return np.where(d >= 0, t[np.abs(d)], np.conj(t[np.abs(d)]))
    return T(0), T(1)

def metric_and_generator(t: np.ndarray, L: int, h: float, rel_tol: float = 1e-11):
    """Métrique G (valeurs propres) et générateur réduit au sous-espace de rang numérique.
    Renvoie dict : mu (valeurs propres de G, croissantes), rang, lam (valeurs propres de F_h), gamma (= log lam / i h),
    poids (masse spectrale de chaque gamma, par Vandermonde)."""
    G, S = toeplitz_pencil(t, L); G = 0.5 * (G + G.conj().T)
    mu, Q = np.linalg.eigh(G); keep = np.abs(mu) > rel_tol * np.max(np.abs(mu))
    P = Q[:, keep]; Gr = P.conj().T @ G @ P; Sr = P.conj().T @ S @ P
    lam = np.linalg.eigvals(np.linalg.solve(Gr, Sr))
    gam = np.log(lam) / (1j * h)
    V = np.exp(1j * np.outer(np.arange(L), gam * h))            # t_n ~ somme w e^{i gamma n h}
    cn = np.linalg.norm(V, axis=0)                              # colonnes normalisées : |lambda| != 1 ne domine plus
    wts = np.linalg.lstsq(V / cn, t[:L], rcond=None)[0] / cn
    o = np.argsort(gam.real)
    return dict(mu=mu, rank=int(keep.sum()), lam=lam[o], gamma=gam[o], weight=wts[o],
                negatives=int(np.sum(mu < -rel_tol * np.max(np.abs(mu)))))

# ------------------------------------------------------------------ V6.12 : la récurrence de Levinson (le Kalman relu)
def levinson(t: np.ndarray, N: int):
    """Récurrence de Levinson–Szegő sur la suite hermitienne t_0..t_N (Toeplitz G_jk = t_{j-k}).
    Renvoie (k, E) : coefficients de réflexion k_1..k_N et erreurs de prédiction (innovations) E_0..E_N.
    E_n = det G_{n+1} / det G_n ; G_{N+1} définie positive <=> tous les E_n > 0 <=> tous les |k_n| < 1.
    C'est le filtre de Kalman d'un signal stationnaire de covariance t : la première innovation négative
    est la première fenêtre où la métrique cesse d'être positive."""
    a = np.array([1.0 + 0j]); E = [float(t[0].real)]; K = []
    for m in range(1, N + 1):
        acc = t[m] + (np.dot(a[1:], t[m - 1:0:-1]) if m > 1 else 0.0)
        k = -acc / E[-1]
        ext = np.concatenate([a, [0.0]]); a = ext + k * np.conj(ext[::-1])
        E.append(float((E[-1] * (1 - abs(k) ** 2)).real)); K.append(k)
    return np.array(K), np.array(E)

# ------------------------------------------------------------------ V6.14 : le seuil de détection, mesuré par les valeurs propres
def lmin_ratio(t: np.ndarray, n: int) -> float:
    """lambda_min / lambda_max de la métrique de Toeplitz G_n (taille n, G_jk = t_{j-k})."""
    from scipy.linalg import toeplitz, eigvalsh
    e = eigvalsh(toeplitz(t[:n], np.conj(t[:n]))); return float(e[0] / e[-1])

def first_negative_size(t: np.ndarray, tau: float, nmax: int) -> int | None:
    """Plus petite taille n <= nmax telle que lambda_min(G_n) < -tau * lambda_max(G_n).
    lambda_min(G_n) ne croît pas avec n (entrelacement de Cauchy : G_n est une sous-matrice principale de G_{n+1}),
    d'où une dichotomie. Critère robuste : contrairement au signe d'une innovation de Levinson, il ne dépend pas
    du conditionnement de G (en double précision, le bruit des valeurs propres est de l'ordre de 1e-15 * lambda_max)."""
    if lmin_ratio(t, nmax) >= -tau: return None
    lo, hi = 1, nmax
    while hi - lo > 1:
        m = (lo + hi) // 2
        if lmin_ratio(t, m) < -tau: hi = m
        else: lo = m
    return hi

def heisenberg_length(q: int, gamma0: float) -> float:
    """Temps de Heisenberg à la hauteur gamma0 : 2 pi x densité moyenne des zéros = log(q gamma0 / 2 pi),
    logarithme du conducteur analytique (degré 1)."""
    return math.log(q * gamma0 / (2 * math.pi))
