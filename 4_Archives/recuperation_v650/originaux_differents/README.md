<!-- CURRENT_V650 -->
## V6.50 - Récupération, transport et destination RH

Transport exact et cœur dense ; certificat local complet jusqu’à S=11/20 dans le modèle arithmétique déclaré. Positivité pour tous les supports ouverte.

[Ouvrir la fiche visuelle](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.html), [preuves PDF](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.pdf), [LaTeX](1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.tex).

Le corpus V6.49 est conservé ; les calculs suivant cette version sont nouvellement reconstruits, sans prétendre récupérer leurs sorties originales. Aucun pourcentage de progression vers RH n’est attribué.

Reproduction du nouveau certificat :

~~~bash
python 3_Preuves_et_calculs/scripts/verify_v650_certificate.py
python 3_Preuves_et_calculs/scripts/run_v650_certificate.py
~~~

Le premier vérifie les témoins archivés et les budgets ; le second reconstruit tout le certificat dans un nouveau dossier. Dépendances : `requirements.txt`.
<!-- END_CURRENT_V650 -->

## V6.49 - Compensation multi-premiers (document74)

Coût multi-premiers exact ; paiement joint D/V certifié avec multiplicité. À S=1 : alpha<0,796 contre somme séparée>1,24. Positivité complète inchangée jusqu’à1/2 ; extension à0,55 exploratoire seulement. Transport des supports et sources fortes de Q ouverts.

Ouvrir `1_Presentation/74_COMPENSATION_MULTI_PREMIERS.html`. Le journal intervalle certifie les paiements relatifs ; les diagnostics de norme sont séparés et non certifiés. Les anciennes données scientifiques sont conservées.

## V6.48 - Opérateur commun, tête, sources et queue (document73)

Tous tests complexes, 0<S≤1/2 : Q_W≥masse/250 et R/2000. Norme de l’opérateur commun certifiée, cadre de Gauss80 et deux blocs40. La même erreur certifie tête, sources croisées, queue et Schur du minorant borné. Multi-premiers, sources fortes de Q et couverture non bornée ouverts.

Ouvrir `1_Presentation/73_OPERATEUR_COMMUN.html`. Le calcul intervalle couvre Gauss, ondes et moments ; Bareiss prouve les plafonds matriciels. Les erreurs d’opérateur assemblent la queue et les sources du minorant. Le dictionnaire courant compte40fiches en cinq étapes et16outils avec usages. Le diagnostic ponctuel reste séparé. Les anciennes données et éditions scientifiques sont conservées.

## V6.47 - Concentration projetée et opérateur commun (document72)

Tous tests complexes, 0<S≤3/8 : Q_W≥masse/12 et R/100, premier2 présent. Concentration Schatten2 encadrée sur des sous-niveaux projetés. Opérateur commun démontré ; diagnostic positif à S=1/2 encore non certifié. Sources générales et couverture non bornée ouvertes.

Ouvrir `1_Presentation/72_CONCENTRATION_PROJETEE.html`. L’article démontre huit lemmes et le certificat. Les programmes, le protocole figé et le journal exact sont inclus. Le dictionnaire courant propose36fiches, cinq étapes et13usages. Les éditionsPDF antérieures et les données scientifiques restent conservées. Les diagnostics à1/2 ne sont pas des certificats. Aucun article n’est publié à l’extérieur.

## V6.46 - Lego réutilisable et certificat complet (document71)

Certificat complet sur tout X_S pour 0<S≤347/1000, premier2 présent : Q_W≥masse/25 et R/200. Projection commune aux sources/fréquences, couches par parité et coût de bord assemblés. Supports plus grands, sources des têtes et transport non borné restent ouverts.

Ouvrir `1_Presentation/71_LEGO_REUTILISABLE.html`. Le document71 démontre les raccords K1–K7 et les constantes simples. Le certificat est analytique et numérique, sans preuve formelle automatisée. Il couvre une famille bornée, pas une exhaustion ; les essais 0,348 et 0,5 restent indéterminés. Les sources fortes des têtes générales ne sont pas certifiées par l’exemple algébrique. Les éditions PDF antérieures sont conservées.

## V6.45 - Pont arithmétique et dette de couplage (document 70)

Annulation polaire et identité de fluctuation de Chebyshev démontrées ; modèle continu négatif pour tout S≥16 ; moments finis insuffisants pour réduire la norme première L² ; queue resserrée et dette de Schur bornée par résidus de sources. Sources/tête certifiées et signe pour tous supports restent ouverts.

Ouvrir `1_Presentation/70_PONT_ARITHMETIQUE.html` pour les budgets et le contrat de dette, et `69_LANGUE_DES_PASSAGES.html` pour le dictionnaire courant. Le document 70 contient les preuves C1–C5, les intervalles et les gardes. Les PDF 68–69 conservent leur édition V6.44 ; le lecteur interactif 69 reçoit treize fiches nouvelles. Les 144 entrées premières/résiduelles sont encadrées ; la quadrature archimédienne et le total restent exploratoires. Aucune tête de dimension 10^37 n’a été calculée.

## V6.44 - La langue des passages (documents 68 et 69)

P et métrique exacte, famille dense, no-go de marge H¹, représentation I−compact, queue effective et arithmétique graduée des jets démontrés. 16 compressions arithmétiques positives numériquement ; signe du Schur pour tous supports ouvert.

Ouvrir `1_Presentation/69_LANGUE_DES_PASSAGES.html` pour le dictionnaire et le jeu de contrats ; document 68 pour L1–L8, calculs et obligations. Le corollaire entier certifie une queue très grossière ; aucune tête effective immense n’a été calculée. Tous les 95 noms du registre sont inclus ; les fonctions Python sont indexées séparément.

# Programme Riemann · version 6.46

Un programme de recherche personnel sur l'hypothèse de Riemann, conservé comme un corpus versionné : documents, preuves, code, données et tests. Il étudie une quantité construite avec les nombres premiers dont la croissance reflète la position des zéros de la fonction ζ, et cartographie les mécanismes qui pourraient rendre l'hypothèse nécessaire.

**Aucune preuve de l'hypothèse de Riemann n'est revendiquée.** Les énoncés démontrés n'ont pas encore été relus par un spécialiste.

Auteur : Vincent P. P. NOËL (Strasbourg). Le travail a été mené avec l'aide de ChatGPT (OpenAI) et de Claude (Anthropic). L'auteur assume la responsabilité finale du contenu.

*English summary at the end of this section.*

## En bref

| Ce qui est… | Contenu |
|---|---|
| **Démontré** (relu en interne) | **Théorème A** : l'exposant de croissance de Q(X) = ∫₁^X \|C(x)\|² x⁻² dx, où C est la somme de c = Λ∗Λ − Λ·log + 2γΛ, vaut 2(Θ − ½). **Théorème B** : sous RH, Q(X) ∼ (S/3)(log X)³. **Corollaire B′** : sous RH, la constante vaut 4κ/3 si et seulement si tous les zéros sont simples. **Critère conjoint** : Q(X)/(log X)³ → 4κ/3 ⇔ RH et simplicité, sans supposer RH au départ. |
| **Mesuré** | Signature de la « surface virtuelle » calculée depuis les nombres premiers (ζ : une direction positive ; Davenport–Heilbronn : des directions en trop) ; archipel d'Euler ; rigidité des zéros à basse hauteur ; etc. Chaque calcul a des prévisions écrites avant lui. |
| **Supposé** | Que ces résultats soient nouveaux sous cette forme. Ce qui manque pour aller plus loin est décrit dans les documents. |

## V6.43 - Construire des ponts avec Bellman (document 67)

Des mécanismes sont maintenant reliés par des identités et des domaines explicites : Beurling → translations ; forme complète de Weil → opérateur signé sur H¹ ; cœur dense et famille de compressions ; régularisation avec décalage ; complément de Schur comme élimination dynamique. Les preuves auxiliaires sont données. L’estimation arithmétique pour toute la famille reste ouverte.

- [Dossier PDF](1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.pdf), [LaTeX](1_Presentation/67_CONSTRUIRE_DES_PONTS_AVEC_BELLMAN.tex), [carte et pilote de contrats](1_Presentation/67_GRAPHE_DES_PONTS.html).
- Deux Bellman : élimination dans une forme ; décision sur contrats AND/OR et issues. Modèle documentaire V642 conservé comme référence.
- 270 scénarios contrôlés indépendamment ; durées et valeurs conventionnelles. Aucun scénario ne peut attribuer RH ou le signe global.
- Sources Hamburger/Beurling relues et corrigées ; lecture intégrale de Weil encore ouverte.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v643_bridges.py
node 3_Preuves_et_calculs/scripts/check_v643_client.js
python 2_Methode/Outils/build_v643.py
~~~

## V6.42 - Un pli certifié et sa paire (document 66)

**Un pli choisi est maintenant validé par intervalles.** Deux contractions 50/80 décimales, un contour continu de deux zéros sur 256 arcs, quatre boîtes uniformes : deux racines critiques avant, une paire hors droite après. Les majorants analytiques et les inégalités rationnelles sont fournis ; le backend iv est explicité et n’est pas indépendamment réévalué. La métrique positive du compagnon ne traverse pas le double. Le contrat arithmétique global devient une inégalité signée précise ; son signe reste ouvert.

- [Dossier PDF et preuves](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.pdf), [LaTeX](1_Presentation/66_UN_PLI_CERTIFIE_ET_SA_PAIRE.tex), [graphe courant](1_Presentation/66_GRAPHE_DES_CERTIFICATS.html).
- [Certificats complets](3_Preuves_et_calculs/data/v642_certification.json) et [relecture rationnelle](3_Preuves_et_calculs/data/v642_verification_rationnelle.json).
- [Contrat arithmétique](3_Preuves_et_calculs/preuves/V642_CONTRAT_ARITHMETIQUE.md) et [protocole prospectif](3_Preuves_et_calculs/data/prevision_v642_certification.md).
- Modèle Bellman courant : douze actions, cinq dossiers achevés ; dependency des sources de Weil corrigée éditorialement après résultats. Poids et coûts conventionnels.
- Suite : déployer un candidat sur sa fibre à A fixé ; contrôler la forme arithmétique complète, pas la norme de la seule partie première.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v642_certification.py
python 3_Preuves_et_calculs/scripts/check_v642_certificate.py
node 3_Preuves_et_calculs/scripts/check_v642_bellman.js
~~~

Rejouer sur une copie après déplacement des sorties : le lanceur refuse leur écrasement. Le même backend sert aux recoupements de formule ; ceux-ci ne sont pas des validations indépendantes du backend.

## V6.41 — Graphe des passages (document 65)

**La destination RH est précise ; son mécanisme arithmétique reste ouvert.** Le dossier établit la géométrie des fibres pour A prescrit, le contreexemple D≡1 à A=0, les sections de jets et les théorèmes conditionnels du pli et des moments. Vingt candidats de collisions sont recoupés ; six sont attribués aux branches suivies ; 18 blocs et 24 racines sont reconstruits. Une perte de continuation coarse reste conservée. Les zéros et les contours ne sont pas certifiés par intervalles.

- [Graphe interactif : idées, énoncés, hypothèses et preuves](1_Presentation/65_GRAPHE_DES_PASSAGES.html).
- [Dossier PDF et démonstrations](1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.pdf) ; [LaTeX](1_Presentation/65_FIBRES_PLIS_ET_POSITIVITE.tex).
- [Contrat global G1–G4](3_Preuves_et_calculs/preuves/V641_PASSAGE_AU_GLOBAL.md) : tests admissibles, densité, limites des préfixes finis et contrôle de Schur.
- [Atlas courant de 65 documents](1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html) et modèle documentaire de douze actions, dont trois achevées ; coûts et poids conventionnels.
- Suite : certifier un bloc local, déployer un candidat à A fixé, puis auditer l’inégalité arithmétique uniforme requise pour l’une des deux portes vers RH.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v641_passages.py --phase branches
python 3_Preuves_et_calculs/scripts/run_v641_bellman.py
node 3_Preuves_et_calculs/scripts/check_v641_bellman.js
python 2_Methode/Outils/build_v641_graph.py
python 2_Methode/Outils/build_v641_document.py
~~~

