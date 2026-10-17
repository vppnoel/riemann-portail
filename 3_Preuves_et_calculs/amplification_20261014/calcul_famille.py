#!/usr/bin/env python3
"""Diagnostic fini de l'amplification quadratique, avec le poids B exact.

F_u(x) = sum_{n impair, n <= x} mu(n) (u/n) B(x/n),
B(t) = log(floor(t)!) - t H_floor(t) + (1 + gamma) floor(t).

Sur chaque intervalle entier [j, j+1), F_u est affine. Son integral
quadratique est donc evaluee par sa primitive polynomiale, sans quadrature.
Les coefficients sont calcules en virgule flottante double : ces nombres
ne sont ni des certificats par intervalles, ni une borne pour X infini.

Usage : python calcul_famille.py --ceilings 100 300 1000
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


GAMMA = 0.5772156649015328606


def sieve(limit: int) -> tuple[list[int], list[int]]:
    """Smallest prime factors and exact integer Mobius coefficients."""
    spf = list(range(limit + 1))
    mu = [1] * (limit + 1)
    mu[0] = 0
    for p in range(2, limit + 1):
        if spf[p] != p:
            continue
        for n in range(p, limit + 1, p):
            if spf[n] == n:
                spf[n] = p
            mu[n] *= -1
        for n in range(p * p, limit + 1, p * p):
            mu[n] = 0
    return spf, mu


def family_diagnostic(ceiling: int) -> dict:
    """Compute Q_H(X), its weighted diagonal and crossed remainder, H=X."""
    x_max = h_max = ceiling
    spf, mu = sieve(x_max)
    ns = np.array([n for n in range(1, x_max + 1, 2) if mu[n]], dtype=int)
    column_of = {int(n): i for i, n in enumerate(ns)}
    us = np.arange(1, h_max + 1)

    # Product of Legendre symbols at the distinct odd prime factors of n.
    # Only odd squarefree denominators appear, so this is the Jacobi symbol.
    chi = np.ones((h_max, len(ns)), dtype=np.int8)
    for i, n in enumerate(ns):
        remaining = int(n)
        while remaining > 1:
            p = spf[remaining]
            quadratic_residues = {a * a % p for a in range(1, p)}
            legendre = np.array(
                [0 if r == 0 else 1 if r in quadratic_residues else -1
                 for r in us % p],
                dtype=np.int8,
            )
            chi[:, i] *= legendre
            remaining //= p
    coefficients = chi * np.array([mu[int(n)] for n in ns], dtype=np.int8)

    harmonics = np.zeros(x_max + 1)
    log_factorials = np.zeros(x_max + 1)
    for j in range(1, x_max + 1):
        harmonics[j] = harmonics[j - 1] + 1 / j
        log_factorials[j] = log_factorials[j - 1] + math.log(j)

    values = np.zeros(h_max)
    slopes = np.zeros(h_max)
    row_energies = np.zeros(h_max)
    basis_energies = np.zeros(len(ns))

    for j in range(1, x_max):
        divisors = [int(n) for n in ns if j % int(n) == 0]
        ids = [column_of[n] for n in divisors]

        # At x=j, B(x/n) jumps by log(j/n)+gamma when n divides j.
        # The derivative jumps by -1/j for each of those divisors.
        jumps = np.array([math.log(j / n) + GAMMA for n in divisors])
        values += coefficients[:, ids] @ jumps
        slopes -= coefficients[:, ids].sum(axis=1) / j

        # Integral_0^1 (v + s*t)^2 dt, exact polynomial formula.
        row_energies += values * values + values * slopes + slopes * slopes / 3

        active = ns <= j
        denominators = ns[active]
        floors = j // denominators
        b = (log_factorials[floors]
             - (j / denominators) * harmonics[floors]
             + (1 + GAMMA) * floors)
        b_slope = -harmonics[floors] / denominators
        basis_energies[active] += b * b + b * b_slope + b_slope * b_slope / 3
        values += slopes

    # chi(u,n)^2 = 1_(u,n)=1; mu(n)^2=1 on retained columns.
    coprime_row_counts = (chi * chi).sum(axis=0)
    diagonal = float(coprime_row_counts @ basis_energies)
    total = float(row_energies.sum())
    crossed = total - diagonal
    square_copy_primes = [
        p for p in range(3, math.isqrt(h_max) + 1)
        if spf[p] == p and p > math.sqrt(h_max) / 2
    ]
    copied_energy = sum(float(row_energies[p * p - 1]) for p in square_copy_primes)
    copy_count = len(square_copy_primes)
    scale = h_max * x_max * x_max
    return {
        "X": x_max,
        "H": h_max,
        "odd_squarefree_columns": int(len(ns)),
        "Q_family": total,
        "D_weighted_diagonal": diagonal,
        "R_crossed_signed": crossed,
        "Q_over_HX2": total / scale,
        "D_over_HX2": diagonal / scale,
        "R_over_HX2": crossed / scale,
        "J_odd_target_over_X2": float(row_energies[0]) / (x_max * x_max),
        "square_copy_primes": square_copy_primes,
        "square_copy_count": copy_count,
        "copied_energy_over_MX2": (
            copied_energy / (copy_count * x_max * x_max) if copy_count else None
        ),
        "rounding_certified": False,
        "infinite_bound_proved": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ceilings", nargs="+", type=int, default=[100, 300, 1000])
    parser.add_argument(
        "--output", type=Path,
        default=Path(__file__).resolve().parent / "results" / "famille_diagnostic.json",
    )
    args = parser.parse_args()
    if any(x < 2 or x > 5000 for x in args.ceilings):
        parser.error("Each ceiling must lie between 2 and 5000 (finite diagnostic).")
    payload = {
        "method": "Exact affine integration on integer intervals; double precision coefficients",
        "family": "F_u(x)=sum_(n odd <=x) mu(n) Jacobi(u,n) B(x/n)",
        "normalization": "Q_H(X)=sum_(1<=u<=H) integral_1^X |F_u(x)|^2 dx; H=X",
        "status": "Finite diagnostic only; no interval certificate or infinite estimate",
        "results": [family_diagnostic(x) for x in args.ceilings],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in payload["results"]:
        print(f"X=H={row['X']}: Q/(HX^2)={row['Q_over_HX2']:.12g}; "
              f"D/(HX^2)={row['D_over_HX2']:.12g}; "
              f"R/(HX^2)={row['R_over_HX2']:.12g}")
    print(f"Results: {args.output}")


if __name__ == "__main__":
    main()
