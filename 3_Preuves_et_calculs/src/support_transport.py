"""Exact polar constructor and support transport, V6.50.

Analytic operator: T_r = D_r P_r P_1^{-1}, with P_r = d²/dx²-r²/4.
This module exposes algebra and reproducible polynomial seeds. It does not
certify the sign of the Weil form, nor arbitrary supplied function domains.
The proofs and domains are in V650_RECUPERATION_TRANSPORT_ET_RH.md.
"""
from fractions import Fraction as F


def positive_rational(value):
    if isinstance(value, bool):
        raise ValueError('a positive rational parameter is required')
    value = F(value)
    if value <= 0:
        raise ValueError('a positive rational parameter is required')
    return value


def differentiate(coefficients, order=1):
    """Ascending coefficients; differentiation uses exact rational arithmetic."""
    if not isinstance(order, int) or order < 0:
        raise ValueError('nonnegative integer derivative order required')
    result = [F(v) for v in coefficients]
    for _ in range(order):
        result = [j * result[j] for j in range(1, len(result))] or [F(0)]
    return result


def apply_polar_constructor(seed_coefficients, rate=1):
    """Return exact coefficients of P_rate k on the seed support.

    The compact seed must satisfy k=k'=0 at both edges for the distributional
    constructor to have no delta terms. The caller owns that premise.
    """
    rate = positive_rational(rate)
    k = [F(v) for v in seed_coefficients]
    second = differentiate(k, 2)
    second += [F(0)] * (len(k) - len(second))
    return [v - rate * rate * c / 4 for v, c in zip(second, k)]


def evaluate(coefficients, x):
    result = 0
    for c in reversed(coefficients):
        result = result * x + c
    return result


def transported_seed_coefficients(seed_coefficients, ratio):
    """Coefficients inside T_r(P_1 k)(x)=r^-1/2 (P_r k)(x/r).

    The returned coefficients omit the single prefactor r^-1/2. They apply
    only on [-r*S,r*S]; support must accompany them.
    """
    ratio = positive_rational(ratio)
    return [c / ratio**j for j, c in enumerate(
        apply_polar_constructor(seed_coefficients, ratio))]


def fourier_weight(frequency, ratio):
    """w_r(t)=(t²+r²/4)/(t²+1/4), before the dilation."""
    ratio = positive_rational(ratio)
    return (frequency * frequency + ratio * ratio / 4) / (
        frequency * frequency + F(1, 4))


def transport_bounds(ratio):
    """Exact mass and R=mass+arch_energy equivalence constants.

    These bound norms of T_r on the stated polar domain. They are not lower
    bounds on Q_W(T_r f).
    """
    ratio = positive_rational(ratio)
    return {
        'ratio': str(ratio),
        'mass_lower': str(min(F(1), ratio**4)),
        'mass_upper': str(max(F(1), ratio**4)),
        'R_lower': str(min(ratio**4, ratio**-2)),
        'R_upper': str(max(ratio**4, ratio**-2)),
        'domain': 'L2 compact support, both exponential moments zero; finite R for R bounds',
        'preserves_polar_moments': True,
        'group_law': 'T_r T_s = T_(r*s)',
        'sign_preserved': False,
        'global_RH_claim': False,
    }


def phase_translation_modulus_bound(delta, cutoff, a_cutoff_lower):
    """Conditional analytic bound for a shifted cosine in the R norm.

    Requires an independently certified lower bound a(T)>=a_cutoff_lower
    and monotonicity of a on [0,infinity). Does not authenticate that input.
    """
    delta, cutoff, a_cutoff_lower = map(F, (delta, cutoff, a_cutoff_lower))
    if delta < 0 or cutoff <= 0 or a_cutoff_lower < 0:
        raise ValueError('nonnegative shift, positive cutoff, nonnegative a required')
    return {
        'bound': str(max(delta * cutoff, 2 / (1 + a_cutoff_lower))),
        'premises_authenticated': False,
        'meaning': 'absolute cosine-difference form <= bound * R(f)',
        'global_RH_claim': False,
    }
