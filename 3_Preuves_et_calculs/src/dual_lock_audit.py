from __future__ import annotations

import math
import warnings
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, IntegrationWarning
from scipy.linalg import eigh
from scipy.special import digamma

from dual_lock import KINDS, _log_derivative_weights, tent_fourier, correlation_direct, _arch_matrix


def gram_matrix(frequencies: np.ndarray, w: float, eps: float = 2e-10) -> np.ndarray:
    m = len(frequencies)
    G = np.zeros((m,m), dtype=float)
    for i, xi in enumerate(frequencies):
        for j in range(i+1):
            v = correlation_direct(0.0, w, float(xi), float(frequencies[j]), eps=eps)
            G[i,j] = G[j,i] = v
    return 0.5*(G+G.T)


def generalized_decomposition(components: dict[str, np.ndarray], G: np.ndarray):
    M = np.asarray(components['total'], dtype=float)
    G = np.asarray(G, dtype=float)
    vals, vecs = eigh(M, G, type=1, check_finite=True)
    v = vecs[:,0]
    # scipy eigh normalizes v^T G v = 1 for type=1
    gnorm = float(v @ G @ v)
    if not np.isfinite(gnorm) or abs(gnorm-1.0) > 1e-8:
        v = v / math.sqrt(gnorm)
        gnorm = float(v @ G @ v)
    names = ['archimedean','conductor','pole','local']
    q = {name: float(v @ np.asarray(components[name]) @ v) for name in names}
    lam = float(vals[0])
    visible = float(sum(abs(x) for x in q.values()))
    return {
        'lambda_min_gen': lam,
        'lambda_max_gen': float(vals[-1]),
        'g_norm': gnorm,
        'q_archimedean_gen': q['archimedean'],
        'q_conductor_gen': q['conductor'],
        'q_pole_gen': q['pole'],
        'q_local_gen': q['local'],
        'q_total_gen': float(sum(q.values())),
        'visible_scale_gen': visible,
        'cancellation_ratio_gen': abs(lam)/visible if visible else 0.0,
        'residual_amplification_gen': visible/max(abs(lam),1e-300),
        'closure_error_gen': abs(lam-sum(q.values())),
        'gram_cond': float(np.linalg.cond(G)),
        'gram_min_eig': float(np.linalg.eigvalsh(G)[0]),
        'n_negative_gen': int(np.sum(vals < -1e-10)),
        'n_positive_gen': int(np.sum(vals > 1e-10)),
    }, v, vals


def _basis_value_np(x: np.ndarray, w: float, xi: float) -> np.ndarray:
    env = np.maximum(0.0, 1.0 - np.abs(x)/w)
    return env*np.cos(xi*x)


def correlation_gauss(x: float, w: float, xi: float, xj: float, order: int=384) -> float:
    lo = max(-w, x-w)
    hi = min(w, x+w)
    if hi <= lo:
        return 0.0
    pts=[lo,hi]
    for p in (0.0,x):
        if lo < p < hi:
            pts.append(p)
    pts=sorted(set(pts))
    z, wz = leggauss(int(order))
    total=0.0
    for a,b in zip(pts[:-1],pts[1:]):
        mid=0.5*(a+b); half=0.5*(b-a)
        y=mid+half*z
        vals=_basis_value_np(y,w,xi)*_basis_value_np(x-y,w,xj)
        total += half*float(np.dot(wz, vals))
    return total


def arch_matrix_gauss(frequencies: np.ndarray, w: float, parity: int,
                      tmax: float | None = None, block: float = 8.0,
                      order: int = 24) -> np.ndarray:
    """Independent composite Gauss--Legendre evaluation of the archimedean term."""
    frequencies=np.asarray(frequencies,dtype=float)
    if tmax is None:
        tmax=max(450.0,float(np.max(np.abs(frequencies)))+120.0)
    z,wz=leggauss(int(order))
    nodes=[]; weights=[]
    a=0.0
    while a < tmax-1e-15:
        b=min(tmax,a+block)
        mid=0.5*(a+b); half=0.5*(b-a)
        nodes.append(mid+half*z)
        weights.append(half*wz)
        a=b
    t=np.concatenate(nodes); wg=np.concatenate(weights)
    arg0=(0.5+parity)/2.0
    psi=np.real(digamma(arg0+0.5j*t))/math.pi
    H=np.array([np.real(tent_fourier(t,w,xi)) for xi in frequencies])
    return (H*(psi*wg))@H.T

def compression_components_independent(center: float, kind: str, *, half_width: float=2.5, dimension: int=7,
                                       frequency_step: float=0.6, gl_order: int=384,
                                       arch_quad_eps: float=2e-9):
    spec=KINDS[kind]
    m=int(dimension); w=float(half_width)
    freqs=float(center)+frequency_step*(np.arange(m,dtype=float)-(m-1)/2.0)
    nmax=int(math.floor(math.exp(2.0*w)))+2
    b=_log_derivative_weights(kind,nmax)
    arch=arch_matrix_gauss(freqs,w,spec.parity,order=28)
    G=np.zeros((m,m),float)
    for i,xi in enumerate(freqs):
        for j in range(i+1):
            G[i,j]=G[j,i]=correlation_gauss(0.0,w,float(xi),float(freqs[j]),order=gl_order)
    conductor=math.log(spec.q/math.pi)*G
    pole=np.zeros_like(G)
    if spec.pole:
        pv=np.array([float(np.real(tent_fourier(0.5j,w,xi))) for xi in freqs])
        pole=2.0*np.outer(pv,pv)
    local=np.zeros_like(G)
    logs=[]; weights=[]
    for n in range(2,nmax+1):
        if abs(b[n])<=1e-14: continue
        lx=math.log(n)
        if lx<=2.0*w+1e-12:
            logs.append(lx); weights.append(float(b[n])/math.sqrt(n))
    for i,xi in enumerate(freqs):
        for j in range(i+1):
            loc=0.0
            for lx,weight in zip(logs,weights):
                loc += weight*correlation_gauss(lx,w,float(xi),float(freqs[j]),order=gl_order)
            local[i,j]=local[j,i]=-2.0*loc
    total=0.5*(arch+conductor+pole+local + (arch+conductor+pole+local).T)
    return freqs, {'archimedean':arch,'conductor':conductor,'pole':pole,'local':local,'total':total}, G

def gram_matrix_closed(frequencies: np.ndarray, w: float) -> np.ndarray:
    """V6.7 — Gram en forme close des tentes modulées f_j(x) = (1 - |x|/w)_+ cos(xi_j x).

    <f_i, f_j> = (I(xi_i - xi_j) + I(xi_i + xi_j)) / 2,  I(k) = int (1 - |x|/w)_+^2 cos(k x) dx
               = 4 (1 - sin(k w)/(k w)) / (w k^2)   (2w/3 en k = 0).
    Identique à gram_matrix (quadrature) à 1e-15 près pour T <= 200 ; la quadrature se dégrade aux grandes
    hauteurs (6e-5 à T = 1400), la forme close non.
    """
    fr = np.asarray(frequencies, dtype=float); w = float(w)
    def I(k):
        k = np.abs(k); x = k * w; safe_k = np.where(k == 0, 1.0, k); safe_x = np.where(x == 0, 1.0, x)
        return np.where(x < 1e-3, 2 * w / 3 - w * x ** 2 / 30, 4.0 / (w * safe_k ** 2) * (1 - np.sin(safe_x) / safe_x))
    return 0.5 * (I(fr[:, None] - fr[None, :]) + I(fr[:, None] + fr[None, :]))
