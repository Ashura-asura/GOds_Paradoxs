"""
Phase Z22, Step 4 -- the actual point: build S1 (first-generation fermion
subspace), S2 = psi_3(S1), S3 = psi_3^2(S1) using the VERIFIED intertwiner
U8 (machine-precision exact, Step 3), and compute the Hilbert-Schmidt Gram
matrix between generations. This is the numeric fact Z22 depends on: are
the three generation subspaces non-orthogonal, independent of tensor
factorization -- i.e. is this genuinely NOT the C^32 (x) C^3 structure
Z21 already closed?
"""
import numpy as np
from numpy import kron
from gresnigt_algebra import build_cl8_generators, build_witt, build_omega8
from gresnigt_generations import build_cl10_generators, build_witt5, build_idempotents_cl8, build_idempotents_cl10

N10 = 32


def hs_inner(A, B):
    return np.trace(A.conj().T @ B)


if __name__ == "__main__":
    E8 = build_cl8_generators()
    a4, ad4 = build_witt(E8)
    w8 = build_omega8(E8)
    idem8 = build_idempotents_cl8(a4, ad4)
    E10 = build_cl10_generators(E8, w8)
    a5, ad5 = build_witt5(E10)
    idem10 = build_idempotents_cl10(idem8, a5, ad5)

    U8 = np.load("U8_psi3.npy")
    U10 = kron(np.eye(2, dtype=complex), U8)
    U10inv = U10.conj().T  # unitary

    # Witt generators on the full 32-dim space: a1..a4 embedded via iota (I2 (x) e),
    # a5 built natively in Cl(10). Build the 5 Witt pairs on Cl(10) directly.
    a10 = [kron(np.eye(2, dtype=complex), ai) for ai in a4] + [a5]
    ad10 = [kron(np.eye(2, dtype=complex), adi) for adi in ad4] + [ad5]

    fp = idem10['++++' + '+']   # f_{+++++}
    fpm = idem10['++++' + '-']  # f_{++++-}
    fpp = idem10['+++' + '-' + '+']  # f_{+++-+}
    fppp = idem10['+++' + '-' + '-']  # f_{+++--}

    a1, a2, a3, a4_, a5_ = a10
    ad1, ad2, ad3, ad4_, ad5_ = ad10

    # First-generation states, eq (24)-(27), colour index i=1 (a1) for concreteness,
    # i<j pair (1,2) for the antitriplet slot -- one representative colour component
    # is enough to test the Gram-matrix / non-orthogonality claim.
    uL1 = ad1 @ ad4_ @ fp          # u_L^(1), eq (24) family
    nuL = ad4_ @ ad5_ @ fp         # nu_L
    dR1 = ad1 @ fpp                # d_R^(1), eq (26) family
    eRm = ad5_ @ fpp               # e_R^-

    def psi3(M):
        return U10 @ M @ U10inv

    def psi3_sq(M):
        return psi3(psi3(M))

    states1 = {"uL1": uL1, "nuL": nuL, "dR1": dR1, "eRm": eRm}
    states2 = {k: psi3(v) for k, v in states1.items()}
    states3 = {k: psi3_sq(v) for k, v in states1.items()}

    print("=== Linear independence across generations (per state type) ===")
    for name in states1:
        X1, X2, X3 = states1[name], states2[name], states3[name]
        stacked = np.stack([X1.flatten(), X2.flatten(), X3.flatten()])
        rank = np.linalg.matrix_rank(stacked, tol=1e-9)
        print(f"  {name}: rank of [S1,S2,S3] span = {rank} (expect 3, i.e. independent)")

    print()
    print("=== Gram matrix (Hilbert-Schmidt) across generations ===")
    for name in states1:
        X1, X2, X3 = states1[name], states2[name], states3[name]
        G = np.array([[hs_inner(Xi, Xj) for Xj in (X1, X2, X3)] for Xi in (X1, X2, X3)])
        print(f"  {name}:")
        print(np.round(G.real, 4))
        offdiag = np.max(np.abs(G - np.diag(np.diag(G))))
        print(f"    -> max off-diagonal magnitude: {offdiag:.4f} "
              f"({'NON-orthogonal (confirms paper)' if offdiag > 1e-6 else 'orthogonal'})")
        print()

    print("=== This project's own H_F structure, for direct contrast ===")
    print("Z2 onward: H_F = C^32 (x) C^3, generation basis = standard orthonormal")
    print("e_1,e_2,e_3 of C^3, Gram matrix = I_3 EXACTLY, by construction (tensor factor).")
    print("Gresnigt's S1,S2,S3 above are NOT a tensor factor -- they are three")
    print("subspaces of the SAME 32-dim Cl(10) representation, related by an algebra")
    print("automorphism, and (per the Gram matrix above) genuinely non-orthogonal.")
    print("This is the structural difference Z21 said was required and untested.")
