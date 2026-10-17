# Amplification arithmétique — dossier intégré au GLOBAL V6.55

Ce dossier fait partie du **corpus GLOBAL V6.55 complet**, construit sur la base
intégrale V6.54. Il contient les programmes et les diagnostics de l'essai du
14 octobre 2026. La note scientifique et ses preuves validées sont conservées
sans modification dans `../../1_Presentation/`.

## Lecture

- [Note HTML autonome, formules MathML](../../1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.html)
- [PDF de la note](../../1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf)
- [Source Markdown](../../1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.md)
- [Source LaTeX](../../1_Presentation/ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.tex)
- [Portail du corpus](../../00_PORTAIL.html)
- [Statut scientifique détaillé](STATUT_RECHERCHE.json)

## Acquis et limite

Les preuves auxiliaires portent sur la restitution exacte par paramètres
carrés, la stabilité des dilatations, le regroupement des corrélations selon
le conducteur q et la borne explicite des petits conducteurs q <= H, à toutes
les échelles. La borne supérieure signée de la queue q > H reste ouverte.
**Aucun gain global d'exposant sur l'énergie totale n'a été obtenu. RH et la
positivité globale de Weil restent ouvertes dans cette construction.**

L'implication conditionnelle est conservée : une majoration supérieure signée
de la queue q > X, lorsque H = X, de taille X^3 à des logarithmes près,
donnerait une borne de l'énergie en X^(5/2), à des logarithmes près, puis
l'absence de zéros pour Re(s) > 3/4. L'estimation manquante n'est pas démontrée.

## Contenu et provenance

- `calcul_famille.py` : énergie de la famille, intégration affine exacte des
  coefficients flottants (NumPy requis).
- `verifier_identites.py` : vérification indépendante à 70 chiffres décimaux,
  regroupement par conducteur et contre-modèle universel (Python standard).
- `results/` : résultats exécutés et avertissements de portée, copiés à
  l'identique de la livraison de l'essai V6.55.
- `generer_html.py` : reconstruction hors ligne de l'HTML de la note avec
  Pandoc et MathML natif, sans bibliothèque distante.
- `SHA256SUMS_INTEGRATION.txt` : empreintes des fichiers de ce dossier et de
  la note intégrée.

Les programmes et les résultats scientifiques sont copiés **octet pour octet**
de la livraison validée de l'essai. Les éventuelles mentions de « complément »
dans les diagnostics historiques décrivent cette livraison d'origine ; le
présent dossier est désormais intégré au corpus global complet.

## Reproduction

Depuis le présent dossier, avec Python 3 :

```sh
python3 verifier_identites.py --output results --precision 70
python3 calcul_famille.py --ceilings 100 300 1000
python3 generer_html.py
```

Les calculs numériques ne sont pas certifiés par intervalles et ne démontrent
aucune borne à l'infini. Les lemmes analytiques sont prouvés dans la note.

Pour reconstruire le PDF, depuis `../../1_Presentation/`, avec Pandoc et
XeLaTeX installés :

```sh
pandoc ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.md --from markdown+tex_math_single_backslash --standalone --pdf-engine=xelatex -o ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf
```

L'intégration au GLOBAL V6.55 complète le dossier documentaire ; elle
n'ajoute aucune preuve de la borne globale et ne revendique aucune priorité
historique.
