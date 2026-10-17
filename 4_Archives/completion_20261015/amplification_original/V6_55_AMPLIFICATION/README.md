# V6.55 - Essai d'amplification arithmétique - 14 octobre 2026

Lire d'abord ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf.

Ce complément constitue la version V6.55, à la suite du dossier V6.54. Il ne remplace pas l'archive
globale et ne revendique pas de preuve de RH ni de nouveau demi-plan sans zéros.

Acquis écrits avec preuves : restitution exacte par paramètres carrés,
regroupement des corrélations selon q, borne explicite des petits conducteurs
q<=H à toutes les échelles. L'estimation de la queue q>H reste ouverte.

## Contenu

- PDF lisible et sources Markdown/LaTeX de la note ;
- calcul_famille.py : énergie de la famille, intégration affine exacte de
  coefficients flottants (NumPy requis) ;
- verifier_identites.py : vérification indépendante à 70 chiffres décimaux,
  regroupement par conducteur et contre-modèle universel (Python standard) ;
- results/ : calculs exécutés et avertissements de portée ;
- SHA256SUMS.txt : empreintes des fichiers de cette livraison.

## Reproduction

    python3 verifier_identites.py --output results --precision 70
    python3 calcul_famille.py --ceilings 100 300 1000

Les calculs numériques ne sont pas certifiés par intervalles et ne démontrent
aucune borne à l'infini. Les lemmes analytiques sont prouvés dans la note.

## Construire le PDF

Avec Pandoc et XeLaTeX installés :

    pandoc ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.md --from markdown+tex_math_single_backslash --standalone --pdf-engine=xelatex -o ESSAI_AMPLIFICATION_ARITHMETIQUE_V6_55.pdf

L'estimation encore recherchée est une majoration supérieure signée de la
queue q>X quand H=X, de taille X^3 à des logarithmes près. Si elle était prouvée,
elle donnerait un demi-plan sans zéros Re(s)>3/4. Cela ne donnerait pas encore RH.
