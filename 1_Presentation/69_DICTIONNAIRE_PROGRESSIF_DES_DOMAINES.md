---
title: "Dictionnaire progressif des domaines"
subtitle: "La langue des passages - V6.44 - Document 69"
author: "Vincent P. P. NOËL - dossier de recherche, rédaction assistée"
date: "12 octobre 2026"
---

# Comment apprendre cette langue

Une fiche commence par une image simple, puis donne un symbole, son domaine et
la condition qui rend le geste autorisé. Le nom imagé aide à comprendre ; la
définition et la garde portent le calcul. Les mots usuels restent canoniques.

La langue des passages relie le **moule** P, la **valise** U, la **portée** Fourier
ou Mellin, le **puzzle** de changement de base et la **balance** de Schur.
Son arithmétique distingue addition, produit ordinaire et convolution. Sa logique
écrit ce qui est conservé, ce qui se perd et le budget du passage. Les preuves
L1–L8 et les domaines exacts sont dans le document 68.

Une phrase possède quatre étiquettes : support S, ordre de jets r aux ±1/2,
ordre q en 0, et unité d’amplitude A^u. Le geste P gagne r ; la dérivée gagne q ;
la convolution additionne les ordres. Le produit ordinaire peut perdre les moments.
Les jets de test aux ±1/2, les jets de test en 0 et les jets des zéros critiques
sont trois entrées différentes de la langue.

Le noyau ci-dessous explique les objets de l’expérience actuelle et les principaux
objets du corpus. Tous les 95 noms du registre canonique sont repris avec leur
ancrage et leur garde. L’index technique séparé donne toutes les déclarations
Python analysées : une fonction de programme n’est pas automatiquement un
opérateur mathématique. Cette édition ne prétend pas avoir désambiguïsé chaque
symbole de toutes les archives historiques.

Une fiche marquée définition n’est pas une preuve nouvelle ; un statut du registre
est hérité, sans validation additionnelle. Les calculs V644 sont exploratoires,
sauf l’algèbre rationnelle et le contrat analytique entier de queue explicités.

Cette édition contient **219 fiches du noyau**, **95 métaphores nommées** et un index de **986 fonctions**, **15 classes**, dans **155 fichiers avec déclarations**, avec 0 erreur de parseur.


# Niveau 1 - Les petits mots et les unités

## Nombre

**Comme un premier jeu.** Une place sur une règle.

**Symbole.** x∈ℝ

**Sens et domaine.** Un réel sert de coordonnée ; les nombres complexes ajoutent une seconde coordonnée.

**Garde.** Une lettre peut changer de rôle ; son domaine doit être annoncé.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Nombre complexe

**Comme un premier jeu.** Une flèche qui va aussi vers le côté.

**Symbole.** z=a+ib, i²=-1

**Sens et domaine.** ℂ est un plan avec addition et multiplication ; Re z=a et Im z=b.

**Garde.** Complexe ne signifie ni positif ni négatif ; seul un réel peut recevoir cet ordre.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Conjugaison

**Comme un premier jeu.** La flèche se regarde dans un miroir.

**Symbole.** z̄=a-ib

**Sens et domaine.** Involution de ℂ ; dans un produit scalaire elle rend la norme réelle.

**Garde.** Oublier la conjugaison peut transformer une forme hermitienne en autre chose.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Module

**Comme un premier jeu.** La longueur de la flèche.

**Symbole.** |z|²=z̄z

**Sens et domaine.** Quantité réelle non négative ; homogène au carré de l’amplitude.

**Garde.** La longueur oublie la phase, donc deux flèches différentes peuvent avoir le même module.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Fonction

**Comme un premier jeu.** Une machine prend un jouet et rend un résultat.

**Symbole.** f:X→Y

**Sens et domaine.** À chaque entrée du domaine X correspond une sortie de Y.

**Garde.** Composer g et f exige que la sortie de f entre dans le domaine de g.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Somme

**Comme un premier jeu.** On rassemble des petites piles.

**Symbole.** Σ\_k a\_k

**Sens et domaine.** Somme finie ou limite de sommes partielles pour une série.

**Garde.** Une série infinie exige une règle de convergence ; réordonner peut changer une série conditionnelle.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Intégrale

**Comme un premier jeu.** On rassemble toutes les fines bandes d’un dessin.

**Symbole.** ∫ f(x) dx

**Sens et domaine.** Intégrale de Lebesgue lorsque f est intégrable ; remplace une somme discrète.

**Garde.** Une intégrale impropre ne peut pas être manipulée sans vérifier sa convergence.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Dérivée

**Comme un premier jeu.** On regarde comment la pente change.

**Symbole.** Df=f′

**Sens et domaine.** D est une dérivation, classique ou faible selon le domaine.

**Garde.** Df et f n’ont pas automatiquement les mêmes unités ; dx doit être typé.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Courbure

**Comme un premier jeu.** On regarde si le chemin se courbe.

**Symbole.** D²f=f″

**Sens et domaine.** Deux dérivations ; définie classiquement pour C² ou faiblement dans H².

**Garde.** Un coin peut ajouter une distribution quand on prolonge une fonction par zéro.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Dérivée partielle

**Comme un premier jeu.** On tourne un bouton en gardant les autres immobiles.

**Symbole.** ∂\_t F

**Sens et domaine.** Dérivation selon une variable déclarée.

**Garde.** Une dérivée en temps physique est une puissance si la grandeur est une énergie ; un paramètre arithmétique n’est pas un temps physique.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Support

**Comme un premier jeu.** L’endroit où le dessin n’est pas effacé.

**Symbole.** supp f⊂[-S,S]

**Sens et domaine.** Fermeture des points où la fonction est non nulle, au sens essentiel pour L².

**Garde.** Déplacer le dessin change son adresse, pas son diamètre.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Limite

**Comme un premier jeu.** Les dessins se rapprochent de plus en plus.

**Symbole.** f\_n→f

**Sens et domaine.** Le sens dépend de la norme ou de la topologie annoncée.

**Garde.** Convergence ponctuelle, L² et H¹ ne sont pas interchangeables.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Norme

**Comme un premier jeu.** Une règle qui mesure un dessin.

**Symbole.** ||f||

**Sens et domaine.** Positive, homogène, triangulaire ; la métrique choisie fixe ce que signifie proche.

**Garde.** Changer la règle conserve parfois le signe, pas les tailles ni les marges.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Produit scalaire

**Comme un premier jeu.** On mesure combien deux dessins se ressemblent.

**Symbole.** ⟨f,g⟩=∫f̄g

**Sens et domaine.** Forme sesquilinéaire hermitienne ; ici convention antilinéaire en première variable.

**Garde.** Une métrique externe doit être définie sans présupposer le signe de Q\_W.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Composition

**Comme un premier jeu.** Deux machines attachées l’une à l’autre.

**Symbole.** g∘f

**Sens et domaine.** Appliquer f puis g ; domaines et codomaines compatibles.

**Garde.** Le nom d’une machine ne suffit pas pour autoriser un passage.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Unités fictives

**Comme un premier jeu.** Chaque quantité porte une étiquette sur sa boîte.

**Symbole.** [f]=A, [Q]=E=A²

**Sens et domaine.** x=log u est sans dimension ; A et E sont des unités formelles de tenue des calculs.

**Garde.** Une unité cohérente ne prouve pas un signe et ne donne pas une énergie physique.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Puissance par dérivation

**Comme un premier jeu.** On mesure combien la pile change à chaque tic.

**Symbole.** dE/dt

**Sens et domaine.** Si t est un temps, unité E/T ; si t est un indice arithmétique, unité formelle différente.

**Garde.** E≥0 n’impose pas dE/dt≥0 ; par exemple E(t)=e\^(-t)>0 et E′<0.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Énergie arithmétique formelle

**Comme un premier jeu.** La balance porte l’étiquette énergie.

**Symbole.** E\_ar=Q\_W(f)

**Sens et domaine.** Unité fictive A² pour une forme quadratique ; changement d’amplitude c multiplie par |c|².

**Garde.** Le nom énergie ne donne pas Q\_W≥0 : c’est précisément le signe recherché.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Positivité

**Comme un premier jeu.** La balance ne descend pas sous sa marque.

**Symbole.** x≥0 ; Q(f)≥0

**Sens et domaine.** Ordre sur les réels ; positivité d’une forme pour toutes les entrées du domaine.

**Garde.** Produit de nombres positifs positif ; une somme signée ou une dérivée n’hérite pas de cette règle.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Règle du produit

**Comme un premier jeu.** Deux dessins bougent, il faut compter deux effets.

**Symbole.** D(fg)=f′g+fg′

**Sens et domaine.** Identité de Leibniz sous régularité suffisante.

**Garde.** Les cutoffs et les phases apportent donc des termes supplémentaires.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Cauchy–Schwarz

**Comme un premier jeu.** L’attache de deux dessins ne dépasse pas leurs tailles.

**Symbole.** |⟨f,g⟩|≤||f||||g||

**Sens et domaine.** Inégalité Hilbert, utilisée pour majorer corrélations et primes.

**Garde.** La majoration de taille ne décide pas du signe de l’attache.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Identité

**Comme un premier jeu.** Le jouet revient pareil.

**Symbole.** If=f

**Sens et domaine.** Opérateur neutre dans le domaine choisi.

**Garde.** Dans I-K, la présence de I ne prouve pas que K≤I.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Partie entière

**Comme un premier jeu.** On garde seulement les piles entières.

**Symbole.** ⌊x⌋

**Sens et domaine.** Plus grand entier ≤x ; détermine le plafond discret des puissances premières.

**Garde.** Près d’un entier, il faut encadrer x avant de décider.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Partie réelle

**Comme un premier jeu.** On garde le pas droit de la flèche.

**Symbole.** Re z=(z+z̄)/2

**Sens et domaine.** Projection ℂ→ℝ ; intervient dans Q\_pr et polarisation.

**Garde.** Oublie la composante imaginaire ; ne permet pas de reconstruire la phase seule.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Linéarité

**Comme un premier jeu.** La machine respecte l’assemblage des dessins.

**Symbole.** A(af+bg)=aAf+bAg

**Sens et domaine.** Propriété des opérateurs P, translations, transforms et corrections fixes.

**Garde.** Q est quadratique, pas linéaire ; il contient des attaches croisées.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Forme quadratique

**Comme un premier jeu.** La pile grandit au carré de la taille.

**Symbole.** Q(cf)=|c|²Q(f)

**Sens et domaine.** Forme issue d’un couplage hermitien ; domaine annoncé.

**Garde.** Homogénéité quadratique seule n’implique pas Q≥0.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.


# Niveau 2 - Les fonctions et leurs miroirs

## Exponentielle

**Comme un premier jeu.** Une taille qui se multiplie quand on ajoute un pas.

**Symbole.** e\^x

**Sens et domaine.** Fonction réelle positive ; e\^(x+y)=e\^x e\^y ; extension entière sur ℂ.

**Garde.** e\^z peut être complexe ; « exponentielle positive » concerne x réel.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Logarithme

**Comme un premier jeu.** On compte les pas multiplicatifs avec une règle additive.

**Symbole.** x=log u

**Sens et domaine.** Inverse réel de exp sur u>0 ; log(uv)=log u+log v.

**Garde.** Le logarithme complexe demande un choix de branche.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Sinus et cosinus

**Comme un premier jeu.** Une roue qui tourne.

**Symbole.** e\^(it)=cos t+i sin t

**Sens et domaine.** Fonctions périodiques réelles ; décrivent les phases Fourier.

**Garde.** Une phase modifie les couplages si elle dépend de x.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Sinus hyperbolique

**Comme un premier jeu.** Deux tailles poussent en sens opposé.

**Symbole.** 2 sinh(x/2)=e\^(x/2)-e\^(-x/2)

**Sens et domaine.** Solution élémentaire utilisée pour l’inverse causal de D²-1/4.

**Garde.** Ce noyau inverse exige les deux moments pour refermer le support à droite.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Fonction Gamma

**Comme un premier jeu.** Une machine prolonge la pile des factorielles.

**Symbole.** Γ(s)=∫₀∞ t\^(s-1)e\^(-t)dt

**Sens et domaine.** Définie par l’intégrale pour Re s>0 puis prolongement méromorphe ; Γ(n+1)=n!.

**Garde.** Ses pôles et branches des facteurs associés doivent être pris en compte.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Fonction zêta

**Comme un premier jeu.** Une chorale où chaque entier chante.

**Symbole.** ζ(s)=Σₙ≥₁ n\^(-s)

**Sens et domaine.** Série absolument convergente pour Re s>1 ; prolongement méromorphe, pôle simple en 1.

**Garde.** La série brute n’est pas la définition convergente dans la bande critique.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Zêta complétée

**Comme un premier jeu.** On habille la chorale pour voir son miroir.

**Symbole.** ξ(s)=½s(s-1)π\^(-s/2)Γ(s/2)ζ(s)

**Sens et domaine.** Fonction entière ; ξ(s)=ξ(1-s), zéros correspondant aux zéros non triviaux de ζ.

**Garde.** Symétrie ne suffit pas à imposer que tous les zéros soient sur l’axe.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Hypothèse de Riemann

**Comme un premier jeu.** Toutes les notes recherchées devraient rester sur une ligne.

**Symbole.** ζ(ρ)=0 ⇒ Re ρ=1/2, 0<Re ρ<1

**Sens et domaine.** Énoncé global sur tous les zéros non triviaux.

**Garde.** Un nombre fini de notes, matrices ou certificats ne couvre pas l’infini.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Zéro et multiplicité

**Comme un premier jeu.** Le dessin touche zéro ; parfois il s’y accroche deux fois.

**Symbole.** F(ρ)=0, F′(ρ)=0

**Sens et domaine.** Un zéro de multiplicité m annule les m premiers jets et pas le suivant.

**Garde.** Zéro double d’une fonction n’est pas automatiquement collision de branches suivies.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Série de Dirichlet

**Comme un premier jeu.** Chaque entier reçoit un volume de voix.

**Symbole.** F(s)=Σ a\_n n\^(-s)

**Sens et domaine.** Fonction sur un demi-plan de convergence ; coefficients a\_n déclarés.

**Garde.** Une équation fonctionnelle seule ne donne pas un produit d’Euler.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Produit d’Euler

**Comme un premier jeu.** Les briques premières fabriquent les entiers.

**Symbole.** ζ(s)=∏ₚ(1-p\^(-s))\^(-1)

**Sens et domaine.** Identité absolument convergente pour Re s>1.

**Garde.** La multiplicativité locale ne prouve pas RH.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Poids de von Mangoldt

**Comme un premier jeu.** Seules les tours de briques premières portent une étiquette.

**Symbole.** Λ(p\^m)=log p, Λ(n)=0 sinon

**Sens et domaine.** Fonction arithmétique ; -ζ′/ζ=ΣΛ(n)n\^(-s) pour Re s>1.

**Garde.** Λ(n) ici n’est pas la constante de de Bruijn-Newman.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Fonction de Möbius

**Comme un premier jeu.** On donne un signe aux sacs de briques sans doublon.

**Symbole.** μ(n)=0 ou (-1)\^r

**Sens et domaine.** Nulle si un carré premier divise n ; sinon signe selon le nombre de facteurs premiers.

**Garde.** Une covariance de μ ne révèle pas chaque zéro.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Caractère de Dirichlet

**Comme un premier jeu.** Une couleur suit la règle de multiplication.

**Symbole.** χ(mn)=χ(m)χ(n)

**Sens et domaine.** Caractère modulo q, périodique et nul sur les non-unités ; L(s,χ)=Σχ(n)n\^(-s).

**Garde.** Ne pas identifier un mélange de fonctions L à un produit d’Euler.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Coefficients de Li

