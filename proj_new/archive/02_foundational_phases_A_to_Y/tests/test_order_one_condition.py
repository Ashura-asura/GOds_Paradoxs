"""
Central Phase Z2 result: for D_F built as a Kronecker-structured operator
on H_F = C^32 (x) C^3, and for generation-trivial gauge/J elements
a = alpha (x) I_3, JbJ^-1 = beta' (x) I_3 (alpha, beta' arbitrary 32x32
operators on the Cl(10) factor -- not restricted to any particular SM
subset), the order-one condition
    [[D_F, a], JbJ^-1]
acting on a single generation-pair block M_kl (x) E_kl reduces EXACTLY
to [[M_kl, alpha], beta'] (x) E_kl, with NO leakage into any other
generation-pair block. This is checked directly on the full 96x96
operators, not assumed from the tensor-product algebra alone (though
that algebra is exact and this is a consistency check of the code, not
a coincidence).
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'support'))
from cl10_gamma_J import build_cl10_gammas, solve_charge_conjugation
from z2_hilbert_space import (
    I3, E_kl, extend_to_HF, order_one_commutator, predicted_block_commutator,
    build_sm_generators_on_cl10,
)
from numpy import kron

rng = np.random.default_rng(1)


def _setup():
    G = build_cl10_gammas()
    gens = build_sm_generators_on_cl10(G)
    C_plus, _, _, _ = solve_charge_conjugation(G, +1)
    alpha = gens['Tx'] + 0.3 * gens['lam3']
    beta = gens['Y'] - 0.2 * gens['Tz']
    beta_prime = C_plus @ beta.conjugate() @ np.linalg.inv(C_plus)
    return alpha, beta_prime


def test_single_block_factorization_exact():
    alpha, beta_prime = _setup()
    M = rng.normal(size=(32, 32)) + 1j * rng.normal(size=(32, 32))
    for (k, l) in [(0, 0), (0, 1), (1, 2), (2, 2), (2, 0)]:
        D_F = kron(M, E_kl(k, l))
        a_HF = kron(alpha, I3)
        Jb_HF = kron(beta_prime, I3)
        full = order_one_commutator(D_F, a_HF, Jb_HF)
        predicted = kron(predicted_block_commutator(M, alpha, beta_prime), E_kl(k, l))
        assert np.abs(full - predicted).max() < 1e-8


def test_cross_block_zero_leakage():
    alpha, beta_prime = _setup()
    M1 = rng.normal(size=(32, 32)) + 1j * rng.normal(size=(32, 32))
    M2 = rng.normal(size=(32, 32)) + 1j * rng.normal(size=(32, 32))
    D_F_two = kron(M1, E_kl(0, 1)) + kron(M2, E_kl(1, 2))
    a_HF = kron(alpha, I3)
    Jb_HF = kron(beta_prime, I3)
    full = order_one_commutator(D_F_two, a_HF, Jb_HF)
    predicted = (
        kron(predicted_block_commutator(M1, alpha, beta_prime), E_kl(0, 1))
        + kron(predicted_block_commutator(M2, alpha, beta_prime), E_kl(1, 2))
    )
    assert np.abs(full - predicted).max() < 1e-8


def test_factorization_holds_for_both_KO_candidates():
    """Result must not depend on the still-open eps=+1 vs eps=-1 KO choice."""
    G = build_cl10_gammas()
    gens = build_sm_generators_on_cl10(G)
    alpha = gens['Tz']
    beta = gens['lam8']
    M = rng.normal(size=(32, 32)) + 1j * rng.normal(size=(32, 32))
    for sign in (+1, -1):
        C, _, _, _ = solve_charge_conjugation(G, sign)
        beta_prime = C @ beta.conjugate() @ np.linalg.inv(C)
        D_F = kron(M, E_kl(1, 1))
        a_HF = kron(alpha, I3)
        Jb_HF = kron(beta_prime, I3)
        full = order_one_commutator(D_F, a_HF, Jb_HF)
        predicted = kron(predicted_block_commutator(M, alpha, beta_prime), E_kl(1, 1))
        assert np.abs(full - predicted).max() < 1e-8
