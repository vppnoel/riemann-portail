"""Vérifications indépendantes des identités [RIG].

Lancer :
    python tests/test_identities.py

`sympy.factorint` est volontairement utilisé ici comme factorisation indépendante des
cribles internes du package.
"""
import sys, math
from pathlib import Path
import numpy as np
import mpmath as mp
from sympy import factorint

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from rh_core import (
    arithmetic_c_via_lambda,
    arithmetic_c_via_a,
    EULER_GAMMA as g,
    KAPPA,
)
from spectral_calibration import parseval_energies
from source_localization import (
    synthetic_source_signal, matched_filter_map, morlet_demodulated_envelope,
    envelope_growth_rate, regularized_laplacian, visibility_metrics,
)
from schrodinger_flux import (
    energy_from_zero, zero_parameters_from_energy, schrodinger_matrix_1d,
    self_adjointness_defect, stationary_eigenpairs, continuity_source_density,
    norm_growth_rate,
)
from arithmetic_generator import (
    modal_state_matrix, fit_propagator, effective_generator, spectral_metric,
    metric_self_adjointness_defect, metric_unitarity_defect,
)

mp.mp.dps = 40
GAMMA = mp.euler


def test_c_equals_1_star_a():
    N = 5000
    err = np.max(np.abs(arithmetic_c_via_lambda(N) - arithmetic_c_via_a(N)))
    assert err < 1e-9, err


def test_support_structure_factorint():
    """L3, factorisation fournie indépendamment par sympy.factorint."""
    N = 3000
    c = arithmetic_c_via_lambda(N)
    for n in range(2, N + 1):
        fac = factorint(n)
        if len(fac) == 1:
            p = next(iter(fac))
            expected = -math.log(p) ** 2 + 2 * g * math.log(p)
        elif len(fac) == 2:
            p, q = fac.keys()
            expected = 2 * math.log(p) * math.log(q)
        else:
            expected = 0.0
        assert abs(c[n] - expected) < 1e-9, (n, c[n], expected)


def test_dirichlet_series_at_s2():
    """L1 : G(s)=q^2+q'+2 gamma q à s=2 (convergence absolue)."""
    s = mp.mpf(2)
    N = 200000
    c = arithmetic_c_via_lambda(N)
    lhs = sum(c[n] / n ** 2 for n in range(2, N + 1))
    qf = lambda z: -mp.diff(mp.zeta, z) / mp.zeta(z)
    q = qf(s)
    dq = mp.diff(qf, s)
    rhs = q * q + dq + 2 * GAMMA * q
    assert abs(lhs - rhs) < 2e-4, (lhs, rhs)


def test_regular_at_1_clean():
    """L4 : teste la valeur limite exacte G(1)=2 gamma^2+6 gamma_1."""
    f = lambda z: 1 / mp.zeta(z)
    Gf = lambda z: mp.zeta(z) * (mp.diff(f, z, 2) + 2 * GAMMA * mp.diff(f, z, 1))
    expected = 2 * GAMMA ** 2 + 6 * mp.stieltjes(1)
    for eps in [mp.mpf("1e-3"), mp.mpf("3e-4"), mp.mpf("1e-4")]:
        val = Gf(1 + eps)
        assert abs(val - expected) < 5e-3, (eps, val, expected)


def test_moment_nul_via_derivatives():
    f = lambda s: 1 / mp.zeta(s)
    s1 = 1 + mp.mpf("1e-10")
    s2 = 1 + mp.mpf("1e-7")
    f1 = mp.diff(f, s1, 1)
    f2 = mp.diff(f, s2, 2)
    assert abs(f1 - 1) < 1e-5, f1
    assert abs(f2 + 2 * GAMMA) < 2e-3, f2
    assert abs(f2 + 2 * GAMMA * f1) < 2e-3


def H_inf_closed(q):
    fac = factorint(q)
    if q == 1 or any(e > 1 for e in fac.values()):
        return 0.0
    mu = (-1) ** len(fac)
    phi = math.prod(p - 1 for p in fac)
    return float(-2 * mu / phi * sum(p * math.log(p) / (p - 1) for p in fac))


def test_H_infty_vs_derivatives_clean():
    """L7 dans la forme courte Phi_q(s)=mu(q) h_q(s)/zeta(s)."""
    for q in [2, 3, 5, 6, 10, 15, 30, 7, 210]:
        fac = factorint(q)
        mu = (-1) ** len(fac)

        def h(s):
            return mp.fprod([(mp.mpf(p) ** s - 1) ** -1 for p in fac])

        Phi = lambda s: mu * h(s) / mp.zeta(s)
        s0 = 1 + mp.mpf("2e-6")
        val = mp.diff(Phi, s0, 2) + 2 * GAMMA * mp.diff(Phi, s0, 1)
        expected = H_inf_closed(q)
        assert abs(val - expected) < 2e-3 * (1 + abs(expected)), (q, val, expected)