**Comme un premier jeu.** On rassemble les notes dans une suite de balances.

**Symbole.** λ\_n=Σρ[1-(1-1/ρ)\^n]

**Sens et domaine.** Somme sur les zéros selon la convention symétrique ; critère global de Li pour ξ.

**Garde.** Sommes tronquées et intervalle fini de n ne prouvent pas toutes les inégalités.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Flot de chaleur

**Comme un premier jeu.** On floute ou on accentue un dessin.

**Symbole.** ∂\_t H=-∂\_x²H selon convention

**Sens et domaine.** Flot de de Bruijn-Newman avec paramètre et signe déclarés, lié à un seuil de réalité des zéros.

**Garde.** Le paramètre n’est pas une température physique et la convention doit être fixée.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Entropie et conventions

**Comme un premier jeu.** On compte combien un choix nous surprend.

**Symbole.** H(p)=-Σp\_i log p\_i

**Sens et domaine.** Entropie de Shannon non négative pour une loi discrète ; entropie différentielle peut être négative.

**Garde.** Il n’existe pas une positivité universelle de toute quantité appelée entropie.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Constante d’Euler

**Comme un premier jeu.** Une petite correction reste après deux grands comptes.

**Symbole.** γ\_E=lim(Σₖ≤n1/k-log n)

**Sens et domaine.** Constante réelle présente dans C₀.

**Garde.** Ne pas l’identifier au rabais γ de Bellman.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Équation fonctionnelle

**Comme un premier jeu.** La chorale se répond dans un miroir.

**Symbole.** ξ(s)=ξ(1-s)

**Sens et domaine.** Symétrie analytique exacte de la fonction complétée.

**Garde.** Le miroir permet des paires hors de la ligne ; il ne force pas RH seul.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Factorielle

**Comme un premier jeu.** On compte tous les rangements de n jouets.

**Symbole.** n!=1·2·…·n

**Sens et domaine.** Fonction sur les entiers non négatifs, 0!=1 ; intervient dans Taylor.

**Garde.** Une série Taylor tronquée exige une borne de reste.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Prolongement analytique

**Comme un premier jeu.** Le dessin continue quand ses règles le forcent.

**Symbole.** F prolongée depuis un domaine

**Sens et domaine.** Unicité sur domaines connexes par identité analytique ; méromorphe si pôles.

**Garde.** Cela ne donne pas automatiquement l’emplacement des zéros.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Puissance première

**Comme un premier jeu.** Une tour faite d’une seule brique première.

**Symbole.** n=p\^m

**Sens et domaine.** Indices portant Λ(n) ; liste exacte finie à support fixé.

**Garde.** Inclure toutes les puissances, pas seulement les premiers simples.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Arc tangente et artanh

**Comme un premier jeu.** Deux petites règles inversent des courbes.

**Symbole.** atan z, artanh z

**Sens et domaine.** Pour les queues archimédiennes réelles ici z=e\^(-S)∈(0,1), formules usuelles.

**Garde.** Les branches complexes ne sont pas utilisées dans ces quadratures réelles.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Branche du logarithme

**Comme un premier jeu.** On choisit où la rotation commence.

**Symbole.** Log F sur domaine sans zéro

**Sens et domaine.** Un logarithme holomorphe exige domaine approprié et absence de zéro ; sinon branches locales.

**Garde.** La phase globale et les passages de branches ne sont pas résolus par une formule locale.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Périodicité

**Comme un premier jeu.** Le dessin recommence après le même pas.

**Symbole.** f(x+T)=f(x)

**Sens et domaine.** Relation exacte à période déclarée ; utilisée dans des mécanismes de rigidité.

**Garde.** Le support compact, une fonction entière et un caractère modulo q ont des domaines différents.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Ligne critique

**Comme un premier jeu.** La porte finale ressemble à une ligne dans un plan.

**Symbole.** Re s=1/2

**Sens et domaine.** Ensemble vertical où RH place tous les zéros non triviaux.

**Garde.** La symétrie autour de cette ligne n’impose pas que les zéros y restent.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## RH et simplicité

**Comme un premier jeu.** La ligne et les doubles notes sont deux règles.

**Symbole.** RH ≠ tous les zéros simples

**Sens et domaine.** RH porte sur la partie réelle ; conjecture de simplicité est plus forte et distincte.

**Garde.** Résoudre une collision de zéros n’est pas nécessairement nécessaire à prouver RH par un critère de forme.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.


# Niveau 3 - Les pièces où vivent les fonctions

## Espace L²

**Comme un premier jeu.** Les dessins ont une taille totale finie.

**Symbole.** ∫|f|²<∞

**Sens et domaine.** Fonctions modulo égalité presque partout ; Hilbert avec norme quadratique.

**Garde.** La dérivée et la forme de Weil ne sont pas contrôlées par la seule norme L².

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Espace H¹

**Comme un premier jeu.** La règle mesure aussi les pentes.

**Symbole.** ||f||H¹²=||f||₂²+||f′||₂²

**Sens et domaine.** Fonctions L² avec dérivée faible L².

**Garde.** Sa positivité est externe ; un opérateur compact peut avoir une forme positive sans marge uniforme.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Espace H₀³

**Comme un premier jeu.** Le dessin et ses deux premières pentes s’attachent au bord.

**Symbole.** ψ,ψ′,ψ″=0 aux bords

**Sens et domaine.** Fermeture de Cc∞(-S,S) dans H³ ; traces nulles jusqu’à l’ordre 2.

**Garde.** La définition dépend du domaine ouvert et du prolongement par zéro.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Cœur lisse

**Comme un premier jeu.** Des dessins sans coins, rangés loin du bord.

**Symbole.** Cc∞(-S,S)

**Sens et domaine.** Fonctions infiniment dérivables à support compact intérieur.

**Garde.** Une fonction polynomiale coupée au bord n’est généralement pas dans ce cœur.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Translation

**Comme un premier jeu.** La valise change d’adresse sans changer son contenu.

**Symbole.** U\_a f(x)=f(x-a)

**Sens et domaine.** Unitaire dans L² et H¹ sur ℝ ; mêmes autocorrélations.

**Garde.** E\_S est transporté dans une fenêtre plus grande, pas forcément dans la même E\_S.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Dilatation Beurling

**Comme un premier jeu.** Le dessin tient dans une boîte plus petite.

**Symbole.** D\_a f(t)=a\^(-1/2)f(t/a)1\_(0,a)(t)

**Sens et domaine.** Isométrie L²(0,1) pour 0<a≤1 ; sous J elle devient translation.

**Garde.** Le facteur a\^(-1/2) est nécessaire et les domaines ne sont pas celui de U sans J.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Fraction Beurling

**Comme un premier jeu.** On garde le petit reste d’un partage.

**Symbole.** ρ\_θ(t)={θ/t}, Σc\_jθ\_j=0

**Sens et domaine.** Combinaisons de parties fractionnaires dans L²(0,1), condition admissible de Nyman-Beurling.

**Garde.** Leur densité est un critère de RH, donc ne peut pas être supposée pour prouver RH.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Passage logarithmique J

**Comme un premier jeu.** Une règle courbe devient une règle droite.

**Symbole.** Jf(x)=e\^(-x/2)f(e\^(-x))

**Sens et domaine.** Unitaire L²(0,1)→L²(0,∞) ; change la mesure avec son facteur.

**Garde.** L² ne devient pas H¹ par simple changement de coordonnées.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Passage multiplicatif

**Comme un premier jeu.** Des pas deviennent des multiplications.

**Symbole.** ℒf(u)=u\^(-1/2)f(log u)

**Sens et domaine.** Unitaire L²(ℝ,dx)→L²(ℝ₊,du).

**Garde.** Ne pas confondre ℒ avec J, qui utilise x=-log t et une demi-droite.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Transformée de Fourier

**Comme un premier jeu.** On entend les rythmes cachés dans le dessin.

**Symbole.** f̂(τ)=(2π)\^(-1/2)∫f(x)e\^(-iτx)dx

**Sens et domaine.** Unitaire L² par Plancherel ; translations deviennent phases, D devient iτ.

**Garde.** Une convention de normalisation différente change les constantes.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Transformée de Mellin

**Comme un premier jeu.** On entend les rythmes de changements de taille.

**Symbole.** Mf(s)=∫₀∞ f(u)u\^(s-1)du

**Sens et domaine.** Pour ℒf, Mℒf(s)=∫f(x)e\^((s-1/2)x)dx ; entier si support compact.

**Garde.** Les moments admissibles sont les valeurs en 0 et 1, pas toute la transformée.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Convolution

**Comme un premier jeu.** Un petit pinceau passe sur le dessin.

**Symbole.** (η\*f)(x)=∫η(x-y)f(y)dy

**Sens et domaine.** Lissage et produit Fourier selon convention ; support s’additionne.

**Garde.** Lisser peut déborder de la fenêtre ; il faut une marge ou un cutoff.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Mollificateur

**Comme un premier jeu.** Un pinceau de largeur δ.

**Symbole.** η\_δ(x)=δ\^(-1)η(x/δ), ∫η=1

**Sens et domaine.** Approximation de l’identité ; η lisse à support compact.

**Garde.** Un contrôle en H¹ ou dans la métrique R doit être prouvé, pas déduit de L² seul.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Fonction de coupure

**Comme un premier jeu.** On efface doucement l’extérieur d’une boîte.

**Symbole.** χ f

**Sens et domaine.** χ∈Cc∞, bornes de dérivées déclarées ; multiplicateur local.

**Garde.** Les dérivées de χ ajoutent des termes au budget.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Deux moments

**Comme un premier jeu.** Deux balances doivent être à zéro.

**Symbole.** ℓ±(f)=∫f(x)e\^(±x/2)dx

**Sens et domaine.** Fonctionnelles linéaires continues à support fixé.

**Garde.** Elles ne sont ni l’intégrale seule ni une condition de signe.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Espace admissible E_S

**Comme un premier jeu.** Les dessins passent deux portes et restent dans la boîte.

**Symbole.** E\_S=H₀¹(-S,S)∩kerℓ₊∩kerℓ₋

**Sens et domaine.** Espace fermé de codimension 2 ; domaine H¹ de la forme complète.

**Garde.** Changer la fenêtre ou la norme impose un nouveau contrat.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Moule admissible P

**Comme un premier jeu.** Un moule ferme les deux ouvertures.

**Symbole.** P=D²-1/4

**Sens et domaine.** Isomorphisme H₀³(-S,S)→E\_S ; annulations exactes par intégration par parties.

**Garde.** P impose les moments, pas le signe de Q\_W. Ce P n’est pas un polynôme zêta.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Inverse du moule

**Comme un premier jeu.** On retrouve le dessin avant le moule.

**Symbole.** ψ(x)=∫₋Sˣ 2sinh((x-y)/2)f(y)dy

**Sens et domaine.** Inverse de P pour f∈E\_S, deux moments ferment les traces à droite.

**Garde.** Sans ces moments, le résultat ne reste pas dans H₀³.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Graine polynomiale

**Comme un premier jeu.** Une pâte qui colle bien aux bords.

**Symbole.** ψS,k=(1-x²/S²)\^4(x/S)\^k 1\_[-S,S]

**Sens et domaine.** Graine H₀⁴, C³ sur ℝ ; fS,k=PψS,k∈H₀² ; famille indépendante et dense dans E\_S.

**Garde.** Pas C∞ en général ; la continuité H¹ de Q justifie son usage.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Modulation

**Comme un premier jeu.** On ajoute une rotation à chaque place.

**Symbole.** M\_τ f=e\^(iτx)f

**Sens et domaine.** Unitaire L² ; déplace la fréquence Fourier.

**Garde.** Brise généralement les deux moments ; P M\_τ ψ reste admissible mais change Q.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Phase constante

**Comme un premier jeu.** Tout le dessin tourne du même angle.

**Symbole.** f↦e\^(iθ)f

**Sens et domaine.** Moments nuls, autocorrélation, R et Q\_W conservés.

**Garde.** Une phase variable e\^(iτx) est une autre opération.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Changement d’échelle

**Comme un premier jeu.** On agrandit la boîte et le dessin.

**Symbole.** f(x)↦f(x/S)

**Sens et domaine.** Le support et les dérivées changent ; P et les points log(p\^m) ne se transportent pas inchangés.

**Garde.** Ce changement n’est pas une invariance de Q\_W.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Dérivée faible

**Comme un premier jeu.** La pente est reconnue par de petits dessins tests.

**Symbole.** ∫fφ′=-∫gφ

**Sens et domaine.** g est la dérivée distributionnelle de f lorsqu’elle appartient à l’espace exigé.

**Garde.** La pente classique peut manquer aux coins ; les traces restent importantes.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Trace au bord

**Comme un premier jeu.** Le bord garde les attaches du dessin.

**Symbole.** f(±S), f′(±S),…

**Sens et domaine.** Valeurs limites définies pour les Sobolev suffisamment réguliers en dimension un.

**Garde.** Un prolongement par zéro sans traces nulles peut créer des masses de Dirac.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Espace de Schwartz

**Comme un premier jeu.** Le dessin et ses pentes s’effacent très vite.

**Symbole.** sup |x\^mD\^nf(x)|<∞

**Sens et domaine.** Fonctions lisses à décroissance rapide, cœur fréquentiel pour les approximations.

**Garde.** Décroissance rapide n’est pas support compact.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Changement de mesure

**Comme un premier jeu.** La règle change l’épaisseur des bandes.

**Symbole.** dt=e\^(-x)dx

**Sens et domaine.** Le facteur racine dans J et ℒ conserve les normes L².

**Garde.** Oublier la racine du jacobien détruit l’isométrie.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Injection j_S

**Comme un premier jeu.** On range un dessin dans une boîte plus large.

**Symbole.** j\_S:X\_S→L²

**Sens et domaine.** Application identité sur les fonctions mais changement de norme ; compacte à S fixé.

**Garde.** Même fonction ne signifie pas même topologie.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Contraction du support

**Comme un premier jeu.** On rapproche le dessin du centre avant de lisser.

**Symbole.** D\_λf(x)=λ\^(-1/2)f(x/λ)

**Sens et domaine.** Pour 0<λ<1, réduit le support ; bornée et continue à λ=1 dans R.

**Garde.** Ne préserve pas les moments ; on les corrige après le lissage.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Convergence absolue

**Comme un premier jeu.** Toutes les briques tiennent même sans leurs signes.

**Symbole.** Σ|a\_n|<∞

**Sens et domaine.** Autorise réarrangement d’une série et facilite les échanges.

**Garde.** Ne pas présumer cette propriété dans la bande critique d’une série de Dirichlet.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Intégration par parties

**Comme un premier jeu.** On déplace la pente d’un dessin vers l’autre.

**Symbole.** ∫ψ″e\^(±x/2)=¼∫ψe\^(±x/2)

**Sens et domaine.** Identité sous traces ψ=ψ′=0, explique ℓ±Pψ=0.

**Garde.** Sans conditions de bord, des termes supplémentaires restent.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Distribution

**Comme un premier jeu.** Un dessin peut être reconnu par son effet sur les tests.

**Symbole.** δ\_a et Df au sens faible

**Sens et domaine.** Forme linéaire continue sur Cc∞ ; dérivées définies par dualité.

**Garde.** Une masse de bord change l’équation Pψ=f ; il faut annuler les traces.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Diamètre du support

**Comme un premier jeu.** On mesure la largeur de la valise.

**Symbole.** D=b-a

**Sens et domaine.** Pour supp f⊂[a,b], h\_f(t)=0 si |t|>D.

**Garde.** Le centre ne change pas le plafond e\^D ; une fenêtre plus large peut le surestimer.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Jet au bord

**Comme un premier jeu.** Les attaches du bord disparaissent jusqu’à quatre niveaux.

