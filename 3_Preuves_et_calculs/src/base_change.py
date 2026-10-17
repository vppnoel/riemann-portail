"""V6.10, suite 2 — La base comme pas de temps.

Une courbe sur F_q vue sur F_q² : N_n(F_q²) = N_2n(F_q), donc les traces normalisées deviennent p'_n = p_2n et
les valeurs propres beta deviennent beta² (P_q²(u²) = P(u) P(-u)). Le pas d'échantillonnage du flot passe de log q
à 2 log q ; le générateur D = log_q F ne change pas, mais il n'est plus vu qu'à pi i / log q près (repliement).
Ce que la base q² efface : le signe de chaque paire de valeurs propres. Les « descentes » possibles sont les choix de
signes qui redonnent un polynôme de Weil réel à coefficients entiers h(x) = prod (x - a_j), a_j = alpha_j + q/alpha_j ;
la courbe (signes vrais) et sa tordue quadratique (tous les signes changés : h(-x)) en font toujours partie.
"""
from __future__ import annotations
import itertools, math
import numpy as np
from frobenius_chain import traces_from_b, distinct

def gns_from_traces(p: np.ndarray, tol: float = 1e-9):
    """Faisceau de Toeplitz sur une suite de traces réelles p_0..p_{L+1} : (rang, valeurs propres, valeurs propres du Gram)."""
    L = len(p) - 2; idx = np.arange(L); G = p[np.abs(idx[None, :] - idx[:, None])]
    ev = np.linalg.eigvalsh(G); r = int(np.sum(np.abs(ev) > tol * np.max(np.abs(ev))))
    i = np.arange(r); S = p[np.abs(i[None, :] + 1 - i[:, None])]
    return r, np.linalg.eigvals(np.linalg.solve(G[:r, :r], S)), ev

def base_q2_traces(b: np.ndarray, L: int) -> np.ndarray:
    """Traces normalisées vues sur F_q² : p'_n = p_2n, n = 0..L-1."""
    return traces_from_b(b, 2 * L)[::2][:L]

def real_weil(c: list[int], q: int) -> np.ndarray:
    """a_j = alpha_j + q / alpha_j (une valeur par paire conjuguée), triés."""
    alpha = 1 / np.roots(np.asarray(c[::-1], dtype=float)) if len(c) > 1 else np.array([])
    a = np.sort((alpha + q / alpha).real)
    return a[::2]                                        # chaque a apparaît pour alpha et pour alpha barre

def descents(a: np.ndarray, q: int, tol: float = 1e-5) -> list[tuple[int, ...]]:
    """Polynômes de Weil réels entiers h(x) = prod (x - s_j |a_j|) qui ont la même image sur F_q² (a² - 2q)."""
    m = np.abs(a); out = set()
    for s in itertools.product((1, -1), repeat=len(a)):
        h = np.poly(np.array(s) * m)
        if np.all(np.abs(h - np.round(h)) < tol * np.maximum(1, np.abs(h))):
            out.add(tuple(int(x) for x in np.round(h)))
    return sorted(out)

def h_of(a: np.ndarray) -> tuple[int, ...]:
    return tuple(int(x) for x in np.round(np.poly(a)))

def descents_by_factors(h: tuple[int, ...]) -> tuple[int, int]:
    """(nombre de facteurs irréductibles distincts de h sur Z, nombre de polynômes prod f_i(±x) unitaires distincts).
    Explication attendue des descentes : la base q² efface un signe par facteur irréductible."""
    import sympy as sp
    x = sp.symbols("x"); H = sp.Poly(list(h), x)
    facs = []
    for f, e in sp.factor_list(H.as_expr())[1]:
        facs += [sp.Poly(f, x)] * e
    out = set()
    for s in itertools.product((1, -1), repeat=len(facs)):
        prod = sp.Poly(1, x)
        for f, si in zip(facs, s):
            g = sp.Poly(f.as_expr().subs(x, si * x), x); g = g * sp.sign(g.LC())
            prod = prod * g
        out.add(tuple(int(cf) for cf in prod.all_coeffs()))
    return len({tuple(f.all_coeffs()) for f in facs}), len(out)
