from pathlib import Path
import sys,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from jet_bound import bound,optimize,certificate,basis,explicit_sqrt_parameters

def test_jet_polynomial_is_nonzero_and_multiple_at_every_square_point():
    c=certificate(29,[1,1,0,1],3,11,4)
    assert c['dimension']==66 and c['rang_majore']==64
    assert c['degre_temoin']>=4*c['S'] and c['multiplicite_minimale']>=4
    assert c['borne_S']==27 and c['noyau_exact']>=2

def test_jet_distinct_leading_degrees_and_rank_bound_at_boundary():
    p=29;K=(p-3)//2;B=basis(p,[1,1,0,1],3,K)
    degrees=[int(np.flatnonzero(B[:,j])[-1]) for j in range(B.shape[1])]
    assert len(set(degrees))==2*3*K
    c=certificate(61,[1,1,0,1],4,25,6)
    assert c['rang_exact']<=c['rang_majore_avec_S']<=c['rang_majore']
    assert c['S']<=c['borne_S']<61

def test_jet_optimization_and_square_root_family_are_nontrivial():
    assert optimize(29)['borne_S']==26
    for p in (29,61,101,1009,10007):
        r=optimize(p);assert r['borne_S']<p and r['noyau_minimal']>0
        s=explicit_sqrt_parameters(p)
        assert s['dimension']>s['rang_majore']
    # Pour une grande valeur, l'écart à p/2 est effectivement O(sqrt(p)).
    p=1000003;r=explicit_sqrt_parameters(p)
    assert 2*r['borne_S']-p<6*np.sqrt(p)

def test_jet_rejects_parameters_without_an_existence_argument():
    for args in ((29,1,1,3),(29,3,14,4),(29,3,11,29)):
        try:bound(*args)
        except ValueError:pass
        else:raise AssertionError('Paramètres non admissibles acceptés')
