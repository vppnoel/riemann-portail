# Horodatage des versions

Preuve d'antériorité sans publication : chaque version livrée est datée par un tiers, sans que son contenu sorte du dépôt privé.

1. **À chaque livraison**, après la mise à jour de `CHECKSUMS.sha256` : `python -B 2_Methode/Horodatage/horodater_version.py`. Le script fige `CHECKSUMS_<version>.sha256` (empreintes de tous les fichiers de la version) et l'inscrit dans `registre_horodatages.json`. Ensuite, regénérer `CHECKSUMS.sha256` et envoyer sur GitHub.
2. **Sur GitHub**, le flux `horodater` envoie l'empreinte de cette copie aux calendriers [OpenTimestamps](https://opentimestamps.org) et dépose la preuve `CHECKSUMS_<version>.sha256.ots`. Chaque jour, il complète les preuves en attente jusqu'à leur ancrage dans la chaîne Bitcoin (quelques heures). Seule l'empreinte part ; le contenu reste privé.
3. **Aux moments importants** (avant d'envoyer les articles à un spécialiste, avant une pré-publication) : une [e-Soleau à l'INPI](https://procedures.inpi.fr/?/), à faire par l'auteur. L'inscrire ensuite dans `registre_horodatages.json`, liste `esoleau` (date, numéro, pièces déposées).

**Vérifier une preuve :** `ots verify CHECKSUMS_<version>.sha256.ots`, puis `sha256sum -c CHECKSUMS_<version>.sha256` dans une archive de la version. Les fichiers `.ots` évoluent après leur dépôt (complétion) ; ils sont donc exclus des sommes de contrôle et de l'empreinte des vues.

*Auteur et titulaire des droits : Vincent NOËL.*
