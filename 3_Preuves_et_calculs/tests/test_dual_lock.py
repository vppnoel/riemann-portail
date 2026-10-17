import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dual_lock import compression_accurate, inertia, tent_fourier


def test_tent_fourier_even_on_real_axis():
    t = np.linspace(0.0, 10.0, 101)
    a = np.real(tent_fourier(t, 2.5, 7.0))
    b = np.real(tent_fourier(-t, 2.5, 7.0))
    assert np.max(np.abs(a - b)) < 1e-12


def test_compression_is_symmetric():
    _, M = compression_accurate(20.0, "L_pair_chi5", half_width=1.5,
                                dimension=3, frequency_step=0.7,
                                correlation_eps=1e-7)
    assert np.max(np.abs(M - M.T)) < 1e-10


def test_positive_control_near_first_DH_witness():
    _, M = compression_accurate(86.0, "L_pair_chi5", half_width=2.5,
                                dimension=5, frequency_step=0.6,
                                correlation_eps=5e-7)
    assert np.linalg.eigvalsh(M)[0] > -1e-6


def test_DH_has_robust_negative_witness_near_86():
    _, M = compression_accurate(86.0, "DH", half_width=2.5,
                                dimension=5, frequency_step=0.6,
                                correlation_eps=5e-7)
    assert np.linalg.eigvalsh(M)[0] < -1e-3
    assert inertia(M)[1] >= 1
