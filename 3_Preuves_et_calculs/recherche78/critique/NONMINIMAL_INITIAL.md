# Variante initiale non minimale

Cette variante retire entièrement l'atome cible en zéro et la première
ligne source par un seul noyau fini. Elle laisse une obligation globale
de positivité exactement équivalente à celle du signal S.

## Hypothèses exactes du certificat

On utilise le raccord réel du problème :

    T=log2,  m=S(T)/T>0,  a=S'(T+)<0,
    c=m−a>0,
    μ=mδ_0+β1_(T,∞)du,
    ν=cδ_T+Σ_(logq>T)c_qδ_logq.

Le poids source en T est **c=m−a**, et non c_2=log2/√2.

Soient l,b certifiés tels que

    T<l<b<log3,
    A'(b)−A'(l)=−a,
    Q(b)−Q(l)=Tc,     Q(t)=tA'(t)−A(t).

Diagnostics numériques, à remplacer par les encadrements du certificat :

    l≈0.84097046684642855537,
    b≈1.02059031817340809495,
    log3≈1.09861228866810969140.

## Existence et unicité de la solution radiale

Avec d=−a>0 et l≥T, définir b(l)>l par `A'(b(l))−A'(l)=d`. La positivité de β
et la croissance illimitée de A' donnent une unique solution. On a

    b'(l)=β(l)/β(b(l))>0,
    F(l):=Q(b(l))−Q(l),
    F'(l)=(b(l)−l)β(l)>0.

Un encadrement opposant F(l)−Tc de part et d'autre de zéro certifie donc
une unique paire. La condition b<log3 doit être encadrée séparément.

## Noyau et conservation exacte

Poser

    η=mδ_0+β1_[l,b]du,     K_T=η/c.

Alors η≤μ, et

    η(R)=m+A'(b)−A'(l)=m−a=c,
    ∫uη(du)=Q(b)−Q(l)=Tc.

Ainsi K_T est une probabilité de barycentre T. Toute la masse μ{0}=m
est consommée par cette seule vraie ligne. Le résidu est

    ρ=μ−η=β1_((T,∞)\[l,b])du≥0,
    ν'=ν−cδ_T=Σ_(logq>T)c_qδ_logq≥0.

Il n'y a aucun atome fictif de fermeture. La portée de cette ligne est
`max(T,b−T)=T`, puisque b<log3<2T.

## Gap de Jensen et résidu

Écrire `Pλ(t)=∫(t−u)+λ(du)` et `G=Pη−c(t−T)+`. Jensen donne G≥0.
La conservation de masse et de moment donne plus explicitement

    G(t)=0                                  (t≤0),
    G(t)=mt                                 (0≤t≤T),
    G(t)=∫_[l,b](u−t)+β(u)du                (t≥T).

Le gap est donc nul pour tout t≥b, et pas seulement pour t≥log3.

Le signal résiduel `R=Pρ−Pν'` satisfait exactement

    R(t)=0                                  (t≤T),
    R(t)=S(t)−G(t)                          (t≥T),
    R(t)=S(t)                               (t≥b).

Comme le premier atome de ν' est en log3, `Pν'(t)=0` pour t≤log3.
Donc R(t)=Pρ(t)≥0 sur toute cette fenêtre. Il est même strictement
positif pour T<t≤log3, grâce à la densité positive restante sur (T,l).

Les domaines se recouvrent car b<log3. On obtient ainsi l'équivalence
exacte

    R(t)≥0 pour tout t
        ⇔ S(t)≥0 pour tout t≥T
        ⇔ RH dans le cadre considéré.

Le premier sens découle de S=R+G. Dans l'autre sens, la petite fenêtre
est positive par la mesure résiduelle, et la queue résiduelle égale S.
Un noyau complet pour le résidu, s'il est construit, se combine avec
K_T en un noyau complet pour la paire originale. Sous RH, le théorème
de balayage quantile s'applique aussi à (ν',ρ).

## Formulation du « coup double » et limites

Formulation exacte : **« Une ligne barycentrique finie consomme à la
fois tout le stock en zéro et l'atome source en T ; le résidu demeure
positif avant log3 et retrouve exactement S dès b. »**

Ce résultat établit un certificat fini utile pour préparer le résidu.
La preuve du signe dans la queue reste entière. La modification du
signal est limitée à une fenêtre finie et son gap devient identiquement
nul au-delà de b.

L'obstruction de portée liée au stock r_N du shadow canonique ne
s'applique pas à cette ligne non minimale : elle a déjà retiré tout
l'atome zéro avec une portée T. La portée d'un futur couplage complet
reste à établir. Ni sa borne, ni son absence de borne ne découlent de
cette première ligne.

Les lignes ultérieures de l'ancien balayage ne peuvent pas être
conservées sans vérifier qu'elles restent sous-mesures de ρ : la réserve
a changé. Il faut reprendre le balayage depuis (ν',ρ), ou donner une
preuve de compatibilité spécifique.

Après translation u↦u−T, le résidu peut être étudié sur [0,∞) avec une
densité β(T+u) et un intervalle retiré. Il n'a aucun atome en sa nouvelle
origine ; les anciennes formules de stock atomique ne constituent donc
plus un invariant disponible pour cette bifurcation.

Les preuves de conservation, de gap et d'équivalence sont exactes sous
les équations et les bornes ci-dessus. Les décimales affichées ne sont
pas, à elles seules, un certificat de ces équations.
