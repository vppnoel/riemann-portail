# V649 — Audit critique de la compensation multi-premiers

Analyse et nouveau rapport seulement. Les diagnostics flottants ne sont pas des plafonds opératoires certifiés. Fourier unitaire : toutes les intégrales de multiplicateurs et de Grams duaux utilisent dt, sans facteur 1/(2π) supplémentaire.

## 1. Identité et seuils

Pour D=2S, prendre q=p^m≤exp(D), avec poids c_q=log(p)/p^(m/2). Poser
b_S(t)=a(t)+2Σ_q c_q[1−cos(t log q)], C_S=C0+2Σ_q c_q.
Alors Q_W(f)=∫[b_S(t)−C_S]|f̂(t)|²dt pour les tests admissibles portés par [−S,S]. L'identité est exacte. Le coût b_S est positif ; cela ne donne PAS le signe de b_S−C_S ni celui de la forme comprimée.

La série et les sommes sont finies à support fixé. Les puissances utilisent log p, PAS log q=m log p. En particulier q=4 a pour poids log2/2 et phase 2t log2.

Seuils S_q=log q/2 : q=2 (~0.346574), 3 (~0.549306), 4 (~0.693147), 5 (~0.804719), 7 (~0.972955), 8 (~1.039721), 9 (~1.098612), 11 (~1.198948). Donc S=.55 et .6 contiennent 2,3 ; S=.7 contient 2,3,4. Ces décimales sont descriptives : la sélection certifiée doit comparer log q et 2S par intervalles.

À l'égalité log q=D, la corrélation h_f(D) est nulle pour tout f∈L² de ce support : les supports ne se rencontrent qu'en un ensemble de mesure nulle. Inclure ou exclure ce terme donne la même forme. Le multiplicateur b_S et la constante C_S sautent séparément ; leur différence ajoutée est −2c_q cos(t log q), dont l'intégrale contre |f̂|² est nulle sur les domaines de diamètre ≤log q. Il faut expliquer ce changement de représentation sans prétendre que les multiplicateurs eux-mêmes sont continus.

## 2. Puissances et dépendance des phases

Pour chaque p, les phases sont harmoniques : θ_p=t log p et θ_{p^m}=mθ_p. Elles ne sont pas des variables indépendantes. On peut grouper
2log p Σ_{m≤M_p}p^(−m/2)[1−T_m(cos θ_p)],
où T_m est le polynôme de Chebyshev. Chaque contribution est positive, mais le groupement conserve les relations.

Pour m=1,2, le groupe vaut
2log p(1−x)[p^(−1/2)+2p^−1(1+x)], x=cos θ_p.
La résonance de p annule toutes ses puissances à la fois. Des diagnostics traitant ces phases comme aléatoires indépendantes perdraient ce fait. La relation entre différents p doit elle aussi rester celle d'un UNIQUE t ; même l'indépendance rationnelle des log p ne fournit pas un majorant uniforme des compensations pondérées.

## 3. Obstruction démontrée : la norme L² saute au seuil

Soit une nouvelle longueur a=log q et a<D<2a, δ=D−a. Les deux bandes d'attache ont longueur δ et sont disjointes. Le terme
Q_q(f)=2c_q Re⟨f,U_af⟩
satisfait |Q_q|≤c_q M_edge≤c_q||f||².

Cette borne est atteignable : choisir un bump φ dans la bande gauche, puis f=(φ+U_aφ)/sqrt2 avec ||φ||=1. La corrélation vaut 1/2 et Q_q=c_q. Avec le signe moins, elle vaut −c_q. On peut imposer les deux moments exponentiels à φ lui-même (le sous-espace de bumps à deux moments nuls est infini), ce qui les impose également à f et à sa translation. Ces témoins peuvent être lisses ; ils appartiennent donc au domaine énergétique.

Par conséquent la norme du nouveau couplage comprimé dans L² est exactement c_q immédiatement après le seuil, alors qu'elle est nulle à D=a. Aucune continuité en norme opératoire L² à travers ce seuil ne peut être postulée. Les corrélations restent continues pour des tests fixés/convergeant fortement ; cette continuité ne devient pas uniforme sur la boule unité L².

Cette obstruction concerne le couplage nouveau, PAS le signe de Q_W. Elle interdit une stratégie de transport fondée uniquement sur une petite largeur géométrique payée en norme L².

## 4. Pont démontré : le même seuil est petit dans la métrique énergétique

Noter w(t)=e^(−t/2)/(1−e^(−2t)), J(d)=∫_d^∞w(t)dt. L'énergie de translation contient le potentiel
E(f)≥∫[J(S−x)+J(S+x)]|f(x)|²dx.

