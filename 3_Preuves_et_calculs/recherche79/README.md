# Document 79 : compensation arithmétique, profils et obstructions

Ouvrir 79_COMPENSATION_PROFILS_ET_OBSTRUCTIONS.pdf (9 pages) ou la version HTML
autonome, avec formules MathML. Le source LaTeX et la note Markdown sont fournis.

Cette passe établit des lemmes auxiliaires et teste une règle de compensation
au plafond EXISTANT q<=1000. Elle ne démontre pas RH ni la loi de signe globale.

Résultat concret : avec support/masse/premier moment seulement, la garde échoue
sur les 9 grands blocs. Avec 8 parties logarithmiques par bloc, les 53 gardes
non vides sont positives dans le certificat par intervalles déclaré.
Une proposition asymptotique montre pourquoi une subdivision fixe ne peut
servir de certificat global. Un contre-modèle exact ferme l'inversion positive
générique de la couche Selberg, même avec le réservoir exponentiel exact.

Reproduction depuis ce dossier :

    python3 -m pip install -r requirements.txt
    python3 compensation_blocks.py --cutoff 1000 --digits 60 --output results
    python3 certify_block_guards.py --corpus mini_corpus --output results/block_guard_certificate.json
    python3 verify_countermodels.py --output results/countermodels_exact.json
    python3 figure_compensation.py

Les deux premiers programmes exigent mpmath. Le contre-modèle rationnel utilise
seulement la bibliothèque standard. matplotlib sert uniquement au visuel.
Le solveur utilise une précision diagnostique explicitement séparée des
intervalles 400 bits. Les données à 75 chiffres et l'audit indépendant sont
fournis. Aucun zéro de zêta n'est utilisé.

Correctif des trois scripts hérités du document 78 : convertir la borne
rationnelle inférieure d'Euler via un intervalle dirigé avant de la transmettre
au constructeur binaire. Cela corrige le témoin formel d'arrondi ; les signes
et conclusions antérieurs restent identiques dans les replays fournis.
Les versions corrigées sont dans correctifs78 ; les nouveaux certificats sont
results/corrected78_*.json. La note historique reste conservée dans le corpus.

Prochaine obligation : une estimation indépendante du profil intérieur des
vrais poids premiers, assez précise pour contrôler le reste signé à toutes
les échelles. La demander directement positive reformulerait RH.
