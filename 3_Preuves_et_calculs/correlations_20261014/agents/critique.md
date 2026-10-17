# Audit critique — corrélations, identité arithmétique et réduction globale

Statut : note interne de recherche. La réduction en énergie ci-dessous est classique ; aucune borne inconditionnelle nouvelle au niveau RH n'est obtenue.

## 1. Le vocabulaire « statistique » ne décide pas à lui seul de la force d'une approche

Il faut distinguer :

- des distributions moyennes qui ignorent une partie de la phase et les exceptions de densité nulle ;
- une énergie déterministe, ancrée, dont une borne est exigée pour chaque plafond X ;
- une reconstruction complète de l'objet, qui n'établit encore aucune propriété de signe.

Une moyenne peut donc fournir une obligation globale rigoureuse. Le candidat I(X) = integral_1^X (psi(x)-x)^2 dx est un exemple exact. Une prédiction GUE ou une autocorrélation stationnaire ne fournit pas automatiquement ce contrôle.

## 2. Audit du pont proposé par le parent

Posons E(x)=psi(x)-x et I(X)=integral_1^X E(x)^2 dx.

La proposition

RH si et seulement si, pour chaque epsilon>0, I(X)=O_epsilon(X^(2+epsilon))

est correcte.

Sens RH vers énergie : le majorant classique E(x)=O(sqrt(x) log^2 x) donne I(X)=O(X^2 log^4 X), donc le majorant annoncé pour chaque epsilon. Un résultat plus fort classique de Cramér donne déjà, sous RH, integral_X^(2X) E^2 = O(X^2), puis I(X)=O(X^2) par sommation dyadique.

Sens énergie vers RH : pour sigma>(1+epsilon)/2, l'intégration par parties donne

integral_1^infty E(x)^2 x^(-2sigma-1) dx < infinity.

En effet le poids appliqué à dI impose 2sigma+1>2+epsilon. Pour Re(s)>sigma, Cauchy–Schwarz assure

integral_1^infty |E(x)| x^(-Re(s)-1) dx < infinity,

car le second facteur est integral_1^infty x^(-2Re(s)+2sigma-1) dx. Cette convergence est uniforme sur les compacts d'un demi-plan plus petit, donc

H(s)=s integral_1^infty E(x) x^(-s-1) dx

est holomorphe sur Re(s)>1/2 lorsque la condition vaut pour chaque epsilon. Pour Re(s)>1,

H(s) = -zeta'(s)/zeta(s) - s/(s-1).

L'identité se prolonge ; le membre de droite ne peut donc avoir aucun pôle de zéro de zeta dans Re(s)>1/2. L'équation fonctionnelle réfléchit les éventuels zéros de l'autre moitié de la bande. Ceci établit RH. Le même argument avec epsilon=0 donne le sens inverse de la version plus forte I(X)=O(X^2).

Conclusion précise : on peut réduire la loi de signe globale à une borne de croissance d'une énergie positive. On n'a pas démontré cette borne ; l'énergie est positive inconditionnellement et sa positivité seule ne signifie rien pour RH.

## 3. Corrélation ancrée exacte

Pour tout X>=1, y compris réel,

I(X) = sum_{m,n<=X} Lambda(m)Lambda(n)(X-max(m,n))
       - sum_{n<=X} Lambda(n)(X^2-n^2)
       + (X^3-1)/3.

Preuve : développer (psi(x)-x)^2 et intégrer chaque indicatrice 1_{x>=n}. La convention aux entiers ne change aucune intégrale ; Lambda(1)=0. Les termes qui touchent exactement X sont nuls.

Le noyau K_X(m,n)=X-max(m,n) est un Gram :

K_X(m,n)=integral_1^X 1_{x>=m}1_{x>=n} dx.

La première somme est donc positive, mais cela ne domine pas le terme croisé. Trois contributions de taille X^3 se compensent ; PNT seul assure I=o(X^3), trop faible. La cible est O(X^2), ou O_epsilon(X^(2+epsilon)). Le noyau conserve la position absolue et chaque coupure X, information perdue par une autocorrélation dépendant uniquement de m-n.

## 4. Contre-exemple exact aux seules corrélations par décalages

A={1,2,5,11,13,18} et B={0,1,8,11,13,17} ont :

- même masse 6 ;
- même premier moment 50 ;
- mêmes différences signées avec leurs multiplicités ;
- différences positives 1,2,...,13,16,17, chacune une fois.

Ce sont les ensembles homométriques classiques de Bloom, après translation pour égaliser le barycentre.

