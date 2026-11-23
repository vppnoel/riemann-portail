"""TAC-006 — Pli transversal sur une fibre à coefficient A fixé (V13 impaire mod 13).

Auteur et titulaire des droits : Vincent NOËL. Producteur : ia:claude (Claude Opus 5.5), 18 octobre 2026.
Prévision enregistrée avant tout calcul : taches.py prevoir TAC-006 (journal_taches.json).

Objet fixé par la prévision : ancre k=1, r=pi/6, A=cos(pi/6) z_1 (eta=0), premier candidat de jets V6.41
(hauteur 5). Chemin exact sur la fibre : c(lam)=cos r e_1 + sin r (cos lam p + sin lam q), p,q orthonormés
de ker M_1, définis exactement par Gram-Schmidt de combinaisons RATIONNELLES fixées de vecteurs exacts du noyau.
Ancre, rayon, norme et A sont donc conservés exactement pour tout lam : le pli certifié est à A constant.

Moteur : celui du document 66 (src/v642_intervalles.py), étendu des deux composantes du rayon aux six
composantes B_j(s)=z_j L(s,chi_j). Reste d'Euler-Maclaurin borné analytiquement (lemme I1), dérivées par
Cauchy, inclusion et contraction (théorème I3), Rouché sur arcs (lemme I4), symétrie et unicité (lemme I5).
Backend : arithmétique d'intervalles mpmath 1.3.0 (documentation : expérimentale).
Aucune donnée de zéro n'est injectée : seuls le vecteur candidat archivé V6.41 (point de départ) et la
hauteur 5 (prescrite par la section de jets V6.41) servent à choisir la boîte et le chemin.
"""
from fractions import Fraction
from math import factorial
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '3_Preuves_et_calculs', 'src'))
import mpmath as mp
from v639_contraintes import exact_phases, point, enclosure
from v642_intervalles import (lower, upper, interval, abs_upper, magnitude, symmetric, complex_exp,
                              rounded_midpoint, bernoulli, rational_inverse, contraction_certificate)

INDICES = (1, 3, 5, 7, 9, 11)
ANCHOR = 0                      # k=1
OFF = (1, 2, 3, 4, 5)           # k=3,5,7,9,11
SIN_R = Fraction(1, 2)          # r = pi/6 exactement


def mid(x):
    return (lower(x) + upper(x)) / 2


def cmid(z):
    return mp.mpc(mp.mpf(mid(z.real).numerator) / mid(z.real).denominator,
                  mp.mpf(mid(z.imag).numerator) / mid(z.imag).denominator)


def to_frac(x, places):
    """Rational fixed once from a numerical value; it defines the path, it certifies nothing."""
    s = mp.nstr(mp.mpf(x), places + 5, strip_zeros=False, min_fixed=-mp.inf, max_fixed=mp.inf)
    return Fraction(s).limit_denominator(10 ** places)


