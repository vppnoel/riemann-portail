#!/usr/bin/env python3
"""Independent replay of archived dyadic congruences and rational budgets.

This replays the final proof witnesses without asking the eigensolver for
new witnesses and without redoing the 700000-cell assembly.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib,math
import numpy as np

sys.set_int_max_str_digits(0)
ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'4_Archives/recus/V650/constructive'
sys.path.insert(0,str(ROOT/'3_Preuves_et_calculs/src'))
import prime_centered_bridge as b
import mpmath as mp


def replay(M,C,tau):
    """Forward-error enclosure, distinct from the assembly's interval replay."""
    n=M.shape[0];u=F(1,2**53);gamma=F(n)*u/(1-F(n)*u)
    assert M.shape==(n,n) and C.shape==(n,n)
    assert np.array_equal(M,M.T)
    assert not np.any(np.triu(C,1)) and np.all(np.diag(C)!=0)
    assert F.from_float(float(tau))==tau
    # A endpoints include every correctly rounded subtraction from tau I-M.
    Ap=float(tau)*np.eye(n)-M
    Alo=np.nextafter(Ap,-np.inf);Ahi=np.nextafter(Ap,np.inf)
    Arad=np.nextafter(np.maximum(np.abs(Ap-Alo),np.abs(Ahi-Ap)),np.inf)
    absC=np.abs(C);absA=np.abs(Ap)
    g=np.nextafter(float(gamma),np.inf)
    # Every nonnegative dot-product result divided by 1-g bounds its exact sum.
    positive_product=lambda X,Y:np.nextafter((X@Y)/np.nextafter(1-g,0),np.inf)
    X=Ap@C.T
    dX=positive_product(absA,absC.T)*g+positive_product(Arad,absC.T)
    dX=np.nextafter(dX,np.inf)
    R=C@X
    dR=positive_product(absC,np.abs(X))*g+positive_product(absC,dX)
    # Slack factor16 absorbs scalar operations used to evaluate the bounds.
    dR=np.nextafter(16*dR+1e-12,np.inf)
    lower=np.nextafter(np.diag(R)-np.diag(dR),-np.inf)
    off=np.nextafter(np.abs(R)+dR,np.inf);np.fill_diagonal(off,0)
    # Sum all dyadic off-diagonal upper bounds exactly, then compare exact floats.
    floors=[]
    for i in range(n):
        q=F.from_float(float(lower[i]))-sum((F.from_float(float(v)) for v in off[i]),F(0))
        floors.append(q)
    assert min(floors)>0
    return float(min(floors))


def main():
    b.setup(320)
    j=json.loads((A/'resultats_certificat_integral.json').read_text())
    mats=A/j['final_matrix_file']
    assert hashlib.sha256(mats.read_bytes()).hexdigest()==j['final_matrix_sha256']
    matrices=np.load(mats,allow_pickle=False)
    print('matrix_keys',matrices.files)
    floors=[];replayed=[]
    for row in j['parities']:
        p=row['parity'];w=row['matrix_certificate'];path=A/w['congruence_matrix_file']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==w['congruence_matrix_sha256']
        C=np.load(path,allow_pickle=False)
        key='matrix_'+p
        M=matrices[key]
        tau=F(w['tau_fraction']);total=F(row['total_operator_error'])
        floor=F(j['U'])-F(j['C_upper'])-tau-total
        assert floor==F(row['mass_floor_lower'])>F(3,10000)
        cg=replay(M,C,tau)
        floors.append(floor);replayed.append(dict(parity=p,congruence_floor=cg,mass_floor=float(floor)))
    S=b.I(F(11,20));lp=[mp.iv.log(b.I(p)) for p in (2,3)]
    assert b.hi(lp[1])<2*F(11,20)<b.lo(mp.iv.log(b.I(4)))
    assert b.lo(lp[0])>F(11,20)
    C0=mp.iv.log(8*mp.iv.pi)+mp.iv.euler+mp.iv.pi/2
    L=C0+sum((mp.iv.log(b.I(p))/mp.iv.sqrt(b.I(p)) for p in (2,3)),b.I(0))
    assert b.hi(L)<F(13,2)
    clean_mass=F(3,10000);clean_R=clean_mass/(clean_mass+1+F(13,2))
    assert clean_R==F(1,25001)
    out=dict(version='V6.50',exact_budget_sums_verified=True,matrix_hashes_verified=True,
        independent_congruence_replay=replayed,clean_mass_floor=str(clean_mass),clean_R_floor=str(clean_R),
        arithmetic_model='declared IEEE64 dot-product model; rational sums; mpmath interval elementary constants',
        inherited_analytic_lifting='reviewed proof and source code; this verifier does not rerun all cells',
        global_RH_claim=False)
    (ROOT/'3_Preuves_et_calculs/data/v650_verification_certificat.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(out,ensure_ascii=False))


if __name__=='__main__':main()
