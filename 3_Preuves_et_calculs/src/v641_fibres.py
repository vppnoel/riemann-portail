"""Affine phase fibres in odd V13, with explicit operator coordinates.

The theorem is exact and recorded in preuves/V641_GEOMETRIE_ET_OPERATEURS.md.
NumPy routines below are geometric diagnostics, not certificates of a boundary
or of a zero. interval_certificate independently encloses the finite Gauss sums.
"""
from dataclasses import dataclass
import math
import numpy as np


def phase_values(dps=80):
    """Binary64 exports of exact V13 phase recipes, explicitly approximate."""
    from v639_contraintes import exact_phases, midpoint
    _, phases = exact_phases(dps)
    return np.array([complex(midpoint(z.real), midpoint(z.imag)) for z in phases])


@dataclass
class Fibre:
    phases: np.ndarray
    anchor: int
    radius: float
    target: complex
    off_indices: np.ndarray
    matrix: np.ndarray
    gram: np.ndarray
    right_inverse: np.ndarray
    projector: np.ndarray
    kernel_basis: np.ndarray
    minimum_solution: np.ndarray
    eta: float
    rho: float
    status: str

    def point(self, direction):
        """Export c=t e_i+s(u0+rho N v), with ||v||=1.

        At boundary_tolerance this is only an approximate boundary export.
        No numerical classification here replaces an exact eta<=1 proof.
        """
        if self.status == 'outside':
            raise ValueError('The requested target is outside the numerical ellipse')
        v = np.asarray(direction, dtype=float)
        if v.shape != (3,) or not np.all(np.isfinite(v)):
            raise ValueError('A finite three-dimensional sphere direction is required')
        if not np.isclose(np.dot(v, v), 1., rtol=0., atol=1e-11):
            raise ValueError('Sphere direction must have norm one')
        c = np.zeros(6)
        c[self.anchor] = math.cos(self.radius)
        c[self.off_indices] = math.sin(self.radius) * (
            self.minimum_solution + self.rho * (self.kernel_basis @ v))
        return c


def fibre_geometry(phases, anchor, radius, target, tolerance=1e-11):
    """Return affine operators and numerical feasibility for a prescribed A.

    Only 0<r<pi/4 and c_i=+cos(r) are covered. 'boundary_tolerance' deliberately
    reports that floating point cannot decide the exact boundary equality.
    """
    z = np.asarray(phases, dtype=complex)
    if z.shape != (6,) or not np.all(np.isfinite(z)):
        raise ValueError('Six finite phases are required')
    if not np.allclose(abs(z), 1., rtol=0., atol=1e-10):
        raise ValueError('The normalised recipe requires unit phases')
    if not isinstance(anchor, (int, np.integer)) or not 0 <= anchor < 6:
        raise ValueError('Anchor index must lie in 0,...,5')
    r = float(radius)
    if not 0. < r < math.pi/4:
        raise ValueError('The unique-anchor chart requires 0<r<pi/4')
    target = complex(target)
    if not np.isfinite(target) or not 0. < tolerance < 1.:
        raise ValueError('Finite target and positive small tolerance required')
    off = np.array([j for j in range(6) if j != anchor])
    matrix = np.stack((z[off].real, z[off].imag))
    gram = matrix @ matrix.T
    eigenvalues = np.linalg.eigvalsh(gram)
    if eigenvalues[0] <= 100 * np.finfo(float).eps * eigenvalues[-1]:
        raise ValueError('Rank-two residual phase map is required')
    right_inverse = np.linalg.solve(gram, matrix).T
    projector = np.eye(5) - right_inverse @ matrix
    _, _, vh = np.linalg.svd(matrix, full_matrices=True)
    kernel_basis = vh[2:].T
    residual = (target - math.cos(r)*z[anchor]) / math.sin(r)
    b = np.array([residual.real, residual.imag])
    minimum_solution = right_inverse @ b
    eta = float(b @ np.linalg.solve(gram, b))
    if eta < 1. - tolerance:
        status = 'interior'
    elif eta > 1. + tolerance:
        status = 'outside'
    else:
        status = 'boundary_tolerance'
    rho = math.sqrt(max(0., 1.-eta))
    return Fibre(z, int(anchor), r, target, off, matrix, gram, right_inverse,
                 projector, kernel_basis, minimum_solution, eta, rho, status)


def ellipse_points(phases, anchor, radius, count=181):
    """Approximate geometric boundary A=t z_i+s M u, not a zero caustic."""
    f = fibre_geometry(phases, anchor, radius,
                       math.cos(radius)*complex(phases[anchor]))
    angles = np.linspace(0., 2.*math.pi, count)
    directions = np.stack((np.cos(angles), np.sin(angles)))
    eigenvalues, eigenvectors = np.linalg.eigh(f.gram)
    root = (eigenvectors * np.sqrt(eigenvalues)) @ eigenvectors.T
    offsets = math.sin(radius) * (root @ directions)
    return math.cos(radius)*f.phases[anchor] + offsets[0] + 1j*offsets[1]


def defect(phases, coefficients):
    """Normalised D for ||c||=1; rejects unnormalised exports."""
    c = np.asarray(coefficients, dtype=float)
    z = np.asarray(phases, dtype=complex)
    if c.shape != (6,) or z.shape != (6,) or not np.isclose(c@c, 1., atol=1e-10, rtol=0.):
        raise ValueError('D in this chart requires six normalised coefficients')
    A = c @ z
    return float(1. + abs(A)**2 - 2.*(A*np.dot(c**3, z.conj())).real)


