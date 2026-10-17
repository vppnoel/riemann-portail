# Audit critique — compensation interblocs et obligation globale

Statut : lemmas auxiliaires démontrés, contre-modèles exacts, cible arithmétique encore ouverte. Aucun résultat ci-dessous ne prouve RH.

## 1. Récurrence exacte et dette de courbure

Posons G(C)=A_T^*(C)=sup_{t≥T}(Ct−A(t)), avec T=log 2. Puisque A''=β>0 sur [T,+∞), G est convexe et différentiable, avec θ(C)=G'(C). Si C≤A'(T), θ(C)=T ; sinon θ(C) est l'unique solution A'(θ)=C.

Pour un état cumulatif (C,L,H), H=L−G(C), et un nouvel atome cδ_x :

H_nouveau−H=cx−[G(C+c)−G(C)]=c[x−(1/c)∫_C^{C+c}θ(v)dv].

En particulier :

c[x−θ(C+c)] ≤ H_nouveau−H ≤ c[x−θ(C)].

Lorsque [C,C+c] est dans la partie intérieure :

H_nouveau−H=c[x−θ(C)]−∫_0^c (c−s)/β(θ(C+s)) ds.

La dernière intégrale est une dette positive de courbure. Un bilan arithmétique doit donc compenser le déplacement du centre ainsi que cette dette. Cette identité n'établit pas le signe de H.

## 2. Garde exacte de toutes les coupures d'un bloc

Supposons un bloc de sources de masse D>0, moment M=D m, et support dans [a,b], a<b. Il commence après un état cumulatif (C,L,H). Un préfixe du bloc a une masse d et un moment l. Par les contraintes du support :

l≥a d ;  M−l≤b(D−d).

Donc :

l≥max(a d,M−b(D−d)).

Le défaut de chaque préfixe satisfait ainsi :

H_préfixe≥H+max(a d,M−b(D−d))−[G(C+d)−G(C)].

Les deux droites se rencontrent à d*=D(b−m)/(b−a). De chaque côté, le minorant est concave puisque G est convexe. Son minimum sur [0,D] est donc l'une des trois valeurs :

1. H ;
2. H_fin=H+M−[G(C+D)−G(C)] ;
3. K=H+a d*−[G(C+d*)−G(C)].

Si ces trois valeurs sont non négatives, tous les défauts de préfixes du bloc le sont. Le certificat est suffisant, pas nécessaire pour le bloc réel. Il est optimal si l'on ne connaît que C,H,D,M,a,b : la mesure d*δ_a+(D−d*)δ_b atteint le coude et son minorant. En cas de support réduit à un point, la concavité suffit à vérifier les deux extrémités.

**Usage :** K mesure la dette intérieure cachée par les seuls bilans aux extrémités. Il peut être calculé avant de déclarer un bloc compatible. Il ne donne aucune raison automatique pour que les premiers satisfassent K≥0.

## 3. Contre-modèle exact : endpoints et masse/moment ne suffisent pas

Prendre µ=1_[0,3](u) du et ν=(3/2)δ_(1/4)+(3/2)δ_(11/4). Les deux mesures ont masse 3 et moment 9/2. Pourtant :

S(t)=P_µ(t)−P_ν(t), S(0)=S(3)=0, mais S(1)=1/2−(3/2)(3/4)=−5/8.

Pour A(t)=t²/2 et G(C)=C²/2, le premier défaut vaut H_1=3/8−9/8=−3/4, alors que le dernier défaut H_2 est nul. Le mauvais signe peut donc se cacher à l'intérieur d'un bloc parfaitement équilibré.

## 4. Obstruction asymptotique au certificat de blocs à ratio fixé

Cette obstruction concerne le certificat précédent, pas le vrai signe du signal de Suzuki.

Considérons les sources arithmétiques c_n=Λ(n)/√n aux positions log n. Un bloc est (X,e^h X], où h>0 est fixé. Posons a=log X, b=a+h, E=e^(h/2), r=E−1, z=2r/h−1. On a 0<z<r : e^(h/2)−1>h/2 donne z>0, et 1−e^(−h/2)<h/2 donne z<r.

Le théorème des nombres premiers Ψ(X)~X implique :

C(X)/(2√X)→1,
D/(2√X)→r,
(M−aD)/(2√X)→hE−2r,
d*/(2√X)→z.

De plus, le défaut avant le bloc satisfait H(X)=o(√X), sans supposer RH. En effet, par intégration de Stieltjes :

P(log X)=∫_1^X Ψ(u) u^(−3/2)[1+(1/2)log(X/u)] du.

Après u=Xv, domination par v^(−1/2)[1+(1/2)log(1/v)] donne P(log X)/√X→4. Comme A(log X)/√X→4, S(log X)=o(√X). Enfin C(X)/(2√X)→1 et A'(t)~2e^(t/2) impliquent θ(C(X))−log X→0 ; le terme de Bregman entre θ(C(X)) et log X est o(√X). L'identité S=H+Bregman donne H(X)=o(√X).

Écrire directement, afin de ne pas multiplier les erreurs asymptotiques par log X :

G(C(X)+d*)−G(C(X))−a d*=∫_0^(d*)[θ(C(X)+s)−a] ds.

Uniformément pour s/(2√X) dans un intervalle compact, θ(C(X)+s)−a=2log(1+s/(2√X))+o(1). Ainsi :

K(X)=−4√X φ(z)+o(√X),
φ(z)=(1+z)log(1+z)−z>0.

