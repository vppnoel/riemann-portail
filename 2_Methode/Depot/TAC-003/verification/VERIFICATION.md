# Vérification indépendante — TAC-003

*Vérificateur : ia:claude · 18 octobre 2026 · fil de discussion #8. Verdict : **non conforme**. Le lemme dual est juste. Mais il est déjà énoncé et démontré au document 76 ; la donnée quantitative du document d'entrée 79 n'est pas utilisée ; aucune borne ni obstruction n'est donnée avec ses constantes.*

## Pièces examinées

- La fiche (question, sortie attendue, critère de rejet, témoin), le registre et le journal des tâches.
- `RAPPORT.md`, seule pièce du dépôt : empreinte `6080ee68…`, inchangée depuis le dépôt.
- Le document d'entrée 79 (`79_SIGNAL_COUPLAGES_ET_RESOLUTION.md`, empreinte inchangée), § 3 : complément de Schur et dette relative ρ.
- Le document 76 : § 2.2 et lemme C, que la sortie attendue de la fiche cite comme « complément 76 ».
- Le fil #8.

## Ce qui a été rejoué

Le dépôt ne contient aucun programme. J'ai rejoué son algèbre dans `rejeu.py`, avec la graine 20261018 ; les résultats sont dans `rejeu.json`.

| Contrôle | Résultat |
|---|---|
| R1. Borne duale H − BC⁻¹B* ⪰ H − μ⁻¹G*, avec G* = BR⁻¹B* et μ = λ_min(R^{−1/2}CR^{−1/2}) ; 2 000 formes aléatoires complexes, tête 1 à 4, queue 1 à 6 | aucune violation ; plus petite valeur de la différence −2·10⁻¹², c'est-à-dire l'arrondi |
| R2. Optimalité de μ⁻¹ en dimension un (H = 2, a = 1,3, μ = 0,7) | infimum numérique −0,4142857130, contre H − a²/μ = −0,4142857143 |
| R3. Garde de restriction : ℝ², R = I, Y = vect(e₁), c(x) = x₁ + 5x₂ | norme ambiante √26, norme restreinte 1 : la borne ambiante surestime la dette d'un facteur 26 |
| R4. Donnée du document 79 : ρ ≈ 0,999999832 à S = 3, partition 4 + 4 | marge relative 1 − ρ ≈ 1,7·10⁻⁷ |

**L'algèbre est juste.** La borne, l'optimalité du coefficient et la garde de restriction sont correctes.

## Écarts

1. **Aucun apport par rapport au document 76.** Ce qui est déjà au document 76 :
   - la définition des fonctionnelles c_i ∈ Y*, des représentants de Riesz z_i et de G*_ij = R(z_i, z_j) ;
   - la minoration G_eff ⪰ H − μ⁻¹G*, sa preuve par complétion du carré, et la garde « Il faut certifier la restriction à Y, son quotient dual, ou une extension adaptée » (§ 2.2) ;
   - la même chose sous forme de lemme, avec la convergence des représentants (lemme C).

   Le rapport le reformule sans le citer. Le seul ajout est l'optimalité de μ⁻¹ en dimension un, immédiate (R2).
2. **Le document d'entrée n'est pas exploité.** Le document 79 donne exactement les données qui décideraient la question :
   - ρ ≈ 0,999999832 pour une partition 4 + 4 à S = 3 ;
   - une dette inférieure à 0,18 % de la marge de tête pour le bloc pair du document 73.

   Une borne duale majore la dette exacte : μ⁻¹BR⁻¹B* ⪰ BC⁻¹B*. Avec la partition du document 79, elle ne garde le signe que si elle la majore de moins d'environ 1,7·10⁻⁷ en relatif (R4). Avec celle du document 73, elle dispose d'une marge d'environ 550 fois la dette. La sortie attendue demandait précisément ce type de résultat : « borne candidate ou obstruction avec domaine et constantes ». Le rapport ne donne ni domaine ni constante.
3. **Le critère de rejet est mal appliqué.** « Atteint pour les formulations qui ne certifient pas la restriction » : c'est la garde du document 76, pas un test de la proposition du producteur, qui n'en fait aucune. Le témoin de la fiche, « matrices positives en tête avec complément ou résidu non contrôlé », n'est pas construit.
4. **Contrôles anti-circularité.**
   - **Davenport–Heilbronn :** non traité. Le lemme est purement hilbertien : il vaut mot pour mot pour DH. Il faudrait le dire, avec la conséquence : aucune information sur RH sans données arithmétiques.
   - **Corps de fonctions :** non traité.
   - **Témoin négatif :** absent.
   - **Constantes :** aucune n'est donnée.
5. **Formules altérées**, comme le signale le producteur.
   - « ight » vient de `\right`, « qquad » de `\qquad`, « mathbb R » de `\mathbb R`.
   - `\|c_i\|_{Y^*}` est devenu « |c_i|_Y|_{Y^*} », ce qui est ambigu : on peut y lire une restriction ou une norme.
6. **Procédure**, pour mémoire. Cela ne fonde pas le verdict, car les règles de `GITHUB.md` § 4 ont été fusionnées après ce dépôt : prévision commitée à 22 h 58 min 43 s UTC, rapport à 23 h 01 min 16 s, écrit sur `main`, et dépôt enregistré par un workflow temporaire. Le producteur le signale lui-même.

## Statut proposé

« Diagnostic » serait juste pour le document 76, pas pour ce dépôt, qui n'ajoute pas d'information. Le statut juste est **ouvert** : la question « peut-on payer la dette par une norme duale spécifique ? » n'a pas reçu de réponse sur un cas du corpus. Aucun énoncé équivalent à RH n'est en jeu.

## Pour un dépôt conforme

- Prendre les matrices du document 79 (partition 4 + 4, S = 3) et celles du document 73.
- Choisir une norme R explicite, par exemple la norme d'énergie du document 76.
- Calculer μ, G* et la dette relative de la borne duale, puis la comparer à la dette exacte ρ.
- Prévoir avant le calcul où la borne duale garde le signe et où elle le perd.
- Ajouter :
  - un témoin négatif, comme une queue dont la coercivité μ est surestimée volontairement, que la chaîne doit signaler ;
  - la remarque DH ;
  - un mot sur l'analogue des corps de fonctions, où la queue est de dimension finie.
- Réparer les formules et citer le document 76.

*La relecture n'est pas à l'aveugle : le fil #8 nomme le producteur. La décision revient à l'auteur.*
