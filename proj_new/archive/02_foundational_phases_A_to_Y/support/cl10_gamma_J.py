"""
Phase Z2 core construction: Gamma_F and J_F on the 32-dim Cl(10) Fock space.

Imports the EXACT gamma-matrix construction from phases/phase_a1_cl10_core.py
(same octonion structure constants, same Weyl-representation recipe) so this
is provably the same Cl(10) representation the rest of the project uses.

Nothing here is fitted or hand-picked: Gamma_F is the standard Clifford
volume element i^5 * gamma_1...gamma_10; J_F's intertwiner C is the unique
(up to phase) solution of a linear system, found by SVD, not guessed.
"""
import numpy as np
from numpy import kron, eye, array
from functools import lru_cache

try:
    from qosc_division_connection import build_octonion_structure_constants
except ImportError:
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'support'))
    from qosc_division_connection import build_octonion_structure_constants

N = 32  # dim H_{Cl(10)}


def build_cl10_gammas():
    """Identical recipe to phases/phase_a1_cl10_core.py::build_cl10_gammas."""
    C, _, _, _ = build_octonion_structure_constants()
    s1 = array([[0, 1], [1, 0]], dtype=complex)
    s2 = array([[0, -1j], [1j, 0]], dtype=complex)
    s3 = array([[1, 0], [0, -1]], dtype=complex)
    I8 = eye(8, dtype=complex)
    I16 = eye(16, dtype=complex)
    G8 = [kron(s1, C[i]) for i in range(1, 8)] + [1j * kron(s2, I8)]
    return [kron(G8[i], s3) for i in range(8)] + [
        kron(I16, 1j * array([[0, 1], [1, 0]], dtype=complex)),
        kron(I16, 1j * array([[0, -1j], [1j, 0]], dtype=complex)),
    ]


def build_gamma_F(G):
    """Chirality/grading operator: Gamma_F = i^5 * gamma_1 ... gamma_10."""
    Gamma_F = (1j ** 5) * G[0]
    for a in range(1, 10):
        Gamma_F = Gamma_F @ G[a]
    return Gamma_F


_solve_cache = {}


def solve_charge_conjugation(G, sign):
    if sign in _solve_cache:
        return _solve_cache[sign]
    result = _solve_charge_conjugation_uncached(G, sign)
    _solve_cache[sign] = result
    return result


def _solve_charge_conjugation_uncached(G, sign):
    """
    Solve for unitary C (up to overall phase) satisfying
        C @ G[a] == sign * conj(G[a]) @ C     for all a = 0..9.
    Built as the exact linear operator on Mat_32(C) (not via a kron/vec
    shortcut, to avoid convention bugs), then take its 1-dim nullspace.
    Returns (C, residual, is_unitary).
    """
    ncols = N * N
    M = np.zeros((10 * N * N, ncols), dtype=complex)
    for k in range(ncols):
        i, j = divmod(k, N)
        E = np.zeros((N, N), dtype=complex)
        E[i, j] = 1.0
        out = np.concatenate([(E @ G[a] - sign * G[a].conj() @ E).flatten() for a in range(10)])
        M[:, k] = out
    u, s, vh = np.linalg.svd(M)
    n_null = int(np.sum(s < 1e-8 * s[0]))
    nv = vh[-1, :].conj()
    C = nv.reshape(N, N)
    C = C / np.linalg.norm(C) * np.sqrt(N)
    idx = np.unravel_index(np.argmax(np.abs(C)), C.shape)
    C = C / (C[idx] / np.abs(C[idx]))  # fix overall phase for reproducibility
    resid = max(np.abs(C @ G[a] - sign * G[a].conj() @ C).max() for a in range(10))
    is_unitary = np.allclose(C @ C.conj().T, eye(N), atol=1e-5)
    return C, resid, is_unitary, n_null