Sur les bandes d'attache, ce potentiel est au moins J(δ)+J(a). En effet J est décroissante et convexe, et le minimum sur une bande est atteint à son bord intérieur, dont les distances sont δ et a. Donc
E(f)≥[J(δ)+J(a)]M_edge,
|Q_q(f)|≤c_q/[J(δ)+J(a)]·E(f).

J(δ)→∞ lorsque δ↓0. Le coût nouveau tend ainsi vers zéro en norme de forme RELATIVE à R=mass+E, bien que sa norme L² saute à c_q. C'est un pont de transport utile et un diagnostic précis du choix de métrique.

Les mêmes bandes prouvent simultanément le couplage et sa localisation énergétique : un vrai coup double. Pour plusieurs termes nouvellement entrants, sommer les majorants relatifs est prudent ; conserver leurs recouvrements peut améliorer la borne, mais nécessite une preuve jointe.

Cela ne prolonge PAS automatiquement un certificat de S0 à S>S0 : il faut également contrôler la forme ancienne sur le domaine agrandi. Le lemme isole et réduit seulement le coût des nouveaux premiers. Les normes doivent être nommées dans les ports, et le même μ ne peut être transféré silencieusement d'une métrique à une autre.

### Enveloppe spatiale jointe proposée par root

Pour chaque déplacement d=log q<D, Cauchy donne une enveloppe valable pour TOUT d : D_q(x)=c_q[1_{x≤S−d}+1_{x≥−S+d}]. Les deux indicatrices se recouvrent si d<S et leur multiplicité doit être conservée. Alors |Q_pr|≤∫D_S|f|², D_S=ΣD_q.

Le potentiel V_S(x)=J(S−x)+J(S+x) est symétrique et convexe ; sa valeur minimale sur un segment est atteinte au point le plus proche de 0. D_S est constant sur un nombre fini de segments, dont les bornes proviennent des attaches S−d et −S+d. Calculer alpha≥sup_x D_S(x)/V_S(x) par ces segments est donc certifiable en intervalles. Les points frontières de segments, de mesure nulle, ne modifient pas l'intégrale.

On obtient |Q_pr|≤alpha E et Q≥(1−alpha)E−C0 mass. Une borne E≥lambda mass donne ensuite Q≥[(1−alpha)lambda−C0]mass SI alpha<1. Ce calcul ne double pas l'énergie : il conserve une fraction 1−alpha avant de minorer. En revanche l'inférence Q_pr≤alpha lambda mass à partir de E≥lambda mass serait fausse.

Pour S=.7, le déplacement log2 est déjà inférieur à S ; les bandes de ce premier se recouvrent. Un gabarit utilisant uniquement l'union de bandes sans multiplicité ne s'applique donc plus. Le schéma des indicatrices ci-dessus couvre ce régime sans nouvel argument.

Près du seuil, J(delta)~(1/2)log(1/delta), donc le coût relatif nouveau est O(1/log(1/delta)), et non proportionnel à la longueur delta. Ce taux lent peut compter dans l'efficacité réelle du transport. Les maxima de l'enveloppe ancienne et nouvelle ne doivent pas être remplacés par une indépendance de leurs localisations.

## 5. Opérateur commun multi-premiers

Le schéma B_U=(1/π)∫(U−b_S(t))_+|r_t⟩⟨r_t|dt demeure valable dans chaque parité, avec le même Gram des deux moments. b_S≥a permet une exclusion de queue indépendante du nombre de premiers, si a(T)_lower≥U.

Q≥(U−C_S)mass−B_U est un minorant suffisant. Il faut U>C_S et une norme certifiée ||B_U||<U−C_S pour une coercivité directe. La norme de Nyström et deux résolutions concordantes ne suffisent pas. Une matrice arrondie peut avoir une petite valeur négative : plafonner lambda_max puis utiliser la positivité de B reste la bonne argumentation.

Les constantes dérivatives du mono-premier doivent être recalculées : ajouter 2Σc_q log q à |b'| et 2Σc_q(log q)² à |b''| est un majorant simple. La dépendance harmonique peut affiner ces coûts ; ne pas garder 13/2 et 33 sans vérifier le nouveau régime. La constante de conversion R doit également être reconstruite à partir d'une borne du couplage premier complet.

Les sources/têtes/queues de B_U sont des objets bornés du minorant. Leur certification ne certifie pas automatiquement les sources fortes de la forme Q originale.

### Éviter une tête brute lorsque U augmente