def test_H_infty_also_equals_log_q_form():
    for q in [6, 30, 105]:
        fac = factorint(q)
        mu = (-1) ** len(fac)
        phi = math.prod(p - 1 for p in fac)
        old = -2 * mu / phi * (math.log(q) + sum(math.log(p) / (p - 1) for p in fac))
        assert abs(old - H_inf_closed(q)) < 1e-12


def test_gcd_covariance():
    for d, e in [(2, 3), (4, 6), (6, 9), (5, 10), (7, 7), (8, 12)]:
        P = d * e // math.gcd(d, e)
        K = 4000
        x = (np.arange(P * K) + 0.5) / K
        sd = (x / d) % 1 - 0.5
        se = (x / e) % 1 - 0.5
        measured = np.mean(sd * se)
        expected = math.gcd(d, e) ** 2 / (12 * d * e)
        assert abs(measured - expected) < 1e-5, (d, e, measured, expected)


def test_jordan_identity():
    from rh_core import jordan_J2_sieve
    J = jordan_J2_sieve(200)
    for n in range(1, 201):
        lhs = sum(J[q] for q in range(1, n + 1) if n % q == 0)
        assert abs(lhs - n * n) < 1e-6, (n, lhs)


def test_kappa_is_sum_over_zeros():
    """Sous RH numérique : kappa/2 = sum_{gamma>0} 1/|rho|^2."""
    from explicit_formula import load_zeros
    gam, _ = load_zeros()
    s = np.sum(1 / (0.25 + gam ** 2))
    tail = (math.log(gam[-1] / (2 * math.pi)) + 1) / (2 * math.pi * gam[-1])
    assert abs(s + tail - KAPPA / 2) < 3e-4, (s, tail, KAPPA / 2)


def test_spectral_parseval():
    """L11 : normalisation FFT/Plancherel du nouveau module spectral."""
    n = 4096
    dt = 0.01
    t = np.arange(n, dtype=float) * dt
    B = np.sin(3.2 * t) + 0.3 * np.cos(7.1 * t) + 0.1 * np.sin(13.0 * t)
    e_time, e_freq = parseval_energies(t, B, window="hann")
    rel = abs(e_time - e_freq) / e_time
    assert rel < 1e-12, (e_time, e_freq, rel)


def test_dh_functional_equation():
    from rejection import dh_functional_equation_defect
    assert max(dh_functional_equation_defect()) < 1e-12

def test_generic_pipeline_reproduces_zeta():
    from rejection import build
    from rh_core import arithmetic_c_via_lambda, von_mangoldt_sieve
    N = 5000
    a, lam, c = build("zeta", N)
    assert np.max(np.abs(lam[1:] - von_mangoldt_sieve(N)[1:])) < 1e-9
    assert np.max(np.abs(c - arithmetic_c_via_lambda(N))) < 1e-9

def test_bcf_first_order_identity():
    """Coefficient de n^-s dans zeta*V_N (V_N de Bettin-Conrey-Farmer) = [n=1] + Lambda(n)/log N - sum_{d|n,d>N} mu(d)(1-log d/log N)."""
    from rh_core import von_mangoldt_sieve, mobius_sieve
    N, M = 30, 3000
    mu = mobius_sieve(M); lam = von_mangoldt_sieve(M); lN = math.log(N)
    for n in range(1, M + 1):
        divs = [d for d in range(1, n + 1) if n % d == 0]
        lhs = sum(mu[d] * (1 - math.log(d) / lN) for d in divs if d <= N)
        tail = sum(mu[d] * (1 - math.log(d) / lN) for d in divs if d > N)
        rhs = (1.0 if n == 1 else 0.0) + lam[n] / lN - tail
        assert abs(lhs - rhs) < 1e-9, n

def test_constants_of_theorem():
    """int dt/(t^2+eta^2)^2 = pi/(2 eta^3) ; Laplace de A L^3 ; S/3 = 4 kappa/3 pour S = 4 kappa."""
    from scipy.integrate import quad
    eta = 0.37
    val = quad(lambda t: 1 / (t * t + eta * eta) ** 2, -np.inf, np.inf)[0]
    assert abs(val - math.pi / (2 * eta ** 3)) < 1e-9
    lam = 0.5
    lap = quad(lambda L: math.exp(-lam * L) * 3 * L * L, 0, np.inf)[0]   # int e^{-lam L} dU, U=L^3
    assert abs(lap - 6 / lam ** 3) < 1e-9
    S = 4 * KAPPA
    assert abs(S / 4 / (2 * eta) ** 0 - KAPPA) < 1e-15 and abs(S / 3 - 4 * KAPPA / 3) < 1e-15

