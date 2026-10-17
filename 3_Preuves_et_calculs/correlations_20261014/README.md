# Corrélations, identité et énergie - complément de recherche

Ouvrir CORRELATIONS_IDENTITE_ET_ENERGIE.html (formules MathML et visuel intégré),
ou la note Markdown. Le dossier distingue réduction classique, identités,
tests exacts, diagnostics et borne globale ouverte.

    python3 -m pip install -r requirements.txt
    python3 anchored_correlations.py --output results
    python3 figure_correlations.py

La réduction J(X)=O(X^2) vers RH est classique. La borne globale n'est pas
obtenue. L'identité sum_{d|n}Lambda(d)=log n donne le véritable logarithme
dérivé de zeta ; des profils arbitraires n'ont pas ce pont.
Le programme contient un profil unitaire à énergie globale bornée mais
signal hybride négatif, un modèle homométrique exact, et deux intégrations
indépendantes de l'énergie des vrais poids jusqu'à 1000.

Diagnostics mpmath70chiffres, recoupés indépendamment à85/90.
Noyau Mobius et profil unitaire certifiés dans le modèle mpmath.iv400bits.
Aucun zéro de zeta n'est utilisé par les programmes.

Les sources historiques 37 et45 du corpus citaient déjà Cramér/BPT et les
moyennes quadratiques A/B ; cette note reprend le fil, sans revendication
de percée. L'archive V6.53 antérieure reste le corpus consolidé ;
ce ZIP est un complément de travail avec son code et ses audits.
