"""V6.37 : protocole verrouillé puis comptage direct des couples V13.

Les grilles q13 ne sont créées qu'après --prepare. Les contrôles restent
numériques : aucun certificat d'arithmétique d'intervalles n'est revendiqué.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import time
import numpy as np
import pandas as pd
from scipy.special import zeta

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / 'data'
sys.path.insert(0, str(ROOT / 'src'))
from relief_direct import DirectGrid, completed_phase_basis, a1_and_defect
from v637_apparie import build_selection, analysis

MANIFEST = D / 'v637_selection_v13.json'
LOCK = D / 'v637_protocole_verrouille.json'
PREVISION = ROOT.parent / '4_Archives/recus/V637/prevision_v637_apparie.md'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    if MANIFEST.exists() or LOCK.exists() or (D / 'v637_v13_comptages.npz').exists() or list(D.glob('v637_cache*.npz')):
        raise RuntimeError('Un protocole ou calcul existe : ne pas réécrire la sélection.')
    manifest = build_selection()
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    PREVISION.parent.mkdir(parents=True,exist_ok=True)
    PREVISION.write_text('''# V6.37 - Ancrage apparié V13 : prévision avant comptage

Suite de la question inscrite dans le navigateur V6.36. V13 est l'espace
impair modulo 13 (six caractères). La génération et l'appariement n'utilisent
aucune évaluation de fonction L ni aucun zéro. La spécification complète,
les graines, les calipers et les strates infaisables figurent dans le manifeste.

Les couples contrôlent exactement l'ancre d'Euler et l'angle projectif.
Dans le bras A1, le défaut D est proche et |a(1)| varie ; dans le bras D,
|a(1)| est proche et D varie. L'appariement reste descriptif, sans interprétation
causale ni échantillonnage aléatoire d'une population.

P1 : les six témoins d'Euler ne présentent aucune détection hors droite sous 150.
P2 : les comptages total et critique sont cohérents et stables aux raffinements.
P3 : dans le bras A1, les signes strictement comparables favorisent davantage une
première détection plus tardive lorsque |a(1)| augmente (plus de signes positifs
que négatifs). Publier les égalités, les non-détections et les ordres indéterminés.
P4 : dans le bras D, la direction du contraste n'est pas uniforme entre ancres
et rayons. Un signe contraire ne constitue pas une preuve d'absence d'effet.

Plafond fixé à 150 ; bilans à 50, 100 et 150. Pas verticaux 0,02 et 0,01 ;
pas horizontaux maximaux 0,05 et 0,025, puis raffinement adaptatif. La droite
critique est également reprise à 0,005 pour toutes les directions. Tout niveau
non résolu, différence de comptage, défaut de parité ou marge relative de bord
inférieure à 1e-10 rend la direction non admissible dans le résumé principal.
Le bord droit est choisi par domination du premier coefficient, avant comptage.

Recoupement indépendant à 50 chiffres : premier couple de chaque bras et ancre
au rayon médian, pour chaque membre présentant une détection admissible. Les
cas où aucune racine n'est localisée sont conservés comme tels. Cette vérification
confirme des racines représentatives, pas l'absence de racines ailleurs.

La première détection est une tranche de hauteur entière pour |Im(s)|. Ce n'est
pas une ordonnée continue exacte. Le numérateur des zéros hors droite est obtenu
par contour moins changements de signe de Hardy : un zéro double ou une paire
critique très proche peut être manqué par les changements de signe. Même après
raffinement et recoupement, ces comptages ne sont pas des certificats d'intervalles.

Conserver les échecs de prévision. Aucune conclusion de RH, de GRH ni de
positivité globale ne résulte de cette expérience finie.
''', encoding='utf-8')
    (D/'prevision_v637_apparie.md').write_text(PREVISION.read_text(encoding='utf-8'),encoding='utf-8-sig')
    lock = dict(selection_sha256=digest(MANIFEST), prevision_sha256=digest(PREVISION),
                created_unix=time.time(), zero_counts_started=False,
                q=13, parity=1, Tmax=150, ceilings=[50,100,150],
                critical_steps=[.02,.01,.005], horizontal_steps=[.05,.025],
                minimum_relative_boundary_margin=1e-10,
                predictions={'P3':'positive > negative among comparable signs',
                             'P4':'contrast direction not uniform across anchor/radius strata'},
                data_independent_selection=True)
    LOCK.write_text(json.dumps(lock, indent=2), encoding='utf-8')
    print('PROTOCOLE VERROUILLE', len(manifest['selection']), 'points, contrôles inclus;', len(manifest['pairs']), 'couples', flush=True)
    print('SELECTION SHA256', lock['selection_sha256'], flush=True)
    print('STRATES FAISABLES',sum(x['complete'] for x in manifest['feasibility']), '/',len(manifest['feasibility']),flush=True)


def critical_from_basis(C, basis, t, levels):
    out = []
    dt = t[1]-t[0]
    for values in C @ basis:
        ids = np.flatnonzero(values[:-1]*values[1:] < 0)
        roots = t[ids] - dt*values[ids]/(values[ids+1]-values[ids])
        out.append(np.searchsorted(np.sort(np.abs(roots)), levels, side='right'))
    return np.asarray(out, dtype=int)


def boundary_margins(C, grid):
    H = np.einsum('nd,dtk->ntk', C, grid.Bhorizontal)
    scaleH = np.einsum('nd,dtk->ntk', np.abs(C), np.abs(grid.Bhorizontal))
    R = C @ grid.Bright
    scaleR = np.abs(C) @ np.abs(grid.Bright)
    horizontal = np.min(np.abs(H)/np.maximum(scaleH,1e-300),axis=(1,2))
    vertical = np.min(np.abs(R)/np.maximum(scaleR,1e-300),axis=1)
    return horizontal, vertical


def run():
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    lock = json.loads(LOCK.read_text(encoding='utf-8'))
    if digest(MANIFEST) != lock['selection_sha256'] or digest(PREVISION) != lock['prevision_sha256']:
        raise RuntimeError('Le protocole ou la sélection ont changé après verrouillage.')
    selection = manifest['selection']
    C = np.asarray([x['coefficients'] for x in selection])
    a1, defect = a1_and_defect(13,1,C)
    right = 3.
    while math.sqrt(C.shape[1])*(zeta(right,1)-1) >= a1.min():
        right += 1
    started = time.time()
    print('CALCUL V13 :',len(C),'directions, bord droit',right,flush=True)
    grids=[]; totals=[]; critical=[]; diags=[]; margins=[]
    for dt, ds in ((.02,.05),(.01,.025)):
        print('GRILLE',dt,'horizontale',ds,flush=True)
        grid = DirectGrid(13,1,150,dt,right,ds,D/f'v637_cache_q13_T150_h{dt:g}_ds{ds:g}_R{right:g}.npz')
        total,crit,off,diag = grid.counts(C)
        grids.append(grid); totals.append(total); critical.append(crit); diags.append(diag)
        margins.append(boundary_margins(C,grid))
        print('DIAGNOSTIC',json.dumps(diag),flush=True)
    t = np.arange(-30000,30001)*.005
    print('DROITE CRITIQUE : pas 0.005',flush=True)
    basis = completed_phase_basis(13,1,.5+1j*t)
    crit005 = critical_from_basis(C,basis.real,t,grids[0].levels)
    imaginary_residual = float(np.max(np.abs(basis.imag)))
    total = totals[-1]; crit = crit005; off = total-crit
    total_stable = np.all(totals[0]==totals[1],axis=1)
    crit_stable = np.all(critical[0]==critical[1],axis=1)&np.all(critical[1]==crit005,axis=1)
    marginH = np.minimum(margins[0][0],margins[1][0])
    marginR = np.minimum(margins[0][1],margins[1][1])
    global_resolved = all(x['unresolved_horizontal_rows']==0 and x['max_integer_residual']<1e-8 and x['max_phase_vertical']<.8 for x in diags)
    rows=[]
    for i, record in enumerate(selection):
        hits=np.flatnonzero(off[i]>0)
        first=int(hits[0]+1) if len(hits) else None
        parity=bool(np.all(off[i]>=0)&np.all(off[i]%2==0))
        monotone=bool(np.all(np.diff(total[i])>=0))
        critical_monotone=bool(np.all(np.diff(crit[i])>=0))
        off_monotone=bool(np.all(np.diff(off[i])>=0))
        stable=bool(total_stable[i] and crit_stable[i] and parity and monotone and critical_monotone and off_monotone and global_resolved and marginH[i]>=1e-10 and marginR[i]>=1e-10)
        row={k:v for k,v in record.items() if k!='coefficients'}
        row.update(first_detected=first,previous_level=first-1 if first else 150,
                   stable=stable,a1=float(a1[i]),D=float(defect[i]),
                   total_stable=bool(total_stable[i]),critical_stable=bool(crit_stable[i]),
                   paired_nonnegative=parity,total_monotone=monotone,
                   critical_monotone=critical_monotone,off_monotone=off_monotone,
                   censure=first is None,boundary_horizontal_min=float(marginH[i]),
                   boundary_vertical_min=float(marginR[i]),
                   total_Tmax=int(total[i,-1]),critical_Tmax=int(crit[i,-1]),off_Tmax=int(off[i,-1]))
        rows.append(row)
    pd.DataFrame(rows).to_csv(D/'v637_v13.csv',index=False)
    np.savez_compressed(D/'v637_v13_comptages.npz',coefficients=C,levels=grids[0].levels,
        total_coarse=totals[0],total_fine=totals[1],critical_coarse=critical[0],
        critical_fine=critical[1],critical_finest=crit005,off=off)
    result=dict(q=13,parity=1,dimension=6,Tmax=150,selection_sha256=digest(MANIFEST),
        prevision_sha256=digest(PREVISION),n_directions=sum(not r['euler'] for r in selection),n_pairs=len(manifest['pairs']),
        n_controls=sum(r['euler'] for r in selection),n_stable=sum(r['stable'] for r in rows),
        diagnostics=diags,critical_imaginary_residual=imaginary_residual,
        n_total_changed=int(np.sum(totals[0]!=totals[1])),
        n_critical_changed_001=int(np.sum(critical[0]!=critical[1])),
        n_critical_changed_0005=int(np.sum(critical[1]!=crit005)),
        euler_no_detection=all(r['first_detected'] is None and r['stable'] for r in rows if r['euler']),
        n_nondetections=sum(r['first_detected'] is None for r in rows if not r['euler']),
        seconds=time.time()-started,arithmetic='float64 with numerical refinement; no interval certification',
        analysis=analysis(manifest,rows,ceilings=(50,100,150)))
    (D/'v637_v13.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('RESULTAT',json.dumps({k:v for k,v in result.items() if k!='analysis'},ensure_ascii=False),flush=True)


def postchecks():
    """Contrôles de classification sur les grilles déjà enregistrées."""
    manifest=json.loads(MANIFEST.read_text(encoding='utf-8'))
    lock=json.loads(LOCK.read_text(encoding='utf-8'))
    if digest(MANIFEST)!=lock['selection_sha256'] or digest(PREVISION)!=lock['prevision_sha256']:
        raise RuntimeError('Empreinte du protocole modifiée.')
    result=json.loads((D/'v637_v13.json').read_text(encoding='utf-8'))
    frame=pd.read_csv(D/'v637_v13.csv')
    counts=np.load(D/'v637_v13_comptages.npz')
    for name,arrayname in (('total_monotone','total_fine'),('critical_monotone','critical_finest'),('off_monotone','off')):
        frame[name]=np.all(np.diff(counts[arrayname],axis=1)>=0,axis=1)
        frame['stable']=frame['stable']&frame[name]
    records=frame.to_dict(orient='records')
    for r in records:
        r['first_detected']=None if pd.isna(r['first_detected']) else int(r['first_detected'])
        r['stable']=bool(r['stable']);r['euler']=bool(r['euler'])
    frame.to_csv(D/'v637_v13.csv',index=False)
    result.update(n_stable=sum(r['stable'] for r in records),
        euler_no_detection=all(r['first_detected'] is None and r['stable'] for r in records if r['euler']),
        n_nondetections=sum(r['first_detected'] is None and r['stable'] for r in records if not r['euler']),
        n_ambiguous=sum(not r['stable'] for r in records),
        n_ambiguous_nondetections=sum(r['first_detected'] is None and not r['stable'] for r in records if not r['euler']),
        all_off_monotone=bool(frame.off_monotone.all()),all_critical_monotone=bool(frame.critical_monotone.all()),
        boundary_margins_are_sampled=True,
        analysis=analysis(manifest,records,ceilings=(50,100,150)))
    (D/'v637_v13.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    for report in result['analysis']['reports']:
        print('BILAN',report['ceiling'],json.dumps(report['arms'],ensure_ascii=False),flush=True)
    print('ADMISSIBLES',result['n_stable'],'MONOTONIE',result['all_off_monotone'],'NON-DETECTIONS',result['n_nondetections'],'AMBIGUS',result['n_ambiguous'],flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--postchecks',action='store_true')
    args=parser.parse_args()
    if args.prepare: prepare()
    if args.run: run()
    if args.postchecks: postchecks()
    if not(args.prepare or args.run or args.postchecks): parser.error('choisir --prepare puis --run ou --postchecks')