**Symbole.** ψ\^(j)(±S)=0, j≤3

**Sens et domaine.** Annulation d’ordre 4 de w\_S ; assure prolongement C³ et dérivées faibles L² d’ordre 4.

**Garde.** La dérivée d’ordre 4 peut sauter ; ne pas annoncer C⁴ ou C∞.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Réflexion

**Comme un premier jeu.** Le dessin passe devant le miroir.

**Symbole.** Rf(x)=f(-x)

**Sens et domaine.** Unitaire sur métriques ; Q invariant car corrélation symétrique.

**Garde.** Ce R de réflexion est distinct de la métrique R(f).

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Algèbre de convolution

**Comme un premier jeu.** Deux dessins s’assemblent en glissant.

**Symbole.** A=Cc∞(ℝ), opération \*

**Sens et domaine.** Algèbre commutative associative, sans unité parmi les fonctions ; ℒ\_exp(f\*g)=ℒ\_exp(f)ℒ\_exp(g).

**Garde.** Le produit ordinaire est une autre multiplication.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Portée exponentielle

**Comme un premier jeu.** Le dessin devient une partition de notes.

**Symbole.** ℒ\_exp f(z)=∫e\^(zx)f(x)dx

**Sens et domaine.** Fonction entière pour f compact ; variable z distincte de s Mellin, z=s-1/2.

**Garde.** Les zéros en ±1/2 sont contraintes auxiliaires, pas zéros de ζ.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Produit qui perd les moments

**Comme un premier jeu.** Deux dessins autorisés peuvent fabriquer un dessin interdit.

**Symbole.** ℓ±(f²)>0 pour f réel non nul

**Sens et domaine.** Si f∈I₁ réel non nul, f²≥0 et poids exponentiels positifs : produit hors I₁.

**Garde.** La convolution f\*f reste admissible et renforce les annulations.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.


# Niveau 4 - Les formes, opérations et invariants

## Adjoint

**Comme un premier jeu.** La machine se regarde dans la bonne balance.

**Symbole.** ⟨Af,g⟩=⟨f,A\*g⟩

**Sens et domaine.** Opérateur adjoint relativement aux domaines et à la métrique déclarés.

**Garde.** A\* dépend du produit scalaire ; les opérateurs non bornés exigent leur domaine.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Corrélation

**Comme un premier jeu.** On glisse deux dessins pour voir où ils se recouvrent.

**Symbole.** h\_ij(t)=∫f\_i(y)f̄\_j(y-t)dy

**Sens et domaine.** Corrélation croisée ; h\_ij(-t)=conj h\_ji(t).

**Garde.** Une corrélation croisée pair/impair peut être non nulle.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Corrélation symétrisée

**Comme un premier jeu.** Deux glissements opposés partagent la balance.

**Symbole.** H\_ij=(h\_ij+h\_ji)/2 pour tests réels

**Sens et domaine.** La partie réelle symétrique gouverne les matrices réelles de Q\_W.

**Garde.** Seule cette symétrisation s’annule entre parités opposées.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Polarisation

**Comme un premier jeu.** On ouvre une balance pour voir les attaches entre jouets.

**Symbole.** q(f,g) reconstruit depuis Q(f)

**Sens et domaine.** Identité de polarisation d’une forme quadratique hermitienne.

**Garde.** Le couplage est indispensable ; des diagonales positives ne suffisent pas.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Forme complète de Weil

**Comme un premier jeu.** Une balance compte tous ses plateaux.

**Symbole.** Q\_W=E\_arch-C₀||f||₂²-Q\_pr

**Sens et domaine.** E\_arch=∫₀∞w(x)||U\_xf-f||₂²dx, C₀=log(8π)+γ\_E+π/2 ; Q\_pr=2Σ Λ(n)n\^(-1/2)Re h\_f(log n).

**Garde.** Toujours utiliser la partie archimédienne ET les premiers ; le signe global reste ouvert.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Noyau archimédien

**Comme un premier jeu.** Les petits déplacements pèsent plus lourd.

**Symbole.** w(x)=e\^(-x/2)/(1-e\^(-2x))

**Sens et domaine.** Positif pour x>0 ; ~1/(2x) près de 0, décroît à l’infini.

**Garde.** Sa singularité exige un contrôle de U\_x f-f.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Forme des premiers

**Comme un premier jeu.** Les tours premières mettent des poids sur la balance.

**Symbole.** Q\_pr=2Σₚ,m log p·p\^(-m/2)Re h\_f(m log p)

**Sens et domaine.** Somme finie à support de diamètre D : p\^m≤e\^D.

**Garde.** Chaque corrélation peut changer de signe ; cette partie n’est pas positive en général.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Métrique logarithmique R

**Comme un premier jeu.** On mesure la taille et les petits glissements.

**Symbole.** R(f)=||f||₂²+E\_arch(f)

**Sens et domaine.** Forme positive fermée de multiplicateur 1+a(τ), indépendante des premiers et de RH.

**Garde.** Domaine X\_S plus large que H¹ ; le Riesz change quand on change de métrique.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Poids logarithmique a

**Comme un premier jeu.** Les rythmes rapides finissent par peser lourd.

**Symbole.** a(τ)=2Σₙ≥₀ τ²/[β\_n(β\_n²+τ²)], β\_n=2n+1/2

**Sens et domaine.** Positif, monotone en |τ|, tend vers l’infini ; multiplicateur de E\_arch.

**Garde.** Il contrôle une queue fréquentielle, pas le signe arithmétique à lui seul.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Domaine logarithmique X_S

**Comme un premier jeu.** Une boîte dont la règle surveille les glissements.

**Symbole.** supp f⊂[-S,S], R(f)<∞, ℓ±f=0

**Sens et domaine.** Hilbert avec métrique R ; cœur admissible Cc∞ dense ; injection compacte dans L².

**Garde.** La compactité vaut à S fixé ; ses constantes ne sont pas uniformes en S.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Riesz dans H¹

**Comme un premier jeu.** La balance devient une machine sur les dessins.

**Symbole.** Q\_W(f,g)=⟨T\_Sf,g⟩H¹

**Sens et domaine.** T\_S signé, borné, autoadjoint et compact sur E\_S.

**Garde.** Aucune marge c>0 dans H¹ sur tout E\_S, même si la forme est positive.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Riesz dans R

**Comme un premier jeu.** Le même dessin est l’identité moins une correction.

**Symbole.** Q\_W(f,g)=⟨(I-K\_S)f,g⟩R

**Sens et domaine.** K\_S compact autoadjoint sur X\_S ; finitement de directions négatives à S fixé.

**Garde.** Cela ne dit pas que leur nombre est zéro.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Opérateur compact

**Comme un premier jeu.** Beaucoup de dessins tiennent dans quelques petites boîtes.

**Symbole.** A(ball) relativement compact

**Sens et domaine.** Les images de suites bornées ont des sous-suites convergentes.

**Garde.** Compact ne signifie pas positif ; ses valeurs propres peuvent s’approcher de zéro.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Coercivité

**Comme un premier jeu.** La balance garde toujours une marge minimale.

**Symbole.** Q(f)≥c||f||², c>0

**Sens et domaine.** Minoration uniforme dans une métrique donnée.

**Garde.** La positivité Q≥0 est plus faible ; la marge H¹ uniforme est exclue ici.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Matrice de Gram

**Comme un premier jeu.** Une table dit comment les dessins se chevauchent.

**Symbole.** B\_ij=⟨f\_i,f\_j⟩H¹

**Sens et domaine.** B positive définie pour une famille indépendante ; ici rationnelle exacte.

**Garde.** B ne doit pas être identifiée à G\_W, la forme dont le signe est recherché.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Compression de Weil

**Comme un premier jeu.** On prend une petite fenêtre dans une grande balance.

**Symbole.** (G\_W)\_ij=Q\_W(f\_i,f\_j)

**Sens et domaine.** Matrice hermitienne finie sur un sous-espace admissible.

**Garde.** Un résultat fini ne vaut que sur ce sous-espace.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Paire de matrices

**Comme un premier jeu.** Deux balances suivent les mêmes coordonnées.

**Symbole.** G\_Wv=λBv

**Sens et domaine.** Problème spectral généralisé avec B>0.

**Garde.** Transformer G\_W exige de transformer B simultanément.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Changement de base

**Comme un premier jeu.** On renomme les pièces du puzzle.

**Symbole.** G↦C\*GC, B↦C\*BC

**Sens et domaine.** C inversible ; inertie de G et spectre généralisé du couple conservés.

**Garde.** Entrées, valeurs propres ordinaires et pivots ne sont pas tous conservés.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Cholesky

**Comme un premier jeu.** On remet la règle de mesure à plat.

**Symbole.** B=LL\*

**Sens et domaine.** Factorisation pour B hermitienne positive définie ; normalise la paire.

**Garde.** Une base très mal conditionnée demande une précision contrôlée.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Valeur propre

**Comme un premier jeu.** Un dessin ressort dans sa propre direction.

**Symbole.** Av=λv

**Sens et domaine.** λ indique la dilatation sur une direction ; pour hermitien λ réel.

**Garde.** Une valeur calculée sans intervalle d’erreur reste numérique.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Inertie

**Comme un premier jeu.** On compte les directions qui montent, descendent ou restent à zéro.

**Symbole.** (n₊,n₋,n₀)

**Sens et domaine.** Signature d’une forme hermitienne ; invariante sous congruence inversible.

**Garde.** Le nombre de directions négatives fini n’est pas leur absence.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Parité

**Comme un premier jeu.** Deux dessins : miroir pareil ou miroir opposé.

**Symbole.** f(-x)=±f(x)

**Sens et domaine.** Q\_W et les métriques respectent la réflexion ; blocs pair/impair découplés.

**Garde.** Un changement de base mêlant ces secteurs peut créer des entrées croisées.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Complément de Schur

**Comme un premier jeu.** Le nouveau jouet tire sur les attaches des anciens.

**Symbole.** δ=a-c\*G\^(-1)c

**Sens et domaine.** Si G>0, δ est le minimum résiduel ; sinon identité algébrique sous inversibilité.

**Garde.** Si G est singulière positive, il faut c∈Ran G et G†.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Pseudo-inverse

**Comme un premier jeu.** La machine inverse ce qu’elle sait voir.

**Symbole.** G†

**Sens et domaine.** Inverse sur les valeurs propres non nulles, zéro sur le noyau.

**Garde.** Ne répare pas un couplage hors de l’image.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Drapeau de sous-espaces

**Comme un premier jeu.** On ouvre des boîtes dans un ordre choisi.

**Symbole.** V₁⊂V₂⊂…

**Sens et domaine.** Une chaîne fixe sert à définir les dettes successives.

**Garde.** Changer l’ordre change les pivots ; l’invariant de dette exige le même drapeau.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Dette normalisée

**Comme un premier jeu.** La nouvelle charge est mesurée avec la même règle.

**Symbole.** δ\_G/δ\_B

**Sens et domaine.** Invariant sous changement de base ancien et v↦αv+w ancien, pour drapeau fixé et inverses valides.

**Garde.** Ce quotient n’est pas invariant sous changement arbitraire du drapeau.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Image et noyau

**Comme un premier jeu.** Ce que la machine peut produire, et ce qu’elle efface.

**Symbole.** Ran G, ker G

**Sens et domaine.** Sous-espaces ; pour G hermitienne finie, Ran G=(ker G)⊥.

**Garde.** Dans Schur singulier, c hors de Ran G crée une direction négative.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Déterminant

**Comme un premier jeu.** On mesure si un puzzle aplati perd une direction.

**Symbole.** det G

**Sens et domaine.** Produit des valeurs propres en dimension finie ; zéro si matrice singulière.

**Garde.** Un déterminant positif seul ne garantit pas une forme positive.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Décomposition LDL*

**Comme un premier jeu.** On ouvre la balance pivot par pivot.

**Symbole.** G=LDL\*

**Sens et domaine.** Factorisation avec pivotage adapté ; D porte l’inertie.

**Garde.** Les petits pivots et les permutations doivent être contrôlés ; ils dépendent du drapeau.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Plafond premier exact

**Comme un premier jeu.** On ferme la liste de briques sans en oublier une.

**Symbole.** X=⌊e\^(2S)⌋

**Sens et domaine.** Encadrement rationnel Taylor inférieur/supérieur avec même partie entière.

**Garde.** Le plafond exact ne certifie pas les poids logarithmiques ni la quadrature archimédienne.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Forme hermitienne

**Comme un premier jeu.** Le miroir répond dans l’autre sens.

**Symbole.** q(g,f)=conj q(f,g)

**Sens et domaine.** Garantit Q(f)=q(f,f) réel ; symétrie de la forme complète.

**Garde.** Réel ne signifie pas positif.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Norme d’opérateur

**Comme un premier jeu.** Le plus grand agrandissement possible.

**Symbole.** ||A||=sup\_||f||=1||Af||

**Sens et domaine.** Dépend des normes de départ et d’arrivée ; contrôlée par une borne effective.

**Garde.** Une petite entrée matricielle ne donne pas une petite norme globale sans estimation.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Reste de Taylor positif

**Comme un premier jeu.** On compte les petites piles encore oubliées.

**Symbole.** e\^x=Σₖ≤N x\^k/k!+reste

**Sens et domaine.** Pour x≥0, termes positifs et borne géométrique si x<N+2.

**Garde.** Le reste rationnel n’est pas une certification de toutes les autres fonctions transcendantes.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Calcul complexe des formes

**Comme un premier jeu.** Chaque flèche tire sur toutes les autres.

**Symbole.** Q(Σc\_i f\_i)=c\*G c

**Sens et domaine.** Une base réelle avec matrice réelle symétrique se complexifie hermitiennement ; critère PSD identique.

**Garde.** Cela couvre les combinaisons complexes de cette famille, pas tout paramètre A d’autres constructions du corpus.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Parties réelle et imaginaire

**Comme un premier jeu.** Deux dessins réels portent une flèche complexe.

**Symbole.** f=u+iv, Q(f)=Q(u)+Q(v)

**Sens et domaine.** Pour une forme à coefficients réels symétriques, les termes mixtes s’annulent.

**Garde.** La propriété dépend de la forme réelle ; les phases d’autres paramètres peuvent rester dans ses coefficients.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Défaut de translation

**Comme un premier jeu.** On compare le dessin à son petit déplacement.

**Symbole.** ||U\_xf-f||²=2||f||²-2Re h\_f(x)

**Sens et domaine.** Identité exacte L² ; pour H¹, défaut≤x²||f′||².

**Garde.** Le défaut est positif, mais Q\_W soustrait aussi une masse et les premiers.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Matrice de correction

**Comme un premier jeu.** Deux retouches règlent deux balances.

**Symbole.** [[A,-A/2],[A,A/2]]

**Sens et domaine.** Pour φ paire et A=∫φe\^(x/2)>0, moments de φ,φ′ donnent déterminant A².

**Garde.** L’ordre des lignes ± et les signes doivent rester annoncés.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Énergie de déplacement

**Comme un premier jeu.** Les petits glissements paient une contribution positive.

**Symbole.** E\_arch=∫w||U\_xf-f||²

**Sens et domaine.** Forme positive, fermée par multiplicateur Fourier a(τ).

**Garde.** E\_arch seule n’est pas Q\_W ; soustractions arithmétiques restent présentes.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Terme croisé

**Comme un premier jeu.** Une attache relie deux jouets.

**Symbole.** 2Re(c̄\_i c\_j q(f\_i,f\_j))

**Sens et domaine.** Partie indispensable d’une forme sur une somme.

**Garde.** Sa phase peut rendre négative une somme à diagonales positives.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Découpage tête et queue

