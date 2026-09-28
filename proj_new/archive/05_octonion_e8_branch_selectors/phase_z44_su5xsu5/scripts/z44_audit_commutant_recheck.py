"""
Z44 adversarial audit -- items 4, 5, 10 (commutant, freedom counting,
numerical artifacts).
"""

import numpy as np
import json

GELL_MANN = [
    np.array([[0,1,0],[1,0,0],[0,0,0]], dtype=complex),
    np.array([[0,-1j,0],[1j,0,0],[0,0,0]], dtype=complex),
    np.array([[1,0,0],[0,-1,0],[0,0,0]], dtype=complex),
    np.array([[0,0,1],[0,0,0],[1,0,0]], dtype=complex),
    np.array([[0,0,-1j],[0,0,0],[1j,0,0]], dtype=complex),
    np.array([[0,0,0],[0,0,1],[0,1,0]], dtype=complex),
    np.array([[0,0,0],[0,0,-1j],[0,1j,0]], dtype=complex),
    (1/np.sqrt(3))*np.array([[1,0,0],[0,1,0],[0,0,-2]], dtype=complex),
]
PAULI = [
    np.array([[0,1],[1,0]], dtype=complex),
    np.array([[0,-1j],[1j,0]], dtype=complex),
    np.array([[1,0],[0,-1]], dtype=complex),
]

def embed_5x5(block3=None, block2=None):
    M = np.zeros((5,5), dtype=complex)
    if block3 is not None:
        M[0:3,0:3] = block3
    if block2 is not None:
        M[3:5,3:5] = block2
    return M

def sm_generators_on_5():
    gens = [embed_5x5(block3=g/2) for g in GELL_MANN]
    gens += [embed_5x5(block2=p/2) for p in PAULI]
    Y = np.diag([-1/3,-1/3,-1/3,1/2,1/2]).astype(complex)
    gens.append(Y)
    return gens  # 12

def su5_generators_5x5():
    n = 5
    gens = []
    for i in range(n):
        for j in range(i+1, n):
            s = np.zeros((n, n), dtype=complex); s[i, j] = 1; s[j, i] = 1
            gens.append(s)
            a = np.zeros((n, n), dtype=complex); a[i, j] = -1j; a[j, i] = 1j
            gens.append(a)
    for k in range(1, n):
        d = np.zeros((n, n), dtype=complex)
        for m in range(k):
            d[m, m] = 1
        d[k, k] = -k
        d = d / np.sqrt(k * (k + 1))
        gens.append(d)
    assert len(gens) == 24
    return gens

def induced_action_on_lambda2(G, n=5):
    basis = [(i, j) for i in range(n) for j in range(i+1, n)]
    idx = {p: k for k, p in enumerate(basis)}
    dim = len(basis)
    T = np.zeros((dim, dim), dtype=complex)
    for k, (i, j) in enumerate(basis):
        for m in range(n):
            if m == j:
                continue
            coeff = G[m, i]
            if coeff == 0:
                continue
            p, q = (m, j) if m < j else (j, m)
            sign = 1 if m < j else -1
            T[idx[(p, q)], k] += sign * coeff
        for m in range(n):
            if m == i:
                continue
            coeff = G[m, j]
            if coeff == 0:
                continue
            p, q = (i, m) if i < m else (m, i)
            sign = 1 if i < m else -1
            T[idx[(p, q)], k] += sign * coeff
    return T

def commutant_dimension_from_gens(full_gens, n):
    def commutator_matrix(G):
        In = np.eye(n, dtype=complex)
        return np.kron(In, G) - np.kron(G.T, In)
    A = np.zeros((n*n, n*n), dtype=complex)
    for G in full_gens:
        C = commutator_matrix(G)
        A += C.conj().T @ C
    eigvals = np.linalg.eigvalsh(A)
    return eigvals

if __name__ == "__main__":
    results = {}

    sm_gens = sm_generators_on_5()
    I10 = np.eye(10, dtype=complex)
    Gs_ungauged = [np.kron(g, I10) for g in sm_gens]
    eig_ungauged = commutant_dimension_from_gens(Gs_ungauged, n=50)
    eig_ungauged_sorted = np.sort(eig_ungauged)
    results["A_spectral_gap_original_z44"] = {
        "smallest_10_eigenvalues": eig_ungauged_sorted[:10].tolist(),
        "eigenvalue_at_rank_199": float(eig_ungauged_sorted[199]),
        "eigenvalue_at_rank_200": float(eig_ungauged_sorted[200]),
        "gap_ratio": float(eig_ungauged_sorted[200] / max(eig_ungauged_sorted[199], 1e-300)) if eig_ungauged_sorted[199] > 1e-12 else "undefined (rank 199 already ~0)",
        "null_dim_recount": int(np.sum(eig_ungauged_sorted < 1e-9 * eig_ungauged_sorted[-1])),
    }

    su5_gens_5x5 = su5_generators_5x5()
    su5_gens_on_10 = [induced_action_on_lambda2(G) for G in su5_gens_5x5]
    I5 = np.eye(5, dtype=complex)
    Gs_A = [np.kron(g, I10) for g in sm_gens]
    Gs_B = [np.kron(I5, h) for h in su5_gens_on_10]
    Gs_both = Gs_A + Gs_B
    eig_both = commutant_dimension_from_gens(Gs_both, n=50)
    eig_both_sorted = np.sort(eig_both)
    null_both = int(np.sum(eig_both_sorted < 1e-9 * eig_both_sorted[-1]))

    results["B_fair_comparison_both_factors_gauged"] = {
        "commutant_complex_dimension": null_both,
        "smallest_10_eigenvalues": eig_both_sorted[:10].tolist(),
        "hand_derivation_expected": 2,
        "matches_hand_derivation": null_both == 2,
    }

    with open("results_z44_audit_commutant_recheck.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