Comme a(t) croît logarithmiquement, augmenter U peut forcer une borne T immense puis une interpolation spatiale de très grand degré. Une autre décomposition conserve le même opérateur : B_U=B_low+B_high selon t≤T0 ou t>T0. Plancherel donne ||B_high||≤max(0,U−a(T0)), sans facteur T. Ajouter ce plafond entier au plafond de B_low peut être trop coûteux ; l'utiliser comme une borne de queue dans un Schur est potentiellement plus utile.

Pour le bloc positif B_high, la norme carrée de son bloc croisé est au plus le produit des normes des blocs diagonaux de tête et de queue. Le bloc de tête peut être petit parce que les fonctions de tête ont peu de Fourier aux grandes fréquences. Des bornes d'intégration par parties rendent cette propriété certifiable. Une tête fenêtrée à plusieurs zéros de bord, par exemple construite à partir du générateur différentiel P déjà présent dans le corpus, peut donner à la fois moments admissibles et décroissance fréquentielle forte.

Ce raccord recyclerait norme, tête, sources et queue, sans représenter directement toutes les ondes jusqu'à une coupure énorme. Les constantes, Grams et résidus doivent encore être construits ; aucun gain numérique ni certificat supplémentaire n'est revendiqué ici.

## 6. Convergence et portée

L'extension S→∞ introduit une somme croissante de premiers et puissances. La finitude à chaque S et la stabilité numérique locale ne fournissent ni domination uniforme ni convergence opératoire de la représentation compensée. Le coût positif b_S et C_S peuvent croître fortement tout en se compensant dans les tests ; prendre leurs limites séparément serait injustifié.

Priorité recommandée : certifier un premier régime 2+3, vérifier les budgets du coût conjoint et construire un transport relatif des nouvelles bandes. Puis distinguer les difficultés d'agrandissement du domaine de celles d'entrée d'un terme arithmétique. Une collection croissante de supports n'est pas une loi couvrante.

Trois statuts à conserver : identité/preuve analytique ; calcul d'intervalles avec budgets complets ; exploration sélectionnant les paramètres. Aucun résultat de ce rapport ne prouve RH ou un contre-exemple à RH.

## 7. Relecture du module et du journal des paiements joints

Le module multi_prime_compensation.py et v649_joint_payment_resultats.json ont été lus. Les règles de prime_power, l'ordre des ruptures, les densités 2→1 pour les bandes recouvrantes et 0→1 pour les bandes disjointes, et la minoration du potentiel au bord gauche positif sont correctes. Les budgets dérivatifs utilisent les constantes archimédiennes 5.7225 et 32.416 puis ajoutent les termes de phase, correctement pondérés par log p et log q.

Un correctif de garde a été signalé à root : l'activation doit refuser une comparaison dont l'intervalle FERME du logarithme contient 2S, y compris quand hi(log q)==2S. Avec le test strict initial, choisir S=hi(log2)/2 pouvait omettre un premier réellement actif. Le correctif est lo(d)<=2S<=hi(d)→refus. Les supports du journal sont éloignés de ce cas et leurs résultats ne sont pas affectés.

Statut final : le correctif fermé a été appliqué au module, vérifié en lecture, et un test de régression est annoncé par root. Aucun autre correctif substantiel n'est demandé.

alpha_lower et alpha_upper encadrent le SUPREMUM DE L'ENVELOPPE D/V, pas la norme optimale de Q_pr/E. L'enveloppe est une majoration prudente. Une valeur >1 à S=2 démontre l'insuffisance de ce paiement relatif pour conserver une fraction positive d'énergie ; elle ne démontre pas une perte de signe de Q_W. Les scopes du journal conservent global_RH_claim=False et extended_positive_support_certificate=False.

## 8. Relecture finale de l'article 74

Les lemmes L1–L8 ont été relus. Aucun correctif substantiel restant. L'article explique explicitement que alpha_lower borne le supremum de l'enveloppe et non la norme optimale. Les correcteurs de moments O(sqrt(delta)) peuvent être choisis dans un sous-espace intérieur fixe à matrice de moments inversible ; le Rayleigh du couplage normalisé tend donc bien vers c_q.

Le lemme des phases finies a un infimum nul : l'approximation simultanée par tiroirs donne des indices arbitrairement grands, puisqu'un ensemble borné d'indices ne pourrait approcher indéfiniment un rapport irrationnel sans égalité exacte. Un seul premier se traite par ses périodes. Les puissances restent harmoniques et ne sont pas indépendantes.

La séparation positive des poids et la borne de queue par Plancherel sont correctes. L'inégalité PSD du bloc croisé ||C||²≤||H||||K|| est valide. Le domaine, l'énergie, le transport sous condition et les statuts exploratoires sont explicitement distingués. Le certificat positif reste limité au domaine antérieur ; aucun accroissement positif de support n'est revendiqué.