Les modèles, documents et résultats historiques sont conservés. Le nouveau modèle Bellman est une extension éditoriale après résultats, pas une prévision scientifique. Les niveaux de maturité RH restent identiques.

## V6.40 — Comparaison exacte V13 (document 64)

**12 couples inchangés : 8 détections plus précoces, 4 plus tardives à D élevé.** Le signe dépend de l’ancre : χ1 contraire, χ3 et χ5 favorables. Comptages stables aux trois pas, six témoins d’Euler, 24 racines recoupées à 80/110 chiffres de travail. Le rapport 8/12 concerne le plan figé ; ni causalité, ni première ordonnée exacte, ni absence antérieure certifiée.

- [Bilan PDF, tableaux, deux lemmes et suite](1_Presentation/64_COMPARAISON_EXACTE_V13.pdf).
- [Source LaTeX](1_Presentation/64_COMPARAISON_EXACTE_V13.tex) et [données complètes](3_Preuves_et_calculs/data/v640_resultats.json).
- [Protocole prospectif](3_Preuves_et_calculs/data/prevision_v640_comparaison.md).
- [Lemmes et prochaine expérience](3_Preuves_et_calculs/preuves/LEMMES_ET_SUITE_V640.md).
- [Atlas courant des 64 documents](1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html) ; les modèles et PDF historiques sont conservés.
- Suite prioritaire : suivre les branches de racines dans les familles exactes et expliquer l’inversion par ancre.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v640_comparaison.py --run
python 3_Preuves_et_calculs/scripts/run_v640_comparaison.py --roots
python 2_Methode/Outils/build_v640_document.py
~~~

Les lanceurs refusent d’écraser les sorties prospectives. Pour rejouer, déplacer les anciennes sorties sur une copie, en conservant manifeste et protocole ; voir document 64.

## V6.39 - Contraintes exactes V13 (document 63)

**Comparaison faisable démontrée**, pour chaque ancre et tout 0<r<pi/4 à A=cos(r)z_i ; pas pour tout A complexe arbitraire.
- [Décision, témoins et preuve](1_Presentation/63_CONTRAINTES_EXACTES_V13.pdf).
- [Source LaTeX](1_Presentation/63_CONTRAINTES_EXACTES_V13.tex).
- [Preuve complète](3_Preuves_et_calculs/preuves/LEMME_CONTRAINTES_V13_V639.md).
- [Certificat rationnel](3_Preuves_et_calculs/data/v639_certificat_rationnel.json) sans backend transcendant flottant.
- [Témoins et encadrements fins](3_Preuves_et_calculs/data/v639_contraintes.json).
- [Reçu analytique de 12 couples futurs](3_Preuves_et_calculs/data/v639_couples_fixes.json). Aucun nouveau zéro compté ; trois ancres représentatives, écarts construits<0,25.
- Étape suivante : comparaison contrôlée des détections, avec erreurs d’entrée et non-détections explicites.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v639_contraintes.py
python 2_Methode/Outils/build_v639_document.py
~~~

## V6.38 - Reprise du corpus et Bellman (document 62)

- [Atlas interactif des décisions](1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html) :61 documents, sources, résultats, corrections et scénarios de priorité.
- [Atlas PDF](1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.pdf).
- [Registre structuré](3_Preuves_et_calculs/data/v638_decisions.json).
- [Lemmes et portée](3_Preuves_et_calculs/preuves/LEMMES_BELLMAN_V638.md).
- Modèle documentaire fini de 9 actions et 16 tokens, comparé à une énumération indépendante sur972 configurations. Coûts et poids conventionnels ; aucune probabilité de découverte ni distance à RH.
- L’état final recherché est un dossier qui justifie la prochaine décision. Le mécanisme arithmétique imposant une positivité globale pour ζ reste ouvert.
- Les anciennes synthèses et les PDF historiques gardent leur portée d’origine ; l’atlas fournit le bilan courant. Les pages actives sont corrigées sans réécrire les prévisions.

~~~bash
python 3_Preuves_et_calculs/scripts/run_v638_bellman.py
python 2_Methode/Outils/build_v638_atlas.py
~~~

## V6.37 — Ancrage apparié V13 (document 61)

72 couples fixés avant comptage, dans six ancres et trois rayons : le bras A1 donne 36/36 détections plus tardives avec le premier coefficient plus grand, pour de grands contrastes ciblés. Le bras D donne 25 détections plus précoces, 8 plus tardives et 3 mêmes tranches ; cette tendance est hétérogène et ne valide pas une absence de signal D. Tous les comptages sont stables aux trois pas ; 24 racines représentatives sont recoupées à 50 chiffres de travail. Aucune absence de zéro ni première ordonnée exacte n’est certifiée.

- [Document 61](1_Presentation/61_ANCRAGE_APPARIE_V13.pdf)
- [Prévision avant comptage](3_Preuves_et_calculs/data/prevision_v637_apparie.md)
- [Relecture critique](3_Preuves_et_calculs/preuves/RELECTURE_INTERNE_V637.md)

Prochain coup : comparer D en fixant exactement le premier coefficient complexe, l’ancre et le rayon. Les trois articles corrigés de V6.36 sont conservés dans cette version.

## V6.36 — Articles et contrôle en norme (document 60)

Troisième note expositive en LaTeX ; corrections justifiées aux deux articles existants. Le protocole reprend son coup en tête : pour DH, a=0,02,h=0,005,L=1115, un sous-espace de 25 directions est validé négatif par traces en intervalles et Gershgorin, sous le modèle d’arrondi indiqué. Le compte exact et la positivité générale de ζ restent ouverts.

- [Document 60](1_Presentation/60_ARTICLES_ET_CERTIFICAT_DE_NEGATIVITE.pdf)
- [Article 3, PDF](1_Presentation/articles/article3_hasse_jets_and_spectral_bound.pdf) et [LaTeX](1_Presentation/articles/article3_hasse_jets_and_spectral_bound.tex)
- [Preuve du budget en norme](3_Preuves_et_calculs/preuves/PREUVE_NORME_V636.md)

## V6.35 — Tour finie et borne spectrale (document 59)

Les jets de Hasse donnent une borne uniforme sur tous les corps finis impairs. Une rationalité justifiée indépendamment par Riemann–Roch permet de déduire les modules √p et la borne de Hasse en genre un lisse. Cinq certificats exacts, douze comptages directs et dix tests ajoutés. La méthode est classique ; le transfert à ζ reste ouvert.

- [Document 59](1_Presentation/59_DE_LA_TOUR_FINIE_A_LA_BORNE_SPECTRALE.pdf)
- [Preuve complète](3_Preuves_et_calculs/preuves/LEMME_TOUR_ET_SPECTRE_V635.md)

Pour reproduire : depuis 3_Preuves_et_calculs, lancer python src/v635_tour_et_spectre.py.

## Par où entrer

- **`00_PORTAIL.html`** : la page d'entrée (état, dernières étapes, tous les documents).
- **`00_Liste_des_figures.html`** (ou `1_Presentation/LISTE_DES_FIGURES.md` sur GitHub) : toutes les figures.
- **`1_Presentation/44_MATRICE_DES_THEORIES.html`** : la matrice d'équivalence et de force des théories ; survoler un nom affiche sa formule.
- **`1_Presentation/articles/`** : les trois articles au format standard (PDF et LaTeX) :
  - `article1_mean_square_double_poles.pdf` : Théorèmes A, B et corollaire B′ ;
  - `article2_prime_side_weil_forms.pdf` : note numérique et certificat dans une fenêtre DH ;
  - `article3_hasse_jets_and_spectral_bound.pdf` : note expositive, jets de Hasse et borne elliptique.
- **`1_Presentation/01_SYNTHESE_FR.pdf`** : l'essentiel en trois pages.

## Reproduire les calculs

Python 3.11 ou plus récent, avec `numpy`, `scipy`, `pandas`, `matplotlib`, `mpmath` et `sympy` (voir `requirements.txt`).

```bash
pip install -r requirements.txt
cd 3_Preuves_et_calculs
python tests/run_all_tests.py        # 311 tests
```

Pages et documents générés :

```bash
python 2_Methode/Sources/build_sources.py
python 2_Methode/Matrice/build_matrice.py
python 2_Methode/Navigateur/build_navigateur.py
python 2_Methode/Indicateur/build_indicateur.py
python 2_Methode/Figures/build_figures.py
python 2_Methode/Portail/build_portail.py
python 2_Methode/Outils/build_v634_pdfs.py  # six PDF révisés en V6.34
python 2_Methode/Outils/build_v635_pdf.py   # document 59
python 2_Methode/Outils/build_v636_pdfs.py  # trois articles, documents 59 et 60
python 2_Methode/Outils/build_v637_pdf.py   # document 61
```

Les fichiers `.md` portent la marque UTF-8 (BOM), pour que les accents s'affichent correctement quand on les ouvre directement dans un navigateur ou sous Windows ; après avoir écrit un nouveau `.md`, lancer `python 2_Methode/Outils/md_utf8_bom.py`.

Les formules de la matrice sont rendues en MathML à l'avance, par `node 2_Methode/Matrice/render_formules.js`, ce qui demande le paquet npm `katex`. Les pages s'affichent sans réseau.

## Licences

- **Code** (`*.py`, `*.js`, scripts de construction) : licence MIT, voir `LICENSE`.
- **Textes, figures et données** (documents, PDF, images, CSV, JSON) : Creative Commons Attribution 4.0 International (CC BY 4.0), voir `LICENSE-CC-BY-4.0.md`.
- © 2026 Vincent P. P. NOËL. Pour citer ce travail, voir `CITATION.cff`.

## English summary

A personal research programme on the Riemann Hypothesis, kept as a versioned corpus of documents, proofs, code, data and tests (mostly in French). **No proof of RH is claimed.** The main proved statements are written up in English in `1_Presentation/articles/`:

1. the growth exponent of a mean square Q(X) built from c = Λ∗Λ − Λ·log + 2γΛ equals 2(Θ − ½) (standard method);
2. under RH, Q(X) ∼ (S/3)(log X)³, a double-pole analogue of Cramér's theorem;
3. under RH, the constant equals 4κ/3 if and only if all zeros are simple; combining A and B′, the limit Q(X)/(log X)³ → 4κ/3 characterises RH and simplicity jointly.

They have not yet been refereed. Code: MIT. Texts, figures and data: CC BY 4.0.

---

# Mode d'emploi détaillé et journal des versions