**Comme un premier jeu.** Une boîte petite et tout ce qui reste.

**Symbole.** X\_S=V⊕\_R V⊥

**Sens et domaine.** Décomposition orthogonale R ; blocs de Q et couplages définis.

**Garde.** La tête et la queue sont liées par G₀₁ ; elles ne sont pas deux tests indépendants.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Transposée conjuguée

**Comme un premier jeu.** On échange lignes et colonnes avec leur miroir.

**Symbole.** C\*=conj Cᵀ

**Sens et domaine.** Adjoint matriciel pour métrique euclidienne ; congruence utilise C\*GC.

**Garde.** Pour métrique B, l’adjoint opérateur est B\^(-1)C\*B si inverses valides.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Codimension

**Comme un premier jeu.** Deux balances retirent deux libertés.

**Symbole.** codim E\_S=2

**Sens et domaine.** Deux moments indépendants continus coupent un sous-espace fermé.

**Garde.** Codimension finie n’implique pas dimension finie du domaine.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Dualité

**Comme un premier jeu.** Un petit capteur lit un dessin.

**Symbole.** ℓ(f)

**Sens et domaine.** Fonctionnelle linéaire continue sur l’espace choisi ; normes et adjoints associés.

**Garde.** Un capteur qui ne lit rien peut laisser des modes invisibles.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Série du noyau

**Comme un premier jeu.** Le poids est une pile de petites décroissances.

**Symbole.** w(x)=Σₙ≥₀e\^(-β\_nx)

**Sens et domaine.** Série positive pour x>0 ; Tonelli produit la série de a(τ).

**Garde.** Le calcul spectral emploie des termes positifs du noyau, pas des zéros de ζ.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Polynôme de corrélation

**Comme un premier jeu.** Deux dessins polynomiaux se recouvrent exactement.

**Symbole.** h\_ij(Sz)=polynôme rationnel, 0≤z≤2

**Sens et domaine.** Intégrale symbolique sur [z-1,1], calcul par fractions rationnelles.

**Garde.** Ce polynôme vaut sur l’intervalle indiqué ; hors recouvrement la corrélation est zéro.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Identité de métrique du moule

**Comme un premier jeu.** Le moule donne aussi une règle exacte.

**Symbole.** ||Pψ||H¹²=||ψ‴||²+3/2||ψ″||²+9/16||ψ′||²+1/16||ψ||²

**Sens et domaine.** Intégration par parties dans H₀³ ; constantes d’équivalence indépendantes de S.

**Garde.** Cette identité concerne la métrique B, pas Q\_W.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Conditionnement

**Comme un premier jeu.** Une règle presque écrasée rend les lectures fragiles.

**Symbole.** κ(B)=λ\_max(B)/λ\_min(B)

**Sens et domaine.** Mesure spectrale pour B>0 euclidien ; amplifie les erreurs de normalisation.

**Garde.** Diffère des autres κ du corpus ; sa valeur est propre à la base.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## PSD et marge

**Comme un premier jeu.** La balance tient ou garde une marge.

**Symbole.** G⪰0 versus G⪰cB

**Sens et domaine.** Première propriété admet directions nulles ; seconde impose c>0 dans la métrique B.

**Garde.** La seconde est impossible pour toute E\_S avec B\_H¹ ; la première reste ouverte.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Équivalence des normes du moule

**Comme un premier jeu.** Le moule fournit deux règles qui ne se contredisent pas.

**Symbole.** 1/16||ψ||H³²≤||Pψ||H¹²≤3/2||ψ||H³²

**Sens et domaine.** Constantes exactes et indépendantes de S avec norme H³ somme des dérivées.

**Garde.** Ces constantes ne sont pas des marges positives de Q\_W.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Idéaux de jets admissibles

**Comme un premier jeu.** Plus de balances sont attachées aux deux portes.

**Symbole.** I\_r={f∈A : ∫x\^j e\^(±x/2)f=0, j<r}

**Sens et domaine.** Idéaux de convolution ; I₀=A ; I\_r\*I\_s⊂I\_(r+s), somme dans I\_min(r,s).

**Garde.** Les unités d’amplitude se multiplient ; convolution n’implique pas positivité de Q\_W.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Arithmétique des fonctions

**Comme un premier jeu.** Quatre gestes ont chacun leur règle de montage.

**Symbole.** addition, scalaire, produit, convolution

**Sens et domaine.** Somme/scalaire conservent I\_r ; convolution additionne les ordres garantis ; produit ordinaire peut perdre I₁.

**Garde.** Ni D\_x ni U\_a ne sont des homomorphismes de convolution dans le sens naïf.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Dérivation pour convolution

**Comme un premier jeu.** Le bouton position se partage entre deux dessins.

**Symbole.** x(f\*g)=(xf)\*g+f\*(xg)

**Sens et domaine.** Multiplication par x est une dérivation de l’algèbre de convolution ; D\_x(f\*g)=Df\*g=f\*Dg.

**Garde.** D\_x est dérivation du produit ordinaire, pas de la convolution.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Échelle de jets par P

**Comme un premier jeu.** Le moule ferme une balance de plus à chaque porte.

**Symbole.** ℒ\_exp(Pf)=(z²-1/4)ℒ\_exp f

**Sens et domaine.** P:I\_r→I\_(r+1) sur graines Cc∞ ; x:I\_(r+1)→I\_r ; D\_x:I\_r→I\_r.

**Garde.** Ordre garanti au moins ; certaines annulations supplémentaires peuvent apparaître.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Jets ordinaires en zéro

**Comme un premier jeu.** Une nouvelle balance lit les rythmes lents.

**Symbole.** ℒ\_exp\^(j)f(0)=∫x\^j f(x)dx

**Sens et domaine.** L’annulation d’ordre q en 0 définit la queue Y\_(q-1) ; D\_x gagne un ordre en 0 et P le conserve.

**Garde.** Ce point du test n’est pas un zéro critique de ζ.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Quotient de jets

**Comme un premier jeu.** Deux petits carnets gardent les premiers traits du dessin.

**Symbole.** A/I\_r ≃ ℂ[ε]/(ε\^r) ⊕ ℂ[ε]/(ε\^r)

**Sens et domaine.** Jets normalisés ℒ\_exp\^(j)f(±1/2)/j! ; produit de coefficients tronqué ; codimension 2r.

**Garde.** Le quotient oublie tous les autres traits ; r>1 ne couvre pas tous les tests de I₁.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Idéal de convolution

**Comme un premier jeu.** Une porte fermée reste fermée quand on colle un autre dessin.

**Symbole.** I\_r\*A⊂I\_r

**Sens et domaine.** Sous-espace stable sous convolution par toute graine ; somme conserve l’ordre minimal garanti.

**Garde.** Idéal ici se rapporte à convolution, pas au produit ordinaire.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Polynôme tronqué

**Comme un premier jeu.** Un carnet efface tous les traits trop hauts.

**Symbole.** ℂ[ε]/(ε\^r)

**Sens et domaine.** Addition coefficient par coefficient et produit Cauchy avec ε\^r=0 ; représentation exacte d’un jet d’ordre r-1.

**Garde.** Ce ε formel est distinct de l’erreur ε\_N(T).

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Deux moules compatibles

**Comme un premier jeu.** Deux clés ferment les portes et les rythmes lents.

**Symbole.** D\_x\^q P\^r ψ∈I\_r∩Y\_(q-1)

**Sens et domaine.** D\_x et P commutent ; ℒ\_exp multiplie par (-z)\^q(z²-1/4)\^r ; support contenu dans celui de la graine.

**Garde.** La construction peut être dans une queue positive sans couvrir la tête où le signe est inconnu.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.


# Niveau 5 - Les contrats de recherche et leurs limites

## Queue de l’opérateur

**Comme un premier jeu.** Les jouets restants ne peuvent plus faire basculer seuls la balance.

**Symbole.** ||K\_S|V⊥||<1

**Sens et domaine.** Une queue coercive explicite est construite par moments ordinaires ; le taux pour la queue orthogonale de la base brute f\_k reste à établir.

**Garde.** Ne pas identifier la queue de moments avec le complément de span(f\_k).

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Réduction par queue et Schur

**Comme un premier jeu.** On range l’infini et l’on garde ses attaches exactes.

**Symbole.** G\_eff=G₀₀-G₀₁G₁₁\^(-1)G₁₀

**Sens et domaine.** Si le bloc de queue est uniformément positif, signe global équivalent au Schur fini.

**Garde.** Une compression finie positive sans borne de queue ne suffit pas.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Densité d’une famille

**Comme un premier jeu.** Les petits dessins peuvent approcher tous les dessins.

**Symbole.** closure(∪V\_n)=E\_S

**Sens et domaine.** Ici densité de P[w\_S·polynômes] dans H¹ ; puis dans X\_S par le cœur.

**Garde.** Dense ne signifie pas que le signe est positif sur cette famille.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Quantificateur global

**Comme un premier jeu.** Chaque boîte et chaque taille doivent être couvertes.

**Symbole.** ∀S>0, ∀n≥1

**Sens et domaine.** Une preuve globale exige tous les supports et tous les tests via cœur et continuité.

**Garde.** Une extension de plafond couvre quelques indices supplémentaires seulement.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Bellman des contrats

**Comme un premier jeu.** On choisit un coup qui ouvre plusieurs portes.

**Symbole.** V(s)=max\_a E[r(s,a)+γV(s′)]

**Sens et domaine.** s porte objets, obligations et preuves ; actions ont résultats conditionnels et coûts ; ici horizon fini γ=1.

**Garde.** Le score de recherche n’est ni une probabilité de RH ni la forme de Weil.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Portes ET et OU

**Comme un premier jeu.** Deux clés pour une porte, ou deux portes possibles.

**Symbole.** ET: tous ; OU: un chemin valide

**Sens et domaine.** Graphe d’obligations avec complémentarités ; utile pour les coups doubles.

**Garde.** Une flèche logique est autorisée seulement si son contrat est prouvé.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Jet

**Comme un premier jeu.** On garde le dessin, la pente et les courbures.

**Symbole.** J\^mF(z)=(F,F′,…,F\^(m))(z)

**Sens et domaine.** Données locales jusqu’à un ordre fini.

**Garde.** Un jet local n’indique pas à lui seul la branche globale suivie.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Branche

**Comme un premier jeu.** Un chemin local à travers une forêt.

**Symbole.** F(z,t)=0, z=z(t)

**Sens et domaine.** Si ∂\_zF≠0, fonction implicite locale ; près d’un zéro multiple il faut un autre modèle.

**Garde.** Continuer à travers une collision nécessite conditions et choix ; sujet encore ouvert du corpus.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Collision de zéros

**Comme un premier jeu.** Deux chemins se touchent.

**Symbole.** F=∂\_zF=0

**Sens et domaine.** Système local de dégénérescence ; jets, discriminant ou préparation locale à spécifier.

**Garde.** Une collision certifiée locale ne contrôle pas tous les passages globaux.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Discriminant

**Comme un premier jeu.** Une alarme quand deux racines se rejoignent.

**Symbole.** Disc(P)=0

**Sens et domaine.** Pour un polynôme, détecte racines multiples ; extension locale à préciser.

**Garde.** Ne pas appliquer la formule polynomiale directement à une fonction entière quelconque.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Coefficient complexe A

**Comme un premier jeu.** Une flèche peut tourner et grandir.

**Symbole.** A∈ℂ

**Sens et domaine.** Paramètre de certaines familles du corpus ; |A|²≥0, mais les termes croisés gardent la phase.

**Garde.** Un argument limité à A réel positif ne couvre pas A complexe arbitraire.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Trace et correspondances de Weil

**Comme un premier jeu.** Une règle relie les allers et les retours.

**Symbole.** σ(ξξ′)>0 dans le cadre géométrique

**Sens et domaine.** Positivité des correspondances dans la preuve sur les courbes sur corps finis ; source Wei48.

**Garde.** Aucun transfert de cette géométrie à ζ des entiers n’est démontré.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Frobenius

**Comme un premier jeu.** On répète un geste exact dans un monde fini.

**Symbole.** Frob:x↦x\^q

**Sens et domaine.** Morphisme en caractéristique p ; action cohomologique avec trace dans le cadre approprié.

**Garde.** Un opérateur virtuel aux mêmes valeurs propres n’est pas automatiquement un morphisme.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Riemann–Roch

**Comme un premier jeu.** On compte les dessins autorisés et les contraintes.

**Symbole.** ℓ(D)-ℓ(K-D)=deg D+1-g

**Sens et domaine.** Théorème pour un diviseur sur une courbe lisse projective ; géométrie nécessaire.

**Garde.** Un bilan formel de dimensions ne construit pas une courbe pour ζ.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Marge spectrale

**Comme un premier jeu.** On cherche le plus petit espace sous la balance.

**Symbole.** inf spec(A)

**Sens et domaine.** Dépend de l’opérateur et de sa métrique ; existence ou borne certifiée à distinguer.

**Garde.** La marge R éventuelle peut dépendre de S ; la marge H¹ strictement positive est impossible ici.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Certificat

**Comme un premier jeu.** On garde une règle qui encadre le résultat.

**Symbole.** borne d’erreur + décision

**Sens et domaine.** Calcul rationnel exact ou intervalle validé et toutes conditions contrôlées.

**Garde.** Deux précisions concordantes ne remplacent pas une borne d’erreur.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Calcul par intervalles

**Comme un premier jeu.** Le résultat habite une petite boîte fermée.

**Symbole.** x∈[a,b]

**Sens et domaine.** Arithmétique à arrondi dirigé et propagation rigoureuse des inclusions.

**Garde.** Une valeur à beaucoup de chiffres n’est pas un intervalle validé.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Stabilité d’un signe

**Comme un premier jeu.** La balance ne bascule pas malgré une petite secousse.

**Symbole.** |erreur|<marge

**Sens et domaine.** Perturbation contrôlée d’une forme ou d’un spectre.

**Garde.** Le couplage et le conditionnement amplifient l’erreur ; il faut les borner.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Invariant symbolique

**Comme un premier jeu.** Un signe survit à la traduction.

**Symbole.** I(Tx)=I(x)

**Sens et domaine.** Une quantité conservée par une transformation définie avec ses conditions.

**Garde.** Un même symbole écrit deux fois n’est pas un invariant.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Invariant relationnel

**Comme un premier jeu.** Les attaches survivent même si les pièces changent.

**Symbole.** R(x,y)⇒R(Tx,Ty)

**Sens et domaine.** Moments nuls, incidence de sous-espaces, congruence simultanée, ordre d’un drapeau.

**Garde.** Une relation peut être conservée sans conserver les valeurs numériques.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Grammaire des passages

**Comme un premier jeu.** Les mots savent quelles phrases ils peuvent former.

**Symbole.** objet : domaine → codomaine ; garde ; coût

**Sens et domaine.** Contrat de traduction typé, preuve et perte séparées ; validateur programmé.

**Garde.** La validation vérifie le contrat codé, pas une preuve automatique de toutes les mathématiques.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Utilité de recherche

**Comme un premier jeu.** On compte les portes réellement ouvertes.

**Symbole.** U\_decision≠U\_a

**Sens et domaine.** Choix éditorial de gains sur obligations ; aucune unité physique.

**Garde.** Ne pas confondre U\_decision avec la translation U\_a.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Les différents G

**Comme un premier jeu.** Quatre boîtes ne portent plus la même étiquette.

**Symbole.** G\_log(s), G\_NB, G\_W, B

**Sens et domaine.** G\_log désigne un logarithme local selon le document ; G\_NB un Gram ; G\_W une compression ; B la métrique externe.

**Garde.** La désambiguïsation exige le document ; le symbole G seul ne donne pas le domaine.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Les différents D

**Comme un premier jeu.** Trois gestes portent des noms complets.

