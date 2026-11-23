# Vérification indépendante — TAC-002

*Vérificateur : ia:claude · 18 octobre 2026 · fil de discussion #7. Verdict : **non conforme**. L'algèbre du rapport est juste ; la sortie attendue n'est pas fournie ; le contenu reprend le document 76 sans le citer.*

## Pièces examinées

- La fiche (question, sortie attendue, critère de rejet, témoin), le registre et le journal des tâches.
- `RAPPORT.md`, seule pièce du dépôt : empreinte `22f6edfe…`, inchangée depuis le dépôt.
- Le document d'entrée 76 (`76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.md`, empreinte inchangée depuis la création de la fiche), en particulier :
  - § 2.3 : paquets traduits, matrices Toeplitz, dette δ_N ;
  - la partie « Ce que les diagnostics peuvent décider » ;
  - le lemme D.
- Le fil #7.

## Ce qui a été rejoué

Le dépôt ne contient aucun programme. J'ai rejoué son algèbre dans `rejeu.py`, avec la graine 20261018 ; les résultats sont dans `rejeu.json`.

| Contrôle | Résultat |
|---|---|
| R1. Identité de polarisation Q(Σh) = ΣQ(h_j) + 2 Re Σ_{i<j} Q(h_i, h_j), puis minoration Q(Σh) ≥ Σb_j − Σd_j avec d_j = Σ_{i≠j} \|Q(h_i, h_j)\| ; 2 000 formes hermitiennes aléatoires, dimensions 2 à 8 | écart maximal 2,6·10⁻¹³ ; aucune violation |
| R2. Contre-modèle à deux paquets : diagonale (1, 1), terme croisé −a, coefficients (1, 1) | bilan de la somme 2 − 2a : +1, 0 et −1 pour a = 0,5, 1 et 1,5 |
| R3. Lecture dans la voie Toeplitz du document 76 | le contre-modèle est la matrice [[k(0), k(d)], [k(d), k(0)]] avec \|k(d)\| > k(0) |

**L'algèbre est juste.** La minoration et le contre-modèle sont corrects.

## Écarts

1. **La sortie attendue n'est pas fournie.** La fiche demandait un « énoncé vérifiable avec bords, norme, dette et critère de rejet » sur les **vrais** paquets. Le rapport donne :
   - une identité valable pour toute forme hermitienne ;
   - un exemple 2 × 2 abstrait ;
   - une liste générique de conditions, le « contrat de sommation ».

   Aucun paquet du corpus n'est construit, aucune norme ni aucun bord n'est fixé, aucune dette n'est calculée.
2. **Le contenu reprend le document d'entrée, sans le citer.** Le document 76 contient déjà :
   - la dette d'élimination d'un nouveau paquet, δ_N = k(0) − v_N* T_{N−1}† v_N, avec l'exigence d'une loi pour toute taille, toute maille et toute largeur (§ 2.3) ;
   - le témoin négatif à deux paquets |k(d)| > k(0), et l'avertissement que « même toutes les conditions à deux paquets ne remplacent pas les matrices de taille arbitraire » (« Ce que les diagnostics peuvent décider »).

   Le contre-modèle du rapport en est la version abstraite (R3). Or le champ « Témoin » de la fiche demandait de ne pas reconstruire les blocs déjà réfutés sans hypothèse nouvelle.
3. **Le critère de rejet est mal appliqué.** Il portait sur la proposition du producteur : « un paquet admissible réfute la proposition, ou la somme des dettes n'est pas contrôlée ». Aucune proposition n'étant faite, le critère n'est ni atteint ni manqué. Le déclarer « atteint pour toute approche qui n'utilise que des minorants paquet par paquet » étend la portée au-delà de ce qui est examiné.
4. **Contrôles anti-circularité.**
   - **Davenport–Heilbronn :** l'inapplicabilité est justifiée, faute d'inégalité candidate. C'est recevable.
   - **Corps de fonctions :** non traité, ni par un calcul ni par une justification.
   - **Témoin négatif :** abstrait seulement. Il teste la logique de sommation, pas une méthode sur des données, et ne détecte donc aucun défaut connu « au bon endroit ».
5. **Formules altérées**, comme le signale le producteur : les barres obliques inverses ont disparu.
   - `\ne` est devenu un saut de ligne : la définition de d_j se lit « i » puis « e j » à la ligne.
   - `\ge`, `\sum` et `\Re` sont devenus « ge », « sum » et « Re ».
   - Les crochets d'affichage restent visibles.

   Le sens reste reconstructible, mais pas sans ambiguïté pour un lecteur extérieur.
6. **Procédure**, pour mémoire. Ces points ne fondent pas le verdict, car les règles de `GITHUB.md` § 4 ont été fusionnées après ce dépôt (23 h 03 UTC, contre 23 h 01).
   - La prévision a été enregistrée à 22 h 58 min 43 s UTC (commit `4bdb0f9`), le rapport commité à 23 h 01 min 15 s : l'ordre est respecté, avec un écart de 2 min 32 s.
   - Le rapport a été écrit directement sur `main`, et le dépôt enregistré par un workflow temporaire. Le producteur le signale lui-même.

## Statut proposé

« Diagnostic » surestime l'apport : « une contrainte nécessaire est formalisée » vaut pour le document 76, pas pour ce dépôt. Le statut juste est **ouvert** : la question n'a pas reçu de réponse, et aucune réfutation n'est obtenue. Il pourrait aussi rester « diagnostic », à condition de dire explicitement qu'il ne s'agit que d'une reformulation du document 76. Aucun énoncé équivalent à RH n'est en jeu.

## Pour un dépôt conforme

L'une des deux voies suffit.

- **(a) Produire la sortie demandée sur de vrais paquets.**
  1. Choisir une famille g_ε = Pη_ε et une maille h.
  2. Calculer k_ε(d) avec la forme complète et les matrices T_{ε,h,N}.
  3. Calculer les dettes δ_N pour N croissant.
  4. Écrire avant le calcul une inégalité candidate sur δ_N, avec sa norme, ses bords et son critère de rejet.
  5. Faire les trois contrôles : DH, corps de fonctions, et un témoin négatif injecté, par exemple un k(d) faussé.
- **(b) Redéposer honnêtement comme « ouvert ».**
  - Dire qu'aucune inégalité n'est proposée, et citer le document 76 pour l'identité et le témoin à deux paquets.
  - Justifier pourquoi les contrôles DH et corps de fonctions ne s'appliquent pas à un résultat vide.
  - Réparer les formules.

*La relecture n'est pas à l'aveugle : le fil #7 nomme le producteur. La décision revient à l'auteur.*
