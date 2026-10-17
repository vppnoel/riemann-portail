# Articles pour relecture (V6.36)

Auteur et titulaire des droits : Vincent NOËL. Préparés le 11 octobre 2026 ; révision du 12 octobre 2026.

## Contenu

| Fichier | Ce que c'est |
|---|---|
| `article1_mean_square_double_poles.pdf` / `.tex` | Article 1, en anglais : Théorème A (méthode standard), Théorème B, corollaire B′, critère conjoint RH et simplicité, lien exact avec Nyman–Beurling, vérifications numériques jusqu'à 10⁸. C'est le candidat sérieux. |
| `article2_prime_side_weil_forms.pdf` / `.tex` | Article 2 : note numérique (forme de Weil côté premiers, témoin Davenport–Heilbronn, modèle des corps de fonctions). Apport modeste, à présenter comme note expérimentale. |
| `lettre_FR.txt`, `letter_EN.txt` | Lettre d'accompagnement, « Cher Professeur » / « Dear Professor », sans nom. |
| `figures/` | Figures (PDF) et les scripts qui les refont depuis les données du corpus. |

Compilation : `pdflatex article1_mean_square_double_poles.tex` (deux passes), de même pour les articles 2 et 3. Les figures doivent être dans le même dossier que le `.tex`.

## À faire avant tout envoi

1. **Adresse électronique** : la ligne `\email{}` est en commentaire dans les deux `.tex`. À compléter si vous le souhaitez.
2. **Divulgation de l'aide par IA** : elle figure dans les remerciements des deux articles. À conserver ; adapter les déclarations au lieu de soumission choisi.
3. **Références à vérifier sur les originaux.** Elles sont citées de mémoire ou d'après une source secondaire :
   - Titchmarsh, Lemme 3.12, Th. 9.2, Th. 9.6(A) ;
   - Montgomery–Vaughan, Th. 13.6 et Cor. 5.3 ;
   - Davenport, ch. 12 et 15 ;
   - Widder ch. V ; Korevaar ch. I ;
   - Cramér (1922), pages 147–153 : article non lu ;
   - Davenport–Heilbronn (1936), pages ;
   - Platt–Trudgian (2021), pages ;
   - Akbary–Ng–Shahabi, revue et pages ;
   - Banks–Sinha : statut de publication inconnu ;
   - Beurling (1955), Nyman (1950), Connes (1999), Bombieri (2000) : volumes et pages.
4. **Nouveauté.** Elle n'est pas établie : la recherche s'est limitée au web, sans MathSciNet ni zbMATH. Les articles le disent.

## Correction trouvée en préparant l'article 2

Le document 52 dit : « DH : directions en trop dès X ≥ 61 (39/39) ». C'est exact, mais ce n'est pas un seuil. Dès X ≈ 56, 8 des 9 réglages montrent déjà 2 directions en trop. Le seuil se situe donc entre X ≈ 20 et X ≈ 56, intervalle qui n'a pas été échantillonné. L'article 2 donne le décompte exact : 0 sur 12 réglages pour X ≤ 20,3 ; 47 sur 48 pour X ≥ 55,7.

## Révision V6.34

Article 1 : correction du signe ≥ dans la remarque sur Cramér ; corollaire conjoint
`Q(X)/(log X)^3 → 4κ/3 ⇔ RH et simplicité de tous les zéros`, obtenu en combinant A et B′.
Article 2 : coefficients arithmétiques généraux pour DH (le coefficient en 6 est non nul),
convention de conjugaison rectifiée, lemme de positivité et conditions de rang après compression.
La concordance des traces à 10⁻⁶ est distinguée d'un certificat de signe à 10⁻¹¹.

Les PDF sont recompilés depuis ces sources. Les lettres sont des brouillons :
aucun destinataire n'est choisi et aucun envoi n'est effectué.

## Questions précises pour une relecture externe

1. Article 1 : vérifier les hypothèses et l'uniformité de la transition de Plancherel au théorème taubérien,
   puis la convergence de la constante S avec multiplicités. Le corollaire conjoint dépend entièrement de A et B′.
2. Article 1 : situer le résultat à pôles doubles par rapport à Cramér et à la littérature sur les moyennes quadratiques ;
   contrôler les références numérotées encore non vérifiées dans les originaux.
3. Article 2 : vérifier le dictionnaire de congruence et la convention complexe de la formule explicite ;
   séparer les résultats exacts du modèle fini et les signatures numériques.
4. Article 2 : les signes proches du seuil demandent une borne en norme sur l'erreur complète
   (traces, queue de zéros, calcul spectral). V6.36 certifie un sous-espace de 25 directions dans ce cas ; la positivité du complément et le compte exact restent à établir.

Le dossier est prêt pour une première relecture mathématique ; la validation externe et
la nouveauté restent à établir. Le document 58 présente les calculs supplémentaires de V6.34.

## V6.36 — Troisième note et corrections

- article3_hasse_jets_and_spectral_bound.tex / .pdf : note expositive autonome, méthode classique de Stepanov, jets de Hasse sur les extensions, rationalité indépendante et modules spectraux ; cinq certificats exacts. Aucun théorème historiquement nouveau ni transfert à ζ revendiqué.
- Article 1 : exposant fini corrigé (0,5174 sans constante ; approximation cubique 0,3445 sous RH et simplicité), normalisation β conditionnelle, non-convergence non démontrée retirée, cas J<2 traité, calibrations limitées aux objets testés.
- Article 2 : tolérance explicite au résumé et tableau, faux jumeaux effectifs seulement dans le domaine testé ; certificat en intervalles établissant au moins 25 directions négatives dans la fenêtre DH a=0,02,h=0,005,L=1115. Le compte exact et les autres fenêtres restent non certifiés.
- Référence Milne : édition de 2021, année antérieure corrigée.

Le document 60 expose le bilan et la reprise du protocole. L’annexe PREUVE_NORME_V636.md décrit les majorants et le modèle d’arrondi ; les données et le témoin sont dans 3_Preuves_et_calculs/data. Le dossier est prêt pour relecture ; aucune acceptation éditoriale ni soumission externe n’est annoncée.