def test_q_prime_partial_fractions():
    """F2 : q' = sum_rho (s-rho)^-2 - 1/(s-1)^2 + O(1/|s|), contrôle à 300 zéros."""
    from explicit_formula import load_zeros
    gam, _ = load_zeros()
    for s in [mp.mpc(0.75, 20.0), mp.mpc(0.9, 60.3)]:
        q = lambda z: -mp.zeta(z, derivative=1) / mp.zeta(z)
        qp = mp.diff(q, s)
        S = sum(1 / (s - (0.5 + 1j * g)) ** 2 + 1 / (s - (0.5 - 1j * g)) ** 2 for g in gam) - 1 / (s - 1) ** 2
        assert abs(qp - S) < 1.0 / abs(s)

def test_nb_gram_basic():
    from nyman_beurling import G, chi_rho, EULER_GAMMA as eg
    assert abs(G(1, 1) - (math.log(2 * math.pi) - eg)) < 1e-11
    assert abs(G(3, 3) - G(1, 1) / 3) < 1e-11 and abs(G(2, 4) - G(1, 2) / 2) < 1e-11
    assert abs(chi_rho(1) - (1 - eg)) < 1e-15

def test_nb_d2_bounds():
    """d_N^2 décroît, reste >= kappa/log N (borne inférieure de Burnol, sous RH+zéros simples attendue = kappa) et <= E(V_N)."""
    from nyman_beurling import d2_optimal, norm2_of_combination
    from rh_core import mobius_sieve
    mu = mobius_sieve(50); prev = 1.0
    for N in (5, 10, 15):
        d2 = d2_optimal(N, dps=40)
        assert d2 < prev and d2 > KAPPA / math.log(N)
        lN = math.log(N)
        EV = norm2_of_combination({k: float(mu[k]) * (1 - math.log(k) / lN) for k in range(1, N) if mu[k] != 0})
        assert d2 <= EV + 1e-12
        prev = d2

def test_local_s2_identity_and_eta_model():
    """Re(A conj u) = 2[Re b/|rho|^2 - 1/|rho|^4] et coefficients eta^-2, eta^-1 du modèle local (40 zéros)."""
    from explicit_formula import load_zeros, _coeffs
    gam, c0 = load_zeros(40); A, u = _coeffs(gam, c0)
    rho = 0.5 + 1j * gam; b = 2 * c0 - 2 * g
    lhs = np.real(A * np.conj(u)); rhs = 2 * (b.real / np.abs(rho) ** 2 - 1 / np.abs(rho) ** 4)
    assert np.max(np.abs(lhs - rhs)) < 1e-12
    allrho = np.concatenate([rho, np.conj(rho)]); allb = np.concatenate([b, np.conj(b)])
    kN = np.sum(1 / np.abs(allrho) ** 2); s2 = np.sum(allb.real / np.abs(allrho) ** 2 - 1 / np.abs(allrho) ** 4); s1 = np.sum(np.abs(u) ** 2)
    eta = 0.02; dt = eta / 6; t = np.arange(0, gam[-1] + 60, dt) + dt / 2; s = 0.5 + eta + 1j * t
    G = np.zeros_like(s)
    for r, bb in zip(allrho, allb):
        G += 2 / (s - r) ** 2 + bb / (s - r)
    I = 2 * np.sum(np.abs(G) ** 2 / np.abs(s) ** 2) * dt / (2 * math.pi)
    assert abs((eta ** 3 * I - kN - s2 * eta) / eta ** 2 - s1) < 0.06 * s1 + 0.02

def test_function_field_analog():
    """Analogue corps de fonctions : Q cubique si |alpha|=sqrt p, exponentiel sinon ; Hasse sur toutes les courbes F_31."""
    def Qm(a, p, M):
        sn = [2, a]
        for n in range(2, M + 2): sn.append(a * sn[-1] - p * sn[-2])
        q = {n: -sn[n] for n in range(1, M + 1)}
        c = {n: sum(q[i] * q[n - i] for i in range(1, n)) - n * q[n] for n in range(1, M + 1)}
        acc, Q = 0, 0.0
        for N in range(1, M + 1):
            acc += c[N]; Q += float(acc * acc) / float(p ** N) * (1 - 1 / p)
        return Q
    p = 101
    r = Qm(10, p, 60) / 60 ** 3
    assert 1.5 < r < 5
    assert Qm(25, p, 40) / 40 ** 3 > 1e12
    p = 31; x = np.arange(p); sq = np.zeros(p, dtype=int)
    for y in range(p): sq[(y * y) % p] += 1
    amax = 0
    for A in range(p):
        for B in range(p):
            if (4 * A ** 3 + 27 * B ** 2) % p == 0: continue
            amax = max(amax, abs(p + 1 - (1 + int(np.sum(sq[(x ** 3 + A * x + B) % p])))))
    assert amax <= 2 * math.sqrt(p)

