# Programme Riemann — Synthèse

*Mis à jour en V6.58, 17 octobre 2026. Mises à jour précédentes : V6.24 et V6.18, conservées dans `4_Archives/historique/`. Version d'origine : synthèse de la version 5.1 (octobre 2026). État décrit : V6.58. Version anglaise : [english/01_SYNTHESIS_EN.md](english/01_SYNTHESIS_EN.md).*

**Statut :** l'essentiel en quelques pages, pour un lecteur qui découvre le programme. Pour l'état courant en un coup d'œil, voir le bloc « À lire d'abord » du [README](../README.md) ; pour la logique complète, la [table logique](../TABLE_LOGIQUE.md).  
**Auteur :** Vincent NOËL

> **À retenir**
>
> - Aucune preuve de l'hypothèse de Riemann (RH) n'est revendiquée. Les résultats ci-dessous sont présentés pour ce qu'ils sont.
> - Trois énoncés analytiques démontrés (Théorèmes A et B, corollaire B′), pré-relus en interne en V6.13. Aucun spécialiste ne les a encore relus ; c'est la prochaine marche.
> - La positivité de Weil est **certifiée sur tous les tests** à moments nuls, mais seulement sur des fenêtres bornées (support jusqu'à 11/20). Zhu (2026) la certifie jusqu'à 0,8 pour toutes les fonctions ; la marge s'effondre à chaque élargissement.
> - Dans le Modèle réduit, là où RH est un théorème, le signe ne vient ni des comptages ni des degrés, mais d'un **carré** (une polarisation). ζ passe déjà les deux premiers niveaux. Ce qui manque est l'objet qui fournirait le carré.
> - Chaque coup récent écrit sa prévision avant le calcul. Plusieurs prévisions ont été fausses, et les documents le disent.

## 1. La question et l'hypothèse de travail

**La question de départ.** On associe aux nombres premiers une quantité Q(X), une somme de carrés construite pour que chaque zéro de la fonction ζ de Riemann devienne un pôle double. Sa vitesse de croissance dit à quelle distance de la droite critique se trouve le zéro le plus éloigné. Les versions 1 à 5 ont établi et contrôlé cette reformulation.

**L'hypothèse de travail de l'auteur.**

> *RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand qui la rend nécessaire.*

Là où un analogue de RH est démontré, la preuve passe par une positivité sur un objet plus grand que la fonction elle-même : la surface C × C pour les courbes sur les corps finis (Weil, 1948 [Wei48]), un espace de Hilbert pour la fonction zêta de Selberg (Selberg, 1956 [Sel56]). Pour ζ, cet objet n'est pas construit. Le programme ne l'attaque pas de front. Il pose trois questions plus petites : quelle est la signature d'une nécessité démontrée ? ζ la présente-t-elle ? Que manque-t-il, exactement ?

## 2. Ce qui est démontré

Les énoncés en forme logique, avec leurs hypothèses et leur statut, sont dans la [table logique](../TABLE_LOGIQUE.md).

| | Énoncé | Statut |
|---|---|---|
| **Théorème A** | Avec c = Λ∗Λ − Λ·log + 2γΛ, C(x) = Σ~n≤x~ c(n) et Q(X) = ∫~1~^X^ \|C(x)\|² x^−2^ dx : ½·limsup log(1+Q(X))/log X = Θ − ½, où Θ est la plus grande partie réelle des zéros. Donc RH ⟺ Q(X) = X^o(1)^. | Démontré, sans hypothèse ; pré-relu (doc. 37). Une reformulation exacte de RH, pas une étape vers elle. |
| **Théorème B** | Sous RH, Q(X) ∼ (S/3)(log X)³, avec S = Σ~ρ~ m²(m+1)²/\|ρ\|². | Démontré sous RH ; transposition au pôle double du théorème de Cramér [Cra22]. |
| **Corollaire B′** | Sous RH, Q(X)/(log X)³ → 4κ/3 si et seulement si tous les zéros sont simples (κ = 2 + γ − log 4π). Avec A, critère conjoint RH–simplicité. | Démontré ; nouveau à notre connaissance, à faire vérifier. |
| **Certificats de Weil** (docs 71, 73, 75) | Pour tous les tests de support [−S, S], d'énergie finie, à moments exponentiels nuls : Q_W(f) ≥ ‖f‖²/25 si S ≤ 0,347 ; ≥ ‖f‖²/250 si S ≤ 1/2 ; ≥ (3/10000)‖f‖² si S ≤ 11/20. Sans zéros ni RH. | Certifiés par arithmétique d'intervalles dans le modèle déclaré. En portée, couverts par le minorant certifié de Zhu [Zhu26]. |
| **Tête des conducteurs** (essai V6.55) | Restitution exacte de la somme de Möbius ; tête q ≤ H bornée explicitement à toutes les échelles. | Démontré sous ses gardes. La grande queue reste ouverte. |
| **Trois niveaux du signe** (doc. 80) | Pour un polynôme stable par α ↦ q/α : degrés N(u) ≥ 0 ⟺ racines réelles de multiplicité paire ; à racines distinctes, la forme B = Tr(u·ι(u)) a r/2 directions négatives. | Démontré (élémentaire) ; 645 polynômes vérifiés exactement. |
| **Autres** | Rigidité au premier ordre aux points d'Euler (doc. 30 ; « RH ⇒ point d'Euler » est un cas de Saias–Weingartner [SW09]) ; lemme d'inertie (38) ; marge locale = corrélation de paires (40) ; lemme des jets (58) ; certificat négatif de DH (60). | Démontrés dans leur cadre. |

