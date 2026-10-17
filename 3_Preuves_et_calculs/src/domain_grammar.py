"""A sound, deliberately partial arithmetic for compact smooth function domains.

This validates typed contracts, not arbitrary user functions or RH proofs.
Judgment A(S,r,u): support[-S,S], guaranteed exponential moment jets<r,
amplitude unit A**u. The semantic domain is C_c^infty(R), not all of H1.
"""
from dataclasses import dataclass,asdict
from fractions import Fraction as F

@dataclass(frozen=True)
class Word:
    S:F
    jets:int=0
    unit:int=1
    smooth:bool=True
    origin_jets:int=0
    def __post_init__(self):
        object.__setattr__(self,'S',F(self.S))
        if self.S<=0 or self.jets<0 or self.origin_jets<0:raise ValueError('support positif et ordres non négatifs exigés')
    def json(self):return dict(S=str(self.S),jets=self.jets,origin_jets=self.origin_jets,unit=self.unit,smooth=self.smooth)

def translate(op,*args,parameter=0):
    if not args or not all(isinstance(a,Word) for a in args):raise TypeError('mots fonctionnels typés exigés')
    if not all(a.smooth for a in args):raise ValueError('arithmétique A : cœur Cc∞ exigé ; domaine Sobolev distinct')
    f=args[0]
    if op in {'add','multiply','convolve'}:
        if len(args)!=2:raise ValueError('deux fonctions exigées')
        g=args[1]
        if op=='add':
            if f.unit!=g.unit:raise ValueError('addition exige unités identiques')
            return Word(max(f.S,g.S),min(f.jets,g.jets),f.unit,origin_jets=min(f.origin_jets,g.origin_jets))
        if op=='multiply':return Word(min(f.S,g.S),0,f.unit+g.unit,f.smooth and g.smooth)
        return Word(f.S+g.S,f.jets+g.jets,f.unit+g.unit,origin_jets=f.origin_jets+g.origin_jets)
    if op=='P':
        if not f.smooth:raise ValueError('ce contrat de jets exige un cœur lisse ; utiliser contrat H0^3 séparé')
        return Word(f.S,f.jets+1,f.unit,origin_jets=f.origin_jets)
    if op=='derivative':
        if not f.smooth:raise ValueError('domaine de dérivation non fourni')
        return Word(f.S,f.jets,f.unit,origin_jets=f.origin_jets+1)
    if op=='position':return Word(f.S,max(0,f.jets-1),f.unit,origin_jets=max(0,f.origin_jets-1))
    if op=='translate':return Word(f.S+abs(F(parameter)),f.jets,f.unit,origin_jets=f.origin_jets)
    if op in {'scalar','phase','conjugate'}:return f
    if op=='modulate':
        if F(parameter)==0:return f
        return Word(f.S,0,f.unit,f.smooth)
    if op=='rescale':
        if F(parameter)<=0:raise ValueError('échelle positive exigée')
        return Word(f.S*F(parameter),0,f.unit,f.smooth,origin_jets=f.origin_jets)
    raise ValueError('règle non définie : '+op)

def assert_admissible(word):
    if word.jets<1:raise ValueError('moments exponentiels nuls non garantis')
    return True

def allow_global_sign(*,all_supports=False,tail_certified=False,schur_psd_certified=False):
    if not(all_supports and tail_certified and schur_psd_certified):raise ValueError('signe global : tous supports, queue et Schur certifiés requis')
    return 'implication conditionnelle ; les prémisses doivent être réellement établies'

RULES=[
 dict(op='add',label='Additionner',input='A(S,r,u), A(T,s,u)',output='A(max(S,T),min(r,s),u)',conserves='annulations communes',loss='annulations au-delà du minimum non garanties'),
 dict(op='scalar',label='Multiplier par un nombre',input='c∈ℂ, A(S,r,u)',output='A(S,r,u)',conserves='annulations ; Q,R multipliés par |c|²',loss='c=0 efface le test'),
 dict(op='multiply',label='Multiplier point par point',input='A(S,r,u), A(T,s,v)',output='A(min(S,T),0,u+v)',conserves='support intérieur et lissage',loss='moments généralement perdus'),
 dict(op='convolve',label='Convoluer',input='A(S,r,u), A(T,s,v)',output='A(S+T,r+s,u+v)',conserves='jets : leurs ordres se renforcent',loss='support et budget premier grandissent'),
 dict(op='P',label='Passer dans le moule P',input='A(S,r,u)',output='A(S,r+1,u)',conserves='support ; un ordre de jets gagné',loss='dérivées et Q changent'),
 dict(op='derivative',label='Dériver dans x',input='A(S,r,u)',output='A(S,r,u)',conserves='jets fixes aux deux points ±1/2',loss='coût de dérivée ; domaine plus exigeant'),
 dict(op='position',label='Multiplier par x',input='A(S,r+1,u)',output='A(S,r,u)',conserves='support',loss='un ordre de jets garanti perdu'),
 dict(op='translate',label='Déplacer la valise',input='A(S,r,u)',output='A(S+|a|,r,u)',conserves='h,Q,R et diamètre ; jets',loss='fenêtre centrée élargie ; translation n’est pas homomorphisme conv'),
 dict(op='phase',label='Tourner tout le dessin',input='A(S,r,u)',output='A(S,r,u)',conserves='moments,h,Q,R',loss='phase variable n’est pas cette règle'),
 dict(op='conjugate',label='Miroir complexe',input='A(S,r,u)',output='A(S,r,u)',conserves='jets car poids réels',loss='action sur phases explicite'),
 dict(op='modulate',label='Tourner selon la position',input='A(S,r,u), τ≠0',output='A(S,0,u)',conserves='L² ; algèbre convolution',loss='points fixes de jets perdus ; Q change'),
 dict(op='rescale',label='Changer d’échelle',input='A(S,r,u), λ>0',output='A(λS,0,u)',conserves='support redimensionné',loss='moments et Q non conservés en général')]

for rule in RULES:
    rule['proof']='V644_LANGUE_ET_DOMAINES.md, L8 ; core Cc∞ only'
    rule['origin_order']={'add':'min(q_f,q_g)','multiply':'0 guaranteed','convolve':'q_f+q_g',
        'P':'q_f','derivative':'q_f+1','position':'max(0,q_f−1)','translate':'q_f',
        'phase':'q_f','scalar':'q_f','conjugate':'q_f','modulate':'0 if τ≠0','rescale':'q_f'}[rule['op']]

def examples():
    f=Word(F(1),1);g=Word(F(2),2)
    return [dict(operation=op,input=[a.json() for a in args],output=translate(op,*args,parameter=parameter).json())
        for op,args,parameter in [('add',[f,g],0),('multiply',[f,g],0),('convolve',[f,g],0),('P',[f],0),('position',[f],0),('translate',[f],F(2)),('modulate',[f],F(1))]]
