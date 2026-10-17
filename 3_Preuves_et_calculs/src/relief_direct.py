"""Comptage numérique direct des zéros dans les familles de l'archipel.

Le contour entoure la fonction complétée (entière), des deux côtés de la
droite critique. La différence avec les zéros comptés sur cette droite
mesure les zéros hors droite dans le rectangle, sans référence à un point
d'Euler. Les contrôles par raffinement restent numériques, non certifiés.
"""
from __future__ import annotations
import math
from pathlib import Path
import numpy as np
from scipy.special import loggamma, zeta
from scipy.stats import rankdata
from euler_archipelago import characters, hurwitz_vec

def completed_phase_basis(q, parity, s):
    """Partie droite Re(s)>=1/2, avec phase de Gamma et facteur réel retiré.

    Retirer un facteur réel positif ne change pas le principe de l'argument.
    La partie gauche s'obtient par conjugaison en 1-conjugate(s).
    """
    s=np.asarray(s,dtype=complex).reshape(-1)
    ch=characters(q,parity)
    H={r:hurwitz_vec(s,r/q) for r in range(1,q)}
    lg=(s+parity)/2*math.log(q/math.pi)+loggamma((s+parity)/2)
    pref=np.exp(-s*math.log(q)+1j*lg.imag)
    return np.array([np.exp(-1j*c['phi'])*pref*sum(c['table'][r]*H[r] for r in H) for c in ch])

def a1_and_defect(q, parity, C):
    C=np.atleast_2d(C); ch=characters(q,parity)
    b=C*np.exp(-1j*np.array([x['phi'] for x in ch]))
    norm=np.sum(np.abs(b)**2,axis=1);a=b.sum(axis=1)
    D=1+np.abs(a)**2/norm-2*np.real(a*np.sum(np.abs(b)**2*np.conj(b),axis=1))/norm**2
    return np.abs(a)/np.sqrt(norm),D

def partial_rank(x,y,z):
    z=np.atleast_2d(z)
    if z.shape[0]!=len(x):z=z.T
    X=np.column_stack([np.ones(len(x))]+[rankdata(z[:,i]) for i in range(z.shape[1])])
    rx,ry=rankdata(x),rankdata(y)
    ex=rx-X@np.linalg.lstsq(X,rx,rcond=None)[0]
    ey=ry-X@np.linalg.lstsq(X,ry,rcond=None)[0]
    return float(np.corrcoef(ex,ey)[0,1])

