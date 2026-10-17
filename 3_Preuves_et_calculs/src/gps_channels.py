"""Divisor-channel representation for the 'analytic GPS' diagnostics."""
from __future__ import annotations
import math
import numpy as np
from rh_core import EULER_GAMMA, arithmetic_a


def mu_phi_spf_sieve(N: int):
    mu=np.zeros(N+1,dtype=np.int8)
    phi=np.zeros(N+1,dtype=np.int64)
    spf=np.zeros(N+1,dtype=np.int64)
    primes=[]
    if N>=1:
        mu[1]=1; phi[1]=1
    for i in range(2,N+1):
        if spf[i]==0:
            spf[i]=i; primes.append(i); mu[i]=-1; phi[i]=i-1
        for p in primes:
            if i*p>N: break
            spf[i*p]=p
            if i%p==0:
                mu[i*p]=0; phi[i*p]=phi[i]*p
                break
            mu[i*p]=-mu[i]; phi[i*p]=phi[i]*(p-1)
    return mu,phi,spf


def distinct_prime_factors(q: int, spf: np.ndarray) -> list[int]:
    out=[]
    while q>1:
        p=int(spf[q]); out.append(p)
        while q%p==0: q//=p
    return out


def terminal_channel(q: int, mu: np.ndarray, phi: np.ndarray, spf: np.ndarray) -> float:
    """Closed form for H_infty(q)=sum_{q|d} a(d)/d.

    For nonsquarefree q it is zero. For squarefree q:
      H_inf(q) = -2 mu(q)/phi(q) * (log q + sum_{p|q} log p/(p-1)).
    H_inf(1)=0.
    """
    if q==1: return 0.0
    if mu[q]==0: return 0.0
    corr=sum(math.log(p)/(p-1) for p in distinct_prime_factors(q,spf))
    return -2.0*float(mu[q])/float(phi[q])*(math.log(q)+corr)


def partial_channel(D: int, q: int, a: np.ndarray) -> float:
    ds=np.arange(q,D+1,q)
    return float(np.sum(a[ds]/ds)) if len(ds) else 0.0


def terminal_channel_table(D: int, Q: int):
    mu,phi,spf=mu_phi_spf_sieve(max(D,Q))
    a=arithmetic_a(D)
    rows=[]
    for q in range(1,Q+1):
        hp=partial_channel(D,q,a)
        ht=terminal_channel(q,mu,phi,spf)
        rows.append((q,hp,ht,ht-hp,float(mu[q]),float(phi[q])))
    return rows
