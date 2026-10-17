"""V6.34 : validation directe V7 et test indépendant V11.

Les prévisions sont dans data/prevision_v634_relief.md. Les résultats ne
remplacent pas la carte historique ; ils sont conservés sous le préfixe v634.
"""
from pathlib import Path
import argparse,json,math,sys,time
import numpy as np,pandas as pd
from scipy.special import zeta
from scipy.stats import spearmanr
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'data';sys.path.insert(0,str(ROOT/'src'))
from relief_direct import DirectGrid,completed_phase_basis,a1_and_defect,partial_rank

def chart_coeff(u,v):
    n=np.ones(3)/np.sqrt(3);a=np.array([1.,-1.,0.])/np.sqrt(2);b=np.cross(n,a)
    c=n+u*a+v*b;return c/np.linalg.norm(c)

def calibration_selection():
    f=pd.read_csv(D/'force_multiplicativite.csv')
    groups=[('col',f[f.T_premiere_paire==145]),('intermediaire',f[(f.T_premiere_paire>=40)&(f.T_premiere_paire<=60)]),
        ('censure',f[f.T_premiere_paire>300]),('bas',f[f.T_premiere_paire<=10])]
    out=[]
    for label,g in groups:
        for side,(_,r) in zip(('a1_min','a1_max'),g.sort_values('a1').iloc[[0,-1]].iterrows()):
            c=chart_coeff(r.u,r.v)
            out.append(dict(id=label+'_'+side,u=float(r.u),v=float(r.v),T_proxy=float(r.T_premiere_paire),
                a1=float(r.a1),distance=float(r.distance),coefficients=c.tolist(),euler=False))
    for i,c in enumerate(np.eye(3)):out.append(dict(id='euler_'+str(i),coefficients=c.tolist(),T_proxy=None,euler=True))
    (D/'v634_selection_v7.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    return out

def evaluate(q,T,selection,name):
    C=np.array([r['coefficients'] for r in selection]);a1,defect=a1_and_defect(q,1,C)
    sig=3.
    while np.sqrt(C.shape[1])*(zeta(sig,1)-1)>=a1.min():sig+=1
    print('Préparation',name,'n=',len(C),'T=',T,'sigma=',sig,flush=True)
    grid=DirectGrid(q,1,T,.02,sig,.05,D/f'v634_cache_q{q}_T{T}_h002_R{sig:g}.npz')
    total,crit,off,diag=grid.counts(C)
    tf=np.arange(-T/.01,T/.01+1)*.01
    finefile=D/f'v634_critique_q{q}_T{T}_h001.npz'
    if finefile.exists():Bfine=np.load(finefile)['B']
    else:
        Bfine=completed_phase_basis(q,1,.5+1j*tf).real
        np.savez_compressed(finefile,B=Bfine)
    Z=C@Bfine;fine=[]
    for z in Z:
        ids=np.flatnonzero(z[1:]*z[:-1]<0);roots=tf[ids]-.01*z[ids]/(z[ids+1]-z[ids])
        fine.append(np.searchsorted(np.sort(np.abs(roots)),grid.levels,side='right'))
    fine=np.array(fine);off_fine=total-fine
    # Le raffinement doit aussi contrôler le bord vertical du contour.
    rightfile=D/f'v634_droit_q{q}_T{T}_h001_R{sig:g}.npz'
    if rightfile.exists():Br=np.load(rightfile)['B']
    else:
        Br=completed_phase_basis(q,1,sig+1j*tf)
        np.savez_compressed(rightfile,B=Br)
    rr=C@Br;inc=np.angle(rr[:,1:]/rr[:,:-1])
    ph=np.c_[np.zeros(len(C)),np.cumsum(inc,axis=1)]
    lo=np.rint((-grid.levels-tf[0])/.01).astype(int);hi=np.rint((grid.levels-tf[0])/.01).astype(int)
    coarse=C@grid.Bright;ci=np.angle(coarse[:,1:]/coarse[:,:-1])
    cp=np.c_[np.zeros(len(C)),np.cumsum(ci,axis=1)]
    clo=np.rint((-grid.levels-grid.t[0])/.02).astype(int);chi=np.rint((grid.levels-grid.t[0])/.02).astype(int)
    delta=(ph[:,hi]-ph[:,lo]-(cp[:,chi]-cp[:,clo]))/math.pi
    diag['max_phase_vertical_fin']=float(np.max(np.abs(inc)))
    diag['max_ecart_enroulement_pas']=float(np.max(np.abs(delta)))
    if diag['unresolved_horizontal_rows'] or np.max(np.abs(delta))>1e-6:
        raise RuntimeError('Contour encore ambigu : résultat non accepté')
    rows=[]
    for i,r in enumerate(selection):
        hits=np.flatnonzero(off_fine[i]>0);first=int(hits[0]+1) if len(hits) else None
        hitold=np.flatnonzero(off[i]>0);firstold=int(hitold[0]+1) if len(hitold) else None
        bad=bool(np.any(off_fine[i]<0)|np.any(off_fine[i]%2!=0))
        rr={k:v for k,v in r.items() if k!='coefficients'}
        rr.update(q=q,a1=float(a1[i]),defaut=float(defect[i]),premiere_detection=first,
            censure=first is None,total_Tmax=int(total[i,-1]),droite_Tmax=int(fine[i,-1]),
            hors_droite_Tmax=int(off_fine[i,-1]),premiere_stable_pas=first==firstold,
            niveaux_differents_pas=int(np.sum(fine[i]!=crit[i])),comptage_pair_nonnegatif=not bad)
        rows.append(rr)
        print(rr,flush=True)
    pd.DataFrame(rows).to_csv(D/f'v634_{name}.csv',index=False)
    np.savez_compressed(D/f'v634_{name}_comptages.npz',total=total,critical=fine,off=off_fine,levels=grid.levels,coefficients=C)
    rep=dict(q=q,Tmax=T,nombre=len(rows),diagnostics=diag,
        nombres_stables_first=int(sum(r['premiere_stable_pas'] for r in rows)),
        tous_pairs_nonnegatifs=all(r['comptage_pair_nonnegatif'] for r in rows),
        niveaux_modifies=int(np.sum(crit!=fine)),
        euler_sans_hors_droite=all(r['hors_droite_Tmax']==0 for r in rows if r['euler']))
    if q==7:
        ordinary=[r for r in rows if not r['euler']]
        rep['P3_proches_proxy']=sum(r['premiere_detection'] is not None and abs(r['premiere_detection']-r['T_proxy'])<=2 for r in ordinary)
        rep['P3_nombre']=len(ordinary)
        rep['proxy_et_direct_censures']=sum(r['censure'] and r['T_proxy']>T for r in ordinary)
        rep['P3_statut']='non validée : 4 concordances observées, 2 désaccords, 2 censures'
    else:
        mask=np.array([not r['euler'] and r['comptage_pair_nonnegatif'] and r['premiere_stable_pas'] for r in rows])
        H=np.array([r['premiere_detection'] or T+1 for r in rows],dtype=float)
        dist=np.arccos(np.clip(np.max(np.abs(C),axis=1),0,1))
        n=int(mask.sum());rep['echantillon_valide']=n
        if n>10:
            xx,aa,dd,di=H[mask],a1[mask],defect[mask],dist[mask]
            rep['corr_T_a1_sachant_distance']=partial_rank(xx,aa,di)
            rep['corr_T_D_sachant_distance_a1']=partial_rank(xx,dd,np.c_[di,aa])
            rep['corr_T_distance']=float(spearmanr(xx,di).statistic)
            unc=xx<=T
            rep['corr_T_a1_non_censures']=partial_rank(xx[unc],aa[unc],di[unc])
            rg=np.random.default_rng(6341102);boots=[];bootsD=[]
            for _ in range(1000):
                k=rg.integers(0,n,n);boots.append(partial_rank(xx[k],aa[k],di[k]))
                bootsD.append(partial_rank(xx[k],dd[k],np.c_[di[k],aa[k]]))
            rep['bootstrap_a1_IC95']=np.quantile(boots,[.025,.975]).tolist()
            rep['bootstrap_D_IC95']=np.quantile(bootsD,[.025,.975]).tolist()
            rep['censures']=int(sum(r['censure'] for r in rows if not r['euler']))
    (D/f'v634_{name}.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf-8')
    print('RÉSUMÉ',json.dumps(rep,ensure_ascii=False),flush=True)
    return rows,rep

def main():
    p=argparse.ArgumentParser();p.add_argument('--part',choices=['v7','v11','all'],default='all');args=p.parse_args()
    if args.part in ('v7','all'):evaluate(7,300,calibration_selection(),'relief_v7')
    if args.part in ('v11','all'):
        rg=np.random.default_rng(6341101);C=rg.normal(size=(96,5));C/=np.linalg.norm(C,axis=1)[:,None]
        selection=[dict(id='v11_'+str(i),coefficients=c.tolist(),euler=False) for i,c in enumerate(C)]
        selection +=[dict(id='euler_'+str(i),coefficients=c.tolist(),euler=True) for i,c in enumerate(np.eye(5))]
        (D/'v634_selection_v11.json').write_text(json.dumps(selection,indent=2),encoding='utf-8')
        evaluate(11,150,selection,'independant_v11')
if __name__=='__main__':main()