## Par où commencer
1. **`00_PORTAIL.html` : la page d'entrée.** Où on en est, les dernières étapes, tous les documents, et une barre de navigation vers les autres pages.
   `00_Carte_des_idees.html` : carte interactive des idées par thème (mise à jour jusqu'à V6.19), avec le statut de chaque élément et ses documents.
   `1_Presentation/31_INDICATEUR_D_AVANCEMENT.html` : les étapes franchies, version par version, sur une échelle de 0 à 9 et six dimensions, avec un lien vers chaque document produit.
   `1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html` : la démonstration comme itinéraire ; position (l'indicateur), opérateurs (les métaphores du registre), coups classés, prochain coup proposé.
2. `1_Presentation/01_SYNTHESE_FR.pdf` : 3 pages, l'essentiel.
3. `1_Presentation/06_CHEMINEMENT_INTELLECTUEL.pdf` : d'où viennent les intuitions, ce qui les a testées, ce qui est resté.
4. `1_Presentation/07_GUIDE_DE_LECTURE_INTUITIF.pdf` : vulgarisation scientifique des résultats, de leur intérêt et des analogies spectrales, avec leurs limites mathématiques explicites.
5. `1_Presentation/08_Dimension_energie_fractale.md` : nouvelle branche active reliant exactement énergie, dimension et zéros.
6. `1_Presentation/09_Attaques_audit_et_amelioration` : audit de deux attaques reçues (énergie transverse ; projection de Nyman–Beurling) et version améliorée, avec témoins chiffrés.
7. `1_Presentation/10_Attaque2_resultats_N1000` : résultats de l'attaque 2 jusqu'à N = 998 (plateau ≈ 1,3 κ/log N ; optimum sans carré ≈ κ/log N), figure et lecture.
8. `1_Presentation/11_Estimation_sous_RH` : test de l'estimation standard sous RH contre la Gram exacte ; elle ne décrit pas N ≤ 1000, et les données désignent ce qui gouverne le plateau.
9. `1_Presentation/12_Annulation_du_pole` : la projection de Nyman–Beurling se ramène exactement à l'énergie Q (vérifié, étendu jusqu'à N = 10⁷) ; branche close.
10. `1_Presentation/13_Lecon_2026` : le résultat de 2026 (≥ 2/3 des zéros simples et sur la droite) tient à la positivité de la forme de Weil, que Q ne contient pas ; clôture du volet « assaut frontal ».
11. `1_Presentation/14_Document_de_travail_V6_Atlas_mecanismes.md` : bascule méthodologique V6 vers un atlas fonctionnel des mécanismes, avec divergence contrôlée et crash-tests.
12. `1_Presentation/15_TOMO_DH_formalisation.md` : formalisation TOMO-2/TOMO-3, défaut multiplicatif et protocole ζ / L / Davenport–Heilbronn / phases randomisées.
13. `1_Presentation/16_DARK_ZETA_secteur_sombre_arithmetique.md` : cadre transversal d'observabilité — cartographier l'information perdue par plusieurs empreintes indépendantes ; TOMO-DH en est le premier détecteur.
14. `1_Presentation/17_DARK_ZETA_premier_detecteur_resultats.md` : premier détecteur exécuté ; TOMO-3 brut est rétrogradé, TOMO-2 survit comme diagnostic conditionnel.
15. `1_Presentation/18_PRIME_LOCK_premier_verrou_local.md` : changement de canal ; dérivée logarithmique décomposée en premiers / puissances de premiers / fuite, eulérisation contrôlée et crash-tests.
16. `1_Presentation/19_DUAL_LOCK_plan_local_global.md` : plan local/global désormais exécuté et annoté.
17. `1_Presentation/20_Registre_metaphores_V6.md` : registre canonique des métaphores, objets exacts, correspondances interdites et statuts.
18. `1_Presentation/21_DUAL_LOCK_RESIDU_SOMBRE_resultats.md` : résultats DUAL-LOCK, décomposition local/global, test du Résidu sombre et sweep de stabilité.
19. `1_Presentation/23_AUDIT_V6_3B_FORMULE_EXPLICITE.md` : conventions de la formule explicite validées (côté premiers = côté zéros à 5·10⁻⁹ pour ζ, ≤ 1,4·10⁻⁶ pour DH) ; chaque direction négative de DH attribuée à un seul quadruplet de zéros hors droite.
20. `1_Presentation/20_Registre_metaphores_V6.md` (+ `20_Carte_du_lexique.png`) : registre unique des métaphores ; l'annexe B reprend le lexique de la v6.0.
21. `1_Presentation/24_CLASSEMENT_DES_INSTRUMENTS_V6_3D.md` (+ `24_Differences_de_zeros.png`) : ce que chaque instrument V6 voit réellement ; les quatre coins (verrou local et signe global indépendants) ; correction du comptage des zéros de DH.
22. `1_Presentation/25_Atlas_metaphores_physique_mathematique_V6.pdf` : atlas des métaphores (pendant physique, pendant mathématique, test) et plan d'expériences ; reçu sous le numéro 24, renuméroté 25.
23. `1_Presentation/26_SEUIL_TAU_C_TEST_DE_L_ATLAS` (md + pdf) : exécution du test prioritaire de l'Atlas ; le seuil τ_c existe, mais n'est pas un invariant.
24. `1_Presentation/27_FAMILLE_MODULO_7_POINT_D_EULER` (md + pdf) : une famille où les zéros bougent vraiment, à équation fonctionnelle constante ; RH n'y tient qu'autour du point où le produit d'Euler existe.
25. `1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE` (md + pdf) : le Modèle réduit — courbes sur les corps finis, où RH est un théorème ; la signature d'une nécessité démontrée, et ce que ζ en présente.
26. `1_Presentation/29_STABILITY_RADIUS_MARGE_DE_LA_FORME_ET_DE_L_OBJET` (md + pdf) : la marge de la forme (exactement nulle au-delà du nombre de zéros) et la marge de l'objet (positive, fixée par la paire la plus serrée) ; correctif au document 26.
27. `1_Presentation/30_ARCHIPEL_D_EULER` (md + pdf) : parmi les fonctions qui ont l'équation fonctionnelle, RH n'existe qu'aux points d'Euler ; les îles autour de chacun rétrécissent avec la hauteur.
28. `1_Presentation/31_INDICATEUR_D_AVANCEMENT.html` : indicateur d'avancement (échelle de maturité 0–9, six dimensions, parcours de v1 à V6.11, liens vers les documents).
29. `1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU` (md + pdf) : le chaînon F = q^D entre le discret et le continu ; l'opérateur se reconstruit depuis les nombres, imposteurs compris ; ce qui manque pour ζ est la métrique.
30. `1_Presentation/33_LE_GENERATEUR_DES_PREMIERS` (md + pdf) : l'opérateur de ζ reconstruit dans une fenêtre finie avec les seuls nombres premiers ; sa métrique est positive pour ζ et L, négative pour DH exactement à ses zéros hors droite.
31. `1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html` : navigateur de recherche (prototype) ; données et générateur dans `2_Methode/Navigateur/`.
32. `1_Presentation/35_LA_BASE_COMME_PAS_DE_TEMPS` (md + pdf) : la base d'un corps fini est un pas de temps du flot ; pour ζ, le seul pas qui convienne est le flot.
33. `1_Presentation/36_LES_IDEES_REJETEES_RELUES` (md + pdf) : les trois idées rejetées en V4.3 (Kalman, sources, Schrödinger) relues avec les opérateurs du chaînon ; priorités refaites.
34. `1_Presentation/37_PRE_RELECTURE_A_B_ARCHIPEL` (md + pdf) : pré-relecture interne des Théorèmes A et B et de la note sur l'Archipel ; verdicts, corrections faites, nouveauté située, corollaire B′, projet de message.
35. `1_Presentation/38_LA_LOI_DE_SEUIL_LE_TEMPS_DE_HEISENBERG` (md + pdf) : un quadruplet hors droite s'entend au temps de Heisenberg de sa hauteur, log(q·γ₀/2π), avec les premiers jusqu'au conducteur analytique ; correction des seuils de la V6.12.
36. `1_Presentation/39_LE_DEGRE_2_ET_LE_RECENSEMENT` (md + pdf) : L(Δ, s) de Ramanujan depuis les premiers, la loi de seuil y double ; la métrique des premiers recense 25 quadruplets hors droite de DH, tous identifiés.
37. `1_Presentation/40_LA_RENCONTRE_A_TROIS` (md + pdf) : RH, simplicité et répulsion se lisent sur la même quantité, la marge locale de la métrique (corrélation de Montgomery) ; les croisements entrent dans l'indicateur.
38. Pour un spécialiste : **le dossier `1_Presentation/relecture/`** (ouvrir `00_READ_ME_FIRST_EN.md`), qui remplace `03_Dossier_de_relecture_EN` et `05_Message_au_relecteur` ; en complément, `02_Article_court_EN` et `04_Brief_specialistes_EN`.

## Organisation
| Dossier | Contenu |
|---|---|
| `1_Presentation/` | documents à lire ou à envoyer |
| `2_Methode/` | protocole multi-agents, plan d'impact, banc d'audit (21 erreurs plantées) |
| `3_Preuves_et_calculs/` | preuves, code, données, 311 tests, lancés par `python tests/run_all_tests.py` (voir son README) |
| `4_Archives/` | historique : rapport d'origine, simulations de relecture, journaux, anciennes branches |

## Où ranger un nouvel élément
Document à lire ou envoyer → `1_Presentation` · méthode, protocole, audit → `2_Methode` · énoncé, preuve ou calcul reproductible → `3_Preuves_et_calculs` · tout ce qui est périmé → `4_Archives`.

**À chaque version** : ajouter l'étape dans `2_Methode/Indicateur/indicateur_avancement.json` (niveaux, raisons, documents), puis lancer `python 2_Methode/Indicateur/build_indicateur.py`. Le test `test_v681_indicateur.py` vérifie que les documents cités existent et que la page est à jour.

## Limites
Calculs numériques = tests de cohérence, pas de RH. Plusieurs sources ont été lues sur résumés ou pages web. Le travail a été mené avec l'aide de ChatGPT (OpenAI) et Claude (Anthropic) ; l'auteur assume la responsabilité finale du contenu.


## Bascule V6
La V6 n'est plus organisée comme une succession d'« attaques RH ». Elle cartographie des mécanismes qui ont résisté aux audits, les nomme, les croise et leur impose des observables, des témoins adversariaux et des règles d'arrêt. Première campagne active : DARK-ZETA. Après TOMO-2/TOMO-3, PRIME-LOCK change le canal d'observation et isole la structure eulérienne locale. DUAL-LOCK est maintenant exécuté : la compression local/global produit des témoins d'inertie sur Davenport–Heilbronn. La V6.3 ajoute le mécanisme **Résidu sombre** : le signe final peut être porté par un petit reliquat après cancellation de gros termes archimédiens et locaux. La prochaine cible n'est plus une nouvelle métaphore, mais la robustesse de ce résidu sous déformations contrôlées.

## V6.3a — audit de l'instrument

La V6.3a corrige le traitement spectral de DUAL-LOCK : la base n'étant pas orthonormale, les confirmations utilisent désormais le problème généralisé `M v = lambda G v`. Voir `1_Presentation/22_AUDIT_V6_3A_INSTRUMENT_DUAL_LOCK.md`. Un faux second mode négatif à T=176 a été retiré ; le signe négatif principal DH survit aux contrôles ciblés. Les anciens facteurs de « Résidu sombre » ont été recalculés dans la métrique de Gram.


## V6.3b — audit des conventions de la formule explicite

La priorité fixée en V6.3a est traitée : la compression DUAL-LOCK côté premiers coïncide avec la somme directe sur les zéros (ζ : 5·10⁻⁹ ; DH : ≤ 1,4·10⁻⁶). Chaque valeur propre généralisée négative de DH (T = 86, 113, 167, 176) est expliquée par un seul quadruplet de zéros hors de la droite ; les zéros sur la droite apportent une masse positive. DUAL-LOCK est donc validé et entièrement expliqué : c'est le critère de Weil comprimé. Les 4 zéros DH « manquants » depuis v3.3 étaient les partenaires 1 − σ des zéros hors droite (129 zéros jusqu'à t = 200, ≈ 129,5 attendus ; **corrigé en V6.3d : 130, deux zéros bas manquaient encore**). Voir `1_Presentation/23_AUDIT_V6_3B_FORMULE_EXPLICITE.md`.


## V6.3c — choses simples

- Contrôle L(s, χ₅) audité contre ses propres zéros (334 zéros, |t| ≤ 245, tous sur la droite) : côté premiers = côté zéros à 1–9·10⁻⁸ ; l'audit a aussi détecté un zéro manquant (t = −119,999), corrigé.
- Référence du « travail numérique 2026 » du doc 21 identifiée : Kim et al., arXiv:2607.24830 (opérateur de Suzuki, arXiv:2606.09096) ; positionnement ajouté (Connes–Consani–Moscovici, Connes–van Suijlekom).
- Doc 22 : « certifié » remplacé par « vérifié par recoupement ».
- Registre unique des métaphores (annexe B du doc 20) ; lanceur de tests sans pytest ; 68 tests.


## V6.3d — ce que chaque instrument voit réellement

