"""V6.3d — Reconstruire le signal TOMO g_F(u) = e^(-u/2) C_F(e^u) à partir des zéros seuls.

Formule de Perron : C_F(x) = somme des résidus de G_F(s) x^s / s, avec
G_F = q^2 + q' (+ 2 gamma q si pôle),  q = -F'/F.
En un zéro simple rho, q = -1/(s - rho) + a_rho + ..., donc G_F a un pôle double et

    résidu = x^rho [ 2 (log x / rho - 1/rho^2) - 2 (a_rho + gamma [pôle]) / rho ].

Après lissage gaussien d'écart-type sigma en u (qui rend la somme sur les zéros absolument
convergente), le terme e^(lam u) (A u + B), lam = rho - 1/2, devient
e^(lam u + lam^2 sigma^2 / 2) (A (u + lam sigma^2) + B).

Côté coefficients, le même lissage est exact :
    g_sigma(u) = e^(-u/2 + sigma^2/8) somme_n c_F(n) PhiC((log n - u + sigma^2/2) / sigma).

Les valeurs de F sont calculées en double précision par Euler-Maclaurin (zeta de Hurwitz),
sans dépendance à mpmath. Diagnostic de cohérence : ne prouve rien sur RH.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path
import numpy as np
from scipy.special import digamma, erfc

try:
    from rejection import KAPPA_DH, EULER_GAMMA, build
    from explicit_formula import load_zeros
except ImportError:
    from .rejection import KAPPA_DH, EULER_GAMMA, build
    from .explicit_formula import load_zeros

ROOT = Path(__file__).resolve().parents[1]
_B2K = [1 / 6, -1 / 30, 1 / 42, -1 / 30, 5 / 66, -691 / 2730, 7 / 6, -3617 / 510, 43867 / 798,
        -174611 / 330, 854513 / 138, -236364091 / 2730, 8553103 / 6, -23749461029 / 870,
        8615841276005 / 14322]
_CHI = {1: 1, 2: 1j, 3: -1j, 4: -1}
# q : conducteur, par : parité du facteur gamma, pole : pôle en s = 1, dual : objet dual dans l'équation fonctionnelle
META = {"zeta": dict(q=1, par=0, pole=True, dual="zeta"),
        "L_chi5": dict(q=5, par=1, pole=False, dual="L_chi5bar"),
        "L_chi5bar": dict(q=5, par=1, pole=False, dual="L_chi5"),
        "DH": dict(q=5, par=1, pole=False, dual="DH")}


def hurwitz_zeta(s: complex, a: float) -> complex:
    """zeta(s, a) par Euler-Maclaurin (prolongement analytique inclus), s complexe != 1."""
    s = complex(s)
    M = int(abs(s)) + 25
    n = np.arange(M, dtype=float) + a
    x = M + a
    tot = np.sum(n ** (-s)) + x ** (1 - s) / (s - 1) + 0.5 * x ** (-s)
    term = s * x ** (-s - 1)          # s (M+a)^(-s-1), sera multiplié par B_2k/(2k)!
    fact = 2.0
    for k, b in enumerate(_B2K, start=1):
        tot += b / fact * term
        term *= (s + 2 * k - 1) * (s + 2 * k) / (x * x)
        fact *= (2 * k + 1) * (2 * k + 2)
    return tot


def F_eval(kind: str, s: complex) -> complex:
    if kind == "zeta":
        return hurwitz_zeta(s, 1.0)
    Lc = 5.0 ** (-complex(s)) * sum(_CHI[a] * hurwitz_zeta(s, a / 5.0) for a in _CHI)
    Lb = 5.0 ** (-complex(s)) * sum(np.conj(_CHI[a]) * hurwitz_zeta(s, a / 5.0) for a in _CHI)
    if kind == "L_chi5":
        return Lc
    if kind == "L_chi5bar":
        return Lb
    if kind == "DH":
        return 0.5 * (1 - 1j * KAPPA_DH) * Lc + 0.5 * (1 + 1j * KAPPA_DH) * Lb
    raise ValueError(kind)


def taylor(kind: str, s0: complex, r: float = 0.05, n: int = 16) -> np.ndarray:
    """Coefficients de Taylor c_0, c_1, c_2 de F en s0 (intégrale de Cauchy sur un cercle)."""
    th = 2 * math.pi * np.arange(n) / n
    vals = np.array([F_eval(kind, s0 + r * np.exp(1j * t)) for t in th])
    return np.array([np.mean(vals * np.exp(-1j * k * th)) / r ** k for k in range(3)])


def regular_part_at_zero(kind: str, rho: complex) -> tuple[complex, complex]:
    """(a_rho, |F(rho)|) avec q = -F'/F = -1/(s - rho) + a_rho + ... en un zéro simple."""
    c0, c1, c2 = taylor(kind, rho)
    return -c2 / c1, abs(c0)


def q_and_derivative(kind: str, s: complex) -> tuple[complex, complex]:
    """q(s) = -F'/F et q'(s) en un point régulier."""
    c0, c1, c2 = taylor(kind, s)
    return -c1 / c0, -(2 * c2 / c0 - (c1 / c0) ** 2)


def trivial_zero_regular_part(kind: str, rho: float) -> complex:
    """a_rho en un zéro trivial rho (entier négatif), par l'équation fonctionnelle.

    F'/F(s) = X'/X(s) - Fdual'/Fdual(1 - s),
    X'/X(s) = -log(q/pi) - psi((1 - s + par)/2)/2 - psi((s + par)/2)/2.
    """
    m = META[kind]
    k = int(round(-(rho + m["par"]) / 2))
    qd, _ = q_and_derivative(m["dual"], 1.0 - rho)          # -Fdual'/Fdual(1 - rho)
    R = -math.log(m["q"] / math.pi) - 0.5 * digamma((1 - rho + m["par"]) / 2) - 0.5 * digamma(k + 1) + qd
    return -R


