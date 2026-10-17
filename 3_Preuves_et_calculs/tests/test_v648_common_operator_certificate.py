"""Independent arithmetic, frame and whole-domain operator-certificate checks."""
from pathlib import Path
from fractions import Fraction as F
from unittest import TestCase
import json,hashlib
import mpmath as mp
import numpy as np
import common_operator_certificate as c
import prime_centered_bridge as b
from certificate_lego import Port
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
def read():return json.loads((D/'v648_common_certificate_resultats.json').read_text())

def test_homogeneous_integer_polynomial_is_exact_legendre():
    for n in [0,1,2,4,8,80]:
        for x in [F(0),F(1,3),F(-2,5),F(1)]:
            p=c.exact_polynomial_value(c.legendre_integer_coefficients(n),x,2**n)
            # Independent Bonnet recurrence in exact rationals.
            a,d=F(1),x
            if n==0:actual=a
            else:
                for k in range(1,n):a,d=d,((2*k+1)*x*d-k*a)/(k+1)
                actual=d
            assert p==actual

def test_gauss_brackets_cover_all_roots_by_exact_sign_changes():
    b.setup(160);rows=read()['certificate']['gauss_positive_nodes'];coeff=c.legendre_integer_coefficients(80);last=F(0)
    assert len(rows)==40
    for r in rows:
        lo,hi=F(r['root_lo']),F(r['root_hi']);assert last<lo<hi<1;last=hi
        a=c.exact_polynomial_value(coeff,lo);d=c.exact_polynomial_value(coeff,hi);assert a*d<0
        assert b.endpoint_q(r['weight']['binary'][0])>0

def test_gauss_weights_enclose_independent_derivative_and_mass():
    b.setup(160);rows=read()['certificate']['gauss_positive_nodes'];lo=F(0);hi=F(0)
    for r in rows:
        a=b.endpoint_q(r['weight']['binary'][0]);d=b.endpoint_q(r['weight']['binary'][1]);lo+=a;hi+=d
    assert lo<=1<=hi # Positive half weights on[-1,1] sum to1.
    for r in rows[::13]:
        x=b.midpoint(b.I((F(r['root_lo'])+F(r['root_hi']))/2))
        actual=2/((1-x*x)*mp.diff(lambda z:mp.legendre(80,z),x)**2)
        assert b.midpoint(b.I(b.endpoint_q(r['weight']['binary'][0])))<=actual<=b.midpoint(b.I(b.endpoint_q(r['weight']['binary'][1])))

def test_outward_array_arithmetic_encloses_rational_endpoint_combinations():
    for x,y in [((F(-3,7),F(2,5)),(F(1,9),F(8,7))),((F(-3),F(-2)),(F(-4),F(-1)))]:
        xx=(c.aiv(x[0])[0],c.aiv(x[1])[1]);yy=(c.aiv(y[0])[0],c.aiv(y[1])[1])
        for f,op in [(c.add,lambda a,d:a+d),(c.mul,lambda a,d:a*d),(c.div,lambda a,d:a/d)]:
            a,d=f(xx,yy)
            for p in x:
                for q in y:assert c.fq(a)<=op(p,q)<=c.fq(d)
    with TestCase().assertRaises(ValueError):c.div((1.,1.),(-1.,1.))

def test_trig_polynomial_intervals_enclose_independent_high_precision_values():
    b.setup(160)
    for x in [F(-45),F(-7,3),F(0),F(1,2000),F(1),F(44),F(45)]:
        co,si=c.trig_interval(c.aiv(x));t=b.midpoint(b.I(x))
        for interval,actual in [(co,mp.cos(t)),(si,mp.sin(t))]:
            assert b.midpoint(b.I(c.fq(interval[0])))<=actual<=b.midpoint(b.I(c.fq(interval[1])))
    with TestCase().assertRaises(ValueError):c.trig_interval((46.,46.))

def test_exponential_polynomial_intervals_cover_generators():
    b.setup(160)
    for x in [F(-1,4),F(0),F(1,4)]:
        lo,hi=c.exp_interval(c.aiv(x));actual=mp.exp(b.midpoint(b.I(x)))
        assert b.midpoint(b.I(c.fq(lo)))<=actual<=b.midpoint(b.I(c.fq(hi)))

def test_bareiss_detects_indefinite_matrices_and_never_uses_int64_products():
    assert c.bareiss_spd([[2,1],[1,2]])[0]
    assert not c.bareiss_spd([[1,2],[2,1]])[0]
    huge=2**150;ok,pivots=c.bareiss_spd([[huge,0],[0,huge]])
    assert ok and int(pivots[-1])==huge*huge
    with TestCase().assertRaises(ValueError):c.bareiss_spd([[1,2],[0,1]])

