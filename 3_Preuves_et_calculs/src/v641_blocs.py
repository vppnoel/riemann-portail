"""Label-free two-root blocks and constrained jet sections.

The moment identities are exact under an isolating two-zero contour. Their
floating evaluations and the SVD rank diagnoses are not interval certificates.
"""
import numpy as np


def pair_from_moments(m0, m1, m2, count_tolerance=1e-5):
    moments=np.asarray([m0,m1,m2],dtype=complex)
    if not np.all(np.isfinite(moments)) or not np.isfinite(count_tolerance) or count_tolerance<=0:
        raise ValueError('Finite moments and a positive finite count tolerance required')
    if abs(complex(m0)-2)>count_tolerance:
        raise ValueError('A two-root block requires an accepted two-zero count')
    centre=complex(m1)/2
    delta=2*complex(m2)-complex(m1)**2
    mu=delta/4
    H=np.array([[centre,1],[mu,centre]],dtype=complex)
    return {'centre':centre,'discriminant':delta,'mu':mu,'companion':H,
        'roots':np.array([centre+np.sqrt(mu),centre-np.sqrt(mu)]),
        'conditional_on_isolating_contour':True,'interval_certification':False}


def jet_section(matrix,rhs,tolerance=1e-10):
    C=np.asarray(matrix,dtype=float);b=np.asarray(rhs,dtype=float)
    if C.shape!=(5,6) or b.shape!=(5,) or not np.all(np.isfinite(C)) or not np.all(np.isfinite(b)):
        raise ValueError('Five finite constraints and six real coefficients required')
    U,s,Vh=np.linalg.svd(C,full_matrices=True)
    rank=int(np.sum(s>tolerance*s[0]))
    c0=Vh[:rank].T@((U[:,:rank].T@b)/s[:rank])
    compatibility=float(np.linalg.norm(C@c0-b))
    nu=float(c0@c0)
    if compatibility>tolerance*max(1,float(np.linalg.norm(b))):
        status='incompatible';solutions=[]
    elif rank!=5:
        status='rank_not_five';solutions=[]
    elif nu>1+tolerance:
        status='empty';solutions=[]
    elif abs(nu-1)<=tolerance:
        status='boundary_tolerance';solutions=[c0]
    else:
        status='two_candidates';n=Vh[5]
        solutions=[c0+np.sqrt(1-nu)*n,c0-np.sqrt(1-nu)*n]
    return {'rank':rank,'singular_values':s,'minimum_solution':c0,'nu':nu,
        'compatibility_residual':compatibility,'status':status,'solutions':solutions,
        'interval_certification':False}