La pré-relecture a été faite par trois relectures indépendantes entre elles, mais menées par des modèles de la même famille que ceux qui ont aidé à écrire les preuves. Elle ne remplace pas un spécialiste.

## 3. Ce qui est mesuré de plus solide

Toutes ces mesures sont reproductibles : données, scripts et tests (`python tests/run_all_tests.py`).

| Résultat (document) | Ce qui est mesuré | Chiffres clés |
|---|---|---|
| **Modèle réduit** (28, 29, 80) | Sur les courbes sur les corps finis, où RH est un théorème : l'équation fonctionnelle et un produit d'Euler positif ne suffisent pas ; la positivité de Castelnuovo [MT58], étage par étage, démasque les faux. En V6.58 : les degrés d'isogénie ne suffisent pas non plus ; seule la trace d'un carré démasque les 119 faux jumeaux de genre 2. | 425 courbes ; 220 faux jumeaux ; réalisation de Gram exacte pour 424 courbes. |
| **Archipel d'Euler** (30) | Parmi les fonctions qui ont la même équation fonctionnelle, RH ne survit qu'autour des points d'Euler, dans des îles qui rétrécissent avec la hauteur. | 27 îles ; rayon médian 0,091 (\|t\| ≤ 25) puis 0,008 (\|t\| ≤ 300). |
| **Générateur des premiers** (33) | L'opérateur de ζ se reconstruit avec les seuls nombres premiers. Sa métrique est positive pour ζ et L(s, χ~5~), négative pour Davenport–Heilbronn [DH36a] [DH36b] exactement à ses zéros hors droite. | 284 zéros de ζ avec les premiers ≤ 23 862 ; aucune fausse détection. |
| **Temps de Heisenberg** (38, 39) | Un quadruplet hors droite s'entend dès que la fenêtre atteint log(q·γ~0~/2π) ; la loi double en degré 2. | Rapport 0,95–1,08 pour ζ et L. |
| **Rencontre à trois et loi de la marge** (40, 41) | RH, simplicité et répulsion se lisent sur une même quantité, la corrélation de paires de Montgomery [Mon73]. | 1 070 zéros de ζ : 4 marges < 0,1 (GUE : 13 ; Poisson : 320). |
| **Fenêtres de Weil** (81) | Les valeurs λ*(L) de Zhu, de 0,5 à 0,8, retrouvées par une méthode indépendante (forme en variable x, contrôlée par les zéros à 2·10⁻¹³). Sur les tests à moments nuls, la marge est beaucoup plus grande. | λ*(0,8) ≈ 1,8·10⁻¹⁷ ; noyau des moments : 9,2·10⁻⁴ à 11/20, 5,4·10⁻¹² à 0,8. |

La lecture qui relie ces mesures est la suivante. ζ présente toutes les signatures observables d'une nécessité démontrée, sauf l'objet qui la porte. Ce qui manque n'est pas l'opérateur, qu'on sait reconstruire, ni un comptage, qui est déjà positif : c'est un carré imposé par une structure, et non seulement mesuré.

## 4. Ce qui reste ouvert ou supposé

**Ouvert, au sens de la table logique.**

- La loi de signe sur une famille de tests couvrante, et la couverture qui la transporte à tous les tests (route W : W9, W10, W11).
- L'objet qui fournirait le carré pour ζ (route C : C5).
- La croissance lente de Q depuis les seuls premiers (route Q : Q4), équivalente à RH.
- La dette signée des grands conducteurs, puis la borne J ≪ X² (route J : J5, J7).
- Une réalisation spectrale exhaustive (route H : H3, H4).