def test_nb_extension_table():
    import csv
    rows = list(csv.DictReader(open(Path(__file__).resolve().parents[1] / "data" / "nb_gram_dN_ext.csv")))
    for r in rows:
        if int(r["N"]) >= 40:
            assert 0.98 * KAPPA < float(r["d2_logN"]) < 1.08 * KAPPA
    assert all(float(a["d2"]) > float(b["d2"]) for a, b in zip(rows, rows[1:]))


def test_source_localization_single_mode():
    """V4.1 : une source synthétique est localisée sur une petite grille (beta,gamma)."""
    t = np.linspace(0.0, 12.0, 600)
    y = synthetic_source_signal(t, [(0.58, 17.0)])
    betas = [0.50, 0.54, 0.58, 0.62]
    gammas = [16.0, 16.5, 17.0, 17.5, 18.0]
    P = matched_filter_map(y, t, betas, gammas)
    i, j = np.unravel_index(np.argmax(P), P.shape)
    assert betas[i] == 0.58 and gammas[j] == 17.0, (betas[i], gammas[j])


def test_morlet_growth_rate_single_mode():
    """V4.1 : la pente d'enveloppe récupère beta-1/2 sur un mode isolé."""
    t = np.linspace(0.0, 18.0, 900)
    y = synthetic_source_signal(t, [(0.61, 20.0)])
    env = morlet_demodulated_envelope(y, t, gamma=20.0, sigma_t=0.7)
    slope = envelope_growth_rate(env, t, trim=0.20)
    assert abs(slope - 0.11) < 0.012, slope


def test_visibility_degrades_for_close_sources_and_laplacian_constant():
    """V4.1 : sources proches moins observables; Laplacien régularisé tue le mode constant."""
    t = np.linspace(0.0, 15.0, 750, endpoint=False)
    sep = visibility_metrics(t, [(0.5, 12.0), (0.5, 19.0)])
    close = visibility_metrics(t, [(0.5, 12.0), (0.5, 12.08)])
    assert sep["sigma_min"] > close["sigma_min"], (sep, close)
    z = regularized_laplacian(np.ones_like(t), t[1]-t[0], lam=0.01)
    assert np.max(np.abs(z)) < 1e-10


def test_schrodinger_zero_energy_roundtrip():
    """V4.2 : beta-1/2 devient exactement la partie imaginaire de l'énergie effective."""
    for beta, gamma in [(0.5, 14.134725), (0.61, 20.0), (0.43, 31.2)]:
        E = energy_from_zero(beta, gamma)
        b2, g2 = zero_parameters_from_energy(E)
        assert abs(b2-beta) < 1e-14 and abs(g2-gamma) < 1e-14
        assert abs(E.imag - (beta-0.5)) < 1e-14
        assert abs(norm_growth_rate(beta) - 2*(beta-0.5)) < 1e-14


def test_schrodinger_real_box_is_self_adjoint():
    """V4.2 : un potentiel réel donne un Hamiltonien hermitien et un spectre réel."""
    x = np.linspace(0.0, 1.0, 160)
    H, xi = schrodinger_matrix_1d(x, 0.0)
    assert self_adjointness_defect(H) < 1e-14
    vals, vecs = stationary_eigenpairs(H, k=3)
    assert np.max(np.abs(vals.imag)) < 1e-13
    # Infinite box: E1 -> pi^2/2 for m=hbar=1.
    assert abs(vals[0].real - math.pi**2/2) < 2e-3


def test_schrodinger_complex_potential_source_rate():
    """V4.2 : Im(V)=eta produit Im(E)=eta et un taux de norme 2 eta."""
    eta = 0.08
    x = np.linspace(0.0, 1.0, 120)
    H, xi = schrodinger_matrix_1d(x, 1j*eta)
    assert self_adjointness_defect(H) > 0
    vals, vecs = stationary_eigenpairs(H, k=1)
    assert abs(vals[0].imag-eta) < 1e-10
    psi = vecs[:,0]
    src = continuity_source_density(psi, 1j*eta)
    assert abs(np.sum(src) - 2*eta*np.sum(np.abs(psi)**2)) < 1e-10


def test_arithmetic_generator_rh_like_metric_certificate():
    """V4.3 : deux modes beta=1/2 donnent un H similaire à un Hermitien avec M>0."""
    dt = 0.002
    t = np.arange(0.0, 0.42, dt)
    mix = np.array([[1.0, 0.35+0.10j], [0.20-0.15j, 1.0]], dtype=complex)
    Z = modal_state_matrix(t, [(0.5, 14.0), (0.5, 21.0)], mixing=mix)
    A = fit_propagator(Z)
    H = effective_generator(A, dt)
    M, vals, cond = spectral_metric(H, imag_tol=1e-8)
    assert M is not None, (vals, cond)
    assert np.max(np.abs(vals.imag)) < 1e-8
    assert metric_self_adjointness_defect(H, M) < 1e-8
    assert metric_unitarity_defect(A, M) < 1e-8


