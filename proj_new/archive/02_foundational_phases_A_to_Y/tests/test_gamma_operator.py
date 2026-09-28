import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from cl10_gamma_J import build_cl10_gammas, build_gamma_F, N


def test_gamma_squares_to_identity():
    G = build_cl10_gammas()
    Gamma_F = build_gamma_F(G)
    assert np.allclose(Gamma_F @ Gamma_F, np.eye(N), atol=1e-8)


def test_gamma_is_hermitian():
    G = build_cl10_gammas()
    Gamma_F = build_gamma_F(G)
    assert np.allclose(Gamma_F, Gamma_F.conj().T, atol=1e-8)


def test_gamma_anticommutes_with_all_generators():
    G = build_cl10_gammas()
    Gamma_F = build_gamma_F(G)
    for a in range(10):
        assert np.allclose(Gamma_F @ G[a] + G[a] @ Gamma_F, np.zeros((N, N)), atol=1e-8)


def test_gamma_eigenvalue_split_is_16_16():
    G = build_cl10_gammas()
    Gamma_F = build_gamma_F(G)
    eigs = np.round(np.linalg.eigvalsh(Gamma_F), 6)
    assert int(np.sum(eigs > 0)) == 16
    assert int(np.sum(eigs < 0)) == 16


def test_gamma_matches_fermion_number_parity_up_to_phase():
    G = build_cl10_gammas()
    Gamma_F = build_gamma_F(G)
    ops = [(-G[2 * j] + 1j * G[2 * j + 1]) / 2 for j in range(5)]
    dops = [o.conj().T for o in ops]
    Nc = [d @ o for o, d in zip(ops, dops)]
    N_tot = sum(Nc)
    w, v = np.linalg.eigh(N_tot)
    parity = v @ np.diag(np.exp(1j * np.pi * np.round(w.real))) @ v.conj().T
    idxs = np.argwhere(np.abs(Gamma_F) > 1e-6)
    i0, j0 = idxs[0]
    phase = Gamma_F[i0, j0] / parity[i0, j0]
    assert abs(abs(phase) - 1) < 1e-6  # phase must be a pure phase
    assert np.allclose(Gamma_F, phase * parity, atol=1e-6)
