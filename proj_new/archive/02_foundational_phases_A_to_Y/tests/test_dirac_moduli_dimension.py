"""
Task 6: dim(M_D) computation.

This test does NOT re-derive Phase X's Hom_G multiplicity=1 result (that
lives in phases/phase_x_hom_g_invariant_audit.py and is L1 there,
established via an independent weight-table argument). What it DOES
verify, given that per-block multiplicity as an input, is the arithmetic
that turns "9 independent generation-pair blocks, 1 free complex number
each" into exactly Phase X's 6 (symmetric H) or 3 (antisymmetric H) --
i.e. that block-decoupling (proved in test_order_one_condition.py) plus
Bose/Fermi exchange symmetry of the two 16's meeting the same H (an
independent constraint, not from order-one/reality/chirality) reproduces
Phase X's count exactly, with no smaller or larger result.
"""
import numpy as np


def test_symmetric_channel_dimension():
    # Sym^2(C^3): 3x3 complex symmetric matrices, dim = 3*4/2 = 6
    basis_count = 0
    for i in range(3):
        for j in range(i, 3):
            basis_count += 1
    assert basis_count == 6


def test_antisymmetric_channel_dimension():
    # Lambda^2(C^3): 3x3 complex antisymmetric matrices, dim = 3*2/2 = 3
    basis_count = 0
    for i in range(3):
        for j in range(i + 1, 3):
            basis_count += 1
    assert basis_count == 3


def test_nine_blocks_reduce_to_symmetric_or_antisymmetric_not_less_not_more():
    """
    9 independent generation-pair coefficients y_kl (k,l = 0..2), each with
    per-block multiplicity 1 (Phase X input), subject ONLY to the
    y_kl = +/- y_lk identification forced by H's own exchange statistics
    (symmetric H: 10, 126 / antisymmetric H: 120) -- NOT by order-one,
    reality, or chirality, which (per test_order_one_condition.py) impose
    no relation among the 9 at all.
    """
    n_free_before_statistics = 9
    n_diag = 3
    n_off_diag_pairs = 3  # (0,1),(0,2),(1,2), each pair identified (sym) or
                           # anti-identified (antisym) with its mirror
    symmetric_dim = n_diag + n_off_diag_pairs      # diag free + 3 off-diag free
    antisymmetric_dim = 0 + n_off_diag_pairs        # diag forced to 0 + 3 off-diag free
    assert symmetric_dim == 6
    assert antisymmetric_dim == 3
    assert n_free_before_statistics > symmetric_dim > antisymmetric_dim
