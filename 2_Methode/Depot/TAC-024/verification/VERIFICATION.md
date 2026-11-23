# TAC-024 — Vérification du théorème A′ par fenêtres

Vérificateur : ia:chatgpt-sol-6.1-max. 23 novembre 2026. Verdict : **conforme** pour le théorème et ses corollaires. La nouveauté de l'énoncé exact reste à établir.

## Pièces et vérifications

Les trois entrées et les quatre pièces correspondent aux empreintes enregistrées. Lecture de la preuve, du rapport, des objections à TAC-022 et du témoin à pôles simples (TAC-017). Rejeu du script déposé par `python -I tac018_numerique.py` jusqu'à 10⁶. La sortie est identique octet pour octet. Le plus grand rapport examiné est 0,09383 en y = 10. La reproduction porte sur la grille testée et ne renseigne pas sur l'existence de fenêtres arbitrairement tardives.

## Sens direct et réciproque

- Le coefficient de (s−ρ)⁻² dans G_c est m(m+1) pour un zéro de multiplicité m. Pour un pôle réel β entre θ et 1, le facteur β(β−1) rend négatif le coefficient correspondant de Φ_c. Le plancher exclut ce cas ; le sens utilisant un plafond emploie en plus l'absence de zéro réel de ζ sur (0,1). Le témoin fictif à pôle réel distingue les deux conclusions.
- La formule de Perron s'applique à la rampe non centrée avec le noyau 1/[s(s−1)]. L'intégrale est absolument convergente sur Re s = 2. Le résidu en 1 est exactement G_c(1)y, ce qui justifie le centrage après le déplacement du contour.
- Sous l'hypothèse qu'aucun zéro n'est à droite de θ, la droite Re s = θ+a reste à distance horizontale au moins a des zéros. Le comptage local et la formule locale de ζ′/ζ sont ceux de [Bingham, leçon 27](https://www.ma.ic.ac.uk/~bin06/M34PM16-Analytic-Number-Theory/2013/m3pm16l27%2813%29.pdf). Sur chaque bloc, le reste holomorphe et sa dérivée sont O(log j). L'intégration de 1/[a²+(t−γ)²] puis Cauchy–Schwarz donnent O(log²j/a). Après multiplication par le noyau, la somme converge. Les segments horizontaux tendent vers zéro pour a fixé. Aux basses hauteurs, le compact est sans zéro et le dénominateur coûte O(1/(1−θ)). Le choix a = 1/log y donne bien H(y) = O_θ(y^θ log y).
- L'infimum du corollaire 1 est pris dans [0,1] avec inf ∅ = 1. Au seuil θ=1/2, le corollaire 2 fournit une équivalence avec RH. Aucune étape ne démontre que H vérifie effectivement cette borne. La preuve utilise des faits propres à ζ ; son transfert à un autre objet arithmétique demanderait sa propre analyse des pôles et des zéros.

## Précisions à joindre à une diffusion

À l'étape 1(a), |c(n)| ≪ log² n donne directement |H(y)| ≪ y log³(2y) ≪ y², qui suffit au reste de la preuve. Employer cette ligne évite à la fois une puissance de logarithme injustifiée par la majoration citée et le problème de log 1 = 0.

Le rapport signale l'équivalence à RH, tandis que le champ `equivalent_rh` du dépôt vaut `false`. Le théorème d'équivalence est établi inconditionnellement ; la borne elle-même est équivalente à RH. Maintenir cette distinction dans toute notice publique. Le contrôle numérique et les arguments classiques de la réciproque ne justifient aucune priorité bibliographique. Une relecture spécialisée et une comparaison avec les résultats d'oscillation et les critères par sommes lissées restent pertinentes avant de revendiquer un résultat original.
