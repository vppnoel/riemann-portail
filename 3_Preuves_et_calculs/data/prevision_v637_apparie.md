# V6.37 - Ancrage apparié V13 : prévision avant comptage

Suite de la question inscrite dans le navigateur V6.36. V13 est l'espace
impair modulo 13 (six caractères). La génération et l'appariement n'utilisent
aucune évaluation de fonction L ni aucun zéro. La spécification complète,
les graines, les calipers et les strates infaisables figurent dans le manifeste.

Les couples contrôlent exactement l'ancre d'Euler et l'angle projectif.
Dans le bras A1, le défaut D est proche et |a(1)| varie ; dans le bras D,
|a(1)| est proche et D varie. L'appariement reste descriptif, sans interprétation
causale ni échantillonnage aléatoire d'une population.

P1 : les six témoins d'Euler ne présentent aucune détection hors droite sous 150.
P2 : les comptages total et critique sont cohérents et stables aux raffinements.
P3 : dans le bras A1, les signes strictement comparables favorisent davantage une
première détection plus tardive lorsque |a(1)| augmente (plus de signes positifs
que négatifs). Publier les égalités, les non-détections et les ordres indéterminés.
P4 : dans le bras D, la direction du contraste n'est pas uniforme entre ancres
et rayons. Un signe contraire ne constitue pas une preuve d'absence d'effet.

Plafond fixé à 150 ; bilans à 50, 100 et 150. Pas verticaux 0,02 et 0,01 ;
pas horizontaux maximaux 0,05 et 0,025, puis raffinement adaptatif. La droite
critique est également reprise à 0,005 pour toutes les directions. Tout niveau
non résolu, différence de comptage, défaut de parité ou marge relative de bord
inférieure à 1e-10 rend la direction non admissible dans le résumé principal.
Le bord droit est choisi par domination du premier coefficient, avant comptage.

Recoupement indépendant à 50 chiffres : premier couple de chaque bras et ancre
au rayon médian, pour chaque membre présentant une détection admissible. Les
cas où aucune racine n'est localisée sont conservés comme tels. Cette vérification
confirme des racines représentatives, pas l'absence de racines ailleurs.

La première détection est une tranche de hauteur entière pour |Im(s)|. Ce n'est
pas une ordonnée continue exacte. Le numérateur des zéros hors droite est obtenu
par contour moins changements de signe de Hardy : un zéro double ou une paire
critique très proche peut être manqué par les changements de signe. Même après
raffinement et recoupement, ces comptages ne sont pas des certificats d'intervalles.

Conserver les échecs de prévision. Aucune conclusion de RH, de GRH ni de
positivité globale ne résulte de cette expérience finie.