class V13Jets:
    """Validated jets of the six components B_j(s)=z_j L(s,chi_j), j over k=1,3,...,11."""

    def __init__(self, digits=50, N=32, M=12, real=('0.29', '0.71'), imag=('4.77', '5.23')):
        self.digits, self.N, self.M = digits, N, M
        _, self.z = exact_phases(digits)                       # sets mp.iv.dps=digits, mp.mp.dps=digits+30
        dl = {pow(2, j, 13): j for j in range(12)}
        self.T = []
        for j, k in enumerate(INDICES):
            row = [None]
            for a in range(1, 13):
                ang = 2 * mp.iv.pi * point(Fraction((k * dl[a]) % 12, 12))
                row.append(self.z[j] * mp.iv.mpc(mp.iv.cos(ang), mp.iv.sin(ang)))
            self.T.append(row)
        self.logs = {a: [mp.iv.log(point(13 * n + a)) for n in range(N)] for a in range(1, 13)}
        self.tail_logs = {a: mp.iv.log(point(13 * N + a)) for a in range(1, 13)}
        self.tail_c = {a: [point(bernoulli(2 * k) * Fraction(13 ** (2 * k - 1), factorial(2 * k) * (13 * N + a) ** (2 * k - 1)))
                           for k in range(1, M + 1)] for a in range(1, 13)}
        self.domain = mp.iv.mpc(interval(*real), interval(*imag))
        d = Fraction(1, 8); self.delta = point(d)
        sigma = lower(self.domain.real) - d; sigma_high = upper(self.domain.real) + d
        tau = abs_upper(self.domain.imag) + d
        prod = point(1)
        for j in range(2 * M):
            rm = max(abs(sigma + j), abs(sigma_high + j))
            prod *= mp.iv.sqrt(point(rm) ** 2 + point(tau) ** 2)
        c = 2 * (point(1) + point(Fraction(1, 2 * M - 1))) / (2 * mp.iv.pi) ** (2 * M)
        y = point(Fraction(13 * N + 1, 13))
        hurwitz = c * prod * mp.iv.exp(point(1 - sigma - 2 * M) * mp.iv.log(y)) / point(sigma + 2 * M - 1)
        scaling = mp.iv.exp(-point(sigma) * mp.iv.log(13))
        # Per Hurwitz block a (weight one): remainder of 13^{-s} zeta_EM(s,a/13) and of its derivatives.
        self.block_remainder = [point(factorial(k)) * hurwitz * scaling / self.delta ** k for k in range(3)]

    def check_domain(self, s):
        if (lower(s.real) < lower(self.domain.real) or upper(s.real) > upper(self.domain.real)
                or lower(s.imag) < lower(self.domain.imag) or upper(s.imag) > upper(self.domain.imag)):
            raise ValueError('Outside the registered analytic remainder rectangle')

    def components(self, s, order=2):
        """Return B[j][k] = d^k/ds^k (z_j L(s,chi_j)), k<=order, as validated complex intervals."""
        s = s if hasattr(s, '_mpci_') else mp.iv.mpc(s)
        self.check_domain(s)
        rising = {}; p0 = mp.iv.mpc(1); p1 = p2 = mp.iv.mpc(0)
        for j in range(2 * self.M - 1):
            f = s + j; p0, p1, p2 = p0 * f, p1 * f + p0, p2 * f + 2 * p1
            if (j + 1) % 2: rising[j + 1] = (p0, p1, p2)
        B = [[mp.iv.mpc(0) for _ in range(order + 1)] for _ in range(6)]
        for a in range(1, 13):
            v = [mp.iv.mpc(0) for _ in range(order + 1)]
            for L in self.logs[a]:
                e = complex_exp(-s * L); v[0] += e
                if order >= 1: v[1] -= L * e
                if order >= 2: v[2] += L * L * e
            L = self.tail_logs[a]; e = complex_exp(-s * L); w = 13 * self.N + a; g = 1 / (s - 1)
            v[0] += e * (point(Fraction(w, 13)) * g + point(Fraction(1, 2)))
            if order >= 1: v[1] += e * (point(Fraction(w, 13)) * (-g * g - L * g) - L / 2)
            if order >= 2: v[2] += e * (point(Fraction(w, 13)) * (2 * g ** 3 + 2 * L * g * g + L * L * g) + L * L / 2)
            for k, c in enumerate(self.tail_c[a], 1):
                q0, q1, q2 = rising[2 * k - 1]
                v[0] += c * e * q0
                if order >= 1: v[1] += c * e * (q1 - L * q0)
                if order >= 2: v[2] += c * e * (q2 - 2 * L * q1 + L * L * q0)
            for k in range(order + 1):
                rb = self.block_remainder[k]
                v[k] += mp.iv.mpc(symmetric(rb), symmetric(rb))
            for j in range(6):
                for k in range(order + 1):
                    B[j][k] += self.T[j][a] * v[k]
        return B


