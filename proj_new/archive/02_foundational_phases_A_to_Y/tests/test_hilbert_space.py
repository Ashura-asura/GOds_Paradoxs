import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from cl10_gamma_J import build_cl10_gammas
from z2_hilbert_space import (
    N_CL, N_GEN, build_generation_basis, build_su3f_generators,
    build_sm_generators_on_cl10, extend_to_HF,
)


def test_generation_basis_orthonormal():
    basis = build_generation_basis()
    for i in range(3):
        for j in range(3):
            expected = 1.0 if i == j else 0.0
            assert np.allclose(basis[i] @ basis[j].conj(), expected, atol=1e-10)


def test_su3f_generators_hermitian_traceless():
    gens = build_su3f_generators()
    assert len(gens) == 8
    for g in gens:
        assert np.allclose(g, g.conj().T, atol=1e-10)
        assert abs(np.trace(g)) < 1e-10


def test_su3f_algebra_closes():
    T1, T2, T3 = build_su3f_generators()[:3]
    assert np.allclose(T1 @ T2 - T2 @ T1, 1j * T3, atol=1e-10)


def test_HF_dimension_is_96():
    assert N_CL * N_GEN == 96


def test_sm_generators_hermitian():
    G = build_cl10_gammas()
    gens = build_sm_generators_on_cl10(G)
    assert len(gens) == 6
    for v in gens.values():
        assert np.allclose(v, v.conj().T, atol=1e-8)


def test_su2L_algebra_on_HF():
    G = build_cl10_gammas()
    gens = build_sm_generators_on_cl10(G)
    Tx_HF = extend_to_HF(gens['Tx'])
    Ty_HF = extend_to_HF(gens['Ty'])
    Tz_HF = extend_to_HF(gens['Tz'])
    assert np.allclose(Tx_HF @ Ty_HF - Ty_HF @ Tx_HF, 1j * Tz_HF, atol=1e-8)
    assert Tx_HF.shape == (96, 96)
