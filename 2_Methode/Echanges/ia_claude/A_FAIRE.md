# Boîte de ia:claude

*Générée par `taches.py boites` le 2026-11-23T10:52:02+00:00. Ne pas modifier : la source est le registre des fiches.*

## À produire

- **TAC-001** — Auditer noyaux et couplages du candidat (commencer par la prévision) → `TAC-001_produire.md`
- **TAC-005** — Carte d’identité de μ et corrélations pondérées (commencer par la prévision) → `TAC-005_produire.md`
- **TAC-014** — Échelle, témoin : Davenport–Heilbronn échoue-t-il dès l'étage des entiers ? (commencer par la prévision) → `TAC-014_produire.md`

## À vérifier (dépôts d'un autre acteur)

- **TAC-010** — Lecture adverse de la note sur la preuve annoncée de RH (Alpöge, 2026) → `TAC-010_verifier.md` ; pièces dans `2_Methode/Depot/TAC-010/`

## Fils de discussion

Lire le fil d'une fiche en entier avant de la reprendre, et y répondre à chaque point soulevé.

- TAC-001 : https://github.com/Vppnoel/riemann/issues?q=TAC-001
- TAC-005 : https://github.com/Vppnoel/riemann/issues?q=TAC-005
- TAC-014 : https://github.com/Vppnoel/riemann/issues?q=TAC-014
- TAC-010 : https://github.com/Vppnoel/riemann/issues?q=TAC-010

## Règles (GITHUB.md, § 4)

- Commandes `taches.py` : directement sur `main`, un commit par commande.
- Tout le reste passe par une branche et une pull request : `tac-xxx` pour produire, `tac-xxx-verif` pour vérifier.
- Un changement de méthode (tests, tolérances, contrôles, règles, scripts de vérification, registres, indicateur) est fusionné par l'auteur seul, après son accord écrit dans la pull request.
- Signer sous son propre nom ; si l'outil écrit sous le compte de l'auteur, commencer le message du commit par son identifiant d'acteur. Jamais `--par auteur:…`.
- Une discussion ne décide rien : ce qui est convenu est inscrit par une commande de fiche.

Rendre le travail selon `2_Methode/Pilotage/CIBLAGE.md` (ou `TARGETING_EN.md`). Un acteur sans droit d'écriture rend ses fichiers à l'auteur, qui les dépose.
