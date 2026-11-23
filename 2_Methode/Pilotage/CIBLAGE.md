# Ciblage et répartition du travail — procédure commune

*Programme Riemann V6.59 · 17 octobre 2026 · Vincent NOËL. Ce texte est la référence de la méthode de travail ; le document 82 en est la version de lecture, avec l'état courant. English: [TARGETING_EN.md](TARGETING_EN.md).*

## 1. But

Travailler par itérations courtes, **indépendamment de l'IA utilisée**, et pouvoir **répartir le travail** entre l'auteur, des IA et des agents.

Trois principes en découlent :

- **Le corpus est la seule mémoire.** Une tâche se reprend à partir des fichiers, sans contexte oral ni historique de conversation.
- **Aucun nom de modèle n'est supposé.** Un acteur s'écrit `type:nom`, avec `type` = `auteur`, `ia` ou `agent` (par exemple `auteur:vincent-noel`, `ia:modele-x`, `agent:calcul-1`).
- **Une seule méthode.** Cette procédure réunit trois sources :
  - le protocole du pilotage (prévision écrite avant, portée, bilan, indicateur réexaminé) ;
  - le ciblage en lecture seule de la branche du 16 octobre ;
  - les rôles et garde-fous du *Protocole multi-agents* du 5 octobre (`2_Methode/Protocole_multi_agents_et_panorama_physique_RH.docx`).

  Là où ces sources différaient, ce texte tranche (§ 8).

## 2. La boucle

| Étape | Qui | Commande | Effet |
|---|---|---|---|
| 1. Cibler | n'importe quel acteur | `python -B 2_Methode/Pilotage/ciblage.py` | Rapport en lecture seule : demandes de calcul, choix Bellman, front des investigations, fiches proposées. |
| 2. Ouvrir | coordinateur | `taches.py ouvrir --par ACTEUR` | Crée les fiches proposées qui n'ont pas déjà une fiche en cours (idempotent). |
| 3. Répartir | coordinateur | `taches.py assigner TAC-001 ia:nom --par ACTEUR` | Une fiche, un acteur producteur. |
| 4. Prévoir | producteur | `taches.py prevoir TAC-001 --par ia:nom --texte "…"` | Prévision horodatée **avant** le travail : ce qui est attendu, ce qui donnerait tort. |
| 5. Produire | producteur | — | Travail dans `2_Methode/Depot/TAC-001/` uniquement ; `RAPPORT.md` obligatoire. |
| 6. Déposer | producteur | `taches.py deposer TAC-001 --par ia:nom --statut-propose STATUT` | Le dépôt est figé par empreintes. |
| 6 bis. Retirer | producteur | `taches.py retirer TAC-001 --par ia:nom --motif "…"` | Seulement avant toute vérification : la fiche repasse « à reprendre » pour compléter le dépôt. Le motif cite le fil de discussion ; le dépôt retiré reste au journal. |
| 7. Vérifier | auditeur, autre que le producteur | `taches.py verifier TAC-001 --par agent:x --verdict conforme --note "…"` | Liste de contrôle dans `TAC-001/verification/VERIFICATION.md`. |
| 8. Décider | auteur | `taches.py decider TAC-001 --par auteur:vincent-noel --decision acceptee` | Acceptée, rejetée ou à reprendre. |
| 9. Intégrer | tout acteur désigné | `taches.py integrer TAC-001 --par … --pieces …` | Le résultat entre au corpus selon le protocole du pilotage ; les pièces sont enregistrées. |
| 10. Recibler | — | `ciblage.py --actualiser-vues` | Les vues et le rapport `data/ciblage_courant.json` sont reconstruits ; la boucle reprend. |

Toutes les commandes s'exécutent depuis la racine du corpus, avec `python -B 2_Methode/Pilotage/…`. La bibliothèque standard de Python suffit.

Pour confier une fiche à une IA ou à un agent, il suffit de lui remettre deux choses : l'archive du corpus et la consigne produite par `taches.py fiche TAC-001`. Pour la vérification, la consigne est `taches.py fiche TAC-001 --verification`. Elle ne nomme pas le producteur (relecture à l'aveugle).

`taches.py etat` donne l'état vivant. `taches.py controler` vérifie la cohérence du registre, du journal et des dépôts.

**Boîtes aux lettres.** `2_Methode/Echanges/<acteur>/` contient, pour chaque IA ou agent, un fichier `A_FAIRE.md` et une consigne par fiche, à produire ou à vérifier. Elles sont régénérées par `taches.py boites`, et automatiquement sur GitHub après chaque changement du registre. Un acteur qui lit le dépôt n'a besoin que de sa boîte.

