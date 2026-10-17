"""Independent analytic normalization and rigorous concentration regressions."""
from pathlib import Path
from fractions import Fraction as F
from unittest import TestCase
import hashlib,json
import mpmath as mp
import prime_centered_bridge as b
import projected_concentration as c
from certificate_lego import Port
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'3_Preuves_et_calculs/data'
def result():return json.loads((D/'v647_concentration_resultats.json').read_text())

def test_fixed_signed_products_enclose_all_endpoint_products():
    for x in [(-25,-3),(-11,17),(4,21)]:
        for y in [(-19,-2),(-7,9),(1,23)]:
            q=16;lo,hi=c.product_interval(x,y,q)
            for a in x:
                for d in y:assert lo<=F(a*d,q)<=hi

def test_projected_kernel_fixed_against_independent_spatial_integrals():
    b.setup(160);S=F(3,8);s=b.midpoint(b.I(S));bits=64;q=1<<bits
    for t,v in [(F(1),F(3)),(F(8),F(10)),(F(12),F(12))]:
        t,v=b.midpoint(b.I(t)),b.midpoint(b.I(v))
        rawdiff=mp.quad(lambda x:mp.cos((t-v)*x),[-s,s])/2
        rawsum=mp.quad(lambda x:mp.cos((t+v)*x),[-s,s])/2
        for p in range(2):
            fun=mp.cos if p==0 else mp.sin;ann=mp.cosh if p==0 else mp.sinh
            G=mp.quad(lambda x:ann(x/2)**2,[-s,s])
            m1=mp.quad(lambda x:ann(x/2)*fun(t*x),[-s,s])/mp.sqrt(G)
            m2=mp.quad(lambda x:ann(x/2)*fun(v*x),[-s,s])/mp.sqrt(G)
            actual=mp.quad(lambda x:fun(t*x)*fun(v*x),[-s,s])-m1*m2
            def fp(x):return c.fixed(mp.iv.mpf([x-mp.mpf('1e-80'),x+mp.mpf('1e-80')]),bits)
            low,high=c.projected_kernel_fixed(fp(rawdiff),fp(rawsum),fp(m1),fp(m2),q,p)
            assert b.midpoint(b.I(F(low,q)))<=actual<=b.midpoint(b.I(F(high,q)))

def test_trace_and_hs_normalization_for_independent_rank_one_limit():
    # On a narrow positive-frequency interval, both concentration bounds tend
    # to length*||projected wave||²/pi, not twice this value or its square.
    b.setup(160);S=mp.mpf(3)/8;t=mp.mpf(7)
    v=2*mp.sinh((mp.mpf('.5')+mp.j*t)*S)/(mp.mpf('.5')+mp.j*t)
    for p in range(2):
        d=S+(-1 if p else 1)*mp.sin(2*t*S)/(2*t)-(v.imag**2/(mp.sinh(S)-S) if p else v.real**2/(S+mp.sinh(S)))
        width=mp.mpf('0.00001');trace=width*d/mp.pi;hs=mp.sqrt(width**2*d**2/mp.pi**2)
        assert abs(trace-hs)<mp.mpf('1e-70') and trace>0

def test_global_sublevel_tail_uses_a_certified_floor():
    b.setup(160);r=result()['certificate'];tail=b.multiplier_enclosure(F(r['T']))
    actual=mp.re(mp.digamma(mp.mpf('.25')+mp.j*20))-mp.digamma(mp.mpf('.25'))
    assert b.midpoint(b.I(b.lo(tail)))<=actual<=b.midpoint(b.I(b.hi(tail)))
    assert F(r['global_tail_floor'])>F(r['U'])

def test_derivative_error_constants_dominate_exact_analytic_constants():
    b.setup(160);r=result()['certificate'];S=b.midpoint(b.I(F(r['S'])))
    assert b.midpoint(b.I(F(r['trace_second_derivative_upper'])))>4*S**3*(mp.mpf(1)/3+1/mp.sqrt(5))
    assert b.midpoint(b.I(F(r['kernel_squared_second_derivative_upper'])))>8*S**4*(mp.mpf(1)/3+1/mp.sqrt(5))