**Symbole.** D\_x, D\_mult, D\_Frob

**Sens et domaine.** D\_x dérive ; D\_mult mesure un défaut multiplicatif ; un logarithme de Frobenius exige une branche et un domaine.

**Garde.** Ne pas composer ces symboles comme s’ils étaient la même machine.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Projection

**Comme un premier jeu.** On garde la partie qui entre dans une boîte.

**Symbole.** Π\_V f

**Sens et domaine.** Projection orthogonale dans une métrique annoncée ; Π\_V²=Π\_V.

**Garde.** Ce P/Π n’est pas le moule D²-1/4 ; projection H¹ et projection R diffèrent.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Polynôme

**Comme un premier jeu.** Un dessin fabriqué par quelques briques de puissances.

**Symbole.** P\_poly(u)=Σc\_k u\^k

**Sens et domaine.** Fonction algébrique de variable déclarée ; zêta polynomiale en corps fini selon le contexte.

**Garde.** Ce P n’est pas l’opérateur différentiel.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Les différentes κ

**Comme un premier jeu.** Deux petites étiquettes doivent garder leur boîte.

**Symbole.** κ\_Li, κ\_pli

**Sens et domaine.** Coefficient ou paramètre selon le document ; définition locale obligatoire.

**Garde.** Aucune égalité entre les κ n’est fournie par leur seule lettre.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Tonelli et échange positif

**Comme un premier jeu.** On compte les mêmes briques dans deux ordres.

**Symbole.** ∫Σ f\_n=Σ∫f\_n si f\_n≥0

**Sens et domaine.** Autorise l’échange pour fonctions mesurables non négatives, même si valeur infinie.

**Garde.** Pour des termes signés, il faut d’autres hypothèses de domination/convergence.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Plancherel

**Comme un premier jeu.** La même chanson a la même taille sur deux portées.

**Symbole.** ||f||₂=||f̂||₂

**Sens et domaine.** Isométrie Fourier L² avec normalisation unitaire.

**Garde.** L’égalité L² seule ne donne pas les domaines des formes plus fortes.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Commutateur

**Comme un premier jeu.** Deux gestes changent selon leur ordre.

**Symbole.** [P,M\_τ]=M\_τ(2iτD-τ²)

**Sens et domaine.** P M\_τψ=M\_τ(Pψ+2iτψ′-τ²ψ).

**Garde.** Il explique pourquoi moduler la graine puis appliquer P n’est pas moduler le test seul.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Pont régularisé

**Comme un premier jeu.** On déplace, lisse, range et passe dans le moule.

**Symbole.** T=P[χ(η\_δ\*Γ\_Sg)]

**Sens et domaine.** Γ\_S est le décalage de l’entrée prolongée par zéro ; sortie admissible ; coût δ\^(-3) en H¹ sous cutoffs fixés.

**Garde.** Le coût et les limites doivent être uniformisés avant de conclure globalement.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Correction des moments

**Comme un premier jeu.** Deux petites retouches remettent les balances à zéro.

**Symbole.** f↦f-aφ-bφ′

**Sens et domaine.** Matrice des moments de φ et φ′ inversible pour φ paire non nulle positive ; correction continue.

**Garde.** Il faut un support intérieur commun et des coefficients calculés, pas une correction abstraite gratuite.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Rabais Bellman γ

**Comme un premier jeu.** Les coups éloignés peuvent peser moins lourd.

**Symbole.** 0≤γ≤1

**Sens et domaine.** Paramètre de décision, ici γ=1 à horizon fini pour les contrats.

**Garde.** γ\_decision n’est ni Γ fonction spéciale ni γ\_E constante d’Euler.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Principe variationnel

**Comme un premier jeu.** On cherche le dessin qui fait descendre le plus la balance.

**Symbole.** λ\_min=inf Q(f)/R(f)

**Sens et domaine.** Quotient de Rayleigh dans la métrique annoncée ; restriction finie donne un diagnostic.

**Garde.** Une infimum sur un petit sous-espace peut manquer une direction négative ailleurs.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Erreur de famille

**Comme un premier jeu.** Les petites dettes disparaissent dans toutes les boîtes.

**Symbole.** G\_n≥-ε\_n B\_n, ε\_n→0

**Sens et domaine.** Avec famille imbriquée dense et continuité, cette borne pour tout n implique Q\_W≥0.

**Garde.** Une suite de bornes non certifiées ou sans tous les n ne remplit pas le contrat.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Défaut de transport

**Comme un premier jeu.** On mesure ce qu’une traduction abîme.

**Symbole.** |q(Tf,Tg)-q(f,g)|

**Sens et domaine.** Différence de formes sur domaines compatibles, bornée par normes et erreurs de T.

**Garde.** Une transformation non isométrique exige cette comptabilité.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Indice négatif

**Comme un premier jeu.** Combien de directions font pencher vers le bas.

**Symbole.** ind₋(Q)

**Sens et domaine.** Dimension maximale d’un sous-espace où Q<0 ; finie à S fixé via I-compact.

**Garde.** Fini ne signifie pas zéro et ne couvre pas tous les supports.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Projection fréquentielle

**Comme un premier jeu.** On écoute seulement les rythmes assez lents.

**Symbole.** Π\_T=ℱ\^(-1)1\_[-T,T]ℱ

**Sens et domaine.** Projection orthogonale L² ; queue contrôlée par 1+a(T) dans R.

**Garde.** Elle ne conserve pas le support compact ni les moments ; c’est un outil d’estimation, pas un test admissible automatique.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Support et temps logarithmique

**Comme un premier jeu.** On transforme les tailles en positions.

**Symbole.** x=log u, D=diam supp f

**Sens et domaine.** Nombre de premiers en jeu lié à e\^D ; support centré n’est qu’une convention.

**Garde.** Ne pas identifier ce x à un temps physique ni réduire le diamètre à la position du centre.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Rigidité de Hamburger

**Comme un premier jeu.** Les règles complètes forcent une chanson précise.

**Symbole.** équation fonctionnelle + série + croissance

**Sens et domaine.** Dans le cadre Ham21, les hypothèses complètes imposent F=cζ ; voir source corrigée document 67.

**Garde.** L’équation fonctionnelle isolée ne suffit pas.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Contre-exemple local

**Comme un premier jeu.** Un seul jouet peut montrer qu’une règle casse.

**Symbole.** ∃x : propriété fausse

**Sens et domaine.** Réfute la proposition avec ses hypothèses exactes ; un témoin numérique demande une certification.

**Garde.** Fermer un candidat ne ferme pas RH ni toutes les autres routes.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## État épistémique

**Comme un premier jeu.** La carte garde ce qui a été construit.

**Symbole.** s=(objets, preuves, obligations)

**Sens et domaine.** État du protocole, résultats et limites, horodatage avant les expériences.

**Garde.** Un résultat appris ensuite ne doit pas être présenté comme une prévision préalable.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Coup double

**Comme un premier jeu.** Une clé ouvre deux portes liées.

**Symbole.** action→deux contrats vérifiés

**Sens et domaine.** Ici P : moments+norme ; parité : réduction+contre-épreuve ; R : domaine+queue finie.

**Garde.** Deux noms nouveaux ne comptent pas comme deux preuves.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Critère Nyman–Beurling

**Comme un premier jeu.** Approcher un dessin simple suffit dans le bon monde.

**Symbole.** 1∈closure span{ρ\_θ avec moments}

**Sens et domaine.** Équivalence à RH sous l’énoncé et la norme exacts de Beurling ; voir document 67.

**Garde.** La densité de toute entrée L² après régularisation n’est pas la densité des entrées NB.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Erreur d’approximation

**Comme un premier jeu.** Les petites boîtes manquent encore une partie du dessin.

**Symbole.** ||(I-Π\_N)j\_S||

**Sens et domaine.** Norme de l’injection compacte après projection finie dans la métrique cible.

**Garde.** Existence d’une limite zéro ne fournit pas son taux certifié.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Budget arithmétique L²

**Comme un premier jeu.** On compte tout le poids qui peut tirer la balance.

**Symbole.** M\_S=C₀+1+2Σₚᵐ≤e²ˢ log p·p\^(-m/2)

**Sens et domaine.** Borne de |(C₀+1)⟨f,g⟩+q\_pr(f,g)|≤M\_S||f||||g||.

**Garde.** Budget valable à S fixé, croît avec le support ; ne donne pas le signe.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Porte de queue positive

**Comme un premier jeu.** Les jouets restants ne tirent plus assez fort.

**Symbole.** ||j\_S|V⊥||² M\_S<1

**Sens et domaine.** La queue de moments Y\_N satisfait la condition par la borne ε\_N(T) ; existence et paramètres explicites prouvés.

**Garde.** Queue positive seule ne rend pas la tête positive ; le Schur complet demeure nécessaire.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Obligation globale de signe

**Comme un premier jeu.** Toutes les dernières balances doivent tenir.

**Symbole.** ∀S, G\_eff,S⪰0

**Sens et domaine.** Après queue certifiée, résoudre le Schur fini pour chaque S, ou une loi uniforme couvrante.

**Garde.** Ni l’existence du Schur ni les expériences finies n’acquittent cette obligation.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Résolvante

**Comme un premier jeu.** On cherche comment une machine répond à une sollicitation.

**Symbole.** (A-zI)\^(-1)

**Sens et domaine.** Définie pour z hors du spectre avec domaines fixés ; utile au contrôle de queue.

**Garde.** Une résolvante postulée sans exclusion spectrale est circulaire.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Spectre essentiel

**Comme un premier jeu.** La grande foule des rythmes reste autour d’un.

**Symbole.** spec\_ess(I-K)={1}

**Sens et domaine.** Pour K compact autoadjoint sur un Hilbert infini ; seules exceptions discrètes ailleurs.

**Garde.** Cela autorise des valeurs négatives isolées ; aucun signe global automatique.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Rang fini

**Comme un premier jeu.** Quelques gestes suffisent pour cette machine.

**Symbole.** A\_N=Σₖ≤N u\_k⟨v\_k,·⟩

**Sens et domaine.** Image de dimension finie ; approxime en norme les compacts sur Hilbert.

**Garde.** La possibilité d’approximer ne fournit pas les coefficients ni leur erreur certifiée.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Série de Neumann

**Comme un premier jeu.** On corrige le dessin par petits retours de plus en plus faibles.

**Symbole.** (I-K)\^(-1)=Σₙ≥₀K\^n si ||K||<1

**Sens et domaine.** Inverse borné avec contrôle 1/(1-||K||).

**Garde.** Utilisable pour le bloc de queue seulement après une borne stricte.

**Ancrage.** Document 68 ; V644\_LANGUE\_ET\_DOMAINES.md, L1-L7 ; preuve auxiliaire interne ; portée et conditions dans L1-L7.

## Métrique indépendante

**Comme un premier jeu.** La règle doit exister avant la décision de la balance.

**Symbole.** R ou B définies sans Q≥0

**Sens et domaine.** Norme externe positive démontrée sans hypothèse RH ; permet un Riesz signé.

**Garde.** Définir la norme comme √Q\_W avant d’avoir prouvé Q\_W≥0 serait circulaire.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Drapeau par secteurs

**Comme un premier jeu.** On range d’abord selon les deux miroirs.

**Symbole.** V\_pair⊕V\_impair

**Sens et domaine.** Schur peut être calculé par bloc de parité ; pivot interprété dans son drapeau.

**Garde.** Comparer à un ordre mélangé nécessite garder la même extension ou signaler un nouveau drapeau.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Noyau de basse fréquence

**Comme un premier jeu.** Les rythmes lents se recouvrent dans la boîte.

**Symbole.** sin(T(x-y))/(π(x-y))

**Sens et domaine.** Noyau de 1\_[-S,S]Π\_T1\_[-S,S], compact positif à support fixé.

**Garde.** Borne de queue effective à construire avec approximation contrôlée du noyau et contraintes.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Minimum de Schur

**Comme un premier jeu.** On règle les anciens jouets pour soulager le nouveau.

**Symbole.** inf\_z Q(z+v)=δ

**Sens et domaine.** Valable si ancien bloc >0 ; formule minimisation avec z=-G\^(-1)c.

**Garde.** Si le bloc est indéfini, ce minimum vaut -∞ même si la formule algébrique existe.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Preuve de phase

**Comme un premier jeu.** Deux rotations identiques se compensent.

**Symbole.** h\_(e\^(iθ)f)=h\_f

**Sens et domaine.** Facteurs e\^(iθ) et conj e\^(iθ) s’annulent dans corrélation et normes.

**Garde.** La compensation n’a pas lieu pour une phase variable aux deux positions.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Une queue existe

**Comme un premier jeu.** Les pièces oubliées deviennent petites après la règle douce.

**Symbole.** η\_N→0

**Sens et domaine.** Compactité j\_S et exhaustion R-orthogonale dense donnent convergence en norme.

**Garde.** La vitesse et les indices de réussite doivent encore être calculés.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## R notation qualifiée

**Comme un premier jeu.** Deux boîtes séparent une lettre partagée.

**Symbole.** R\_metric, R\_reflection

**Sens et domaine.** La métrique logarithmique et l’opérateur miroir ont des rôles différents.

**Garde.** L’identifiant stable empêche une composition ambiguë.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Croissance logarithmique

**Comme un premier jeu.** Les rythmes rapides prennent un poids qui grandit doucement.

**Symbole.** a(τ) comparable à log(2+|τ|)

**Sens et domaine.** La série positive donne divergence ; comparaisons élémentaires donnent ordre logarithmique.

**Garde.** Les constantes d’une estimation effective doivent être écrites, pas remplacées par le mot comparable.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Budget de contraction

**Comme un premier jeu.** Rétrécir peut rendre les rythmes plus rapides, mais leur coût est borné.

**Symbole.** a(τ/λ)≤λ\^(-2)a(τ)

**Sens et domaine.** Termes positifs de la série de a donnent l’inégalité pour 0<λ≤1 ; continuité forte à1.

**Garde.** Ce budget ne préserve pas Q\_W ni les moments.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Transport d’opérateur

**Comme un premier jeu.** La même machine change de pièce avec sa règle.

**Symbole.** A↦UAU\^(-1) si U unitaire

**Sens et domaine.** Spectre et propriétés unitaires conservés pour domaines correctement transportés.

**Garde.** Changer la métrique de Riesz H¹→R n’est pas automatiquement cette opération.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Fonction logarithmique G(s)

**Comme un premier jeu.** Un carnet mesure la rotation d’une fonction.

**Symbole.** G(s)=Log F(s) selon archive

**Sens et domaine.** Définition dépendant d’un domaine sans zéros et d’une branche ; voir source historique locale.

**Garde.** Ne pas l’identifier au Gram ni la considérer globalement définie à travers tous les zéros.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Surface virtuelle

**Comme un premier jeu.** Un dessin ressemble à un terrain avant d’en être un.

**Symbole.** axiomes formels du corpus

**Sens et domaine.** Construction comparative/virtuelle des documents46-48, dont domaine et axiomes doivent être repris.

**Garde.** Aucune variété géométrique de ζ construite par cette seule analogie.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Zéro critique double

**Comme un premier jeu.** La note touche la ligne deux fois.

**Symbole.** F(ρ)=F′(ρ)=0, Re ρ=1/2

**Sens et domaine.** Question de multiplicité/collision avec jets certifiés locaux selon la famille.

**Garde.** RH n’impose pas la simplicité des zéros ; ne pas confondre ces deux buts.

**Ancrage.** Documents 67-68 et noyau du corpus ; définition locale explicitée dans cette fiche ; définition pédagogique ; voir portée précise dans ancrage et garde.

## Logique des domaines

**Comme un premier jeu.** La phrase dit quelle boîte le dessin peut atteindre.

