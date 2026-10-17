# V6.34 — Validation directe du relief et test indépendant de l'ancrage

Protocole écrit avant les nouveaux comptages. La carte V₇, ses corrélations et les échecs de V6.33 sont connus : sa reprise est une validation de l'instrument, pas une découverte indépendante.

## Validation V₇

Sélection fixée : pour chacune des catégories T*=145, 40≤T*≤60, T*>300 et T*≤10, prendre les deux extrêmes de |a(1)|. Ajouter les trois points d'Euler exacts. Sélection, coefficients et valeurs historiques sont enregistrés avant calcul.

Compter par le principe de l'argument les zéros de la fonction complétée dans le rectangle symétrique [1−σR,σR]×[−T,T]. Choisir σR par la domination du premier coefficient ; comparer aux changements de signe de la fonction de Hardy sur la droite. La différence paire donne le nombre de zéros hors droite dans ce rectangle. Pas initial 0,02 ; reprendre la droite avec pas 0,01 et contrôler les contours adaptativement. Localiser numériquement une première paire pour des points représentatifs, puis recouper des racines par haute précision.

P1 : les trois témoins d'Euler n'ont aucune paire hors droite détectée jusqu'à 300.
P2 : les comptages hors droite sont stables au raffinement et pairs.
P3 : le T* historique est proche (±2 en hauteur) de la première détection directe dans au moins six des huit points non Euler. Une réfutation indiquerait que le relief historique ne mesure pas directement une première sortie.

## Test indépendant V₁₁ impair

Tirer 96 directions réelles uniformes sur la sphère, graine 6341101, indépendamment de la carte V₇. Ajouter les cinq points d'Euler comme témoins. Plafond 150 ; les observations sans sortie sont censurées à ce plafond et identifiées comme telles.

P4 : à distance projective du point d'Euler contrôlée, la corrélation partielle de rang entre la première hauteur directement détectée et |a(1)| est positive et au moins 0,3. Il s'agit d'une nouvelle prévision, plus faible que le 0,81 observé après coup sur V₇.
P5 : le défaut de multiplicativité, après contrôle de distance et |a(1)|, a une corrélation négative. D et |a(1)| sont algébriquement liés ; aucune causalité n'est postulée.

Règles : n'accepter un signe hors droite que si les comptages sont cohérents aux raffinements. Conserver les cas ambigus, les valeurs censurées et les prévisions fausses. Les calculs en double précision, même recoupés, ne sont pas des certificats d'arithmétique d'intervalles.
