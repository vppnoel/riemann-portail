"""Permutation-free roots, multiplicities, constrained sections and unseen modes."""
import numpy as np
from v641_blocs import pair_from_moments,jet_section
from v641_global import hidden_negative_prefix,schur_diagnostic


def test_moments_preserve_an_unordered_pair_and_a_double_jordan_block():
    for roots in ([3.,5.],[3+2j,3-2j],[3.,3.]):
        roots=np.array(roots);block=pair_from_moments(2,roots.sum(),(roots**2).sum())
        for x in roots:assert abs(np.linalg.det(block['companion']-x*np.eye(2)))<1e-12
        metric=np.diag([block['mu'],1]);assert np.linalg.norm(block['companion'].T@metric-metric@block['companion'])<1e-12
        assert abs(block['discriminant']-(roots[0]-roots[1])**2)<1e-12
    H=pair_from_moments(2,6,18)['companion']
    assert np.linalg.matrix_rank(H-3*np.eye(2))==1
    assert np.linalg.norm((H-3*np.eye(2))@(H-3*np.eye(2)))==0
    try:pair_from_moments(3,9,27)
    except ValueError:pass
    else:raise AssertionError('A three-zero contour was treated as a pair')
    for args in ((float('nan'),6,18),(2,float('inf'),18),(2,6,complex(0,float('nan')))):
        try:pair_from_moments(*args)
        except ValueError:pass
        else:raise AssertionError('Non-finite moments were accepted')
    for tolerance in (0,-1,float('nan'),float('inf')):
        try:pair_from_moments(2,6,18,count_tolerance=tolerance)
        except ValueError:pass
        else:raise AssertionError('An invalid count tolerance was accepted')


def test_rank_five_jet_sections_distinguish_two_one_zero_and_incompatibility():
    C=np.c_[np.eye(5),np.zeros(5)]
    for norm,status,n in ((.5,'two_candidates',2),(1.,'boundary_tolerance',1),(1.1,'empty',0)):
        b=np.array([norm,0,0,0,0]);s=jet_section(C,b)
        assert s['status']==status and len(s['solutions'])==n
        for c in s['solutions']:assert np.linalg.norm(C@c-b)<1e-12 and abs(c@c-1)<1e-12
    C[-1]=0;s=jet_section(C,np.array([0,0,0,0,1]))
    assert s['status']=='incompatible' and not s['solutions']


def test_positive_prefixes_do_not_determine_the_global_sign():
    for n in (1,2,10):
        K=hidden_negative_prefix(n)
        assert np.array_equal(K[:n,:n],np.eye(n))
        assert K[-1,-1]==-1 and np.linalg.eigvalsh(K)[0]==-1
        assert np.linalg.norm(K,2)==1


def test_schur_budget_controls_an_omitted_coupling():
    A=np.diag([2.,3.]);C=np.diag([4.,5.]);B=np.eye(2)
    r=schur_diagnostic(A,B,C);assert r['sufficient_norm_budget_passes']
    assert np.linalg.eigvalsh(np.block([[A,B],[B.T,C]]))[0]>0
    B=5*np.eye(2);r=schur_diagnostic(A,B,C)
    assert not r['sufficient_norm_budget_passes'] and np.linalg.eigvalsh(r['schur'])[0]<0
    assert np.linalg.eigvalsh(np.block([[A,B],[B.T,C]]))[0]<0