def defect_polynomial(fibre):
    """C+L.v+v^T Q v+T[v,v,v] on the fibre's unit S2 coordinates."""
    if fibre.status == 'outside':
        raise ValueError('Empty fibre has no defect polynomial')
    z, i = fibre.phases, fibre.anchor
    beta = (fibre.target * z.conj()).real
    a, N = fibre.minimum_solution, fibre.kernel_basis
    weights = beta[fibre.off_indices]
    t, s, rho = math.cos(fibre.radius), math.sin(fibre.radius), fibre.rho
    constant = 1.+abs(fibre.target)**2-2.*t**3*beta[i]-2.*s**3*np.dot(weights, a**3)
    linear = -6.*s**3*rho * np.einsum('j,j,ja->a', weights, a*a, N)
    quadratic = -6.*s**3*rho**2 * np.einsum('j,j,ja,jb->ab', weights, a, N, N)
    cubic = -2.*s**3*rho**3 * np.einsum('j,ja,jb,jc->abc', weights, N, N, N)
    return {'constant': float(constant), 'linear': linear,
            'quadratic': quadratic, 'cubic': cubic}


def evaluate_polynomial(polynomial, direction):
    v = np.asarray(direction, dtype=float)
    return float(polynomial['constant'] + polynomial['linear']@v
                 + v@polynomial['quadratic']@v
                 + np.einsum('abc,a,b,c', polynomial['cubic'], v, v, v))


def constancy_residual(polynomial):
    """Approximate residual of the exact algebraic constancy criterion.

    Exact constancy iff Q=(tr Q/3)I and T=-sym(I tensor L).
    A small returned value is a diagnostic, never an exact proof.
    """
    L, Q, T = (polynomial[key] for key in ('linear', 'quadratic', 'cubic'))
    identity = np.eye(3)
    trace_free = Q-np.trace(Q)/3.*identity
    symmetric = (np.einsum('ab,c->abc', identity, L)
                 + np.einsum('ac,b->abc', identity, L)
                 + np.einsum('bc,a->abc', identity, L))/3.
    return float(np.linalg.norm(trace_free)**2 + np.linalg.norm(T+symmetric)**2)


def tangent_projector(fibre, direction):
    """Orthogonal projector in the five off-anchor coordinates onto T_u fibre."""
    v = np.asarray(direction, dtype=float)
    if fibre.status != 'interior' or v.shape != (3,) or not np.isclose(v@v, 1., atol=1e-11, rtol=0.):
        raise ValueError('A sphere point in an interior fibre is required')
    N = fibre.kernel_basis
    return N @ (np.eye(3)-np.outer(v, v)) @ N.T


def interval_certificate(dps=80):
    """Enclose G and a feasible A=0 counterexample at the exact radius 13/20.

    Boundary targets use an exact analytic recipe; interval boxes only verify
    consistency of its identities. An interval touching eta=1 alone would not
    certify a singleton. Nothing here evaluates or counts a zero.
    """
    from fractions import Fraction
    from v639_contraintes import exact_phases, point, lo, hi, contains, enclosure, conj
    import mpmath as mp
    _, z = exact_phases(dps)
    t, s = mp.iv.cos(point(Fraction(13, 20))), mp.iv.sin(point(Fraction(13, 20)))
    rows = []
    for i in range(6):
        off = [j for j in range(6) if j != i]
        G00 = sum(z[j].real**2 for j in off)
        G01 = sum(z[j].real*z[j].imag for j in off)
        G11 = sum(z[j].imag**2 for j in off)
        det = G00*G11-G01**2
        assert lo(G00) > 0 and lo(det) > 0
        bx, by = -t*z[i].real/s, -t*z[i].imag/s
        eta_zero = (G11*bx**2-2*G01*bx*by+G00*by**2)/det
        assert lo(eta_zero) > 0 and hi(eta_zero) < 1
        # u=M^T e_1/sqrt(G00), hence ||u||=1 and b=G e_1/sqrt(G00).
        root = mp.iv.sqrt(G00)
        c = [point(0) for _ in range(6)]
        c[i] = t
        for j in off:
            c[j] = s*z[j].real/root
        boundary_A = t*z[i] + s*mp.iv.mpc(G00/root, G01/root)
        assert contains(sum(x*x for x in c), 1)
        A_export = sum((c[j]*z[j] for j in range(6)), mp.iv.mpc(0))
        assert contains((A_export-boundary_A).real) and contains((A_export-boundary_A).imag)
        boundary_D = 1.+boundary_A.real**2+boundary_A.imag**2-2.*(
            boundary_A*sum((c[j]**3*conj(z[j]) for j in range(6)), mp.iv.mpc(0))).real
        rows.append({'anchor_index': i, 'character_k': 2*i+1,
                     'gram': [[enclosure(G00), enclosure(G01)],
                              [enclosure(G01), enclosure(G11)]],
                     'gram_determinant': enclosure(det),
                     'zero_target_eta': enclosure(eta_zero),
                     'zero_target_slack': enclosure(1.-eta_zero),
                     'zero_target_exact_D': '1',
                     'boundary_recipe': 'u_j=Re(z_j)/sqrt(sum_{ell!=i} Re(z_ell)^2), j!=i',
                     'boundary_A': {'real': enclosure(boundary_A.real), 'imag': enclosure(boundary_A.imag)},
                     'boundary_unique_D': enclosure(boundary_D)})
    return {'version': 'V6.41', 'precision_digits': dps,
            'radius_exact': '13/20', 'anchor_sign': '+', 'rows': rows,
            'zero_counting_performed': False, 'positivity_proves_RH': False,
            'scope': 'Finite phase-map geometry and two counterexamples to universal D variation',
            'boundary_proof': 'Analytic recipe eta=1; not an inference from a numerical interval touching one'}