- **Les quatre coins.** Deux témoins F(s) = P(s)·ζ(s) : F6 (pas de produit d'Euler, zéros sur la droite, forme de Weil positive) et E2 (produit d'Euler, zéros hors droite, forme négative). Côté premiers = côté zéros à 2–4·10⁻⁹. Le verrou local mesuré par PRIME-LOCK et le signe global mesuré par DUAL-LOCK sont indépendants ; il manque une borne de taille locale, et avec elle la question redevient GRH.
- **TOMO-2 expliqué.** Le signal de TOMO est reconstruit à partir des zéros seuls (écart ≤ 1,1·10⁻⁸ pour ζ, L(s, χ₅), DH). L'excès d'entropie de DH sur L est porté par ses zéros hors droite.
- **TOMO-3 clos.** Dans le canal de C_F, un bispectre teste les relations additives entre zéros ; dans le canal t, la fermeture ternaire est le défaut multiplicatif (tautologie).
- **Empreinte en creux.** Les différences entre zéros évitent les zéros de ζ : déficit de 30 % (ζ), 17 % (L(s, χ₅)), 5 % (DH, zéros de la droite). Phénomène connu (Pérez-Marco ; Ford–Zaharescu) ; la comparaison avec DH distingue le produit d'Euler sans utiliser les zéros hors droite.
- **Erreur corrigée.** Deux zéros bas de DH (t = 5,0942 ; 8,9399) manquaient depuis la v3.3 ; le comptage « 129 » de la V6.3b était faux (130 par le principe de l'argument). Nouvelles listes jusqu'à |t| = 600, complétude contrôlée ; entrée E12 du banc d'audit réécrite.
- **V6.3e — idée hors cadre testée (doc 24, §7.4).** La demi-largeur du creux vaudrait 1 − β (distance du zéro à la droite Re s = 1). Avec le profil sommé sur les zéros voisins : 0,53 ± 0,02 pour L(s, χ₅) (accord, amplitude comprise), mais 0,68 à 0,71 pour ζ (désaccord ; seulement 300 zéros, à basse hauteur). Test non concluant ; de toute façon une reformulation de RH, probablement circulaire.
- **V6.3f — le cas de ζ est tranché.** Zéros de ζ calculés jusqu'à t = 1500 (1 070 zéros, complétude contrôlée). Par tranches de hauteur, la demi-largeur du creux descend de 0,73 à 0,51 ± 0,04 pour ζ, et l'amplitude rejoint la valeur attendue : le désaccord de la V6.3e tenait aux basses hauteurs. Le test passe pour ζ et L(s, χ₅) ; cela reste une reformulation de RH, mesurée sur des zéros déjà connus sur la droite.
- Tests : 77 exécutés et réussis sur 84 dans la session de production. Sept tests de `test_identities.py` exigent mpmath, non installable dans cette session, et n'ont pas été relancés (code non modifié) ; quarante autres du même fichier ont tourné avec un module de remplacement.

Voir `1_Presentation/24_CLASSEMENT_DES_INSTRUMENTS_V6_3D.md`.


## V6.4 — le test prioritaire de l'Atlas des métaphores

L'Atlas (document 25) demandait de mesurer le seuil τ_c où la forme M_T(τ) = (1 − τ)·M^L + τ·M^DH cesse d'être positive.

- Le seuil existe et il est unique (λ_min est concave en τ). Trois calculs le donnent : zéros et Gauss–Legendre à six chiffres, quadrature adaptative à 4·10⁻⁴ près.
- Ce n'est pas un invariant : 0,66 à 0,96 selon la fenêtre, baisse avec la dimension, et tend vers 0 quand le support s'élargit (0,87 à W = 2 ; 0,0002 à W = 10). C'est le critère de Weil : le seuil mesure le pouvoir de résolution de la fenêtre.
- Ce n'est pas une transition de phase : aucun zéro ne bouge, τ repondère deux listes de zéros fixes.
- La carte à deux clés (τ, δ) est la courbe 1D décalée, exactement.
- Le seuil suit les zéros hors droite, pas le produit d'Euler (ζ → E2 : seuil ; ζ → F6 : aucun).
- Tests (V6.4) : 83 exécutés et réussis sur 90 ; 7 exigeaient mpmath, alors non installable. Voir V6.4.1.

Voir `1_Presentation/26_SEUIL_TAU_C_TEST_DE_L_ATLAS.md`.


## V6.4.1 — mpmath rétabli, tout recoupé

- mpmath 1.3.0 installé depuis un fichier fourni par l'auteur (le dépôt de paquets n'était pas accessible depuis la session).
- Les 7 tests en attente depuis la V6.3d passent. **93 tests sur 93 exécutés et réussis.** Réserve : sympy reste absent de la session ; pour `test_identities.py`, sa seule fonction utilisée (`factorint`) a été remplacée par une factorisation par divisions successives, exacte.
- Nouveau fichier `tests/test_v64_mpmath_crosscheck.py` (3 tests) : mpmath, à 30 chiffres, confirme l'évaluateur maison (10⁻⁹), la liste des 1 070 zéros de ζ (comptage et valeurs), et les listes de zéros de L(s, χ₅) et de DH, dont les 30 zéros hors droite et les deux zéros bas ajoutés en V6.3d.
- Aucun résultat des versions V6.3d à V6.4 n'est modifié.


## V6.5 — là où les zéros bougent : le point d'Euler

Hypothèse de travail de l'auteur : RH n'existe que parce qu'elle est nécessaire à quelque chose de plus grand. Test : la famille F_θ = (1 − θ)·L(s, χ₃ mod 7) + θ·f₇, qui garde la même équation fonctionnelle pour tout θ et n'a de produit d'Euler qu'en θ = 0.

- Les 958 zéros de L(s, χ₃) jusqu'à t = 1000 ne restent tous sur la droite que pour θ entre −0,0096 et +0,072 ; la plage se referme avec la hauteur.
- Chaque sortie de la droite est une rencontre de deux zéros voisins (écart à la droite en racine de θ − θ_c) ; le seuil d'une paire suit son écart (corrélation de rang 0,71). 89 des 100 seuils les plus bas sont du côté θ < 0.
- L'empreinte de ζ dans les écarts entre zéros est maximale en θ = 0 (12,4 %), tombe à 2 % en θ = 0,5.
- Lecture : la symétrie globale ne rend pas RH nécessaire ; au point d'Euler culminent ensemble la position des zéros et leur arrangement collectif, qui porte la trace de ζ.
- Tests (V6.5) : 101 sur 101 exécutés et réussis. Voir V6.5.1.

Voir `1_Presentation/27_FAMILLE_MODULO_7_POINT_D_EULER.md`.


## V6.5.1 — ce qui est démontré ; sympy rétabli

- Document 27, §8 : ce qui rend une RH nécessaire dans les cas démontrés. Toujours une positivité sur un objet plus grand que la fonction (produit avec elle-même, surface, espace de Hilbert). Pour ζ, ce mécanisme est démontré jusqu'à la droite Re s = 1.
- Vérification dans la famille modulo 7 : aucun zéro à droite de Re s = 1 au point d'Euler ; le sosie f₇ en a 5 (jusqu'à σ = 1,061), et il y en a 71 en θ = −0,5. La partie démontrée de RH disparaît aussi avec le produit d'Euler.
- sympy 1.14.0 installé depuis un fichier fourni par l'auteur : la suite complète tourne sans aucun remplacement. **103 tests sur 103 exécutés et réussis.**


## V6.6 — le Modèle réduit : la signature d'une nécessité démontrée

Question : là où RH est un théorème (courbes sur les corps finis, Weil 1948), à quoi ressemble ce qui la rend nécessaire ? On le mesure, pour savoir quoi chercher du côté de ζ.