def test_arithmetic_generator_offline_mode_rejected():
    """V4.3 : un mode beta>1/2 laisse une énergie complexe et échoue au certificat M>0."""
    dt = 0.002
    t = np.arange(0.0, 0.42, dt)
    mix = np.array([[1.0, 0.35+0.10j], [0.20-0.15j, 1.0]], dtype=complex)
    Z = modal_state_matrix(t, [(0.5, 14.0), (0.60, 21.0)], mixing=mix)
    H = effective_generator(fit_propagator(Z), dt)
    M, vals, cond = spectral_metric(H, imag_tol=1e-6)
    assert M is None
    assert abs(np.max(vals.imag) - 0.10) < 1e-6, vals


def test_effective_generator_recovers_zero_dictionary():
    """V4.3 : H_eff récupère -gamma+i(beta-1/2) sur un mode exact."""
    dt = 0.003
    t = np.arange(0.0, 0.3, dt)
    beta, gamma = 0.57, 17.0
    Z = modal_state_matrix(t, [(beta, gamma)])
    H = effective_generator(fit_propagator(Z), dt)
    E = H[0,0]
    assert abs(E.real + gamma) < 1e-8, E
    assert abs(E.imag - (beta-0.5)) < 1e-8, E

def test_generator_real_signal_zeta_bias():
    """v4.4 : sur le vrai signal psi, ESPRIT retrouve gamma_1 à 1e-2 mais Re(lambda) est biaisé (jamais exactement 0)."""
    from rh_core import von_mangoldt_sieve
    from explicit_formula import load_zeros
    N = 1_000_000
    psi = np.cumsum(von_mangoldt_sieve(N)); gam, _ = load_zeros()
    dt = 0.02; t = np.arange(3.0, math.log(N) - 0.01, dt); x = np.exp(t); i = np.floor(x).astype(int)
    y = np.exp(-t / 2) * (psi[i] - x + math.log(2 * math.pi))
    n = len(y); L = n // 2
    H = np.array([y[k:k + L] for k in range(n - L + 1)]).T
    U, s_, Vh = np.linalg.svd(H, full_matrices=False)
    Us = U[:, :16]; Am = np.linalg.pinv(Us[:-1]) @ Us[1:]
    lm = np.log(np.linalg.eigvals(Am).astype(complex)) / dt
    pos = lm[lm.imag > 0]; z1 = pos[np.argmin(abs(pos.imag - gam[0]))]
    assert abs(z1.imag - gam[0]) < 0.02
    assert abs(z1.real) < 0.05
    assert max(abs(pos.real)) > 0.0        # le biais est strictement non nul : aucun mode n'est exactement sur la droite

def test_second_order_signal_is_jordan_block():
    """v4.4 : un signal (A t + u) e^{i g t} (type G, double pôle) donne un propagateur DÉFECTIF (bloc de Jordan).
    Le certificat par défaut (cond(V) <= 1e12) l'accepte à tort, mais la métrique obtenue est dégénérée (cond(M) > 1e10) :
    le critère de coercivité uniforme (c|u|^2 <= u*Mu <= C|u|^2) échoue. Un contrôle sur cond(M) est nécessaire."""
    from arithmetic_generator import fit_propagator, effective_generator, spectral_metric
    dt = 0.01; t = np.arange(0.0, 1.5, dt); g_ = 14.1347
    Z = np.vstack([np.exp(1j * g_ * t), t * np.exp(1j * g_ * t)])
    H = effective_generator(fit_propagator(Z), dt)
    assert np.linalg.matrix_rank(H - np.mean(np.linalg.eigvals(H)) * np.eye(2), tol=1e-6) == 1     # non diagonalisable
    M, vals, cond = spectral_metric(H, imag_tol=1e-6)          # garde-fous par défaut
    assert M is not None and np.linalg.cond(M) > 1e10
    assert spectral_metric(H, imag_tol=1e-6, metric_cond_max=1e8)[0] is None       # garde-fou v4.4 sur cond(M)

def test_metric_certificate_is_equivalent_to_real_spectrum():
    """v4.4 : pour H diagonalisable, M>0 avec H*M=MH existe ssi le spectre est réel : le certificat n'apporte aucune information
    au-delà de Im(lambda)=0."""
    from arithmetic_generator import spectral_metric, metric_self_adjointness_defect
    rng = np.random.default_rng(3)
    V = rng.standard_normal((5, 5)) + 1j * rng.standard_normal((5, 5))
    real_spec = np.array([1.0, 2.5, -3.0, 7.0, 0.3])
    H = V @ np.diag(real_spec) @ np.linalg.inv(V)
    M, vals, cond = spectral_metric(H, imag_tol=1e-8, cond_max=1e12)
    assert M is not None and metric_self_adjointness_defect(H, M) < 1e-8
    H2 = V @ np.diag(real_spec + 1j * np.array([0, 0, 0, 0, 1e-3])) @ np.linalg.inv(V)
    assert spectral_metric(H2, imag_tol=1e-8, cond_max=1e12)[0] is None