class FibrePath:
    """Exact great circles of the fibre {anchor=cos r, A=cos r z_1, |c|=1} (eta=0: the unit sphere of ker M_1)."""

    def __init__(self, z, a_free, b_free, n_free=None, pivots=None):
        rows = [[z[j].real for j in OFF], [z[j].imag for j in OFF]]
        self.pivots = pivots or (0, 1)                       # positions inside OFF
        self.free = tuple(i for i in range(5) if i not in self.pivots)
        P0, P1 = self.pivots
        a11, a12, a21, a22 = rows[0][P0], rows[0][P1], rows[1][P0], rows[1][P1]
        det = a11 * a22 - a12 * a21
        if lower(det) <= 0 <= upper(det): raise ValueError('Pivot minor not separated from zero')
        self.pivot_det = det
        basis = []
        for e in self.free:                                   # exact kernel vectors k_e
            r0, r1 = rows[0][e], rows[1][e]
            x0 = -(a22 * r0 - a12 * r1) / det; x1 = -(-a21 * r0 + a11 * r1) / det
            v = [mp.iv.mpf(0)] * 5; v[e] = mp.iv.mpf(1); v[P0] = x0; v[P1] = x1
            basis.append(v)
        self.rows, self.basis = rows, basis
        comb = lambda f: [sum((point(f[i]) * basis[i][m] for i in range(3)), mp.iv.mpf(0)) for m in range(5)]
        dot = lambda u, v: sum((u[m] * v[m] for m in range(5)), mp.iv.mpf(0))
        unit = lambda u: [x / mp.iv.sqrt(dot(u, u)) for x in u]
        sub = lambda u, v, c: [u[m] - c * v[m] for m in range(5)]
        self.p = unit(comb(a_free))
        q = comb(b_free); q = sub(q, self.p, dot(self.p, q)); self.q = unit(q)
        self.n = None
        if n_free is not None:
            n = comb(n_free); n = sub(n, self.p, dot(self.p, n)); n = sub(n, self.q, dot(self.q, n)); self.n = unit(n)
        self.dot = dot
        # exact-membership diagnostics (enclosures must contain 0 / 1)
        self.kernel_residual = [abs_upper(sum((rows[r][m] * v[m] for m in range(5)), mp.iv.mpf(0)))
                                for v in (self.p, self.q) for r in (0, 1)]

    def coefficients(self, lam, second=None):
        """c(lam) and dc/dlam on the great circle spanned by p and (q or n)."""
        w = self.q if second is None else second
        cl, sl = mp.iv.cos(lam), mp.iv.sin(lam)
        cos_r = mp.iv.sqrt(point(3)) / 2; sin_r = point(SIN_R)
        c = [cos_r] + [sin_r * (cl * self.p[m] + sl * w[m]) for m in range(5)]
        dc = [mp.iv.mpf(0)] + [sin_r * (-sl * self.p[m] + cl * w[m]) for m in range(5)]
        return c, dc


def combine(B, c, order):
    return [sum((c[j] * B[j][k] for j in range(6)), mp.iv.mpc(0)) for k in range(order + 1)]


def critical_system(jets, path, lam, t, omega, second=None):
    s = mp.iv.mpc(point(Fraction(1, 2)), t)
    B = jets.components(s, 2)
    c, dc = path.coefficients(lam, second)
    f = combine(B, c, 2); fl = combine(B, dc, 1)
    I = mp.iv.mpc(0, 1)
    H = (omega * f[0]).real; Ht = (omega * I * f[1]).real; Htt = -(omega * f[2]).real
    Hl = (omega * fl[0]).real; Hlt = (omega * I * fl[1]).real
    return {'values': [H, Ht], 'jacobian': [[Hl, Ht], [Hlt, Htt]],
            'anchor_projection': (omega * B[ANCHOR][0]).real, 'H_lam': Hl, 'H_tt': Htt}


