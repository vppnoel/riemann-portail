# V6.39 — Relecture indépendante des contraintes exactes V13

Date : 12 octobre 2026. Statut : relecture mathématique et informatique interne. Aucun résultat sur les zéros n'est calculé ici ; aucune expertise externe n'est prétendue.

## 1. Question effectivement résolue

Les documents 61 et 62 demandent si le défaut de multiplicativité D peut varier quand on fixe exactement le premier coefficient complexe, l'ancre d'Euler et l'angle projectif. Le contrôle complexe est plus fort que le rapprochement des seuls modules a1 effectué en V6.37.

La construction examinée fixe, dans chaque strate d'ancre i et d'angle r, le coefficient particulier

\[
A=a(1)=\cos(r)z_i,\qquad z_j=e^{-i\phi_j}.
\]

Elle ne démontre pas la faisabilité pour tout coefficient complexe A arbitrairement prescrit, ni pour toutes les anciennes valeurs du plan V6.37. Elle suffit pour une famille nouvelle explicitement définie.

## 2. Phases, branche et symétrie

Les indices impairs modulo 13 sont k = 1, 3, 5, 7, 9, 11. Le générateur 2 de (Z/13Z)* donne les caractères χ_k(2^m) = exp(2πikm/12). Le nombre racine est ε_k = τ(χ_k)/(i√13). Pour ces caractères primitifs impairs, |ε_k| = 1 et

\[
\varepsilon_{12-k}=\overline{\varepsilon_k}.
\]

Le signe moins provenant de χ_k(−1) dans la somme de Gauss est compensé par le facteur i de la parité impaire. Employer τ(χ_k) et non τ(\overline{χ_k}) est nécessaire pour rester compatible avec le module historique.

Définir z_k² = \overline{ε_k} et Re z_k > 0 reproduit φ_k = Arg(ε_k)/2 lorsque ε_k ≠ −1. La positivité de Re z_k doit être contrôlée ; une prescription de branche sans cette vérification serait incomplète. Les intervalles construits dans cette version écartent cette exception.

La conjugaison permute les coordonnées selon k ↔ 12−k, soit [5,4,3,2,1,0] dans l'ordre historique. Elle ne fournit pas une nouvelle réplication indépendante.

## 3. Noyau exact et géométrie projective

Posons

\[
K_i=\{u\in\mathbb R^6:u_i=0,\ \sum_jz_ju_j=0\}.
\]

Il s'agit de trois contraintes linéaires réelles. L'affirmation « dimension au moins trois » est insuffisante pour conclure que D varie. Le rang vaut néanmoins exactement trois ici : après retrait de la colonne i, il reste une paire conjuguée z_j, \overline{z_j} avec Re z_j > 0 et Im z_j ≠ 0. Les colonnes (Re z_j, Im z_j) et (Re z_j, −Im z_j) ont un déterminant non nul. Le noyau réel a donc dimension trois, et ses vecteurs unitaires forment une sphère S².

Pour t = cos(r), s = sin(r), u ∈ K_i de norme un et 0 < r < π/4,

\[
c_\pm=t e_i\pm s u,
\qquad \|c_\pm\|_2=1,
\qquad \sum_jz_j(c_\pm)_j=t z_i.
\]

De plus, |(c_±)_j| ≤ s < t pour j ≠ i. L'ancre la plus proche est donc unique, et arccos(max_j |(c_±)_j|) = r. Il s'agit de l'angle projectif, non du sinus utilisé dans certains calculs historiques de projection. Le signe positif de la coordonnée d'ancrage fixe le représentant projectif ; les deux points ne sont pas opposés.

## 4. Vérification du défaut cubique

Dans `relief_direct.a1_and_defect`, b_j = c_j z_j et N = Σ|b_j|². Pour une direction normalisée, N = 1. Le défaut considéré est

\[
D(c)=1+|A|^2-2\Re\!\left(A\sum_j|b_j|^2\overline{b_j}\right).
\]