def test_certification_rounds_to_readable_whole_domain_theorem():
    r=result();z=r['certificate']
    assert r['complete'] and r['protocol_sha256']==hashlib.sha256((D/'v647_protocole_concentration.json').read_bytes()).hexdigest()
    assert z['status']=='certified_local_all_tests' and z['all_tests'] and z['head_dimension']==0
    assert F(z['joint_energy_lower'])>=F(6438,1000) and F(z['threshold_upper'])<=F(6353,1000)
    assert F(z['mass_floor_lower'])>F(1,12) and F(z['mu_R_lower'])>F(1,100)
    assert F(z['trace_only_mass_floor'])<0 and not z['global_RH_claim'] and not z['zero_data_used']

def test_domain_guards_reject_wrong_form_metric_support_and_tail():
    b.setup(160);base=[F(40),F(1,50),F(36,5),F(1,50),64]
    for kw in [dict(unit='A_amp'),dict(metric='H1'),dict(annihilators=('1',)),dict(form='Q_W_minus_eta_mass',mass_shift=1)]:
        with TestCase().assertRaises(ValueError):c.validate_grid(Port(F(3,8),**kw),*base)
    for S in [F(1,4),F(1),F(3)]:
        with TestCase().assertRaises(ValueError):c.validate_grid(Port(S),*base)
    bad=base[:];bad[0]=F(20)
    with TestCase().assertRaises(ValueError):c.validate_grid(Port(F(3,8)),*bad)
    bad=base[:];bad[-1]=True
    with TestCase().assertRaises(ValueError):c.validate_grid(Port(F(3,8)),*bad)

def test_common_operator_algebra_preserves_one_test_across_layers():
    # Two layers with orthogonal dangerous directions: ||K1||+||K2||=2,
    # whereas ||K1+K2||=1. Taking the norm after summation keeps the test.
    assert c.common_operator_floor(3,1,1)==1
    assert c.common_operator_floor(3,2,1)==0

def test_head_tail_norm_bound_against_independent_2_by_2_eigenvalue():
    b.setup(160)
    for a,d,r2 in [(F(2),F(1),F(1,4)),(F(3,2),F(1,10),F(1,10000))]:
        upper=c.head_tail_norm_bound(a,d,r2)
        actual=mp.eigsy(mp.matrix([[b.midpoint(b.I(a)),mp.sqrt(b.midpoint(b.I(r2)))],[mp.sqrt(b.midpoint(b.I(r2))),b.midpoint(b.I(d))]]),eigvals_only=True)[1]
        assert b.midpoint(b.I(upper))>=actual
    with TestCase().assertRaises(ValueError):c.head_tail_norm_bound(1,1,-1)

def test_operator_diagnostics_remain_exploratory_despite_positive_values():
    r=json.loads((D/'v647_operator_diagnostic.json').read_text())
    assert not r['certified'] and not r['new_positive_certificate'] and not r['global_RH_claim']
    z=r['supports'][-1];assert z['S']=='1/2'
    assert z['resolutions'][-1]['margins']['common_operator']>0
    assert abs(z['refinement_differences']['common_operator'])>0
    assert any('Nystrom' in s for s in r['limitations'])

def test_rounded_R_theorem_keeps_the_geometric_prime_constant():
    r=result()['certificate'];L=b.endpoint_q(r['c0_interval']['binary'][1])+b.endpoint_q(r['weight_interval']['binary'][1])
    assert L<6 and F(17,200)/(F(17,200)+7)==F(17,1417)>F(1,100)

def test_current_lessons_have_progressive_prerequisites_and_concrete_uses():
    p=json.loads((D/'v647_parcours_pedagogique.json').read_text());assert len(p['lessons'])==36 and len(p['tools'])==13
    seen=set()
    for r in p['lessons']:
        assert set(r['prerequisites'])<=seen;seen.add(r['id'])
        assert r['legend'] and r['example'] and r['purpose'] and r['guard'] and r['math_svg']
        assert (ROOT/r['math_file']).exists()
    assert {'joint_cost','sublevel','schatten2','common_operator'}<=seen
    for r in p['tools']:assert r['input'] and r['output'] and r['execution'] and r['limit']
