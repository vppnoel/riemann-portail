"""Contrôles algébriques exacts ; aucun calcul de la forme de Weil ou de RH."""
from pathlib import Path
import json
import sympy as s
I=s.I
v=s.Matrix
checks=[]
def ck(name,condition,value):
 assert condition,name
 checks.append(dict(test=name,passed=True,value=str(value)))
def q(M,x):return s.expand((x.conjugate().T*M*x)[0])
Q=v([[1,2],[2,1]]);e1=v([1,0]);e2=v([0,1])
ck('diagonales exactes mais mélange négatif',q(Q,e1)==1 and q(Q,e2)==1 and q(Q,e1-e2)==-2,q(Q,e1-e2))
Q=v([[1,2*I],[-2*I,1]]);x,y=s.symbols('x y',real=True)
ck('tous vecteurs réels corrects, phase complexe négative',s.simplify(q(Q,v([x,y]))-x*x-y*y)==0 and q(Q,v([1,I]))==-2,q(Q,v([1,I])))
D=Q-s.eye(2)
a=(e1.conjugate().T*D*e2)[0]
re=(q(D,e1+e2)-q(D,e1-e2))/4
im=-(q(D,e1+I*e2)-q(D,e1-I*e2))/4
ck('polarisation complexe et convention',s.simplify(re+I*im-a)==0,a)
M=s.diag(1,0);b=v([0,1]);MP=M.pinv();delta=1-(b.T*MP*b)[0]
Z=M.row_join(b).col_join(b.T.row_join(v([[1]])))
ck('garde image indispensable malgré dette positive',delta==1 and M*MP*b!=b and q(Z,v([0,-2,1]))==-3,q(Z,v([0,-2,1])))
b=v([1,0]);delta=2-(b.T*MP*b)[0];V=s.diag(1,0);w=(V*MP*b).col_join(v([s.sqrt(delta)]));V3=V.col_join(s.zeros(1,2));W=V3.row_join(w)
G=M.row_join(b).col_join(b.T.row_join(v([[2]])))
ck('insertion Gram singulière compatible',W.T*W==G,G)
# Formule de complétion sur un exemple rationnel non diagonal.
M=v([[2,1],[1,2]]);b=v([1,2]);a=s.Rational(4);xx=v(s.symbols('u v',real=True));yy=s.symbols('w',real=True)
left=(xx.T*M*xx)[0]+2*(xx.T*b)[0]*yy+a*yy**2
right=((xx+M.inv()*b*yy).T*M*(xx+M.inv()*b*yy))[0]+(a-(b.T*M.inv()*b)[0])*yy**2
ck('identité Schur rationnelle',s.expand(left-right)==0,s.expand(left-right))
r={'scope':'Contrôles exacts de lemmes et contre-modèles abstraits; ni matrice de Weil ni évaluation de Suzuki.', 'checks':checks,'passed':len(checks),'RH_proved':False,'Suzuki_identity_proved':False}
Path(__file__).with_name('resultats.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False))
