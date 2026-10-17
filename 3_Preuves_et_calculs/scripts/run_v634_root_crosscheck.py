"""Localise les premières paires détectées et les recoupe par mpmath.

Le calcul haute précision emploie des caractères et phases reconstruits à
50 chiffres, et la fonction de Dirichlet de mpmath; il est indépendant de
l'évaluateur Euler-Maclaurin en double précision utilisé par la carte.
"""
from pathlib import Path
import json,sys
import numpy as np,pandas as pd
from scipy.optimize import root
import mpmath as mp
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';sys.path.insert(0,str(ROOT/'src'))
from euler_archipelago import F_values,primitive_root

def mp_function(q,c):
    generator=primitive_root(q);log={pow(generator,j,q):j for j in range(q-1)}
    tables=[];weights=[]
    for k in range(1,q-1,2):
        tab=[mp.mpc(0)]+[mp.exp(2j*mp.pi*log[a]*k/(q-1)) for a in range(1,q)]
        tau=sum(tab[a]*mp.exp(2j*mp.pi*a/q) for a in range(1,q))
        eps=tau/(1j*mp.sqrt(q));tables.append(tab);weights.append(mp.exp(-1j*mp.arg(eps)/2))
    coeff=[mp.mpf(str(x)) for x in c]
    return lambda s:sum(a*w*mp.dirichlet(s,tab) for a,w,tab in zip(coeff,weights,tables))

def locate(q,c,ceiling):
    def fun(x):
        z=F_values(q,1,c,np.array([x[0]+1j*x[1]]))[0]
        return [z.real,z.imag]
    for sign in (1,-1):
        for t in np.linspace(ceiling-.95,ceiling-.05,7):
            for beta in (.53,.6,.8,1.1,1.6,2.5):
                r=root(fun,[beta,sign*t],tol=1e-11)
                b,h=r.x
                if .50001<b<4 and ceiling-1-1e-7<abs(h)<ceiling+1e-7 and np.linalg.norm(fun(r.x))<1e-8:
                    return complex(b,h)
    raise RuntimeError(f'Racine non localisée q={q} hauteur={ceiling}')

def main():
    out=[]
    jobs=[(7,'relief_v7','col_a1_min'),(7,'relief_v7','col_a1_max'),
          (7,'relief_v7','intermediaire_a1_max'),(7,'relief_v7','bas_a1_min'),
          (11,'independant_v11','v11_0'),(11,'independant_v11','v11_57')]
    for q,name,id in jobs:
        sel=json.loads((D/f'v634_selection_v{q}.json').read_text())
        c=np.array(next(r['coefficients'] for r in sel if r['id']==id))
        row=pd.read_csv(D/f'v634_{name}.csv').set_index('id').loc[id]
        if row.censure:continue
        k=int(row.premiere_detection);z=locate(q,c,k)
        mp.mp.dps=50;f=mp_function(q,c)
        zz=mp.findroot(f,(mp.mpc(z),mp.mpc(z)+mp.mpf('0.00001')),tol=mp.mpf('1e-44'),maxsteps=40)
        residual=abs(f(zz));gap=abs(complex(zz)-z)
        assert residual<mp.mpf('1e-40') and gap<1e-8 and zz.real>mp.mpf('.5')
        result=dict(id=id,q=q,premiere_detection=k,beta_em=z.real,gamma_em=z.imag,
            beta_mp=mp.nstr(zz.real,45),gamma_mp=mp.nstr(zz.imag,45),
            residu_mp=mp.nstr(residual,8),ecart_em_mp=gap,
            partenaire_beta=mp.nstr(1-zz.real,45),partenaire_gamma=mp.nstr(zz.imag,45),
            chiffres=50,certification_intervalles=False)
        out.append(result);print(result,flush=True)
        (D/'v634_racines_recoupees.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
if __name__=='__main__':main()
