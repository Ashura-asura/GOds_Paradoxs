"""
Phase Z22, Step 2 — psi_3 automorphism, Cl(10) extension, primitive
idempotents, and the three generation subspaces S1, S2, S3.

Continues gresnigt_algebra.py. Builds eq (4)-(41) of arXiv:2604.24795.
"""
import numpy as np
from numpy import kron, eye
from gresnigt_algebra import build_cl8_generators, build_witt, build_omega8, s1, s2, s3, I2, kron4

N8 = 16
N10 = 32


def build_idempotents_cl8(a, ad):
    """pi_j^(+) = a_j ad_j, pi_j^(-) = ad_j a_j ; primitive idempotents f_eps (eq 4-5)."""
    pi_plus = [a[j] @ ad[j] for j in range(4)]
    pi_minus = [ad[j] @ a[j] for j in range(4)]

    def pi(j, eps):
        return pi_plus[j] if eps == '+' else pi_minus[j]

    idem = {}
    for e1 in '+-':
        for e2 in '+-':
            for e3 in '+-':
                for e4 in '+-':
                    f = pi(0, e1) @ pi(1, e2) @ pi(2, e3) @ pi(3, e4)
                    idem[e1 + e2 + e3 + e4] = f
    return idem


def check_idempotents(idem, tol=1e-9):
    N = list(idem.values())[0].shape[0]
    total = np.zeros((N, N), dtype=complex)
    max_offdiag = 0.0
    keys = list(idem.keys())
    for k in keys:
        total += idem[k]
    for i, ki in enumerate(keys):
        for kj in keys[i + 1:]:
            max_offdiag = max(max_offdiag, np.max(np.abs(idem[ki] @ idem[kj])))
    err_complete = np.max(np.abs(total - np.eye(N)))
    return err_complete, max_offdiag


# ---- Cl(10) extension, eq (13)-(14) ----
def build_cl10_generators(E8, w8):
    sb1 = np.array([[0, 1], [1, 0]], dtype=complex)
    sb2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
    E10 = [kron(I2, e) for e in E8]  # iota(e_i) = I2 (x) e_i, i=1..8
    e9 = -1j * kron(sb1, w8)
    e10 = 1j * kron(sb2, w8)
    E10 = E10 + [e9, e10]
    return E10


def build_witt5(E10):
    a5 = 0.5 * (-E10[8] + 1j * E10[9])
    ad5 = 0.5 * (E10[8] + 1j * E10[9])
    return a5, ad5


def build_idempotents_cl10(idem8, a5, ad5):
    pi5p = a5 @ ad5
    pi5m = ad5 @ a5
    idem10 = {}
    for k8, f8 in idem8.items():
        f8_ext = kron(np.eye(2, dtype=complex), f8)
        idem10[k8 + '+'] = f8_ext @ pi5p
        idem10[k8 + '-'] = f8_ext @ pi5m
    return idem10


