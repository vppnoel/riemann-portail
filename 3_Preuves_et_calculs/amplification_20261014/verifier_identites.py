#!/usr/bin/env python3
"""Independent Decimal diagnostics for the exact quadratic amplifier.

The algebraic proofs are in the accompanying note. Decimal residuals are
numerical diagnostics, not interval certificates or estimates at infinity.
Only the Python standard library is required.
"""
from __future__ import annotations

import argparse
import bisect
import csv
import json
import math
from decimal import Decimal, getcontext
from pathlib import Path

GAMMA_TEXT = (
    "0.577215664901532860606512090082402431042159335939923598805767234884867726"
    "7776646709369470632917467495"
)


def jacobi(a: int, n: int) -> int:
    if n <= 0 or n % 2 == 0:
        raise ValueError("The denominator must be a positive odd integer")
    if n == 1:
        return 1
    a %= n
    value = 1
    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                value = -value
        a, n = n, a
        if a % 4 == n % 4 == 3:
            value = -value
        a %= n
    return value if n == 1 else 0


def mobius_sieve(limit: int):
    mu = [0] * (limit + 1)
    mu[1] = 1
    smallest = [0] * (limit + 1)
    primes = []
    for n in range(2, limit + 1):
        if smallest[n] == 0:
            smallest[n] = n
            primes.append(n)
            mu[n] = -1
        for p in primes:
            if p * n > limit:
                break
            smallest[p * n] = p
            if n % p == 0:
                mu[p * n] = 0
                break
            mu[p * n] = -mu[n]
    return mu, primes