- 425 courbes hyperelliptiques (genre 1 à 8 sur F₃, F₅, F₇) : fonction zêta reconstruite depuis les comptages de points, comptage suivant vérifié à l'unité (425 sur 425) ; positivité de Castelnuovo exacte à tous les étages jusqu'à 60.
- **Le Faux jumeau entier** : 220 polynômes avec l'équation fonctionnelle et un produit d'Euler à comptages entiers positifs, mais RH fausse. Aucun n'est une courbe ; la positivité de Castelnuovo les démasque à un étage fini (2 à 5 en genre 2). Le produit d'Euler positif seul ne leur donne que « aucun zéro sur Re s = 1 », le niveau de de la Vallée Poussin.
- **La Positivité saturée** : la marge 1 − max ρ_n s'annule en montant dans **la Tour** des corps à qⁿ éléments ; elle est exactement nulle pour la courbe y² = x⁵ + x³ + 1 sur F₃ à l'étage 4 (118 points sur F₈₁).
- Plage de survie positive pour chaque courbe, de plus en plus mince quand le genre croît.
- Lecture : ζ présente les signatures observables d'une nécessité démontrée (traits 1 à 3), sauf l'objet qui la porte (l'analogue de la surface C × C). Question ouverte : quel est l'« étage n » de ζ ?
- Tests : 7 ajoutés ; **110 sur 110 exécutés et réussis.**

Voir `1_Presentation/28_MODELE_REDUIT_NECESSITE_DEMONTREE.md`.


## V6.7 — STABILITY-RADIUS : la marge de la forme et la marge de l'objet

Programme proposé dans une réponse reçue par l'auteur : « quelle est la marge de stabilité de la positivité de Weil face à une déformation du côté local ? ». Testé d'abord dans le Modèle réduit, puis pour ζ, L(s, χ₅), DH, F6, E2.

- **Deux marges.** Marge de la forme : plus petite valeur propre de la forme de Weil (toute perturbation permise). Marge de l'objet : plus petite perturbation des données locales, équation fonctionnelle conservée, qui fait perdre la positivité.
- **Modèle réduit (525 courbes, genre 1 à 12).** La marge de la forme est exactement nulle dès que la fenêtre dépasse le nombre de zéros (2g). À la fenêtre 2g, le nombre de directions négatives compte exactement les zéros hors droite (900 sur 900 en 60 chiffres, 220 faux jumeaux sur 220). La marge de l'objet est en général positive, fixée par la paire de zéros la plus serrée, et décroît avec le genre ; elle est exactement nulle pour les courbes à zéros confondus, où RH reste un théorème. Le produit d'Euler ne bloque la sortie la plus proche que pour 24 courbes sur 525.
- **ζ, L, DH, F6, E2.** Même loi de rang : λ_min chute géométriquement quand la dimension dépasse les zéros atteints, sans distinction entre ζ et F6 (sans produit d'Euler) ; les vrais s'arrêtent à zéro, DH et E2 passent dessous.
- **De L(s, χ₅) à DH.** En interpolant les fonctions (symétrie de Hardy conservée), exactement quatre paires quittent la droite, à θ = 0,280 ; 0,602 ; 0,646 ; 0,937 : ce sont les quatre paires hors droite de DH. Le seuil de la forme, lui, dépend de la fenêtre. **Correctif au document 26** : sa décroissance vers 0 n'était vraie qu'à la hauteur 85,7.
- Matrice de Gram en forme close (la quadrature se dégradait aux grandes hauteurs ; aucun résultat antérieur concerné).
- Lecture : là où RH est démontrée, les deux marges peuvent être nulles sans qu'aucune courbe sorte. La nécessité n'éloigne pas du bord, elle interdit le passage.
- Tests : 8 ajoutés ; **118 sur 118 exécutés et réussis.**

Voir `1_Presentation/29_STABILITY_RADIUS_MARGE_DE_LA_FORME_ET_DE_L_OBJET.md`.


## V6.8 — L'Archipel d'Euler

Question (document 29) : parmi les fonctions qui ont l'équation fonctionnelle, une sortie de RH peut-elle garder un produit d'Euler ?

- **Espaces V_q** (q premier ≤ 13, parité fixée) : combinaisons réelles des L(s, χ) normalisées, toutes à la même équation fonctionnelle. Points d'Euler : une seule L(s, χ). ζ, L(s, (·/3)) et L(s, (·/5)) sont seules dans leur espace (Hamburger pour ζ).
- **Démontré.** Rigidité au premier ordre (prouvée ici) : aucune direction qui garde l'équation fonctionnelle ne garde le produit d'Euler. Avec Saias–Weingartner (2009) : dans V_q, toute fonction qui vérifie RH, et même toute fonction sans zéro dans Re s > 1, est un point d'Euler. RH implique le produit d'Euler, sans hypothèse.
- **Mesuré.** Autour de chacun des 27 points d'Euler, une île de rayon r(T) (forme close, contrôlée de part et d'autre et dans 100 directions au hasard) : médiane 0,091 à |t| ≤ 25, 0,008 à |t| ≤ 300 ; pente −0,77 en fonction du nombre de zéros. On en sort par la paire la plus serrée (112 sorties sur 116 dans les 5 % d'écarts les plus petits).
- **Carte de V₇ impair** : un continent sans paire hors droite à |t| ≤ 50 (32 % de la carte), trois îles séparées à |t| ≤ 300 (1 %).
- **Partie démontrée** : hors des points d'Euler, des dizaines de zéros dans Re s > 1 dès |t| ≤ 300 ; aucun aux points d'Euler.
- Lecture : la hauteur T joue le rôle de l'étage de la tour du Modèle réduit ; dans ces espaces, RH n'existe que là où un objet (un caractère) se tient derrière la fonction.
- Tests : 6 ajoutés ; **124 sur 124 exécutés et réussis.**

Voir `1_Presentation/30_ARCHIPEL_D_EULER.md`.


## V6.8.1 — l'indicateur d'avancement

- `1_Presentation/31_INDICATEUR_D_AVANCEMENT.html` : échelle de maturité de 0 à 9 (inspirée des niveaux de maturité technologique), six dimensions (voir, comprendre, situer, étendre au degré 2, démontrer et faire relire, la case vide), 14 étapes de v1 (3 octobre) à V6.8 (9 octobre), avec pour chacune ce qui a été franchi, les niveaux qui changent et les liens vers les documents produits ; tableau des degrés ; prochaines marches.
- Données et générateur : `2_Methode/Indicateur/indicateur_avancement.json`, `2_Methode/Indicateur/build_indicateur.py`.
- Lecture : « voir » est à 4 depuis v3.2 et « démontrer » à 6 depuis v2 ; « comprendre » (3 → 5), « situer » (3 → 6) et « la case vide » (2 → 3) ont bougé depuis le 7 octobre ; le niveau 7 (relecture) n'a jamais été atteint.
- Correction : le premier instantané publié (9 octobre au soir) partait de « comprendre » 1, « situer » 2 et « la case vide » 1 au 7 octobre. L'histoire complète montre que ces niveaux étaient déjà 3, 3 et 2 (mémo Weil v3.7, banc de rejet v3.2, leçon 2026).
- Test : 1 ajouté ; **125 sur 125 exécutés et réussis.**


## V6.9 — Le chaînon

Question de l'auteur : « il manque un opérateur symbolique entre la version discrète/réduite et la version continue/complète ».

- **Le chaînon.** Dans le Modèle réduit, F = q^D : les zéros sont le spectre du générateur D, répété avec la période 2πi / log q. Le pas discret est l'exponentielle d'un générateur, comme dans le calcul symbolique (E = e^hD).
- **Mesuré : l'opérateur se reconstruit depuis les seuls comptages** (construction GNS/Krylov, 749 objets). 524 vraies courbes : dimension 2g, valeurs propres à 10⁻¹³, opérateur unitaire, métrique positive. 220 faux jumeaux : opérateur et symétrie reconstruits aussi bien, mais métrique jamais positive (une direction négative par paire de zéros hors cercle). 5 objets à zéros confondus : un axe par zéro distinct, la multiplicité reparaît comme masse.
- **Mesuré : le spectre des longueurs se lit dans les zéros.** ζ : pics aux log p^k (35 longueurs, écart 0,045) ; DH : 45,6 % du signal aux longueurs composites (log 6, log 12…), l'absence de produit d'Euler lue dans les seuls zéros ; courbes : réseaux n·log q, un par base.
- **Lecture.** Ce qui manque pour ζ n'est pas l'opérateur, c'est la métrique positive. Dans le Modèle réduit, elle vient de la surface C×C, un étage au-dessus. Le dictionnaire de v3.7 est révisé : la tour a une image (les longueurs).
- Question divergente : la simplicité des zéros de ζ se lit comme « l'espace est engendré par le seul vecteur des nombres premiers ».
- Indicateur : étape V6.9 ajoutée ; aucun niveau ne change (comprendre et case vide précisés).
- Tests : 4 ajoutés ; **129 sur 129 exécutés et réussis.**

Voir `1_Presentation/32_LE_CHAINON_DU_DISCRET_AU_CONTINU.md`.


## V6.10 — Le générateur des premiers, et un navigateur de recherche

Demande de l'auteur : « Tenter les 3 suites envisagées. Par priorité explicative. » Puis : repenser la démonstration comme un itinéraire (GPS), les métaphores comme opérateurs symboliques, l'indicateur comme but ; « finis le 1, puis laisse-le proposer une suite ».

- **Le générateur des premiers (suite 1, document 33).** Traces t_n = Σ ĝ(γ) e^(iγnh) calculées par la formule explicite avec les seuls nombres premiers (audit : 3,5·10⁻¹⁴ pour ζ) ; faisceau de Toeplitz → opérateur de translation e^(hD). Avec les premiers ≤ 439 : 226 zéros de ζ, 334 de L(s, χ₅), 330 de DH, aucune fausse détection ; chaque vraie valeur propre porte la masse ĝ(γ) (zéro simple). Avec les premiers ≤ 23 862 : 284 zéros de ζ, tous à mieux que 1,6·10⁻⁴.
- **La métrique, lue depuis les premiers.** Positive pour ζ et L ; pour DH, deux directions négatives par quadruplet hors droite, attribuées exactement ; elle voit le quadruplet de 240,4 avant que l'opérateur ne le résolve.
- **Le pas.** Au pas h, les zéros ne sont vus qu'à 2π/h près ; au pas log 2 (une « base »), tous sont repliés.
- **Navigateur de recherche (document 34, prototype).** Position : l'indicateur ; opérateurs : les 69 métaphores du registre avec leur garde ; coups avec thèse, témoin contraire, réfutation, gain et coût ; score = (valeur + explicatif) / coût. Prochain coup proposé : la base comme pas de temps (suite 2), puis la métrique des premiers plus haut, puis le degré 2.
- **Suite 2 (la base comme pas de temps) :** calculs faits en V6.10, rédigés en V6.11 (document 35).
- Indicateur : étape V6.10 ; la case vide passe de 3 à 4 (la métrique, ce que l'objet doit porter, mesurée depuis les premiers avec témoins).
- Tests : 5 ajoutés ; **134 sur 134 exécutés et réussis.**

Voir `1_Presentation/33_LE_GENERATEUR_DES_PREMIERS.md` et `1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html`.


## V6.11 — La base comme pas de temps ; le navigateur calibré

Coup choisi par le navigateur (score 3,0). Accord de l'auteur : « Ok on avance. »

- **Modèle réduit (525 courbes, 220 faux jumeaux), vu sur F_q².** D est intrinsèque : zéros sur F_q² = zéros de la courbe ∪ de sa tordue (525 sur 525). La métrique survit au changement de base (525 unitaires ; 220 faux jumeaux, directions négatives = zéros hors cercle distincts / 2). La descente efface un signe par facteur irréductible (525 sur 525) : 2 objets possibles en bas dans 440 cas, jusqu'à 12. La réfutation annoncée (deux courbes non tordues aux mêmes comptages sur F_q²) n'a pas eu lieu dans le corpus.
- **ζ, L, DH : la métrique selon le pas.** ζ et L : aucune direction négative à aucun pas. DH, à nombres premiers fixés : 10 → 4 → 2 → 0 directions négatives quand h passe de 0,01 à 0,1 ; à N fixé : elles restent (4 → 10). Un pas grossier noie la métrique, faute d'échantillons ; le seul pas qui convienne à ζ est le flot.
- **Navigateur ajusté** : distance au but (le chaînon : finitude non nécessaire, traces et symétrie acquises, métrique manquante ; bonus aux coups sur le maillon manquant) et pré-enregistrement des prévisions (bilan prévu contre obtenu). Prochain coup proposé : la métrique des premiers, plus haut (2,25), puis les paires de Lehmer (1,0), le degré 2 (0,6).
- Ménage : copies de travail des versions V6.3d à V6.9 retirées de l'espace de travail ; dans les sorties, 29 fichiers isolés qui existaient à l'identique dans un zip.
- Indicateur : étape V6.11 (aucun niveau ne change). Tests : 3 ajoutés ; **137 sur 137 exécutés et réussis.**

Voir `1_Presentation/35_LA_BASE_COMME_PAS_DE_TEMPS.md` et `1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html`.


## V6.11.1 — Le portail

Demande de l'auteur : un index qui reprenne tout, à jour, avec lequel on passe d'une page à l'autre et vers les documents.

- `00_PORTAIL.html` (généré par `2_Methode/Portail/build_portail.py`) : où on en est (six niveaux, maillon manquant, prochain coup), les cinq dernières étapes, tous les documents de présentation avec leurs formats, leurs figures et l'étape où ils ont été produits.
- `00_Carte_des_idees.html` mise à jour : nouvelle partie « V6.4 à V6.11 · Nécessité et chaînon » (12 nœuds avec fiches et documents), statut « mesuré, reproduit », renvois depuis Positivité de Weil, Hilbert–Pólya et Kalman.
- Barre de navigation commune (portail, carte, indicateur, navigateur, mode d'emploi) sur les quatre pages.
- Publication en ligne : `python 2_Methode/Portail/build_portail.py --publication DOSSIER` prépare une copie où les .md et .docx sont convertis en HTML et les liens réécrits ; elle est publiée comme page en ligne avec ses documents.
- Tests : 2 ajoutés ; **139 sur 139 exécutés et réussis.**


## V6.12 — Les idées rejetées relues ; les priorités refaites

Demande de l'auteur : refaire les priorités au regard de la relecture, et relire symboliquement les trois idées rejetées avec le dictionnaire des idées.

- **Le Kalman relu.** Sur les traces des premiers, le filtre de Kalman est la récurrence de Levinson. Innovations positives pour ζ et L(s, χ₅) jusqu'à l'horizon numérique (|k_n| ≤ 0,79) ; pour DH, première innovation négative à la fenêtre 3,52, avec les nombres premiers ≤ 36 ; seuil de 2,7 à 3,5 selon le quadruplet.
- **Les sources relues.** Le mode fantôme de V4.3 (Im ≈ 73,8) porte une masse de 1,3·10⁻⁹ ; le vrai zéro hors droite, 1.
- **Le Schrödinger relu.** L'opérateur existe sans zéro injecté ; les blocs de Jordan venaient du signal d'ordre 2 ; le Théorème A se lit au rayon spectral (DH : 0,308517 ; ζ et L : < 10⁻⁶). Le verrou M > 0 ⟺ RH reste, situé.
- **Priorités refaites (navigateur)** : la loi de seuil (2,33), la métrique plus haut (1,75), l'île vue par les premiers (1,5), préparer la relecture (1,07), les paires de Lehmer (1,0), le degré 2 par les premiers (0,96 ; coût revu de 4 à 2,5).
- Carte des idées : les trois nœuds rétrogradés renvoient à leur relecture. Portail : document 36 en ligne.
- Tests : 2 ajoutés ; **141 sur 141 exécutés et réussis.**

Voir `1_Presentation/36_LES_IDEES_REJETEES_RELUES.md`.


## V6.13 — La pré-relecture

Demande de l'auteur : « Suis cette trajectoire avec les 3 relectures d'abord en parallèle puis les autres. »

- Trois relectures indépendantes, en parallèle : Théorème A, Théorème B, note sur l'Archipel (§3). Chacune a refait la preuve pas à pas, avec contrôles numériques et recherche d'antériorité.
- **Théorème A** : correct ; trois retouches de rédaction ; méthode standard (analogue au second ordre de la caractérisation de Θ par ψ(x) − x) ; attribution à Brent–Platt–Trudgian corrigée.
- **Théorème B** : correct ; quatre retouches ; transposition du théorème de Cramér au pôle double. Corollaire nouveau B′, à faire vérifier : sous RH, Q(X)/(log X)³ → 4κ/3 si et seulement si tous les zéros sont simples. α corrigé : −0,3074.
- **Archipel** : correct sur le fond ; phrase fausse du §3.1 corrigée ; trou du §3.4 comblé en citant Saias–Weingartner (Th. 2) ; le corollaire n'est pas nouveau ; Booker–Thorne couvrent déjà le degré 2 pour cette partie. Rigidité au premier ordre : identité exacte de constante 3.
- Dossier envoyable en anglais : `1_Presentation/relecture/`. Corrections dans `30_ARCHIPEL_D_EULER`, `LEMMES_RIGOUREUX.md`, `ALPHA_BETA_ANALYSE.md`.
- Navigateur : « Préparer la relecture » fait (réfutation tenue) ; degré 2 recentré ; prochain coup : la loi de seuil des innovations. Indicateur : étape V6.13, aucun niveau ne change (une pré-relecture n'est pas une relecture).
- Tests : 3 ajoutés ; **144 sur 144 exécutés et réussis.**

Voir `1_Presentation/37_PRE_RELECTURE_A_B_ARCHIPEL.md`.


## V6.14 — La loi de seuil : le temps de Heisenberg

Coup du navigateur « La loi de seuil des innovations », joué après la pré-relecture.

- **Correction de la V6.12.** Le signe d'une innovation de Levinson n'est pas fiable dès que la métrique est mal conditionnée, même si |E/E₀| reste grand (−2·10⁻³ sur un fond positif par construction). Les seuils se lisent désormais sur les valeurs propres. Les seuils par quadruplet 2,71 ; 3,30 ; 2,78 ; 2,76 étaient du bruit (3,91 ; 4,35 ; 4,17 ; 4,21). La détection principale de DH (3,53, premiers ≤ 36) et l'absence d'alarme pour ζ et L tiennent.
- **La loi.** Un quadruplet hors droite à la hauteur γ₀ s'entend à la fenêtre L_c ≈ log(q·γ₀/2π), le temps de Heisenberg, c'est-à-dire avec les premiers jusqu'au conducteur analytique q·γ₀/2π. Rapport 0,95–1,08 pour ζ et L(s, χ₅) (hauteurs 20 à 200), 0,80–0,89 pour les quadruplets réels de DH. Prévision écrite avant les tests (ζ, pas, largeur, « trou ») : trois sur quatre tenues.
- L'écart à la droite, le poids (environ 6 % par décade), la position entre deux zéros, le pas (sous Nyquist) et la largeur ne jouent qu'en correction ; retirer les zéros plus bas ne change rien.
- **Lemme d'inertie** (exact) : la métrique cesse d'être positive si et seulement si C⁻¹ + U*B⁻¹U est définie positive. Précision étendue : 80 chiffres pour la détection exacte (30 ne suffisent pas).
- Navigateur : prochain coup, le temps de Heisenberg en degré 2 avec Δ de Ramanujan ; nouveaux coups « le facteur de DH » et « le devineur de lois » ; registre : Le Temps de Heisenberg, La Balance d'inertie, Le Signe fragile (78 opérateurs).
- Tests : 3 ajoutés, 1 mis à jour ; **147 sur 147 exécutés et réussis.**

Voir `1_Presentation/38_LA_LOI_DE_SEUIL_LE_TEMPS_DE_HEISENBERG.md`.


## V6.15 — Le degré 2 et le recensement

Demande de l'auteur : « Faire les deux points suivants » (les deux premiers coups du navigateur). Prévisions écrites avant tout calcul (`data/prevision_v615.md`).

- **Degré 2, Δ de Ramanujan.** τ(n) exacts jusqu'à 25 000 (restes chinois) ; L(Δ, s) reconstruite depuis les premiers, zéros à 1,2·10⁻⁹ de ceux calculés sans les premiers (mpmath) ; loi de Weyl. La loi de seuil y double : L_c/Ω = 1,02–1,05, L_c(Δ)/L_c(ζ) = 1,91–2,07. La longueur d'écoute est le poids archimédien Ω(γ₀) = 2π × densité des zéros.
- **Le recensement.** Plan de la loi (a = 0,012 ; h = 0,004 ; premiers ≤ 1 370) : la métrique de DH a 50 directions négatives, toutes attribuées à 25 quadruplets hors droite (15 jusqu'à 600, 6 jusqu'à 785, 4 repliés de 1 092 à 1 464) ; zéros de DH calculés de 600 à 1 700 avec contrôle de complétude. L(s, χ₅) et ζ : aucune. Allumages à 0,75–0,95 du temps de Heisenberg.
- Prévisions : P1, P2, P5 tenues ; P4 et P6 tenues à une exception près ; P3 (« exactement 30 ») fausse dans sa lettre.
- Indice non pré-enregistré : le produit ζ·L(s, χ₅) s'allume plus tôt (0,87–0,98), comme DH : deux familles de zéros sans répulsion mutuelle.
- Indicateur : degré 2, 2 → 3. Navigateur : prochain coup, l'Archipel en degré 2. Registre : Le Poids archimédien, Le Quadruplet replié, La Somme sans répulsion (81 opérateurs).
- Tests : 4 ajoutés ; **151 sur 151 exécutés et réussis.**

Voir `1_Presentation/39_LE_DEGRE_2_ET_LE_RECENSEMENT.md`.


## V6.16 — La Rencontre à trois, et les croisements dans l'indicateur

Demandes de l'auteur : « Ce qui m'étonne, c'est qu'il n'y a pas de croisement entre les 3 aussi difficiles que RH » ; « il faut que les croisements soient pris en compte dans l'indicateur ». Prévisions écrites avant le calcul (`data/prevision_v616.md`).

- **L'identité.** À la fenêtre de Heisenberg, la marge locale de la métrique pour une paire de zéros d'écart normalisé s vaut 1 − sinc²(πs) : la densité de corrélation de paires de Montgomery, nulle à la rencontre, négative hors de la droite.
- **Mesuré sur 1 070 zéros de ζ.** 4 marges sous 0,1, contre 13 (GUE) et 320 (Poisson). β est lisse à 95 % ; sa part d'écart suit 1/s² et compte les paires serrées ; la paire de Lehmer (7 005) : marge 0,006, part d'écart environ mille fois la médiane.
- Prévisions : P4 tenue ; P1 qualitative tenue, quantitative fausse (3 fois moins de petites marges que le GUE) ; P2 et P3 fausses pour β entier ; P5 à moitié.
- **Les croisements dans l'indicateur.** Septième dimension « Croiser » (niveau = plus haut croisement produit par le corpus), comptée rétroactivement (V6.5 : 4 ; V6.7 : 5 ; V6.13 : 6) ; carte des croisements avec zones d'ombre et pendants dans le Modèle réduit.
- **Navigateur.** Règle du croisement (+0,5 par conjecture reliée au-delà de la première), veille rétrospective des pistes écartées, règle du pendant ; trois idées reprises des textes « Nécessité démontrée du Modèle réduit » et « Classement des instruments 3D ». Prochain coup : la Rencontre en degré 2.
- Registre : La Rencontre à trois, Le Compteur de paires, La Zone d'ombre (84 opérateurs). Tests : 3 ajoutés ; **154 sur 154 exécutés et réussis.**

Voir `1_Presentation/40_LA_RENCONTRE_A_TROIS.md`.


## V6.17 — La Rencontre en degré 2, et son pendant dans le Modèle réduit

Demande de l'auteur : « Suite » : les deux coups en tête du navigateur, « La Rencontre en degré 2 » et « La Rencontre dans le Modèle réduit ». Prévisions écrites avant le calcul (`data/prevision_v617.md`).

- **Le Contour tourné.** La rotation du contour de Mellin, repliée par la modularité, donne Λ(6+it) = 2e^{−φt} Re(e^{6iφ}A(6+it)) : plus d'annulation exponentielle, la double précision suffit. 2 139 zéros de L(Δ, s) jusqu'à 1 500 en deux minutes (accord 10⁻¹³ avec mpmath ; complétude de Turing). Correctif V6.15 : 196 zéros jusqu'à 232,08, et non 189 (7 manqués au bord de la fenêtre du générateur).
- **Trois identités.** À la fenêtre N, la marge totale de la métrique est la densité de Weyl de U(N), et la marge d'une paire la corrélation de paires du CUE(N) ; pour une paire conjuguée, marge = sin²θ = 1 − ρ₁² = (π/2) × densité de Sato–Tate.
- **Mesuré.** Les zéros de Δ se repoussent (8 marges sous 0,1, contre 26 pour le GUE et 641 pour Poisson), avec le même déficit à basse hauteur que ζ. ζ·L(s, χ₅) superpose deux familles étrangères (15 % de petites marges, toutes mixtes). Aux premiers de Δ : Sato–Tate (KS p = 0,86), marge minimale 0,026. Modèle réduit : Sato–Tate sur 561 258 courbes ; à l'étage 2, collisions exactement aux 18 338 courbes supersingulières, avec RH vraie.
- Prévisions : P1, P3, P4 tenues ; P2 fausse (le déficit ne dépend pas que de la densité) ; P5 tenue sauf la clause de monotonie.
- Indicateur : degré 2, 3 → 4 ; trois croisements (La Rencontre en degré 2, La Rencontre locale, Les Familles étrangères) ; zones d'ombre simplicité × degré 2 et répulsion × degré 2 remplies. Navigateur : prochain coup, la Loi de la marge en genre 2. Registre : Le Contour tourné, La Loi de la marge, Les Familles étrangères (87 opérateurs).
- Tests : 4 ajoutés ; **158 sur 158 exécutés et réussis.**

Voir `1_Presentation/41_LA_RENCONTRE_EN_DEGRE_2.md`.


## V6.34 — Validation directe et lemme des jets

- Document 58 : deux articles corrigés ; portée des documents 47, 51 et 56 rectifiée ; critère conjoint RH et simplicité.
- V7 : comptage direct de onze fonctions jusqu’à 300, stable aux raffinements ; au col annoncé à 145, sorties confirmées vers 79,40 et 112,55. Deux censures sont conservées.
- V11 : 96 directions indépendantes, cinq témoins ; corrélation partielle T–|a(1)| +0,815, IC [0,704 ; 0,876]. Prévision résiduelle sur le défaut D fausse (+0,142).
- Jets : lemme de rang démontré, témoins exacts pour p=29,61,101 ; paramètres optimisés jusqu’à p=10007 ; erreur O(√p) par une famille explicite et le tordu. Méthode classique de Stepanov.
- Neuf tests nouveaux (192 au total) ; données, protocole et scripts sous le préfixe v634. Index et PDF mis à jour. Les signatures proches du seuil et la relecture externe restent à contrôler.

## V6.33 — La force qui abaisse le relief

Demande de l'auteur : mesurer si la hauteur T* du relief suit le défaut de multiplicativité.
- `1_Presentation/57_LA_FORCE_DU_RELIEF.md/.pdf/.png` : défaut de multiplicativité D (nul aux points d'Euler) sur la carte de V₇ impair. Les trois prévisions sont fausses : corrélation T*–D −0,31 ; à distance égale, plus de défaut va avec plus de hauteur (+0,38) ; le col des îles passe là où le défaut est fort. Après coup (non prévu) : à distance égale, la hauteur suit le premier coefficient |a(1)| (corrélation partielle +0,81) ; à |a(1)| égal, le défaut abaisse bien le relief (−0,24). Deux forces : un ancrage (a(1)) et une poussée (le défaut). À retester avec des prévisions sur V₁₁ ou V₁₃.
- Script `scripts/run_force_multiplicativite.py` ; prévisions `data/prevision_v633_force.md` ; données `data/force_multiplicativite.csv/.json` ; test `tests/test_v633_force.py` (1).

## V6.32 — Les accents des fichiers .md

Demande de l'auteur : « Pourquoi tous les fichiers .md posent problème pour les signes diacritiques ? »
- Cause : les fichiers sont en UTF-8 valide, mais un fichier .md n'annonce pas son encodage. Ouvert directement dans un navigateur ou un éditeur Windows, il est lu dans l'ancien encodage Windows-1252 : « é » devient « Ã© ».
- Correction : la marque UTF-8 (BOM) est ajoutée à tous les fichiers .md (115, hors documents reçus, laissés intacts) par `2_Methode/Outils/md_utf8_bom.py` ; tous les scripts lisent désormais en « utf-8-sig » (avec ou sans marque) ; les générateurs écrivent leurs .md avec la marque. Pages produites inchangées.
- Test `tests/test_v632_encodage.py` (1).

## V6.31 — Le relief de l'archipel, les formules de la matrice, la liste des figures, le dépôt GitHub

Demandes de l'auteur : préparer la publication sur GitHub (licence, README) ; les formules de chaque théorie en popup dans la matrice ; une liste des figures ; une seule vue 3D oblique pour l'archipel (« trois îlots, puis une grande île »).
- `1_Presentation/56_LE_RELIEF_DE_L_ARCHIPEL.md/.pdf/.png` : relief T*(u, v) de la carte de V₇ impair (seuil de déficit persistant ; portée corrigée en V6.34) ; un seul continent jusqu'à T = 144, trois îles dès T = 145. Prévisions : fausses avec le critère prévu (dominé par un bruit de bord : 75 % des points ont un déficit transitoire) ; critère persistant choisi après coup. Script `scripts/run_archipel_relief.py` ; prévisions `data/prevision_v631_relief.md` ; données `data/archipel_relief.csv/.json`.
- Matrice (doc. 44) : chaque théorie a sa formule (champ `formule`, LaTeX), rendue en MathML (`2_Methode/Matrice/render_formules.js`) ; popup au survol ou au toucher du nom, et formule dans la fiche.
- `00_Liste_des_figures.html` et `1_Presentation/LISTE_DES_FIGURES.md` (générateur `2_Methode/Figures/build_figures.py`) : 29 figures des documents, 28 figures de calcul, 4 figures d’articles ; lien « Figures » dans la barre de navigation.
- Publication : `LICENSE` (MIT, code), `LICENSE-CC-BY-4.0.md` (textes, figures, données), `CITATION.cff`, `requirements.txt`, `.gitignore` ; README d'accueil bilingue. La copie publique (préparée à part) exclut le document reçu de tiers et remplace l'adresse électronique personnelle dans trois fichiers ; détail dans `4_Archives/NON_PUBLIE.md` de cette copie.
- Test `tests/test_v631.py` (1).

## V6.30 — Les articles présentables

Demande de l'auteur : « Prépare les articles présentables » ; lettre avec « Cher Professeur », sans nom.
- `1_Presentation/articles/` : article 1 (*A mean square with double poles at the zeros of ζ*, 10 pages : Théorèmes A et B, corollaire B′, identité de Nyman–Beurling, Q(X) jusqu'à 10⁸) et article 2 (*Prime-side Weil forms in finite windows*, 6 pages : dictionnaire C × C, proposition d'inertie des faux polynômes, 180 réglages avec le témoin DH), en LaTeX et PDF ; lettres `lettre_FR.txt` et `letter_EN.txt` ; liste des vérifications à faire avant envoi (`LISEZMOI_ARTICLES.md`) ; scripts des figures (`figures/`).
- `1_Presentation/55_ARTICLES_PRESENTABLES.md/.pdf` : présentation. Correctif au doc. 52 : le seuil de DH se situe entre X ≈ 20 et X ≈ 56 (47 réglages sur 48 dès X ≥ 55,7), et non à 61.
- Portail : le dossier des articles est rattaché au document 55. Test `tests/test_v630_articles.py` (1) : les chiffres des articles sont recoupés avec les données.

## V6.29 — Le trou à trois, lu ; les proportions de 2026 ; la matrice complétée

Demande de l'auteur : « Suites » (les trois coups en tête du navigateur).
- `1_Presentation/54_LE_TROU_A_TROIS_LU.md/.pdf/.png` : la correction de Bogomolny et al. prise dans son domaine (CUE de taille N ≥ 3) donne un déficit de triples serrés du bon sens mais trop faible (CUE(3) : 0,0082, soit 8,8 attendus pour ζ ; 0 observé) ; le rapport de deux écarts consécutifs (Nishigaki 2025), insensible à l'échelle et au dépliage, s'écarte aussi du noyau sinus (ζ +2,7σ, L(χ5) +4,4σ, Δ +5,2σ) : le trou à trois est une rigidité de forme. Prévisions : B1 juste, B2 et B3 fausses ; prévision du navigateur tenue. Les deux tiers d'Alpöge–Furman : sous forme normalisée, la borne rang–trace est une fonction des marges des paires (identité). Matrice : 11 cases sourcées, dont Mertens ⇔ RH (Titchmarsh, cité de mémoire) et DH ✗ proportion (Bombieri–Hejhal) ; ligne « Lindelöf pour les premiers ».
- Registre : 160 fiches (Nishigaki 2025, Bogomolny–Keating 2013, Atas et al. 2013). Navigateur : trois coups faits ; ouverts : « Le trou à trois par la formule à trois points de Bogomolny–Keating », « Compléter la matrice, deuxième séance ». Plan (doc. 43) adapté.
- Script `scripts/run_bblm_trou_a_trois.py` ; prévisions `data/prevision_v629_bblm.md` ; résultats `data/bblm_trou_a_trois.json` ; test `tests/test_v629_bblm.py` (1) ; le test de la matrice de la V6.19 vérifie désormais la transitivité sur Weil × Nyman–Beurling, la case Weil × Li étant écrite.

## V6.28 — Axe A : la Rencontre à n en hauteur

Demande de l'auteur : « Go ».
- `1_Presentation/53_LA_RENCONTRE_EN_HAUTEUR.md/.pdf` : la formule det[D_N] prolongée à la taille effective de Bogomolny et al. (N ≈ 1,0–1,26) donne des densités négatives : modèle inutilisable à ces hauteurs (les trois prévisions sont fausses). Fait mesuré, le trou à trois : triples de zéros consécutifs de portée < 1 : ζ 0 pour 15,6 attendus (t ≤ 1 500), L(χ5) 0 pour 7,2, Δ 3 pour 31,1 ; le CUE de taille 20 et 60 suit le noyau sinus (la taille finie seule ne crée pas le trou).
- Navigateur : axe A fait ; « Lire Bogomolny et al. pour de vrai » ouvert. Script `scripts/run_rencontre_hauteur.py` ; prévisions `data/prevision_v628_hauteur.md` ; résultats `data/rencontre_hauteur.json` ; test `tests/test_v628_hauteur.py` (1).

## V6.27 — J6 : le carré, en continu

Demande de l'auteur : « Suite » (axe J).
- `1_Presentation/52_J6_LE_CARRE_EN_CONTINU.md/.pdf/.png` : surface virtuelle recalculée sur 180 réglages fiables (4 largeurs, 3 pas, 5 fenêtres, jusqu'à X = 3 000) ; ζ : une seule direction positive dans 60 réglages sur 60 ; L(χ5) : aucune (60/60) ; DH : directions en trop dès X ≥ 61 (39/39). Le nombre de directions en trop de DH dépend du pas et de la largeur (prévision P3 fausse) : il n'est pas un invariant. Axe A reformulé (N_eff ≈ 1).
- Script `scripts/run_carre_continu.py` ; prévisions `data/prevision_v627_carre.md` ; résultats `data/carre_continu.csv/.json` ; test `tests/test_v627_carre.py` (1).

## V6.26 — J3b : le Frobenius de caractéristique un

Demande de l'auteur : faire le suivant, J3 ou J3b.
- `1_Presentation/51_J3B_LE_FROBENIUS_DE_CARACTERISTIQUE_UN.md/.pdf` : lecture ciblée (Arithmetic Site, caractéristique un et entropie, semi-anneaux thermodynamiques) ; le Frobenius de caractéristique un est un automorphisme pour tout λ > 0, il dilate les pentes et n'annule aucune dérivation : il ne fournit pas l'élément dont Stepanov a besoin (prévision tenue). J3 sous la forme de Stepanov est écarté ; l'axe J revient à la route de Weil, celle de Connes–Consani (positivité sur le carré) ; prochain coup J6, le carré en continu.
- Registre : 157 fiches (Connes–Consani 2009 et 2014, Marcolli–Thorngren). Navigateur : J3b fait, J3 dans les pistes écartées, J6 ouvert. Registre des métaphores : Le Frobenius trop bon.

## V6.25 — Les unités fictives : audit du document reçu

Document reçu de l'auteur le 11 octobre 2026 (« Unités fictives et bilan d'énergie du corpus RH », base V6.21), conservé sans modification dans `4_Archives/recus/Unites_fictives_RH/`.
- `1_Presentation/50_LES_UNITES_FICTIVES_AUDIT.md/.pdf` : script relancé en lecture seule sur la V6.24, résultats identiques ; formules vérifiées ; le bilan K + Q = Σ W_n est une sommation par parties (identité vraie pour toute suite) ; masses négatives = directions négatives de la métrique = directions positives en trop de la surface virtuelle ; borner le travail total revient à borner Q, donc à RH ; l'analyse dimensionnelle désigne 2Θ − 1 comme seul nombre sans unité du Théorème A, sans en fixer la valeur.
- Test `tests/test_v625_unites.py` (1).

## V6.24 — Analyse de risques, J3 simplifié, les deux tiers, et les documents de description à jour

Demande de l'auteur : une analyse de risques pour décider ; creuser J3 en le simplifiant ; comment est calculé le 67 %, et combien donne le même calcul ; mettre à jour les éléments de description.
- `1_Presentation/49_ANALYSE_DE_RISQUES_J3_ET_LES_DEUX_TIERS.md/.pdf/.png` : tableau de décision (J3 par petites étapes, axe A en parallèle) ; J3a : l'additivité ne décide rien, ce qui compte est la présence de x^p dans l'espace des fonctions auxiliaires ; les 67 % sont d'Alpöge–Furman (rang–trace sur la forme de Weil, sans hypothèse), pas d'OpenAI ni d'un tamis ; le même calcul sur nos zéros : 56 % de simples à la fenêtre démontrée (théorie 50 %), 88 % à A = 2, 97 % à A = 4 ; mélange ζ·L(χ5) : 30 %.
- Documents de description mis à jour jusqu'à V6.24 : synthèse (01), cheminement intellectuel (06), guide de lecture (07, avec un glossaire étendu).
- Navigateur : J3a et « le même calcul » faits ; J3b (lecture ciblée de Connes–Consani) ouvert. Plan : J par petites étapes, A en parallèle.
- Script `scripts/run_v624.py` ; prévisions `data/prevision_v624.md` ; résultats `data/v624.json` ; tests `tests/test_v624.py` (2).

## V6.23 — Axe J5 : le Frobenius qui n'est pas un morphisme

Demande de l'auteur : revenir au Théorème A avec des « dimensions fictives » et une dérivation en puissance ; sinon, faire le programme de la piste actuelle.
- `1_Presentation/48_LE_FROBENIUS_QUI_N_EST_PAS_UN_MORPHISME.md/.pdf/.png` : construction de Stepanov faite en algèbre linéaire exacte sur F_61 et F_101 ; avec le Frobenius, 13 à 52 fonctions auxiliaires (10 cas sur 12) ; avec l'identité (mêmes valeurs aux points) ou une permutation aléatoire, aucune (sauf deux coïncidences de rang) ; ce qui compte est l'inséparabilité (dérivée nulle). Prévisions : 3 justes (dont une à une exception près), 1 fausse (borne triviale aux tailles calculées). Note : les dimensions fictives du Théorème A sont la dimension énergétique (doc. 08) ; une dérivation fractionnaire ne la déplace pas.
- Plan : J5 fait, J3 précisé (l'action d'échelle a-t-elle une dérivée nulle ?). Navigateur, matrice, registre des métaphores (La Dérivée nulle) mis à jour.
- Script `scripts/run_frobenius_non_geometrique.py` ; prévisions `data/prevision_v623_frobenius.md` ; résultats `data/frobenius_non_geometrique.json` ; tests `tests/test_v623_frobenius.py` (2).

## V6.22 — Axe J2 : le Riemann–Roch virtuel

Demande de l'auteur : étape suivante ; viser une propriété d'existence, de dimension ou de dualité, justifiée sans RH, en comparaison avec le Riemann–Roch de Connes–Consani.
- `1_Presentation/47_LE_RIEMANN_ROCH_VIRTUEL.md/.pdf/.png` : sur 425 courbes et 220 faux jumeaux, le long de la tour (m ≤ 80) : existence (Pic⁰ non vide) 2 jumeaux, Clifford 0, Stepanov–Bombieri 121, Stepanov + tordu quadratique 220 sur 220 (étage médian 4 ; Castelnuovo 3) ; aucune courbe en défaut. Prévisions : 2 justes, 2 fausses, 1 ajoutée entre les deux calculs (juste). Le lemme manquant pour ζ est formulé : une borne unilatérale de ψ(x) − x obtenue par une fonction auxiliaire, ce qui demande un Frobenius absolu.
- Registre : Connes–Consani 2022 et 2024, van der Geer–Schoof, Groenewegen (154 fiches). Matrice : lignes Stepanov–Bombieri, borne unilatérale des premiers, Riemann–Roch pour Spec Z. Navigateur : J2 fait ; J5 (le Frobenius qui n'est pas un morphisme) et J3 (la fonction auxiliaire pour les premiers) ouverts. Registre des métaphores : La Fonction auxiliaire, Le Frobenius absolu.
- Script `scripts/run_riemann_roch_virtuel.py` ; prévisions `data/prevision_v622_riemann_roch.md` ; résultats `data/riemann_roch_virtuel.csv/.json` ; tests `tests/test_v622_riemann_roch.py` (2).

## V6.21 — Axe J : la surface virtuelle

Demande de l'auteur : « Et si on résolvait par une géométrie impossible ou virtuelle ? » ; « Axe J prioritaire. »
- `1_Presentation/46_LA_SURFACE_VIRTUELLE.md/.pdf/.png` : dictionnaire démontré dans le Modèle réduit (fibres ↔ pôle, intersections ↔ puissances de premiers, genre ↔ terme archimédien ; orthogonalement aux fibres, forme d'intersection = −métrique des zéros) ; indice de Hodge vérifié pour 425 courbes sur 425, violé avec un surplus exact pour les 220 faux jumeaux ; surface virtuelle de ζ calculée depuis les premiers ≤ 439 : une seule direction positive ; DH : 2 puis 10 en trop. Dictionnaire classique (Weil, Bombieri, Connes) : redécouverte, signalée.
- Plan (doc. 43) : axe J en tête (J2 Riemann–Roch virtuel, J3, J4). Navigateur : coup fait « La surface virtuelle », coup ouvert « Le Riemann–Roch virtuel ». Matrice : ligne « Indice de Hodge de la surface virtuelle » ; ligne CF renommée « Modèle réduit (RH des corps de fonctions) ».
- Script `scripts/run_surface_virtuelle.py` ; prévisions `data/prevision_v621_surface.md` ; résultats `data/surface_virtuelle*.csv/.json` ; tests `tests/test_v621_surface.py` (2).

## V6.20 — Le Palier 4/3 recalculé, les pistes d'OpenAI dans la matrice, et ce que le programme a retrouvé

Demande de l'auteur : marquer dans la matrice ce qui vient d'OpenAI, dire ce que le corpus a redécouvert avec la référence, adapter le plan, et refaire le calcul du 4/3 pour voir s'il n'est pas légèrement différent.
- `1_Presentation/45_LE_PALIER_RECALCULE_ET_LES_REDECOUVERTES.md/.pdf/.png` : palier recalculé jusqu'à 5·10⁶ (prévisions écrites avant : 2 justes, 2 à moitié) ; médiane 1,313 = 0,985 × 4/3, sans montée visible ; le 4/3 apparent est une compensation (b² ≈ 1,16, r_Q ≈ 0,72, queue ≈ 0,15) ; pics jusqu'à 3,27 × 4/3 là où A_N s'annule ; correctif à la clôture V5.6 ; recensement de 14 résultats retrouvés ici puis reconnus dans la littérature, avec documents du corpus et clés.
- Matrice (doc. 44) : 22 théories ; provenance « retrouvé puis reconnu » ; coin bleu et « OA » pour ce qui vient d'OpenAI ; lignes Archipel d'Euler, dimension ½ (Lapidus), Tamis à deux ; cases NB × simplicité (palier), DH × (★), Tamis × NB ; tableau « Ce que le programme a retrouvé ».
- Plan (doc. 43) adapté : correspondance des 27 pistes d'OpenAI avec les axes et la matrice ; axes H (Tamis à deux) et I (Palier et simplicité) ; ordre refait.
- Script `scripts/run_palier_quatre_tiers.py` ; prévisions `data/prevision_v620_palier.md` ; résultats `data/palier_quatre_tiers.csv/.json`, `data/palier_balayage.csv` ; tests `tests/test_v620_palier.py` (3).

## V6.19 — Plan de recherche : la Rencontre à n et la matrice des théories

Demande de l'auteur : un plan de recherche qui utilise les nouvelles lectures (figures semblables, mais en 3D), en gardant la méthode symbolique → opérateur → fonctions → identification, et une représentation qui situe la matrice d'équivalence et de force des théories, à compléter.
- `1_Presentation/43_PLAN_DE_RECHERCHE_LA_RENCONTRE_A_N.md/.pdf/.png` : identité démontrée (la marge d'un n-uplet est sa corrélation à n points du CUE(N)) ; triplets des zéros de ζ conformes au noyau sinus (χ² 1,34 ; Poisson 17,3) ; loi de superposition des Familles étrangères (χ² 0,87) ; déficit à basse hauteur ; sept axes avec prévisions, témoins et règles d'arrêt.
- `1_Presentation/44_MATRICE_DES_THEORIES.html` (générée par `2_Methode/Matrice/build_matrice.py` depuis `matrice_theories.json`) : 19 théories, 50 cases écrites, 144 déduites par transitivité, 148 à compléter ; fiche de chaque théorie selon les quatre temps de la méthode ; échelle de force.
- Navigateur : coup fait « La Rencontre à n » ; coups ouverts : la Rencontre à n en hauteur, Montgomery sans RH, les collisions du flot, lire les proportions de 2026, compléter la matrice. Registre des métaphores : La Rencontre à n, Le Carillon de Bohr. Registre des sources : Rudnick–Sarnak 1996 (150 fiches).
- Script `scripts/run_rencontre_a_n.py` ; prévisions `data/prevision_v619.md` ; résultats `data/rencontre_a_n.json`, `data/rencontre_a_n_zeta.csv` ; tests `tests/test_v619_rencontre_a_n.py`.


### V6.19.1 — La matrice plus lisible, avec la provenance

Demande de l'auteur : mettre en couleur ce qui a été recalculé dans ce programme et ce qui serait nouveau ; rendre la carte plus lisible ; liens vers les articles dans les en-têtes.
- Matrice (doc. 44) : chaque théorie et chaque relation porte sa provenance (littérature, recalculé ou vérifié ici, éventuellement nouveau, question ouverte, déduit), avec une note qui renvoie aux documents ; couleur au choix par provenance ou par type de relation ; cases déduites atténuées et masquables ; cases vides discrètes ; traits épais entre les groupes de force ; ligne et colonne éclairées au survol.
- En-têtes : lien ↗ vers le résumé de l'article principal de chaque théorie ; liste des 48 articles de la matrice avec leurs liens.
- Bilan : 8 théories recalculées dans le programme, 3 éventuellement nouvelles (Théorème A, critère (★), identité de la Rencontre à n), toutes à confirmer par la littérature ou une relecture.

## V6.18 — Les sources, la carte des croisements, les documents explicatifs

Demandes de l'auteur : savoir où sont les sources et où elles sont citées, en gardant la référence dans le texte ; situer chaque article dans les grilles de lecture par couleur d'intérêt, avec un lien vers le résumé et des priorités ; le Modèle réduit dans la carte des croisements, et des cases qui mènent aux documents ; mettre à jour les documents explicatifs et mettre le Cheminement intellectuel sur le site ; voir les pistes évoquées par OpenAI.

- **Registre des sources** (`1_Presentation/42_REGISTRE_DES_SOURCES.md`, généré par `2_Methode/Sources/build_sources.py` depuis `sources.json`) : 132 fiches, 64 vérifiées en ligne ; couleurs 🔴 appui, 🟠 à confronter, 🔵 contexte, ⚪ outil ; 12 citations du corpus à corriger (dont Hadamard–de la Vallée Poussin/Mertens, Hamburger, Weil 1948, Zhu, « loi de Weyl » = formule de Riemann–von Mangoldt) ; priorités de lecture. Les citations restent dans le texte, avec une clé [Xxx00] qui renvoie à la fiche (111 clés ajoutées dans les documents 01–41). Les anciennes bibliographies sont conservées.
- **Carte des croisements** (document 31) : colonne « Modèle réduit » avec ses zones d'ombre ; chaque croisement mène à son document ; pastilles de littérature colorées, vers le résumé.
- **Navigateur** : trois coups « lecture » (Weil 1948, Hamburger 1921, Beurling 1955) ; pistes d'OpenAI inventoriées (27 pistes, 18 explorées ; 7 nouveaux coups, 7 pistes écartées). Prochain coup : « Plusieurs bouchons ».
- **Documents explicatifs** mis à jour jusqu'à V6.17 et mis en ligne, en tête du portail : Synthèse (01), Cheminement intellectuel (06), Guide de lecture intuitif (07). Les versions Word d'origine sont dans `4_Archives/historique/documents_v5/`.
- Tests : 2 ajoutés.

Voir `1_Presentation/42_REGISTRE_DES_SOURCES.md`.

### V6.18.1 — Toutes les références, au bon format

Demande de l'auteur : reprendre le travail des échanges de 13 h 47 à 16 h 37 en partant de la V6.18 livrée, et donner toutes les références citées au bon format.
- Registre : 139 fiches (65 vérifiées en ligne) ; ajoutées : Ramanujan 1916, Mattuck–Tate 1958, Grothendieck 1958, Wigner 1957, Weyl 1912 et 1939, Hecke 1937. Bibliographie au format uniforme ([clé] auteurs, *titre*, publication, lien) dans le document 42.
- Chaque document numéroté (sauf 20 et 42) se termine par une section « Références », générée depuis le registre (marqueurs `references:debut/fin`), avec le statut de vérification et les correctifs. Clés ajoutées dans les documents 08 et 14–23.
- Corrections faites dans le texte : Hamburger (doc. 30), Zhu (29), Rubinstein (41), Connes–Consani–Moscovici (21), « loi de Weyl » → formule de Riemann–von Mangoldt (39). Les autres correctifs figurent dans la section « Références » de chaque document.
- Sources d'OpenAI et documents Word : le registre lit aussi les documents qui n'existent qu'en Word (02 à 05, 09 à 13, dont les audits des réponses d'OpenAI). Dix fiches ajoutées, 149 au total : Maier–Rassias 2018, Conrey 2003 (Notices AMS), MathOverflow 400779 (non vérifiée : site bloqué), Gonek 1989, Platt–Trudgian 2021, Baluyot–Goldston–Suriajaya–Turnage-Butterbaugh 2024, B. Wang 2026 (deux prépublications), Pearce-Crump 2026, Besicovitch 1932 (non vérifiée). Liens d'OpenAI nettoyés du traceur utm_source.