**Symbole.** Γ⊢f : A(S,r,u)

**Sens et domaine.** S support, r ordre garanti de jets, u degré d’unité A ; règles sound dans A, preuves L8.

**Garde.** Pas un système complet décidant toute identité ou la vérité de RH.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Queue de moments ordinaires

**Comme un premier jeu.** Les rythmes lents deviennent minuscules après plusieurs balances.

**Symbole.** Y\_N={∫x\^j f=0, 0≤j≤N}

**Sens et domaine.** Codimension N+1 dans X\_S ; queue positive effective via Taylor Fourier et budget L².

**Garde.** Distincte des idéaux I\_r, qui utilisent les poids e\^(±x/2).

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Borne explicite de queue

**Comme un premier jeu.** On encadre les rythmes lents dans une petite boîte.

**Symbole.** ε\_N(T)=2(ST)\^(2N+3)/[π(2N+3)²((N+1)!)²]

**Sens et domaine.** Pour Y\_N, énergie Fourier dans [-T,T]≤ε\_N||f||₂² ; si ε<1, ||f||₂²≤R/[(1-ε)r(T)].

**Garde.** Borne prouvée, mais choisir des paramètres grossiers peut donner une tête astronomique.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Contrat de queue entier

**Comme un premier jeu.** Une recette ferme la queue avec des comptes entiers.

**Symbole.** Lbar=8+2M, T=2\^(8Lbar), q=ceil(6ST)

**Sens et domaine.** Pour Y\_(q-1), Q\_W≥R/(1+2Lbar) ; M nombre exact de puissances premières actives.

**Garde.** La tête a dimension q ; elle n’a pas été calculée dans cette expérience.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Erreur de dette par Neumann

**Comme un premier jeu.** Les corrections restantes ont un ticket de taille.

**Symbole.** reste≤η\^(m+1)/(1-η)

**Sens et domaine.** η=L\_S/[(1-ε)r(T)]<1 borne le compact comprimé sur la queue ; budget inverse et Schur prouvés.

**Garde.** Le solveur des actions/projections doit encore être certifié.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.

## Représentant Riesz des moments

**Comme un premier jeu.** Un capteur devient un dessin dans la bonne règle.

**Symbole.** ⟨h\_j,f⟩R=∫x\^j f(x)dx

**Sens et domaine.** Les h\_j engendrent F\_N=Y\_N⊥\_R ; codimension N+1 ; solveur et résidus à certifier.

**Garde.** Cette tête diffère du préfixe polynomial brut utilisé par les matrices exploratoires.

**Ancrage.** 3\_Preuves\_et\_calculs/preuves/V644\_LANGUE\_ET\_DOMAINES.md ; L6-L8 ; relation démontrée dans V644, L6-L8.


# Annexe - Tous les noms du registre canonique

Les 95 entrées suivantes conservent les dernières lignes nommées du registre 20. Les images historiques peuvent rester plus techniques que celles du noyau. Leur absence éventuelle de statut explicite est signalée.

## Miroir de Möbius

**Image héritée.** zéros et cancellation sont deux faces d'un même paysage

**Ancrage exact.** $1/\zeta(s)=\sum \mu(n)n^{-s}$, sommes de Möbius

**Garde héritée.** assimiler $\mu$ à des tirages indépendants exacts

**Correspondance autorisée.** traduire localisation spectrale en fluctuation arithmétique

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:11 ; 1. Tableau canonique. **Statut :** hérité du registre : MÉCANISME RETENU.

## Filtre antipôle

**Image héritée.** filtre notch supprimant un mode cohérent

**Ancrage exact.** $W_N(1)=0$

**Garde héritée.** présenter l'annulation du pôle comme un mécanisme suffisant pour RH

**Correspondance autorisée.** isoler un mode universel avant d'étudier le résidu

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:12 ; 1. Tableau canonique. **Statut :** hérité du registre : BRANCHE CLOSE / OUTIL RETENU.

## Thermomètre d'horizon

**Image héritée.** thermomètre qui mesure sans produire la température

**Ancrage exact.** énergie $Q$, exposant relié à $\Theta=\sup\Re\rho$

**Garde héritée.** demander à une norme positive de fabriquer la positivité de Weil

**Correspondance autorisée.** utiliser $Q$ comme diagnostic de croissance

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:13 ; 1. Tableau canonique. **Statut :** hérité du registre : DIAGNOSTIC EXACT.

## Effaceur orthogonal

**Image héritée.** filtre adaptatif retirant une composante structurée

**Ancrage exact.** projection Nyman-Beurling / Gram

**Garde héritée.** confondre forte corrélation finie et convergence asymptotique

**Correspondance autorisée.** quantifier l'énergie capturée par une direction

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:14 ; 1. Tableau canonique. **Statut :** hérité du registre : DIAGNOSTIC.

## Positivité porteuse

**Image héritée.** arche dont le signe porte une contrainte

**Ancrage exact.** forme hermitienne de Weil, signature, inertie

**Garde héritée.** appeler « information » toute quantité $\ge0$ par définition

**Correspondance autorisée.** distinguer une positivité arithmétique d'une somme de carrés automatique

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:15 ; 1. Tableau canonique. **Statut :** hérité du registre : CENTRAL.

## Census spectral

**Image héritée.** recenser plutôt que localiser chaque individu

**Ancrage exact.** rang, trace, inertie, proportions

**Garde héritée.** transformer une proportion en RH complète

**Correspondance autorisée.** obtenir des résultats proportionnels sans localisation totale

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:16 ; 1. Tableau canonique. **Statut :** hérité du registre : MÉTHODE CENTRALE.

## Microscope de population

**Image héritée.** épidémiologie plutôt qu'autopsie individuelle

**Ancrage exact.** familles de fonctions $L$, moyennes

**Garde héritée.** attribuer automatiquement une propriété moyenne à $\zeta$ seule

**Correspondance autorisée.** faire émerger des symétries collectives

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:17 ; 1. Tableau canonique. **Statut :** hérité du registre : PARADIGME EXTERNE.

## Thermostat critique

**Image héritée.** seuil de transition

**Ancrage exact.** flot de de Bruijn-Newman, $\Lambda$

**Garde héritée.** interpréter $\Lambda$ comme température physique

**Correspondance autorisée.** reformuler RH comme criticité exacte $\Lambda=0$

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:18 ; 1. Tableau canonique. **Statut :** hérité du registre : RÉSERVE CONCEPTUELLE.

## Scène manquante

**Image héritée.** chorégraphie visible, théâtre absent

**Ancrage exact.** géométrie/cohomologie/trace

**Garde héritée.** postuler une géométrie parce qu'une formule lui ressemble

**Correspondance autorisée.** chercher une structure expliquant trace, dualité, positivité

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:19 ; 1. Tableau canonique. **Statut :** hérité du registre : OUVERT.

## Jumeau de crash-test

**Image héritée.** même carrosserie analytique, moteur différent

**Ancrage exact.** Davenport-Heilbronn et analogues

**Garde héritée.** traiter DH comme un modèle complet de $\zeta$

**Correspondance autorisée.** rejeter les critères ne voyant que la symétrie fonctionnelle

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:20 ; 1. Tableau canonique. **Statut :** hérité du registre : INSTRUMENT ACTIF.

## Modes sombres

**Image héritée.** mode réel que le capteur ne voit pas

**Ancrage exact.** observabilité des opérateurs / complétude

**Garde héritée.** baptiser « sombre » toute inconnue non comprise

**Correspondance autorisée.** formuler explicitement les pertes d'observabilité

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:21 ; 1. Tableau canonique. **Statut :** hérité du registre : CADRE D'OBSERVABILITÉ.

## Compression fertile

**Image héritée.** biopsie informative

**Ancrage exact.** compressions finies d'une forme/opérateur infini

**Garde héritée.** croire qu'une discrétisation finie prouve à elle seule une propriété asymptotique

**Correspondance autorisée.** transférer rang, signe, inertie vers un calcul fini

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:22 ; 1. Tableau canonique. **Statut :** hérité du registre : ACTIF.

## Secteur sombre arithmétique / DARK-ZETA

**Image héritée.** cartographier l'invisible par ses déformations du visible

**Ancrage exact.** information perdue par norme, moyenne, covariance

**Garde héritée.** introduire une entité ou « énergie noire » physique

**Correspondance autorisée.** trianguler plusieurs empreintes indépendantes

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:23 ; 1. Tableau canonique. **Statut :** hérité du registre : CADRE TRANSVERSAL.

## Tomographie de cohérence TOMO-2

**Image héritée.** scanner inter-échelles

**Ancrage exact.** Gram des translations logarithmiques

**Garde héritée.** prétendre voir la phase Fourier

**Correspondance autorisée.** mesurer le spectre de puissance/covariance

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:24 ; 1. Tableau canonique. **Statut :** hérité du registre : DIAGNOSTIC SURVIVANT.

## Tomographie de phase TOMO-3

**Image héritée.** scanner de fermeture de phase

**Ancrage exact.** tricorrélation / bispectre

**Garde héritée.** identifier automatiquement bicoherence et multiplicativité

**Correspondance autorisée.** tester des couplages ternaires

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:25 ; 1. Tableau canonique. **Statut :** hérité du registre : RÉTROGRADÉE EN BRUT.

## Fermeture multiplicative

**Image héritée.** une relation locale qui se referme sur elle-même

**Ancrage exact.** $\Delta_F(m,n)=a(mn)-a(m)a(n)$, lois sur $p^k$

**Garde héritée.** confondre multiplicativité et RH

**Correspondance autorisée.** mesurer la cohérence eulérienne

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:26 ; 1. Tableau canonique. **Statut :** hérité du registre : FORMALISÉE.

## Flux d'inertie

**Image héritée.** suivre les directions de signe sous déformation

**Ancrage exact.** $(n_+,n_-,n_0)$ d'une famille hermitienne

**Garde héritée.** interpréter un saut fini comme la criticité asymptotique sans limite contrôlée

**Correspondance autorisée.** remplacer le suivi de chaque zéro par un invariant de signature

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:27 ; 1. Tableau canonique. **Statut :** hérité du registre : RÉSERVE.

## Géométrie par empreintes

**Image héritée.** reconstruire l'animal par ses traces

**Ancrage exact.** signatures/indices/dualités distinguant $\zeta$ de faux jumeaux

**Garde héritée.** prendre une liste d'analogies pour une géométrie existante

**Correspondance autorisée.** inférer des axiomes nécessaires avant de construire la géométrie

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:28 ; 1. Tableau canonique. **Statut :** hérité du registre : ACTIF CONCEPTUEL.

## Census de Möbius

**Image héritée.** recenser la structure d'une population de blocs

**Ancrage exact.** covariances/rangs de blocs de $\mu$

**Garde héritée.** déduire les zéros individuels d'une covariance d'ordre 2

**Correspondance autorisée.** étudier où la cancellation apparaît statistiquement

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:29 ; 1. Tableau canonique. **Statut :** hérité du registre : SECONDAIRE.

## PRIME-LOCK / verrou premier

**Image héritée.** serrure locale du produit d'Euler

**Ancrage exact.** $-F'/F$, support sur puissances de premiers, défaut de tour

**Garde héritée.** appeler « RH » une propriété satisfaite aussi par Steinhaus

**Correspondance autorisée.** détecter la structure eulérienne locale

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:30 ; 1. Tableau canonique. **Statut :** hérité du registre : TESTÉ / VALIDÉ COMME DÉTECTEUR LOCAL.

## DUAL-LOCK / serrure à deux clés

**Image héritée.** une serrure ne s'ouvre que si local et global sont compatibles

**Ancrage exact.** compression de la forme explicite : archimédien + conducteur/pôle + local

**Garde héritée.** juxtaposer deux scores indépendants et appeler cela interaction

**Correspondance autorisée.** tester intrinsèquement la compatibilité entre données aux premiers et complétion globale

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:31 ; 1. Tableau canonique. **Statut :** hérité du registre : TESTÉ / SURVIT COMME DÉTECTEUR D'INERTIE.

## Résidu sombre

**Image héritée.** information visible seulement après avoir retiré presque tout le signal dominant

**Ancrage exact.** petite valeur finale après cancellation des contributions local/global

**Garde héritée.** assimiler le résidu à une substance ou conclure qu'un petit nombre est automatiquement profond

**Correspondance autorisée.** quantifier où signe/inertie sont portés par un résidu de cancellation

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:32 ; 1. Tableau canonique. **Statut :** hérité du registre : NOUVEAU - TESTÉ V6.3.

## Le Thermomètre

**Image héritée.** Q(X) prend la « fièvre transverse » : sa vitesse de croissance dit de combien le zéro le plus éloigné s'écarte de la droite.

**Ancrage exact.** Théorème A : ½ limsup log(1+Q)/log X = Θ - ½ ; RH ⇔ Q = X^o(1). (LEMMES, L6)

**Garde héritée.** Lire la fièvre ne la fait pas baisser : c'est une reformulation de RH.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:98 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Loupe double

**Image héritée.** c est fabriqué pour que chaque zéro devienne un pôle double : chaque zéro est grossi d'un facteur log.

**Ancrage exact.** G = m(m+1)/(s-ρ)² + … (Lemme 5) ; Q ∼ (S/3)log³X sous RH.

**Garde héritée.** Une loupe grossit aussi les défauts : les oscillations du terme suivant (les Battements).

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:99 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Contrepoids

**Image héritée.** Le terme 2γΛ équilibre exactement le pôle de ζ en s = 1.

**Ancrage exact.** G est régulière en 1, G(1) = 2γ² + 6γ₁ (Lemme 4).

**Garde héritée.** L'équilibre ne tient qu'en un point.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:100 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Tamis à deux

**Image héritée.** c ne retient que les entiers qui ont au plus deux facteurs premiers distincts.

**Ancrage exact.** Lemme 3 : c(n) = 0 dès trois facteurs premiers distincts.

**Garde héritée.** Aucun argument n'a encore utilisé cette parcimonie.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:101 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Note fondamentale

**Image héritée.** κ = 2 + γ - log 4π est la note que donnent tous les zéros ensemble ; elle revient partout.

**Ancrage exact.** κ = Σ 1/(ρ(1-ρ)) = 2λ₁ (Li) ; dans Q (Théorème B), dans d_N² (Burnol, BCF).

**Garde héritée.** C'est une constante, pas un mécanisme ; Σ 1/∣ρ∣² = κ seulement sous RH.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:107 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Diapason

**Image héritée.** Le son de référence quand tout est accordé.

**Ancrage exact.** Théorème B : sous RH, Q ∼ (4κ/3) log³X (zéros simples).

**Garde héritée.** Le son pur n'apparaît qu'à l'infini : à X ≤ 4·10^6, Q n'est qu'à 44-72 % du diapason.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:108 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Les Battements

**Image héritée.** Deux cordes presque accordées battent ; deux zéros voisins font battre le terme en L².

**Ancrage exact.** Proposition C : coefficient α + Φ(L), Φ = somme de termes e^i(γ-γ′)L/(γ-γ′) ; corrélation 0,996.

**Garde héritée.** Les paires trop proches ne sont pas résolues et brouillent le signal.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:109 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Carrousel

**Image héritée.** Chaque zéro sur la droite est une nacelle qui tourne sans monter ; un zéro hors de la droite serait une nacelle qui s'élève.

**Ancrage exact.** Les modes e^iγu sont les vecteurs propres de la translation ; sous RH, orthogonaux en moyenne (doc. 14).

**Garde héritée.** La rotation pure est équivalente à RH : on ne voit pas le moteur qui l'impose.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:110 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Gare centrale

**Image héritée.** Toutes les lignes essayées arrivent à Q.

