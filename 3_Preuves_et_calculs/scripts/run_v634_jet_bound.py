"""V6.34 : paramètres sans comptage préalable, puis certificats exacts des jets."""
from pathlib import Path
import json,sys,csv
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from jet_bound import optimize,certificate,square_points,explicit_sqrt_parameters

def main():
    f=[1,1,0,1];out=[]
    # Enregistrer les paramètres indépendamment des points de la courbe.
    params=[optimize(p) for p in (29,61,101,1009,10007)]
    (ROOT/'data/v634_jets_parametres.json').write_text(json.dumps(params,indent=2),encoding='utf-8')
    for r in params:
        p=r['p'];S,z=square_points(f,p)
        nr=next(x for x in range(2,p) if pow(x,(p-1)//2,p)==p-1)
        St,zt=square_points([nr*c%p for c in f],p)
        assert S and len(S)+len(St)+z==p and z==zt
        c=certificate(p,f,r['J'],r['K'],r['M']) if p<=101 else dict(r,f=f,S=len(S),racines_f=z,points_courbe=2*len(S)+z+1)
        U=r['borne_S'];c.update(S_tordu=len(St),non_residu=nr,
            borne_points_superieure=2*U+z+1,borne_points_inferieure=2*p-z-2*U+1,
            borne_ecart=2*U-p+z,famille_racine_carree=explicit_sqrt_parameters(p))
        assert len(S)<=U and len(St)<=U
        out.append(c)
        print({k:v for k,v in c.items() if k not in ('coefficients_temoin','vecteur_noyau')},flush=True)
    (ROOT/'data/v634_jets_certificats.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    cols=['p','J','K','M','dimension','rang_majore','borne_S','S','S_tordu','points_courbe','borne_ecart']
    with (ROOT/'data/v634_jets.csv').open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=cols,extrasaction='ignore');w.writeheader();w.writerows(out)
if __name__=='__main__':main()
