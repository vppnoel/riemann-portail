import sys, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))

from dark_residual import compression_components
from dual_lock import compression_accurate, KINDS
from dual_lock_audit import generalized_decomposition


def _gram(comp, kind):
    return comp['conductor']/math.log(KINDS[kind].q/math.pi)


def test_same_run_component_matrix_reconciliation():
    _, comp = compression_components(86.0,'DH',half_width=2.5,dimension=5,
                                     frequency_step=0.6,arch_dt=0.02,correlation_eps=2e-8)
    _, M = compression_accurate(86.0,'DH',half_width=2.5,dimension=5,
                                frequency_step=0.6,arch_dt=0.02,correlation_eps=2e-8)
    assert np.max(np.abs(M-comp['total'])) < 1e-12


def test_generalized_sign_separates_DH_and_control_at_86():
    vals={}
    for kind in ('DH','L_pair_chi5'):
        _, comp = compression_components(86.0,kind,half_width=2.5,dimension=5,
                                         frequency_step=0.6,arch_dt=0.02,correlation_eps=2e-8)
        metrics,_,_=generalized_decomposition(comp,_gram(comp,kind))
        vals[kind]=metrics['lambda_min_gen']
        assert metrics['closure_error_gen'] < 1e-9
        assert abs(metrics['g_norm']-1.0) < 1e-8
    assert vals['DH'] < -0.5
    assert vals['L_pair_chi5'] > 1.0


def test_generalized_result_stable_to_tighter_local_tolerance_at_dim5():
    vals=[]
    for eps in (1e-7,2e-8):
        _, comp = compression_components(86.0,'DH',half_width=2.5,dimension=5,
                                         frequency_step=0.6,arch_dt=0.02,correlation_eps=eps)
        metrics,_,_=generalized_decomposition(comp,_gram(comp,'DH'))
        vals.append(metrics['lambda_min_gen'])
    assert abs(vals[0]-vals[1]) < 1e-7
