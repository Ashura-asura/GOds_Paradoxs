import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from cl10_gamma_J import build_cl10_gammas, build_gamma_F, solve_charge_conjugation, N


def test_charge_conjugation_exists_and_is_unitary_both_signs():
    G = build_cl10_gammas()
    for sign in (+1, -1):
        C, resid, is_unitary, n_null = solve_charge_conjugation(G, sign)
        assert n_null == 1, f"expected 1-dim intertwiner space for sign={sign}, got {n_null}"
        assert resid < 1e-6
        assert is_unitary


def test_J_squared_is_scalar_and_matches_expected_epsilon():
    G = build_cl10_gammas()
    expected = {+1: -1, -1: +1}  # sign of intertwiner -> eps = J^2
    for sign in (+1, -1):
        C, resid, is_unitary, n_null = solve_charge_conjugation(G, sign)
        J2 = C @ C.conj()
        eps = J2[0, 0]
        assert np.allclose(J2, eps * np.eye(N), atol=1e-5)
        assert abs(eps.real - expected[sign]) < 1e-4
        assert abs(eps.imag) < 1e-4


def test_J_gamma_relation_is_minus_gamma_both_signs():
    G = build_cl10_gammas()
    Gamma_F = build_gamma_F(G)
    for sign in (+1, -1):
        C, resid, is_unitary, n_null = solve_charge_conjugation(G, sign)
        JGJinv = C @ Gamma_F.conj() @ np.linalg.inv(C)
        assert np.allclose(JGJinv, -Gamma_F, atol=1e-5)
