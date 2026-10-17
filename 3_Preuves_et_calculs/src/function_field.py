"""V6.6 — Le Modèle réduit : courbes hyperelliptiques sur un corps fini, où RH est un théorème (Weil, 1948).

Courbe C : y^2 = f(x), f de degré 2g + 1 sans facteur carré sur F_q (q premier impair), genre g, un point à l'infini.
N_n = #C(F_{q^n}) = q^n + 1 - S_n,  S_n = somme des alpha_i^n,  P(u) = prod_{i=1}^{2g} (1 - alpha_i u).
Équation fonctionnelle : P(u) = q^g u^{2g} P(1/(q u)).  RH (théorème) : |alpha_i| = sqrt(q).
Produit d'Euler : Z(u) = P(u)/((1-u)(1-qu)) = prod_d (1 - u^d)^(-a_d), a_d = nombre de points fermés de degré d (>= 0).
Positivité de Castelnuovo sur la surface C x C (graphe du Frobenius F^n et diagonale) :
    Q_n(r, s) = g r^2 - (N_n - q^n - 1) r s + g q^n s^2 >= 0  pour tous r, s   <=>   |S_n| <= 2 g q^(n/2).
Pour tout n : c'est ce qui rend RH nécessaire (et, réciproquement, RH l'implique).
"""
from __future__ import annotations
import math, random
import numpy as np

