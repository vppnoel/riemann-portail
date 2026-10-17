# V6.25 — Les unités fictives : audit du document reçu

**Date :** 11 octobre 2026  
**Statut :** audit d'un document reçu de l'auteur le 11 octobre 2026, à 0 h 44 : « Unités fictives et bilan d'énergie du corpus RH ». Le texte a été écrit sur la base V6.21 ; son origine n'est pas précisée. Les fichiers d'origine sont conservés sans modification dans `4_Archives/recus/Unites_fictives_RH/`. Il ne contient pas d'erreur, et tous ses calculs ont été reproduits. Il n'apporte pas de contrainte nouvelle sur les zéros, mais il propose une lecture mécanique cohérente du corpus.  
**Demande de l'auteur :** l'idée des « dimensions fictives » appliquée au Théorème A (message de 0 h 11), puis l'envoi de ce document.

## 1. Ce que propose le document

Il donne des **unités** aux objets du corpus : une masse u~M~, une longueur u~L~ et un temps u~T~. Ensuite, il garde ces unités dans tous les calculs. Trois lectures en découlent :

1. **La métrique devient une matrice de masses**, M = m~0~ G. Une valeur propre négative de G devient une masse négative, donc une énergie négative dans cette direction.
2. **L'énergie Q devient l'énergie cumulée d'un mobile.** Le temps est τ = τ~0~ log x et la vitesse v = v~0~ C(x)/√x. Entre deux entiers, le mobile se décharge : v̇ = −v/(2τ~0~). À chaque entier n, il reçoit une impulsion J~n~ ∝ c(n)/√n.
3. **Un bilan exact** relie le stock d'énergie K = C(N)²/N, l'énergie cumulée Q(N) et le travail total des impulsions :

  K + Q(N) = Σ~2≤n≤N~ W~n~,  avec W~n~ = (2C(n−1)c(n) + c(n)²)/n.

## 2. Vérifications

| Point | Vérification | Résultat |
|---|---|---|
| Reproduction | script relancé tel quel, en lecture seule, sur le corpus V6.24 | bilan et impulsions identiques (écart 0) ; métrique identique à 10^−6^ près relatif, sur des valeurs propres de l'ordre de 10^−12^ (bruit numérique) |
| Q(10⁴), Q(10⁵) | comparés au calcul indépendant de la V6.20 (doc. 45) | 27,027234 et 60,494067 : identiques |
| Formules de la décharge | dérivation à la main | P = K/τ~0~, v̇ = −v/(2τ~0~), K̇ = −K/τ~0~ : **exactes** |
| Bilan K + Q = Σ W~n~ | vérifié en nombres rationnels exacts sur des suites quelconques | **exact**, pour toute suite c. C'est une **sommation par parties** (Abel) : W~n~ = (C(n)² − C(n−1)²)/n. |
| Masses négatives | comparées au doc. 46 | DH : 2 puis 10, comme les directions positives en trop de la surface virtuelle ; ζ et L(χ5) : aucune |
| Théorèmes A et B en unités | analyse dimensionnelle | taux (2Θ − 1)/τ~0~ et E~Q~ ∼ E~0~ (S/3)(T/τ~0~)³ : **cohérents** |

Le document est honnête sur ses limites. Il précise que le seuil des valeurs propres est numérique et non certifié, et qu'une équivalence intégrée ne donne pas d'équivalence ponctuelle.

## 3. Ce que cela apporte, et ce que cela n'apporte pas

**Un dictionnaire de plus.** La même quantité porte désormais trois noms :

| Corpus | Surface virtuelle (doc. 46) | Unités fictives |
|---|---|---|
| valeur propre négative de la métrique | direction positive en trop de la forme d'intersection | masse négative |
| RH (Weil) | indice de Hodge = 1 | toutes les masses positives |

**L'analyse dimensionnelle répond à votre question sur les « dimensions nécessaires ».** Dans le Théorème A, le seul nombre sans unité qui reste est 2Θ − 1, c'est-à-dire le taux d'amplification multiplié par τ~0~. RH dit que ce taux est nul. Les unités montrent *quelle* grandeur doit s'annuler, mais elles ne disent pas *pourquoi*. C'est la conclusion du doc. 48, §5 : la dimension nécessaire est intrinsèque, et aucune unité ni dimension fictive ne peut la fixer.

**Pas de contrainte nouvelle.** Le bilan est une identité, vraie pour n'importe quelle suite c(n) : il ne contient pas d'information sur les zéros. Le document conclut qu'il faudrait « borner le travail total des impulsions ». Or le travail total vaut K + Q, et borner Q, c'est RH (Théorème A). C'est le même mur que dans toutes les attaques d'OpenAI : tout revient à Q (doc. 13).

La forme du bilan montre quand même où se trouve la difficulté. Le travail d'une impulsion est la somme de deux termes :

- un carré, c(n)², toujours positif ;
- un terme d'interaction, 2C(n−1)c(n), dont le signe varie. Sur les 10⁵ premiers entiers, 21 457 impulsions ont un travail négatif : l'impulsion freine le mobile.

RH revient à dire que ces freinages compensent assez les accélérations.

**Lien avec la piste actuelle.** Le §2 du document écrit la puissance P~G~ = ½ v*(A*M + MA)v et le « bilan dissipatif » A*M + MA ≤ 0. C'est exactement le Hilbert–Pólya dissipatif d'OpenAI (piste OA07), qui retombe sur la positivité de Weil (docs 09, 36). Pour que toutes les masses soient positives, il faudrait une structure qui l'impose. Dans le Modèle réduit, cette structure est la surface, et la surface tient grâce au Frobenius (docs 46 à 49). Les unités fictives donnent un nom mécanique au lemme manquant. Elles n'en fournissent pas la preuve.

## 3 bis. Redécouverte

Le bilan d'énergie est la sommation par parties d'Abel appliquée à Q. Le corpus utilisait déjà la forme Q(N) = Σ C(k)²/(k(k+1)) dans ses calculs, depuis la V5.6 (script `run_pole_cancellation.py`) et encore en V6.20.

## 4. Démontré, mesuré, supposé

| | Énoncé |
|---|---|
| **Démontré** | Le bilan K + Q = Σ W~n~ (sommation par parties) ; les lois de décharge ; la cohérence dimensionnelle des Théorèmes A et B. |
| **Mesuré** | 21 457 impulsions de travail négatif sur 10⁵ ; masses négatives : 0 pour ζ et L(χ5), 2 puis 10 pour DH (identique au doc. 46). |
| **Supposé** | Rien de nouveau : « toutes les masses positives » est RH, sous un autre nom. |

## 5. Lecture selon l'hypothèse de travail

La lecture mécanique rend l'hypothèse de l'auteur concrète. Le mobile reçoit des impulsions des nombres premiers et se décharge entre elles. Pour que son énergie ne croisse pas exponentiellement, il faut que les impulsions se compensent. Or rien, dans les impulsions prises une à une, ne l'impose. Si une telle contrainte existe, elle vient de plus haut que les impulsions elles-mêmes : d'une structure qui fixerait le signe de toutes les masses à la fois.
