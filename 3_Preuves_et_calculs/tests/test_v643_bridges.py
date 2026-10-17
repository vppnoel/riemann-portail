"""Scenario branching, semantic invariance, singular Schur and independent checks."""
import sys,json
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'scripts'))
from bridge_planning import solve,bottom_up,utility,validate
from schur_bridge import append_contract,quadratic,psd
from run_v643_bridges import build_model,toy


def test_complementarity_and_document_invariance():
    m=toy();s=solve(m,4);assert s['value']==12
    assert set(s['first_choices'])=={'construction_a','construction_b'}
    for a in m['actions']:a['documents']=['rapport'+str(i) for i in range(10)]
    assert solve(m,4)==s
    m['capabilities'][0]['requires_any'].append(['a','b'])
    assert utility(m,{'a','b'})==12


def test_adaptive_results_are_not_completion_flags():
    m=dict(facts={k:{} for k in ['a','b','reward']},initial_facts=[],capabilities=[dict(id='r',weight=5,requires_any=[['reward']])],actions=[
      dict(id='observe',duration=[1,1],requires_any=[[]],outcomes=[dict(id='a',adds=['a']),dict(id='b',adds=['b'])]),
      dict(id='after_a',duration=[1,1],requires_any=[['a']],outcomes=[dict(id='ok',adds=['reward'])]),
      dict(id='after_b',duration=[1,1],requires_any=[['b']],outcomes=[dict(id='ok',adds=['reward'])])])
    assert solve(m,2)['value']==5 and solve(m,2)['first_choices']==['observe']
    m['actions'].pop();assert solve(m,2)['value']==0 and solve(m,2,'upper')['value']==5
    assert solve(m,1,done=['observe'])['value']==0


def test_scenario_duration_and_global_guard():
    m=toy();m['actions'][0]['duration']=[2,5]
    assert solve(m,4)['value']==6 and solve(m,4,'upper')['value']==12
    m['reserved_global_claims']=['a']
    try:validate(m)
    except ValueError:pass
    else:raise AssertionError('Unconditional global credit accepted')


def test_independent_graph_and_ties():
    for m in (toy(),build_model()):
      for b in range(11):
       for mode in ('lower','upper'):
        s=solve(m,b,mode);r=bottom_up(m,b,mode)
        assert s['value']==r['value'] and s['first_choices']==r['first_choices']
        assert solve(m,b,'lower')['value']<=solve(m,b,'upper')['value']


def test_singular_schur_range_and_square_identity():
    assert not append_contract([[0]],[1],100)['accepted']
    assert append_contract([[0]],[0],0)['accepted']
    r=append_contract([[1,1],[1,1]],[2,2],5)
    assert r['accepted'] and r['debt']==1
    G=[[2,0],[0,3]];c=[1,2];a=4;r=append_contract(G,c,a);z=r['solution']
    A=[G[0]+[c[0]],G[1]+[c[1]],c+[a]]
    for x1,x2,y in [(-2,3,5),(1,2,-1),(0,0,1)]:
        x=[F(x1)+z[0]*y,F(x2)+z[1]*y]
        assert quadratic(A,[x1,x2,y])==quadratic(G,x)+r['debt']*y*y


def test_rational_schur_vs_independent_spectrum():
    import numpy as np
    for a,b,c in [(1,1,1),(1,2,1),(0,0,0),(0,1,1),(2,2,1),(-1,0,2)]:
        A=[[a,b],[b,c]];r=append_contract([[a]],[b],c)
        assert r['accepted']==bool(np.linalg.eigvalsh(np.array(A,dtype=float)).min()>=-1e-12)
        assert psd(A)==r['accepted']


def test_model_no_simulation_promoted_to_evidence():
    m=build_model()
    assert all(m['facts'][f]['status']=='proved_internal' for f in m['initial_facts'])
    assert not {'RH_proved','global_sign_proved'} & set(m['initial_facts'])
    assert all('RH_proved' not in o['adds'] for a in m['actions'] for o in a['outcomes'])
    r=json.loads((ROOT/'data/v643_bellman_ponts.json').read_text())
    assert r['comparisons_passed']==270


def test_archimedean_normalization_independent_quadrature():
    import mpmath as mp
    with mp.workdps(45):
        h0=mp.sqrt(mp.pi/2)
        def original(x):
            if x==0:return h0/2
            return (2*mp.exp(-x/2)*h0*mp.exp(-x*x/2)-2*mp.exp(-x)*h0)/(1-mp.exp(-2*x))
        def translated(x):
            if x==0:return mp.mpf(0)
            return mp.exp(-x/2)/(1-mp.exp(-2*x))*2*h0*(-mp.expm1(-x*x/2))
        old=-(mp.log(4*mp.pi)+mp.euler)*h0-mp.quad(original,[0,1,mp.inf])
        new=mp.quad(translated,[0,1,mp.inf])-(mp.log(8*mp.pi)+mp.euler+mp.pi/2)*h0
        assert abs(old-new)<mp.mpf('1e-35')


def test_shifted_regularization_covers_negative_abscissae():
    import math
    S=2
    def psi(x):return math.exp(-1/(1-x*x)) if abs(x)<1 else 0
    def g(y):return psi(y-S-1) if y>0 else 0
    for x in [-1.5,-.5,0,.5,1.5]:assert g(x+S+1)==psi(x)
    assert psi(-.5)>0 and g(-.5)==0
