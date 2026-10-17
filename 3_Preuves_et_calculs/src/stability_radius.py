"""V6.7 — STABILITY-RADIUS dans le Modèle réduit : marge de la forme contre marge de l'objet.

Polynôme normalisé B(u) = P(u / sqrt q) = sum b_k u^k = prod_{j=1}^{2g} (1 - beta_j u), beta_j = alpha_j / sqrt q.
Équation fonctionnelle  <=>  B palindromique : b_{2g-k} = b_k, b_0 = 1.  RH  <=>  |beta_j| = 1.
Données locales libres : b_1, ..., b_g (équivalent aux comptages N_1, ..., N_g).

Forme de Weil fenêtrée (fenêtre = L étages), construite depuis les seuls comptages :
    T_L = (p_|m-n|)_{0 <= m, n < L},   p_k = S_k / q^(k/2) = somme des beta_j^k,  p_0 = 2g.
Pour une vraie courbe, T_L = V* V (V : Vandermonde des 2g points beta_j du cercle) : positive, de rang 2g.

Deux marges :
  - marge de la forme (non structurée) : lambda_min(T_L) / 2g ; toute perturbation de la matrice permise ;
  - marge de l'objet (structurée) : plus petite perturbation des données locales (b_1..b_g), équation
    fonctionnelle conservée, qui fait perdre la positivité. Norme : coefficients du polynôme B entier
    (chaque b_k, k < g, compte deux fois).
Écriture de Chebyshev : B(u) = u^g H(u + 1/u), H unitaire de degré g, linéaire en (b_1..b_g) ;
RH <=> les g racines de H sont réelles dans [-2, 2] (y_j = 2 cos phi_j).
La sortie de la région RH se fait par une racine double de H dans [-2, 2] (deux zéros se rencontrent)
ou par une racine en +-2 : contraintes linéaires en la perturbation, d'où une distance en forme close.
"""
from __future__ import annotations
import math
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import minimize_scalar

# ---------------------------------------------------------------- normalisation et écriture de Chebyshev
def normalized(c: list[int], q: int) -> np.ndarray:
    """b_k = c_k q^(-k/2), k = 0..2g."""
    return np.array([ck * q ** (-k / 2) for k, ck in enumerate(c)], dtype=float)

def from_free(bfree: np.ndarray) -> np.ndarray:
    """(b_1..b_g) -> B palindromique complet (b_0 = 1)."""
    g = len(bfree); b = np.empty(2 * g + 1); b[0] = b[-1] = 1.0
    for k in range(1, g + 1): b[k] = b[2 * g - k] = bfree[k - 1]
    return b

def _cheb_term(m: int) -> np.ndarray:
    """u^m + u^-m = 2 T_m(w/2) comme polynôme en w (coefficients, degré croissant)."""
    if m == 0: return np.array([2.0])   # non utilisé (terme central séparé)
    c = np.zeros(m + 1); c[m] = 1.0
    p = C.cheb2poly(c)                   # T_m(x), x = w/2
    return 2.0 * p * (0.5 ** np.arange(m + 1))

def H_poly(b: np.ndarray) -> np.ndarray:
    """Coefficients de H (degré croissant), B(u) = u^g H(u + 1/u)."""
    g = (len(b) - 1) // 2; h = np.zeros(g + 1); h[0] += b[g]
    for m in range(1, g + 1):
        t = _cheb_term(m); h[: m + 1] += b[g - m] * t
    return h

def basis(g: int) -> list[np.ndarray]:
    """Effet sur H d'une variation unité de b_k (k = 1..g) : e_k(w), degré croissant."""
    out = []
    for k in range(1, g + 1):
        e = np.zeros(g + 1)
        if k == g: e[0] = 1.0
        else: m = g - k; e[: m + 1] = _cheb_term(m)
        out.append(e)
    return out

def weights(g: int) -> np.ndarray:
    """Poids de la norme : b_k (k < g) apparaît deux fois dans B, b_g une fois."""
    w = np.full(g, 2.0); w[-1] = 1.0; return w

def is_rh(b: np.ndarray) -> bool:
    return off_circle(b) == 0

def off_circle(b: np.ndarray, tol: float = 1e-6) -> int:
    r = np.roots(np.asarray(b[::-1], dtype=float)); return int(np.sum(np.abs(np.abs(r) - 1) > tol))

# ---------------------------------------------------------------- forme de Weil fenêtrée
def power_sums_b(b: np.ndarray, L: int) -> np.ndarray:
    """p_0..p_{L-1} (réels) des racines inverses beta_j de B (identités de Newton)."""
    m = len(b) - 1; e = [(-1) ** k * b[k] for k in range(m + 1)]; S = [float(m)]
    for n in range(1, L):
        s = sum((-1) ** (i - 1) * e[i] * S[n - i] for i in range(1, min(n - 1, m) + 1))
        if n <= m: s += (-1) ** (n - 1) * n * e[n]
        S.append(s)
    return np.array(S)

def toeplitz_form(b: np.ndarray, L: int) -> np.ndarray:
    p = power_sums_b(b, L); i = np.arange(L)
    return p[np.abs(i[:, None] - i[None, :])]

def form_margin(b: np.ndarray, L: int) -> float:
    """Marge de la forme : lambda_min(T_L) / 2g."""
    g = (len(b) - 1) // 2
    return float(np.linalg.eigvalsh(toeplitz_form(b, L))[0]) / (2 * g)