class DirectGrid:
    def __init__(self,q,parity,Tmax=300,dt=.02,sigma_right=3.,ds=.05,cache=None):
        self.q,self.parity,self.Tmax=q,parity,Tmax
        self.dt,self.sigma_right,self.ds=dt,sigma_right,ds
        self.levels=np.arange(1,Tmax+1,dtype=float)
        self.t=np.arange(-int(round(Tmax/dt)),int(round(Tmax/dt))+1)*dt
        self.sig=np.linspace(.5,sigma_right,int(math.ceil((sigma_right-.5)/ds))+1)
        file=Path(cache) if cache else None
        if file and file.exists():
            d=np.load(file);self.Bcrit=d['Bcrit'];self.Bright=d['Bright'];self.Bhorizontal=d['Bhorizontal']
        else:
            self.Bcrit=completed_phase_basis(q,parity,.5+1j*self.t).real
            self.Bright=completed_phase_basis(q,parity,sigma_right+1j*self.t)
            ss=(self.sig[None,:]+1j*np.r_[-self.levels,self.levels][:,None]).reshape(-1)
            b=completed_phase_basis(q,parity,ss)
            self.Bhorizontal=b.reshape(len(b),2*Tmax,len(self.sig))
            if file:np.savez_compressed(file,Bcrit=self.Bcrit,Bright=self.Bright,Bhorizontal=self.Bhorizontal)

    def critical_counts(self,C):
        C=np.atleast_2d(C);Z=C@self.Bcrit
        result=[]
        for z in Z:
            ids=np.flatnonzero(z[1:]*z[:-1]<0)
            roots=self.t[ids]-self.dt*z[ids]/(z[ids+1]-z[ids])
            result.append(np.searchsorted(np.sort(np.abs(roots)),self.levels,side='right'))
        return np.array(result,dtype=int)

    def total_counts(self,C,refine=True):
        C=np.atleast_2d(C)
        a,_=a1_and_defect(self.q,self.parity,C)
        tail=np.sqrt(C.shape[1])*(zeta(self.sigma_right,1)-1)
        if np.any(a<=tail):raise ValueError('Bord droit non garanti sans zéro par domination du premier terme')
        R=C@self.Bright
        increments=np.angle(R[:,1:]/R[:,:-1]);phase=np.c_[np.zeros(len(C)),np.cumsum(increments,axis=1)]
        lo=np.rint((-self.levels-self.t[0])/self.dt).astype(int)
        hi=np.rint((self.levels-self.t[0])/self.dt).astype(int)
        vertical=phase[:,hi]-phase[:,lo]
        H=np.einsum('nd,dtk->ntk',C,self.Bhorizontal)
        step=np.angle(H[:,:,1:]/H[:,:,:-1]);alpha=step.sum(axis=2)
        maxstep=np.max(np.abs(step),axis=2)
        refinements=0;unresolved=0
        if refine:
            for k in np.flatnonzero(np.max(maxstep,axis=0)>.8):
                for subdivision in (2,4,8,16,32):
                    sig=np.linspace(.5,self.sigma_right,(len(self.sig)-1)*subdivision+1)
                    ht=-self.levels[k] if k<self.Tmax else self.levels[k-self.Tmax]
                    hb=completed_phase_basis(self.q,self.parity,sig+1j*ht)
                    hh=C@hb;st=np.angle(hh[:,1:]/hh[:,:-1]);mx=np.max(np.abs(st),axis=1)
                    bad=maxstep[:,k]>.8
                    alpha[bad,k]=st.sum(axis=1)[bad];maxstep[bad,k]=mx[bad]
                    refinements+=int(bad.sum())
                    if not np.any(mx[bad]>.8):break
                # Une racine très proche du bord critique impose un pas local
                # minuscule. Ne pas garder une ambiguïté de phase sous prétexte
                # que l'enroulement arrondi est entier : bissection locale.
                for row in np.flatnonzero(maxstep[:,k]>.8):
                    nodes=sig.copy();values=hh[row].copy()
                    for _ in range(24):
                        local=np.angle(values[1:]/values[:-1])
                        ids=np.flatnonzero(np.abs(local)>.8)
                        if not len(ids):break
                        mid=(nodes[ids]+nodes[ids+1])/2
                        vm=C[row]@completed_phase_basis(self.q,self.parity,mid+1j*ht)
                        order=np.argsort(np.r_[nodes,mid])
                        nodes=np.r_[nodes,mid][order];values=np.r_[values,vm][order]
                        refinements+=1
                    local=np.angle(values[1:]/values[:-1])
                    alpha[row,k]=local.sum();maxstep[row,k]=np.max(np.abs(local))
                unresolved+=int((maxstep[:,k]>.8).sum())
        wind=(vertical+alpha[:,:self.Tmax]-alpha[:,self.Tmax:])/math.pi
        count=np.rint(wind).astype(int)
        diagnostics=dict(max_phase_vertical=float(np.max(np.abs(increments))),
            max_phase_horizontal=float(maxstep.max()),max_integer_residual=float(np.max(np.abs(wind-count))),
            refined_rows=refinements,unresolved_horizontal_rows=unresolved,
            sigma_right=self.sigma_right,first_term_margin_min=float(a.min()-tail))
        return count,diagnostics

    def counts(self,C):
        total,diag=self.total_counts(C)
        critical=self.critical_counts(C)
        return total,critical,total-critical,diag
