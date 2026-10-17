# Programme Riemann — Synthèse

*Mis à jour en V6.24, 11 octobre 2026 (précédente mise à jour : V6.18) ; version d'origine : synthèse de la version 5.1 (octobre 2026). État décrit : V6.24.*

**Date :** 10 octobre 2026  
**Statut :** l'essentiel en trois pages, pour un lecteur qui découvre le programme. Remplace la synthèse 5.1. Les détails sont dans les documents 26 à 41 de `1_Presentation/`.

> **À retenir**
>
> - Aucune preuve de l'hypothèse de Riemann (RH) n'est revendiquée. Les résultats ci-dessous sont présentés pour ce qu'ils sont.
> - Trois énoncés démontrés (Théorèmes A et B, corollaire B′), pré-relus en interne en V6.13. Aucun spécialiste ne les a encore relus.
> - Depuis la V6, le programme cherche ce qui rendrait RH nécessaire, et mesure les traces de cette chose là où elle existe (le Modèle réduit) puis du côté de ζ.
> - Chaque coup récent écrit sa prévision avant le calcul. Plusieurs prévisions ont été fausses, et les documents le disent.

## 1. La question et l'hypothèse de travail

**La question de départ.** On associe aux nombres premiers une quantité Q(X), une somme de carrés construite pour que chaque zéro de la fonction ζ de Riemann devienne un pôle double. Sa vitesse de croissance dit à quelle distance de la droite critique se trouve le zéro le plus éloigné. Les versions 1 à 5 ont établi et contrôlé cette reformulation.

**L'hypothèse de travail de l'auteur.**

> *RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand qui la rend nécessaire.*

Là où un analogue de RH est démontré, la preuve passe par une positivité sur un objet plus grand que la fonction elle-même : la surface C × C pour les courbes sur les corps finis (Weil, 1948 [Wei48]), un espace de Hilbert pour la fonction zêta de Selberg (Selberg, 1956 [Sel56]). Pour ζ, cet objet n'est pas construit. Le programme ne l'attaque pas de front. Il pose trois questions plus petites : quelle est la signature d'une nécessité démontrée ? ζ la présente-t-elle ? Que manque-t-il ?

## 2. Ce qui est démontré

Les énoncés exacts sont dans le document 37 et dans le dossier `1_Presentation/relecture/` (en anglais, avec un résumé français par résultat).

| | Énoncé | Statut | Pré-relecture V6.13 |
|---|---|---|---|
| **Théorème A** | Avec C(x) = Σ~n≤x~ c(n), c = Λ∗Λ − Λ·log + 2γΛ, et Q(X) = ∫~1~^X^ \|C(x)\|² x^−2^ dx : ½·limsup log(1+Q(X))/log X = Θ − ½, où Θ est la plus grande partie réelle des zéros. Donc RH ⟺ Q(X) = X^o(1)^. | Démontré, sans hypothèse. Équivalent à RH : une reformulation, pas une étape vers RH. | Correct après trois retouches. Méthode standard : à présenter comme une proposition. |
| **Théorème B** | Sous RH, Q(X) ∼ (S/3)(log X)³, avec S = Σ~ρ~ m²(m+1)²/\|ρ\|². Pour des zéros simples, S = 4κ, κ = 2 + γ − log 4π. | Démontré sous RH. | Correct après quatre retouches. Transposition au pôle double du théorème de Cramér [Cra22] ; énoncé non trouvé tel quel. |
| **Corollaire B′** | Sous RH, Q(X)/(log X)³ → 4κ/3 si et seulement si tous les zéros de ζ sont simples. | Démontré en quelques lignes. | Nouveau à notre connaissance ; à faire vérifier. |

La pré-relecture a été faite par trois relectures indépendantes entre elles, mais menées par des modèles de la même famille que ceux qui ont aidé à écrire les preuves. Elle ne remplace pas un spécialiste.

