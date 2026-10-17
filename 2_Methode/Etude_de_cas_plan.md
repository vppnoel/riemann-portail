# Étude de cas : comment une recherche assistée par IA se trompe et se corrige (plan, v4.9)

**Question.** Qu'apprend-on d'un projet de recherche sur l'hypothèse de Riemann mené avec un assistant IA, une fois comptées les erreurs, leurs causes et les mécanismes qui les ont attrapées ?
**Public visé** (à choisir) : concepteurs de protocoles de recherche avec agents ; revue ou atelier sur l'IA et la méthodologie scientifique.

## Plan
1. Contexte et périmètre : objet mathématique, durée, intervenants, outils ; pas d'annonce de résultat sur RH.
2. Chronologie : versions v1 à v4.9 (`4_Archives/historique/CHANGELOG.md`, `4_Archives/docs_techniques/ROADMAP_HISTORY.md`).
3. Catalogue des erreurs (`2_Methode/Banc_d_audit/PLANTED_ERRORS.md`) : types (mathématique, test circulaire, numérique, interprétation, rédaction, physique/numérologie), qui les a commises (assistant, utilisateur, sources externes), comment elles ont été détectées.
4. Mécanismes d'attrapage : exécution contre vérité connue, témoins négatifs, relecture externe, vérification de la littérature, lecture des fichiers avant d'affirmer.
5. Corrections qui étaient elles-mêmes fausses (ex. E02, E11) : ce que cela dit de la confiance dans les corrections.
6. Résultats : ce qui a tenu (Théorèmes A et B conditionnés), ce qui a été abandonné (générateur arithmétique, Weil, densité).
7. Recommandations : règles du protocole (`2_Methode/Protocole_multi_agents_et_panorama_physique_RH.docx`, A4 et A9).
8. Limites : un seul projet, un seul assistant, pas de groupe de contrôle ; divulgation de l'assistance par IA.

## Données disponibles dans le corpus
Journal des versions, audits (`4_Archives/docs_techniques/AUDIT_V4_3.md`, `4_Archives/docs_techniques/USER_CORRECTIONS_2026-10-04.md`), simulations de relecture (`4_Archives/referee/`), corpus d'erreurs, tests et sorties numériques.

## À ne pas faire
Surinterpréter un échantillon de 16 erreurs ; présenter les simulations de relecture comme indépendantes ; attribuer à l'IA ou à l'humain les erreurs sans le journal pour le prouver.


## Matériau déjà rédigé
`1_Presentation/06_CHEMINEMENT_INTELLECTUEL.pdf` : frise, intuitions, sources, tests, verdicts, erreurs corrigées et questionnaire d'origine à compléter par l'auteur.