def nontrivial_zeros(kind: str, extended: bool = True) -> np.ndarray:
    """Zéros non triviaux connus (complexes), des deux signes de la partie imaginaire.

    extended=True : listes V6.3d jusqu'à |t| <= 600 (complétude contrôlée par le principe de l'argument) ;
    extended=False : listes historiques (L : |t| <= 245 ; DH : t <= 200, partenaires 1 - sigma ajoutés ici).
    """
    if kind == "zeta":
        g, _ = load_zeros()
        return np.concatenate([0.5 + 1j * g, 0.5 - 1j * g])
    if kind == "L_chi5":
        name = "L_chi5_zeros_600.csv" if extended and (ROOT / "data" / "L_chi5_zeros_600.csv").exists() else "L_chi5_zeros.csv"
        rows = list(csv.DictReader(open(ROOT / "data" / name)))
        return np.array(sorted({complex(float(r["sigma"]), float(r["t"])) for r in rows}, key=lambda z: z.imag))
    if kind == "DH":
        name = "dh_zeros_600.csv" if extended and (ROOT / "data" / "dh_zeros_600.csv").exists() else "dh_zeros.csv"
        rows = list(csv.DictReader(open(ROOT / "data" / name)))
        pts = []
        for r in rows:
            z = complex(float(r["sigma"]), float(r["t"]))
            cands = [z] if abs(z.real - 0.5) < 1e-6 else [z, complex(1 - z.real, z.imag)]
            for w in cands:
                if all(abs(w - p) > 1e-4 for p in pts):
                    pts.append(w)
        return np.array(pts + [np.conj(p) for p in pts])
    raise ValueError(kind)


def zero_terms(kind: str, n_trivial: int = 14) -> dict[str, np.ndarray]:
    """Pour chaque pôle de G_F(s)/s : lam = rho - 1/2 et (A, B) tels que le terme vaut e^(lam u)(A u + B)."""
    m = META[kind]
    gp = EULER_GAMMA if m["pole"] else 0.0
    rho = nontrivial_zeros(kind)
    if kind == "zeta":                       # a_rho = -c0 déjà tabulé (data/zeros_300.csv)
        _, c0 = load_zeros()
        a = np.concatenate([-c0, -np.conj(c0)])
        resid = np.zeros(len(rho))
    else:
        pairs = [regular_part_at_zero(kind, r) for r in rho]
        a = np.array([p[0] for p in pairs]); resid = np.array([p[1] for p in pairs])
    lam = [r - 0.5 for r in rho]
    A = [2 / r for r in rho]
    B = [-2 / r ** 2 - 2 * (ar + gp) / r for r, ar in zip(rho, a)]
    family = ["sur_droite" if abs(r.real - 0.5) < 1e-6 else "hors_droite" for r in rho]
    # zéros triviaux
    first = 2 if m["par"] == 0 else 1
    for j in range(n_trivial):
        r = -float(first + 2 * j)
        ar = trivial_zero_regular_part(kind, r)
        lam.append(r - 0.5); A.append(2 / r); B.append(-2 / r ** 2 - 2 * (ar + gp) / r); family.append("trivial")
    # pôle simple de 1/s en s = 0 : résidu G_F(0)
    q0, dq0 = q_and_derivative(kind, 0.0)
    lam.append(-0.5); A.append(0.0); B.append(q0 ** 2 + dq0 + 2 * gp * q0); family.append("s=0")
    return dict(rho=rho, lam=np.array(lam, dtype=complex), A=np.array(A, dtype=complex),
                B=np.array(B, dtype=complex), family=np.array(family), residual=resid)


def g_from_zeros(terms: dict, u: np.ndarray, sigma: float, families: tuple[str, ...] | None = None) -> np.ndarray:
    """Signal lissé reconstruit à partir des pôles de G_F(s)/s (zéros de F, zéros triviaux, s = 0)."""
    u = np.asarray(u, dtype=float)
    out = np.zeros(len(u), dtype=complex)
    for lam, A, B, fam in zip(terms["lam"], terms["A"], terms["B"], terms["family"]):
        if families is not None and fam not in families:
            continue
        out += np.exp(lam * u + 0.5 * lam * lam * sigma * sigma) * (A * (u + lam * sigma * sigma) + B)
    return out


def g_from_coefficients(c: np.ndarray, u: np.ndarray, sigma: float, chunk: int = 256) -> np.ndarray:
    """Signal lissé calculé exactement à partir des coefficients c_F(n) (aucun zéro)."""
    u = np.asarray(u, dtype=float)
    N = len(c) - 1
    if math.log(N) < u.max() + 6 * sigma:
        raise ValueError("c doit couvrir n <= exp(u_max + 6 sigma)")
    n = np.arange(1, N + 1)
    ln = np.log(n.astype(float)); cn = np.asarray(c)[1:]
    out = np.zeros(len(u), dtype=complex)
    for i in range(0, len(u), chunk):
        uu = u[i:i + chunk, None]
        hi = int(min(N, math.exp(float(uu.max()) + 6 * sigma) + 2))
        z = (ln[None, :hi] - uu + 0.5 * sigma * sigma) / sigma
        out[i:i + chunk] = (0.5 * erfc(z / math.sqrt(2.0))) @ cn[:hi]
    return np.exp(-0.5 * u + sigma * sigma / 8.0) * out


def coefficients_c(kind: str, N: int) -> np.ndarray:
    return build(kind, N)[2]
