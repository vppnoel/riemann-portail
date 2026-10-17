# DARK-RESIDUAL — définition technique et protocole

Pour une compression finie DUAL-LOCK,

\[
M=M_\infty+M_q+M_{pole}+M_{loc}.
\]

Le vecteur \(v\) est le vecteur propre unitaire associé à \(\lambda_{min}(M)\). On pose

\[
q_i=v^TM_iv,\qquad
\eta=\frac{|\lambda_{min}|}{\sum_i|q_i|},\qquad A=1/\eta.
\]

`eta` est uniquement un indice de cancellation. Il n'est ni un critère de RH ni une probabilité.

## Garde-fous

- zéro interdit dans la construction ;
- décomposition définie avant diagonalisation ;
- fermeture numérique vérifiée : \(\lambda_{min}=\sum q_i\) ;
- sweep de quadrature ;
- contrôle positif apparié ;
- post-hoc seulement pour la comparaison aux zéros DH.

## Fichiers

- `src/dark_residual.py`
- `scripts/run_dark_residual.py`
- `tests/test_dark_residual.py`
- `data/dark_residual_cases.csv`
- `data/dark_residual_stability.csv`
- `data/dark_residual_summary.json`
- `data/dark_residual_amplification.png`