def newton(jets, path, lam0, t0, omega, second=None, iters=40, tol=Fraction(1, 10 ** 35)):
    lam, t = Fraction(lam0), Fraction(t0)
    for it in range(iters):
        S = critical_system(jets, path, point(lam), point(t), omega, second)
        G = [mid(x) for x in S['values']]; J = [[mid(x) for x in row] for row in S['jacobian']]
        det = J[0][0] * J[1][1] - J[0][1] * J[1][0]
        if det == 0: return None
        dl = (J[1][1] * G[0] - J[0][1] * G[1]) / det; dt = (-J[1][0] * G[0] + J[0][0] * G[1]) / det
        lam, t = lam - dl, t - dt
        sc = 10 ** (jets.digits - 5)              # essai 1 : arrondi fixe 10^-45, incompatible avec le plan 80
        lam = Fraction(round(lam * sc), sc); t = Fraction(round(t * sc), sc)
        if abs(lam) > 1 or abs(t - 5) > Fraction(1, 5): return None
        if abs(dl) + abs(dt) < tol: return lam, t, it + 1
    return None


def fold_certificate(jets, path, centre, halfwidth, omega, second=None):
    lam0, t0 = centre
    S0 = critical_system(jets, path, point(lam0), point(t0), omega, second)
    box = critical_system(jets, path, interval(lam0 - halfwidth, lam0 + halfwidth),
                          interval(t0 - halfwidth, t0 + halfwidth), omega, second)
    C = rational_inverse(box['jacobian'], places=30)
    cert = contraction_certificate([lam0, t0], halfwidth, S0['values'], box['jacobian'], C)
    ap = box['anchor_projection']
    sep = lambda x: lower(x) > 0 or upper(x) < 0
    return {'accepted': cert['accepted'], 'strict_inclusion': cert['strict_inclusion'],
            'contraction_upper': float(Fraction(cert['contraction_upper'])),
            'centre': [str(lam0), str(t0)], 'halfwidth': str(halfwidth),
            'K': [enclosure(x, 40) for x in cert['K_intervals']],
            'H_lam_box': enclosure(box['H_lam'], 18), 'H_tt_box': enclosure(box['H_tt'], 18),
            'H_lam_separated': sep(box['H_lam']), 'H_tt_separated': sep(box['H_tt']),
            'anchor_projection_box': enclosure(ap, 18), 'anchor_projection_separated': sep(ap),
            'kappa_box': enclosure(-2 * box['H_lam'] / box['H_tt'], 18) if sep(box['H_tt']) else None,
            'accepted_with_separations': cert['accepted'] and sep(box['H_lam']) and sep(box['H_tt']) and sep(ap)}


def _decimal_lower(x, places=12):
    """Décimale arrondie vers le bas : borne extérieure inférieure d'une Fraction."""
    from math import floor
    return _dec(floor(x * 10 ** places), places)


def _decimal_upper(x, places=12):
    from math import ceil
    return _dec(ceil(x * 10 ** places), places)


def _dec(k, places):
    sg = '-' if k < 0 else ''; k = abs(k); e, f = divmod(k, 10 ** places)
    return f"{sg}{e}.{f:0{places}d}"


