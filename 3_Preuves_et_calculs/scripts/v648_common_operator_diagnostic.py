#!/usr/bin/env python3
"""Point diagnostic for the continuous common operator, never a certificate.

B_U=(1/pi) integral (U-b(t))_+ |P_W cos(tx)><P_W cos(tx)| dt
on even parity, with sin on odd. No discretization in the value level U.
Unitary Fourier normalization; all quadrature/eigenvalues are exploratory.
"""
import json
import math
import time
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import digamma

S=.5;TMAX=100.;US=[8.,8.125]
CONFIGS=[dict(spatial_nodes=96,frequency_nodes=40000),
         dict(spatial_nodes=144,frequency_nodes=80000)]
SHIFT=np.log(2.);WEIGHT=SHIFT/np.sqrt(2.)
C0=np.log(8*np.pi)+np.euler_gamma+np.pi/2

def run(U,configuration):
    start=time.monotonic();N=configuration['spatial_nodes'];nf=configuration['frequency_nodes']
    x,wx=leggauss(N);x*=S;wx*=S;sw=np.sqrt(wx)
    W=sw[:,None]*np.column_stack([np.cosh(x/2),np.sinh(x/2)])
    Gram=W.T@W;P=np.eye(N)-W@np.linalg.inv(Gram)@W.T
    dt=TMAX/nf;t=(np.arange(nf)+.5)*dt
    a=np.real(digamma(.25+1j*t/2))-digamma(.25)
    b=a+2*WEIGHT*(1-np.cos(SHIFT*t));phi=np.maximum(0,U-b)
    parity=[]
    for p,sign in enumerate([1,-1]):
        V=np.zeros((N,N//2))
        for i in range(N//2):V[i,i]=1/np.sqrt(2);V[-1-i,i]=sign/np.sqrt(2)
        projector=V.T@P;B=np.zeros((N//2,N//2))
        for i in range(0,nf,4096):
            tt=t[i:i+4096]
            wave=np.cos(x[:,None]*tt) if p==0 else np.sin(x[:,None]*tt)
            columns=projector@(sw[:,None]*wave)
            columns*=np.sqrt(phi[i:i+4096]*dt/np.pi)
            B+=columns@columns.T
        eig=np.linalg.eigvalsh(B);assert eig[0]>-1e-10
        parity.append(dict(parity='even' if p==0 else 'odd',
            largest_eigenvalue=float(eig[-1]),second_eigenvalue=float(eig[-2]),
            spectral_gap=float(eig[-1]-eig[-2]),
            top_six_eigenvalues=eig[-6:][::-1].tolist(),
            trace=float(np.trace(B)),schatten2=float(np.linalg.norm(B)),
            energy_floor=U-float(eig[-1]),
            margin=U-C0-2*WEIGHT-float(eig[-1])))
    analytic_Gram=np.diag([S+np.sinh(S),np.sinh(S)-S])
    return dict(configuration=configuration,U=U,Tmax=TMAX,
        duration_seconds=time.monotonic()-start,
        annihilator_gram=Gram.tolist(),
        gram_max_point_error=float(np.max(np.abs(Gram-analytic_Gram))),
        omitted_frequency_tail_point_check=float(np.real(digamma(.25+1j*TMAX/2))-digamma(.25)),
        parity=parity,margin=min(p['margin'] for p in parity))

def main():
    cases=[]
    for U in US:
        records=[run(U,c) for c in CONFIGS]
        cases.append(dict(U=U,resolutions=records,
            refinement_margin_difference=records[1]['margin']-records[0]['margin']))
        print('U',U,'fine margins',[p['margin'] for p in records[-1]['parity']],
              'stability only',cases[-1]['refinement_margin_difference'])
    tails=[]
    for degree_count in [128,136,144]:
        epsilon=math.exp(degree_count*math.log(45)-math.lgamma(degree_count+1))
        tails.append(dict(T=90,S=S,degree_count=degree_count,
            wave_remainder_point=epsilon,
            crude_operator_tail_point=8*90/np.pi*(2*epsilon+epsilon**2),
            scope='architecture budget only; projected-annihilator remainder still required'))
    result=dict(version='V6.48',S='1/2',scope='continuous common operator point diagnostic',
        certified=False,new_positive_certificate=False,global_RH_claim=False,
        zero_data_used=False,chosen_after_exploration=True,
        normalization='unitary Fourier, projected parity B_U integral 1/pi',
        constants=dict(C0=C0,prime_shift=SHIFT,prime_weight=WEIGHT),
        numerical_method='Gauss-Legendre spatial Nystrom; frequency midpoint weighted phi; symmetric eigenvalues',
        limitations=['no outward intervals','no certified quadrature error',
            'Nystrom eigenvalues are not upper bounds on the infinite operator',
            'resolution stability is not proof of accuracy',
            'a(Tmax)>U is a point check, not a certified omitted-tail bound'],
        cases=cases,proposed_taylor_tail_budgets=tails,
        architecture='ambient Legendre compression of projected waves; Legendre projection does not commute with moment projection; certify head, source residual and complement together')
    target=Path(__file__).resolve().parents[1]/'data/v648_common_operator_diagnostic.json'
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assert not any(result[k] for k in ['certified','new_positive_certificate','global_RH_claim'])
    print('discrete PSD/Gram and exploratory guards passed;',target.name)

if __name__=='__main__':main()
