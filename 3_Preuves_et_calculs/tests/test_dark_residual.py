import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dual_lock import compression_accurate
from dark_residual import compression_components, residual_metrics


def test_components_close_to_dual_lock_matrix():
    _, M0 = compression_accurate(
        86.0, "DH", half_width=2.5, dimension=5, frequency_step=0.6,
        arch_dt=0.03, correlation_eps=5e-7,
    )
    _, comp = compression_components(
        86.0, "DH", half_width=2.5, dimension=5, frequency_step=0.6,
        arch_dt=0.03, correlation_eps=5e-7,
    )
    assert np.max(np.abs(M0 - comp["total"])) < 1e-10


def test_dark_residual_is_real_cancellation_for_DH_witness():
    _, comp = compression_components(
        86.0, "DH", half_width=2.5, dimension=5, frequency_step=0.6,
        arch_dt=0.03, correlation_eps=5e-7,
    )
    m = residual_metrics(comp)
    assert m["q_total"] < -0.3
    assert m["cancellation_ratio"] < 0.12
    assert m["residual_amplification"] > 8.0
    assert m["closure_error"] < 1e-10


def test_matched_L_control_keeps_positive_sign():
    _, comp = compression_components(
        86.0, "L_pair_chi5", half_width=2.5, dimension=5,
        frequency_step=0.6, arch_dt=0.03, correlation_eps=5e-7,
    )
    m = residual_metrics(comp)
    assert m["q_total"] > 0.0
    assert m["closure_error"] < 1e-10
