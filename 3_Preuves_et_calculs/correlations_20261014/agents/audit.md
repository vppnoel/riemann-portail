# Audit indépendant du programme anchored_correlations.py

## Verdict

Audit réussi. Le programme a été inspecté puis reproduit à 85 chiffres décimaux, plafond 1000, sans modification. Une seconde intégration a été faite à 90 chiffres avec un crible premier et tous les intervalles entiers, indépendamment de l'intégration par cassures aux puissances premières utilisée par le programme. Les résultats imprimés concordent à une tolérance absolue de 10^-29.

La positivité de l'énergie est une identité exacte. Les valeurs numériques des énergies sont des diagnostics multiprécision ; elles ne sont pas des certificats d'une borne globale. La négativité du noyau de Möbius est, séparément, évaluée par intervalles dirigés à 400 bits.

## Contrôles

- 193 puissances premières jusqu'à 1000.
- Identité de diviseurs exacte pour 1000 entiers : les coefficients de log(p) sont comptés comme des entiers, sans comparer des logarithmes arrondis.
- Doubler Lambda(2) viole l'identité à 500 indices pairs, en commençant à 2.
- J(10)=29.0403512049705155997933751934128383819475496.
- J(100)=622.779291690150194028459085450601682747999351.
- J(1000)=22954.7733276957805008147337633038170199890282.
- L'intégration à termes positifs et la formule de corrélation ancrée donnent les mêmes résultats ; erreur du recoupement à 85 chiffres inférieure à 3e-77 au plafond 1000.
- Le noyau K_mu(log 15) est rigoureusement encadré, dans le modèle mpmath.iv à 400 bits, par -0.038 < K_mu(log 15) < -0.037. Il n'est donc pas un inverse préservant l'ordre par simple convolution positive.

## Homométrie renforcée : même masse, moment et support

P={0,30,80}, Q={0,1,6,8,10}, Qrev=10-Q={0,2,4,9,10}.

A=P+Q et B=P+Qrev donnent chacun 15 points distincts. La masse est 15, le premier moment 625, le minimum 0 et le maximum 90. Les ensembles ne sont ni des translations ni des réflexions globales l'un de l'autre.

Autocorrélations : nu_A=nu_P*nu_Q et nu_B=nu_P*reflected(nu_Q) décalé de 10. Comme la translation disparaît dans l'autocorrélation, les autocorrélations de A et B sont égales. Le programme vérifie cette égalité par comptage entier de toutes les différences signées avec multiplicité.

Pour le potentiel P_A(t)=sum_{a in A}(t-a)_+, on a P_A(3)=5, P_B(3)=4, puis P_A(7)=14, P_B(7)=15. Relativement à la même source mu=nu_A, S_A=0 partout et S_B(7)=-1.

La triple corrélation C3(h,k)=nombre de x tels que x,x+h,x+k appartiennent à l'ensemble vaut C3_A(1,6)=3 et C3_B(1,6)=0. Les amas sont assez espacés pour qu'aucun de ces triplets ne chevauche deux amas. L'ordre trois conserve donc une information perdue à l'ordre deux dans cet exemple précis. Il ne s'ensuit pas que toute triple corrélation impose la positivité.

Ces mesures sont un contre-modèle abstrait à la compression des données, et non des coefficients premiers ni un contre-exemple à RH.

## Coordonnées logarithmiques

E(x)=psi(x)-x,
J(X)=integral_1^X E(x)^2 dx,
F(y)=exp(-y/2) E(exp(y)),
R(Y)=exp(-2Y) J(exp(Y)).

R est localement absolument continue et, presque partout,

R'(Y)=F(Y)^2-2R(Y), R(0)=0.

Ainsi

R(Y)=integral_0^Y exp(-2(Y-u)) F(u)^2 du.

Cette représentation donne un réservoir à mémoire décroissante. Le forçage est positif sans supposer RH. Ce qui reste à démontrer est la bornitude de R, connue équivalente à RH pour les vrais coefficients Lambda. Un forçage positif ne suffit pas à limiter la taille du réservoir. Une borne de R n'impose pas non plus une borne ponctuelle de F ; les pics sont pondérés par leur largeur et leur poids.

## Limite essentielle du pont énergie vers Weil

Il faut conserver les vrais coefficients arithmétiques. Si a=Lambda+c*delta_2 avec c>0, alors

psi_a(x)-x = E(x)+c*1_{x>=2}.

Sous RH,

J_a(X) <= 2J_Lambda(X)+2c^2(X-2)_+ = O(X^2).

Pourtant le signal hybride construit en conservant le même terme archimédien vaut

S_a(t)=S_zeta(t)-(c/sqrt(2))*(t-log2)_+.

Sous RH, S_zeta est borné ; donc S_a finit par être négatif. La classe énergétique peut tolérer une modification finie, tandis que le signe de ce signal hybride ne le peut pas. La réduction est donc liée à l'identité exacte de zeta et à sa continuation analytique ; elle ne fournit pas un théorème universel de positivité pour des mesures arbitraires.

## Bénéfice et limitation

Bénéfice : un pont global classique, valide et techniquement différent de la construction de blocs ; des outils exacts pour distinguer identité arithmétique, corrélation stationnaire et énergie ancrée ; une obstruction certifiée à l'inversion de Möbius par positivité du noyau.

Limitation : aucune majoration inconditionnelle nouvelle J(X)=O(X^2) n'est établie. Les valeurs à trois plafonds et la courbe finie ne justifient ni la bornitude future ni une convergence vers une limite. La littérature montre même que le ratio dyadique n'a pas de limite.

Fichiers de recoupement : agents/audit.json et agents/audit85_results/anchored_results.json. L'empreinte SHA256 du programme audité est inscrite dans audit.json.

## Complément : contre-modèle inconditionnel de profil unitaire

Le profil a(1)=0 et a(n)=1 pour n>=2 donne psi_a(x)=floor(x)-1. Son défaut vaut E_a(x)=-1-{x}, donc |E_a(x)|<=2 et J_a(X)<=4(X-1), pour tout X>=1, sans RH.

La nouvelle fonction de certification du programme a été inspectée puis reproduite à 400 bits. Elle conserve le terme archimédien A du corpus mais remplace les coefficients premiers par le profil unitaire. La queue des 64 termes archimédiens retenus est dominée par une série géométrique positive ; Euler gamma est encadré par H_1024-log1024-1/(2*1024)+1/(12*1024^2), avec reste dirigé de taille au plus 1/(120*1024^4). Le résultat donne -1.338 < S_a(log1000) < -1.337, strictement négatif.

Ce contre-modèle renforce la nécessité de l'identité arithmétique sans supposer RH. Le mécanisme est précis : pour les vrais coefficients, le Mellin du défaut s'identifie à -zeta'/zeta-s/(s-1), donc les zéros deviennent des pôles exclus par l'holomorphie. Pour le profil unitaire, le même Mellin est zeta(s)-1-s/(s-1), qui peut être holomorphe sans exclure les zéros de zeta. Ainsi la borne quadratique seule n'impose pas le signe du signal hybride.

Le programme principal a été enrichi par le parent après l'audit initial ; l'empreinte initiale d'audit.json et celle du complément unit_profile_audit.json identifient les versions respectivement auditées. Aucun code n'a été modifié par l'auditeur.
