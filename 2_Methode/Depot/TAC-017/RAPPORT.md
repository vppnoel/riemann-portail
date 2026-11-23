﻿# TAC-017 — Échelle, niveau 3 : une preuve humaine du Landau localisé pour ζ, confrontée au Lean

*Producteur : ia:claude · 23 novembre 2026 · branche `tac-017`. Auteur et titulaire des droits : Vincent NOËL. Fil : [#40](https://github.com/vppnoel/Riemann/issues/40). Code Lean consulté : `leanprover-community/riemann-hypothesis`, commit `51d9b1a` (23 novembre 2026).*

**En une phrase.** L'étape « Landau localisé » de la preuve annoncée se démontre en trois pages d'analyse classique, que le code Lean suit pas à pas (`PREUVE.md`). Elle n'utilise ni produit d'Euler, ni positivité des coefficients : la seule positivité est celle des résidus aux pôles réels, qui vient de la multiplicité des zéros. Le chiffre du guide (0,023 √y jusqu'à 10⁷) est confirmé, avec une marge de 1,4 %. *Reprise du 23 novembre 2026 : trois défauts relevés par la vérification (#40) sont corrigés, voir la section « Reprise ».*

## Prévision

Enregistrée le 23 novembre 2026 à 1 h 18 UTC (commit `f55adc2` sur `main`), avant d'ouvrir le code Lean et avant tout calcul. Texte intégral dans `taches.json`. En résumé :
- **P1** : la preuve se fait avec Mellin, la formule explicite, Laplace et ses dérivées, et Landau unilatéral. Ingrédients supplémentaires attendus : des bornes classiques (N(T), croissance de ζ′/ζ). Aucun outil automorphe. 4 à 8 pages.
- **P2** : l'énoncé Lean a la forme du guide, avec des paramètres plus particuliers (δ = ½ fixé, ou θ dans ]½, 1[).
- **P3** : le maximum de |G − log 2π|/√y sur [10, 10⁷] est entre 0,010 et 0,023, atteint pour y < 10³.
- **P4** : la Proposition donne la moitié « minoration » d'un énoncé du type du théorème A, pas la moitié « majoration », et ne contient pas le théorème A, qui porte sur Q.
- **P5** : pour Davenport–Heilbronn, l'argument échoue à l'étape « un seul côté suffit », faute de coefficients positifs.

## Méthode

1. **Lecture du code Lean.** Les 32 fichiers de `DedekindLFunctions/LandauTheorems/`, plus `CharFamily.lean` et `LandauZeroFreeCriterion.lean`, au commit `51d9b1a`, obtenus par un clonage partiel du dépôt public. J'ai lu les énoncés de chaque lemme de la chaîne, la preuve complète de [`landau_window`] et de [`landau_window_key`], et le début des preuves de [`poleData_char`] et [`poleData`]. Les autres preuves n'ont pas été lues ligne à ligne : la correspondance de `PREUVE.md` repose sur leurs énoncés.
2. **Preuve humaine** (`PREUVE.md`) : cinq étapes, avec pour chacune les déclarations Lean correspondantes, et un tableau de confrontation à l'énoncé du guide.
3. **Calcul** (`tac017_numerique.py`, environ 18 s, sans dépendance ; **version corrigée lors de la reprise**). On maximise |H(y)|/√y avec H = G − log 2π. Sur chaque intervalle [n, n + 1), H(y) = y·Sₙ − ψ(n) − y log y + (1 + γ)y − log 2π. Les points critiques de H/√y vérifient 2yH′ − H = 0, soit D(y) = y(Sₙ + γ − 1 − log y) + ψ(n) + log 2π = 0. D est concave : on la coupe en exp(Sₙ + γ − 2), puis on cherche ses zéros par bissection. Les deux bords exacts de chaque intervalle sont aussi évalués. Sommes compensées (Kahan). Sortie : `resultat_numerique.txt`. *La première version cherchait les zéros de G′ au lieu de ceux de D, ce qui ne garantissait pas le maximum ; la valeur trouvée était néanmoins la bonne, comme l'ont confirmé la vérification (C++, `long double`) et la nouvelle version.*

## Résultat

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| **P1** | outils classiques, avec N(T) et la croissance de ζ′/ζ ; rien d'automorphe ; 4 à 8 pages | rien d'automorphe ; environ 3 pages ; **ni N(T), ni croissance de ζ′/ζ** : seulement \|G(y)\| ≪ y², l'isolement des zéros et les inégalités de Cauchy | **juste sur l'essentiel, fausse sur les ingrédients** : la preuve est plus économe que prévu |
| **P2** | forme du guide, paramètres particuliers | forme contraposée, **équivalente**, avec **les mêmes** paramètres que le guide (0 < θ < 1, δ > 0, C quelconque) ; aucun paramètre n'est plus particulier | **juste sur le fond, fausse sur le détail** (corrigé à la reprise : la première version disait à tort « Lean est plus général que le guide ») |
| **P3** | max entre 0,010 et 0,023, pour y < 10³ | **0,022681**, atteint en y ≈ 319 439 ; maximum par décade entre 0,017 et 0,023 | **juste pour la valeur, fausse pour le lieu** |
| **P4** | minoration seulement, et ne contient pas le théorème A | voir Portée, point 3 | **juste** |
| **P5** | DH échoue à « un seul côté suffit » | cette étape n'utilise aucune positivité des coefficients | **fausse** (voir Portée, point 2) |

**Le chiffre du guide.** Le guide annonce |G(y) − log 2π| < 0,023 √y pour 10 ≤ y ≤ 10⁷. Le maximum exact est 0,022681 : la borne est vraie, avec une marge de 1,4 %. Sous RH, la borne théorique est κ ≈ 0,0462, soit environ deux fois plus.

## Portée

1. **Une marche de l'échelle rendue lisible.** Ce module de la preuve tient en trois pages d'analyse classique, et chaque étape correspond à un lemme Lean nommé. C'est la contribution visée par la fiche : un morceau de la preuve vérifiée par machine, réécrit pour un lecteur humain, avec la machine comme arbitre.
2. **Où est la positivité.** Je prévoyais (P5) que l'étape « un seul côté suffit » utiliserait Λ ≥ 0, comme le théorème de Landau classique et le tableau du document 47. **Ce n'est pas le cas.** L'astuce |g| = 2g⁺ − g n'utilise que le fait que g soit réelle. La seule positivité de l'étape est celle des **résidus aux pôles réels**, −m/(ρ(ρ − 1)) > 0, qui vient de la multiplicité m ≥ 1 des zéros, plus les poids positifs de la famille. Le Lean le confirme : [`landau_window`] ne prend qu'une structure abstraite `PoleData`.

   Conséquences :
   - **ce qui est positif, ce sont les multiplicités des zéros, pas les coefficients** ;
   - le produit d'Euler n'intervient pas à cette étape : il sert ailleurs, pour obtenir la borne (⋆) ;
   - le Sosie (DH) ne devrait donc **pas** échouer ici, mais à l'étape des entiers. C'est ce que disait le bloc 7 du document de travail. Je n'ai pas vérifié que DH satisfait les hypothèses `PoleData` (croissance, représentation de Laplace pour Re s > 2) : c'est le travail de TAC-016.
3. **Le lien avec le théorème A** (article 1). Le théorème A dit que ½ limsup log(1 + Q(X))/log X = Θ − ½, c'est-à-dire que la croissance du Thermomètre Q lit Θ exactement.
   - La Proposition donne, pour la statistique G, une **minoration locale et unilatérale** : si Θ > θ, G dépasse C y^θ dans chaque fenêtre tardive.
   - Le théorème A est **global et bilatéral** : il porte sur une moyenne quadratique, Q, construite sur des pôles doubles, et donne aussi la majoration. La Proposition ne le contient pas, et il ne contient pas la Proposition.
   - **Ce qu'ils ont en commun** : une singularité à droite de θ se voit dans la croissance. Une version « par fenêtres » du théorème A, avec un Q qui dépasse X^(2θ−1) dans chaque fenêtre tardive, serait l'analogue direct. Elle n'est **pas démontrée ici** ; c'est une piste.
4. **Anti-circularité.** La preuve n'utilise pas RH. Le calcul de P3 mesure G, il ne suppose rien.

## Reprise

Le 23 novembre 2026, la vérification de `ia:chatgpt-sol-6.1-max` ([`verification/VERIFICATION.md`](verification/VERIFICATION.md), fil [#40](https://github.com/vppnoel/Riemann/issues/40)) a jugé le dépôt **non conforme**. Elle a relevé trois défauts, qui sont tous fondés et tous corrigés ici.

1. **L'étape 5 contenait une implication géométrique fausse.** J'avais écrit que ρ₀ appartient au disque B(σ, σ − θ), alors que seule sa distance **horizontale** à σ est < σ − θ. L'étape est réécrite avec la dichotomie exacte du Lean [`landau_dichotomy`] : soit le disque fermé est vide de pôles, soit on prend la distance minimale et l'on distingue un pôle réel isolé d'un pôle de distance horizontale plus petite. Le passage par le centre déplacé [`landau_nearest`] est maintenant détaillé, avec le choix des rayons d′ < r′ < r ≤ D et de η < log((σ − θ)/d′).
2. **La comparaison guide/Lean était fausse sur θ.** Le guide énonce lui aussi 0 < θ < 1 ; le Lean n'est donc pas plus général. Le tableau de `PREUVE.md`, le verdict P2 et le critère de rejet sont corrigés.
3. **Le script cherchait les extrema de la mauvaise fonction.** Il est réécrit (méthode ci-dessus). Le résultat, 0,022681 en y ≈ 319 439, est inchangé et confirmé indépendamment.

S'y ajoutent, comme demandé, des **liens directs vers chaque déclaration Lean** citée (40 liens, au commit `51d9b1a`). Ces corrections ne changent pas la prévision, qui reste celle de l'enregistrement d'origine (commit `f55adc2`).

## Critère de rejet

Le critère de la fiche portait sur quatre points :
- une hypothèse de la preuve humaine absente de l'énoncé Lean : **aucune** ;
- un énoncé Lean différent du guide sur le fond : **non**, ils sont contraposés, avec les mêmes paramètres ;
- un rapport ≥ 0,023 √y sur [10, 10⁷] : **non**, le maximum est 0,022681 ;
- une preuve qui recopierait le guide : non, elle détaille cinq étapes que le guide résume en trois idées.

**Le critère n'est pas atteint.** Le vérificateur peut réfuter ce rapport par :
- une étape de `PREUVE.md` qui ne correspond pas au lemme Lean cité ;
- une erreur dans le calcul exact du supremum ;
- un usage du produit d'Euler ou de Λ ≥ 0 que j'aurais manqué dans la chaîne de [`landau_window`].

## Statut proposé

**demontre**, pour la Proposition dans le cas de ζ, au sens d'une preuve humaine complète d'un énoncé déjà vérifié en Lean. Ce n'est pas un résultat nouveau : c'est une exposition. Le chiffre du guide est **mesuré**.

Je demande la vérification à `ia:chatgpt-sol-6.1-max`, qui n'a pas produit ce dépôt. Points à regarder en priorité :
1. l'étape 3 (« un seul côté suffit ») et l'affirmation qu'elle n'utilise pas Λ ≥ 0 ;
2. le cas 2 de l'étape 5, choix de γ et inégalités de Cauchy ;
3. la formule de Φ, comparée à [`mellin_Gchi_modOne`].
