"""V6.36 : budget en norme et sous-espace négatif de la fenêtre DH fixée."""
from pathlib import Path
import json
import math
import sys
import time
import numpy as np
from scipy.linalg import toeplitz, eigh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from weil_trace_intervals import traces, I, upper, mp
from prime_generator import traces_from_primes, traces_from_zeros
from rejection import coeffs, log_derivative_coeffs
sys.path.insert(0, str(ROOT/"scripts"))
import run_prime_generator as RPG

DATA = ROOT/"data"
L = 1115
A = .02
H = .005


def safe_float(x):
    return float(np.nextafter(float(x), np.inf))


def trace_norm_bound(radii):
    L = len(radii)
    value = L*I(float(radii[0]))**2
    for k in range(1, L):
        value += 2*(L-k)*I(float(radii[k]))**2
    return safe_float(upper(mp.iv.sqrt(value)))


def negative_compression(G, vectors, epsilon):
    """Gershgorin avec budget gamma_2L pour les deux produits matriciels.

Le modèle d'arrondi IEEE binary64, sans débordement ni sous-flux significatif,
est une hypothèse explicitée dans la preuve. Les vecteurs sont des dyadiques
exactes ; aucun signe d'une valeur propre flottante n'est utilisé comme preuve.
"""
    L, k = vectors.shape
    u = I(2)**(-53)
    gamma = upper((2*L+2)*u/(1-(2*L+2)*u))
    gamma_float = safe_float(gamma)
    S = G@vectors
    B = vectors.T@S
    V = abs(vectors)
    # Produits positifs : leur borne relative permet de majorer les résultats
    # exacts à partir des produits flottants, sans annulation.
    P = abs(G)@V
    positive1 = V.T@abs(S)
    positive2 = V.T@P
    error = gamma_float*(positive1/(1-gamma_float)
                         +positive2/(1-gamma_float)**2)
    error = np.nextafter(error*(1+16*np.finfo(float).eps), np.inf)
    norms = [sum((I(float(v))**2 for v in vectors[:, j]), I(0))
             for j in range(k)]
    assert max(upper(v) for v in norms) < 2
    # |v_i^T E v_j| <= ||E||_2 ||v_i|| ||v_j|| <= 2 epsilon.
    error = np.nextafter(error+2*epsilon, np.inf)
    row_bounds = []
    for i in range(k):
        bound = I(float(B[i, i]))
        for j in range(k):
            bound += I(float(error[i, j]))
            if i != j:
                bound += abs(I(float(B[i, j])))
        row_bounds.append(safe_float(upper(bound)))
    return dict(dimension=k,gershgorin_superieur=max(row_bounds),
                erreur_entree_compression=float(error.max()),
                negatif=max(row_bounds)<0), B


def main():
    assert (DATA/"prevision_v636_norme.md").exists()
    start = time.perf_counter()
    t, radii, intervals, qerrors = traces(
        L, 60, lambda n,c,r: print(f"Trace {n}/{L-1}, rayon={r:.3e}",flush=True))
    epsilon = trace_norm_bound(radii)
    G = toeplitz(t)
    eigenvalues, vectors = eigh(G, check_finite=False)
    tolerance = 1e-11*max(abs(eigenvalues))
    numerical_count = int(np.sum(eigenvalues < -tolerance))
    checks = []
    accepted = None
    for k in range(25, 0, -1):
        check, _ = negative_compression(G, vectors[:, :k], epsilon)
        checks.append(check)
        if check["negatif"]:
            accepted = k
            break
    M = math.ceil(math.exp(L*H+2*A))+2
    old = traces_from_primes("DH",log_derivative_coeffs(coeffs("DH",M)),L-1,H,A).real
    zeros = traces_from_zeros(RPG.zeros("DH"),L-1,H,A).real
    old_delta = np.max(abs(old-t))
    discrepancy_norm = np.linalg.norm(toeplitz(old-t),ord="fro")
    zero_delta = np.max(abs(zeros-t))
    rep = dict(version="V6.36",objet="DH",a=A,h=H,L=L,
        precision_intervalles=60,quadrature_ordre=16,
        erreur_norme_traces=epsilon,rayon_trace_max=float(max(radii)),
        reste_quadrature_max=float(max(qerrors)),
        ecart_Fourier_physique_max=float(old_delta),
        ecart_Fourier_physique_Frobenius=float(discrepancy_norm),
        ecart_zeros_connus_max=float(zero_delta),
        compte_numerique=numerical_count,seuil_numerique=float(tolerance),
        valeurs_propres_40_premieres=eigenvalues[:40].tolist(),
        controles_compression=checks,negatives_certifiees_au_moins=accepted or 0,
        nombre_negatives_exact="non établi : les directions proches de zéro restent ambiguës",
        hypothese_arrondi="IEEE binary64, produits matriciels soumis au modèle gamma_(2L+2), sans débordement ni sous-flux significatif.",
        comparaison="Les écarts Fourier/physique et côté zéros sont mesurés, pas utilisés comme bornes de l'erreur exacte.",
        secondes=round(time.perf_counter()-start,2))
    if accepted:
        np.savez_compressed(DATA/"v636_temoin_negatif.npz",
                            traces=t,rayons=radii,vecteurs=vectors[:, :accepted])
    payload=dict(centres=t.tolist(),rayons=radii.tolist(),
                 intervalles_binaires=intervals,restes_quadrature=qerrors,
                 encodage="Chaque extrémité est le tuple mpmath (signe, mantisse, exposant binaire, nombre de bits), donc exacte.")
    (DATA/"v636_traces_intervalles.json").write_text(
        json.dumps(payload,ensure_ascii=False)+"\n",encoding="utf-8")
    (DATA/"v636_norme.json").write_text(
        json.dumps(rep,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(rep,ensure_ascii=False,indent=2),flush=True)


if __name__=="__main__":
    main()