def rouche(jets, path, lam_interval, w0, R, n_arcs, alpha):
    """Lemma I4 of document 66 in w=-i(s-1/2), uniformly for lam in lam_interval and for every centre in w0.
    w0 is a Fraction or an interval (all centres of an enclosure); alpha is a fixed rational comparison coefficient.
    Revision of 18 October (review of PR #18, C1): the comparison |alpha| R^2 is a true lower bound,
    lower(sqrt(re^2 + im^2)) R^2, not the lower end of magnitude() (an upper bound of modulus on a rectangle).
    Bounds are exported as exact fractions; decimals are rounded outward."""
    I = mp.iv.mpc(0, 1); half = point(Fraction(1, 2))
    W0 = w0 if hasattr(w0, '_mpi_') else point(w0)
    c, _ = path.coefficients(lam_interval)
    al = mp.iv.mpc(point(alpha.real), point(alpha.imag))
    Rp = point(R); bound = mp.iv.sqrt(al.real ** 2 + al.imag ** 2) * Rp * Rp   # |P| = |alpha| R^2 on the circle
    comparison = lower(bound)
    d = 2 * Rp * mp.iv.sin(mp.iv.pi / (2 * n_arcs))
    worst = Fraction(0); worst_arc = None
    for i in range(n_arcs):
        th = mp.iv.pi * point(Fraction(2 * i + 1, n_arcs))
        wm = mp.iv.mpc(W0 + Rp * mp.iv.cos(th), Rp * mp.iv.sin(th))
        sm = half + I * wm
        Bm = jets.components(sm, 1); fm = combine(Bm, c, 1)
        Fw = I * fm[1]
        Dm = fm[0] - al * (wm - W0) ** 2
        Dwm = Fw - 2 * al * (wm - W0)
        dd = symmetric(d)
        wb = mp.iv.mpc(wm.real + dd, wm.imag + dd)
        sb = half + I * wb
        Bb = jets.components(sb, 2); fb = combine(Bb, c, 2)
        Dww = -fb[2] - 2 * al
        est = magnitude(Dm) + magnitude(Dwm) * d + magnitude(Dww) * d * d / 2
        u = upper(est)
        if u > worst: worst, worst_arc = u, i
        if not u < comparison:
            return {'accepted': False, 'failed_arc': i, 'defect_upper': str(u), 'comparison_lower': str(comparison)}
    m = comparison - worst
    return {'accepted': worst < comparison, 'arcs': n_arcs, 'radius': str(R),
            'comparison_lower_exact': str(comparison), 'defect_upper_max_exact': str(worst), 'margin_lower_exact': str(m),
            'comparison_lower': _decimal_lower(comparison), 'defect_upper_max': _decimal_upper(worst),
            'margin_lower': _decimal_lower(m), 'worst_arc': worst_arc}


def root_certificate(jets, path, lam, centre, halfwidth):
    """Complex zero of F_{c(lam)} in the square box centre +/- halfwidth (Theorem I3, real 2x2 form)."""
    c, _ = path.coefficients(point(lam))
    x0, y0 = centre
    s0 = mp.iv.mpc(point(x0), point(y0))
    sb = mp.iv.mpc(interval(x0 - halfwidth, x0 + halfwidth), interval(y0 - halfwidth, y0 + halfwidth))
    f0 = combine(jets.components(s0, 0), c, 0)[0]
    fb = combine(jets.components(sb, 1), c, 1)[1]
    J = [[fb.real, -fb.imag], [fb.imag, fb.real]]
    C = rational_inverse(J, places=30)
    cert = contraction_certificate([x0, y0], halfwidth, [f0.real, f0.imag], J, C)
    K = cert['K_intervals']
    return {'accepted': cert['accepted'], 'contraction_upper': float(Fraction(cert['contraction_upper'])),
            'centre': [str(x0), str(y0)], 'halfwidth': str(halfwidth),
            'Re_s': enclosure(K[0], 24), 'Im_s': enclosure(K[1], 24),
            'excludes_critical_line': lower(K[0]) > Fraction(1, 2) or upper(K[0]) < Fraction(1, 2),
            'symmetric_box': x0 == Fraction(1, 2)}


def numeric_root(jets, path, lam, s_start, iters=60):
    c, _ = path.coefficients(point(lam))
    s = mp.mpc(s_start)
    for _ in range(iters):
        # mpmath 1.3.0 : iv.mpc(mpc) échoue (constructeur de copie, cf. document 66) ; passer par les parties réelles
        f = combine(jets.components(mp.iv.mpc(mp.iv.mpf(s.real), mp.iv.mpf(s.imag)), 1), c, 1)
        step = cmid(f[0]) / cmid(f[1]); s -= step
        if abs(step) < mp.mpf(10) ** (-(jets.digits - 8)): break
    return s