## 3. La fiche de tâche

| Champ | Contenu | Obligatoire |
|---|---|---|
| `genre` | calcul, investigation, lier_instance, verification_temoin, bibliographie, formalisation, redaction | oui |
| `role` | rôle attendu du producteur (§ 4) | oui |
| `titre`, `question` | ce qui est demandé, en une phrase précise | oui |
| `entrees` | fichiers lus, avec leur empreinte SHA-256 à la création | oui |
| `sortie_attendue` | ce qui doit être rendu | oui |
| `critere_rejet` | ce qui ferait conclure à l'échec, écrit avant | oui |
| `objet`, `domaine` | objet mathématique et domaine de validité | si connus |
| `commande` | commande bornée, quand elle existe | non |
| `temoin`, `budget`, `noeuds` | témoin contraire, durée déclarée, idées du graphe concernées | non |

Le ciblage remplit ces champs depuis les données :
- pour une investigation du pilotage, la question, le témoin, la sortie attendue et le critère de réfutation sont déjà pré-enregistrés ;
- pour une étude Bellman, la fiche demande d'abord de lier une instance exécutable (genre `lier_instance`) ;
- pour une cellule de calcul non conclue, elle demande le bilan détaillé.

Une fiche manuelle se crée avec `taches.py creer --depuis fiche.json`, avec les mêmes champs obligatoires.

**Statuts d'une fiche :** ouverte → assignée → déposée → vérifiée → acceptée → intégrée. Les autres issues sont : à reprendre, rejetée, abandonnée et périmée (une entrée a changé depuis la création de la fiche).

## 4. Rôles

Les rôles viennent du protocole multi-agents. Une même personne ou une même IA peut tenir plusieurs rôles, mais **jamais producteur et vérificateur sur la même fiche**.

| Rôle | Mission | Garde-fou |
|---|---|---|
| Coordinateur | Ouvre et répartit les fiches, applique budgets et règle d'arrêt | N'écrit aucune preuve |
| Explorateur | Suit une reformulation | Sans partager son contexte avec les autres explorateurs avant le dépôt |
| Auditeur | Vérifie en adversaire | Cherche circularités, équivalences à RH déguisées, erreurs de signe, hypothèses cachées |
| Bibliothécaire | Antériorité, références vérifiées sur l'original | Dit « non trouvé » sans conclure à l'absence |
| Numérique | Calculs, tests sur témoins | Tout test doit pouvoir échouer ; aucune donnée injectée |
| Formalisateur | Formalise des énoncés précis et figés | Un énoncé non formalisable reste « esquissé » |
| Rapporteur | Rédige | Aucune formulation au-delà du statut établi |

L'auteur (`auteur:vincent-noel`, déclaré dans `taches.json`) est seul à accepter ou rejeter un résultat.

## 5. Règles

**Appliquées par le programme `taches.py` :**
1. une fiche a, dès sa création, sa sortie attendue et son critère de rejet ;
2. le producteur enregistre sa prévision avant de déposer ;
3. le producteur n'écrit que dans `2_Methode/Depot/<ID>/`. Le dépôt est figé par empreintes : un dépôt modifié après coup n'est pas vérifiable ;
4. si une entrée change, la fiche est périmée et une nouvelle fiche doit être ouverte ;
5. le vérificateur est un autre acteur que le producteur ;
6. seul un acteur déclaré auteur accepte ou rejette ; l'acceptation exige une vérification conforme ;
7. chaque événement est ajouté au journal (`journal_taches.json`), chaîné par empreintes.

**Méthode, à respecter par chaque acteur :**
- **Contrôles anti-circularité :**
  - tester sur Davenport–Heilbronn : un énoncé qui y fonctionne mot pour mot ne peut pas servir pour RH ;
  - confronter à l'analogue des corps de fonctions ;
  - n'injecter aucune donnée qui contient la réponse ;
  - exiger un témoin négatif ;
  - signaler tout énoncé équivalent à RH (option `--equivalent-rh`) ;
  - donner chaque constante avec son erreur.