def prime_sieve(limit: int):
    mask = bytearray(b"\1") * (limit + 1)
    mask[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if mask[p]:
            mask[p * p::p] = b"\0" * ((limit - p * p) // p + 1)
    return [n for n in range(2, limit + 1) if mask[n]]


class Arithmetic:
    def __init__(self, limit: int):
        self.mu, primes = mobius_sieve(limit)
        self.gamma = Decimal(GAMMA_TEXT)
        self.c = 1 + self.gamma
        self.logfac = [Decimal(0)] * (limit + 1)
        self.harmonic = [Decimal(0)] * (limit + 1)
        for n in range(1, limit + 1):
            self.logfac[n] = self.logfac[n - 1] + Decimal(n).ln()
            self.harmonic[n] = self.harmonic[n - 1] + Decimal(1) / n
        lambdas = [Decimal(0)] * (limit + 1)
        for p in primes:
            power = p
            while power <= limit:
                lambdas[power] = Decimal(p).ln()
                power *= p
        self.psi = [Decimal(0)] * (limit + 1)
        for n in range(1, limit + 1):
            self.psi[n] = self.psi[n - 1] + lambdas[n]

    def B(self, x: Decimal) -> Decimal:
        if x < 1:
            return Decimal(0)
        n = int(x)
        return self.logfac[n] - x * self.harmonic[n] + self.c * n

    def A_direct(self, x: Decimal) -> Decimal:
        return self.psi[int(x)] - x + self.c if x >= 1 else Decimal(0)

    def A_mobius(self, x: Decimal, odd_only=False) -> Decimal:
        return sum((self.mu[n] * self.B(x / n)
                    for n in range(1, int(x) + 1)
                    if self.mu[n] and (not odd_only or n % 2)), Decimal(0))

    def F(self, u: int, x: Decimal) -> Decimal:
        return sum((self.mu[n] * jacobi(u, n) * self.B(x / n)
                    for n in range(1, int(x) + 1, 2) if self.mu[n]), Decimal(0))


def run(output: Path, precision: int):
    getcontext().prec = precision
    output.mkdir(parents=True, exist_ok=True)
    arithmetic = Arithmetic(1000)
    checks = []
    for value in ["1", "1.4", "2.7", "10.3", "31.25", "100.75", "257.125"]:
        x = Decimal(value)
        a = arithmetic.A_direct(x)
        ao = arithmetic.A_mobius(x, odd_only=True)
        forward = sum((arithmetic.A_direct(x / k)
                       for k in range(1, int(x) + 1)), Decimal(0))
        errors = {
            "divisor_forward": abs(forward - arithmetic.B(x)),
            "mobius_inverse": abs(a - arithmetic.A_mobius(x)),
            "remove_two": abs(a - ao + arithmetic.A_mobius(x / 2, odd_only=True)),
        }
        for p in [3, 5, 11, 17]:
            errors[f"square_copy_p{p}"] = abs(
                ao - arithmetic.F(p * p, x) + arithmetic.F(p * p, x / p)
            )
        checks.append({"x": value, "residuals": {k: str(v) for k, v in errors.items()}})
    max_error = max(Decimal(v) for row in checks for v in row["residuals"].values())
    if max_error > Decimal(10) ** (-precision + 12):
        raise ArithmeticError(f"Identity diagnostic residual too large: {max_error}")

    # A genuinely independent reindexing of the expanded family mean.
    x, h = Decimal("31.25"), 31
    ids = [n for n in range(1, int(x) + 1, 2) if arithmetic.mu[n]]
    b = {n: arithmetic.B(x / n) for n in ids}
    direct_mean = sum((arithmetic.F(u, x) ** 2 for u in range(1, h + 1)), Decimal(0))
    groups = {}
    character_cache = {}
    for n in ids:
        for m in ids:
            g = math.gcd(n, m)
            a, bb = n // g, m // g
            q = a * bb
            assert math.gcd(g, q) == 1
            assert arithmetic.mu[n] * arithmetic.mu[m] == arithmetic.mu[q]
            key = q, g
            if key not in character_cache:
                character_cache[key] = sum(jacobi(u, q) for u in range(1, h + 1)
                                           if math.gcd(u, g) == 1)
            term = arithmetic.mu[q] * b[n] * b[m] * character_cache[key]
            groups[q] = groups.get(q, Decimal(0)) + term
    grouped_mean = sum(groups.values(), Decimal(0))
    diag = sum((b[n] ** 2 * sum(jacobi(u, n) ** 2 for u in range(1, h + 1))
                for n in ids), Decimal(0))
    group_error = abs(grouped_mean - direct_mean)
    assert group_error < Decimal(10) ** (-precision + 12)
    assert abs(groups[1] - diag) < Decimal(10) ** (-precision + 12)
    with (output / "conducteurs_point.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["q", "mobius_q", "contribution_signee"])
        writer.writerows((q, arithmetic.mu[q], str(groups[q])) for q in sorted(groups))

    # Independent integration: recompute each affine coefficient from B itself,
    # rather than updating jumps as calcul_famille.py does.
    integrated_checks = []
    integrated_groups = {}
    for ceiling in [31, 100]:
        columns = [n for n in range(1, ceiling + 1, 2) if arithmetic.mu[n]]
        chars = {(u, n): jacobi(u, n)
                 for u in range(1, ceiling + 1) for n in columns}
        q_energy, d_energy = Decimal(0), Decimal(0)
        for j in range(1, ceiling):
            active = [n for n in columns if n <= j]
            bv = {n: arithmetic.B(Decimal(j) / n) for n in active}
            sv = {n: -arithmetic.harmonic[j // n] / n for n in active}
            for u in range(1, ceiling + 1):
                value = sum((arithmetic.mu[n] * chars[u, n] * bv[n]
                             for n in active), Decimal(0))
                slope = sum((arithmetic.mu[n] * chars[u, n] * sv[n]
                             for n in active), Decimal(0))
                q_energy += value ** 2 + value * slope + slope ** 2 / 3
            for n in active:
                multiplicity = sum(chars[u, n] ** 2 for u in range(1, ceiling + 1))
                d_energy += multiplicity * (bv[n] ** 2 + bv[n] * sv[n] + sv[n] ** 2 / 3)
            if ceiling == 31:
                for n in active:
                    for m in active:
                        g = math.gcd(n, m)
                        conductor = (n // g) * (m // g)
                        char_sum = sum(jacobi(u, conductor) for u in range(1, ceiling + 1)
                                       if math.gcd(u, g) == 1)
                        kernel_piece = (bv[n] * bv[m]
                                        + (bv[n] * sv[m] + bv[m] * sv[n]) / 2
                                        + sv[n] * sv[m] / 3)
                        integrated_groups[conductor] = integrated_groups.get(conductor, Decimal(0)) + (
                            arithmetic.mu[conductor] * char_sum * kernel_piece)
        item = {"X": ceiling, "H": ceiling,
                "Q_decimal": str(q_energy), "D_decimal": str(d_energy),
                "R_decimal": str(q_energy - d_energy)}
        if ceiling == 31:
            regrouped = sum(integrated_groups.values(), Decimal(0))
            assert abs(regrouped - q_energy) < Decimal(10) ** (-precision + 12)
            item.update({
                "grouping_residual": str(abs(regrouped - q_energy)),
                "R_q_le_X": str(sum((v for q, v in integrated_groups.items() if 1 < q <= ceiling), Decimal(0))),
                "R_q_gt_X": str(sum((v for q, v in integrated_groups.items() if q > ceiling), Decimal(0))),
            })
        integrated_checks.append(item)
    with (output / "conducteurs_energie_X31.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["q", "mobius_q", "contribution_signee_integree"])
        writer.writerows((q, arithmetic.mu[q], str(integrated_groups[q])) for q in sorted(integrated_groups))

    # Universal obstruction: coefficients mu(n) on a prime-only support.
    # Every square row u=s^2, s<=sqrt(D), is the SAME row on these primes.
    prime_list = prime_sieve(1_000_000)
    counterexamples = []
    for d in [100, 1000, 10_000, 100_000, 1_000_000]:
        count = bisect.bisect_right(prime_list, d) - bisect.bisect_right(prime_list, d // 2)
        copies = math.isqrt(d)
        assert d / 2 > math.sqrt(d)
        lower = copies * count ** 2
        counterexamples.append({
            "D": d, "H": d, "prime_support_size": count,
            "exact_square_rows": copies, "exact_square_energy": lower,
            "square_energy_over_primitive_scale": lower / (2 * d * count),
        })

    report = {
        "status": "diagnostics_only_no_infinite_bound",
        "precision_decimal_digits": precision,
        "gamma_input_digits": len(GAMMA_TEXT) - 2,
        "identity_max_absolute_residual": str(max_error),
        "identity_checks": checks,
        "conductor_reindexing": {
            "x": str(x), "H": h, "direct_mean": str(direct_mean),
            "grouped_mean": str(grouped_mean), "absolute_residual": str(group_error),
            "diagonal_q1": str(diag),
            "signed_debt_q_gt_1": str(grouped_mean - diag),
            "different_q_group_signs": sorted({int(v.compare(Decimal(0)))
                                                for q, v in groups.items() if q > 1}),
        },
        "independent_affine_integrals": integrated_checks,
        "universal_countermodel": counterexamples,
        "warning": "The countermodel uses a prime-only mask, not the exact B weight; it refutes a coefficient-blind estimate, not the special estimate for B.",
    }
    path = output / "verification_decimale.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"saved": str(path), "identity_max_residual": str(max_error),
                      "grouping_residual": str(group_error),
                      "countermodel_ratios": [r["square_energy_over_primitive_scale"] for r in counterexamples]},
                     ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument("--precision", type=int, default=70)
    args = parser.parse_args()
    run(args.output, args.precision)
