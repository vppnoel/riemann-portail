#!/usr/bin/env python3
"""TAC-007, P2 : l'architecture du certificat du document 75 (S = 11/20) peut-elle atteindre une marge de 10⁻¹² ?

Lit les budgets d'erreur réellement certifiés à 11/20 (4_Archives/recus/V650/constructive/resultats_certificat_integral.json)
et calcule, pour chacun, le facteur de réduction qu'exigerait une marge de 5·10⁻¹², ainsi que le coût induit
selon la loi d'échelle de chaque budget (lecture du code tentative_certificat_integral.py, lignes 184–203).
python -B 2_Methode/Depot/TAC-007/p2_budgets_architecture_doc75.py  →  p2_resultats.json
Auteur et titulaire des droits : Vincent NOËL. Producteur : ia:claude.
"""
from pathlib import Path
import json
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[2]
j = json.loads((ROOT / '4_Archives/recus/V650/constructive/resultats_certificat_integral.json').read_text())
cible = 5e-12
budgets = {
    'table (poids digamma, table linéaire par morceaux)': (j['table_error_float'], "∝ rayon de table + 35·H²/8 : pas H divisé par √facteur"),
    'quadrature en fréquence (trapèzes)': (j['weighted_quadrature_error_float'], "∝ T·h² : pas h divisé par √facteur, donc cellules ×√facteur"),
    "assemblage binary64 (modèle γ_n)": (j['assembly_error_float'], "∝ nf·2⁻⁵³ : inatteignable en binary64 dès que nf croît"),
    'poids intégrés': (j['integrated_weight_error_float'], "∝ nf·erreur locale de poids"),
    'spatial (troncature N)': (j['spatial_error_float'], "négligeable"),
}
out = dict(source='resultats_certificat_integral.json (V6.50, S = 11/20)', marge_certifiee_11_20=j['mass_floor_lower_float'],
           cellules_frequence=j['frequency_cells'], marge_visee=cible, budgets={})
for k, (v, loi) in budgets.items():
    f = v / cible
    out['budgets'][k] = dict(valeur=v, facteur_de_reduction=f, loi=loi)
fq = out['budgets']['quadrature en fréquence (trapèzes)']['facteur_de_reduction']
out['cellules_necessaires_quadrature_seule'] = j['frequency_cells'] * fq ** 0.5
out['budget_assemblage_binary64_avec_ces_cellules'] = j['assembly_error_float'] * fq ** 0.5
out['conclusion'] = ("Même en ignorant les autres budgets, la quadrature en trapèzes exige environ "
                     f"{out['cellules_necessaires_quadrature_seule']:.2e} cellules ; le budget d'assemblage binary64 monte alors à "
                     f"{out['budget_assemblage_binary64_avec_ces_cellules']:.1e}, très au-dessus de la marge. L'architecture du document 75 "
                     "(fréquence, trapèzes, table linéaire, binary64) ne peut pas certifier une marge de l'ordre de 10⁻¹².")
(HERE / 'p2_resultats.json').write_text(json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print(json.dumps(out, indent=1, ensure_ascii=False))
