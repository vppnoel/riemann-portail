"""Finite algebraic controls for the global-positivity research contract."""
import numpy as np


def hidden_negative_prefix(size):
    if type(size) is not int or size<1:raise ValueError('Positive integer size required')
    matrix=np.eye(size+1);matrix[-1,-1]=-1
    return matrix


def schur_diagnostic(A,B,C):
    A=np.asarray(A,dtype=float);B=np.asarray(B,dtype=float);C=np.asarray(C,dtype=float)
    if not np.allclose(A,A.T) or not np.allclose(C,C.T):raise ValueError('Hermitian real blocks required')
    amin=float(np.linalg.eigvalsh(A)[0])
    if amin<=0:raise ValueError('The stated Schur criterion requires positive definite A')
    schur=C-B.T@np.linalg.solve(A,B)
    cmin=float(np.linalg.eigvalsh(C)[0]);bnorm=float(np.linalg.norm(B,2))
    return {'schur':schur,'minimum_A':amin,'minimum_C':cmin,'coupling_norm':bnorm,
        'sufficient_norm_budget_passes':bool(cmin>=0 and bnorm**2<=amin*cmin),
        'global_RH_implication':False}
