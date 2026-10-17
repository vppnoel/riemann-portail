from pathlib import Path
import sys,json,hashlib
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import multi_prime_compensation as c
import prime_centered_bridge as b
import mpmath as mp

def setup():b.setup(240)

def test_prime_powers_use_underlying_prime_and_exact_integer_factorization():
    assert c.prime_power(4)==(2,2,4) and c.prime_power(27)==(3,3,27)
    assert c.prime_power(6) is None and c.prime_power(997)==(997,1,997)
    for bad in [True,1,2.5]:
        try:c.prime_power(bad)
        except ValueError:pass
        else:raise AssertionError('invalid power accepted')

def test_activation_and_power_weight_are_interval_resolved():
    setup();rows=c.active_powers(F(7,10));assert [r['q'] for r in rows]==[2,3,4]
    w=rows[2]['weight'];exact=mp.log(2)/2
    assert b.lo(w)<=F(str(exact))<=b.hi(w)
    assert b.hi(w)<F(str(mp.log(4)/2))
    assert [r['q'] for r in c.active_powers(F(1,2))]==[2]

def test_joint_multiplier_matches_independent_digamma_phase_formula():
    setup();S=F(7,10)
    for t in [F(0),F(1,3),F(11),F(100)]:
        tt=mp.mpf(t.numerator)/t.denominator
        value=mp.re(mp.digamma(mp.mpf('0.25')+1j*tt/2))-mp.digamma(mp.mpf('0.25'))
        for p,m,q in [(2,1,2),(3,1,3),(2,2,4)]:value+=2*mp.log(p)/mp.sqrt(q)*(1-mp.cos(tt*mp.log(q)))
        v=c.joint_multiplier(t,S);assert b.lo(v)<=F(str(value))<=b.hi(v)

def test_joint_ratio_encloses_all_independent_segment_candidates():
    setup()
    for s in ['11/20','7/10','1']:
        S=mp.mpf(F(s).numerator)/F(s).denominator;rows=c.active_powers(s);result=c.joint_edge_payment(s)
        points=sorted([mp.mpf(0)]+[abs(mp.log(r['q'])-S) for r in rows]+[S])
        al=mp.mpf(F(result['alpha_lower']).numerator)/F(result['alpha_lower']).denominator
        au=mp.mpf(F(result['alpha_upper']).numerator)/F(result['alpha_upper']).denominator
        values=[]
        for a,z in zip(points,points[1:]):
            x=(a+z)/2;D=mp.mpf(0)
            for r in rows:
                d=mp.log(r['q']);w=mp.log(r['p'])/mp.sqrt(r['q'])
                D+=w*(int(x<S-d)+int(x>d-S))
            def J(d):return mp.atanh(mp.exp(-d/2))+mp.atan(mp.exp(-d/2))
            if D:values.append(D/(J(S-a)+J(S+a)))
        exact=max(values);assert al<=exact<=au

def test_overlapping_bands_count_twice_at_center():
    setup();r=c.joint_edge_payment(F(7,10));first=r['segments'][0]
    assert b.lo(c.active_powers(F(7,10))[0]['shift'])<F(7,10)
    den=first['density']['binary'];dv=mp.iv.mpf([b.midpoint(b.I(b.endpoint_q(v))) for v in den])
    w=c.active_powers(F(7,10))[0]['weight'];assert b.lo(dv)<=b.lo(2*w)<=b.hi(dv)
    assert b.lo(dv)>b.hi(w)

def test_joint_budget_improves_separate_payment_without_global_sign_claim():
    setup();r=c.joint_edge_payment(F(1));sep=sum((F(c.joint_edge_payment(1,[q])['alpha_upper']) for q in r['active_q']),F(0))
    assert F(r['alpha_upper'])<1<sep
    assert not r['Q_positive_certified'] and not r['global_RH_claim']

def test_entry_relative_payment_tends_down_and_does_not_claim_l2_continuity():
    setup();d=b.hi(mp.iv.log(b.I(3)));values=[F(c.joint_edge_payment(d/2+F(1,2**k),[3])['alpha_upper']) for k in [2,4,8,16,32]]
    assert all(a>z>0 for a,z in zip(values,values[1:]))

def test_conditional_sign_keeps_positive_energy_coefficient_and_authentication_guard():
    assert c.sufficient_sign(F(6,5),100,6)['status']=='inconclusive'
    good=c.sufficient_sign(F(1,5),8,6)
    assert good['status']=='positive_if_energy_premise_certified' and not good['premises_authenticated']
    assert c.sufficient_sign(F(4,5),8,6)['status']=='inconclusive'

def test_frozen_journal_hash_and_scope_are_preserved():
    r=json.loads((ROOT/'data/v649_joint_payment_resultats.json').read_text())
    assert r['source_sha256']==hashlib.sha256((ROOT/'src/multi_prime_compensation.py').read_bytes()).hexdigest()
    assert not r['extended_positive_support_certificate'] and not r['global_RH_claim']
    assert len(r['supports'])==7
    one=next(x for x in r['supports'] if x['S']=='1')
    assert F(one['alpha_upper'])<F(796,1000)<1<F(124,100)<F(one['separate_alpha_sum_lower'])

def test_enumeration_resource_guard_rejects_unbounded_sweep():
    setup()
    try:c.active_powers(10)
    except ValueError:pass
    else:raise AssertionError('resource ceiling ignored')

def test_interval_endpoint_activation_is_rejected_instead_of_omitted():
    setup();d=mp.iv.log(b.I(2))
    for S in [b.lo(d)/2,b.hi(d)/2]:
        try:c.active_powers(S)
        except ValueError:pass
        else:raise AssertionError('unresolved closed interval activation accepted')

def test_current_course_and_tools_have_ordered_prerequisites_and_scope():
    r=json.loads((ROOT/'data/v649_parcours_pedagogique.json').read_text());rows=r['lessons'];seen=set()
    assert len(rows)==43 and len(r['tools'])==19
    for x in rows:
        assert set(x['prerequisites'])<=seen
        assert x['math_svg'] and x['legend'] and x['purpose'] and x['guard']
        seen.add(x['id'])
    assert {'prime_phase','edge_multiplicity','joint_payment'}<=seen

def test_current_state_retains_prior_support_certificate_and_does_not_promote_diagnostic():
    r=json.loads((ROOT/'data/v649_etat_recherche.json').read_text())
    assert r['local_certificate']['maximum_support']=='1/2'
    assert not r['extended_positive_support_certificate'] and not r['global_sign_certified']
    d=json.loads((ROOT/'data/v649_multi_prime_diagnostic.json').read_text())
    assert not d['certified'] and not d['new_positive_certificate']
    for s in d['supports']:
        assert len(s['cases'])==3
        for case in s['cases']:assert len(case['resolutions'])==2
