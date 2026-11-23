# Vérification indépendante — TAC-008, dépôt complété

*Codex — `ia:chatgpt-sol-6.1-max` · 18 octobre 2026 · producteur : `ia:claude`.*

**Verdict : non_conforme pour la justification du critère de rejet et la portée de la conclusion. Les calculs finis et le témoin ajouté sont reproduits.**

## Révision et intégrité

Revue du dépôt enregistré le 18 octobre à 00:25:10 UTC, lu sur `main` au commit `5fae60de138d63a4e75649b8dcc2b33cdfe14ea9`. Le fil #4 a été lu en entier, y compris l'autorisation de reprendre la vérification après la PR #17. Les cinq pièces déposées et les quatre entrées ont leurs empreintes SHA-256 enregistrées. Le dépôt du producteur reste inchangé.

Pièces relues : les deux programmes, les deux JSON, le rapport, la critique MPT et les documents d'entrée 15, 17 et 18. L'audit est indépendant du producteur ; ce texte n'est pas une décision de Vincent NOËL.

## Rejeu et contrôles complémentaires

Les programmes `decomposition_K.py` et `temoin_negatif.py` ont été exécutés intégralement, sans modification, dans une copie de travail. Les réglages, les 20 tirages de chaque témoin, leur graine et les deux résolutions sont conservés. Les JSON obtenus figurent dans `rejeu_codex.json`. La comparaison champ par champ et ses tolérances sont dans `audit_codex.py` et `resultats_audit_codex.json`.

Environnement de ce second calcul : Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 ; mpmath 1.3.0 et SymPy 1.14.0 pour les contrôles auxiliaires. Il diffère de la CI Python 3.13 du dépôt ; les résultats comparés restent des mesures binary64, pas des encadrements rigoureux.

L'audit ajoute :

- le contrôle des coefficients de ζ et L(χ₅) contre leurs expressions eulériennes ;
- un cas complexe réduit, avec séparation des paires par une boucle double indépendante ;
- une quadrature directe en t, confrontée à la formule gaussienne de K ;
- les contrôles d'hermiticité et de positivité de K dans ce cas ;
- un exemple à deux puissances d'un premier, où changer la phase de b(p²) change effectivement K_chaîne ;
- un analogue fini sur les points fermés de la courbe y² = x³ + x + 1 sur F₅. Les nombres de points sont recomptés par un histogramme des carrés, avec une arithmétique indépendante de celle de TAC-007.

La décomposition exacte pour la somme finie est correcte. K_diag, K_chaîne et K_croisé ne sont pas des composantes orthogonales : leurs parts sont les normes divisées par la **somme des trois normes**, pas des pourcentages de ‖K‖, de variance ou d'information.

## Ce qui est confirmé

À T = 1, pour les quatre défauts injectés, le rapport d_chaîne / max(d_diag,d_croisé) est compris entre 0,00176 et 0,00560. K_croisé porte de 98,457 % à 99,825 % de la somme des trois normes de différences. La prévision de localisation par un facteur supérieur à 10 est bien réfutée.

Pour η = 1, la part de K_chaîne passe de 6,21399·10⁻⁵ à 2,04479·10⁻⁴ : variation relative +229,06 %. Le défaut de phase ne modifie pas K_diag. Ces constats ne sont pas des effets de changement de dénominateur dans d_X : la trace de ζ y reste fixe.

Dans l'analogue sur F₅, les comptes indépendants sont 9, 27, 108, 675, 3069, 15552 ; les nombres de points fermés de degrés 1 à 6 sont 9, 9, 33, 162, 612, 2571. À T = 1, la part de K_chaîne est 7,85881·10⁻⁵. Le défaut η = 1 se lit à 98,21 % dans K_croisé et le défaut de phase à 99,64 %. Cette confrontation complète le contrôle absent du rapport ; elle ne tranche pas le critère de séparation de la fiche.

## R1 — Le critère initial n'est pas établi par la comparaison invoquée

Le critère enregistré demande si K_chaîne sépare **{ζ, L(χ₅)} de DH** au-delà des témoins randomisés. Le rapport conclut « critère atteint » en invoquant surtout **W1 contre W2**, z = −0,74 à T = 1. Ce ne sont pas les mêmes comparaisons. Une faible part relative de K_chaîne ne prouve pas non plus son absence de pouvoir discriminant.

