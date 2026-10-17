from pathlib import Path
import importlib.util
import json
import sys
import numpy as np
from scipy.linalg import toeplitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from weil_trace_intervals import (
    setup, I, A, H, lower, upper, mp, g_closed, arch_interval,
    gauss_rule, dh_coefficients,
)


def runner():
    spec = importlib.util.spec_from_file_location("v636_runner",ROOT/"scripts/run_v636_norme.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_closed_convolution_matches_independent_high_precision_integral():
    setup()
    a = mp.mpf(1)/50
    for x in (mp.mpf(0),a/2,a,3*a/2):
        val = mp.quad(lambda y: mp.cos(mp.pi*y/(2*a))**4
                      *mp.cos(mp.pi*(x-y)/(2*a))**4,[x-a,a])
        enclosed = g_closed(I(mp.nstr(x,85)))
        assert abs(val-(lower(enclosed)+upper(enclosed))/2) < mp.mpf("1e-55")
    edge = g_closed(I(2*A))
    assert lower(edge) <= 0 <= upper(edge)


def test_gauss_nodes_and_weights_reproduce_polynomial_moments():
    setup()
    rule = gauss_rule()
    for power in (0,1,2,15,30,31):
        val = sum((w*x**power for x,w in rule),I(0))
        exact = mp.mpf(0) if power%2 else mp.mpf(2)/(power+1)
        assert lower(val) <= exact <= upper(val)


def test_arch_interval_matches_independent_digamma_fourier_quadrature():
    setup()
    from prime_generator import arch_traces
    ns=np.array([0,9,40])
    ref=arch_traces(ns,.005,.02,5,1)
    for n,value in zip(ns,ref):
        enclosed,_=arch_interval(int(n))
        center=(lower(enclosed)+upper(enclosed))/2
        assert abs(float(center)-value) < 2e-15


def test_dh_interval_coefficients_match_direct_dirichlet_log_expansion():
    setup()
    c=dh_coefficients(30)
    from rejection import coeffs,log_derivative_coeffs
    old=log_derivative_coeffs(coeffs("DH",30)).real
    for n in range(2,31):
        center=(lower(c[n])+upper(c[n]))/2
        assert abs(float(center)-old[n]) < 1e-12
    # Valeur exacte indépendante au premier indice composé non-puissance.
    xi=(mp.sqrt(10-2*mp.sqrt(5))-2)/(mp.sqrt(5)-1)
    exact=(1+xi**2)*mp.log(6)
    assert lower(c[6]) <= exact <= upper(c[6])


def test_saved_intervals_enclose_centres_with_outward_radii():
    data=json.loads((ROOT/"data/v636_traces_intervalles.json").read_text())
    setup()
    assert len(data["centres"])==1115
    for center,radius,binary in zip(data["centres"],data["rayons"],data["intervalles_binaires"]):
        lo,hi=[mp.mpf(tuple(v)) for v in binary]
        assert mp.mpf(center)-mp.mpf(radius) <= lo <= hi <= mp.mpf(center)+mp.mpf(radius)
    mod=runner()
    bound=mod.trace_norm_bound(np.array(data["rayons"]))
    rep=json.loads((ROOT/"data/v636_norme.json").read_text())
    assert bound==rep["erreur_norme_traces"]


def test_negative_witness_revalidates_and_rejects_positive_counterexample():
    setup()
    mod=runner()
    saved=np.load(ROOT/"data/v636_temoin_negatif.npz")
    rep=json.loads((ROOT/"data/v636_norme.json").read_text())
    result,_=mod.negative_compression(toeplitz(saved["traces"]),saved["vecteurs"],rep["erreur_norme_traces"])
    assert result["negatif"] and result["dimension"]==25
    assert result["gershgorin_superieur"] < -6e-9
    positive,_=mod.negative_compression(np.eye(8),np.eye(8)[:,:3],0.)
    assert not positive["negatif"]
    excessive,_=mod.negative_compression(-np.eye(8),np.eye(8)[:,:3],1.)
    assert not excessive["negatif"]