**Supposé.**

- Qu'un objet plus grand porte la positivité de ζ, comme la jacobienne polarisée le fait pour une courbe. C'est l'hypothèse de travail elle-même.
- Que ce même objet impose aussi la loi de la marge entre les zéros, comme le groupe de monodromie le fait sur les corps finis (Katz–Sarnak [KS99]).
- Que les îles de l'Archipel se referment jusqu'à zéro à grande hauteur.
- Que le déficit de petites marges vienne de la hauteur finie (Bogomolny et al. [BBLM06]).

## 5. Le chemin depuis la V6.24

La synthèse précédente s'arrêtait à la V6.24 (11 octobre 2026). Les étapes suivantes, regroupées :

| Versions | Ce qui a été fait | Statut |
|---|---|---|
| V6.25–V6.33 | Audit des unités fictives (50) ; Frobenius de caractéristique un, lu (51) ; le carré en continu (52) ; Rencontre en hauteur (53) ; trou à trois (54) ; articles présentables (55) ; relief et force du relief de l'Archipel (56, 57). | mesuré ; plusieurs prévisions fausses, dites |
| V6.34–V6.37 | Lemme des jets (58) ; de la tour finie à la borne spectrale (59) ; trois articles en LaTeX et un certificat de négativité pour DH (60) ; ancrage apparié (61). | démontré dans le cadre ; certificat |
| V6.38–V6.43 | Atlas des décisions et Bellman (62) ; contraintes et comparaison exactes (63, 64) ; fibres, plis et un pli certifié (65, 66) ; ponts avec Bellman (67). | outils ; preuves auxiliaires |
| V6.44–V6.50 | Domaines et queue effective (68, 69) ; pont arithmétique et dette de couplage (70) ; premiers certificats complets de Weil sur des fenêtres, jusqu'à S = 11/20 (71 à 75). | certifié dans le domaine déclaré |
| V6.51–V6.57 | Piste globale de Weil reconstruite (76) et son complément (parité de Suzuki suspendue, opérateur unilatéral T₊) ; mécanismes pour le signe (77) ; transport positif (78) ; compensation, profils et obstructions (79) et signal (complément 79) ; corrélations ancrées ; amplification arithmétique (tête acquise, queue ouverte). | preuves auxiliaires ; obstructions ; ouvert |
| V6.58 | D'où vient le signe : comptage, degré ou carré (80) ; Zhu reproduit (81) ; réorganisation (README, plan, table logique, références hiérarchisées, guide pour une IA, couche anglaise). | démontré (élémentaire) ; mesuré |

## 6. L'indicateur à la V6.58, et la suite

L'indicateur place le programme sur une échelle de 0 (rien) à 9 (résolu). Les niveaux n'ont pas bougé depuis la V6.18 ; chaque étape a été réévaluée et motivée.

| Dimension | V5 (5 oct.) | V6.58 (17 oct.) | Niveau atteint |
|---|---:|---:|---|
| Voir | 4 | 4 | Mesure robuste |
| Comprendre | 3 | 5 | Mécanisme compris, dans un cas où RH est démontrée |
| Situer | 3 | 6 | Énoncé démontré |
| Étendre au degré 2 | 0 | 4 | Mesure robuste |
| Démontrer, faire relire | 6 | 6 | Énoncé démontré |
| La case vide | 2 | 4 | Mesure robuste |
| Croiser | 0 | 6 | Énoncé démontré |

Aucune dimension n'atteint 7 (« Relu ») : il faut un lecteur humain.

**La suite.** Le coup le plus rentable reste humain : faire relire l'article 1 (Théorèmes A et B) par un spécialiste, qui pourrait aussi parrainer un premier dépôt sur arXiv. Côté recherche, la table logique montre deux manques nets : la loi de signe sur une famille couvrante (route W) et l'objet qui fournirait le carré (route C, sans investigation ouverte à ce jour). Prolonger les fenêtres une à une n'est pas une stratégie vers RH.

## 7. Comment lire le corpus

