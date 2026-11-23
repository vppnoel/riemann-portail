# Protocole expérimental — rapprocher la preuve Lean de la compréhension humaine

*Programme Riemann — Auteur et titulaire des droits : Vincent NOËL.*

*Version 1. Elle tient lieu de pré-enregistrement à la date de sa fusion sur `main`. Toute
modification ultérieure est un amendement daté et motivé, consigné en bas de ce fichier.
Elle intègre la note de passage de relais du mode fiches
(`relais/PASSAGE_RELAIS_DIALOGUE_LEAN.md`, 23 novembre 2026).*

## 1. Question
Un dialogue autonome entre deux LLM (Claude, ChatGPT) peut-il produire, à partir de la preuve
formalisée en Lean 4 (`leanprover-community/riemann-hypothesis`, commit
`51d9b1a28026d458aef9c9af3df8b083276e3d2d`, figé), une explication à la fois **fidèle** au
code et **compréhensible** par un humain ? La relecture croisée entre modèles apporte-t-elle
un contrôle réel, ou seulement une apparence de contrôle ?

## 2. Hypothèses (pré-enregistrées)
- **H0 — Étalonnage.** Sur les deux unités déjà couvertes en mode fiches, le texte du
  dialogue omet ou fausse moins de 20 % des affirmations du texte de référence
  (items B / (A + B)). Il commet au plus une des huit erreurs connues.
- **H1 — Sensibilité de la critique.** Sur les unités sondées, le critique détecte
  l'erreur injectée dans au moins 70 % des cas.
- **H2 — Valeur du croisement.** Le taux de détection est plus élevé en relecture croisée
  qu'en auto-relecture.
- **H3 — Complaisance.** En auto-relecture, la proportion de « OK » dès la première relecture
  est plus élevée qu'en relecture croisée.
- **H4 — Compréhension humaine (volet 2).** Des lecteurs disposant du chapitre répondent mieux
  aux questions de compréhension que des lecteurs n'ayant que le source Lean, à temps égal.
- **H5 — Calibration (volet 2).** L'écart entre confiance déclarée et exactitude est plus
  faible avec le chapitre.

## 3. Unités (fichier `programme.json`, modifié par l'auteur seul, sur `main`)
| Unité | Phase | Fichiers Lean | Référence |
|---|---|---|---|
| E1-landau | étalonnage | les 34 fichiers cités par TAC-017 (`LandauTheorems/` et deux parents) | TAC-017 `PREUVE.md` : vérifiée conforme, acceptée |
| E2-chaine | étalonnage | les 21 fichiers propres à TAC-023 (`CharacterBoxes/`, `TotientGaloisClasses/`, haut de la chaîne, `Main.lean`) | TAC-023 `NOTE_EN.md` : déposée, **non vérifiée** |
| N1-core-gm | nouveau | `PrimitiveCosets/CoreGm.lean` et ses imports sous `PrimitiveCosets/` (au plus 25) | aucune |

Les textes de référence **ne sont jamais montrés aux IA** pendant la rédaction ni pendant la
critique. Ils n'interviennent qu'après coup, dans la comparaison. N1 couvre le §5 du guide :
tant qu'il est en cours, la fiche TAC-020 ne doit pas être assignée en parallèle, sauf si elle
sert de passerelle.

## 4. Dispositif (volet 1, automatique)
Pour chaque unité :
1. **Rédaction** par l'auteur (alternance Claude / ChatGPT d'une unité à l'autre). Le source
   est fourni avec ses numéros de ligne d'origine ; les imports sont résumés ; un fichier
   trop long est réduit à l'index de ses déclarations plus ses 150 dernières lignes.
   L'auteur ne note pas sa propre explication.
2. **Contrôle des liens** (`relais/verifier_liens_lean.py`) : pour chaque lien, il vérifie le
   commit, l'existence du fichier, et que la ligne contient la déclaration. Un écart, ou
   l'absence de tout lien, vaut **REVISER automatique**, sans passer par le critique.
3. **Sonde (si tirée au sort)** : une IA autre que le critique produit une copie du chapitre
   avec **une** erreur subtile, de l'un des huit types connus. Le critique la relit en
   aveugle, puis une IA juge dit si l'erreur précise a été relevée. Le chapitre réel n'est
   jamais altéré.
