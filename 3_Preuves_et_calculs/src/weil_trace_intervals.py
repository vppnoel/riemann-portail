"""V6.36 : traces DH par quadrature physique et intervalles.

Cadre fixé : a=1/50, h=1/200, conducteur 5, parité impaire.
Les bornes analytiques de quadrature sont documentées dans PREUVE_NORME_V636.md.
La proposition d'un sous-espace est numérique ; son signe doit être contrôlé
séparément. Aucun zéro ne sert à construire ces traces.
"""
from fractions import Fraction as Q
from functools import lru_cache
import math
import mpmath as mp
import numpy as np

A = Q(1, 50)
H = Q(1, 200)
ORDER = 16


def setup(dps=60):
    mp.mp.dps = dps+25
    mp.iv.dps = dps
    gauss_rule.cache_clear()
    physical_grid.cache_clear()


def I(x):
    if isinstance(x, Q):
        return mp.iv.mpf(x.numerator)/x.denominator
    return mp.iv.mpf(x)


def lower(x):
    return mp.mpf(x._mpi_[0])


def upper(x):
    return mp.mpf(x._mpi_[1])


def g_closed(x):
    """Prolongement analytique de la branche 0<x<2a."""
    a = I(A)
    b = mp.iv.pi/a
    return ((2*a-x)*(I(9)/64+mp.iv.cos(b*x)/8+mp.iv.cos(2*b*x)/128)
            +I(5)/(24*b)*mp.iv.sin(b*x)
            +I(25)/(768*b)*mp.iv.sin(2*b*x))


def g_interval(x):
    x = abs(x)
    edge = I(2*A)
    if lower(x) >= upper(edge):
        return I(0)
    value = g_closed(x)
    if upper(x) >= lower(edge):
        return mp.iv.mpf([min(lower(value), mp.mpf(0)),
                          max(upper(value), mp.mpf(0))])
    return value


def legendre(n, x):
    p, q = I(1), x
    if n == 0:
        return p, I(0)
    for k in range(2, n+1):
        p, q = q, ((2*k-1)*x*q-(k-1)*p)/k
    return q, p


@lru_cache(maxsize=1)
def gauss_rule():
    nodes, _ = mp.gauss_quadrature(ORDER, "legendre")
    out = []
    # Les centres haute précision proposent des racines ; les signes de
    # P_16 aux extrémités prouvent les encadrements utilisés.
    width = mp.mpf(2)**(-180)
    for c in nodes:
        lo, hi = c-width, c+width
        xl = I(mp.nstr(lo, 85))
        xh = I(mp.nstr(hi, 85))
        pl, _ = legendre(ORDER, xl)
        ph, _ = legendre(ORDER, xh)
        assert ((upper(pl) < 0 < lower(ph))
                or (upper(ph) < 0 < lower(pl)))
        x = mp.iv.mpf([lower(xl), upper(xh)])
        pn, pn1 = legendre(ORDER, x)
        derivative = ORDER*(x*pn-pn1)/(x*x-1)
        weight = 2/((1-x*x)*derivative*derivative)
        assert lower(weight) > 0
        out.append((x, weight))
    assert all(upper(out[i][0]) < lower(out[i+1][0]) for i in range(ORDER-1))
    return tuple(out)


def panel_error(width, radius, majorant):
    """Reste Gauss et estimation de Cauchy de la dérivée d'ordre 32."""
    m = ORDER
    bound = (I(width)**(2*m+1)*math.factorial(m)**4*majorant
             /((2*m+1)*math.factorial(2*m)**2*I(radius)**(2*m)))
    return upper(bound)


def enclose_quadrature(fun, breaks, radius, majorant):
    total, error = I(0), mp.mpf(0)
    for left, right in zip(breaks, breaks[1:]):
        count = max(1, math.ceil(2*(right-left)/radius))
        width = (right-left)/count
        for j in range(count):
            center = I(left+(j+Q(1, 2))*width)
            half = I(width)/2
            for x, weight in gauss_rule():
                total += half*weight*fun(center+half*x)
        error += count*panel_error(width, radius, majorant)
    return total+mp.iv.mpf([-error, error]), error