# ---------------------------------------------------------------- corps F_{q^n} par tables de logarithmes
class FiniteField:
    def __init__(self, q: int, n: int, seed: int = 0):
        self.q, self.n, self.Q = q, n, q ** n
        rng = random.Random(seed)
        self.pow_q = np.array([q ** k for k in range(n)], dtype=np.int64)
        while True:                                   # polynôme primitif : x engendre le groupe multiplicatif
            mod = [rng.randrange(q) for _ in range(n)]  # x^n = -(mod[0] + mod[1] x + ...) ; terme constant non nul
            if mod[0] == 0: continue
            exp = self._try(mod)
            if exp is not None: break
        self.mod = mod; self.exp = exp
        self.log = np.full(self.Q, -1, dtype=np.int64); self.log[exp] = np.arange(self.Q - 1)
        self.digits = np.array([[(c // q ** k) % q for k in range(n)] for c in range(self.Q)], dtype=np.int64)

    def _try(self, mod):
        q, n, Q = self.q, self.n, self.Q
        v = [0] * n; v[0] = 1; codes = np.empty(Q - 1, dtype=np.int64)
        for k in range(Q - 1):
            codes[k] = sum(c * q ** i for i, c in enumerate(v))
            if k > 0 and codes[k] == 1: return None   # ordre trop petit
            top = v[-1]; v = [0] + v[:-1]                # multiplication par x
            if top: v = [(v[i] - top * mod[i]) % q for i in range(n)]
        return codes if sum(c * q ** i for i, c in enumerate(v)) == 1 else None

    def mul(self, a, b):
        a = np.asarray(a); b = np.asarray(b); out = np.zeros(np.broadcast(a, b).shape, dtype=np.int64)
        nz = (a != 0) & (b != 0)
        la = np.broadcast_to(self.log[a], out.shape)[nz]; lb = np.broadcast_to(self.log[b], out.shape)[nz]
        out[nz] = self.exp[(la + lb) % (self.Q - 1)]; return out

    def add_const(self, a, c: int):
        d0 = self.digits[a, 0]; return a + ((d0 + c) % self.q - d0)

    def quad_char(self, a):
        a = np.asarray(a); out = np.zeros(a.shape, dtype=np.int64); nz = a != 0
        out[nz] = np.where(self.log[a[nz]] % 2 == 0, 1, -1); return out

_FIELDS: dict = {}
def field(q: int, n: int) -> FiniteField:
    if (q, n) not in _FIELDS: _FIELDS[(q, n)] = FiniteField(q, n)
    return _FIELDS[(q, n)]

def count_points(f: list[int], q: int, n: int) -> int:
    """#C(F_{q^n}) pour y^2 = f(x), f à coefficients dans F_q (du plus haut degré au plus bas), degré impair."""
    F = field(q, n); x = np.arange(F.Q, dtype=np.int64)
    acc = np.zeros(F.Q, dtype=np.int64)
    for c in f:                                       # Horner
        acc = F.add_const(F.mul(acc, x), c % q)
    return int(F.Q + np.sum(F.quad_char(acc))) + 1    # affine : somme (1 + chi(f(x))) ; plus un point à l'infini

# ---------------------------------------------------------------- polynômes sur F_q (sans facteur carré)
def _polymod(a, b, q):
    a = a[:]
    while len(a) >= len(b) and any(a):
        if a[0] == 0: a.pop(0); continue
        c = a[0] * pow(b[0], q - 2, q) % q
        for i in range(len(b)): a[i] = (a[i] - c * b[i]) % q
        a.pop(0)
    while a and a[0] == 0: a.pop(0)
    return a
def squarefree(f, q):
    d = len(f) - 1; df = [(c * (d - i)) % q for i, c in enumerate(f[:-1])]
    while df and df[0] == 0: df.pop(0)
    if not df: return False
    a, b = f[:], df
    while b: a, b = b, _polymod(a, b, q)
    return len(a) == 1

def random_curve(q: int, g: int, rng: random.Random) -> list[int]:
    while True:
        f = [1] + [rng.randrange(q) for _ in range(2 * g + 1)]
        if squarefree(f, q): return f

# ---------------------------------------------------------------- fonction zêta à partir des comptages
def L_polynomial(N: list[int], q: int, g: int) -> list[int]:
    """Coefficients entiers c_0..c_{2g} de P(u) à partir de N_1..N_g (identités de Newton + équation fonctionnelle)."""
    S = [None] + [q ** n + 1 - N[n - 1] for n in range(1, g + 1)]
    e = [1]                                           # P(u) = sum (-1)^k e_k u^k, e_k fonctions symétriques élémentaires
    for k in range(1, g + 1):
        s = sum((-1) ** (i - 1) * e[k - i] * S[i] for i in range(1, k + 1))
        assert s % k == 0; e.append(s // k)
    c = [(-1) ** k * e[k] for k in range(g + 1)]
    return c + [q ** (g - k) * c[k] for k in range(g - 1, -1, -1)]

def power_sums(c: list[int], nmax: int) -> list[int]:
    """S_1..S_nmax (entiers exacts) des racines inverses alpha_i de P(u) = sum c_k u^k (identités de Newton)."""
    m = len(c) - 1; e = [(-1) ** k * c[k] for k in range(m + 1)]; S = [m]
    for n in range(1, nmax + 1):
        s = sum((-1) ** (i - 1) * e[i] * S[n - i] for i in range(1, min(n - 1, m) + 1))
        if n <= m: s += (-1) ** (n - 1) * n * e[n]
        S.append(s)
    return S[1:]

def closed_points(S: list[int], q: int) -> list[int]:
    """a_1..a_D : nombre de points fermés de chaque degré (formule de Möbius), entiers exacts."""
    def mu(n):
        r, p, m = 1, 2, n
        while p * p <= m:
            if m % p == 0:
                m //= p
                if m % p == 0: return 0
                r = -r
            p += 1
        return -r if m > 1 else r
    N = [q ** n + 1 - S[n - 1] for n in range(1, len(S) + 1)]
    out = []
    for d in range(1, len(S) + 1):
        t = sum(mu(d // e) * N[e - 1] for e in range(1, d + 1) if d % e == 0)
        assert t % d == 0; out.append(t // d)
    return out

def roots_alpha(c: list[int]) -> np.ndarray:
    """Racines inverses alpha_i (P(u) = prod (1 - alpha_i u))."""
    return 1.0 / np.roots(np.array(c[::-1], dtype=float))

def castelnuovo_ratio(S: list[int], q: int, g: int) -> np.ndarray:
    """rho_n = |S_n| / (2 g q^(n/2)) ; Q_n >= 0 <=> rho_n <= 1."""
    n = np.arange(1, len(S) + 1, dtype=float)
    return np.array([abs(float(s)) for s in S]) / (2 * g * q ** (n / 2))

def angles(c: list[int], q: int) -> np.ndarray:
    """Angles phi_j dans [0, pi] des racines alpha = sqrt(q) e^{+-i phi} (une par paire conjuguée)."""
    a = roots_alpha(c) / math.sqrt(q); ph = np.sort(np.abs(np.angle(a)))
    return ph[::2] if len(ph) % 2 == 0 else ph   # chaque angle apparaît deux fois (alpha et son conjugué)

def survival_margin(phi: np.ndarray) -> tuple[float, float, float]:
    """H(w) = prod (w - 2 cos phi_j). Intervalle [e_-, e_+] des eps pour lesquels H + eps garde ses g racines réelles
    dans [-2, 2] (perturbation de la forme symétrique de P qui conserve l'équation fonctionnelle).
    Renvoie (e_-, e_+, max |H| sur [-2, 2])."""
    y = 2 * np.cos(phi); H = np.poly(y)
    ok = lambda e: (lambda r: np.all(np.abs(r.imag) < 1e-7) and np.all(np.abs(r.real) <= 2 + 1e-9))(np.roots(H + np.r_[np.zeros(len(H) - 1), e]))
    w = np.linspace(-2, 2, 4001); scale = float(np.max(np.abs(np.polyval(H, w))))
    def edge(sign):
        lo, hi = 0.0, scale
        if ok(sign * hi): return sign * hi
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if ok(sign * mid): lo = mid
            else: hi = mid
        return sign * lo
    return edge(-1), edge(+1), scale