D'autres énoncés, plus courts, sont démontrés dans les documents récents : la rigidité au premier ordre aux points d'Euler (document 30 ; le corollaire « RH implique le produit d'Euler » y est un cas particulier de Saias–Weingartner [SW09], 2009), le lemme d'inertie (document 38), l'identité entre la marge locale et la corrélation de paires (document 40), le Contour tourné et les identités de la marge (document 41).

## 3. Ce qui est mesuré de plus solide

Toutes ces mesures sont reproductibles : données, scripts et 158 tests (tous exécutés et réussis en V6.17).

| Résultat (document) | Ce qui est mesuré | Chiffres clés |
|---|---|---|
| **Modèle réduit** (28, 29) | Sur les courbes sur les corps finis, où RH est un théorème : l'équation fonctionnelle et un produit d'Euler positif ne suffisent pas ; la positivité de Castelnuovo [MT58], étage par étage, démasque les faux. | 425 courbes, positivité exacte jusqu'à l'étage 60 ; 220 faux jumeaux démasqués à un étage fini. |
| **Archipel d'Euler** (30) | Parmi les fonctions qui ont la même équation fonctionnelle, RH ne survit qu'autour des points d'Euler, dans des îles qui rétrécissent avec la hauteur. | 27 îles ; rayon médian 0,091 (\|t\| ≤ 25) puis 0,008 (\|t\| ≤ 300) ; pente −0,77. |
| **Générateur des premiers** (33) | L'opérateur de ζ se reconstruit avec les seuls nombres premiers. Sa métrique est positive pour ζ et L(s, χ~5~), négative pour Davenport–Heilbronn [DH36b] [DH36a] (DH) exactement à ses zéros hors droite. | 226 zéros avec les premiers ≤ 439 ; 284 avec ≤ 23 862 ; aucune fausse détection dans la fenêtre principale. |
| **Temps de Heisenberg** (38) | Un quadruplet de zéros hors droite s'entend dès que la fenêtre atteint log(q·γ~0~/2π). | Rapport 0,95–1,08 pour ζ et L ; 0,80–0,89 pour DH. |
| **Degré 2** (39, 41) | L(Δ, s) de Ramanujan [Ram16], reconstruite depuis les τ(n), se comporte comme ζ : même loi de seuil (elle double), même répulsion. | Zéros à 1,2·10^−9^ près ; L~c~/Ω = 1,02–1,05 ; 2 139 zéros jusqu'à 1 500 par le Contour tourné. |
| **Rencontre à trois** (40) | RH, simplicité des zéros et répulsion se lisent sur une même quantité : la marge locale 1 − sinc²(πs), qui est la corrélation de paires de Montgomery (1973) [Mon73]. | 1 070 zéros de ζ : 4 marges < 0,1, contre 13 attendues (GUE) et 320 (Poisson) ; paire de Lehmer [Leh56] : marge 0,006. |
| **Loi de la marge** (41) | Partout où une loi est démontrée (Weyl, Sato–Tate, Dyson), la fréquence d'une configuration est proportionnelle à la marge qu'elle laisse à la métrique. Les zéros de ζ et de Δ la suivent, avec un déficit à basse hauteur. | Δ : 8 marges < 0,1 (GUE 26 ; Poisson 641) ; ζ·L(χ~5~) : aucune répulsion entre les deux familles ; Sato–Tate sur 561 258 courbes ; collisions de l'étage 2 = 18 338 courbes supersingulières. |

La lecture qui relie ces mesures est la suivante. ζ présente toutes les signatures observables d'une nécessité démontrée, sauf l'objet qui la porte (document 28). Ce qui manque n'est pas l'opérateur, qu'on sait reconstruire : c'est une métrique positive imposée, et non seulement mesurée (documents 32 et 33).

## 4. Ce qui reste supposé

- Qu'un objet plus grand porte la positivité de ζ, comme la surface C × C le fait pour les courbes. C'est l'hypothèse de travail elle-même.
- Que ce même objet impose aussi la loi de la marge entre les zéros, comme le groupe de monodromie le fait sur les corps finis (Katz–Sarnak, 1999 [KS99]).
- Que les îles de l'Archipel se referment jusqu'à zéro à grande hauteur.
- Que le seuil au temps de Heisenberg s'explique par le noyau reproduisant d'une mesure discrète (heuristique).
- Que le déficit de petites marges vienne de la hauteur finie (Bogomolny et al., 2006 [BBLM06]), avec une taille effective Λ~Δ~ entre 2,8 et 5,1.
- Que le facteur 0,8–0,9 de DH vienne de la statistique de ses zéros.

### Démontré, mesuré, supposé

| | Contenu |
|---|---|
| **Démontré** | Théorèmes A et B, corollaire B′ (pré-relus, non relus par un spécialiste) ; rigidité au premier ordre dans l'Archipel ; lemme d'inertie ; marge locale = corrélation de paires ; Contour tourné ; marge totale = densité de Weyl [Wey39]. Cités : Weil [Wei48], Deligne (1974) [Del74], Sato–Tate (2011) [BGHT11], Saias–Weingartner (2009). |
| **Mesuré** | Modèle réduit, Archipel d'Euler, générateur des premiers, temps de Heisenberg, degré 2, Rencontre à trois, Loi de la marge (§3). Hauteurs basses : ζ et Δ jusqu'à 1 500, DH jusqu'à 1 700. Contrôles par mpmath et par la méthode de Turing (1953) [Tur53]. |
| **Supposé** | Tout le §4. |

Plusieurs résultats classiques sont cités de mémoire ; chaque document le signale.

## 4 bis. Depuis la V6.18 : la géométrie virtuelle et ce qui manque (V6.19–V6.24)

| Version | Ce qui a été fait | Statut |
|---|---|---|
| V6.19 | La marge d'un groupe de n zéros est leur corrélation à n points (matrices unitaires aléatoires) ; les triplets de ζ suivent le noyau sinus (doc. 43) ; plan de recherche ; matrice des théories (doc. 44). | identité démontrée ; triplets mesurés |
| V6.20 | Le palier « 4/3 » recalculé jusqu'à 5·10⁶ : 0,985 × 4/3 en médiane, avec des pics ; quatorze résultats retrouvés ici puis reconnus dans la littérature (doc. 45). | mesuré ; correctif |
| V6.21 | La marge du corpus est, au signe près, la forme d'intersection d'une surface : indice de Hodge vérifié dans le Modèle réduit (425 courbes), violé exactement par les 220 faux jumeaux ; pour ζ, la « surface virtuelle » calculée depuis les premiers a la bonne signature (doc. 46). | dictionnaire classique (Weil, Bombieri, Connes), mesures nouvelles |
| V6.22 | Parmi les propriétés démontrées sans RH, seule la fonction auxiliaire de Stepanov (avec le tordu) démasque tous les faux jumeaux ; Clifford n'en démasque aucun. Le lemme manquant pour ζ est formulé (doc. 47). | mesuré ; formulation |
| V6.23 | La fonction auxiliaire n'existe qu'avec le Frobenius : l'identité et une permutation échouent (doc. 48). | mesuré |
| V6.24 | Analyse de risques ; J3 simplifié : ce qui compte est la présence de x^p^ dans l'espace des fonctions ; le calcul des deux tiers d'Alpöge–Furman refait sur nos zéros : 56 % à la fenêtre démontrée (doc. 49). | mesuré |

**Le lemme manquant, en une phrase.** Pour ζ, on sait déjà que les comptages sont positifs, que ζ n'a pas de zéro réel entre 0 et 1, et qu'une borne des nombres premiers d'un seul côté suffirait à RH (Landau). Riemann–Roch existe pour Spec Z (Connes–Consani). Il manque un « Frobenius absolu » qui rendrait possible une fonction auxiliaire aux nombres premiers, comme x^p^ la rend possible sur une courbe.

## 5. L'indicateur à la V6.24, et le prochain coup

L'indicateur place le programme sur une échelle de 0 (rien) à 9 (résolu). Les niveaux n'ont pas bougé depuis la V6.18 : les versions V6.19 à V6.24 ont précisé ce qui manque, sans franchir de niveau.

| Dimension | V5 (5 oct.) | V6.24 (11 oct.) | Niveau atteint |
|---|---:|---:|---|
| Voir | 4 | 4 | Mesure robuste |
| Comprendre | 3 | 5 | Mécanisme compris, dans un cas où RH est démontrée |
| Situer | 3 | 6 | Énoncé démontré |
| Étendre au degré 2 | 0 | 4 | Mesure robuste |
| Démontrer, faire relire | 6 | 6 | Énoncé démontré |
| La case vide | 2 | 4 | Mesure robuste |
| Croiser | 0 | 6 | Énoncé démontré |

Aucune dimension n'atteint 7 (« Relu ») : il faut un lecteur humain.

**Les prochains coups (analyse de risques, doc. 49).** On creuse l'axe J par petites étapes : J3b, une lecture ciblée de Connes–Consani pour savoir si leur Frobenius de caractéristique un fournit une fonction « invisible aux dérivations » pour tous les premiers à la fois. En parallèle, on fait l'axe A, la Rencontre à n en hauteur, qui est sûr. J3 complet ne se lance que si J3b réussit. Le coup le plus rentable reste humain : faire relire les Théorèmes A et B.

## 6. Comment lire le corpus

| Entrée | À quoi elle sert |
|---|---|
| `00_PORTAIL.html` | La page d'entrée : où on en est, les dernières étapes, tous les documents. |
| `00_Carte_des_idees.html` | Les idées par thème, avec le statut de chacune et ses documents. |
| `1_Presentation/31_INDICATEUR_D_AVANCEMENT.html` | Les étapes franchies, version par version, sur l'échelle de 0 à 9. |
| `1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html` | La recherche comme itinéraire : position, opérateurs (les métaphores du registre, document 20), coups classés, prochain coup. |
| `1_Presentation/42_REGISTRE_DES_SOURCES.md` | Le registre des sources : chaque clé entre crochets, par exemple [Del74], renvoie à la référence complète, à un lien et à ce qui a été vérifié. |
| `1_Presentation/relecture/` | Le dossier à envoyer à un spécialiste ; on l'ouvre par `00_READ_ME_FIRST_EN.md`. |
| `3_Preuves_et_calculs/` | Preuves, code, données, tests (`python tests/run_all_tests.py`). |

Pour un premier parcours : ce document, puis le portail, puis le document 28 (le Modèle réduit) et le document 41 (la dernière étape). Le document 06 raconte le chemin, erreurs comprises.

Le travail a été mené avec l'aide de ChatGPT (OpenAI) et de Claude (Anthropic) pour l'exploration, le code, la recherche bibliographique et la rédaction. L'auteur assume la responsabilité finale du contenu.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [BBLM06] E. Bogomolny, O. Bohigas, P. Leboeuf, A. G. Monastra. *On the spacing distribution of the Riemann zeros: corrections to the asymptotic result*. J. Phys. A 39 (2006), 10743–10754 ; arXiv:math/0602270. <https://arxiv.org/abs/math/0602270> — vérifié en ligne
- [BGHT11] T. Barnet-Lamb, D. Geraghty, M. Harris, R. Taylor. *A family of Calabi–Yau varieties and potential automorphy II*. Publ. RIMS 47 (2011), 29–98 ; DOI 10.2977/PRIMS/31. <https://ems.press/journals/prims/articles/4468> — vérifié en ligne
- [Cra22] H. Cramér. *Ein Mittelwertsatz in der Primzahltheorie*. Math. Z. 12 (1922), 147–153. — partiellement vérifié
- [Del74] P. Deligne. *La conjecture de Weil. I*. Publ. Math. IHÉS 43 (1974), 273–307 ; DOI 10.1007/BF02684373. <https://www.numdam.org/item/PMIHES_1974__43__273_0/> — vérifié en ligne
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [KS99] N. M. Katz, P. Sarnak. *Zeroes of zeta functions and symmetry*. Bull. Amer. Math. Soc. 36 (1999), 1–26 ; voir aussi le livre Random Matrices, Frobenius Eigenvalues, and Monodromy, AMS Colloq. Publ. 45 (1999). <https://www.ams.org/bull/1999-36-01/S0273-0979-99-00766-1/> — vérifié en ligne
- [Leh56] D. H. Lehmer. *On the roots of the Riemann zeta-function*. Acta Math. 95 (1956), 291–298. <https://en.wikipedia.org/wiki/Lehmer_pair> — partiellement vérifié
- [Mon73] H. L. Montgomery. *The pair correlation of zeros of the zeta function*. Analytic Number Theory, Proc. Sympos. Pure Math. 24, AMS (1973), 181–193. <https://public.websites.umich.edu/~hlm/paircor1.pdf> — vérifié en ligne
- [MT58] A. Mattuck, J. Tate. *On the inequality of Castelnuovo–Severi*. Abh. Math. Sem. Univ. Hamburg 22 (1958), 295–299 (volume et pages non confirmés en ligne). <https://arxiv.org/abs/1210.7459> — partiellement vérifié
- [Ram16] S. Ramanujan. *On certain arithmetical functions*. Trans. Cambridge Philos. Soc. 22 (1916), 159–184. <https://encyclopediaofmath.org/wiki/Ramanujan_function> — partiellement vérifié
- [Sel56] A. Selberg. *Harmonic analysis and discontinuous groups in weakly symmetric Riemannian spaces with applications to Dirichlet series*. J. Indian Math. Soc. 20 (1956), 47–87. <https://informaticsjournals.com/index.php/jims/article/view/16985> — partiellement vérifié
- [SW09] É. Saias, A. Weingartner. *Zeros of Dirichlet series with periodic coefficients*. Acta Arith. 140 (2009), no. 4, 335–344 ; DOI 10.4064/aa140-4-4 ; arXiv:0807.0783. <https://arxiv.org/abs/0807.0783> — vérifié en ligne
- [Tur53] A. M. Turing. *Some calculations of the Riemann zeta-function*. Proc. London Math. Soc. (3) 3 (1953), 99–117. <https://en.wikipedia.org/wiki/Turing%27s_method> — partiellement vérifié. **Correctif V6.18 :** Le corpus applique une forme simple (contrôle empirique de S(t)) de la méthode de Turing ; la méthode certifiée utilise une borne explicite sur ∫S(t)dt et les points de Gram.
- [Wei48] A. Weil. *Sur les courbes algébriques et les variétés qui s'en déduisent*. Actualités Sci. Ind. 1041, Hermann, Paris (1948). <https://denisevellachemla.eu/Weil-courbes-varietes.pdf> — partiellement vérifié. **Correctif V6.18 :** Le mémoire Sur les courbes… établit directement la positivité par correspondances, intersections et Riemann–Roch. La fiche précédente le résumait trop exclusivement par la jacobienne ; ne pas confondre ce mémoire et celui sur les variétés abéliennes.
- [Wey39] H. Weyl. *The Classical Groups: Their Invariants and Representations*. Princeton University Press (1939). <https://press.princeton.edu/books/paperback/9780691057569/the-classical-groups> — partiellement vérifié

<!-- references:fin -->