Pour nu_A=sum_{a in A} delta_a et nu_B=sum_{b in B} delta_b, les autocorrélations nu_A * reflected(nu_A) et nu_B * reflected(nu_B) sont exactement égales. Pourtant leurs potentiels P_nu(t)=sum (t-a)_+ diffèrent :

| t | P_A(t) | P_B(t) | P_A-P_B |
|---|---:|---:|---:|
| 2 | 1 | 3 | -2 |
| 8 | 16 | 15 | 1 |
| 18 | 58 | 58 | 0 |

Fixer mu=nu_A donne S_A identiquement nul et S_B(2)=-2 : une même autocorrélation, masse et premier moment ne force pas la positivité relative au même mu.

Cela ne prétend pas construire une autre fonction zeta avec les mêmes contraintes arithmétiques. Cela démontre seulement l'information perdue par ce résumé statistique.

L'énergie ancrée n'est pas réfutée par cet exemple. Pour le jouet Q_nu(X)=integral_0^X (nu([0,u])-u)^2 du, Q_A(6)=16 et Q_B(6)=22. Les valeurs aux coupures intérieures diffèrent. Après le support entier, Q_A(18)=Q_B(18)=868, ce qui souligne encore la nécessité de toutes les coupures, pas d'un seul bilan terminal.

Vérification : différences et intégrales de jouet ont été calculées en nombres entiers / fractions exactes, indépendamment des calculs en flottants.

## 5. Une énergie globale n'efface pas nécessairement un mode hors ligne

Pour le modèle E_beta(x)=2|c| x^beta cos(gamma log x+phi), beta>1/2 et gamma!=0, on obtient

integral_1^X E_beta(x)^2 dx
= 2|c|^2 X^(2beta+1) [1/(2beta+1) + Re(exp(2i phi) X^(2i gamma)/(2beta+1+2i gamma))] + O(1).

Le crochet a un minimum strictement positif :

1/(2beta+1) - 1/sqrt((2beta+1)^2+4gamma^2) > 0.

L'énergie divisée par X^2 diverge donc comme X^(2beta-1), malgré l'oscillation du signe. C'est une illustration ; le passage pour zeta complète est donné par le Mellin holomorphe ci-dessus et ne suppose pas un zéro de partie réelle maximale isolé.

## 6. Carte d'identité et réductionnisme

L'identité Lambda * 1 = log détermine Lambda de manière unique, par inversion de Möbius : Lambda=mu*log. Elle distingue donc les vrais poids premiers de contre-modèles arbitraires. Mais l'identification de l'objet ne démontre pas la borne de son énergie. Il faut exploiter une conséquence quantitative nouvelle de cette identité, et conserver les signes de mu et les termes de bord.

Une équation fonctionnelle et des symétries seules sont insuffisantes. Toute proposition qui utilise une corrélation déjà démontrée sous RH en entrée doit être marquée conditionnelle et ne peut servir à prouver RH.

Il convient de parler de réduction globale connue et de nouvelle organisation du travail, pas d'une percée mathématique nouvelle.

## 7. Sources primaires vérifiées

1. Richard P. Brent, David J. Platt, Timothy S. Trudgian, The mean square of the error term in the prime number theorem, Journal of Number Theory 238 (2022), 740–762 ; arXiv:2008.06140. PDF ouvert : https://arxiv.org/pdf/2008.06140 (réf. navigateur de cet agent turn192view0). Pages 1–2 : résultat conditionnel Cramér O(X^2), borne supérieure 0.8603 sous RH, absence de limite du ratio dyadique ; page 2 : si RH est fausse, ratio non borné. Ne pas utiliser sa borne conditionnelle comme entrée inconditionnelle.

2. H. L. Montgomery, The pair correlation of zeros of the zeta function, 1973, PDF auteur : https://www-personal.umich.edu/~hlm/paircor1.pdf (réf. turn189view0). La première page annonce explicitement RH comme hypothèse de tout le papier. Ceci n'interdit pas toute recherche de corrélations inconditionnelles ; cela signale précisément la circularité de ce résultat utilisé en sens inverse.

3. Le fait homométrique est vérifié ici directement ; la littérature de fond comprend Bloom et la théorie des ensembles homométriques. Aucun recours à cette référence n'est nécessaire au calcul exact donné.

## 8. Verdict de cette confrontation

Le pont le plus net est : identité arithmétique exacte -> corrélation ancrée / énergie -> borne globale -> exclusion analytique des zéros hors ligne -> positivité globale de Weil.

L'étape ouverte est la borne globale, de portée RH. Un calcul fini de I(X)/X^2 ne l'établit pas. Aucune nouvelle majoration inconditionnelle à l'exposant 2 n'a été trouvée dans cette passe.