def test_saved_matrix_spd_has_exact_positive_leading_minors():
    z=read()['certificate']
    for p in z['finite_matrix_certificates']:
        scale=int(p['scale']);tau=F(p['tau']);den=np.lcm(scale,tau.denominator) if scale*tau.denominator<2**63 else __import__('math').lcm(scale,tau.denominator)
        den=int(den);M=[[int(v) for v in row] for row in p['integer_matrix']]
        A=[[(int(tau*den) if i==j else 0)-M[i][j]*(den//scale) for j in range(40)] for i in range(40)]
        ok,pivots=c.bareiss_spd(A);assert ok and pivots==p['leading_minors']

def test_complete_protocol_and_code_are_hashed_and_scope_is_whole_domain():
    r=read();z=r['certificate'];assert r['complete'] and z['all_tests']
    assert r['protocol_sha256']==hashlib.sha256((D/'v648_protocole_operateur_commun.json').read_bytes()).hexdigest()
    assert r['source_sha256']==hashlib.sha256((ROOT/'3_Preuves_et_calculs/src/common_operator_certificate.py').read_bytes()).hexdigest()
    assert z['status']=='certified_local_all_tests' and z['support_range']=='0<S<=1/2'
    assert not z['global_RH_claim'] and not z['zero_data_used']
    assert F(z['mass_floor_lower'])>F(1,250) and F(z['mu_R_lower'])>F(1,2000)

def test_all_operator_error_categories_are_present_and_nonnegative():
    z=read()['certificate']
    for k in ['weight_error','kernel_midpoint_error','spatial_operator_error','matrix_roundoff_norm_upper']:
        assert F(z[k])>=0
    for x in z['sample_vector_epsilon']:assert 0<=F(x)<F(1,10**6)
    assert F(z['global_tail_floor'])>8 and z['spatial_nodes']==80 and z['frequency_cells']==90000
    assert F(z['weight_error'])>F(z['spatial_operator_error'])

def test_same_error_supplies_minorant_sources_tail_and_positive_schur():
    z=read()['certificate'];eta=8-F(z['C1_upper'])
    for i,x in enumerate(z['head_source_tail_contracts']):
        a=c.assemble_minorant_contract(F(z['finite_matrix_certificates'][i]['tau']),F(z['total_operator_errors'][i]),eta)
        assert a==x['assembly'] and a['status']=='certified_bounded_minorant_schur'
        assert F(a['schur_floor'])>F(1,250) and F(a['source_gram_operator_upper'])==F(z['total_operator_errors'][i])**2
        assert not a['original_Q_strong_sources_certified'] and a['metric']=='L2 mass'

def test_insufficient_minorant_and_wrong_form_do_not_become_RH_claims():
    assert c.assemble_minorant_contract(2,F(1,10),1)['status']=='inconclusive'
    assert c.assemble_minorant_contract(1,2,1)['status']=='inconclusive'
    for kwargs in [dict(metric='H1'),dict(unit='A_amp'),dict(form='Q_W_minus_eta_mass',mass_shift=1)]:
        with TestCase().assertRaises(ValueError):c.certify(Port(F(1,2),**kwargs))
    with TestCase().assertRaises(ValueError):c.certify(Port(F(3,8)))

def test_continuous_point_diagnostic_is_kept_separate():
    r=json.loads((D/'v648_common_operator_diagnostic.json').read_text())
    assert not r['certified'] and not r['new_positive_certificate'] and not r['global_RH_claim']
    assert r['cases'][0]['resolutions'][-1]['margin']>0 and len(r['cases'][0]['resolutions'])==2

def test_current_dictionary_prerequisites_and_source_scope_are_explicit():
    p=json.loads((D/'v648_parcours_pedagogique.json').read_text());assert len(p['lessons'])==40 and len(p['tools'])==16
    seen=set()
    for r in p['lessons']:
        assert set(r['prerequisites'])<=seen;seen.add(r['id'])
        assert r['legend'] and r['purpose'] and r['guard'] and r['math_svg'] and (ROOT/r['math_file']).exists()
    assert {'cardinal_frame','interpolation_error','operator_error','minorant_sources'}<=seen
    r=next(t for t in p['tools'] if t['id']=='minorant_assembly')
    assert 'forme originale' in r['limit'] and r['execution']

def test_current_support_and_global_obligations_are_not_confused():
    r=json.loads((D/'v648_etat_recherche.json').read_text())
    assert r['local_certificate']['maximum_support']=='1/2' and r['local_certificate']['head_form']=='bounded A_U minorant'
    assert not r['local_certificate']['original_Q_strong_sources_certified'] and not r['global_sign_certified']
    assert len(r['next_actions'])==4 and r['maturity_levels_unchanged']