Ce terme cubique en b doit être conservé : remplacer Σ|b_j|²\overline{b_j} par une somme quadratique définirait un autre objet. La formule se retrouve indépendamment en développant le défaut de multiplicativité sur les 12 × 12 couples de classes non nulles et en appliquant l'orthogonalité des caractères.

Puisque u_i = 0 et A = t z_i,

\[
\sum_j |b_j|^2\overline{b_j}
=t^3\overline{z_i}\pm s^3\sum_j u_j^3\overline{z_j}.
\]

Par conséquent,

\[
D(c_\pm)=1+t^2-2t^4\mp2ts^3P_i(u),
\quad
P_i(u)=\Re\!\left(z_i\sum_j u_j^3\overline{z_j}\right),
\]

et

\[
D(c_-)-D(c_+)=4ts^3P_i(u).
\]

Cette identité a été redérivée avant la lecture des résultats du nouveau pilote. Elle montre que la variation dépend de la non-annulation du polynôme cubique P_i sur K_i, et non de la seule dimension de K_i.

## 5. Témoin explicite par paires conjuguées

Prenons les deux paires conjuguées qui n'incluent pas l'ancre : (j,j*) et (ℓ,ℓ*). Posons a = sinφ_j, b = sinφ_ℓ et

\[
v_j=b,\quad v_{j*}=-b,\quad v_\ell=-a,\quad v_{\ell*}=a,
\quad v_i=v_{i*}=0.
\]

La conjugaison donne directement Σv_jz_j = 0. Avec n = √(2(a²+b²)) et u = v/n, on obtient exactement

\[
\sum_jv_j^3\overline{z_j}=2iab(b^2-a^2),
\qquad
P_i(u)=\frac{2\sin\phi_i\,ab(b^2-a^2)}{[2(a^2+b^2)]^{3/2}}.
\]

Cette formule est validée algébriquement. Les trois parties réelles des nombres racines des représentants k = 1, 3, 5 sont distinctes, et leurs parties imaginaires sont non nulles. Puisque sin²φ_k = (1−Re ε_k)/2, ces deux contrôles suffisent à garantir P_i(u) ≠ 0 pour toutes les ancres. Il en résulte deux défauts distincts au même coefficient complexe, à la même ancre et au même angle, pour tout 0 < r < π/4.

Le témoin se situe sur une ligne antisymétrique du noyau tridimensionnel. Il ne maximise pas P_i sur S². Ni l'optimalité du contraste ni l'existence de toutes les tailles de contraste ne sont démontrées.

## 6. Limites utiles pour la prochaine expérience

Les premiers recoupements avec les phases historiques trouvent P_k1 ≈ −0,02980463, P_k3 ≈ −0,06303208 et P_k5 ≈ −0,03766727, avec signes inversés pour leurs conjugués. Aux angles 0,45, 0,65 et 0,75 radian, les contrastes absolus de ces témoins sont compris approximativement entre 0,008834 et 0,058427. Ces valeurs descriptives sont recoupées par les enclosures validées de la section suivante.

Ces témoins n'atteignent pas le seuil de contraste D = 0,25 du plan V6.37. Cela n'établit pas l'impossibilité d'atteindre ce seuil ailleurs dans K_i ; aucune optimisation globale n'a été réalisée. Le nouveau plan devra définir un critère adapté avant de consulter les zéros.

Dans chaque strate le coefficient A est fixé exactement. Il change avec i et r entre les strates. Il serait incorrect de présenter toutes les strates comme une expérience à un unique A global.

La construction vérifie u_{j*} = −u_j. La conjugaison transforme donc le membre + de l'ancre i en le membre − de l'ancre i*. Pour un observable symétrique en |Im(s)|, les 18 strates historiques se répartissent en neuf classes conjuguées. Un nouveau comptage doit distinguer ces copies des réplications indépendantes.

Enfin, fixer A ne conserve pas tous les autres coefficients. Une éventuelle différence de détection des zéros restera une comparaison conditionnelle de deux fonctions, sans attribution causale à D. Le nouveau résultat de cette étape est une faisabilité mathématique locale, sans conséquence établie sur RH.

