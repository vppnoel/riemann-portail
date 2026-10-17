# Relecture du Théorème A — résumé pour l'auteur (2026-10-10)

**Verdict : la preuve est correcte, et le dossier est prêt à partir après de petites corrections.**

**Vérifié.** Les deux sens de la preuve ont été refaits pas à pas : Mellin, puis Cauchy–Schwarz dyadique et prolongement analytique ; Perron aux demi-entiers, puis déplacement du contour jusqu'à Θ+ε/2. J'ai aussi vérifié L1, L3, L4 et L5, les cas Θ = ½ et Θ = 1, la convention log(1+Q), limsup contre lim, et les multiplicités. Contrôles numériques courts : L3, G(1), le coefficient 2 au premier zéro, Q jusqu'à 10⁷.

**Solide.** Je n'ai trouvé aucune erreur mathématique. Le double pôle ne sert pas pour A : il suffit d'un vrai pôle en chaque zéro, et c'est le signe + de q² + q′ qui le garantit (avec ζ″/ζ, il faudrait ζ″(ρ) ≠ 0). Le double pôle sert pour B.

**Fragile : la rédaction et la nouveauté, pas la preuve.**
- Le cercle de Cauchy sort de la région où la borne sur q est énoncée : il suffit d'énoncer F1 sur σ ≥ Θ+ε/4.
- Dans LEMMES_RIGOUREUX, les bornes (6.3)–(6.4) sont énoncées pour Θ+ε mais utilisées en Θ+ε/2.
- Il manque la référence exacte de Perron (Titchmarsh, lemme 3.12), avec ses hypothèses.
- A est l'analogue au second ordre, en moyenne quadratique, de la caractérisation classique de Θ par ψ(x) − x (Montgomery–Vaughan, ch. 13 et 15). Le sens RH ⇒ Q = X^{o(1)} découle presque de Banks–Sinha (Thm 1.1, k = 2). Je n'ai pas trouvé l'énoncé tel quel, mais un spécialiste y verra un exercice standard.

**À changer avant envoi.** Joindre RELECTURE_THEOREME_A_EN.md à la place de la section 3 du dossier v4.5. Corriger la phrase sur Brent–Platt–Trudgian : leur résultat porte sur ∫_X^{2X}(ψ−x)²dx, et le c·log X vient de Cramér et de Montgomery–Vaughan (Thm 13.6). Présenter A comme une proposition de méthode standard, sans revendiquer de nouveauté.

**Les 3 questions au relecteur.**
1. La majoration (Perron aux demi-entiers, contour avec G ≪ log²|t|) est-elle complète telle qu'écrite ?
2. A est-il une conséquence de routine des résultats classiques sur ψ(x) − x ? Existe-t-il une référence citable ?
3. Faut-il publier la forme limsup ou la forme « abscisse = Θ » ? Faut-il viser la limite, qui demanderait un théorème Ω localisé ?
