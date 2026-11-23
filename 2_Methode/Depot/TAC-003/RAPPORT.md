# TAC-003 — Dette de Schur dans la norme duale

*Producteur : Codex — ia:chatgpt-sol-6.1-max · 18 octobre 2026 · Programme Riemann V6.59.*

## Prévision

Une norme duale contrôlera un couplage de Schur seulement sur un sous-espace de queue et dans une norme explicitement coercive. Sans contrôle de la restriction au sous-espace, elle ne dominera pas nécessairement le résidu réel.

## Méthode

Soit une décomposition (X=Hoplus Y). Supposons (Q_W(y)gemu R(y)), (mu>0), sur (Y). Pour une famille de tête (h_i), définir la fonctionnelle restreinte
(c_i(y)=Q_W(h_i,y)in Y^*), où le dual est pris pour (sqrt{R}).

Les représentants de Riesz (z_iin Y), définis par (c_i(y)=R(z_i,y)), donnent
(G^*_{ij}=R(z_i,z_j)). La complétion du carré donne

[
Q_Wleft(sum_i a_ih_i+yight)
ge a^*left(H-mu^{-1}G^*ight)a,
qquad H_{ij}=Q_W(h_i,h_j).
]

## Résultat

La borne duale est mathématiquement valide sous les hypothèses ci-dessus et le coefficient (mu^{-1}) est optimal dans le modèle quadratique : pour (Y=mathbb R), (R(y)=y^2), (Q_W(y)=mu y^2) et (c_h(y)=ay), l’infimum vaut exactement (H-a^2/mu).

Le point de rupture est la restriction : une borne sur une source dans le dual ambiant ne détermine pas nécessairement (|c_i|_Y|_{Y^*}). En particulier, une part de la source peut vivre hors de la boîte ou hors du quotient admissible. Remplacer une norme (L^2) par le mot « dual » ne réduit donc pas automatiquement la dette.

Aucune minoration universelle de la forme (H-mu^{-1}G^*succeq0) n’est produite ici : elle demanderait des données quantitatives sur (mu), les représentants restreints et la tête choisie.

## Portée

Le résultat isole un contrat suffisant et sa garde obligatoire :
- coercivité démontrée sur la queue (Y) ;
- fonctionnelles effectivement restreintes à (Y) ;
- calcul ou borne certifiée de (G^*) dans ce dual ;
- positivité du complément de Schur résultant.

Il ne fournit ni signe global, ni couverture des supports, ni conséquence sur RH. Il confirme que la piste est conditionnelle plutôt qu’une solution autonome.

## Critère de rejet

Atteint pour les formulations qui ne certifient pas la restriction au dual de (Y) : elles ne dominent pas le vrai couplage. Le témoin est le résidu ou complément non contrôlé, déjà prévu dans la fiche.

## Statut proposé

**diagnostic.** Le lemme dual est utilisable comme contrat de calcul ; aucune borne arithmétique nouvelle n’est obtenue.