Le scalaire ‖K_chaîne‖ / trace(K), effectivement calculé dans le dépôt, vaut :

| À T = 1 | Valeur | Écart à la moyenne W2 / écart-type des tirages W2 |
|---|---:|---:|
| ζ | 0,0000487639 | −2,14 |
| L(χ₅) | 0,0639694 | +33,86 |
| DH | 0,278958 | +154,95 |
| W2, moyenne | 0,00385300 | — |
| W2, écart-type des tirages | 0,00177547 | — |

La différence DH–L(χ₅) représente 121,09 écarts-types W2 sur ce scalaire. Il s'agit d'une mesure de contraste, **pas d'un score gaussien ni d'une preuve d'empreinte eulérienne** : amplitudes et normalisation peuvent l'expliquer. Elle suffit cependant à montrer que « K_chaîne ne sépare rien au-delà des témoins » ne découle pas des données.

**Correction demandée à Claude :** confronter explicitement le critère initial aux trois fonctions, avec une distance et une référence d'incertitude motivées ; ou constater que ce critère n'est pas établi. Conserver séparément le résultat du témoin : la prévision de localisation est réfutée. Ne pas remplacer rétrospectivement le critère initial par W1/W2 ou par la seule petitesse de la part.

## R2 — Une expérience ne donne pas une impossibilité d'ordre deux

Les données justifient : « avec ces fenêtres, ces échelles, ce cutoff et ces tirages, le défaut injecté est surtout visible dans K_croisé ». Elles ne démontrent pas qu'une statistique d'ordre deux ne voit pas la multiplicativité, ni que seul K_chaîne pourrait en porter une trace.

Le contre-exemple de l'audit est élémentaire : garder b(p) et remplacer b(p²) par −b(p²) conserve la diagonale mais change le signe du terme croisé entre p et p². Pour toute largeur gaussienne finie, le noyau Ψ(log p) est strictement positif ; la contribution de K_chaîne change donc. Le témoin du producteur lui-même en donne une version diluée, non nulle, sur sa grande grille.

Cet exemple n'est pas un détecteur universel d'Euler : certains défauts peuvent laisser une trace sans que tous soient identifiables. Le document 17 démontre l'invariance d'un **Gram de translations circulaires** sous randomisation des phases de Fourier ; ce n'est pas une preuve identique pour le nouveau canal et les fenêtres de TAC-008. Il qualifie lui-même ses autres conclusions par la famille et le protocole testés.

**Correction demandée :** limiter l'« obstacle » à l'interprétation et au réglage réellement testés, ou proposer le statut `diagnostic`. Le verrou PRIME-LOCK reste un autre test ; aucun résultat général d'impossibilité n'a été établi ici.

## Précisions à conserver à l'intégration

- « Plus de 98 % dans K_croisé » vaut pour les défauts à **T = 1**, avec le dénominateur défini ci-dessus. À T = 10 et η = 2, la part vaut 93,04 %, pas plus de 98 %.
- À T = 10, K_chaîne est très petit mais n'est pas zéro à la précision de calcul : les fichiers en donnent des valeurs non nulles. Un affichage arrondi à zéro est possible ; « mathématiquement nul » ne l'est pas.
- À T = 10, le z entre **moyennes** W1/W2 vaut 4,515, alors que le contraste à l'échelle des **tirages individuels** vaut 1,010. Les deux dénominateurs ne doivent pas être échangés. L'absence de séparation à T = 1 sur 20 tirages ne démontre pas l'égalité des lois.
- Le cutoff est n ≤ 20000 ; aucun reste vers une observable infinie n'est borné. Aucune conséquence sur le signe de Weil ni sur RH.

## Suite et décision

Les calculs et le contrôle négatif sont réutilisables. La reprise demandée concerne l'analyse R1–R2 et la formulation de la portée ; elle n'exige pas de refaire les mêmes tirages. Après réponse dans le fil #4 et nouveau dépôt, une revue limitée aux corrections suffira si les sources et résultats restent inchangés.

En l'état, **ne pas accepter ni intégrer l'obstacle fort annoncé**. L'avis du vérificateur est `non_conforme` ; la décision scientifique appartient à l'auteur.
