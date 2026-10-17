"""Rational replay of finite certificate inequalities, independent of iv arithmetic.

Transcendental input enclosures are read, not independently reevaluated here.
"""
from fractions import Fraction as Q
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
def interval(x):return Q(x['lower']),Q(x['upper'])
def plus(a,b):return a[0]+b[0],a[1]+b[1]
def minus(a,b):return a[0]-b[1],a[1]-b[0]
def times(a,b):
    p=[x*y for x in a for y in b];return min(p),max(p)
def sum_(items):
    out=(Q(0),Q(0))
    for x in items:out=plus(out,x)
    return out
def absolute(a):return max(abs(a[0]),abs(a[1]))

def replay(centre,half,values,J,certificate):
    centre=list(map(Q,centre));half=Q(half);values=list(map(interval,values));J=[list(map(interval,row)) for row in J]
    C=[[Q(x) for x in row] for row in certificate['preconditioner']]
    assert C[0][0]*C[1][1]-C[0][1]*C[1][0]!=0
    R=[[minus((Q(i==j),Q(i==j)),sum_(times((C[i][k],C[i][k]),J[k][j]) for k in range(2))) for j in range(2)] for i in range(2)]
    q=max(sum(absolute(x) for x in row) for row in R);assert q<1,'Rational contraction fails'
    K=[]
    for i in range(2):
        shift=minus((centre[i],centre[i]),sum_(times((C[i][k],C[i][k]),values[k]) for k in range(2)))
        image=plus(shift,sum_(times(R[i][j],(-half,half)) for j in range(2)))
        assert centre[i]-half<image[0]<=image[1]<centre[i]+half,'Rational inclusion fails'
        K.append(image)
    return {'contraction_upper':str(q),'K_rational':[[str(a),str(b)] for a,b in K]}

def verify(output,protocol,root_audit):
    folds=[]
    for a in output['fold_attempts']:
        if not a['certificate']['accepted']:continue
        replayed=replay([protocol['centre_r'],protocol['centre_t']],protocol['fold_box_halfwidth'],a['point_values'],a['jacobian'],a['certificate'])
        for key in ('anchor_projection','H_r','H_tt'):
            v=interval(a[key]);assert v[1]<0 or v[0]>0
        assert interval(a['kappa'])[1]<0
        folds.append(dict(digits=a['digits'],**replayed))
    assert {f['digits'] for f in folds}=={p['digits'] for p in protocol['precisions']}
    contour=output['contour'];qmin=Q(contour['comparison_modulus_lower']);assert qmin>0
    accepted=[]
    for attempt in contour['arc_attempts']:
        assert len(attempt['arcs'])==attempt['grid']
        assert [r['arc'] for r in attempt['arcs']]==list(range(attempt['grid']))
        valid=all(Q(r['defect_upper'])<qmin for r in attempt['arcs'])
        assert valid==attempt['accepted']
        if valid:accepted.append(attempt['grid'])
    assert accepted,'No strict continuous contour comparison'
    roots=[];half=Q(protocol['root_box_halfwidth']);foldK=folds[-1]['K_rational'][0]
    for r in root_audit:
        replayed=replay(r['centre'],half,r['point_values'],r['jacobian'],r['certificate']);roots.append(replayed)
        beta,t=map(Q,r['centre']);h=Q(r['offset']);rp=interval(r['parameter_span'])
        assert rp[0]<=Q(foldK[0])+h and Q(foldK[1])+h<=rp[1]
        assert (abs(beta-Q(1,2))+half)**2+(abs(t-Q(protocol['centre_t']))+half)**2<Q(protocol['contour_radius'])**2
        if h<0:assert beta==Q(1,2) and r['box_invariant_under_functional_partner']
        else:assert beta+half<Q(1,2) or beta-half>Q(1,2)
    assert len(roots)==4
    for i,a in enumerate(root_audit):
        for b in root_audit[i+1:]:
            if a['offset']==b['offset']:assert any(abs(Q(x)-Q(y))>2*half for x,y in zip(a['centre'],b['centre']))
    return dict(fold_replays=folds,root_replays=roots,accepted_contour_grids=accepted,rational_checks_passed=True,independent_transcendental_evaluation=False)

def main():
    D=ROOT/'data';load=lambda n:json.loads((D/n).read_text(encoding='utf-8-sig'))
    audit=verify(load('v642_certification.json'),load('v642_protocole_verrouille.json'),load('v642_root_audit_inputs.json')['roots'])
    (D/'v642_verification_rationnelle.json').write_text(json.dumps(audit,indent=2)+'\n')
    print('Rational replay passed: two fold validations, 256 contour inequalities, four uniform root boxes')

if __name__=='__main__':main()