## 7. Audit des enclosures et de la reproduction

Fichiers relus : `src/v639_contraintes.py`, `src/v639_rational.py`, `scripts/run_v639_contraintes.py`, `data/v639_contraintes.json`, `data/v639_contraintes_precision120.json`, `data/v639_certificat_rationnel.json` et le lemme constructif `preuves/LEMME_CONTRAINTES_V13_V639.md`.

Le module reconstruit les six sommes de Gauss à 80 et 120 décimales d'intervalles. Il ne reprend aucune phase binary64 du module historique pour établir les enclosures. Le demi-angle est défini par une racine carrée réelle positive et par −Im ε/(2 Re z), ce qui évite les ambiguïtés d'un argument numérique. La conjugaison est construite explicitement à partir des parties réelle et imaginaire ; elle ne dépend pas de la méthode défectueuse `iv.mpc.conjugate` de mpmath 1.3.0.

Les bornes décimales de publication sont arrondies vers l'extérieur à partir des endpoints binaires, avec des fractions exactes. Le champ `binary_endpoints` conserve les bornes plus fines ; les décimales à douze places sont des enclosures volontairement élargies, et non douze chiffres présentés comme une erreur absolue calculée a posteriori.

### Certificat arithmétique indépendant de mpmath

Le module `v639_rational.py` fournit une seconde preuve des seules inégalités nécessaires à la non-constance : trois parties réelles distinctes, six parties imaginaires non nulles et branches évitant ε = −1. Il n'utilise que les entiers Python et `Fraction`, avec `factorial` et `isqrt` ; aucun calcul transcendant flottant ni arithmétique complexe n'y intervient.

Les bornes de π utilisent l'identité de Machin

\[
\pi=16\arctan(1/5)-4\arctan(1/239).
\]

La justification de branche est explicite : pour α = arctan(1/5), β = arctan(1/239), on a tan(2α) = 5/12 et tan(4α) = 120/119. Puisque 0 < 4α < π et que cette dernière tangente est positive, 4α < π/2 ; de plus β < α, donc 0 < 4α−β < π/2. La formule de soustraction donne tan(4α−β) = 1, d'où 4α−β = π/4. Les séries alternées de l'arctangente, tronquées respectivement après 20 et 5 termes, encadrent exactement α et β par le premier terme omis avec son signe.

Pour chaque somme de Gauss, les angles sont réduits rationnellement modulo 2π et encadrés dans (−4,4). Le sinus est développé jusqu'au degré 48, dont le coefficient pair est nul ; son reste est borné par 4⁴⁹/49!. Le cosinus est développé jusqu'au degré 49, dont le coefficient impair est nul ; son reste est borné par 4⁵⁰/50!. Les polynômes sont évalués au milieu rationnel de l'intervalle d'angle. Ajouter sa demi-largeur est légitime, puisque les dérivées de sin et cos ont un module au plus un sur les réels.

La racine carrée de 13 est encadrée par les deux rationnels successifs déduits de `isqrt(13·10⁶⁰)`. Les inclusions se vérifient directement en élevant les bornes au carré. Les sommes finies, divisions par des intervalles positifs et contrôles de signes sont ensuite entièrement rationnels.

Le certificat JSON a été régénéré et sa structure est identique à celle sauvegardée. Les bornes de la racine, la tangente de Machin, les six signes imaginaires et la séparation des trois parties réelles ont été vérifiés en fractions exactes. En contrôle supplémentaire, les douze composantes des nombres racines calculées à 120 décimales d'intervalles sont strictement contenues dans les boîtes rationnelles.

**La non-annulation du témoin et le théorème de faisabilité ne dépendent donc pas de mpmath.** Ils résultent des identités algébriques et des inégalités de ce certificat rationnel. Les enclosures beaucoup plus fines des contrastes continuent, elles, d'utiliser le backend `mpmath.iv`.

### Contrôles indépendants effectivement exécutés

