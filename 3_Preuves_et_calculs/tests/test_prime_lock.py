import os, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from rejection import build, log_derivative_coeffs
from dark_zeta import steinhaus_completely_multiplicative
from prime_lock import (
    support_leakage,
    degree1_tower_defect,
    eulerize_lambda_degree1,
    prime_lock_metrics_from_coefficients,
    decompose_lambda,
)


def test_zeta_prime_lock_exact():
    _, lam, _ = build("zeta", 4096)
    assert support_leakage(lam) < 1e-24
    assert degree1_tower_defect(lam) < 1e-24
    assert np.max(np.abs(lam - eulerize_lambda_degree1(lam))) < 1e-10


def test_dirichlet_L_prime_lock_exact():
    _, lam, _ = build("L_chi5", 4096)
    assert support_leakage(lam) < 1e-24
    assert degree1_tower_defect(lam) < 1e-24


def test_DH_has_large_prime_power_leakage():
    _, lam, _ = build("DH", 4096)
    assert support_leakage(lam) > 0.5
    assert degree1_tower_defect(lam) > 0.3


def test_steinhaus_control_is_prime_locked():
    a = steinhaus_completely_multiplicative(4096, seed=7)
    m = prime_lock_metrics_from_coefficients(a, pole=False, n_log=512)
    assert m.support_leakage < 1e-22
    assert m.tower_defect < 1e-22


def test_decomposition_reconstructs_lambda():
    _, lam, _ = build("DH", 2048)
    d = decompose_lambda(lam)
    rec = d["prime"] + d["higher_prime_power"] + d["leakage"]
    assert np.max(np.abs(rec - lam)) < 1e-12
