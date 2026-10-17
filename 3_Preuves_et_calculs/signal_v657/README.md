# V6.57 — Information de signe et résolution adaptative

Les deux expériences ont des statuts différents. Le certificat de résolution emploie mpmath.iv et les primitives encadrées existantes du corpus. Le diagnostic matriciel réutilise les quadratures exploratoires V644, sans les transformer en intervalles certifiés.

Depuis la racine du corpus :

```sh
python -B 3_Preuves_et_calculs/signal_v657/certifier_resolution.py
python -B 3_Preuves_et_calculs/signal_v657/v657_signal_couplings.py --corpus . --output 3_Preuves_et_calculs/signal_v657/v657_signal_couplings_resultats.json
python -B 3_Preuves_et_calculs/signal_v657/figure_signal.py
```

Dépendances : Python, mpmath ; NumPy/Matplotlib pour la figure. Les imports scientifiques du premier programme reprennent les fichiers de V645 et de recherche79 déjà présents. Aucun de ces fichiers anciens n’est modifié.

Le domaine scalaire est log2≤t≤log1000. Ce domaine était déjà certifié dans le document79 : aucun agrandissement n’est revendiqué. Les 44 cellules donnent maintenant une représentation adaptative et une borne de perte explicite. Les 45 évaluations de bords de cette exécution sont distinctes des 257 évaluations de la comparaison de grilles uniformes ; cette dernière est une expérience de comparaison séparée.

Le complément PDF et HTML est `1_Presentation/79_SIGNAL_COUPLAGES_ET_RESOLUTION`. Les deux notes de confrontation sont conservées dans ce dossier. La loi de signe sur l’axe non borné reste ouverte.

La subdivision du programme est plafonnée à20 niveaux ; les cellules non conclues sont signalées comme telles. La propriété théorique de terminaison suppose la possibilité de raffiner également les erreurs numériques et ne remplace pas cette garde d’arrêt.
