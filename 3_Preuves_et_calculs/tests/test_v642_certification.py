"""Containment, refusal cases, serialization and independent rational replay."""
from pathlib import Path
from fractions import Fraction
from copy import deepcopy
import importlib.util
import json
import mpmath as mp
from v642_intervalles import (IntervalFamily,point,lower,upper,bernoulli,serial,
    contraction_certificate)
from v641_collisions import make_family,periodic_jet

ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text(encoding='utf-8-sig'))
def checker():
    spec=importlib.util.spec_from_file_location('v642_rational_check',ROOT/'scripts/check_v642_certificate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def test_exact_bernoulli_and_real_complex_serialization_are_unambiguous():
    assert bernoulli(1)==Fraction(-1,2)
    assert bernoulli(12)==Fraction(-691,2730)
    assert bernoulli(24)==Fraction(-236364091,2730)
    real=serial(point(Fraction(1,3)),30);complex_=serial(mp.iv.mpc(1,0),30)
    assert set(real)=={'lower','upper','binary_endpoints'}
    assert set(complex_)=={'real','imag'}
    assert Fraction(real['lower'])<Fraction(1,3)<Fraction(real['upper'])

def test_interval_jets_contain_hurwitz_references_and_refuse_an_uncovered_domain():
    pair=next(x for x in load('v639_couples_fixes.json')['pairs'] if x['id']=='k1_rpi_6')
    f=IntervalFamily(pair,digits=50,N=32,M=12);ref=make_family(pair,digits=100)
    for re,im in [('0.3','4.67'),('0.5','4.861023490998'),('0.7','5.05')]:
        x,y=f.jets(mp.iv.mpc(point(re),point(im)),2)
        with mp.workdps(90):
            s=mp.mpc(re,im);values=[periodic_jet(ref.anchor_table,s,2),periodic_jet(ref.direction_table,s,2)]
            for actual,expected in zip((x,y),values):
                for a,b in zip(actual,expected):
                    for part in ('real','imag'):
                        q=getattr(a,part);l,h=lower(q),upper(q)
                        assert mp.mpf(l.numerator)/l.denominator<=getattr(b,part)<=mp.mpf(h.numerator)/h.denominator
    try:f.jets(mp.iv.mpc(point('0.9'),point('4.9')))
    except ValueError:pass
    else:raise AssertionError('Uncovered rectangle treated as validated')

def test_contraction_refuses_noninclusion_and_noncontraction():
    mp.iv.dps=50;zero=point(0);one=point(1);I=[[one,zero],[zero,one]];C=[[Fraction(1),Fraction(0)],[Fraction(0),Fraction(1)]]
    good=contraction_certificate([Fraction(0),Fraction(0)],Fraction(1),[zero,zero],I,C)
    assert good['accepted']
    outside=contraction_certificate([Fraction(0),Fraction(0)],Fraction(1),[point(2),zero],I,C)
    assert not outside['accepted'] and not outside['strict_inclusion']
    bad=contraction_certificate([Fraction(0),Fraction(0)],Fraction(1),[zero,zero],[[point(-1),zero],[zero,point(-1)]],C)
    assert not bad['accepted'] and Fraction(bad['contraction_upper'])>=1

def test_rational_verifier_accepts_complete_certificate_and_rejects_tampering():
    c=checker();out=load('v642_certification.json');p=load('v642_protocole_verrouille.json');roots=load('v642_root_audit_inputs.json')['roots']
    assert c.verify(out,p,roots)['rational_checks_passed']
    broken=deepcopy(out);broken['contour']['arc_attempts'][0]['arcs'][17]['defect_upper']='1'
    try:c.verify(broken,p,roots)
    except AssertionError:pass
    else:raise AssertionError('A violated contour inequality was accepted')
    broken_roots=deepcopy(roots);broken_roots[0]['point_values'][0]['lower']='1';broken_roots[0]['point_values'][0]['upper']='1'
    try:c.verify(out,p,broken_roots)
    except AssertionError:pass
    else:raise AssertionError('A nonisolating root box was accepted')

def test_zero_configurations_follow_from_certified_boxes_not_approximate_discriminants():
    p=load('v642_protocole_verrouille.json');r=load('v642_certification.json');half=Fraction(p['root_box_halfwidth'])
    assert r['fold_certified'] and r['four_root_boxes_certified'] and r['contour']['accepted']
    for root in r['roots']:
        beta=Fraction(root['centre'][0]);h=Fraction(root['offset'])
        if h<0:assert beta==Fraction(1,2) and root['box_invariant_under_functional_partner']
        else:assert abs(beta-Fraction(1,2))>half and root['critical_line_excluded']
    protocol=load('v642_protocole_verrouille.json')
    import hashlib
    for name,digest in protocol['input_hashes'].items():assert hashlib.sha256((ROOT/'data'/name).read_bytes()).hexdigest()==digest
