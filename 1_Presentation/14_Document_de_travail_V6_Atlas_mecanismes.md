# Programme Riemann — Version 6
## Document de travail : Atlas des mécanismes critiques de ζ

**Date :** 5 octobre 2026  
**Statut :** document exploratoire de travail — aucune revendication de preuve de RH  
**Origine :** transition méthodologique après la clôture V5.8 du volet « cibles »

---

## 0. Objet de la V6

La V5.8 a clarifié un point décisif : accumuler des reformulations équivalentes de RH ou des énergies positives par construction ne suffit pas. Le verrou n'est pas seulement de trouver une nouvelle quantité ; il faut trouver une **structure qui porte une information arithmétique discriminante**.

La V6 change donc volontairement de question.

Au lieu de demander en permanence :

> « Cette idée prouve-t-elle que tous les zéros sont sur la droite critique ? »

on demandera :

> **« Quel mécanisme cette idée révèle-t-elle, que conserve-t-elle, que détruit-elle, et avec quels autres mécanismes peut-elle être recombinée ? »**

L'objectif n'est pas de réduire la rigueur, mais d'augmenter l'espace de recherche sans transformer l'exploration en analogie incontrôlée.

La règle centrale de la V6 est donc :

> **Divergence conceptuelle forte, validation mathématique stricte.**

Une métaphore n'a de valeur que si elle conduit à un objet exact, un observable calculable ou démontrable, un témoin négatif et une règle d'arrêt.

---

# 1. Changement de cadre : de « preuve de RH » à « atlas de mécanismes »

Le programme est réorganisé autour de quatre grands continents conceptuels.

### A. Hasard arithmétique

La fonction de Möbius et les fonctions multiplicatives sont considérées comme des signaux où l'on cherche à comprendre **où apparaît la cancellation**, à quelles échelles, et sous quelles formes statistiques.

Précision : RH n'affirme pas littéralement que

\[
M(x)=\sum_{n\le x}\mu(n)=O(\sqrt{x}),
\]

mais elle équivaut à

\[
M(x)=O_\varepsilon(x^{1/2+\varepsilon})
\quad\text{pour tout }\varepsilon>0.
\]

L'image « pile ou face » est donc une heuristique de cancellation à l'échelle racine carrée, pas un modèle probabiliste exact.

### B. Structure / géométrie

Sur les corps finis, la localisation des zéros est forcée par une architecture géométrique et cohomologique. Pour ζ, plusieurs programmes cherchent l'objet manquant : géométrie non commutative, cohomologie, espaces adéliques, géométries de type « corps à un élément », etc.

La V6 n'essaiera pas de construire directement une « géométrie ultime ». Elle cherchera d'abord **ses empreintes nécessaires**.

### C. Collectif / familles

Un objet individuel peut être opaque alors qu'une population d'objets révèle des symétries stables. Les familles de fonctions L et la théorie des matrices aléatoires montrent la puissance de ce changement d'échelle.

La V6 distinguera donc systématiquement :

- propriétés individuelles ;
- propriétés moyennes ;
- proportions ;
- distributions ;
- rangs effectifs et spectres statistiques.

### D. Criticité

La constante de de Bruijn–Newman [DeB50] [New76] transforme RH en une condition de seuil : Rodgers–Tao [RT20] ont montré \(\Lambda\ge 0\), tandis que RH équivaut à \(\Lambda\le0\). Ainsi RH équivaut à \(\Lambda=0\).

La question conceptuelle devient :

> **Quel mécanisme pourrait forcer ζ à se trouver exactement au seuil critique ?**

Ici, la valeur \(1/2\) elle-même est imposée par la symétrie fonctionnelle ; ce qui serait « émergent » n'est pas le centre, mais la **criticité exacte**.

---

# 2. Atlas des mécanismes ayant résisté au programme

Les branches précédentes sont renommées non par le problème qu'elles devaient résoudre, mais par **ce qu'elles font réellement**.