**Ancrage exact.** (★) ⇔ Q ≪ log³X ; e² = β²Q + T_N ; RH ⇔ Q = X^o(1).

**Garde héritée.** Ce n'est pas une destination : c'est le carrefour où RH se cache.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:116 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Bouchon et la Fuite

**Image héritée.** Boucher le pôle en s = 1 ; ce qui fuit encore est exactement Q, plus un filet (la queue).

**Ancrage exact.** β = -S_N/A_N ⇒ W_N(1) = 0 ; e² = β²Q(N) + T_N ; b_N → -1 - 2γ/log N (doc. 12).

**Garde héritée.** Boucher n'arrête pas la fuite principale.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:117 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Palier

**Image héritée.** La famille à deux directions s'arrête sur un palier, un étage au-dessus du sol.

**Ancrage exact.** {μ, a} ≈ 1,3 κ/log N de N = 50 à 10^5 (doc. 10, 12).

**Garde héritée.** Sous RH le palier devrait monter vers 4/3 : ce n'est pas un sol.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:118 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Dernier millième

**Image héritée.** Quatre coups de pinceau font 90 % du tableau ; les derniers détails en demandent toujours plus.

**Ancrage exact.** 90 % en 3-4 directions propres ; 99,9 % en 52, 81, 121 directions (N = 200, 500, 998) (doc. 14).

**Garde héritée.** N ≤ 998 : la loi de croissance n'est qu'observée.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:119 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## L'Écho des pgcd

**Image héritée.** Deux dents de scie de périodes a et b se répondent avec l'intensité pgcd²/(12ab).

**Ancrage exact.** Franel-Landau (L8) ; V_N = (1/12) Σ J₂(q)(Σ_q∣d w_d/d)².

**Garde héritée.** L'écho est une moyenne : il gouverne la queue, pas les zéros.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:120 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Sosie

**Image héritée.** Même visage que ζ (même équation fonctionnelle) mais sans produit d'Euler, et avec des zéros hors de la droite.

**Ancrage exact.** Davenport-Heilbronn : zéro 0,8085 + 85,699i ; pente de Q 0,56 contre 0,33 (doc. DH).

**Garde héritée.** -

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:126 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Modèle réduit

**Image héritée.** Une maquette où RH est vraie, grâce à une géométrie que l'original n'a pas.

**Ancrage exact.** Courbes sur F_q (Weil) ; test F_101 : max ∣a∣ = 20 ≤ 2√101 (mémo P2.2).

**Garde héritée.** La maquette a une dimension de plus : Spec ℤ × Spec ℤ = Spec ℤ.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:127 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Détecteur

**Image héritée.** K(L) monte doucement pour ζ et s'emballe pour le Sosie.

**Ancrage exact.** K(15) = 0,098 pour ζ ; K(12) = 0,885 pour DH (doc. 09).

**Garde héritée.** Dépistage, pas preuve.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:128 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Distance de sécurité

**Image héritée.** Les zéros ne doivent pas se coller : une répulsion sous l'espacement moyen.

**Ancrage exact.** (H3⋆) (doc. H3) ; plus petit écart normalisé des 300 premiers zéros : 0,29.

**Garde héritée.** Non démontrée, hors de portée de RH seule.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:134 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Point critique

**Image héritée.** ζ serait exactement au seuil d'une transition, au bord de l'eau.

**Ancrage exact.** de Bruijn-Newman : 0 ≤ Λ ≤ 0,22 ; RH ⇔ Λ = 0 (Rodgers-Tao ; Polymath15).

**Garde héritée.** Λ n'est pas une température physique.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:135 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Compteur

**Image héritée.** Au lieu de localiser chaque zéro (GPS), on compte les valeurs propres positives d'une forme de Weil comprimée.

**Ancrage exact.** 2026 : ≥ 2/3 des zéros simples et sur la droite (rang-trace, inertie de Sylvester) (doc. 13).

**Garde héritée.** Ne donne que des proportions.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:136 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Musée des erreurs

**Image héritée.** Des erreurs réelles exposées, avec des leurres, pour entraîner l'œil.

**Ancrage exact.** Banc d'audit : 21 erreurs, 7 leurres, script de notation.

**Garde héritée.** Petit échantillon, un seul projet.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:142 ; Annexe B - Lexique des résultats qui ont porté (fusion de la v6.0, Claude). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Les Quatre coins

**Image héritée.** Une table à deux entrées dont les quatre cases sont remplies.

**Ancrage exact.** ζ, L(s, χ₅) / E2 / F6 / DH : verrou local (fuite nulle) et signe global (zéros sur la droite) sont indépendants.

**Garde héritée.** Les témoins sont fabriqués.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:152 ; Mise à jour V6.3d/e - cinq noms proposés. **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Peigne

**Image héritée.** Des dents régulières posées sur la droite critique.

**Ancrage exact.** Zéros de 1 + 6^(1/2-s) : pas 2π/log 6 ; leur transformée de Fourier est la fuite Λ_F(6^k).

**Garde héritée.** Le peigne s'ajoute aux zéros de ζ, il ne les déplace pas.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:153 ; Mise à jour V6.3d/e - cinq noms proposés. **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## L'Empreinte en creux

**Image héritée.** Les zéros de ζ laissent leur moule dans les écarts entre zéros des produits d'Euler.

**Ancrage exact.** Déficit des différences de zéros près des zéros de ζ : 30 % (ζ), 17 % (L(s, χ₅)), 5 % (DH).

**Garde héritée.** Phénomène connu (Pérez-Marco ; Ford-Zaharescu) ; seule la comparaison avec le Sosie est propre au corpus.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:154 ; Mise à jour V6.3d/e - cinq noms proposés. **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Tour du propriétaire

**Image héritée.** Faire le tour de la parcelle et compter les tours de l'aiguille.

**Ancrage exact.** Principe de l'argument : nombre exact de zéros dans un rectangle ; a révélé deux zéros de DH manquants.

**Garde héritée.** Compte, ne localise pas.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:155 ; Mise à jour V6.3d/e - cinq noms proposés. **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Pied à coulisse

**Image héritée.** Les zéros hauts servent de règle pour mesurer les zéros bas.

**Ancrage exact.** Demi-largeur du creux = 1 - β (heuristique) ; pour ζ, 0,73 aux basses hauteurs, 0,51 ± 0,04 entre 1200 et 1500, pour 0,5 attendu (doc 24, 7.4).

**Garde héritée.** Reformulation de RH, probablement circulaire ; ne mesure que des zéros déjà connus sur la droite.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:156 ; Mise à jour V6.3d/e - cinq noms proposés. **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Portée

**Image héritée.** Jusqu'où la lunette porte avant de voir l'intrus.

**Ancrage exact.** Largeur W du support (donc nombre de premiers) à partir de laquelle une fenêtre voit un zéro hors droite : entre 1,5 et 2,0 pour le zéro de DH à 85,7.

**Garde héritée.** Propriété de l'instrument, pas de l'objet.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:170 ; Mise à jour V6.4 - après le test de l'Atlas (document 26). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Point d'Euler

**Image héritée.** Le seul endroit de la route où tout est aligné.

**Ancrage exact.** θ = 0 dans F_θ : seul point où 100 % des zéros sont sur la droite et où l'empreinte de ζ est maximale.

**Garde héritée.** Une seule famille testée.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:180 ; Mise à jour V6.5 - la famille modulo 7 (document 27). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Plage de survie

**Image héritée.** La bande de terrain sec qui rétrécit quand la marée monte.

**Ancrage exact.** Intervalle de θ où tous les zéros jusqu'à T restent sur la droite : [-0,0096 ; +0,072] pour T = 1000.

**Garde héritée.** Observée jusqu'à 1000 seulement.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:181 ; Mise à jour V6.5 - la famille modulo 7 (document 27). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Rencontre

**Image héritée.** Deux danseurs se rejoignent sur la ligne et la quittent ensemble.

**Ancrage exact.** Deux zéros voisins se touchent en θ_c, puis s'écartent de la droite comme √(θ - θ_c).

**Garde héritée.** Rien n'est détruit : le nombre de zéros est conservé.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:182 ; Mise à jour V6.5 - la famille modulo 7 (document 27). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Tour

**Image héritée.** Les étages d'un immeuble, chacun contrôlé par la même règle.

**Ancrage exact.** Les corps à qⁿ éléments ; à chaque étage n, la forme de Castelnuovo Q_n est positive.

**Garde héritée.** Pour ζ, on ne sait pas ce que sont les étages.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:192 ; Mise à jour V6.6 - le Modèle réduit (document 28). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Positivité saturée

**Image héritée.** Une poutre chargée exactement à sa limite, qui tient.

**Ancrage exact.** Courbe y² = x⁵ + x³ + 1 sur F₃ (P(u) = 1 + 9u⁴) : ρ_4 = 1 exactement, 118 points sur F₈₁.

**Garde héritée.** Saturation à un étage, pas à tous.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:193 ; Mise à jour V6.6 - le Modèle réduit (document 28). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Faux jumeau entier

**Image héritée.** Un faux billet avec un vrai filigrane.

**Ancrage exact.** Équation fonctionnelle, comptages de points fermés entiers positifs, RH fausse (220 cas en genre 1 et 2 sur F₃, F₅) ; démasqué à l'étage 2 à 5.

**Garde héritée.** Ne vient d'aucune géométrie.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:194 ; Mise à jour V6.6 - le Modèle réduit (document 28). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Rang

**Image héritée.** Plus d'inconnues que d'équations : il reste des directions libres.

**Ancrage exact.** Fenêtre L > 2g : forme de Weil d'une vraie courbe exactement singulière ; pour ζ, L et F6, chute géométrique de λ_min avec la dimension excédentaire.

**Garde héritée.** Pour ζ, la chute n'est jamais totale.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:204 ; Mise à jour V6.7 - STABILITY-RADIUS (document 29). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Recensement

**Image héritée.** Un appel où chaque absent répond « absent ».

**Ancrage exact.** À la fenêtre 2g, nombre de valeurs propres négatives = zéros hors droite / 2.

**Garde héritée.** Exact dans le modèle seulement.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:205 ; Mise à jour V6.7 - STABILITY-RADIUS (document 29). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Rencontre figée

**Image héritée.** Deux danseurs arrêtés au moment où ils se rejoignent.

**Ancrage exact.** Vraie courbe à deux zéros confondus : marge de l'objet nulle, RH démontrée.

**Garde héritée.** Aucune courbe voisine ne franchit.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:206 ; Mise à jour V6.7 - STABILITY-RADIUS (document 29). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Passage interdit

**Image héritée.** Une porte au ras du mur, mais murée.

**Ancrage exact.** Marge nulle sans sortie : aucune perturbation qui sort de RH n'est une courbe.

**Garde héritée.** Formulé dans le modèle seulement.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:207 ; Mise à jour V6.7 - STABILITY-RADIUS (document 29). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## L'Archipel d'Euler

**Image héritée.** Des îles dans une mer qui monte.

**Ancrage exact.** Dans V_q, la région RH jusqu'à la hauteur T est faite d'îles autour des points d'Euler, de rayon ≈ N^(-0,77) ; à l'infini, il ne reste que les points (Saias-Weingartner).

**Garde héritée.** La mer n'est pas uniforme : chenaux le long de certains grands cercles.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:217 ; Mise à jour V6.8 - L'Archipel d'Euler (document 30). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## L'Île sans mer

**Image héritée.** Une île seule au monde.

**Ancrage exact.** Espaces de dimension 1 : ζ (Hamburger), L(s, (·/3)), L(s, (·/5)) : aucune voisine qui garde l'équation fonctionnelle.

**Garde héritée.** Parmi les séries de Dirichlet seulement.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:218 ; Mise à jour V6.8 - L'Archipel d'Euler (document 30). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Continent bas

**Image héritée.** À marée basse, les îles sont reliées.

**Ancrage exact.** À |t| ≤ 50, les trois points d'Euler de V₇ impair sont dans une même région sans paire hors droite.

**Garde héritée.** Dépend de la carte et de la hauteur.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:219 ; Mise à jour V6.8 - L'Archipel d'Euler (document 30). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Chaînon

**Image héritée.** Le pas discret est l'exponentielle d'un générateur continu.

**Ancrage exact.** F = q^D ; les zéros de ζ_C sont le spectre de D, répété avec la période 2πi / log q.

**Garde héritée.** Dans le Modèle réduit, D n'est défini qu'à cette période près.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:229 ; Mise à jour V6.9 - Le chaînon (document 32). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Spectre des longueurs

**Image héritée.** Les zéros chantent les longueurs des orbites.

**Ancrage exact.** S(u), calculé sur les zéros seuls, a des pics en log n de hauteur c(n)/√n ; produit d'Euler ⟺ pics seulement en log p^k.

**Garde héritée.** Fenêtre finie ; fond lisse non retiré.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:230 ; Mise à jour V6.9 - Le chaînon (document 32). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## L'Axe par zéro distinct

**Image héritée.** Les nombres construisent un axe par note, pas par instrument.

**Ancrage exact.** Le rang du Gram de Krylov est le nombre de zéros distincts ; la multiplicité y est une masse.

**Garde héritée.** Pour ζ, la simplicité des zéros n'est que conjecturée.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:231 ; Mise à jour V6.9 - Le chaînon (document 32). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Métrique manquante

**Image héritée.** La machine est là ; il manque la règle qui mesure.

**Ancrage exact.** Les 220 faux jumeaux ont l'opérateur, la symétrie et le réseau ; seul leur Gram est indéfini.

**Garde héritée.** Pour ζ, « là » veut dire dans une fenêtre finie.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:232 ; Mise à jour V6.9 - Le chaînon (document 32). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Générateur des premiers

**Image héritée.** Les nombres premiers jouent la partition ; l'opérateur est l'instrument qu'on en déduit.

**Ancrage exact.** Avec les seuls premiers ≤ e^(Nh+2a), le faisceau de Toeplitz des traces donne e^(iγh) pour les zéros de la fenêtre (226 zéros de ζ avec les premiers ≤ 439).

**Garde héritée.** Fenêtre finie ; pas h choisi.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:242 ; Mise à jour V6.10 - Le générateur des premiers (document 33). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Masse unité

**Image héritée.** Un vrai zéro pèse exactement son poids.

**Ancrage exact.** Une vraie valeur propre porte la masse ĝ(γ) ; masse 1 = zéro simple ; test sans aucun zéro.

**Garde héritée.** Tolérance de 1 % ; zéros proches confondus.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:243 ; Mise à jour V6.10 - Le générateur des premiers (document 33). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Repliement

**Image héritée.** Une roue filmée trop lentement semble tourner à l'envers.

**Ancrage exact.** Au pas h, γ n'est vu qu'à 2π/h près ; au pas log 2, tous les zéros de ζ sont repliés.

**Garde héritée.** Le Modèle réduit, avec 2g zéros par période, n'en souffre pas.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:244 ; Mise à jour V6.10 - Le générateur des premiers (document 33). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Métrique en avance

**Image héritée.** La sentinelle entend avant de voir.

**Ancrage exact.** DH : le quadruplet de 240,4 crée deux directions négatives avant d'être résolu par l'opérateur.

**Garde héritée.** Seuil de bruit (10^-11 de la plus grande valeur propre).

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:245 ; Mise à jour V6.10 - Le générateur des premiers (document 33). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Pas de base

**Image héritée.** La base d'un corps fini est la cadence d'une caméra qui filme un même mouvement.

**Ancrage exact.** F_q² voit le même D avec une demi-période : zéros = courbe ∪ tordue (525 sur 525) ; RH conservée.

**Garde héritée.** Pour ζ, il n'y a pas de cadence naturelle.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:255 ; Mise à jour V6.11 - La base comme pas de temps (document 35). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Descente