@lru_cache(maxsize=32)
def physical_grid(count):
    """g aux noeuds ; deux branches analytiques séparées au point 0."""
    width = 2*A/count
    points = []
    for left in (-2*A, Q(0)):
        for j in range(count):
            center = I(left+(j+Q(1, 2))*width)
            half = I(width)/2
            for x, weight in gauss_rule():
                u = center+half*x
                points.append((u, half*weight*g_interval(u)))
    return tuple(points), width


def arch_interval(n):
    t = n*H
    sigma = I(3)/4
    if t > 2*A:
        radius = min(Q(1, 50), (t-2*A)/2)
        count = max(1, math.ceil(4*A/radius))
        points, width = physical_grid(count)
        ti = I(t)
        value = I(0)
        for u, weight_g in points:
            v = ti-u
            value -= weight_g*mp.iv.exp(-2*sigma*v)/(1-mp.iv.exp(-2*v))
        majorant = ((I(2*A+radius)*mp.iv.exp(4*mp.iv.pi/I(A)*I(radius)))
                    /(1-mp.iv.exp(-2*I(t-2*A-radius))))
        error = 2*count*panel_error(width, radius, majorant)
        return value+mp.iv.mpf([-error, error]), error

    # Seulement n=0,...,8. La singularité en u=0 est amovible.
    # Les panneaux ne traversent aucun changement de branche de g.
    gt = I(0) if t == 2*A else g_closed(I(t))
    limit = 2*t+4*A
    breaks = sorted({Q(0), 2*t, 4*A-2*t, limit})
    breaks = [x for x in breaks if 0 <= x <= limit]
    ti = I(t)

    def integrand(u):
        gp = g_interval(ti+u/2)
        gm = g_interval(ti-u/2)
        return (mp.iv.exp(-u)*gt-mp.iv.exp(-sigma*u)*(gp+gm)/2)/(1-mp.iv.exp(-u))

    # Majorant uniforme 1000 sur les disques de rayon 1/1000 :
    # voir l'annexe (quotient amovible pour la première branche).
    integral, error = enclose_quadrature(integrand, breaks, Q(1, 1000), I(1000))
    tail = -gt*mp.iv.log(1-mp.iv.exp(-I(limit)))
    value = (mp.iv.log(5/mp.iv.pi)-mp.iv.euler)*gt+integral+tail
    return value, error


def dh_coefficients(M):
    kappa = (mp.iv.sqrt(10-2*mp.iv.sqrt(5))-2)/(mp.iv.sqrt(5)-1)
    table = (I(0), I(1), kappa, -kappa, I(-1))
    a = [table[n % 5] for n in range(M+1)]
    c = [I(0) for _ in range(M+1)]
    for n in range(2, M+1):
        c[n] = a[n]*mp.iv.log(n)
        for d in range(2, n):
            if n % d == 0:
                c[n] -= c[d]*a[n//d]
    return c


def prime_interval(n, c, logs, roots):
    ti = I(n*H)
    result = I(0)
    for m in range(2, len(c)):
        x = logs[m]-ti
        if lower(abs(x)) > upper(I(2*A)):
            continue
        result -= c[m]/roots[m]*g_interval(x)
    # log(2)>2a et t>=0 : le second support g(-log(m)-t) est vide.
    return result


def float_center_and_radius(value):
    center = float((lower(value)+upper(value))/2)
    radius = upper(abs(I(center)-value))
    radius_float = np.nextafter(float(radius), np.inf)
    return center, float(radius_float)


def traces(L=1115, dps=60, progress=None):
    setup(dps)
    M = math.ceil(math.exp(float((L-1)*H+2*A)))+2
    assert upper(mp.iv.exp(I((L-1)*H+2*A))) < M
    c = dh_coefficients(M)
    logs = [I(0), I(0)]+[mp.iv.log(m) for m in range(2, M+1)]
    roots = [I(0), I(1)]+[mp.iv.sqrt(m) for m in range(2, M+1)]
    centers, radii, intervals, errors = [], [], [], []
    for n in range(L):
        arch, qerror = arch_interval(n)
        value = arch+prime_interval(n, c, logs, roots)
        center, radius = float_center_and_radius(value)
        centers.append(center)
        radii.append(radius)
        intervals.append([list(v) for v in value._mpi_])
        errors.append(float(qerror))
        if progress and (n < 9 or n % 100 == 0 or n == L-1):
            progress(n, center, radius)
    return np.array(centers), np.array(radii), intervals, errors