- **Statut proposé :** il appartient au vocabulaire du corpus (demontre, classique, mesure, ouvert, partiel, conditionnel, obstacle, diagnostic, outil, refute). Le vérificateur juge si la portée annoncée est établie.
- **Explorateurs indépendants :** deux explorateurs sur une même question ne partagent pas leur contexte avant leurs dépôts. Les consignes qu'ils reçoivent peuvent différer.
- **Règle d'arrêt :** après trois cycles d'une même clé sans résultat nouveau, positif ou négatif documenté, le coordinateur propose à l'auteur de fermer la piste. Le numéro de cycle figure sur chaque fiche.
- **Un échec documenté est un résultat :** il se dépose comme les autres.

## 6. Ce que lit le ciblage, et ce qu'il recommande

Le ciblage lit l'état sans rien modifier, et produit des recommandations motivées. Il ne change ni un fait mathématique, ni un niveau d'indicateur, ni un coût de Bellman. Il distingue deux sorties :

- **les demandes de calcul**, qui viennent des cellules de calcul et des études Bellman. Une étude retenue par Bellman n'est pas un programme exécutable : il faut encore lui lier une instance, des entrées et une commande bornée ;
- **le front des investigations.** Ce sont les investigations ouvertes dont les prérequis sont satisfaits. Un prérequis n'est satisfait que par une issue positive déclarée avec sa portée complète : objet, domaine, norme, quantificateurs et source. Une investigation close par réfutation ne le satisfait pas.

Les dépendances lues sont déclarées dans `ciblage_contrats.json`. Leurs empreintes de référence sont celles du **registre unique** du pilotage (`reviewed_source_hashes`). Une dépendance absente, non revue ou modifiée met la pièce « à revérifier ». CSS et menus n'en font pas partie.

| Constat fourni par un calcul | Recommandation |
|---|---|
| Cellule certifiée | La conserver ; ne pas la raffiner pour feindre une extension |
| La garde pourrait devenir positive en réduisant l'incertitude des bords | Augmenter la précision |
| Même les bornes hautes de bord ne paient pas la dette de courbure | Subdiviser ou améliorer la garde |
| Valeur négative strictement encadrée | Faire vérifier indépendamment le témoin |
| Borne suffisante négative, sans témoin négatif | Garder le statut indécis |
| Cellule non résolue sans marges ni budgets détaillés | Obtenir ces informations avant de choisir le raffinement |
| Programme ou donnée mathématique modifiés | Marquer la pièce à revérifier |
| CSS ou menu modifiés seuls | Conserver l'état des résultats mathématiques |
| Coût ou raccord Bellman absents | Afficher « hors modèle » ; ne pas inventer zéro ni une probabilité |
| STOP dans un scénario budgétaire | Conserver les verrous théoriques ouverts |

## 7. Décisions de l'auteur (17 octobre 2026)

1. **Une zone de dépôt.** Une IA ou un agent n'écrit jamais directement dans le corpus. Il dépose dans `2_Methode/Depot/<ID>/`, et l'intégration se fait après la décision de l'auteur.
2. **L'auteur décide.** Le vérificateur rend un verdict ; l'acceptation ou le rejet revient à l'auteur, pour tout ce qui touche aux statuts scientifiques.
3. **Une seule méthode.** Les écarts entre les sources sont tranchés comme au § 8. Toute modification ultérieure de cette procédure suit la règle du corpus : une proposition, puis l'accord préalable de l'auteur.

## 8. Ce qui a été tranché lors de la fusion

| Point | Retenu |
|---|---|
| Textes et chiffres des vues | Calculés depuis les données, jamais écrits en dur |
| Empreintes | Un registre unique (`reviewed_source_hashes`) ; `ciblage_contrats.json` ne déclare que des chemins |
| Prérequis | Issue positive attestée avec sa portée (venue de la branche ciblage) |
| Recommandations | Lecture seule, arithmétique exacte par fractions (branche ciblage) |
| Front des investigations | Toutes les investigations ouvertes du pilotage, non une liste fixe |
| Rôles et garde-fous | Ceux du protocole multi-agents du 5 octobre, appliqués aux fiches |
| Langues | Français et anglais |
| Lien de téléchargement externe de la branche ciblage | Retiré |

## 9. Limites

- Ces règles organisent le travail. Elles **ne vérifient pas une preuve** et ne remplacent pas un contrôle d'accès : un acteur qui se déclare auteur n'est pas authentifié. La garantie vient du journal chaîné et de la relecture de l'auteur.
- Le ciblage automatise l'orientation et sa justification. La production d'une loi arithmétique et la validation d'une preuve restent des travaux de recherche.
- Les vues HTML sont des instantanés : elles ne montrent l'état des fiches qu'à la dernière reconstruction.
