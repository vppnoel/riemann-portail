"""Feasible complex targets, exact counterexamples and sphere operators."""
import math
import numpy as np
import sympy as sp
from euler_archipelago import characters
from v641_fibres import (phase_values, fibre_geometry, defect,
    defect_polynomial, evaluate_polynomial, constancy_residual,
    tangent_projector, interval_certificate)


def test_affine_fibre_identity_with_exact_symbolic_matrix():
    # Independent rational model of the rank-two constraint, not V13 phases.
    M = sp.Matrix([[1, 2, 0, -1, 3], [0, 1, 1, 2, -1]])
    b = sp.Matrix([sp.Rational(1, 3), sp.Rational(-1, 5)])
    G = M*M.T
    R = M.T*G.inv()
    P = sp.eye(5)-R*M
    u0 = R*b
    assert M.rank() == 2 and M*R == sp.eye(2)
    assert P.T == P and P*P == P and M*P == sp.zeros(2, 5)
    assert P.rank() == 3 and P*u0 == sp.zeros(5, 1)
    assert (u0.T*u0)[0] == (b.T*G.inv()*b)[0]


def test_arbitrary_interior_targets_obey_all_constraints():
    z = phase_values(70)
    r = 13/20
    for i in range(6):
        centre = math.cos(r)*z[i]
        base = fibre_geometry(z, i, r, centre)
        b = base.gram[:, 0]/(3*math.sqrt(base.gram[0, 0]))
        A = centre+math.sin(r)*complex(*b)
        f = fibre_geometry(z, i, r, A)
        assert f.status == 'interior' and abs(f.eta-1/9) < 2e-14
        for v in np.concatenate((np.eye(3), -np.eye(3))):
            c = f.point(v)
            assert abs(c@c-1) < 2e-14 and abs(c@z-A) < 3e-14
            assert np.argmax(abs(c)) == i
            assert abs(math.acos(max(abs(c)))-r) < 2e-14


def test_boundary_and_exterior_remain_explicit():
    z = phase_values(70)
    i, r = 0, .65
    centre = math.cos(r)*z[i]
    base = fibre_geometry(z, i, r, centre)
    b = base.gram[:, 0]/math.sqrt(base.gram[0, 0])
    boundary = fibre_geometry(z, i, r, centre+math.sin(r)*complex(*b))
    assert boundary.status == 'boundary_tolerance'
    assert abs(boundary.eta-1.) < 2e-14
    outside = fibre_geometry(z, i, r, centre+2*math.sin(r)*complex(*b))
    assert outside.status == 'outside' and abs(outside.eta-4) < 5e-14
    try:
        outside.point([1., 0., 0.])
        assert False, 'An empty fibre must not produce coefficients'
    except ValueError:
        pass
    try:
        fibre_geometry(z, i, 0., z[i])
        assert False, 'r=0 requires the separate singleton chart'
    except ValueError:
        pass


def test_zero_A_is_feasible_and_forces_constant_D():
    z = phase_values(70)
    for i in range(6):
        f = fibre_geometry(z, i, 13/20, 0.)
        assert f.status == 'interior' and f.eta < .98
        p = defect_polynomial(f)
        assert p['constant'] == 1. and constancy_residual(p) == 0.
        for v in np.concatenate((np.eye(3), -np.eye(3))):
            c = f.point(v)
            assert abs(c@z) < 2e-14 and abs(defect(z, c)-1.) < 3e-14


def test_general_defect_polynomial_matches_independent_group_average():
    z = phase_values(70)
    chars = characters(13, 1)
    n = range(1, 13)
    chi = np.array([[ch['table'][k] for k in n] for ch in chars])
    products = np.array([[ch['table'][(a*b) % 13] for a in n for b in n] for ch in chars])
    i, r = 2, .65
    base = fibre_geometry(z, i, r, math.cos(r)*z[i])
    b = base.gram[:, 1]/(3*math.sqrt(base.gram[1, 1]))
    target = math.cos(r)*z[i]+math.sin(r)*complex(*b)
    f = fibre_geometry(z, i, r, target)
    p = defect_polynomial(f)
    for v in np.concatenate((np.eye(3), -np.eye(3), np.array([[1, 2, 3.]])/math.sqrt(14))):
        c = f.point(v)
        a = (c*z)@chi
        amn = ((c*z)@products).reshape(12, 12)
        D_group = np.mean(abs(target*amn-np.outer(a, a))**2)
        assert abs(D_group-defect(z, c)) < 3e-13
        assert abs(D_group-evaluate_polynomial(p, v)) < 3e-13


def test_kernel_and_tangent_operators_have_correct_ranks():
    z = phase_values(70)
    f = fibre_geometry(z, 1, .65, math.cos(.65)*z[1])
    P, M, N = f.projector, f.matrix, f.kernel_basis
    assert np.linalg.norm(P.T-P) < 2e-14
    assert np.linalg.norm(P@P-P) < 2e-14 and np.linalg.norm(M@P) < 2e-14
    assert np.linalg.norm(N.T@N-np.eye(3)) < 2e-14
    v = np.array([1., 2., 3.])/math.sqrt(14)
    T = tangent_projector(f, v)
    assert np.linalg.norm(T@T-T) < 3e-14 and np.linalg.norm(M@T) < 3e-14
    assert abs(np.trace(P)-3) < 2e-14 and abs(np.trace(T)-2) < 2e-14
    assert np.linalg.norm(T@(N@v)) < 2e-14


def test_constancy_criterion_handles_cubic_sphere_identity():
    L = np.array([1., -2., 3.])
    I = np.eye(3)
    sym = (np.einsum('ab,c->abc', I, L)+np.einsum('ac,b->abc', I, L)
           + np.einsum('bc,a->abc', I, L))/3
    p = {'constant': 7., 'linear': L, 'quadratic': 2.*I, 'cubic': -sym}
    assert constancy_residual(p) < 1e-28
    for v in np.eye(3):
        assert abs(evaluate_polynomial(p, v)-9.) < 2e-14
    p['cubic'] = sym
    assert constancy_residual(p) > 1.
    z = phase_values(70)
    for i in range(6):
        f = fibre_geometry(z, i, .65, math.cos(.65)*z[i])
        assert constancy_residual(defect_polynomial(f)) > 1e-5


def test_interval_certificate_proves_feasible_zero_target():
    from fractions import Fraction
    cert = interval_certificate(70)
    assert cert['zero_counting_performed'] is False and cert['positivity_proves_RH'] is False
    assert len(cert['rows']) == 6 and cert['radius_exact'] == '13/20'
    for row in cert['rows']:
        assert 0 < Fraction(row['zero_target_eta']['lower']) <= Fraction(row['zero_target_eta']['upper']) < 1
        assert Fraction(row['zero_target_slack']['lower']) > 0
        assert Fraction(row['gram_determinant']['lower']) > 0
        assert row['zero_target_exact_D'] == '1'
