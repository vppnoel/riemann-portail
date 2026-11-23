# 2_Methode/Dialogue_Lean — dialogue autonome Claude ↔ ChatGPT sur la preuve Lean

*Programme Riemann — Auteur et titulaire des droits : Vincent NOËL.*

Zone du **mode dialogue autonome** (GITHUB.md § 4.5). Rien ici n'entre dans le corpus sans
une fiche créée par l'auteur.

Sur `main` (l'auteur seul y touche) :
- `programme.json` : dépôt Lean, **commit figé**, unités à traiter (étalonnage puis nouvelles)
- `CHARTE.md` : consignes données aux deux IA, dont les huit erreurs connues
- `PROTOCOLE.md` : protocole expérimental pré-enregistré
- `dialogue_ia.py` : le moteur (Python, bibliothèque standard seulement)
- `relais/` : note de passage de relais du mode fiches et contrôle des liens Lean

Sur la branche `ia-dialogue` seulement, dans `travail/` :
- `INDEX.md` : avancement et mesures provisoires
- `modules/` : les chapitres
- `JOURNAL.md` : chaque tour (rédactions, contrôles de liens, critiques, désaccords)
- `experience/` : mesures, questions, bilans d'étalonnage ; `experience/scelle/` à ne pas ouvrir avant la fin

Arrêt : créer `2_Methode/Dialogue_Lean/STOP` sur `main`, ou désactiver le workflow `dialogue-ia`.
