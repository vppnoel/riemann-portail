"""Exact recipes and interval enclosures for constrained odd V13.

Gauss sums use primitive root2 and the character convention of euler_archipelago.
No binary64 phase is used in a certificate. Approximate vectors are exported
only for checking the historical numerical implementation.
"""
from fractions import Fraction
from itertools import combinations
import mpmath as mp
import numpy as np

INDICES = (1, 3, 5, 7, 9, 11)
PAIRS = ((0, 5), (1, 4), (2, 3))


def lo(x):
    return mp.mpf(x._mpi_[0])


def hi(x):
    return mp.mpf(x._mpi_[1])


def contains(x, number=0):
    return lo(x) <= number <= hi(x)


def point(q):
    q = Fraction(q)
    return mp.iv.mpf(q.numerator) / q.denominator


def endpoint_fraction(endpoint):
    sign, mantissa, exponent, _ = endpoint
    numerator = (-1 if sign else 1) * mantissa
    return Fraction(numerator * (1 << exponent), 1) if exponent >= 0 else Fraction(numerator, 1 << (-exponent))


def enclosure(x, places=12):
    """Outward decimal bounds from exact binary endpoints, with no float rounding."""
    scale = 10 ** places
    low = endpoint_fraction(x._mpi_[0]) * scale
    high = endpoint_fraction(x._mpi_[1]) * scale
    floor = low.numerator // low.denominator
    ceiling = -((-high.numerator) // high.denominator)
    def fmt(integer):
        sign = '-' if integer < 0 else ''
        integer = abs(integer)
        return f'{sign}{integer // scale}.{integer % scale:0{places}d}'
    return {'lower': fmt(floor), 'upper': fmt(ceiling),
            'binary_endpoints': [list(x._mpi_[0]), list(x._mpi_[1])]}


def midpoint(x):
    return float((lo(x) + hi(x)) / 2)


def conj(z):
    # mpmath1.3.0's inherited iv.mpc.conjugate does not handle interval tuples.
    return mp.iv.mpc(z.real, -z.imag)


def exact_phases(dps=80):
    mp.mp.dps = dps + 30
    mp.iv.dps = dps
    discrete_logs = {pow(2, j, 13): j for j in range(12)}
    assert len(discrete_logs) == 12 and pow(2, 6, 13) == 12
    epsilons, phases = [], []
    for k in INDICES:
        tau = mp.iv.mpc(0)
        for a in range(1, 13):
            angle = 2 * mp.iv.pi * (point(Fraction(k * discrete_logs[a], 12)) + point(Fraction(a, 13)))
            tau += mp.iv.mpc(mp.iv.cos(angle), mp.iv.sin(angle))
        epsilon = tau / mp.iv.mpc(0, mp.iv.sqrt(13))
        # z=e^{-i Arg(epsilon)/2}; |epsilon|=1 is proved separately by orthogonality.
        real = mp.iv.sqrt((1 + epsilon.real) / 2)
        assert lo(real) > 0, 'Half-angle branch not certified'
        imag = -epsilon.imag / (2 * real)
        epsilons.append(epsilon)
        phases.append(mp.iv.mpc(real, imag))
    return epsilons, phases


def antisymmetric_direction(phases, anchor):
    remaining = [pair for pair in PAIRS if anchor not in pair]
    (j, js), (ell, ls) = remaining
    # sin(phi)=-Im z, consistent with z=e^{-i phi}.
    a, b = -phases[j].imag, -phases[ell].imag
    normalizer = mp.iv.sqrt(2 * (a*a + b*b))
    assert lo(normalizer) > 0
    u = [point(0) for _ in INDICES]
    u[j], u[js], u[ell], u[ls] = b/normalizer, -b/normalizer, -a/normalizer, a/normalizer
    explicit = 2 * (-phases[anchor].imag) * a * b * (b*b-a*a) / normalizer**3
    direct = (phases[anchor] * sum((u[n]**3 * conj(phases[n]) for n in range(6)), mp.iv.mpc(0))).real
    assert contains(explicit-direct)
    assert not contains(explicit), 'Cubic coefficient not separated from zero'
    residual = sum((phases[n] * u[n] for n in range(6)), mp.iv.mpc(0))
    assert contains(residual.real) and contains(residual.imag)
    assert contains(sum(x*x for x in u), 1)
    return u, explicit, {'pairs': remaining, 'normalizer': normalizer}


def minor_direction(phases, anchor, support):
    j, k, ell = support
    def det(a, b):
        return (conj(phases[a])*phases[b]).imag
    vector = [point(0) for _ in INDICES]
    vector[j], vector[k], vector[ell] = det(k, ell), det(ell, j), det(j, k)
    norm = mp.iv.sqrt(sum(x*x for x in vector))
    if lo(norm) <= 0:
        return None
    u = [x/norm for x in vector]
    p = (phases[anchor] * sum((u[n]**3*conj(phases[n]) for n in range(6)), mp.iv.mpc(0))).real
    return u, p


def radius_values(name):
    if name == 'pi/6':
        return mp.iv.sqrt(3)/2, point(Fraction(1, 2))
    radius = {'9/20': Fraction(9,20), '13/20': Fraction(13,20), '3/4': Fraction(3,4)}[name]
    return mp.iv.cos(point(radius)), mp.iv.sin(point(radius))


def pair_record(phases, anchor, u, p, radius, kind):
    t, s = radius_values(radius)
    assert lo(t) > hi(s) > 0
    base = 1 + t*t - 2*t**4
    plus = base - 2*t*s**3*p
    minus = base + 2*t*s**3*p
    gap = 4*t*s**3*abs(p)
    assert lo(gap) > 0
    vectors = []
    residuals = []
    for sign in (1,-1):
        c = [s*sign*x for x in u]
        c[anchor] = t
        norm = sum(x*x for x in c)
        A = sum((c[n]*phases[n] for n in range(6)), mp.iv.mpc(0))
        residuals.append({'norm_minus_1': enclosure(norm-1),
                          'A_minus_target_real': enclosure((A-t*phases[anchor]).real),
                          'A_minus_target_imag': enclosure((A-t*phases[anchor]).imag)})
        assert contains(norm,1) and contains((A-t*phases[anchor]).real) and contains((A-t*phases[anchor]).imag)
        direct = 1 + A.real**2 + A.imag**2 - 2*(A*sum((c[n]**3*conj(phases[n]) for n in range(6)),mp.iv.mpc(0))).real
        assert contains(direct-(plus if sign==1 else minus))
        vectors.append([midpoint(x) for x in c])
    return {'anchor_index': anchor, 'character_k': INDICES[anchor], 'radius': radius, 'kind': kind,
            'target_A': {'real': enclosure((t*phases[anchor]).real), 'imag': enclosure((t*phases[anchor]).imag)},
            'cubic_P': enclosure(p), 'D_plus': enclosure(plus), 'D_minus': enclosure(minus),
            'gap_D': enclosure(gap), 'exported_binary64_vectors': vectors,
            'export_status': 'Approximations only; exact objects are given by the analytic recipe.',
            'interval_checks': residuals}


def certificate(dps=80):
    eps, z = exact_phases(dps)
    rows, minor_rows = [], []
    anchors = []
    for i in range(6):
        u, p, recipe = antisymmetric_direction(z, i)
        # A conjugate pair away from anchor certifies rank2 of the residual phase matrix.
        j, js = recipe['pairs'][0]
        determinant = (conj(z[j])*z[js]).imag
        assert not contains(determinant)
        anchors.append({'anchor_index': i, 'character_k': INDICES[i], 'kernel_dimension': 3,
                        'residual_rank_minor': enclosure(determinant), 'pairs': recipe['pairs'],
                        'normalizer': enclosure(recipe['normalizer']), 'cubic_P': enclosure(p)})
        for radius in ('9/20','13/20','3/4','pi/6'):
            rows.append(pair_record(z,i,u,p,radius,'conjugate_pairs'))
        candidates = []
        for support in combinations([j for j in range(6) if j!=i],3):
            trial = minor_direction(z,i,support)
            if trial is not None:
                uv, pv = trial
                candidates.append((support,uv,pv))
        assert len(candidates)==10
        # A constructive search; this choice is not a statistical preregistered sample.
        support, uv, pv = max(candidates,key=lambda x: lo(abs(x[2])))
        if hi(pv)<0:
            uv,pv=[-x for x in uv],-pv
        for radius in ('9/20','13/20','3/4','pi/6'):
            item=pair_record(z,i,uv,pv,radius,'three_column_minors')
            item['support_indices']=list(support)
            item['support_character_k']=[INDICES[n] for n in support]
            minor_rows.append(item)
    return {'version':'V6.39', 'precision_digits':dps, 'character_indices':list(INDICES),
            'primitive_root':2, 'gauss_convention':'tau_k=sum chi_k(a)*exp(2pi i a/13); epsilon=tau/(i sqrt13)',
            'epsilons':[{'k':k,'real':enclosure(e.real),'imag':enclosure(e.imag)} for k,e in zip(INDICES,eps)],
            'phases':[{'k':k,'real':enclosure(v.real),'imag':enclosure(v.imag)} for k,v in zip(INDICES,z)],
            'anchors':anchors, 'conjugate_pair_witnesses':rows, 'minor_witnesses':minor_rows,
            'scope':'Existence of variation at A=cos(r)*z_i; not every prescribed complex A.',
            'zero_counting_performed':False, 'causal_inference':False,
            'proof_basis':'Exact algebraic definitions and identities; interval evaluation separates cubic coefficient and gaps from zero.'}
