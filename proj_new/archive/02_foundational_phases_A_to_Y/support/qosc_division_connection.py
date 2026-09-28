"""
Octonion structure constants and division algebra connection.
Provides left/right multiplication matrices for the octonion algebra.
"""
import numpy as np

def build_octonion_structure_constants():
    """
    Build the octonion structure constants using the Fano plane convention.

    Fano plane lines (cyclic order, with anticommutation):
    1->2->4->1: e1*e2=e4, e2*e4=e1, e4*e1=e2  (and reversed = negative)
    2->3->5->2
    3->4->6->3
    4->5->7->4
    5->6->1->5
    6->7->2->6
    7->1->3->7

    Returns:
        C_struct: list of 8 left-multiplication matrices L_i (8x8)
        R_struct: list of 8 right-multiplication matrices R_i (8x8)
        f_ijk: 8x8x8 structure constants tensor
        mult_table: 8x8 multiplication table
    """
    f = np.zeros((8, 8, 8), dtype=np.float64)

    # Identity: e_0 * e_i = e_i * e_0 = e_i
    for i in range(8):
        f[0, i, i] = 1.0
        f[i, 0, i] = 1.0

    # e_i * e_i = -e_0 for i=1..7
    for i in range(1, 8):
        f[i, i, 0] = -1.0

    # Fano plane lines (each defines 6 entries: 3 positive cyclic, 3 negative reverse)
    lines = [
        (1, 2, 4),
        (2, 3, 5),
        (3, 4, 6),
        (4, 5, 7),
        (5, 6, 1),
        (6, 7, 2),
        (7, 1, 3),
    ]

    for a, b, c in lines:
        # e_a * e_b = e_c
        f[a, b, c] = 1.0
        # e_b * e_c = e_a
        f[b, c, a] = 1.0
        # e_c * e_a = e_b
        f[c, a, b] = 1.0
        # e_b * e_a = -e_c (anticommutation)
        f[b, a, c] = -1.0
        # e_c * e_b = -e_a
        f[c, b, a] = -1.0
        # e_a * e_c = -e_b
        f[a, c, b] = -1.0

    # Build left multiplication matrices L_i (8x8)
    # L_i(e_j) = e_i * e_j = sum_k f[i][j][k] e_k
    # (L_i)_{kj} = f[i][j][k]
    C_struct = []
    for i in range(8):
        L = np.zeros((8, 8), dtype=np.float64)
        for j in range(8):
            for k in range(8):
                L[k, j] = f[i, j, k]
        C_struct.append(L)

    # Build right multiplication matrices R_i (8x8)
    # R_i(e_j) = e_j * e_i = sum_k f[j][i][k] e_k
    # (R_i)_{kj} = f[j][i][k]
    R_struct = []
    for i in range(8):
        R = np.zeros((8, 8), dtype=np.float64)
        for j in range(8):
            for k in range(8):
                R[k, j] = f[j, i, k]
        R_struct.append(R)

    # Build multiplication table
    mult_table = np.zeros((8, 8), dtype=np.int64)
    for i in range(8):
        for j in range(8):
            for k in range(8):
                if abs(f[i, j, k]) > 0.5:
                    sign = int(np.sign(f[i, j, k]))
                    mult_table[i, j] = sign * k
                    break

    return C_struct, R_struct, f, mult_table
