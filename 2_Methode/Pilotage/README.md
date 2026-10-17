# Continuité des outils — V6.55 corrigée

Ouvrir `00_PORTAIL.html`. Les quatre pages principales restent **Portail,
Indicateurs, Navigateur, Graphe des idées**. Le même menu donne un accès direct à
**Bellman** et groupe les ressources sous **Documents** : références, figures,
articles et catalogue de tous les fichiers et fiches. Le style de référence de Claude,
les 42 cases d’origine et leurs détails sont conservés ; les informations
courantes sont reliées aux mêmes idées et aux documents effectivement travaillés.

Le protocole de recherche convenu reste l’autorité : preuves, programmes,
analyses constructives et critiques, références, publications LaTeX et PDF.
**Aucun changement de méthode ne peut être adopté sans proposition et accord
préalable de l’auteur.** Cette réparation porte sur la continuité, les liens et
les bilans ; elle ne remplace aucun acquis scientifique.

## Sources communes et évaluation

- `Indicateur/indicateur_avancement.json` conserve toutes les étapes et l’échelle.
  Les sept dimensions ont une justification actuelle ; leurs niveaux restent
  inchangés. La comparaison rejoint V6.55.
- `Navigateur/carte_navigation.json` conserve les 99 actions et leurs prévisions.
  Les bilans sont rapprochés des pièces. Treize dates ou statuts ont été corrigés ;
  les autres bilans ne sont pas présentés comme de nouvelles relectures complètes.
- `pilotage_recherche.json` relie les obligations, les évaluations et les idées.
  `graphe_source.json` conserve les 42 détails d’origine sans réécriture.
- `registre_identifiants.json` conserve les numéros des documents 1–79 et les
  identifiants permanents des69 idées. Les72 cases de cartes détaillées ont des
  renvois vers ces idées, leurs preuves et leurs publications.
- `etat_recherche_courant.json` garde l’état scientifique : RH, loi globale du
  signe et borne globale de force RH restent ouvertes.

Les sept graphiques chronologiques des indicateurs et leurs comparaisons ainsi
que les sept échelles du navigateur conservent leur grammaire initiale. Les trois
cartes 2D des cibles actuelles sont liées aux mêmes identifiants ; leur affichage
reste accessible sur téléphone avec déplacement et zoom.

Le catalogue intégré au portail recense les fichiers de tous formats, les69
fiches et les174 références. Sa recherche porte sur les titres, chemins, types,
numéros DOC, identifiants IDE et clés bibliographiques. Les archives ont leur
filtre. Les fiches relient aussi les formats, figures, données et programmes
repérés par des renvois locaux explicites ; ces associations ne sont pas des
implications mathématiques.

Les quatre pages partagent les données et une empreinte de construction.
`reviewed_source_hashes` recense les pièces stables suivies par empreinte ; cette
liste ne signifie pas que chaque énoncé a été redémontré. Les pages générées sont
contrôlées séparément, pour éviter une dépendance circulaire des empreintes.

## Bellman : conserver les contrats déjà établis

Le moteur reprend le modèle à contrats du document67, avec capacités
complémentaires AND/OR, issues alternatives, STOP et enveloppes. Le modèle
antérieur à union de tokens reste consultable dans le document62 ; il ne
remplace pas le modèle contractuel plus complet.

L’état courant est explicitement rapproché des documents68,70,75 et76 : famille
admissible/couvrante qualitative et dette évaluée, encore ouverte. Deux **études
bornées** sont enregistrées comme examinées. Les deux obligations générales du
registre restent partielle et ouverte. Aucun invariant favorable, transfert
uniforme ou certificat à A fixé n’est ajouté.

Les enveloppes prennent les durées et issues déclarées les moins/plus favorables.
Elles ne sont ni des intervalles statistiques ni une distance à RH. Les unités H
(travail conventionnel) et U (préférence de capacité) sont fictives et explicites.
Les huit questions courantes gardent leurs témoins et critères de rejet, sans
nouveau score non validé ; les grands conducteurs V6.55 ne sont pas encore une
action du modèle67.

## Reconstruction et vérification

La mise à jour des outils accompagne chaque résultat du protocole : conserver sa
prévision, enregistrer sa preuve et sa portée, rapprocher le bilan, réexaminer les
indicateurs, puis les dépendances et les contrats. Les identifiants ne sont pas
recyclés. Une correction d’interface ne crée aucun nouvel acquis sur RH.

```bash
python3 -B 2_Methode/Outils/integrate_v655.py --rebuild
python3 -B 2_Methode/Pilotage/verify_contracts.py
python3 -B 2_Methode/Pilotage/verify_recovered_v650.py
python3 -B 2_Methode/Pilotage/verify_pilotage.py
```

Le premier programme reconstruit les vues et ressources liées. Le deuxième
contrôle le calcul fini du modèle contractuel et ses références conservées. Le vérificateur des sources retrouvées exécute 85 tests fonctionnels originaux et compare les moteurs, avec mpmath 1.3.0 et NumPy disponibles. Le dernier contrôle les liens, la cohérence des vues et les gardes documentaires.
Ils ne rejouent pas toutes les expériences historiques ni les preuves de RH.

## Figures, références et récupération

`Figures/registre_figures.json` fige les numéros existants et attribue les suivants
sans renuméroter. La liste générale relie les figures à leur document ou à leur
article PDF/LaTeX. Le document42 conserve174 fiches et relie les clés des trois
articles aux références globales, sans nouvelle vérification bibliographique.

Les27 scripts/modules du relevéV649 et les trois notes recherchées sont retrouvés.
Le ZIP V6.50 fourni permet176 ajouts originaux, vérifiés par leurs empreintes ;40 versions
anciennes divergentes sont archivées sans remplacer les fichiers courants. Les
sources des cases66 redeviennent leurs liens actifs, avec le PDF également conservé.
Deux références V6.51 restent absentes et sont calculées sur les chemins présents.
Les inventaires sont `RECUPERATION_2026_10_15.json` et
`RECUPERATION_2026_10_15_V651_V652.json` ; les diagnostics antérieurs restent archivés.
Les pièces jointes V6.51/V6.52/77/75 ajoutent deux rapports originaux et100 pièces
archivées, sans écrasement des sources scientifiques courantes. Le ZIP V6.51
fourni est tronqué ; les deux références V6.51 ne figurent dans aucune des
parties vérifiables ni dans le ZIP V6.52 fourni.