def test_generator_dh_ghost_mode_in_data():
    """v4.4 : sur DH, le mode de plus grande partie réelle trouvé n'est PAS le zéro hors droite connu (fantôme)."""
    import csv
    rows = [r for r in csv.DictReader(open(Path(__file__).resolve().parents[1] / "data" / "generator_real_signal.csv")) if r["objet"] == "DH" and r["ordre"] == "30"]
    top = max(rows, key=lambda r: float(r["Re_beta_moins_demi"]))
    assert abs(float(top["beta_moins_demi_vrai"])) < 1e-6          # le plus "hors ligne" des modes pointe un zéro SUR la droite
    off = [r for r in rows if abs(float(r["Im"]) - 85.699) < 0.1][0]
    assert 0.15 < float(off["Re_beta_moins_demi"]) < 0.3085 + 1e-6    # le vrai zéro hors droite est sous-estimé

def test_docs_conventions_v45():
    """v4.5 : reliquat a_1 supprimé de L6.2 ; la convention log(1+Q) est employée dans l'énoncé de L6."""
    root = Path(__file__).resolve().parents[1]
    t = open(root / "preuves" / "LEMMES_RIGOUREUX.md", encoding="utf-8-sig").read()
    assert "a_1<a" not in t and "\\log(1+Q(X))" in t
    n = open(root / "preuves" / "SYNTHESIS_NOTE_EN.md", encoding="utf-8-sig").read()
    assert "log(1+Q(X))/log X" in n
    assert (root.parent / "1_Presentation" / "03_Dossier_de_relecture_EN.docx").exists() or (root.parent / "4_Archives" / "NON_PUBLIE.md").exists()

def test_kappa_is_twice_first_li_coefficient():
    """kappa = 2+gamma-log(4 pi) = 2*lambda_1, lambda_1 = sum_rho 1/rho = 1+gamma/2-(1/2)log(4 pi) (valeur classique)."""
    lam1 = 1 + g / 2 - 0.5 * math.log(4 * math.pi)
    assert abs(KAPPA - 2 * lam1) < 1e-15 and abs(lam1 - 0.0230957) < 1e-6
    from explicit_formula import load_zeros
    gam, _ = load_zeros()
    partial = np.sum(1.0 / (0.25 + gam ** 2))                  # sum_{rho} Re(1/rho) pour gamma>0, = lambda_1 si RH (sommes symétriques)
    tail = (math.log(gam[-1] / (2 * math.pi)) + 1) / (2 * math.pi * gam[-1])
    assert abs(partial + tail - lam1) < 3e-4

def test_h3_gap_statistics():
    """v4.7 : noyau croisé d'intégrale nulle ; les 300 premiers zéros n'ont pas d'écart normalisé < 0,25 ; E[1/s] finie."""
    import csv
    from scipy.integrate import quad
    for eta in (0.02, 0.2):
        assert abs(quad(lambda x: (8 * eta ** 3 - 6 * eta * x * x) / (4 * eta ** 2 + x * x) ** 3, -np.inf, np.inf)[0]) < 1e-10
    d = {r["cle"]: float(r["valeur"]) for r in csv.DictReader(open(Path(__file__).resolve().parents[1] / "data" / "h3_gaps.csv"))}
    assert d["min_ecart_normalise"] > 0.25 and 0.8 < d["E_inverse_s"] < 2.0
    assert d["S_pair_N300"] > d["S_pair_N100"] > d["S_pair_N25"] > 0

def test_protocol_document_present():
    """v4.8 : le document de protocole est présent et contient les sections attendues (Partie A, garde-fous cognitifs, Partie B)."""
    import zipfile
    f = Path(__file__).resolve().parents[2] / "2_Methode" / "Protocole_multi_agents_et_panorama_physique_RH.docx"
    assert f.exists()
    xml = zipfile.ZipFile(f).read("word/document.xml").decode("utf-8")
    for needle in ("Partie A", "Garde-fous cognitifs", "Partie B", "Bruijn", "Registre des affirmations"):
        assert needle in xml, needle

