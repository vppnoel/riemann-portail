# TAC-002 — Paquets signés : garder premiers, coupures et dette

*Producteur : Codex — ia:chatgpt-sol-6.1-max · 18 octobre 2026 · Programme Riemann V6.59.*

## Prévision

Aucune inégalité locale uniforme ne se sommera sur des paquets arbitraires sans dette explicite de bord et de couplage. Le critère de rejet est atteint si cette dette ne peut être dominée par une norme globale déclarée.

## Méthode

On distingue le bilan local d’un paquet (h_j) du bilan de sa somme (f=sum_jh_j). Pour une forme hermitienne (Q_W),

[
Q_W(f)=sum_jQ_W(h_j)+2Resum_{i<j}Q_W(h_i,h_j).
]

Posons une borne locale (Q_W(h_j)ge b_j), et une dette (d_jgesum_{i
e j}|Q_W(h_i,h_j)|). Alors seulement

[
Q_W(f)gesum_j b_j-sum_jd_j.
]

Cette identité ne transforme pas les couplages en erreur négligeable : elle impose de les payer dans une norme, une structure Toeplitz, ou une estimation signée indépendante.

## Résultat

Il n’existe pas de passage de « bilans locaux positifs » à « bilan positif de la somme » sans une hypothèse supplémentaire sur les couplages. Un modèle algébrique minimal le montre : deux paquets avec diagonale (1,1) et terme croisé (-a) ont un bilan (2-2a) pour les coefficients ((1,1)). Les bilans individuels restent positifs alors que le bilan total devient négatif dès que (a>1).

La condition minimale vérifiable n’est donc pas une inégalité locale seule, mais un contrat de sommation, par exemple :
1. une décomposition précise des paquets et de leurs bords ;
2. une majoration ou une compensation signée des couplages ;
3. une norme (N) dans laquelle (sum d_j) est bornée ou absorbée par (sum b_j);
4. une règle d’échelle garantissant que le coût ne diverge pas quand les paquets couvrent des supports croissants.

Les documents d’entrée identifient déjà la dette de Schur et l’échec des majorations absolues comme le point critique. Le présent examen ne fournit pas de nouvelle loi arithmétique qui remplirait ce contrat.

## Portée

Résultat de structure : toute future proposition de « paquets signés » doit porter une dette quantifiée ; une positivité locale non accompagnée de ce terme est insuffisante. Cela ne conclut rien sur RH ni sur le signe de la forme complète.

Le test Davenport–Heilbronn n’est pas encore applicable, faute d’une inégalité arithmétique candidate non tautologique. Le contre-modèle ci-dessus est le témoin négatif minimal pour la logique de sommation elle-même.

## Critère de rejet

Atteint pour toute approche qui n’utilise que des minorants paquet par paquet : le contre-modèle à deux paquets laisse les bilans locaux inchangés et rend la somme négative. La dette doit être contrôlée ou compensée explicitement.

## Statut proposé

**diagnostic.** Une contrainte nécessaire est formalisée ; aucune inégalité nouvelle sur les vrais paquets premiers n’est obtenue.
