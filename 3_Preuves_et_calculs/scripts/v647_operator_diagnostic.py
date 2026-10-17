#!/usr/bin/env python3
"""Exploratory projected sublevel concentration operators (not certificates).

Unitary Fourier convention. On each parity, K_u=(1/pi) integral_{b(t)<u,
t>0} |P cos(tx)><P cos(tx)| dt, respectively sin. Spatial quadrature and
frequency membership are approximate. Resolution agreement proves no errors.
The same annihilator Gram projects sources and the frequency functions.
"""
import json
import time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import digamma

SUPPORTS=[('3/8',3/8),('1/2',1/2)]
CONFIGS=[dict(spatial_nodes=80,frequency_nodes=40000,u_step=1/80),
         dict(spatial_nodes=120,frequency_nodes=80000,u_step=1/160)]
TMAX=100.;UMAX=8.
SHIFT=np.log(2.);WEIGHT=SHIFT/np.sqrt(2.)
C0=np.log(8*np.pi)+np.euler_gamma+np.pi/2

def run(S,config):
    start=time.monotonic();N=config['spatial_nodes'];nf=config['frequency_nodes'];du=config['u_step']
    x,wx=leggauss(N);x*=S;wx*=S;sw=np.sqrt(wx)
    U=sw[:,None]*np.column_stack([np.cosh(x/2),np.sinh(x/2)])
    Gram=U.T@U;P=np.eye(N)-U@np.linalg.inv(Gram)@U.T
    analytic_Gram=np.diag([S+np.sinh(S),np.sinh(S)-S])
    parity_basis=[]
    for sign in [1,-1]:
        V=np.zeros((N,N//2))
        for i in range(N//2):V[i,i]=1/np.sqrt(2);V[-1-i,i]=sign/np.sqrt(2)
        parity_basis.append(V)
    dt=TMAX/nf;t=(np.arange(nf)+.5)*dt
    a=np.real(digamma(.25+1j*t/2))-digamma(.25)
    joint=a+2*WEIGHT*(1-np.cos(SHIFT*t))
    order=np.argsort(joint);joint=joint[order];t=t[order]
    matrices=[np.zeros((N//2,N//2)) for _ in range(2)]
    integrated=[np.zeros_like(matrices[0]) for _ in range(2)]
    floors={key:[0.,0.] for key in ['trace','schatten2','operator']}
    stops=[None,None];rows=[];old=0
    for u in np.arange(du,UMAX+du/2,du):
        new=np.searchsorted(joint,u);tt=t[old:new];old=new
        measures=[]
        for p in range(2):
            f=np.cos(x[:,None]*tt) if p==0 else np.sin(x[:,None]*tt)
            columns=parity_basis[p].T@P@(sw[:,None]*f)
            matrices[p]+=dt/np.pi*(columns@columns.T)
            integrated[p]+=du*matrices[p]
            eig=np.linalg.eigvalsh(matrices[p])
            assert eig[0]>-1e-10
            values=dict(trace=float(np.trace(matrices[p])),
                schatten2=float(np.linalg.norm(matrices[p])),operator=float(eig[-1]))
            for key,value in values.items():floors[key][p]+=du*max(0,1-value)
            if stops[p] is None and values['schatten2']>=1:stops[p]=float(u)
            measures.append(values)
        rows.append(dict(u=float(u),concentration_even_odd=measures))
    common=[float(UMAX-np.linalg.eigvalsh(B)[-1]) for B in integrated]
    common_hs=[float(UMAX-np.linalg.norm(B)) for B in integrated]
    margins={k:min(v)-C0-2*WEIGHT for k,v in floors.items()}
    margins['common_operator']=min(common)-C0-2*WEIGHT
    margins['common_schatten2']=min(common_hs)-C0-2*WEIGHT
    return dict(configuration=config,Tmax=TMAX,umax=UMAX,
        duration_seconds=time.monotonic()-start,
        annihilator_gram=Gram.tolist(),analytic_annihilator_gram=analytic_Gram.tolist(),
        gram_max_point_error=float(np.max(np.abs(Gram-analytic_Gram))),
        layer_energy_even_odd=floors,
        common_operator_energy_even_odd=common,
        common_schatten2_energy_even_odd=common_hs,margins=margins,
        schatten2_first_level_at_least_one=stops,
        tail_check_point_a_Tmax=float(np.real(digamma(.25+1j*TMAX/2))-digamma(.25)),
        rows=rows)

def main():
    supports=[]
    for label,S in SUPPORTS:
        records=[run(S,c) for c in CONFIGS]
        differences={k:records[1]['margins'][k]-records[0]['margins'][k]
                     for k in records[0]['margins']}
        supports.append(dict(S=label,resolutions=records,
            refinement_differences=differences))
        print(label,'fine margins',records[-1]['margins'],
              'stability only',differences)
    result=dict(version='V6.47',scope='exploratory operator diagnostic only',
        certified=False,new_positive_certificate=False,global_RH_claim=False,
        zero_data_used=False,chosen_after_exploration=True,
        normalization='unitary Fourier; projected parity concentration 1/pi',
        constants=dict(C0=C0,prime_shift=SHIFT,prime_weight=WEIGHT),
        common_operator_principle='b >= min(b,U); integral K_u before taking its norm retains a common test across levels',
        limitations=['spatial Nystrom eigenvalues are not rigorous operator norm bounds',
            'frequency midpoint membership has no certified sublevel inclusion',
            'no outward intervals or proven quadrature errors',
            'a(Tmax)>umax tail check is a point value only',
            'all resolution differences describe stability, not accuracy'],
        supports=supports)
    target=Path(__file__).resolve().parents[1]/'data/v647_operator_diagnostic.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assert not any(result[k] for k in ['certified','new_positive_certificate','global_RH_claim'])
    print('exploratory guards and discrete Gram/PSD checks passed;',target.name)

if __name__=='__main__':main()