def inertia(b: np.ndarray, L: int, tol: float = 1e-9) -> int:
    """Nombre de valeurs propres négatives de T_L (relativement à 2g)."""
    g = (len(b) - 1) // 2; ev = np.linalg.eigvalsh(toeplitz_form(b, L)); return int(np.sum(ev < -tol * 2 * g * max(1.0, np.max(np.abs(ev)) / (2 * g))))

# ---------------------------------------------------------------- marge de l'objet (rayon structuré)
def exit_candidates(b: np.ndarray, ngrid: int = 4001) -> list[dict]:
    """Points de sortie candidats de la région RH (minima locaux de la distance à une racine double de H, et les
    deux bords x = +-2), triés par distance. Chaque élément : dict(rayon, mecanisme, x, delta)."""
    g = (len(b) - 1) // 2; h = H_poly(b); E = basis(g); Dinv = 1.0 / weights(g)
    ev = lambda p, x: np.polynomial.polynomial.polyval(x, p)
    dv = lambda p, x: np.polynomial.polynomial.polyval(x, np.polynomial.polynomial.polyder(p)) if len(p) > 1 else 0.0 * x
    def cost_double(x):
        A = np.array([[ev(e, x) for e in E], [dv(e, x) for e in E]]); r = np.array([ev(h, x), dv(h, x)])
        M = (A * Dinv) @ A.T
        try: lam = np.linalg.solve(M, r)
        except np.linalg.LinAlgError: return np.inf, None
        return float(r @ lam), -(Dinv * (A.T @ lam))
    out = []
    if g >= 2:
        xs = np.linspace(-2, 2, ngrid); cs = np.array([cost_double(x)[0] for x in xs])
        loc = [i for i in range(1, ngrid - 1) if cs[i] <= cs[i - 1] and cs[i] <= cs[i + 1]]
        for i in loc:
            res = minimize_scalar(lambda x: cost_double(x)[0], bounds=(xs[i - 1], xs[i + 1]), method="bounded", options=dict(xatol=1e-13))
            c, d = cost_double(res.x)
            if d is not None and np.isfinite(c): out.append(dict(rayon=math.sqrt(max(c, 0.0)), mecanisme="rencontre", x=float(res.x), delta=d))
    for x in (-2.0, 2.0):
        a = np.array([ev(e, x) for e in E]); r = ev(h, x); n2 = float(a @ (Dinv * a))
        out.append(dict(rayon=abs(r) / math.sqrt(n2), mecanisme="bord", x=x, delta=-(Dinv * a) * r / n2))
    return sorted(out, key=lambda d: d["rayon"])

def structured_radius(b: np.ndarray, ngrid: int = 4001) -> dict:
    """Plus petite perturbation (b_1..b_g), norme de B, qui fait sortir de la région RH.
    Renvoie dict(rayon, mecanisme, x, delta) ; mecanisme = 'rencontre' (racine double de H en x : deux zéros se
    rencontrent) ou 'bord' (racine de H en x = +-2 : un zéro réel alpha = +-sqrt q)."""
    return exit_candidates(b, ngrid)[0]

def perturbed(b: np.ndarray, delta: np.ndarray, scale: float = 1.0) -> np.ndarray:
    g = (len(b) - 1) // 2; return from_free(b[1: g + 1] + scale * delta)

# ---------------------------------------------------------------- seuils le long d'un trajet vraie courbe -> faux jumeau
def form_threshold(A: np.ndarray, Bm: np.ndarray) -> float:
    """Interpolation des formes (1 - tau) A + tau B, A > 0 : tau_c = -1/mu_min, (B - A) v = mu A v."""
    from scipy.linalg import eigh
    w = np.linalg.eigvalsh(A)
    if w[0] <= 1e-12 * w[-1]: return 0.0
    mu = eigh(Bm - A, A, eigvals_only=True)[0]
    return -1.0 / mu if mu < 0 else float("nan")

def object_threshold(b0: np.ndarray, b1: np.ndarray, tol: float = 1e-12) -> float:
    """Interpolation des objets (1 - tau) b0 + tau b1 (équation fonctionnelle conservée) : premier tau où RH tombe."""
    rh = lambda t: off_circle((1 - t) * b0 + t * b1) == 0
    ts = np.linspace(0, 1, 401); bad = [t for t in ts if not rh(t)]
    if not bad: return float("nan")
    hi = bad[0]; lo = ts[max(np.searchsorted(ts, hi) - 1, 0)]
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if rh(mid): lo = mid
        else: hi = mid
    return hi

# ---------------------------------------------------------------- produit d'Euler (comptages réels) au point de sortie
def euler_counts(b: np.ndarray, q: int, D: int = 200) -> np.ndarray:
    """a_1..a_D (réels) pour des données normalisées b : N_n = q^n + 1 - q^(n/2) p_n, puis Möbius."""
    p = power_sums_b(b, D + 1)
    N = [q ** n + 1 - q ** (n / 2) * p[n] for n in range(1, D + 1)]
    def mu(n):
        r, k, m = 1, 2, n
        while k * k <= m:
            if m % k == 0:
                m //= k
                if m % k == 0: return 0
                r = -r
            k += 1
        return -r if m > 1 else r
    return np.array([sum(mu(d // e) * N[e - 1] for e in range(1, d + 1) if d % e == 0) / d for d in range(1, D + 1)])
