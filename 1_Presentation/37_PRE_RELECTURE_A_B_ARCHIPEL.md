# V6.13 — Pré-relecture : les Théorèmes A et B et l'Archipel d'Euler

**Date :** 10 octobre 2026  
**Statut :** pré-relecture interne. Trois relectures indépendantes, menées en parallèle, ont chacune refait une preuve pas à pas, avec des contrôles numériques courts et une recherche d'antériorité. Ce n'est pas une relecture par un spécialiste : le niveau « Démontrer, faire relire » de l'indicateur reste à 6. Le niveau 7 (« Relu ») demande un lecteur humain.  
**Demande de l'auteur :** « Suis cette trajectoire avec les 3 relectures d'abord en parallèle puis les autres. » Le coup « Préparer la relecture » venait en tête des priorités refaites en V6.12 (document 36, §7).  
**Dossier à envoyer :** `1_Presentation/relecture/`, en anglais. On l'ouvre par `00_READ_ME_FIRST_EN.md`.

## 1. Le coup et sa prévision

Le navigateur avait pré-enregistré ce coup en V6.12 :

- **Question :** le dossier de relecture (Théorèmes A et B, note sur l'Archipel) est-il à jour, et pose-t-il des questions précises ?
- **Réfutation possible :** une erreur trouvée dans A ou B pendant la préparation.
- **Ce qui était attendu :** un dossier court, à jour, avec trois questions précises.

**Résultat : la réfutation n'a pas eu lieu.** Aucune erreur dans A ni dans B. Une phrase fausse a été trouvée et corrigée dans la note 30 (§3.1). Le dossier existe, avec trois questions précises par résultat.

## 2. La méthode

Trois relectures ont tourné en même temps, chacune sur un seul résultat et sans voir les deux autres. Chacune devait :

1. refaire la preuve étape par étape, à partir des énoncés du corpus ;
2. lister ce qui est solide et ce qui est fragile ;
3. faire de courts contrôles numériques avec son propre code ;
4. chercher l'antériorité (articles, livres, notes de cours) ;
5. écrire une note en anglais, autonome et envoyable, plus un résumé en français.

**Limite de la méthode.** Les trois relectures ont été faites par des agents de la même famille de modèles que celui qui a aidé à écrire les preuves. Elles sont indépendantes entre elles, mais pas du processus d'écriture. Plusieurs références sont citées de mémoire ; chaque note dit lesquelles.

## 3. Les verdicts

| Résultat | Énoncé court | Verdict | Nouveauté |
|---|---|---|---|
| **Théorème A** | Avec c = Λ∗Λ − Λ·log + 2γΛ, C(x) = Σ~n≤x~ c(n) et Q(X) = ∫~1~^X^ \|C(x)\|² x^−2^ dx : ½·limsup log(1+Q(X))/log X = Θ − ½. Sans hypothèse. | **Correct.** Prêt après trois retouches de rédaction. | Analogue au second ordre de la caractérisation classique de Θ par ψ(x) − x. Méthode standard : à présenter comme une proposition, sans revendiquer de nouveauté. |
| **Théorème B** | Sous RH : Q(X) ∼ (S/3)(log X)³ avec S = Σ~ρ~ m²(m+1)²/\|ρ\|². Pour des zéros simples, S = 4κ, κ = 2 + γ − log 4π. | **Correct.** Prêt après quatre retouches. | Énoncé non trouvé dans la littérature, mais c'est la transposition du théorème de Cramér au pôle double. Corollaire nouveau à faire vérifier (§5). |
| **Archipel d'Euler** (note 30, §3) | Rigidité au premier ordre aux points d'Euler ; dans V~q~, « aucun zéro dans Re s > 1 » ⟺ point d'Euler. | **Correct sur le fond.** Une phrase fausse (§3.1), un trou comblable (§3.4). | Le corollaire est un cas particulier immédiat de Saias–Weingartner [SW09] (2009, Th. 2) : pas nouveau. La proposition de rigidité est juste et élémentaire. |

## 4. Théorème A

**Vérifié.** Les deux sens de la preuve ont été refaits :

- minoration : transformée de Mellin, Cauchy–Schwarz sur des intervalles dyadiques, prolongement analytique ;
- majoration : formule de Perron tronquée aux demi-entiers, puis déplacement du contour jusqu'à Θ + ε/2.

Les lemmes L1, L3, L4, L5, les cas Θ = ½ et Θ = 1, la convention log(1+Q), la différence entre limsup et lim, et le rôle des multiplicités ont aussi été vérifiés.

**Un point de structure éclairci.** Le pôle double ne sert pas pour A. Il suffit d'un vrai pôle en chaque zéro, et c'est le signe + de q² + q′ qui le garantit : au zéro ρ de multiplicité m, le coefficient polaire vaut m(m+1) ≠ 0. Construite sur ζ″/ζ, la même preuve exigerait ζ″(ρ) ≠ 0. Le pôle double sert pour B.

**Retouches faites.**

| Où | Problème | Correction |
|---|---|---|
| Étape 2(a) | Le cercle de Cauchy qui borne q′ sort de la région où la borne sur q est énoncée. | Énoncer la borne sur σ ≥ Θ + ε/4. Fait dans la note A et dans `LEMMES_RIGOUREUX.md` (correctif avant (6.3)). |
| Perron | Référence et hypothèses manquantes. | Titchmarsh [Tit86], lemme 3.12, avec la borne Σ\|c(n)\|n^−σ^ ≪ (σ−1)^−2^ qu'il exige. |
| Littérature | Le dossier v4.5 attribuait à Brent–Platt–Trudgian [BPT22] la croissance en c·log X de la moyenne logarithmique de (ψ − x)². | Leur résultat porte sur ∫~X~^2X^(ψ−x)²dx. Le c·log X vient de Cramér (1922) [Cra22] et de Montgomery–Vaughan [MV07] (Th. 13.6). |

**Conséquence pratique.** Le dossier de relecture 03 (V4.5) et le message 05 ne doivent plus être envoyés tels quels : la note `RELECTURE_THEOREME_A_EN.md` remplace la section 3 du dossier 03, et corrige l'attribution.

## 5. Théorème B

**Vérifié.** Toute la preuve a été refaite :

- Plancherel [Tit37] sur la droite Re s = ½ + η ;
- borne ponctuelle de G et queue uniforme en η ;
- calcul local du pôle double, de constante A²/(4|ρ|²) ;
- termes croisés entre zéros, et ordre des limites ;
- étape taubérienne de Karamata [Kar31], et valeur S = 4κ.

Q~η~ est exactement la transformée de Laplace–Stieltjes de la fonction croissante U(L) = Q(e^L^), au point λ = 2η : le théorème de Karamata s'applique tel quel. La valeur de κ est vérifiée à 8·10^−6^ près (en relatif), avec 1 070 zéros et une correction de queue.

**Un point qu'un relecteur posera.** Les paires de zéros très proches ne touchent pas le terme dominant, parce que la limite η → 0 est prise à hauteur Y fixée, avant Y → ∞. C'est aussi pourquoi le théorème ne donne aucune vitesse.

**Retouches faites dans la note B.**

1. Restreindre η à (0, ¼] à l'étape 4, sinon la droite sort du rectangle [½, ¾].
2. Remplacer O~Y~(η^½^) par O~Y~(η).
3. Rédiger en entier la borne \|G\| ≪ (log t)·W + log² t (le « point majeur » de l'ancien rapport REFEREE_B).
4. Donner des références exactes pour les entrées classiques F1–F4 (Titchmarsh 9.2 et 9.6(A), Davenport ch. 12, Widder [Wid41] ou Korevaar [Kor04] pour Karamata). Elles sont citées de mémoire et signalées comme telles.

**Un corollaire nouveau (B′), à faire vérifier.** Sous RH, S ≥ 4κ, avec égalité si et seulement si tous les zéros sont simples. Donc, sous RH :

> Q(X)/(log X)³ → 4κ/3 ⟺ tous les zéros de ζ sont simples.

*Preuve.* L'identité qui donne κ compte les zéros avec multiplicité : Σ~distincts~ m/|ρ|² = κ. Donc S − 4κ = Σ~distincts~ (m²(m+1)² − 4m)/|ρ|². Chaque terme est positif ou nul, et nul exactement quand m = 1. ∎

**Remarque de rédaction (non vérifiée dans la littérature).** Le même argument, appliqué à la constante de Cramér Σ~distincts~ m²/|ρ|², donne l'énoncé jumeau pour ψ : sous RH, ∫~1~^X^ (ψ(x) − x)² x^−2^ dx ∼ κ·log X si et seulement si les zéros sont simples. Cette version est probablement connue. Ce qui distingue B, c'est la sensibilité. Un zéro double compte 36/|ρ|² dans S, contre 8/|ρ|² pour deux zéros simples au même endroit : 4,5 fois plus. Dans la constante de Cramér, il compte 4/|ρ|² contre 2/|ρ|² : 2 fois plus.

**Hors du Théorème B : α corrigé.** L'ancienne valeur α ≈ −0,264 était une somme partielle sur 300 zéros, sans correction de queue. La valeur corrigée est **α ≈ −0,3074**, stable de 100 à 1 070 zéros, parce que Re b~ρ~ = −2θ′(γ) − 2γ~E~ exactement. β ≈ 0,64 reste incertain. Avec ces valeurs, Q(X) est reproduit à 1–5 % près jusqu'à X = 10^8^. Correctif ajouté à la fin de `ALPHA_BETA_ANALYSE.md`.

## 6. L'Archipel d'Euler

**Vérifié.** Les preuves du §3 de la note 30 ont été refaites : équation fonctionnelle commune, formule du défaut au premier ordre, noyau du défaut, déduction à partir de Saias–Weingartner. La formule du défaut est exacte à 2,9·10^−14^ près aux 27 points d'Euler, pour toutes les directions et tous m, n ≤ 40.

**Ce qui est solide, et même renforcé.**

- La Proposition 3.3 est juste, et la formule vaut pour tous m, n, pas seulement pour m et n premiers entre eux.
- Elle devient une **identité exacte** : pour une direction transverse b = Σ~χ′≠χ~ β~χ′~ u~χ′~ χ′ au point d'Euler λ·u~χ~·L(s, χ), la moyenne du carré du défaut sur les paires de classes vaut λ²·(3·Σβ² + |Σβu|²), donc au moins 3λ²·Σβ². Les valeurs propres 2,36 à 3,27 de la V6.8 dépendaient de la troncature (M = 40) ; c'est l'identité qu'il faut citer.
- Le corollaire 3.4 devient une **équivalence** : pour c ≠ 0, aucun zéro dans Re s > 1 ⟺ point d'Euler.

**Ce qui était faux ou incomplet, et la correction faite dans la note 30.**

| Endroit | Problème | Correction |
|---|---|---|
| §3.1 | « Même chose dans V~5~ pair » est faux tel quel : (1 + 5^1/2−s^)·ζ(s) a exactement l'équation fonctionnelle de L(s, (·/5)), et donne une déformation (avec un pôle). | La phrase ne vaut que dans V~q~, ou parmi les fonctions entières. Corrigée. |
| §3.3 | La phrase en gras et le titre ne disaient pas « dans V~q~ ». D'autres directions gardent l'équation fonctionnelle hors de V~q~. | « dans V~q~ » ajouté ; identité exacte ajoutée. |
| §3.4 | La déduction écrite avait un trou : phases u~χ~ disparues, module du caractère de Saias–Weingartner quelconque, cas particuliers (p(1) = 0, caractère trivial ou de mauvaise parité, c = 0) non traités. | Citer directement Saias–Weingartner, Th. 2 : une combinaison d'au moins deux fonctions L primitives a ≫ T zéros dans 1 < Re s < 1 + η. |
| Attribution | « Démontré ici » pour le corollaire. | « Cas particulier immédiat de Saias–Weingartner (Th. 2) et de Booker–Thorne [BT14] (Th. 1.2) ». |

**Le degré 2 est déjà en partie connu.** Booker et Thorne (2014, Th. 1.1) donnent l'analogue du corollaire 3.4 pour les formes de poids 24 et niveau 1 : une forme sans zéro dans Re s > 25/2 est une forme propre de Hecke. Ce qui reste à faire en degré 2 :

- l'analogue de la rigidité au premier ordre (Proposition 3.3), et de la constante 3 ;
- les îles mesurées autour des deux formes propres, et leur rétrécissement avec la hauteur.

Le cadre naturel des §4 à §6 de la note 30 est celui de Bombieri et Hejhal (1995) [BH95], qui étudient exactement ces combinaisons à équation fonctionnelle commune (référence lue dans Booker–Thorne, non revérifiée).

## 7. Ce qui a changé dans le corpus

| Fichier | Changement |
|---|---|
| `1_Presentation/relecture/` (nouveau) | Trois notes envoyables en anglais, trois résumés en français, une page d'entrée `00_READ_ME_FIRST_EN.md`. |
| `1_Presentation/30_ARCHIPEL_D_EULER.md` (et PDF) | §3.1 corrigé ; §3.3 « dans V~q~ » et identité exacte ; §3.4 correctif et attribution. |
| `3_Preuves_et_calculs/preuves/LEMMES_RIGOUREUX.md` | Correctif ε/4 avant les bornes (6.3)–(6.4). |
| `3_Preuves_et_calculs/preuves/ALPHA_BETA_ANALYSE.md` | Correctif α ≈ −0,3074. |
| Navigateur | « Préparer la relecture » passe à fait ; « L'Archipel en degré 2 » est recentré sur ce que Booker–Thorne ne couvrent pas ; « Faire relire » pointe vers le nouveau dossier. |

## 8. Ce que cela change pour la suite

- **Faire relire** est maintenant possible sans préparation supplémentaire. C'est un coup humain : choisir un destinataire et envoyer `relecture/`. Un projet de message est en annexe.
- **Le degré 2** perd une partie de son gain attendu, puisque l'analogue de 3.4 est publié. Il garde la rigidité au premier ordre et la mesure des îles.
- **La loi de seuil des innovations** devient le premier coup de recherche. C'est le suivant.

## 9. Lecture selon l'hypothèse

L'hypothèse de travail est que RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand qui la rend nécessaire.

**L'Archipel n'est pas nouveau, et c'est une bonne nouvelle pour l'hypothèse.** L'énoncé « l'absence de zéro dans Re s > 1 force le produit d'Euler », dans les espaces V~q~, est un théorème publié : Saias–Weingartner en degré 1, Booker–Thorne en degré 2. Le sens local de l'hypothèse (la propriété des zéros oblige la structure multiplicative) est donc un terrain établi par d'autres, avec d'autres méthodes. L'apport propre du corpus est ailleurs : la constante 3 de la rigidité au premier ordre, et la mesure des îles qui rétrécissent avec la hauteur.

**Le corollaire B′ ajoute un trait.** Sous RH, la simplicité des zéros, une autre conjecture, se lit dans une seule constante de croissance d'une somme sur les premiers : 4κ/3. Les deux propriétés des zéros (être sur la droite, être simples) se lisent donc du côté des premiers, sur la même fonctionnelle Q : l'exposant de Q donne Θ (Théorème A), sa constante donne les multiplicités (B′). Le pôle double rend cette constante 4,5 fois plus sensible à un zéro double que la constante de Cramér.

**Supposé.** Que cette double lecture (exposant, constante) soit la trace, du côté des premiers, d'une seule positivité sur l'objet plus grand. Rien ici ne le montre.

## 10. Démontré, mesuré, supposé

| | Énoncé | Statut |
|---|---|---|
| Démontré (relu en interne) | Théorème A ; Théorème B sous RH ; Proposition 3.3 et identité λ²·(3·Σβ² + \|Σβu\|²). | Preuves refaites ; aucune erreur. Relecture humaine à venir. |
| Démontré, déjà connu | Corollaire 3.4 de l'Archipel (degré 1) ; son analogue en degré 2 pour S~24~. | Saias–Weingartner ; Booker–Thorne. |
| Démontré, à faire vérifier | Corollaire B′ : sous RH, S ≥ 4κ, égalité ⟺ zéros simples. | Preuve d'une ligne ; nouveauté non établie. |
| Mesuré | κ à 8·10^−6^ ; α ≈ −0,3074, stable de 100 à 1 070 zéros ; Q reproduit à 1–5 % jusqu'à 10^8^ ; formule du défaut à 2,9·10^−14^. | Contrôles des relectures. |
| Supposé | Exposant et constante de Q comme traces d'une même positivité. | Aucune preuve. |

## 11. Limites

- Relectures faites par des agents IA, pas par des spécialistes.
- Recherche d'antériorité limitée au web : ni MathSciNet ni zbMATH.
- Références citées de mémoire (numéros de lemmes de Titchmarsh, Montgomery–Vaughan Th. 13.6) : signalées dans chaque note.
- Cramér (1922) et Hamburger [Ham21] n'ont pas été lus ; seules leurs données bibliographiques ont été vérifiées.

## 12. Les questions au relecteur

Les neuf questions des trois notes, ramenées à trois :

1. **Théorème A.** La majoration est-elle complète telle qu'écrite (Perron aux demi-entiers, contour jusqu'à Θ + ε/2 avec G ≪ log²|t|) ? A est-il une conséquence de routine des résultats classiques sur ψ(x) − x, et quelle référence citer ?
2. **Théorème B.** B, ou un théorème de type Cramér pour des pôles d'ordre k sur Re s = ½, existe-t-il déjà ? La preuve peut-elle se passer de toute information sur les écarts entre zéros ? Le corollaire B′ est-il juste et connu ?
3. **Archipel.** L'attribution « corollaire immédiat de Saias–Weingartner, Th. 2 » est-elle la bonne ? En degré 2, la rigidité au premier ordre aux formes propres de Hecke [Hec37] est-elle connue ?

## Annexe — Projet de message d'accompagnement (anglais)

> **Subject:** Request for a check of three short notes (no claim on the Riemann Hypothesis)
>
> Dear Professor X,
>
> I am not a mathematician. With help from AI assistants, I have written three short notes on mean squares of sums over primes and on combinations of Dirichlet L-functions. I make no claim about the Riemann Hypothesis: Theorem A is an exact reformulation of the position of the rightmost zero, and Theorem B is conditional on RH.
>
> Each note was pre-checked internally, but not by a specialist. Could you tell me, in a few lines, whether the proofs have errors or gaps, and whether the results are already known? The questions are on the first page (`00_READ_ME_FIRST_EN.md`).
>
> Whatever your answer, I will take it as final. Thank you for your time.
>
> [signature]

## Fichiers

- Dossier : `1_Presentation/relecture/` (`00_READ_ME_FIRST_EN.md`, trois notes `RELECTURE_*_EN.md`, trois résumés `RELECTURE_*_RESUME_FR.md`).
- Corrections : `30_ARCHIPEL_D_EULER.md` (et PDF), `LEMMES_RIGOUREUX.md`, `ALPHA_BETA_ANALYSE.md`.
- Test : `tests/test_v613_relecture.py`.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [BH95] E. Bombieri, D. A. Hejhal. *On the distribution of zeros of linear combinations of Euler products*. Duke Math. J. 80 (1995), 821–862. <https://arxiv.org/abs/0704.3448> — partiellement vérifié. **Correctif V6.18 :** Bombieri–Hejhal montrent (sous RH pour chaque fonction et une hypothèse d'espacement) que 100 % des zéros, en densité, sont sur la droite ; la fermeture de la plage de survie n'en découle pas directement : elle reste une attente du corpus.
- [BPT22] R. P. Brent, D. J. Platt, T. S. Trudgian. *The mean square of the error term in the prime number theorem*. J. Number Theory 238 (2022), 740–762 ; arXiv:2008.06140. <https://arxiv.org/abs/2008.06140> — vérifié en ligne
- [BT14] A. R. Booker, F. Thorne. *Zeros of L-functions outside the critical strip*. Algebra Number Theory 8 (2014), no. 9, 2027–2042 ; DOI 10.2140/ant.2014.8.2027 ; arXiv:1306.6362 ; correction ANT 8:9. <https://arxiv.org/abs/1306.6362> — vérifié en ligne
- [Cra22] H. Cramér. *Ein Mittelwertsatz in der Primzahltheorie*. Math. Z. 12 (1922), 147–153. — partiellement vérifié
- [Ham21] H. Hamburger. *Über die Riemannsche Funktionalgleichung der ζ-Funktion*. Math. Z. 10 (1921), 240–254. <https://gdz.sub.uni-goettingen.de/download/pdf/PPN266833020_0010/PPN266833020_0010.pdf> — vérifié en ligne
- [Hec37] E. Hecke. *Über Modulfunktionen und die Dirichletschen Reihen mit Eulerscher Produktentwicklung I, II*. Math. Ann. 114 (1937), 1–28 et 316–351 (non vérifié). — non vérifié
- [Kar31] J. Karamata. *Neuer Beweis und Verallgemeinerung der Tauberschen Sätze, welche die Laplacesche und Stieltjessche Transformation betreffen*. J. reine angew. Math. 164 (1931), 27–39. — non vérifié
- [Kor04] J. Korevaar. *Tauberian Theory: A Century of Developments*. Grundlehren math. Wiss. 329, Springer, 2004. — partiellement vérifié
- [MV07] H. L. Montgomery, R. C. Vaughan. *Multiplicative Number Theory I. Classical Theory*. Cambridge Stud. Adv. Math. 97, Cambridge University Press, 2007. <https://personal.science.psu.edu/rcv4/personal/Publications/MNTI/19.0_pp_463_485_Oscillations_of_error_terms.pdf> — partiellement vérifié
- [SW09] É. Saias, A. Weingartner. *Zeros of Dirichlet series with periodic coefficients*. Acta Arith. 140 (2009), no. 4, 335–344 ; DOI 10.4064/aa140-4-4 ; arXiv:0807.0783. <https://arxiv.org/abs/0807.0783> — vérifié en ligne
- [Tit37] E. C. Titchmarsh. *Introduction to the Theory of Fourier Integrals*. Oxford, Clarendon Press, 1937. — non vérifié
- [Tit86] E. C. Titchmarsh. *The Theory of the Riemann Zeta-Function*. 2e éd., révisée par D. R. Heath-Brown, Oxford, Clarendon Press, 1986. — partiellement vérifié
- [Wid41] D. V. Widder. *The Laplace Transform*. Princeton Univ. Press, 1941. — partiellement vérifié

<!-- references:fin -->