# ---- psi_3 automorphism on Cl(8), eq (9)-(11) ----
def build_psi3_images(E8):
    e = E8  # e[0]=e1 ... e[7]=e8
    e8_op = e[7]

    def prod(*idxs):
        m = np.eye(N8, dtype=complex)
        for i in idxs:
            m = m @ e[i - 1]
        return m

    g = [None] * 7  # g[0..6] correspond to g1..g7
    g[0] = 0.5 * e[0] @ e8_op @ (-prod(2, 3, 4, 5) + prod(2, 3, 6, 7) + prod(4, 5, 6, 7) - np.eye(N8, dtype=complex))
    g[1] = 0.5 * e[1] @ e8_op @ (prod(1, 3, 4, 6) + prod(1, 3, 5, 7) + prod(4, 5, 6, 7) - np.eye(N8, dtype=complex))
    g[2] = 0.5 * e[2] @ e8_op @ (prod(1, 2, 5, 6) - prod(1, 2, 4, 7) + prod(4, 5, 6, 7) - np.eye(N8, dtype=complex))
    g[3] = 0.5 * e[3] @ e8_op @ (prod(1, 2, 5, 6) + prod(1, 3, 5, 7) + prod(2, 3, 6, 7) - np.eye(N8, dtype=complex))
    g[4] = 0.5 * e[4] @ e8_op @ (-prod(1, 2, 4, 7) + prod(1, 3, 4, 6) + prod(2, 3, 6, 7) - np.eye(N8, dtype=complex))
    g[5] = 0.5 * e[5] @ e8_op @ (-prod(1, 2, 4, 7) + prod(1, 3, 5, 7) - prod(2, 3, 4, 5) - np.eye(N8, dtype=complex))
    g[6] = 0.5 * e[6] @ e8_op @ (prod(1, 2, 5, 6) + prod(1, 3, 4, 6) - prod(2, 3, 4, 5) - np.eye(N8, dtype=complex))

    psi3_e = []
    for i in range(7):
        psi3_e.append(0.25 * e[i] + (np.sqrt(3) / 4) * g[i]
                       - (np.sqrt(3) / 4) * (e[i] @ e8_op) - 0.75 * (g[i] @ e8_op))
    psi3_e.append(e8_op.copy())  # psi_3: e8 -> e8
    return psi3_e


def apply_psi3_to_matrix(M_in_e_basis_builder, psi3_e, E8):
    """Given a function that builds a target Cl(8) element as a polynomial in
    e_1..e_8 (symbolically via callback), this isn't generic -- instead we
    directly conjugate-free-map basis monomials. For our purposes we only need
    psi_3 applied to specific short products, done by direct substitution
    below in the test script, not via this generic helper."""
    raise NotImplementedError("apply psi3 to specific monomials directly; see test script")


if __name__ == "__main__":
    E8 = build_cl8_generators()
    a4, ad4 = build_witt(E8)
    w8 = build_omega8(E8)
    idem8 = build_idempotents_cl8(a4, ad4)
    err_complete, max_offdiag = check_idempotents(idem8)
    print(f"[Check] Cl(8) primitive idempotents: sum=I error {err_complete:.3e}, "
          f"max pairwise product (orthogonality) {max_offdiag:.3e}")

    E10 = build_cl10_generators(E8, w8)
    a5, ad5 = build_witt5(E10)
    idem10 = build_idempotents_cl10(idem8, a5, ad5)
    err_complete10, max_offdiag10 = check_idempotents(idem10)
    print(f"[Check] Cl(10) primitive idempotents (32-dim): sum=I error {err_complete10:.3e}, "
          f"max pairwise product {max_offdiag10:.3e}")

    # spot-check against paper's eq (7),(18): f_{++++} = E_{1,1}
    fpppp = idem8['++++']
    E11 = np.zeros((16, 16), dtype=complex)
    E11[0, 0] = 1.0
    print(f"[Check] f_++++ == E_1,1 in Cl(8)? max err = {np.max(np.abs(fpppp - E11)):.3e}")

    psi3_e = build_psi3_images(E8)
    # check psi_3^3 = Id on generators e1..e8
    def apply_seq(vec_list, mats):
        return [mats[i] for i in range(len(mats))]

    # compose psi3 with itself symbolically is hard without full algebra map;
    # instead verify psi3 is an automorphism on generators: check e_i images
    # satisfy same anticommutation relations (a necessary automorphism check)
    max_err_auto = 0.0
    Iden = np.eye(N8, dtype=complex)
    for i in range(8):
        for j in range(8):
            target = -2 * Iden if i == j else np.zeros((N8, N8), dtype=complex)
            anticomm = psi3_e[i] @ psi3_e[j] + psi3_e[j] @ psi3_e[i]
            max_err_auto = max(max_err_auto, np.max(np.abs(anticomm - target)))
    print(f"[Check] psi_3(e_i) satisfy SAME Clifford algebra as e_i (automorphism necessary condition): "
          f"max err = {max_err_auto:.3e}")