Donc K(X)<0 pour tous les X assez grands, à tout ratio e^h>1 fixé. Même si le vrai signal était positif, ce certificat fondé uniquement sur masse, moment et support échouerait finalement.

**Conséquence :** une compensation uniforme à ratio fixé doit utiliser une information sur la distribution intérieure des premiers. Raffiner mécaniquement la maille peut réduire la dette géométrique ; cela ne fournit pas la loi de signe arithmétique manquante. Aucune borne chiffrée du seuil asymptotique n'est donnée ici.

## 5. Obstruction à une inversion positive de l'identité de Selberg, avec le réservoir exponentiel exact

Cette section renforce le contre-modèle générique. Le réservoir est maintenant exactement α(dx)=e^(x/2)1_[0,+∞)(x)dx ; seule la source ν est artificielle.

Prendre ν=12δ_(12/5), R=α−ν, Z=P_R et D=xR+(α+ν)*R. Alors :

Z(t)=4(e^(t/2)−1−t/2)−12(t−12/5)_+.

Au point t=4 : Z(4)=4e²−156/5<−8/5, grâce à e²<37/5. Donc Z est réellement négatif.

Pourtant le forcing double intégré est :

Q(t)=P_D(t)=8[(t−4)e^(t/2)+t+4]−(144/5)(t−12/5)_+−144(t−24/5)_+,

et Q(t)≥0 pour tout t≥0.

Preuve : avant b=12/5, Q est l'intégrale positive de 2x e^(x/2). Sur [b,2b], Q''(t)=2t e^(t/2)≥72/5. Avec les bornes élémentaires 22/5<e^(3/2)<9/2 et e^(6/5)>3 :

Q(3)≥68/25 ; |Q'(3)|≤16/5.

La minoration quadratique d'une fonction de courbure au moins 72/5 donne :

Q(t)≥68/25−(16/5)²/[2(72/5)]=532/225>0.

Sur [2b,+∞), Q''(t)≥96. Les bornes 12<e^(5/2)<123/10 et e^(12/5)>10 donnent :

Q(5)≥1608/25 ; |Q'(5)|≤104/5.

Donc :

Q(t)≥1608/25−(104/5)²/(2·96)=931/15>0.

Les bornes exponentielles utilisées peuvent être certifiées par des sommes de Taylor rationnelles et une majoration géométrique du reste. Les changements de pente de Q aux deux atomes ne posent pas de problème : chacune des minorations est appliquée sur son propre intervalle lisse fermé, et Q est continue aux raccords.

**Conclusion :** même avec le continuum exponentiel exact, la positivité du forcing Selberg intégré ne suffit pas à donner Z≥0. Le modèle ne porte pas les poids Λ(n), donc ce n'est pas une réfutation de RH ou d'une propriété supplémentaire spécifique aux premiers.

### Contre-modèle générique complémentaire

Pour deux mesures positives α et ν, poser R=α−ν et D=xR+(α+ν)*R=xR+α*α−ν*ν. L'identité exacte ne permet pas d'inférer P_R≥0 de P_D≥0.

Contre-modèle : α=10δ_1+11δ_(9/2), ν=15δ_2. Alors :

Z=P_R=20−5t pour 2≤t≤9/2, puis Z=6t−59/2 pour t≥9/2.

Donc Z<0 sur (4,59/12). Pourtant :

D=10δ_1+70δ_2−225δ_4+(99/2)δ_(9/2)+220δ_(11/2)+121δ_9.

P_D est linéaire par morceaux, avec les valeurs suivantes :

| t | 1 | 2 | 4 | 9/2 | 11/2 |
|---|---:|---:|---:|---:|---:|
| P_D(t) | 0 | 10 | 170 | 195/2 | 2 |

Après 11/2, sa pente vaut 249/2>0 ; après 9, elle augmente encore. Donc P_D≥0 partout.

Ce modèle n'a pas α=e^(x/2)dx et ne constitue pas un contre-exemple au système arithmétique spécifique. Il réfute seulement l'idée qu'une réserve Selberg intégrée positive impose le signe par l'identité et la positivité des mesures seules. Une propriété supplémentaire des premiers ou du noyau exponentiel est indispensable.

## 6. Expérience discriminante recommandée

Au même plafond fini, comparer pour chaque bloc : H_initial, H_final, le vrai minimum de tous les H_préfixes et K (garde universelle du coude). Trois issues :

1. K≥0 : le bloc est certifié avec les seules données de masse, moment et support.
2. K<0 mais tous les H_préfixes≥0 : l'information intérieure perdue est quantitativement identifiée ; le bloc peut rester bon mais le certificat est trop grossier.
3. Un H_préfixe<0 : la règle proposée échoue réellement dans le modèle calculé ; vérifier alors précision et définition avant interprétation.

L'expérience doit conserver le plafond existant et tester une règle explicite. Elle ne sert pas à revendiquer une positivité globale par accumulation de fenêtres finies.

## 7. Synthèse critique

Acquis : récurrence exacte, garde intra-bloc optimale au niveau des données agrégées, contre-modèle endpoints, échec asymptotique du certificat à ratio fixé sous PNT, contre-modèle à l'inversion Selberg positive générique.

Ouvert : une estimation arithmétique indépendante donnant assez d'information intérieure pour payer la dette à toutes les échelles. Demander directement H_j≥0, K_j≥0 sans preuve arithmétique, la positivité de tous les stocks, ou la réussite de toutes les extensions, revient à déplacer l'obligation globale.
