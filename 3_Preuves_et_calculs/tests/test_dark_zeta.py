import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dark_zeta import (
    build_signal, phase_randomize_preserve_power,
    tomo2_gram, multiplicative_defect,
    steinhaus_completely_multiplicative,
)


def test_phase_randomization_preserves_tomo2_circular_gram():
    _a, _c, _u, g = build_signal("zeta", N=4096, n_log=1024)
    gr = phase_randomize_preserve_power(g, seed=123)
    K = tomo2_gram(g, n_shifts=16, shift_step=5)
    Kr = tomo2_gram(gr, n_shifts=16, shift_step=5)
    assert np.max(np.abs(K - Kr)) < 1e-10


def test_multiplicative_defect_zero_for_zeta_and_random_completely_multiplicative():
    a, *_ = build_signal("zeta", N=4096, n_log=512)
    dz = multiplicative_defect(a, P=32)
    assert dz["defect_max"] < 1e-12
    ar = steinhaus_completely_multiplicative(4096, seed=7)
    dr = multiplicative_defect(ar, P=32)
    assert dr["defect_max"] < 1e-10


def test_DH_has_nonzero_multiplicative_defect():
    a, *_ = build_signal("DH", N=4096, n_log=512)
    d = multiplicative_defect(a, P=16)
    assert d["defect_normalized"] > 1e-3
