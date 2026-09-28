"""
Z44 Task 4 -- commutant / freedom counting, same methodology as Z21.

Z21 asked: what is the space of operators on the generation factor
that commute with every gauged SM/family generator? (Schur's Lemma,
solved directly by building the generators and finding the nullspace
of the commutator map via SVD, not by citing the lemma.) Z21's
answer, for SU(3)_f acting irreducibly on C^3: commutant dimension
exactly 1 (pure scalars) -- i.e. gauging SU(3)_f as a family group
pins the generation basis up to an overall phase, ZERO residual
rotation freedom among generations.

This script asks the identical question for the Z44 construction:
after breaking SU(5)_A -> SU(3)xSU(2)xU(1) and leaving SU(5)_B's
10bar block completely untouched (confirmed in z44_structure_check.py
to be a literal tensor factor), what is the commutant of the 12 SM
generators, acting as g_a (x) I_10 on the 50-dimensional (5_A,10bar_B)
piece? This is solved directly, the same way: build all 12 generators
numerically, vectorize the commutator condition, take the SVD
nullspace.
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
    return gens

def commutant_dimension(gens, dim_family):
    """
    Numerically compute dim_C of {T in Mat_{5*dim_family}(C) :
    [g (x) I_family, T] = 0 for all g in gens}, via SVD nullspace of
    the stacked (real-vectorized) commutator map -- identical method
    to Z21 (support/... commutant solver), just applied to a bigger
    generator set / bigger space.
    """
    base_dim = gens[0].shape[0]
    n = base_dim * dim_family
    I_family = np.eye(dim_family, dtype=complex)
    Gs = [np.kron(g, I_family) for g in gens]

    # Build the (complex) linear map L: T -> stack of [G_a, T], as a
    # matrix acting on vec(T) in C^{n^2}, then find nullspace via SVD
    # on the real embedding (stack real & imaginary parts).
    def commutator_matrix(G):
        In = np.eye(n, dtype=complex)
        # vec(GT - TG) = (I (x) G - G^T (x) I) vec(T)
        return np.kron(In, G) - np.kron(G.T, In)

    L_blocks = [commutator_matrix(G) for G in Gs]
    # Nullspace of the stacked matrix == nullspace of sum_a C_a^H C_a
    # (a Hermitian, positive-semidefinite Gram matrix) -- avoids ever
    # materializing the full stacked (12*n^2 x n^2) matrix, which OOMs
    # for n=50 (n^2=2500).
    A = np.zeros((n * n, n * n), dtype=complex)
    for C in L_blocks:
        A += C.conj().T @ C
    eigvals = np.linalg.eigvalsh(A)
    tol = 1e-9 * eigvals[-1] if eigvals[-1] > 0 else 1e-9
    null_dim = int(np.sum(eigvals < tol))
    return null_dim, n

if __name__ == "__main__":
    gens = sm_generators_on_5()

    # Z44 case: family block = 10bar_B, untouched, dim 10
    z44_null, z44_n = commutant_dimension(gens, dim_family=10)

    # Z21 comparison case, reproduced with this same solver: SU(3)_f
    # acting IRREDUCIBLY (not via a product embedding) on a 3-dim
    # generation factor with trivial SM action -- i.e. the commutant
    # of a single irreducible SU(3) fundamental. We reproduce this
    # here as a sanity cross-check of the solver itself: use the 8
    # Gell-Mann generators directly (irreducible on C^3), family
    # block dimension 1 (nothing tensored on) is the wrong comparison;
    # the correct Z21 reproduction is "commutant on C^3 alone" which
    # is generators-in-Mat_3, family_dim=1 trivial case restructured:
    su3_irred_gens = [g/2 for g in GELL_MANN]
    z21_null, z21_n = commutant_dimension(su3_irred_gens, dim_family=1)

    results = {
        "z21_reproduction": {
            "description": "Commutant of SU(3)_f acting irreducibly on C^3 (Schur's Lemma reproduction, cross-check of this solver against Z21's known result of exactly 1).",
            "commutant_complex_dimension": z21_null,
            "matches_Z21_known_result_of_1": z21_null == 1,
        },
        "z44_su5AxSu5B_after_breaking_su5A": {
            "description": "Commutant of the 12 SM generators (from broken SU(5)_A) acting as g(x)I_10 on the (5_A, 10bar_B) piece, family block dim 10, completely untouched.",
            "commutant_complex_dimension": z44_null,
            "ambient_space_dimension": z44_n,
        },
        "ratio_z44_over_z21": (z44_null / z21_null) if z21_null else None,
    }
    with open("results_z44_freedom_count.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
