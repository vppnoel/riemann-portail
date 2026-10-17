"""Quantile-shadow sweep, source is the actual beta density plus its atom at 0.

This is a finite numerical diagnostic.  Exact formulas and the proof are in
constructive_report.md.  Source pieces are represented in original source-mass
coordinates; no density has been replaced by point masses.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import polygamma

OUT = Path(__file__).resolve().parent
X = 1000
T = math.log(2)
C0 = math.log(8 * math.pi) + np.euler_gamma + math.pi / 2
lam = 2 * np.arange(100) + 0.5
ACONST = float(polygamma(1, 0.25)) / 4


def A(t):
    return (4 * (math.exp(t / 2) + math.exp(-t / 2) - 2)
            - C0 * t / 2 + ACONST - float(np.sum(np.exp(-lam * t) / lam**2)))


def Ap(t):
    return (2 * (math.exp(t / 2) - math.exp(-t / 2))
            - C0 / 2 + float(np.sum(np.exp(-lam * t) / lam)))


AT, APT = A(T), Ap(T)
m = AT / T
a = APT - math.log(2) / math.sqrt(2)
mu_T, nu_T = max(a - m, 0), max(m - a, 0)


def M(u):
    """Source mass through u>=T."""
    return m + mu_T + Ap(u) - APT


def H(u):
    """Source first moment through u>=T."""
    return T * mu_T + u * Ap(u) - A(u) - T * APT + AT


def G(s):
    if s <= m:
        return 0.0
    if s <= m + mu_T:
        return T
    high = max(T + 0.5, 2 * math.log(s / 2 + 3))
    while M(high) < s:
        high += 1
    return brentq(lambda u: M(u) - s, T, high, xtol=1e-13, rtol=1e-14)


def J(s):
    """Integral of the original source quantile from 0 to s."""
    if s <= m:
        return 0.0
    if s <= m + mu_T:
        return T * (s - m)
    return H(G(s))


def powers(n):
    prime = [True] * (n + 1)
    prime[0] = prime[1] = False
    for p in range(2, math.isqrt(n) + 1):
        if prime[p]:
            prime[p*p:n+1:p] = [False] * (((n - p*p) // p) + 1)
    out = []
    for p in range(2, n + 1):
        if prime[p]:
            q = p
            while q <= n:
                out.append((q, p))
                q *= p
    return sorted(out)


pp = powers(X)
C = sum(math.log(p) / math.sqrt(q) for q, p in pp)
P = sum(math.log(p) / math.sqrt(q) * math.log(q) for q, p in pp)
L = math.log(X)


def Sx(t):
    return A(t) - sum(math.log(p) / math.sqrt(q) * max(t - math.log(q), 0)
                      for q, p in pp)


SL = Sx(L)
budget = lambda U: (U - L) * Ap(U) - A(U) + A(L)
U = brentq(lambda u: budget(u) - SL, L, L + 2, xtol=1e-13)
D = Ap(U) - C
if not D > 0:
    raise RuntimeError("The finite closure has a negative boundary mass.")

# Greedy operations use only the finite source cap U.  Each source piece is an
# interval in original source-mass coordinates.  Removing a residual-quantile
# interval can cut across previously removed pieces, but never consumes twice.
remaining = [(0.0, M(U))]


def pieces(s, c):
    result = []
    rank = 0.0
    for left, right in remaining:
        length = right - left
        lo = max(0.0, s - rank)
        hi = min(length, s + c - rank)
        if hi > lo:
            result.append((left + lo, left + hi))
        rank += length
        if rank >= s + c - 1e-12:
            break
    return result


def block_moment(s, c):
    return sum(J(right) - J(left) for left, right in pieces(s, c))


def remove(block):
    global remaining
    updated = []
    for left, right in remaining:
        cursor = left
        for lo, hi in block:
            if hi <= cursor or lo >= right:
                continue
            if lo > cursor + 2e-13:
                updated.append((cursor, lo))
            cursor = max(cursor, hi)
        if right > cursor + 2e-13:
            updated.append((cursor, right))
    remaining = updated


atoms = [("T", T, nu_T)] + [(str(q), math.log(q), math.log(p)/math.sqrt(q))
                                for q, p in pp if q > 2]
atoms.append(("boundary", L, D))
rows, kernels = [], []
for label, x, c in atoms:
    available = sum(right - left for left, right in remaining)
    bmin = block_moment(0, c) / c
    bmax = block_moment(max(available - c, 0), c) / c
    if bmin > x + 2e-10 or bmax < x - 2e-10:
        raise RuntimeError(f"Greedy obstruction at {label}: {bmin} <= {x} <= {bmax}")
    if available - c < 2e-10:
        s = 0.0
    else:
        s = brentq(lambda z: block_moment(z, c) - c*x,
                   0, available - c, xtol=1e-12, rtol=1e-14)
    block = pieces(s, c)
    mass = sum(right - left for left, right in block)
    moment = sum(J(right) - J(left) for left, right in block)
    low = G(block[0][0])
    high = G(block[-1][1])
    rows.append(dict(atom=label,x=x,c=c,min_barycenter=bmin,
                     availability_slack=x-bmin,source_low=low,source_high=high,
                     width=high-low,mass_error=mass-c,moment_error=moment-c*x,
                     pieces=len(block)))
    kernels.append(dict(atom=label,x=x,c=c,source_mass_intervals=block))
    remove(block)

source_mass, demand_mass = M(U), nu_T + sum(c for _, _, c in atoms[1:])
source_moment, demand_moment = H(U), sum(x*c for _, x, c in atoms)
summary = dict(cutoff=X,prime_power_count=len(pp),actual_nu_atoms=len(atoms)-1,
               T=T,S_T=AT,m=m,a=a,nu_T=nu_T,L=L,S_L=SL,U=U,U_minus_L=U-L,
               boundary_mass=D,source_mass=source_mass,demand_mass=demand_mass,
               source_first_moment=source_moment,demand_first_moment=demand_moment,
               total_mass_error=source_mass-demand_mass,
               total_moment_error=source_moment-demand_moment,
               max_atom_mass_error=max(abs(r['mass_error']) for r in rows),
               max_atom_moment_error=max(abs(r['moment_error']) for r in rows),
               residual_source_mass=sum(r-l for l,r in remaining),
               min_availability_slack=min(r['availability_slack'] for r in rows[:-1]),
               max_kernel_width=max(r['width'] for r in rows[:-1]),
               max_actual_source=max(r['source_high'] for r in rows[:-1]))
with (OUT / "shadow_sweep_rows.csv").open("w") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
(OUT / "shadow_sweep_kernels.json").write_text(json.dumps(kernels,indent=2))
(OUT / "shadow_sweep_summary.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
print("First three allocations:")
for row in rows[:3]:
    print(row)