**Image héritée.** Redescendre d'un étage, c'est deviner un signe par pièce.

**Ancrage exact.** Les objets sur F_q compatibles avec les comptages sur F_q² sont les choix de signe des facteurs irréductibles (525 sur 525 ; 2 dans 440 cas, jusqu'à 12).

**Garde héritée.** Polynômes de Weil, pas forcément des courbes.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:256 ; Mise à jour V6.11 - La base comme pas de temps (document 35). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Métrique noyée

**Image héritée.** Une voix seule couverte par une foule.

**Ancrage exact.** À nombres premiers fixés, DH perd ses directions négatives quand le pas grandit (10 → 0 entre h = 0,01 et 0,1) ; à N fixé, elle les garde.

**Garde héritée.** Une seule fonction test ; seuil de bruit fixé.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:257 ; Mise à jour V6.11 - La base comme pas de temps (document 35). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## L'Innovation

**Image héritée.** Le GPS qui dit, à chaque pas, si la position est encore possible.

**Ancrage exact.** Récurrence de Levinson sur les traces des premiers : ζ et L restent dans le disque (\|k_n\| ≤ 0,79) ; DH sonne à la fenêtre 3,52 (premiers ≤ 36).

**Garde héritée.** Horizon numérique (double précision).

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:267 ; Mise à jour V6.12 - Les idées rejetées relues (document 36). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Fantôme pesé

**Image héritée.** On reconnaît un fantôme à ce qu'il ne pèse rien.

**Ancrage exact.** Le mode fantôme de V4.3 (Im ≈ 73,8) porte une masse de 1,3·10^-9 ; les vrais zéros, 1.

**Garde héritée.** Critère par fenêtre, pas borne uniforme.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:268 ; Mise à jour V6.12 - Les idées rejetées relues (document 36). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Rayon spectral

**Image héritée.** La plus grande dérive se lit au bord du spectre.

**Ancrage exact.** Θ - ½ dans une fenêtre = max \|Im γ\| du générateur : 0,308517 pour DH, < 10^-6 pour ζ et L.

**Garde héritée.** Borne inférieure : un quadruplet non résolu ne compte pas.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:269 ; Mise à jour V6.12 - Les idées rejetées relues (document 36). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Temps de Heisenberg

**Image héritée.** Une note n'est entendue que lorsque l'oreille sépare les notes voisines.

**Ancrage exact.** Un quadruplet hors droite à la hauteur γ₀ est détecté à la fenêtre L_c ≈ log(q·γ₀/2π) : rapport 0,95-1,08 pour ζ et L(s, χ₅), 0,80-0,89 pour DH ; premiers jusqu'à ≈ q·γ₀/2π (conducteur analytique).

**Garde héritée.** Poids < 10^-5 (lobes secondaires de ĝ) ; repliement si h > π/γ₀ ; le facteur de DH n'est pas expliqué.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:279 ; Mise à jour V6.14 - La loi de seuil (document 38). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Balance d'inertie

**Image héritée.** Deux poids opposés sur un plateau qui est le fond.

**Ancrage exact.** G = B + paire cesse d'être positive ⟺ C^-1 + U*B^-1U est définie positive (noyau reproduisant du fond aux deux points de la paire).

**Garde héritée.** B doit être définie positive.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:280 ; Mise à jour V6.14 - La loi de seuil (document 38). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Signe fragile

**Image héritée.** L'aiguille d'une boussole cassée continue de pointer avec assurance.

**Ancrage exact.** Fond positif par construction, innovation de -2·10^-3 à la taille 296 (λ_min/λ_max = 4·10^-17) ; à 30 chiffres, une erreur de 0,45 sur la fenêtre.

**Garde héritée.** -

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:281 ; Mise à jour V6.14 - La loi de seuil (document 38). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Poids archimédien

**Image héritée.** La longueur d'une corde fixe la note qu'elle peut entendre.

**Ancrage exact.** La longueur de détection d'un quadruplet est Ω(γ₀) = 2π × densité des zéros : 1,02-1,08 pour ζ, L(s, χ₅) et L(Δ, s) ; elle double en degré 2.

**Garde héritée.** Facteur 0,8-0,9 pour DH et 0,87-0,98 pour ζ·L.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:291 ; Mise à jour V6.15 - Le degré 2 et le recensement (document 39). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Quadruplet replié

**Image héritée.** Un passager qui revient par l'autre porte.

**Ancrage exact.** Au pas h, un quadruplet au-delà de π/h entre dans la fenêtre en γ - 2π/h ; 4 quadruplets de DH (1 092 à 1 464) sont comptés ainsi, avec un poids de 5·10^-8 à 5·10^-7.

**Garde héritée.** Le poids tombe vite dans les lobes secondaires.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:292 ; Mise à jour V6.15 - Le degré 2 et le recensement (document 39). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Somme sans répulsion

**Image héritée.** Deux chorales qui chantent sans s'écouter.

**Ancrage exact.** ζ·L(s, χ₅) : allumage à 0,87-0,98 de Ω, contre 1,02-1,08 pour une seule fonction.

**Garde héritée.** Un seul produit testé, non pré-enregistré.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:293 ; Mise à jour V6.15 - Le degré 2 et le recensement (document 39). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Rencontre à trois

**Image héritée.** Trois chemins qui se croisent au même carrefour : le choc de deux zéros.

**Ancrage exact.** À la fenêtre de Heisenberg, la marge locale de la métrique d'une paire de zéros d'écart normalisé s vaut 1 - sinc²(πs), la densité de corrélation de paires de Montgomery ; elle s'annule à la rencontre. Mesuré sur 1 070 zéros de ζ : 4 marges sous 0,1 (13 pour le GUE, 320 pour Poisson).

**Garde héritée.** Modèle à deux atomes ; les voisins comptent pour la métrique réelle.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:303 ; Mise à jour V6.16 - La Rencontre à trois (document 40). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Compteur de paires

**Image héritée.** Un compteur qui ne bouge qu'aux chocs.

**Ancrage exact.** β = 2Σ\|u_γ\|² est lisse à 95 % (terme θ′) ; sa part d'écart 2Σ(Z″/Z′)²/\|ρ\|² est portée à 35 % par les 10 % de zéros les plus serrés ; la paire de Lehmer près de 7 005 y pèse environ mille fois la médiane.

**Garde héritée.** Heuristique pour la finitude (répulsion nécessaire).

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:304 ; Mise à jour V6.16 - La Rencontre à trois (document 40). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Zone d'ombre

**Image héritée.** Une case blanche sur la carte.

**Ancrage exact.** Case de la carte des croisements sans croisement produit par le corpus, ou croisement sans pendant dans le Modèle réduit ; le navigateur peut la viser.

**Garde héritée.** Une case vide n'est pas une question : il faut encore la formuler.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:305 ; Mise à jour V6.16 - La Rencontre à trois (document 40). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Contour tourné

**Image héritée.** Regarder une falaise de biais pour en voir le relief.

**Ancrage exact.** Λ(6+it) = 2e^{-φt} Re(e^{6iφ} A(6+it)), A = ∫ F(e^{x+iφ}) e^{(6+it)x} dx, F(w) = Σ τ(n) e^{-2πnw} : la rotation du contour de Mellin, repliée par la modularité, supprime l'annulation exponentielle ; 2 139 zéros de L(Δ, s) jusqu'à 1 500 en double précision (accord 10⁻¹³ avec mpmath, complétude de Turing).

**Garde héritée.** Il faut la modularité pour replier le contour.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:313 ; Mise à jour V6.17 - La Rencontre en degré 2 (document 41). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Loi de la marge

**Image héritée.** Une foule qui laisse à chacun une place en proportion de l'espace disponible.

**Ancrage exact.** La fréquence d'une configuration est proportionnelle à la marge de la métrique : à la fenêtre N, marge totale = densité de Weyl de U(N), marge d'une paire = corrélation de paires du CUE(N) ; paire conjuguée : marge = sin²θ = (π/2) × densité de Sato-Tate (démontré) ; zéros de ζ et de Δ (mesuré, déficit à basse hauteur).

**Garde héritée.** Familles symplectiques (genre ≥ 2) : la densité de Haar n'est plus le déterminant de la métrique de taille 2g.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:314 ; Mise à jour V6.17 - La Rencontre en degré 2 (document 41). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Les Familles étrangères

**Image héritée.** Deux foules qui se traversent sans se voir.

**Ancrage exact.** Une fonction non primitive superpose des familles sans répulsion mutuelle : ζ·L(χ5), 15 % de marges sous 0,1, toutes mixtes, paire mixte à 8,9·10⁻⁴ ; pendant exact : le changement de base F_p → F_p², P(u²) = P(u)·P(-u), où les collisions existent (courbes supersingulières) avec RH vraie.

**Garde héritée.** Sur Q aucune collision n'est connue ; sur F_p² elles existent.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:315 ; Mise à jour V6.17 - La Rencontre en degré 2 (document 41). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Rencontre à n

**Image héritée.** La Rencontre à trois, vue en relief : une surface au lieu d'une courbe.

**Ancrage exact.** Pour n atomes à la fenêtre N, det(G/N) = det[D_N(θ_l - θ_m)] = (2π/N)^n^ R_n du CUE(N) (démontré) ; les triplets des 1 070 zéros de ζ suivent le noyau sinus R3 (χ² réduit 1,34, Poisson 17,3) ; pour ζ·L(χ5), loi de superposition de deux familles indépendantes (χ² 0,87).

**Garde héritée.** Mesure à basse hauteur : 0 triplet serré pour 4,4 attendus (effet de taille finie supposé).

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:323 ; Mise à jour V6.19 - La Rencontre à n et la matrice des théories (documents 43 et 44). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Carillon de Bohr

**Image héritée.** Un carillon dont chaque cloche est un zéro : le signal sonne sans s'amplifier ni s'éteindre.

**Ancrage exact.** Ψ(u) = e^-u/2^C(e^u^)/u dans l'espace de Besicovitch B² ; coefficients de Bohr A_γ(L) ; sous RH, Σ\|A_γ\|² = S (Théorème B).

**Garde héritée.** Proposé, pas encore calculé (axe E du plan).

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:324 ; Mise à jour V6.19 - La Rencontre à n et la matrice des théories (documents 43 et 44). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Palier (précisé)

**Image héritée.** Un palier par endroits, avec des marches cassées là où le sol se dérobe.

**Ancrage exact.** Médiane de e_N² log N/κ = 0,985 × 4/3 de 10⁴ à 5·10⁶, sans montée visible ; compensation b² ≈ 1,16, r_Q ≈ 0,72, queue ≈ 0,15 ; pics jusqu'à 3,27 × 4/3 là où A_N s'annule ; sous RH, la médiane tend vers (S/4κ)·4/3 si la queue s'éteint.

**Garde héritée.** La limite 4/3 n'est pas atteinte dans les calculs ; elle reste conditionnelle.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:332 ; Mise à jour V6.20 - Le Palier recalculé (document 45). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Surface virtuelle

**Image héritée.** Une surface dont on connaît les croisements sans en connaître les points.

**Ancrage exact.** Forme d'intersection sur {fibres, graphes de Frobenius} : dans le Modèle réduit, celle de C × C (indice de Hodge : 425 courbes sur 425 ; surplus exact pour les 220 faux jumeaux) ; pour ζ, la même par le dictionnaire fibres ↔ pôle, intersections ↔ puissances de premiers, genre ↔ terme archimédien ; une seule direction positive depuis les premiers ≤ 439 ; DH : 2 puis 10 en trop. Orthogonalement aux fibres, c'est l'opposé de la métrique des zéros.

**Garde héritée.** Le dictionnaire est classique (Weil, Bombieri, Connes) ; la surface elle-même n'existe pas.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:338 ; Mise à jour V6.21 - La surface virtuelle (document 46). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Fonction auxiliaire

**Image héritée.** Un filet tendu sur tous les points à la fois : s'il y en a trop, il se déchire.

**Ancrage exact.** Stepanov-Bombieri : par Riemann-Roch et le Frobenius, une fonction s'annule fortement en tous les points rationnels, d'où N_m ≤ Q + (2g + 1)√Q + 1 ; avec le tordu quadratique, elle démasque les 220 faux jumeaux (étage médian 4, Castelnuovo 3) ; Clifford seul n'en démasque aucun.

**Garde héritée.** Pour ζ, la fonction auxiliaire n'existe pas encore : il manque le Frobenius.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:344 ; Mise à jour V6.22 - Le Riemann-Roch virtuel (document 47). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Frobenius absolu

**Image héritée.** Une horloge qui tournerait sur les entiers comme x ↦ x^q tourne sur une courbe.

**Ancrage exact.** Hypothèse de travail de l'axe J3 : une application de « Spec Z » dans lui-même dont les points fixes seraient les nombres premiers ; Connes-Consani proposent l'action d'échelle.

**Garde héritée.** Rien de tel n'est construit ; l'image n'est pas un objet.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:345 ; Mise à jour V6.22 - Le Riemann-Roch virtuel (document 47). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## La Dérivée nulle

**Image héritée.** Une aiguille qui pointe exactement au même endroit que les autres, mais qui ne bouge pas quand on la touche.

**Ancrage exact.** Le Frobenius x ↦ x^p, l'identité et une permutation prennent les mêmes valeurs ou permutent les points ; seule la dérivée nulle de x^p fait chuter le rang des conditions de Stepanov (34 au lieu de 104 pour p = 101) : 13 à 52 fonctions auxiliaires contre 0.

**Garde héritée.** Aux tailles calculées, la borne de Stepanov reste triviale ; seule la construction est vérifiée.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:351 ; Mise à jour V6.23 - Le Frobenius qui n'est pas un morphisme (document 48). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.

## Le Frobenius trop bon

**Image héritée.** Une horloge si parfaite qu'elle ne perd jamais une seconde, et ne peut donc rien marquer.

**Ancrage exact.** En caractéristique un (Connes-Consani), Fr_λ est un automorphisme pour tout λ > 0 : il dilate les pentes au lieu d'annuler les dérivations ; il ne fournit pas l'élément invisible aux dérivations de Stepanov. La contrainte doit venir de la positivité sur le carré (route de Weil).

**Garde héritée.** Lu sur résumés et extraits.

**Provenance.** 1\_Presentation/20\_Registre\_metaphores\_V6.md:357 ; Mise à jour V6.26 - J3b (document 51). **Statut :** hérité du registre : statut non explicité dans cette ligne historique.


# Index technique et version interactive

Le lecteur interactif `69_LANGUE_DES_PASSAGES.html` permet recherche par nom,
symbole, image ou garde, filtres de niveau et consultation d’une fiche à la fois.
L’atelier applique les règles typées et signale les moments perdus.

L’index `v644_index_fonctions.csv` / `.json`, dans le dossier de données, donne
fichier, ligne, nom qualifié, signature, type et docstring. Sans docstring,
le comportement n’est pas inventé. La couverture technique est celle de l’AST,
non une analyse sémantique certifiée de tous les programmes.

Le dictionnaire JSON permet d’ajouter des entrées qualifiées en conservant leur
provenance. Les symboles G, P, D, U, R, gamma et kappa demandent leur contexte :
le même caractère écrit ne suffit pas à définir le même objet.

Les unités fictives accompagnent les calculs : x logarithmique sans dimension,
f d’amplitude A, Q et métriques d’unité A², quotient spectral sans dimension.
Le mot énergie, chaleur ou entropie ne fournit pas une preuve de signe.

Les preuves complètes et les expériences figurent dans le document 68 ; les
critères globaux, branches, collisions et coefficients des anciennes familles
gardent leurs obligations ouvertes. Cette langue crée des phrases vérifiables
et des ponts de domaines ; elle ne fournit pas encore la loi arithmétique globale.