4. **Relecture** en aveugle, avec la **liste de contrôle des huit erreurs connues**
   (`CHARTE.md`) : chaque point est rendu « non applicable », « vérifié : … » ou
   « PROBLÈME : … ». Verdict OK ou REVISER, au plus 2 révisions. Un désaccord persistant est
   consigné dans le chapitre.
5. **Questions** : 4 questions de compréhension, rédigées d'après le source Lean par l'IA qui
   n'est pas l'auteur. Les réponses sont scellées.
6. **Comparaison (étalonnage seulement)** : le chapitre figé est comparé au texte de référence
   par **deux juges indépendants** (les deux modèles). Ils produisent les items A (juste et
   présent dans la référence), B (omis ou faussé), C (ajouté, faux ou invérifiable), et
   l'erreur connue commise ou non, pour chacune des huit. L'accord entre les deux juges est
   rapporté.

**Conditions tirées au sort par unité** (graine fixe `EXPERIMENT_SEED`, reproductible) :
relecture **croisée** (70 %) ou **auto-relecture** (30 %, contrôle) ; **sonde** oui (50 %) ou
non. Les unités d'étalonnage sont **toujours en relecture croisée**.

## 5. Mesures (`travail/experience/`, branche `ia-dialogue`)
| Événement | Variables |
|---|---|
| redaction | unité, auteur, révision, condition, longueur |
| liens | unité, révision, nombre de liens, écarts |
| sonde | condition, critique, injecteur, juge, détectée (oui/non) |
| relecture | condition, critique, révision, verdict, « PROBLÈME » de la liste, nombre de remarques |
| etalonnage | unité, fiche de référence, juge (bilans dans `etalonnage/`) |

Critères principaux : items B et C et erreurs connues commises (H0) ; taux de détection
(H1, H2) ; taux de « OK » en 1re relecture (H3) ; écarts de liens au premier jet (descriptif).
Analyse : proportions avec intervalles de Wilson, croisé contre auto par test exact de Fisher.
Aucune autre comparaison n'est confirmatoire. Avec 3 unités, H1 à H3 n'auront de puissance
qu'une fois d'autres unités ajoutées au programme. Elles restent descriptives jusque-là.

## 6. Volet 2 (humain, plus tard)
- Lecteurs : 6 à 12 personnes de culture mathématique, non spécialistes de Lean.
- Plan intra-sujet : chaque lecteur traite des unités en condition **chapitre** et d'autres
  en condition **Lean seul**, contrebalancées (carré latin).
- Pour chaque unité : temps de lecture fixe, puis les questions de `experience/questions/`,
  avec une confiance déclarée (0-100 %) pour chaque réponse.
- Notation contre `experience/scelle/` par un correcteur qui ignore la condition.

## 7. Biais et limites connus
- **Juges non indépendants** : les IA juges ont pu écrire ou relire le chapitre.
  Contrôles : deux juges pour l'étalonnage ; audit humain de 20 % des sondes.
- **Référence E2 non vérifiée** : TAC-023 attend sa vérification, donc l'étalonnage sur E2
  est un contrôle plus faible que sur E1. À relire si TAC-023 est corrigée.
- **Les huit erreurs viennent de ces mêmes textes de référence** (versions antérieures) :
  l'étalonnage mesure aussi si le duo reproduit des erreurs déjà commises par un LLM.
- **Erreurs injectées ≠ erreurs naturelles** : H1 mesure la détection d'erreurs fabriquées.
- **Contrôle des liens ≠ contrôle des énoncés** : un lien juste ne garantit pas un énoncé
  juste. C'est précisément ce que visent les huit points.
- **Gros fichiers réduits** : un énoncé au milieu d'un fichier trop long peut manquer au
  lecteur IA. Ces cas sont signalés dans le source fourni.
- **« Scellé » = convention** : ne pas ouvrir `experience/scelle/` avant la fin du volet 2.

## 8. Ce que le dialogue ne touche pas
`main` ; tout fichier listé comme entrée d'une fiche ; `2_Methode/Depot/TAC-*` ;
`taches.json` et le journal des fiches ; toute publication externe (Zulip, MathOverflow,
dépôt Lean). Le workflow refuse d'enregistrer un changement hors de
`2_Methode/Dialogue_Lean/travail/`.

## 9. Arrêt
Fin du programme, plafond de tours, fichier `2_Methode/Dialogue_Lean/STOP` sur `main`, ou
désactivation du workflow. Un changement de commit Lean arrête le moteur : on ne mélange pas
deux versions dans un même dossier de travail.

## Amendements
*(aucun)*