| Entrée | À quoi elle sert |
|---|---|
| [README](../README.md), « À lire d'abord » | Six points essentiels, leurs statuts et leurs liens ; [version anglaise](../README_EN.md). |
| `00_PORTAIL.html` | La page d'entrée interactive : état, dernières étapes, catalogue de tous les fichiers. |
| [Table logique](../TABLE_LOGIQUE.md) | Les énoncés en forme logique, cinq routes vers RH, ce qui manque au plus court. |
| [Plan du corpus](../PLAN_DU_CORPUS.md) | Les 81 documents rangés par question. |
| [Références hiérarchisées](../REFERENCES_HIERARCHISEES.md) | Les 177 références par rôle ; celles à vérifier en priorité. |
| Indicateur, navigateur, graphe des idées | L'évaluation, les actions et Bellman, les dépendances (menu du portail). |
| `1_Presentation/articles/` et `relecture/` | Les trois articles (anglais) et le dossier à envoyer à un spécialiste. |
| [Guide pour une IA](../GUIDE_POUR_UNE_IA.md) | Le mode d'emploi à donner à une autre IA, avec la procédure pour proposer les prochaines étapes. |

Pour un premier parcours : ce document, puis le [guide de lecture intuitif](07_GUIDE_DE_LECTURE_INTUITIF.md), puis le document 28 (le Modèle réduit) et le document 80 (d'où vient le signe). Le document 06 raconte le chemin jusqu'à la V6.24, erreurs comprises.

Le travail a été mené avec l'aide de ChatGPT (OpenAI) et de Claude (Anthropic) pour l'exploration, le code, la recherche bibliographique et la rédaction. L'auteur assume la responsabilité finale du contenu.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [BBLM06] E. Bogomolny, O. Bohigas, P. Leboeuf, A. G. Monastra. *On the spacing distribution of the Riemann zeros: corrections to the asymptotic result*. J. Phys. A 39 (2006), 10743–10754 ; arXiv:math/0602270. <https://arxiv.org/abs/math/0602270> — vérifié en ligne
- [Cra22] H. Cramér. *Ein Mittelwertsatz in der Primzahltheorie*. Math. Z. 12 (1922), 147–153. — partiellement vérifié
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [KS99] N. M. Katz, P. Sarnak. *Zeroes of zeta functions and symmetry*. Bull. Amer. Math. Soc. 36 (1999), 1–26 ; voir aussi le livre Random Matrices, Frobenius Eigenvalues, and Monodromy, AMS Colloq. Publ. 45 (1999). <https://www.ams.org/bull/1999-36-01/S0273-0979-99-00766-1/> — vérifié en ligne
- [Mon73] H. L. Montgomery. *The pair correlation of zeros of the zeta function*. Analytic Number Theory, Proc. Sympos. Pure Math. 24, AMS (1973), 181–193. <https://public.websites.umich.edu/~hlm/paircor1.pdf> — vérifié en ligne
- [MT58] A. Mattuck, J. Tate. *On the inequality of Castelnuovo–Severi*. Abh. Math. Sem. Univ. Hamburg 22 (1958), 295–299 (volume et pages non confirmés en ligne). <https://arxiv.org/abs/1210.7459> — partiellement vérifié
- [Sel56] A. Selberg. *Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series*. J. Indian Math. Soc. 20 (1956), 47–87. <https://informaticsjournals.com/index.php/jims/article/view/16985> — partiellement vérifié
- [SW09] É. Saias, A. Weingartner. *Zeros of Dirichlet series with periodic coefficients*. Acta Arith. 140 (2009), no. 4, 335–344 ; DOI 10.4064/aa140-4-4 ; arXiv:0807.0783. <https://arxiv.org/abs/0807.0783> — vérifié en ligne
- [Wei48] A. Weil. *Sur les courbes algébriques et les variétés qui s'en déduisent*. Actualités Sci. Ind. 1041, Hermann, Paris (1948). <https://denisevellachemla.eu/Weil-courbes-varietes.pdf> — partiellement vérifié. **Correctif V6.18 :** Le mémoire Sur les courbes… établit directement la positivité par correspondances, intersections et Riemann–Roch. La fiche précédente le résumait trop exclusivement par la jacobienne ; ne pas confondre ce mémoire et celui sur les variétés abéliennes.
- [Zhu26] X. Zhu. *Weil positivity in compact windows: a finite reduction, certified two-sided bounds, and a Landau–Widom decay law*. arXiv:2608.24827 (v2, sept. 2026). <https://arxiv.org/abs/2608.24827> — vérifié en ligne. **Correctif V6.18 :** λ*(L) est un infimum variationnel sur toutes les fonctions test de support [−L, L] ; la plus petite valeur propre d'une matrice de Weil de taille finie en est un majorant (Zhu, remarque 2.2).

<!-- references:fin -->