def test_audit_bench_scorer():
    """v4.9/v5.3 : le corpus a 20 erreurs et 6 leurres ; la notation donne rappel 1 pour l'auditeur parfait, 0 pour le vide, et pénalise les fausses alarmes."""
    import json, importlib.util
    root = Path(__file__).resolve().parents[2] / "2_Methode" / "Banc_d_audit"
    corpus = json.load(open(root / "planted_errors.json", encoding="utf-8-sig"))
    assert len(corpus["errors"]) == 21 and len(corpus["decoys"]) == 7
    spec = importlib.util.spec_from_file_location("score_auditor", root / "score_auditor.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    ids = [e["id"] for e in corpus["errors"]]
    r = mod.score(ids, corpus); assert r["recall"] == 1.0 and r["precision"] == 1.0 and r["false_alarm_rate"] == 0.0
    assert mod.score([], corpus)["recall"] == 0.0
    r2 = mod.score(ids + ["D01", "D02"], corpus); assert r2["false_alarm_rate"] > 0 and r2["precision"] < 1.0
    assert mod.score(["E01", "X99"], corpus)["unknown_ids"] == ["X99"]
    assert (root.parent.parent / "README.md").exists()
    assert (root.parent / "Plan_d_impact.md").exists()



def test_energy_zeta_matches_weighted_energy():
    """V5.2: Z_E(1/2+eta) is exactly the damped energy Q_eta on a finite truncation."""
    from rh_core import arithmetic_c_via_lambda, C_partial, H_eta_truncated
    from energy_dimension import energy_zeta_truncated
    N = 5000
    c = arithmetic_c_via_lambda(N)
    C = C_partial(c)
    for eta in (0.05, 0.17, 0.4):
        lhs = energy_zeta_truncated(C, 0.5 + eta, N)
        rhs = H_eta_truncated(C, eta, N)
        assert abs(lhs-rhs) < 1e-10 * (1+abs(rhs)), (eta, lhs, rhs)


def test_energy_dimension_from_power_growth():
    """V5.2: the finite-scale dimension recovers 1/2+alpha/2 for Q~X^alpha."""
    from energy_dimension import effective_dimension_from_Q
    alpha = 0.36
    X = np.array([1e20, 1e40, 1e80])
    Q = X**alpha
    D = effective_dimension_from_Q(X, Q)
    target = 0.5 + alpha/2
    assert abs(D[-1]-target) < 1e-5, (D[-1], target)


def test_finite_energy_zeta_formula_vs_quadrature():
    """V5.2: exact pair-average pole formula agrees with direct integration."""
    from scipy.integrate import quad
    from energy_dimension import finite_energy_zeta, finite_model_B
    rho = np.array([0.5+3j, 0.5-3j])
    A = np.array([1+0.2j, 1-0.2j])
    u = np.array([0.3-0.1j, 0.3+0.1j])
    s = 0.9 + 0.2j
    exact = finite_energy_zeta(s, rho, A, u)
    def part(t, imag=False):
        B = finite_model_B(np.array([t]), rho, A, u)[0]
        z = B*B*np.exp(-2*(s-0.5)*t)
        return float(z.imag if imag else z.real)
    num = quad(lambda t: part(t, False), 0, np.inf, limit=300)[0] + 1j*quad(lambda t: part(t, True), 0, np.inf, limit=300)[0]
    assert abs(exact-num) < 1e-7, (exact, num)


def test_energy_complex_dimensions_RH_and_offline():
    """V5.2: RH modes give Re pole=1/2; an off-line conjugate pair gives a real pole at beta."""
    from energy_dimension import finite_complex_dimensions
    rho_rh = np.array([0.5+14j,0.5-14j,0.5+21j,0.5-21j])
    p = finite_complex_dimensions(rho_rh)
    assert np.max(np.abs(p.real-0.5)) < 1e-14
    beta, gamma = 0.63, 7.0
    rho_off = np.array([beta+1j*gamma,beta-1j*gamma])
    po = finite_complex_dimensions(rho_off)
    assert np.min(np.abs(po-beta)) < 1e-14
    assert abs(np.max(po.real)-beta) < 1e-14


def test_attack_audit_v53():
    """v5.3 : reproduction du tableau reçu (projection mu + a), témoins, identité E_perp et discrimination par K(L)."""
    import csv
    d = Path(__file__).resolve().parents[1] / "data"
    fam = {int(r["N"]): r for r in csv.DictReader(open(d / "attack_nb_family.csv"))}
    for N, v in ((20, 0.01956), (50, 0.01443), (100, 0.01363)):
        assert abs(float(fam[N]["mu_a_libres"]) - v) < 2e-5
    for N in (50, 100, 150, 200):
        assert float(fam[N]["deg1"]) > 2 * float(fam[N]["mu_a_libres"])          # la courbure en log n est indispensable
        assert abs(float(fam[N]["alpha_libre"]) - 1) < 0.03                      # alpha ~ 1
        assert abs(float(fam[N]["beta_proj"]) * math.log(N) ** 2 + 1.3) < 0.15   # beta_N ~ -1.3 / log^2 N
    ctr = {r["famille"]: r for r in csv.DictReader(open(d / "attack_controls.csv"))}
    c2 = [v for k, v in ctr.items() if k.startswith("C2")][0]; c3 = [v for k, v in ctr.items() if k.startswith("C3")][0]
    c5 = [v for k, v in ctr.items() if k.startswith("C5")][0]; r1 = [v for k, v in ctr.items() if k.startswith("R1")][0]
    assert float(c3["e2_N100"]) < float(c2["e2_N100"]) < float(c5["e2_N100"]) < float(r1["e2_N100"])
    ident = {r[""]: float(r["valeur"]) for r in csv.DictReader(open(d / "attack_identities.csv"))}
    assert ident["A_identite_max_ecart"] < 1e-15 and abs(ident["A_kappa"] - KAPPA) < 1e-15
    K = [(r["objet"], int(r["L"]), float(r["K"])) for r in csv.DictReader(open(d / "attack_K_of_L.csv"))]
    z = [k for o, L, k in K if o == "zeta"]; h = [k for o, L, k in K if o == "DH"]
    assert z == sorted(z) and max(z) < 4 * KAPPA and h == sorted(h) and h[-1] > 4 * KAPPA
    # decomposition : la somme des morceaux redonne e^2
    for r in csv.DictReader(open(d / "attack_decomposition.csv")):
        tot = float(r["un"]) + float(r["croise"]) + float(r["rang1_1_sur_ab"]) + float(r["rang1_quart"]) + float(r["canal_gcd"]) + float(r["delta"])
        assert abs(tot - float(r["total"])) < 1e-9

def test_attack_iter_results():
    """v5.4 : résultats itératifs de l'attaque 2 (Gram sans carré) : plateau de {mu,a} < 1,5 kappa/log N, optimum sans carré proche de kappa/log N."""
    import csv
    f = Path(__file__).resolve().parents[1] / "data" / "attack_iter_results.csv"
    rows = sorted(csv.DictReader(open(f)), key=lambda r: int(r["N"]))
    assert len(rows) >= 10 and int(rows[-1]["N"]) >= 500
    for r in rows:
        assert 1.1 < float(r["mu_a_rk"]) < 1.5
        assert 0.95 < float(r["opt_sansCarre_rk"]) < 1.1
        assert float(r["opt_sansCarre"]) <= float(r["poly_x_deg5"]) + 1e-9
        assert -1.45 < float(r["beta_log2N"]) < -1.0

def test_rh_heuristic_v55():
    """v5.5 : le terme principal sous RH ne décrit pas N <= 998 ; second terme stable pour 1 - x ; ordre par courbure en 0."""
    import csv
    d = Path(__file__).resolve().parents[1] / "data"
    rows = list(csv.DictReader(open(d / "rh_heuristic_test.csv", encoding="utf-8-sig")))
    R = {(r["famille"], int(r["N"])): float(r["R"]) for r in rows}
    lin = [k for k in {f for f, _ in R} if k.startswith("P1")][0]
    c100 = (R[(lin, 100)] - 1) * math.log(100); c998 = (R[(lin, 998)] - 1) * math.log(998)
    assert 70 < c100 < 85 and abs(c100 - c998) < 2                        # e^2 ~ kappa/L + ~3,6/L^2
    get = lambda p: R[([k for k in {f for f, _ in R} if k.startswith(p)][0], 998)]
    assert get("P7") < get("P3") < get("P6") < get("P5") < get("P4")       # ordre par |P''(0)|
    fl = list(csv.DictReader(open(d / "rh_heuristic_flatness.csv")))
    for k in ("3", "4", "5", "6", "8"):
        v = [float(r["e2_logN_k"]) for r in fl if r["k"] == k]
        assert max(v) - min(v) < 0.25                                       # stable en N

def test_pole_cancellation_v56():
    """v5.6 : e^2 = beta^2 Q(N) + T_N exactement ; b_N -> -1 - 2 gamma/log N ; plateau jusqu'à 1e5 ; part beta^2 Q = (4/3) b^2 Q/((4k/3)L^3)."""
    import csv
    d = Path(__file__).resolve().parents[1] / "data"
    for r in csv.DictReader(open(d / "pole_cancellation_check.csv")):
        assert float(r["ecart_rel"]) < 1e-6          # limité par la troncature de la queue (≈ 5e-8)
    bN = {int(r["N"]): float(r["b_N"]) for r in csv.DictReader(open(d / "pole_cancellation_bN.csv"))}
    for N in (1000, 10000, 100000, 1000000, 10000000):
        assert abs((bN[N] + 1) * math.log(N) + 2 * g) < 0.6
    assert abs(bN[10000000] + 1) < abs(bN[1000] + 1)
    for r in csv.DictReader(open(d / "pole_cancellation_extension.csv")):
        assert 1.2 < float(r["e2_pc_rk"]) < 1.4
        pred = 4 / 3 * float(r["b_N"]) ** 2 * float(r["Q_sur_4k3L3"])
        assert abs(pred - float(r["part_beta2Q_rk"])) < 1e-9

if __name__ == "__main__":
    fails = 0
    count = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            count += 1
            try:
                fn()
                print("OK  ", name)
            except AssertionError as e:
                fails += 1
                print("FAIL", name, e)
    print(f"{count-fails}/{count} tests OK")
    sys.exit(1 if fails else 0)
