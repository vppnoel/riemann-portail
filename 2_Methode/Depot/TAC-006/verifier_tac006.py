"""TAC-006 — relecture rationnelle des inégalités finies du certificat (sans opération d'intervalles).

Auteur des droits : Vincent NOËL. Producteur : ia:claude, 18 octobre 2026.
Relit resultats_tac006.json, reconstruit les bornes binaires exactes en fractions et recontrôle :
inclusions strictes K ⊂ int B (pli aux deux plans, quatre racines), séparations de H_lam, H_tt et de la
projection d'ancre, symétrie ou exclusion de la droite critique, disjonction des boîtes et appartenance au
disque de Rouché. Comme au document 66, ne réévalue pas les primitives transcendantes.
Usage : python -I verifier_tac006.py
"""
import json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, 'resultats_tac006.json')))
checks = []
def check(name, ok): checks.append((name, bool(ok))); print(('OK   ' if ok else 'ÉCHEC'), name)

def ep(e):
    sign, man, exp, _ = e
    v = F(man * (1 << exp)) if exp >= 0 else F(man, 1 << (-exp))
    return -v if sign else v
def bounds(enc): return ep(enc['binary_endpoints'][0]), ep(enc['binary_endpoints'][1])
def sep(enc):
    lo, hi = bounds(enc); return lo > 0 or hi < 0

for plan in ('P1_pli_50', 'P1_pli_80'):
    x = d[plan]; c = [F(s) for s in x['centre']]; h = F(x['halfwidth'])
    for i, name in enumerate(('lam', 't')):
        lo, hi = bounds(x['K'][i])
        check(f'{plan} : K_{name} strictement dans la boîte', c[i] - h < lo and hi < c[i] + h)
    check(f'{plan} : contraction < 1', x['contraction_upper'] < 1)
    check(f'{plan} : H_lam séparé de 0 (transversalité sur la fibre)', sep(x['H_lam_box']))
    check(f'{plan} : H_tt séparé de 0 (zéro exactement double)', sep(x['H_tt_box']))
    check(f'{plan} : projection d\'ancre séparée de 0 (lemme I2)', sep(x['anchor_projection_box']))
    lo, hi = bounds(x['K'][0]); check(f'{plan} : |lam*| < 1e-6 (P1)', max(abs(lo), abs(hi)) < F(1, 10 ** 6))
    lo, hi = bounds(x['K'][1]); check(f'{plan} : |t* - 5| < 1e-6 (P1)', max(abs(lo - 5), abs(hi - 5)) < F(1, 10 ** 6))

# Rouché (révision du 18 octobre) : tous les centres de la boîte de t* et tout λ de [boîte de λ* ± 10⁻⁴]
R = F(d['P2_rouche']['R'])
P2 = d['P2_rouche']; ar, ai = (F(x) for x in P2['alpha']); cmp_, dfm = F(P2['comparison_lower_exact']), F(P2['defect_upper_max_exact'])
check('P2 : Rouché accepté, défaut max < comparaison (fractions exactes)', P2['accepted'] and dfm < cmp_ and F(P2['margin_lower_exact']) == cmp_ - dfm)
check('P2 : la comparaison est un minorant de |alpha| R² (carrés rationnels)', cmp_ > 0 and cmp_ ** 2 <= (ar * ar + ai * ai) * R ** 4)
check('P2 : décimales exportées extérieures', F(P2['comparison_lower']) <= cmp_ and F(P2['defect_upper_max']) >= dfm and F(P2['margin_lower']) <= cmp_ - dfm)
lam_c_, t_c_ = (F(x) for x in d['P1_pli_50']['centre']); hw = F(d['P1_pli_50']['halfwidth'])
check('P2 : λ couvert ⊇ [boîte du pli ± 10⁻⁴] et centres ⊇ boîte de t*',
      F(P2['lam_couvert'][0]) <= lam_c_ - hw - F(1, 10 ** 4) and F(P2['lam_couvert'][1]) >= lam_c_ + hw + F(1, 10 ** 4)
      and F(P2['centres_couverts'][0]) <= t_c_ - hw and F(P2['centres_couverts'][1]) >= t_c_ + hw)

boxes = []
for side, critical in (('P3_moins', None), ('P3_plus', None)):
    for b in d[side]['boites']:
        c = [F(s) for s in b['centre']]; h = F(b['halfwidth'])
        re, im = bounds(b['Re_s']), bounds(b['Im_s'])
        check(f'{side} : K strictement dans la boîte', c[0] - h < re[0] and re[1] < c[0] + h and c[1] - h < im[0] and im[1] < c[1] + h)
        check(f'{side} : contraction < 1', b['contraction_upper'] < 1)
        crit = c[0] == F(1, 2)
        if crit: check(f'{side} : boîte invariante par s -> 1 - conj(s) (centre Re = 1/2)', True)
        else: check(f'{side} : boîte exclut la droite critique', re[0] > F(1, 2) or re[1] < F(1, 2))
        # w = -i(s - 1/2) : Re w = Im s, Im w = 1/2 - Re s ; le carré de la boîte est dans le disque
        # pour tout centre de la boîte de t* : le pire est atteint à une extrémité (distance convexe en w0)
        far = max((c[1] + sy * h - w0) ** 2 + (F(1, 2) - c[0] - sx * h) ** 2 for sx in (-1, 1) for sy in (-1, 1)
                  for w0 in (F(P2['centres_couverts'][0]), F(P2['centres_couverts'][1])))
        check(f'{side} : boîte dans le disque de Rouché, pour tout centre couvert', far < R * R)
        boxes.append((side, crit, c, h))
for side in ('P3_moins', 'P3_plus'):
    bs = [b for b in boxes if b[0] == side]
    (_, _, c1, h1), (_, _, c2, h2) = bs
    check(f'{side} : deux boîtes disjointes', abs(c1[0] - c2[0]) > h1 + h2 or abs(c1[1] - c2[1]) > h1 + h2)
kinds = {side: {b[1] for b in boxes if b[0] == side} for side in ('P3_moins', 'P3_plus')}
check('P3 : un côté hors droite, l\'autre critique', kinds['P3_moins'] == {False} and kinds['P3_plus'] == {True})
kap = bounds(d['P1_pli_50']['kappa_box'])
check('P3 : côté critique = signe de kappa (lam > lam* et kappa > 0)', kap[0] > 0 and F(d['P3_plus']['lam']) > F(d['P1_pli_50']['centre'][0]))
w = d['P4_temoin']
check('P4 : témoin refusé (pas de pli certifié le long de n)', not w['accepted'] and not w['H_lam_separated'])

print(f"{sum(ok for _, ok in checks)}/{len(checks)} contrôles réussis")
sys.exit(0 if all(ok for _, ok in checks) else 1)
