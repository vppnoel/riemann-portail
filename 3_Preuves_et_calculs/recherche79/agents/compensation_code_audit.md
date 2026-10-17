# Audit ciblé des programmes de compensation

Périmètre : `work/compensation_blocks.py`, `work/certify_block_guards.py` et `work/results/block_guard_certificate.json`, plafond 1000. Relecture mathématique et replay indépendant à 140 chiffres. Aucun programme racine modifié par l'auditeur.

## Vérifications positives

- Les deux cribles indépendants concordent sur les 193 puissances de premiers ≤1000, sans doublon, avec poids log(p)/sqrt(p^k).
- La subdivision utilise la comparaison entière exacte q^P≤lo^(P−j)hi^j. Une vérification séparée confirme que chaque partition couvre exactement une fois les 192 sources après q=2. Le premier préfixe q=2 est certifié séparément. Les sous-blocs vides n'ajoutent aucun préfixe.
- La garde à trois points est une minoration de tous les défauts internes : support ⇒ moment du préfixe ≥max(ad,M−b(D−d)), puis concavité sur chacune des deux branches. Un échec de la garde ne réfute pas le vrai signe.
- L'inversion du dual est valide. β=A'' est strictement positive sur [log2,+∞). Les signes intervalles stricts de A'(borne)−C encadrent donc le maximiseur pour toutes les valeurs exactes contenues dans C. L'évaluation intervalle Cθ−A(θ) englobe G(C). Les dépendances entre occurrences ne font qu'élargir les intervalles.
- La queue archimédienne après 64 termes est correctement majorée géométriquement, avec premier exposant 257/2. La constante totale π²/4+2Catalan est la somme exacte des inverses carrés. Le témoin de queue à T est exporté et contient le recalcul indépendant.
- Toutes les 62 gardes sauvegardées (9 grossières et 53 raffinées), ainsi que le défaut q=2, contiennent les valeurs d'un replay indépendant à 140 chiffres. Les minima réels de tous les préfixes vérifiés sont supérieurs aux gardes correspondantes.
- Les informations de portée sont correctes : les défauts concernent les sources tronquées ; le signal original coïncide avec ce signal sur [log2,log1000]. Aucun certificat de toutes les fonctions tests de Weil, aucune preuve globale, aucune preuve de RH n'est déclaré.

## Deux corrections signalées, appliquées et vérifiées

1. La docstring disait que les bornes de racines et la queue étaient conservées dans JSON. Elles étaient vérifiées au recalcul mais non exportées explicitement. Le responsable a maintenant exporté les 117 témoins de dual : 116 racines intérieures avec résidus de signes stricts et un cas au bord T. Tous ces signes ont été vérifiés indépendamment ; les positions numériques aux deux extrémités de chaque intervalle de masse sont contenues dans les témoins. Le témoin de queue est aussi exporté.
2. La conversion initiale de la borne rationnelle inférieure de γ par `w.mpq` arrondissait cette borne vers l'intérieur de 1.7494×10^−142. La vraie valeur γ restait à environ 3.44×10^−21 au-dessus, mais la construction ne conservait pas exactement le témoin Euler annoncé. Le responsable a converti la borne rationnelle par `I`, puis utilisé son extrémité inférieure binaire dirigée. La comparaison exacte confirme que la borne binaire sauvegardée ne dépasse plus la borne rationnelle. Ce correctif n'affecte aucun signe observé ; il rétablit la justification formelle d'arrondi.

État final : **PASS**. Les contrôles du certificat corrigé sont consignés dans `compensation_code_audit_checks.json`.

## Relecture du document 79

Les preuves des lemmes 1 à 3 et de la proposition 4 sont cohérentes. Le crédit total fini découle des bornes de Chebyshev, de la croissance de β et de la série convergente ∑(log n)²/n^(3/2), sans RH. La proposition 4 vise uniquement le certificat agrégé à rapport fixé ; elle ne démontre aucune négativité du vrai signal. Le contre-modèle à l'inversion Selberg est exact et son réservoir exponentiel est bien celui annoncé, tandis que sa demande reste artificielle. Les sommes du diagnostic, la réserve radiale du document 78 et la loi de signe globale sont distinguées.

Une précision rédactionnelle a été signalée : pour l'optimalité, dire que la mesure extrémale atteint le minorant au coude suffit ; l'expression « à toutes les masses » supposerait de permettre des préfixes fractionnant les atomes. Cette nuance n'affecte ni la garde ni son certificat. La citation assurant le signe sur [0,T] et les autres références publiées sont vérifiées par le responsable ; le présent audit porte sur les démonstrations auxiliaires et le calcul fini.

## Limite

Le contrôle indépendant des valeurs numériques ne remplace pas la justification de la bibliothèque d'arithmétique intervalle. Le certificat est validé dans le modèle mpmath.iv 400 bits déclaré ; il ne fournit aucune borne au-delà du plafond fini. Le passage au global exige toujours une estimation arithmétique indépendante de la distribution intérieure.