| Nom V6 | Objet mathématique | Métaphore | Ce qui a réellement porté | Nouvelle question |
|---|---|---|---|---|
| **Le miroir de Möbius** | \(1/\zeta(s)=\sum \mu(n)n^{-s}\) | Deux faces d'un même paysage : zéros / cancellation | Les zéros peuvent être reformulés comme lois de fluctuation arithmétique | Où la cancellation cesse-t-elle d'être aléatoire ? |
| **Le filtre antipôle** | \(W_N(1)=0\) | Filtre notch supprimant une fréquence cohérente | La projection énergétique s'est presque réduite à l'annulation du mode \(s=1\) | Quels modes universels peut-on supprimer exactement avant d'étudier le résidu ? |
| **Le thermomètre d'horizon** | énergie \(Q\), exposant relié à \(\Theta=\sup \Re\rho\) | Un thermomètre mesure la température mais ne la crée pas | \(Q\) détecte une croissance liée au zéro le plus à droite | Quel objet conserve davantage d'information que la simple norme ? |
| **L'effaceur orthogonal** | projection Nyman–Beurling [Nym50] [Beu55] / Gram | Annulation adaptative d'un bruit structuré | Une direction structurée peut retirer une forte fraction du résidu fini | Quelles directions de faible dimension concentrent l'information ? |
| **La positivité porteuse** | forme hermitienne de Weil, signature, inertie | Une structure qui porte une charge | La positivité informative est différente d'une positivité automatique | Quelle positivité serait fausse pour un faux ζ ? |
| **Le census spectral** | rang, trace, inertie, proportions | Recenser plutôt que localiser chaque individu | Compter peut être beaucoup plus accessible que localiser tous les zéros | Quelles propriétés de RH admettent une version quantitative ou proportionnelle ? |
| **Le microscope de population** | familles de fonctions L | Épidémiologie plutôt qu'autopsie individuelle | Des symétries deviennent visibles après moyenne | Quelle propriété invisible pour ζ seule devient rigide dans une famille ? |
| **Le thermostat critique** | flot de de Bruijn–Newman | Chauffage/refroidissement jusqu'à une transition | RH devient « exactement au seuil » | Quel mécanisme épingle le seuil à zéro ? |
| **La scène manquante** | géométrie/cohomologie/trace | On voit la chorégraphie, pas encore le théâtre | La formule explicite ressemble à une formule de trace | Quel objet rendrait la positivité nécessaire plutôt que postulée ? |
| **Le jumeau de crash-test** | Davenport–Heilbronn [DH36b] [DH36a] et analogues | Même carrosserie analytique, moteur arithmétique différent | Détecte les critères trop universels | Toute nouvelle structure distingue-t-elle ζ d'un analogue sans produit d'Euler ? |
| **Les modes sombres** | observabilité/opérateurs | Un mode existe mais aucun capteur ne le voit | Les approches opératorielles butent sur la complétude/observabilité | Quel observable empêcherait un zéro hors ligne de rester invisible ? |
| **Le secteur sombre arithmétique** | information perdue par norme, moyenne ou projection | Une structure est inférée par plusieurs déformations du visible | Les réductions successives peuvent effacer précisément l'information discriminante | À quel étage d'observabilité ζ se sépare-t-elle irréductiblement de ses faux jumeaux ? |
| **La fermeture multiplicative** | défaut \(\Delta_F(m,n)\), bispectre/TOMO-3 | Une relation ternaire ferme les phases comme \(\log(mn)=\log m+\log n\) | TOMO-2 ne voit que la puissance ; TOMO-3 conserve un couplage de phase | La multiplicativité laisse-t-elle une empreinte ternaire mesurable ? |
| **La compression fertile** | compressions finies d'un objet infini | Biopsie informative | Une compression peut transformer une structure globale en borne quantitative | Quelle compression conserve l'information de signe utile ? |
| **Tomographie de cohérence TOMO-2** | Gram de translations logarithmiques | Scanner inter-échelles | Conserve covariance/spectre de puissance | Quelle cohérence survit au changement d'échelle ? |
| **Tomographie de phase TOMO-3** | tricorrélation / bispectre | Scanner de fermeture de phase | Conserve des couplages ternaires absents de TOMO-2 | Existe-t-il une fermeture de phase réellement arithmétique ? |
| **Flux d'inertie** | triplet \((n_+,n_-,n_0)\) | Suivre les directions de signe plutôt que chaque zéro | Rend le signe mesurable sous déformation | Quelle limite finie/infinie conserve une transition critique ? |
| **Géométrie par empreintes** | signatures, indices, dualités discriminantes | Reconstruire l'animal par ses traces | Cherche des propriétés nécessaires avant la géométrie | Quelle empreinte est spécifique à la structure arithmétique ? |
| **Census de Möbius** | covariances/rangs de blocs de \(\mu\) | Recenser une population de blocs | Mesure où la cancellation apparaît statistiquement | Quel invariant collectif dépasse les moyennes connues ? |
| **PRIME-LOCK / verrou premier** | \(-F'/F\), puissances de premiers, défaut de tour | Serrure locale eulérienne | Distingue l'Euler-produit local d'une superposition non multiplicative | Quelle information globale manque aux objets multiplicatifs aléatoires ? |
| **DUAL-LOCK / serrure à deux clés** | compression de la forme explicite : local + archimédien | Deux clés qui doivent s'emboîter | Teste intrinsèquement la compatibilité local/global | L'inertie finie voit-elle un défaut de compatibilité ? |
| **Le résidu sombre** | reliquat après cancellation des composantes local/global | Ce qui devient visible seulement après avoir soustrait le visible dominant | Quantifie où le signe final est porté par une petite différence | Quelles déformations changent le signe du résidu sans toucher les gros termes ? |

---

# 3. Ce que la V5.8 nous impose comme discipline

La V6 part de trois leçons négatives mais productives.

## 3.1 Une positivité automatique n'est pas une information

Si une quantité est positive parce qu'elle est une norme ou une somme de carrés, cette positivité peut ne rien dire sur la localisation des zéros.

Le test V6 sera :

> **La propriété de signe serait-elle encore vraie pour Davenport–Heilbronn ou pour un modèle artificiel qui viole RH ?**

Si oui, le signe n'est probablement pas le levier recherché.

## 3.2 Une norme détruit de l'information

Passer d'un signal \(C\) à

\[
Q=\|C\|^2
\]

supprime signe, phase, orientation et corrélations entre échelles.

La V6 privilégiera donc, lorsque cela est pertinent, des objets **polarisés, matriciels ou multicanaux** avant de les réduire à un scalaire.

## 3.3 Une équivalence n'est pas encore un mécanisme

Nyman–Beurling, Weil, Li, de Bruijn–Newman et d'autres cadres peuvent reformuler RH exactement. Une équivalence devient intéressante pour V6 seulement si elle fournit au moins l'un des éléments suivants :

- une variable que l'on peut déformer ;
- une signature ou une inertie ;
- une moyenne ou une proportion accessible ;
- un témoin négatif naturel ;
- une compression finie ;
- un observable nouveau.

---

# 4. Grammaire de divergence contrôlée

La V6 utilisera une grammaire explicite pour générer de nouvelles questions :

\[
\boxed{
\text{OBJET}
\xrightarrow{\text{OPÉRATION}}
\text{OBSERVABLE}
\xrightarrow{\text{CRASH-TEST}}
\text{QUESTION}
}
\]

## Opérations considérées comme particulièrement fertiles

- annuler ;
- centrer ;
- projeter ;
- polariser ;
- compresser ;
- déformer ;
- moyenner ;
- conditionner ;
- comparer adversarialement ;
- changer d'échelle ;
- remplacer un scalaire par une matrice ;
- remplacer un objet individuel par une population.

### Exemple 1 — Tomographie

\[
Q
\xrightarrow{\text{polariser}}
K_{ij}
\xrightarrow{\text{spectre}}
\zeta\;\text{vs}\;\text{Davenport–Heilbronn}.
\]

### Exemple 2 — Flux d'inertie

\[
H_t
\xrightarrow{\text{compresser}}
H_N(t)
\xrightarrow{\text{inertie}}
\text{transition à }t=0\;?
\]

### Exemple 3 — Census de Möbius

\[
\mu
\xrightarrow{\text{regrouper en blocs}}
\mathcal C
\xrightarrow{\text{rang effectif}}
\text{comportement sur intervalles courts}.
\]

---

# 5. Quatre programmes exploratoires V6

## V6-A — Flux d'inertie

### Croisement

**Thermostat critique + compression fertile + positivité porteuse.**

### Question

Existe-t-il une famille naturelle de compressions hermitiennes

\[
H_N(t)
\]

associée à une déformation de type de Bruijn–Newman, telle que l'on puisse suivre son inertie

\[
(n_+(t),n_-(t),n_0(t))
\]

et détecter un changement qualitatif à \(t=0\) ?

### Métaphore

**Flux d'inertie** : au lieu de suivre chaque zéro, on suit le nombre de directions positives, négatives et nulles d'une compression finie lorsque le système traverse le seuil.

### Prédiction minimale

Un invariant de signature doit varier de façon non triviale avec le paramètre de déformation et ne pas être déterminé par une positivité automatique.

### Témoin négatif

Construire la même compression pour une fonction analogue ne partageant pas la même criticité.

### Règle d'arrêt

Si l'inertie est constante, triviale ou déterminée par la seule symétrie fonctionnelle, la branche est fermée.

---

## V6-B — TOMO-DH : tomographie multiplicative inter-échelles **[priorité 1]**

### Croisement

**Thermomètre d'horizon + polarisation + jumeau de crash-test + fermeture multiplicative.**

### Correction conceptuelle acquise

La matrice de Gram d'ordre 2 ne peut pas être un détecteur de phase au sens strict. Après passage en coordonnées logarithmiques

\[
u=\log t,\qquad g_F(u)=e^{-u/2}C_F(e^u),
\]

on définit

\[
K^{(2)}_{ij}(F)=\langle T_{\tau_i}g_F,T_{\tau_j}g_F\rangle.
\]

Par Plancherel [Tit37],

\[
K^{(2)}_{ij}
=\frac1{2\pi}\int |\widehat g_F(\omega)|^2
 e^{i\omega(\tau_i-\tau_j)}\,d\omega.
\]

Ainsi TOMO-2 ne voit que le **spectre de puissance** : la phase de Fourier a disparu. Son rôle exact est donc la **cohérence inter-échelles d'ordre 2**, pas la « tomographie de phase ».

### TOMO-3 : récupération d'un couplage de phase

Pour conserver une information ternaire, on passe au bispectre

\[
\boxed{
B_F(\omega_1,\omega_2)=
\widehat g_F(\omega_1)
\widehat g_F(\omega_2)
\overline{\widehat g_F(\omega_1+\omega_2)}.
}
\]

Si \(\widehat g_F(\omega)=A_F(\omega)e^{i\phi_F(\omega)}\), alors

\[
\arg B_F=
\phi_F(\omega_1)+\phi_F(\omega_2)-\phi_F(\omega_1+\omega_2).
\]

TOMO-3 conserve donc un couplage de phase que TOMO-2 détruit.

### Étalon arithmétique : défaut multiplicatif

Pour

\[
F(s)=\sum_{n\ge1}a_F(n)n^{-s},\qquad a_F(1)=1,
\]

poser

\[
\boxed{\Delta_F(m,n)=a_F(mn)-a_F(m)a_F(n),\qquad (m,n)=1.}
\]

Pour \(\zeta\), \(\Delta_\zeta=0\) exactement. Pour Davenport–Heilbronn, qui satisfait une équation fonctionnelle de type Riemann mais n'a pas de produit d'Euler, le défaut est non nul.

### Principe de fermeture multiplicative

La relation

\[
a(mn)=a(m)a(n)
\]

se transforme sous le logarithme en

\[
\log(mn)=\log m+\log n.
\]

Le bispectre couple précisément des fréquences liées par

\[
\omega_3=\omega_1+\omega_2.
\]

Hypothèse de travail V6 :

> **Une structure multiplicative cohérente peut laisser, après représentation logarithmique adaptée, une signature ternaire plus rigide qu'une superposition non multiplicative.**

Cette hypothèse n'est ni un théorème ni une formulation de RH ; elle doit être falsifiée.

### Crash-tests obligatoires

- \(\zeta\) : multiplicativité + équation fonctionnelle ;
- un \(L(s,\chi)\) approprié : contrôle multiplicatif proche de DH ;
- Davenport–Heilbronn : équation fonctionnelle sans produit d'Euler ;
- signal de \(\zeta\) à phases Fourier randomisées : même spectre de puissance, phase détruite ;
- suite complètement multiplicative aléatoire : multiplicativité sans la structure analytique de \(\zeta\).

Test interne impératif : si \(|\widehat{\widetilde g}|=|\widehat g_\zeta|\), alors TOMO-2 doit donner le même résultat à effets de bord contrôlés, tandis que TOMO-3 doit généralement changer.

### Question minimale

\[
\boxed{
\text{Existe-t-il une relation mesurable entre }
B_F(\omega_1,\omega_2)
\text{ et }
\Delta_F(m,n)
\text{ après passage logarithmique ?}
}
\]

### Règle d'arrêt

Si TOMO-3 n'apporte aucune séparation au-delà du défaut multiplicatif explicite, ou si toute séparation disparaît sous randomisation/normalisation contrôlée, TOMO-DH est rétrogradée en représentation diagnostique.

## V6-C — Census de Möbius

### Croisement

**Miroir de Möbius + microscope de population + census spectral.**

### Changement de question

Au lieu de demander seulement si

\[
M(x)=\sum_{n\le x}\mu(n)
\]

est petit, étudier la structure collective des blocs de Möbius.

### Objet prototype

Pour des décalages \(h,k\), considérer une covariance de bloc du type

\[
\mathcal C_{h,k}(X,H)
=
\mathbb E_{x\sim X}
\left[
\mu(x+h)\mu(x+k)
\right]
\]

ou une variante rigoureusement compatible avec les résultats disponibles sur les intervalles courts.

### Observables

- spectre de la matrice de covariance ;
- rang effectif ;
- modes cohérents ;
- proportion de fenêtres atypiques ;
- stabilité par changement d'échelle.

### Métaphore

**Census de Möbius** : ne pas demander si chaque individu est « aléatoire », mais mesurer la structure de la population des blocs.

### Règle d'arrêt

Si les observables ne donnent rien de plus que les théorèmes de moyenne déjà connus, ou si l'information disparaît dès que l'on impose une définition asymptotiquement rigoureuse, la branche est classée descriptive.

---

## V6-D — Géométrie par empreintes

### Croisement

**Scène manquante + positivité porteuse + jumeau de crash-test.**

### Inversion de démarche

Ne pas commencer par inventer un analogue de

\[
\operatorname{Spec}\mathbf Z\times\operatorname{Spec}\mathbf Z.
\]

Commencer par demander :

> Quelles propriétés une telle géométrie devrait-elle nécessairement laisser dans la formule explicite ou dans les objets arithmétiques ?

### Méthode

Chercher des propriétés candidates :

- dualité ;
- signature ;
- indice ;
- convexité ;
- trace ;
- relation d'intersection ;
- contrainte de rang ;
- positivité non automatique.

Puis exiger qu'elles soient :

\[
\text{vraies pour }\zeta
\]

et

\[
\text{fausses ou différentes pour Davenport–Heilbronn}.
\]

### Métaphore

**Géométrie par empreintes** : reconstruire l'animal à partir de ses traces plutôt que dessiner l'animal d'abord.

### Règle d'arrêt

Toute propriété qui dépend seulement de l'équation fonctionnelle et non du produit d'Euler ou d'une structure arithmétique spécifique est insuffisamment discriminante.

---

## V6-E — DARK-ZETA : cartographie du secteur sombre arithmétique **[cadre transversal]**

### Nature de l'analogie

L'analogie avec la matière noire est **épistémologique et non ontologique**. Elle ne postule aucune « substance cachée » derrière \(\zeta\). Elle formalise une stratégie : une structure peut être absente de l'observable direct tout en étant inférée par plusieurs effets indépendants.

En cosmologie, la matière noire n'est pas observée par émission lumineuse ; sa distribution est reconstruite par ses effets gravitationnels sur des observables visibles. La transposition autorisée pour V6 est uniquement :

> **cartographier une information invisible par les déformations qu'elle impose à plusieurs observables visibles.**

### Hypothèse de perte d'information

Les formulations énergétiques/quadratiques peuvent échouer non parce que l'objet de départ est mauvais, mais parce que l'opération de réduction détruit précisément l'information discriminante :

\[
C\to |C|^2\to Q,
\qquad
\widehat g\to |\widehat g|^2\to K^{(2)},
\qquad
\text{objet individuel}\to\text{moyenne}.
\]

Norme, moyenne et covariance peuvent supprimer signe, phase, orientation, relations ternaires ou événements rares.

### Échelle d'observabilité

La V6 introduit une hiérarchie expérimentale :

\[
\boxed{
\text{niveau 1 : énergie}
\to
\text{niveau 2 : covariance}
\to
\text{niveau 3 : bispectre}
\to
\text{niveau 4 : polyspectres / relations multiplicatives}.
}
\]

La question n'est plus « quelle quantité vaut zéro sous RH ? », mais :

> **À quel premier étage d'observabilité \(\zeta\) devient-elle irréductiblement différente d'un faux jumeau qui partage ses propriétés superficielles ?**

### Réseau d'empreintes

Une hypothétique structure cachée \(S\) n'est recevable que si elle explique simultanément plusieurs empreintes indépendantes, par exemple :

\[
\begin{cases}
\text{fermeture multiplicative},\\
\text{cohérence TOMO-3},\\
\text{séparation }\zeta/\mathrm{DH},\\
\text{signature/inertie informative de Weil},\\
\text{criticité de Bruijn--Newman}.
\end{cases}
\]

Une construction qui n'explique qu'un seul phénomène est faible. Une même structure qui contraint plusieurs canaux indépendants mérite une investigation.

### Détecteurs DARK-ZETA

DARK-ZETA n'est pas une nouvelle théorie : c'est un protocole de détection multi-observable. Les premiers détecteurs sont :

1. **TOMO-2** — détecteur de cohérence d'ordre 2 ;
2. **TOMO-3** — détecteur de fermeture de phase ternaire ;
3. **défaut multiplicatif** \(\Delta_F\) — étalon arithmétique exact ;
4. **forme/inertie de Weil** — détecteur de signe non automatique ;
5. **flux critique** — détecteur potentiel de transition sous déformation ;
6. **census de Möbius** — détecteur statistique de structure collective.

### Principe de triangulation

Une empreinte DARK-ZETA n'est considérée sérieuse que si elle satisfait au moins deux conditions :

- elle est observée par des canaux mathématiquement distincts ;
- elle survit à des normalisations qui détruisent les effets triviaux ;
- elle distingue \(\zeta\) d'au moins un témoin adversarial ;
- elle admet une formulation analytique indépendante du réglage numérique.

### Interdictions

DARK-ZETA ne doit jamais servir de mot-valise pour « ce que nous ne comprenons pas ». Sont interdits :

- postuler une entité cachée parce qu'un calcul échoue ;
- appeler « secteur sombre » une simple variable omise ;
- interpréter une corrélation unique comme une cause ;
- transformer la métaphore cosmologique en affirmation physique sur \(\zeta\).

### Critère de réussite

Le meilleur résultat possible à court terme n'est pas de découvrir \(S\), mais de démontrer une implication du type

\[
\text{structure arithmétique A}
\Longrightarrow
\text{empreintes indépendantes B et C},
\]

avec échec de B/C chez Davenport–Heilbronn ou sous randomisation de phase.

### Position de TOMO dans DARK-ZETA

TOMO-DH devient le **premier détecteur** de la campagne DARK-ZETA. Le programme n'est plus « faire marcher TOMO coûte que coûte », mais utiliser TOMO pour tester l'hypothèse générale de perte d'information et décider rapidement à quel ordre les informations spécifiques à la multiplicativité deviennent visibles.

---

# 6. Protocole « thèse — antithèse — synthèse » pour chaque branche

Chaque idée V6 sera analysée par deux rôles explicites.

## Agent G — générateur

Mission : maximiser la divergence conceptuelle sous contrainte mathématique.

Il doit produire :

1. une reformulation inattendue ;
2. une analogie ;
3. un nouvel observable ;
4. une prédiction ;
5. une connexion à au moins un autre continent de l'atlas.

## Agent F — falsificateur

Mission : détruire l'idée aussi vite que possible.

Il doit rechercher :

1. circularité avec RH ;
2. positivité automatique ;
3. dépendance cachée aux zéros ;
4. équivalence déjà connue ;
5. absence de discrimination ζ / Davenport–Heilbronn ;
6. artefact de normalisation ou de taille finie ;
7. collision bibliographique.

## Synthèse

Une branche survit seulement si la synthèse peut formuler :

- un objet mathématique exact ;
- un test calculable ;
- une prédiction non triviale ;
- un témoin négatif ;
- une règle d'arrêt.

---

# 7. Fiche standard d'une métaphore V6

Chaque nouvelle intuition doit être enregistrée avec le template suivant.

## Nom

Nom court et mémorisable.

## Objet exact

Équation, fonction, forme, espace ou opérateur précis.

## Métaphore

Image mentale utilisée.

## Correspondance autorisée

Ce que l'analogie transporte réellement.

## Correspondance interdite

Ce que l'analogie ne permet **pas** de conclure.

## Nouvel observable

Nombre, matrice, forme quadratique, spectre, rang, inertie, distribution, etc.

## Prédiction

Phénomène concret attendu si l'idée contient une information réelle.

## Témoin négatif

Davenport–Heilbronn, modèle aléatoire, fonction synthétique ou autre analogue pertinent.

## Test de circularité

L'objet ou sa propriété utilise-t-il RH, un critère équivalent, des zéros supposés sur la droite ou une estimation qui implique déjà l'objectif ?

## Collision bibliographique

Existe-t-il déjà un objet mathématiquement équivalent sous un autre nom ?

## Règle d'arrêt

Résultat qui tue explicitement la piste.

## Statut

`IDÉE` · `FORMALISÉE` · `TESTÉE` · `SURVIT` · `RÉTROGRADÉE` · `FERMÉE`

---

# 8. Matrice de priorités V6

| Priorité | Branche | Coût initial | Falsifiabilité | Potentiel d'information nouvelle | Décision |
|---|---|---:|---:|---:|---|
| **P1** | DARK-ZETA / TOMO-DH (TOMO-2 → TOMO-3) | faible à moyen | très forte | moyen à élevé | **Lancer comme campagne multi-observable** |
| **P2** | Géométrie par empreintes | moyen | forte si témoin fixé | élevé mais spéculatif | **Lancer en parallèle bibliographique** |
| **P3** | Flux d'inertie | moyen à élevé | moyenne | élevé si construction canonique | **Prototype conceptuel** |
| **P4** | Census de Möbius | moyen | forte | surtout structurel | **Exploration secondaire** |

La priorité P1 ne signifie pas « plus proche de RH ». Elle signifie : **meilleur rapport entre coût, pouvoir de falsification et capacité à révéler une information absente de Q**.

---

# 9. Critères de succès de la V6

La V6 ne sera pas évaluée uniquement par « preuve / pas preuve ».

Un résultat V6 est considéré comme réel s'il produit au moins l'un des éléments suivants :

1. **un invariant nouveau ou une identité exacte** qui conserve une information perdue par Q ;
2. **un test discriminant** ζ / Davenport–Heilbronn démontré ou numériquement robuste puis expliqué analytiquement ;
3. **une compression finie canonique** dont la signature/rang/inertie porte une information arithmétique ;
4. **une impossibilité démontrée** fermant toute une classe de métaphores ou de constructions ;
5. **un pont exact** entre deux mécanismes jusque-là séparés ;
6. une reformulation qui transforme une question inaccessible en une suite de sous-questions falsifiables.

Une fermeture propre d'une branche compte comme progrès méthodologique si elle élimine une classe entière de raisonnements séduisants mais non informatifs.

---

# 10. Critères d'exclusion immédiate

Une idée est rejetée ou mise en quarantaine si elle satisfait l'un des critères suivants :

- métaphore sans objet mathématique exact ;
- observable défini à partir des zéros que l'on cherche à contraindre ;
- positivité vraie par définition et présentée comme information arithmétique ;
- ajustement post hoc sans prédiction hors échantillon ;
- reconstruction d'un critère déjà équivalent à RH sans mécanisme nouveau ;
- succès identique sur Davenport–Heilbronn ;
- paramètre choisi après inspection du résultat visé ;
- comportement uniquement numérique sans loi d'échelle stable ;
- vocabulaire physique utilisé au-delà de la correspondance mathématique démontrée.

---

# 11. Première expérience proposée : TOMO-DH

## But

Tester si une version polarisée/matricielle de l'énergie contient une information que la norme scalaire Q élimine.

## Étape 1 — définir les canaux

Construire plusieurs versions \(C_j\) du signal arithmétique existant par :

- fenêtres logarithmiques ;
- échelles différentes ;
- dérivées/poids déjà présents dans le programme ;
- canaux pair/impair ou archimédien/arithmetic si une séparation canonique existe.

Aucune séparation ne doit être choisie après inspection du résultat.

## Étape 2 — matrice de covariance

\[
K_{ij}(X)=\langle C_i,C_j\rangle_X.
\]

Calculer :

- valeurs propres ;
- conditionnement ;
- rang effectif ;
- vecteurs propres dominants ;
- invariants normalisés ;
- évolution avec \(X\).

## Étape 3 — témoin Davenport–Heilbronn

Construire le même objet, avec exactement les mêmes règles, pour le témoin négatif.

## Étape 4 — test aveugle

Chercher un invariant défini **avant** de regarder la séparation finale.

## Étape 5 — verdict

- **séparation stable + explication analytique possible** : branche maintenue ;
- séparation instable ou dépendante du réglage : diagnostic numérique seulement ;
- absence de séparation : branche fermée rapidement.

---

# 12. Positionnement par rapport aux travaux extérieurs

Les directions suivantes servent de repères, non de revendication de nouveauté.

### Matomäki [MRST26]–Radziwiłł

Leur travail sur les fonctions multiplicatives en intervalles courts montre que la cancellation de Möbius peut être démontrée dans presque tous les intervalles courts dont la longueur tend vers l'infini. Cela motive le passage d'une propriété ponctuelle globale à une propriété statistique locale.

### Tao / Chowla logarithmiquement moyennée

Le résultat à deux points illustre qu'une conjecture inaccessible peut devenir attaquable après changement de moyenne et de notion d'observable. C'est un exemple méthodologique direct pour la V6.

### Katz–Sarnak [KS99]

Les familles de fonctions L révèlent des types de symétrie unitaires, orthogonaux et symplectiques et montrent qu'un comportement collectif peut rendre visible une structure invisible au niveau d'un objet isolé.

### Rodgers–Tao / de Bruijn–Newman

Le résultat \(\Lambda\ge0\) transforme RH en criticité exacte \(\Lambda=0\). Ce cadre est le prototype V6 d'une reformulation qui ne change pas seulement les coordonnées du problème, mais introduit un **paramètre de déformation** et un seuil.

### Alpöge–Furman (2026) [AF26]

Le résultat sur plus de deux tiers des zéros simples et sur la droite critique confirme la puissance d'un changement de question : compter/proportionner au lieu d'exiger immédiatement une localisation totale. La compression de la forme hermitienne de Weil, l'inégalité rang–trace et l'inertie constituent pour la V6 un modèle de « compression fertile ».

---

# 13. Noms de travail retenus pour la V6

Les noms suivants deviennent le vocabulaire interne proposé :

- **Miroir de Möbius**
- **Filtre antipôle**
- **Thermomètre d'horizon**
- **Effaceur orthogonal**
- **Positivité porteuse**
- **Census spectral**
- **Microscope de population**
- **Thermostat critique**
- **Scène manquante**
- **Jumeau de crash-test**
- **Modes sombres**
- **Compression fertile**
- **Tomographie de cohérence TOMO-2**
- **Tomographie de phase TOMO-3**
- **Fermeture multiplicative**
- **Secteur sombre arithmétique / DARK-ZETA**
- **Flux d'inertie**
- **Géométrie par empreintes**
- **Census de Möbius**
- **PRIME-LOCK / verrou premier**
- **DUAL-LOCK / serrure à deux clés**
- **Résidu sombre**

Ces noms ne remplacent jamais les définitions mathématiques dans les preuves ou les notes techniques. Ils servent à **désolidariser l'intuition du chemin historique qui l'a produite** et à faciliter les recombinaisons.

---

# 14. Décision de lancement V6

La V6 ne reprend pas l'attaque RH là où la V5.8 l'a fermée.

Elle ouvre un laboratoire de mécanismes avec une première séquence :

1. **DARK-ZETA / TOMO-DH** — établir l'échelle d'observabilité et ses témoins adversariaux ;
2. **TOMO-2** — vérifier les invariants d'ordre 2 et le contrôle par randomisation de phase ;
3. **TOMO-3** — tester le lien entre fermeture bispectrale et défaut multiplicatif ;
4. trianguler tout signal survivant avec au moins un second canal : Weil/inertie, criticité, Möbius ou géométrie par empreintes ;
5. fermer immédiatement toute branche qui ne dépasse pas l'information explicitement injectée.

La règle de gouvernance est simple :

> **Aucune grande métaphore ne gagne le droit de devenir une branche tant qu'elle n'a pas produit un petit objet falsifiable.**

Et réciproquement :

> **Une petite structure robuste qui survit aux témoins négatifs mérite d'être suivie, même si son rapport à RH est encore indirect.**

---

# 15. Références de cadrage vérifiées pour cette note

- K. Matomäki, M. Radziwiłł, *Multiplicative functions in short intervals*, Annals of Mathematics 183 (2016), 1015–1056.
- T. Tao, *The logarithmically averaged Chowla and Elliott conjectures for two-point correlations*, 2015.
- N. Katz, P. Sarnak, *Zeroes of zeta functions and symmetry*, Bulletin of the AMS 36 (1999), 1–26.
- B. Rodgers, T. Tao, *The de Bruijn–Newman constant is non-negative*, 2018.
- L. Alpöge, R. Furman, *More than two thirds of the zeta zeros are simple and on the critical line*, arXiv:2608.13637 (2026).
- NIST DLMF, §25.2(iv), produit d'Euler de la fonction zêta de Riemann — repère pour la rigidité multiplicative.
- NASA Science, *Dark Matter* — utilisé uniquement comme référence pour l'analogie méthodologique d'inférence d'une structure invisible par ses effets ; aucune analogie physique avec ζ n'est revendiquée.
- Littérature des spectres d'ordre supérieur / bispectres — repère méthodologique pour distinguer statistiques d'ordre 2 et couplages de phase d'ordre 3.

## Références internes V5.8 à conserver comme points d'ancrage

- `1_Presentation/13_Lecon_2026.*`
- `3_Preuves_et_calculs/preuves/MEMO_P2_2_WEIL.md`
- `3_Preuves_et_calculs/preuves/DAVENPORT_HEILBRONN_TEST.md`
- `1_Presentation/12_Annulation_du_pole.*`
- `3_Preuves_et_calculs/preuves/NB_GRAM.md`
- `3_Preuves_et_calculs/preuves/ENERGY_FRACTAL_DIMENSION.md`

---

## Résumé opérationnel

La V6 conserve les résultats, les échecs et les contrôles de la V5.8, mais change le mode de recherche :

\[
\boxed{
\text{nommer les mécanismes}
\to
\text{les désolidariser de RH}
\to
\text{les recombiner}
\to
\text{construire un observable}
\to
\text{le soumettre à un témoin négatif}
}
\]

Le premier pari n'est donc pas « une nouvelle preuve ».

Le premier pari est :

\[
\boxed{
\text{retrouver une information que }Q\text{ a écrasée, puis la trianguler.}
}
\]

**DARK-ZETA** est le cadre transversal ; **TOMO-DH** en est le premier détecteur expérimental. Le programme doit déterminer non seulement *si* une séparation existe, mais *à quel ordre d'observabilité* elle apparaît et si elle est réellement reliée à la rigidité multiplicative.


# 16. Premier retour expérimental de la V6

Le premier détecteur DARK-ZETA/TOMO a été construit et exécuté. La règle V6 de falsification a joué son rôle : la piste « fermeture de phase bispectrale = signature de multiplicativité » n'est pas soutenue par le premier protocole. TOMO-2 conserve une valeur diagnostique dans une famille appariée, mais n'est pas un invariant universel.

Ce résultat déplace la question de « quel ordre de corrélation ? » vers « quel canal rend la structure arithmétique observable ? ». La prochaine branche devra donc tester des couplages **inter-canaux arithmétiques**, plutôt que simplement augmenter l'ordre du polyspectre d'un signal agrégé.

Voir `17_DARK_ZETA_premier_detecteur_resultats.md`.


# 17. Mise à jour V6.2 — PRIME-LOCK et bascule DUAL-LOCK

Le premier détecteur TOMO a montré que l'ordre 3 du signal agrégé ne suffisait pas. PRIME-LOCK a donc changé le canal : la dérivée logarithmique a été décomposée en contributions des nombres premiers, des puissances supérieures de premiers et des indices hors puissances de premiers.

Résultat : zeta et `L_chi5` satisfont exactement le verrou eulérien à l'arrondi ; Davenport–Heilbronn présente une fuite massive hors puissances de premiers et un défaut local de tour. Une eulérisation conservant les données aux premiers modifie fortement son signal global. Les témoins Steinhaus complètement multiplicatifs satisfont néanmoins PRIME-LOCK : le verrou local ne suffit donc pas.

La prochaine branche devient **DUAL-LOCK** : rechercher non deux scores juxtaposés, mais une identité ou un opérateur où structure locale aux premiers et structure globale archimédienne/fonctionnelle interagissent intrinsèquement.

Références internes : `18_PRIME_LOCK_premier_verrou_local.md`, `19_DUAL_LOCK_plan_local_global.md`, `preuves/PRIME_LOCK_DETECTOR.md`.


# 18. Mise à jour V6.3 — DUAL-LOCK et Résidu sombre

DUAL-LOCK a maintenant été construit et exécuté. Des compressions finies de la forme explicite, calculées uniquement côté archimédien + conducteur/pôle + dérivée logarithmique locale, produisent des directions négatives pour Davenport–Heilbronn dans plusieurs fenêtres fréquentielles, tandis que le contrôle eulérien apparié `L_pair_chi5` reste positif sur les témoins confirmés. Les zéros DH ne sont utilisés qu'après le scan comme validation post hoc.

La décomposition du vecteur propre négatif montre un nouveau mécanisme V6 : le **Résidu sombre**. Le signe final ne provient pas d'un terme dominant isolé ; il survit après cancellation de contributions local/global beaucoup plus grandes. Sur les témoins DH confirmés, le facteur d'amplification de cancellation va d'environ 10× à 70×. Un sweep de quadrature conserve le signe et les valeurs à l'arrondi utile.

Cette notion ne postule aucune « énergie noire » physique. Elle formalise une situation d'observabilité : l'information discriminante peut vivre dans le petit reliquat d'une soustraction entre gros termes. La conséquence méthodologique est sévère : plus le résidu est petit, plus il doit être vérifié par des méthodes numériques indépendantes et des contrôles analytiques.

Références internes : `20_Registre_metaphores_V6.md`, `21_DUAL_LOCK_RESIDU_SOMBRE_resultats.md`, `preuves/DARK_RESIDUAL.md`, `src/dark_residual.py`.

<!-- references:debut -->

## Références

Format : [clé] auteurs, *titre*, publication, lien. Fiches complètes et état de vérification : document 42 (registre des sources).

- [AF26] L. Alpöge, R. Furman. *More than two thirds of the zeros of the Riemann zeta function are simple and on the critical line*. arXiv:2608.13637 (août 2026). <https://arxiv.org/abs/2608.13637> — vérifié en ligne
- [Beu55] A. Beurling. *A closure problem related to the Riemann zeta-function*. Proc. Natl. Acad. Sci. USA 41 (1955), 312–314. <https://www.pnas.org/doi/pdf/10.1073/pnas.41.5.312> — vérifié en ligne
- [DeB50] N. G. de Bruijn. *The roots of trigonometric integrals*. Duke Math. J. 17 (1950), 197–226. <https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Newman_constant> — partiellement vérifié
- [DH36a] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series*. J. London Math. Soc. 11 (1936), no. 3, 181–185. <https://doi.org/10.1112/jlms/s1-11.3.181> — partiellement vérifié
- [DH36b] H. Davenport, H. Heilbronn. *On the zeros of certain Dirichlet series. II*. J. London Math. Soc. 11 (1936), no. 4, 307–312. <https://doi.org/10.1112/jlms/s1-11.4.307> — partiellement vérifié
- [KS99] N. M. Katz, P. Sarnak. *Zeroes of zeta functions and symmetry*. Bull. Amer. Math. Soc. 36 (1999), 1–26 ; voir aussi le livre Random Matrices, Frobenius Eigenvalues, and Monodromy, AMS Colloq. Publ. 45 (1999). <https://www.ams.org/bull/1999-36-01/S0273-0979-99-00766-1/> — vérifié en ligne
- [MRST26] K. Matomäki, M. Radziwiłł, X. Shao, T. Tao, J. Teräväinen. *Higher uniformity of arithmetic functions in short intervals II. Almost all intervals*. Invent. Math. 244 (2026), 967–1091. <https://link.springer.com/article/10.1007/s00222-026-01408-6> — vérifié en ligne
- [New76] C. M. Newman. *Fourier transforms with only real zeros*. Proc. Amer. Math. Soc. 61 (1976), 245–251. <https://en.wikipedia.org/wiki/De_Bruijn%E2%80%93Newman_constant> — partiellement vérifié
- [Nym50] B. Nyman. *On the one-dimensional translation group and semi-group in certain function spaces*. Thèse, Université d'Uppsala, 1950. — partiellement vérifié
- [RT20] B. Rodgers, T. Tao. *The De Bruijn–Newman constant is non-negative*. Forum Math. Pi 8 (2020), e6 ; arXiv:1801.05914. <https://arxiv.org/abs/1801.05914> — vérifié en ligne
- [Tit37] E. C. Titchmarsh. *Introduction to the Theory of Fourier Integrals*. Oxford, Clarendon Press, 1937. — non vérifié

<!-- references:fin -->
