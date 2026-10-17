#!/usr/bin/env python3
"""Exploratory Fourier joint budgets; no interval certification.

Uses the unitary Fourier transform: Q=integral(b-C0-2w)|fhat|².
Parity concentration traces retain the factor 1/pi. Grid refinement only
measures numerical stability; it supplies neither rigorous tails nor errors.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.special import digamma

SUPPORTS = [('347/1000',347/1000),('3/8',3/8),('1/2',1/2)]
RESOLUTIONS = [40000,80000]
TMAX = 100.0
SHIFT = np.log(2.0)
WEIGHT = SHIFT/np.sqrt(2.0)
C0 = np.log(8*np.pi)+np.euler_gamma+np.pi/2

def projected_diagonals(S,t):
    z=.5+1j*t
    b=2*np.sinh(z*S)/z
    v=S*np.sinc(2*S*t/np.pi)
    return [np.maximum(0,S+v-b.real**2/(S+np.sinh(S))),
            np.maximum(0,S-v-b.imag**2/(np.sinh(S)-S))]

def run_resolution(S,N):
    dt=TMAX/N
    # Midpoint grid for sublevel measure; endpoint grid for layer integrals.
    t=(np.arange(N)+.5)*dt
    a=np.real(digamma(.25+1j*t/2))-digamma(.25)
    joint=a+2*WEIGHT*(1-np.cos(SHIFT*t))
    order=np.argsort(joint);sorted_b=joint[order]
    mid_diagonals=projected_diagonals(S,t)
    sublevel=[]
    for d in mid_diagonals:
        concentration=np.cumsum(d[order])*dt/np.pi
        sublevel.append(float(np.sum(np.diff(np.r_[0.,sorted_b])*
                                       np.maximum(0,1-concentration))))
    endpoint=np.linspace(0,TMAX,N+1)
    ae=np.real(digamma(.25+1j*endpoint/2))-digamma(.25)
    be=ae+2*WEIGHT*(1-np.cos(SHIFT*endpoint))
    envelope=np.minimum.accumulate(be[::-1])[::-1]
    separate=[];monotone=[]
    for d in projected_diagonals(S,endpoint):
        concentration=cumulative_trapezoid(d,endpoint,initial=0)/np.pi
        remaining=np.maximum(0,1-concentration[1:])
        separate.append(float(np.sum(np.diff(ae)*remaining)))
        monotone.append(float(np.sum(np.diff(envelope)*remaining)))
    return dict(Nfrequency=N,Tmax=TMAX,frequency_microstep=dt,
        separate_energy_even_odd=separate,
        separate_geometric_margin=min(separate)-C0-WEIGHT,
        monotone_envelope_energy_even_odd=monotone,
        monotone_envelope_margin=min(monotone)-C0-2*WEIGHT,
        sublevel_joint_energy_even_odd=sublevel,
        sublevel_joint_margin=min(sublevel)-C0-2*WEIGHT)

def main():
    rows=[]
    for label,S in SUPPORTS:
        resolutions=[run_resolution(S,N) for N in RESOLUTIONS]
        stability={k:resolutions[1][k]-resolutions[0][k] for k in
            ['separate_geometric_margin','monotone_envelope_margin','sublevel_joint_margin']}
        rows.append(dict(S=label,resolutions=resolutions,
            refinement_differences=stability,
            interpretation='positive diagnostics do not create a new certificate'))
    out=dict(version='V6.46',scope='exploratory diagnostic only',
        certified=False,global_RH_claim=False,new_positive_certificate=False,
        chosen_after_exploration=True,zero_data_used=False,
        normalization='unitary Fourier; Q=integral (b-C0-2w)|fhat|^2; parity trace 1/pi',
        constants=dict(C0=C0,prime_shift=SHIFT,prime_weight=WEIGHT),
        numerical_method='midpoint sublevel sorting; endpoint trapezoid concentration and finite layers',
        limitations=['no outward intervals','no proven quadrature error',
            'finite-frequency envelope infimum is not certified against omitted tail',
            'resolution agreement is stability only',
            'Schatten-2 diagnostic not done in this reproducible experiment'],
        supports=rows)
    target=Path(__file__).resolve().parents[1]/'data/v646_fourier_joint_diagnostic.json'
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    for r in rows:
        p=r['resolutions'][-1]
        print(r['S'], 'separate',format(p['separate_geometric_margin'],'.10f'),
              'envelope',format(p['monotone_envelope_margin'],'.10f'),
              'sublevels',format(p['sublevel_joint_margin'],'.10f'),
              'stability',r['refinement_differences'])
    assert all(not out[k] for k in ['certified','global_RH_claim','new_positive_certificate'])
    print('exploratory guards verified; wrote',target.name)

if __name__=='__main__':main()
