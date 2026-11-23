# TAC-024 — Théorème A par fenêtres (v3) : pôles doubles, réciproque refaite

*Producteur : ia:claude · 23 novembre 2026 · branche `tac-024`. Auteur et titulaire des droits : Vincent NOËL. Reprise de TAC-022, périmée et jugée non conforme ([#54](https://github.com/vppnoel/Riemann/issues/54)).*

**En une phrase.** Pour la statistique de l'article 1, H(y) = Σ_{n≤y} c(n)(y/n − 1) − G_c(1)·y, la caractérisation de Θ est maintenant démontrée dans les deux sens, au seuil :
- un **plancher** H ≥ −C y^θ sur des fenêtres tardives exclut les zéros à droite de θ ;
- réciproquement, sans zéro à droite de θ, |H(y)| = O_θ(y^θ log y) **pour tous les y grands**.

En particulier, RH équivaut à H(y) = O(√y log y). La réciproque de TAC-022, qui était fausse, est refaite par la méthode des blocs que proposait le vérificateur. Elle n'utilise que des faits classiques. La méthode n'est pas nouvelle.

## Prévision

Enregistrée le 23 novembre 2026 vers 3 h 20 UTC (commit `c3815f7` sur `main`), après lecture de la vérification de TAC-022 et avant toute rédaction. Je suis l'auteur de TAC-022 : la prévision n'est donc pas aveugle sur le sens direct, et je l'ai dit dans son texte. En résumé :
- **P1** : le sens direct passe sans changement de fond.
- **P2** : la forme affaiblie O(y^(θ+ε)) se démontre avec des bornes classiques de ζ′/ζ.
- **P3** : la forme au seuil O(y^θ log y) s'obtient par les blocs, avec pour seul comptage N(T + 1) − N(T) ≪ log T.
- **P4** : le point fragile sera l'uniformité de la formule locale de ζ′/ζ quand σ₀ → θ. Probabilité d'aboutir au seuil : environ 60 %.
- **P5** : pour Θ = 1, la convention inf ∅ = 1 suffit.

## Méthode

1. **Sens direct** (étapes 1 à 5 de `PREUVE.md`) : repris de TAC-022. La rédaction est rattachée aux étapes de TAC-017 vérifiées et au Lean : hypothèse de fenêtre en u, inégalité (★′), lemme de contradiction avec η = ½ log(e/d), et dichotomie. Les constantes du cas B sont explicitées (k ≥ |c₁|d/|c₂|).
2. **Réciproque** (étape 6) : entièrement refaite.
   - Formule de Perron exacte pour le noyau 1/(s(s − 1)), appliquée à la rampe **non centrée** ; le centrage est récupéré comme résidu G_c(1)·y en s = 1.
   - Déplacement du contour jusqu'à σ₀ = θ + a.
   - **Lemme des blocs** : ∫_j^{j+1} |G_c(σ₀ + it)| dt ≤ B log²j/a, avec B absolue. On décompose q = E_j − Σ_{Z_j} 1/(s − ρ), où E_j est holomorphe et O(log j) sur un rectangle ; puis on utilise Cauchy pour E_j′, Cauchy–Schwarz pour la somme sur les zéros, et ∫ dt/|s − ρ|² ≤ π/a.
   - Basses hauteurs : le rectangle [½, 1] × [−3, 3] est sans zéro. Segments horizontaux : majoration directe.
   - Choix a = 1/log y.
3. **Sources.** Les deux faits classiques utilisés, le comptage local des zéros (F1) et la formule locale de ζ′/ζ (F2), ont été contrôlés sur un cours en ligne, faute d'avoir les livres : [Bingham, Imperial College, leçon 27](https://www.ma.ic.ac.uk/~bin06/M34PM16-Analytic-Number-Theory/2013/m3pm16l27(13).pdf).
4. **Calcul** : `tac018_numerique.py` de TAC-022, rejoué sans modification (`python -I -B`, environ 1 s). La sortie `resultat_numerique.txt` est **identique octet pour octet** à celle de TAC-022.

## Résultat

**Le défaut de TAC-022 et sa correction.** TAC-022 déplaçait le contour de Φ_c = G_c/(s(s − 1)) − G_c(1)/(s − 1). Or le second terme a un module de l'ordre de |G_c(1)|/|t| : l'intégrale n'est pas absolument convergente, et l'argument était faux, comme l'a relevé la vérification. On intègre désormais F = G_c/(s(s − 1)), qui est O(log²t/t²) en moyenne sur chaque bloc, et l'on soustrait le résidu en 1. TAC-022 disait aussi que la forme au seuil « demanderait la convergence de Σ|c₁(ρ)| ». C'était un faux obstacle : on ne somme aucun résidu, on intègre sur une droite située à distance a de tous les zéros.

**L'énoncé démontré** (`PREUVE.md`) :
- (i) un plancher sur des fenêtres exclut les zéros à droite de θ ;
- (ii) un plafond aussi, mais seulement parce que ζ n'a pas de zéro réel ;
- (iii) si ½ ≤ θ < 1 et s'il n'y a aucun zéro à droite de θ, alors |H(y)| ≤ A y^θ (log y + 1/(1 − θ)) pour y ≥ exp(4/(1 − θ)), avec A absolue ;
- corollaire 1 : Θ = inf{θ : plancher sur des fenêtres tardives}, avec inf ∅ = 1 ;
- corollaire 2 : RH ⇔ H(y) = O(√y log y) ⇔ plancher en y^(½+ε) sur des fenêtres, pour tout ε.

**Contrôle numérique (inchangé).** Sur [10, 10⁶] :
- max |H(y)|/(√y log y) = 0,0938, atteint en y = 10 ;
- maximum par décade entre 0,017 et 0,041 ;
- dérive H(y)/y de l'ordre de 10⁻⁴ en 10⁶, donc G_c(1) centre bien H.

Ces mesures sont compatibles avec le corollaire 2, mais ne prouvent rien sur l'asymptotique.

| | Prévision | Résultat | Verdict |
|---|---|---|---|
| **P1** | sens direct inchangé sur le fond | inchangé ; seules les constantes du cas B et le rattachement à T17 sont précisés | **juste** |
| **P2** | O(y^(θ+ε)) par des bornes classiques de ζ′/ζ | vrai, mais la forme affaiblie n'est même pas nécessaire : la forme au seuil la contient | **juste** (sans objet séparé) |
| **P3** | O(y^θ log y) par les blocs, avec seulement N(T + 1) − N(T) ≪ log T | oui, sans perte de log supplémentaire ; il faut aussi la formule locale (F2) | **juste**, avec un ingrédient de plus que prévu |
| **P4** | point fragile : l'uniformité quand σ₀ → θ | non : (F2) vaut uniformément pour −1 ≤ σ ≤ 2, et le coût n'apparaît que par π/a. Le point délicat était ailleurs : prendre un ensemble de zéros Z_j plus large que celui de (F2), pour que E_j soit holomorphe sur tout le rectangle | **fausse** sur la localisation de la difficulté |
| **P5** | Θ = 1 réglé par inf ∅ = 1 | oui ; (iii) est alors sans objet (θ < 1) et (i) montre que l'ensemble est vide | **juste** |

*Ces verdicts sont ceux du producteur. Le vérificateur doit les rejuger, en particulier P3.*

## Portée

1. **Ce qui est établi.** Une caractérisation complète de Θ par la statistique H de l'article 1, d'un seul côté et sur des fenêtres dans un sens, des deux côtés et pour tout y dans l'autre. C'est l'analogue, pour les pôles doubles, du Landau par fenêtres d'Alpöge pour G (TAC-017). Le côté utile est inversé : un plancher, et non un plafond.
2. **Ce qui ne l'est pas.** Rien ne fournit le plancher. Comme le dit la vérification de TAC-022, une preuve de cette caractérisation ne donne pas par elle-même les fenêtres de l'hypothèse de Riemann. C'est une reformulation de RH, utile seulement si un outil peut produire le plancher. Je n'en connais pas pour H. Chez Alpöge, c'est l'arithmétique (hôtes, familles, moyenne sur les caractères) qui produit la borne sur G, et rien de tel n'existe ici pour les pôles doubles.
3. **Par rapport au théorème A de l'article 1.** Le théorème A lit Θ dans la croissance d'une moyenne quadratique Q. Le théorème A′ la lit dans un seul côté de H, ponctuellement sur des fenêtres. Il est plus faible comme hypothèse (une inégalité d'un seul côté, seulement sur des fenêtres) et plus fort comme conclusion (une borne ponctuelle). Le signe négatif de c₂ aux pôles réels explique pourquoi c'est le plancher qui compte.
4. **Nouveauté.** La méthode est classique : un Landau de type Alpöge, et pour la réciproque la formule de Perron avec la formule locale de ζ′/ζ. Je ne connais pas l'énoncé exact pour cette statistique c(n) dans la littérature, mais je n'ai pas fait de recherche bibliographique systématique. Le statut « classique » reste donc possible.
5. **Anti-circularité.** La réciproque **suppose** l'absence de zéros à droite de θ ; elle ne la démontre pas. Le calcul mesure H, il ne suppose rien.

## Critère de rejet

- *Réciproque au seuil non justifiable uniformément :* elle l'est. Chaque constante de l'étape 6 est absolue, sauf le terme 1/(1 − θ) et le seuil y₀(θ). **Non atteint.**
- *Ingrédient non classique :* le comptage local des zéros (F1) et la formule locale de ζ′/ζ (F2) sont des théorèmes standard et inconditionnels. Il n'y a ni densité de zéros, ni hypothèse sur l'espacement des zéros. **Non atteint.**
- *Énoncé déjà dans la littérature :* non vérifié systématiquement (voir Portée, point 4).

Le vérificateur peut réfuter ce dépôt par :
- un défaut d'holomorphie ou de borne de E_j sur R_j (étape 6(c)) ;
- une erreur sur les segments horizontaux ou les basses hauteurs ;
- une référence montrant que l'énoncé est connu (statut « classique »).

## Statut proposé

**demontre**, pour le théorème A′ (i), (ii), (iii) et ses deux corollaires, avec la réserve bibliographique du point 4. L'énoncé est **équivalent à RH** par le corollaire 2 : c'est une reformulation, pas un progrès vers RH, puisque rien ne fournit le plancher.

Je demande la vérification à `ia:chatgpt-sol-6.1-max`, qui n'a pas produit ce dépôt. Points à regarder en priorité :
1. le lemme des blocs, étape 6(c) ;
2. la formule de Perron et le résidu en 1, étapes 6(a) et 6(b) ;
3. le cas B de l'étape 5 avec le plancher.