1. Les **618 enclosures** de chaque certificat ont été parcourues avec une reconstruction des endpoints en `Fraction`. Toutes les bornes décimales contiennent leurs bornes binaires, dans le bon ordre. Les 618 intervalles à 120 décimales sont contenus dans leurs correspondants à 80 décimales.
2. Une reconstruction séparée à **160 décimales d'intervalles**, sans import du module nouveau, a refait les six sommes de Gauss en réunissant les angles des caractères et de la racine treizième. Les douze composantes des nombres racines et les douze composantes des phases sont contenues dans les enclosures archivées aux deux précisions.
3. Les deux familles de témoins ont été reconstruites indépendamment : quatre angles par ancre, soit **24 couples par famille**, avec six témoins antisymétriques et six témoins par mineurs de trois colonnes, chacun repris aux quatre angles. Les 48 valeurs de P et les 48 écarts de D sont contenus dans leurs enclosures binaires à 80 et 120 décimales.
4. Pour les **96 directions** ainsi définies, D a été recalculé par sa définition originale : coefficients périodiques sur les douze classes non nulles, puis somme des carrés de défaut sur les **12 × 12 couples**. La formule cubique du module n'a pas servi à ce recoupement. Les 96 résultats, ainsi que les coefficients complexes A reconstruits, sont contenus dans les enclosures binaires sauvegardées.
5. La preuve constructive a été relue dans son intégralité. Sont également valides la preuve |τ|² = 13, le déterminant de la paire conjuguée, la caractérisation de l'image exacte de D comme intervalle par compacité et connexité de S², et les développements D₀ = 3r² + O(r⁴), |ΔD| = 4|P_i|r³ + O(r⁵).

Les témoins par mineurs augmentent les contrastes effectivement construits aux trois rayons historiques : les enclosures extrêmes sont **0,029444878421 à 0,143780083557**. Les témoins antisymétriques donnent **0,008834183870 à 0,058426643054**. Aucun de ces témoins n'atteint 0,25. La sélection informatique par le plus grand minorant de |P| choisit un témoin parmi dix triplets ; elle ne constitue pas une preuve d'optimalité globale sur S². En cas de chevauchement d'intervalles, elle ne démontre pas non plus à elle seule un maximum exact parmi les dix valeurs.

### Statut du certificat et des coefficients exportés

La preuve symbolique porte sur les objets définis par les sommes de Gauss, les racines de phase et la normalisation exacte. Les coordonnées binary64 exportées pour les programmes historiques n'obéissent aux contraintes qu'à une tolérance numérique ; elles ne doivent pas être présentées comme des coefficients exacts. Un intervalle de résidu contenant zéro ne prouve pas à lui seul l'égalité exacte : celle-ci vient des identités analytiques, et l'intervalle contrôle leur implémentation.

Les enclosures fines utilisent le backend `mpmath.iv`. Leur reconstruction indépendante emploie le même backend à une autre précision : elle recoupe le code et les données, sans constituer une certification formelle de la bibliothèque elle-même. Leur validité numérique reste liée au modèle d'arithmétique d'intervalles déclaré. Le certificat rationnel indépendant établit toutefois toutes les inégalités nécessaires au théorème de non-constance. Aucun comptage de zéros, aucune région sans zéro et aucune causalité ne sont certifiés par ce travail.

## 8. Verdict et décision de protocole

**La faisabilité est établie pour la famille A = cos(r)z_i, pour chacune des six ancres et tout 0 < r < π/4.** Le coefficient complexe fixé ne force pas D à être constant. Le témoin explicite et les enclosures donnent un résultat mathématique local contrôlable ; l'étape 1 proposée après V6.38 peut être considérée achevée dans cette portée.

La prochaine étape devra fixer la famille de témoins, les rayons, le contraste minimal et le traitement des strates conjuguées avant consultation des zéros. Elle testera une association conditionnelle et un mécanisme encore ouvert, avec des contrastes plus petits que ceux du plan V6.37. Les anciennes hauteurs de détection ne peuvent pas être transférées à ces nouvelles directions.
