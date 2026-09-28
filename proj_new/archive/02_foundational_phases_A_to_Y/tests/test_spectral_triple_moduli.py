"""
test_spectral_triple_moduli.py -- Phase Z1 support file

WHAT THIS DOES AND DOES NOT DO:
This does NOT construct a Cl(10)xE8 Dirac operator, J, or Gamma -- Phase
Z1's own finding is that those don't exist yet in this project (Phase A1
stops at the gamma-matrix/Witt-basis level). This file only verifies,
generically, the one piece of pure linear algebra Phase Z1's Task 3/4
argument rests on: that a solution set cut out by homogeneous linear
conditions can never be an isolated nonzero point. That fact needs no
physics-specific representation to check -- it holds for any linear
operator equation, which is exactly the point (order-one, reality, and
chirality conditions all have this shape, verified by hand-expansion in
PHASE_Z1_SPECTRAL_TRIPLE_MODULI_RESULT.md, Task 2).

This is a generic demonstration, not a Cl(10)xE8-specific result. It
should not be cited as computing dim(M_D)=6 or 3 -- Phase Z1 is explicit
that that specific number is L2 (argued), not L1 (independently
computed here).
"""

import numpy as np

print('=' * 72)
print('test_spectral_triple_moduli: generic homogeneous-linear-system check')
print('=' * 72)

rng = np.random.default_rng(0)

# --- Build a random set of homogeneous linear constraints on a matrix D ---
# Stand-in for "order-one condition" / "reality condition" / "chirality
# condition" -- each of those is, as shown in Task 2, a linear equation
# in D_F. Here D is flattened to a vector of unknowns and each constraint
# is a random linear functional set to zero, which is the generic shape
# of "[[D,a],JbJ^-1] = 0 for fixed a,b" once a,b are fixed matrices.
n = 6  # stand-in dimension (arbitrary, not tied to any physics number)
num_constraints = 4  # stand-in count, arbitrary

D_dim = n * n  # D is an n x n matrix, flattened
constraint_matrix = rng.normal(size=(num_constraints, D_dim))

# Solution space = nullspace of constraint_matrix
u, s, vt = np.linalg.svd(constraint_matrix)
tol = 1e-10
rank = np.sum(s > tol)
nullspace_dim = D_dim - rank

print(f'\nStand-in D is a {n}x{n} matrix ({D_dim} real unknowns).')
print(f'{num_constraints} random homogeneous linear constraints imposed.')
print(f'Constraint-matrix rank: {rank}')
print(f'Solution space dimension (nullspace): {nullspace_dim}')

assert nullspace_dim >= D_dim - num_constraints, "rank-nullity sanity check"

# --- The actual point: check whether a nonzero solution can be isolated ---
if nullspace_dim > 0:
    basis = vt[rank:]  # rows spanning the nullspace
    D0 = basis[0]
    assert not np.allclose(D0, 0), "picked a nonzero solution"
    for lam in (0.3, 1.0, 7.5, -2.2):
        Dlam = lam * D0
        residual = constraint_matrix @ Dlam
        assert np.allclose(residual, 0, atol=1e-8), \
            f"lambda={lam} should still satisfy every homogeneous constraint"
    print('\nConfirmed: every scalar multiple of a nonzero solution also')
    print('satisfies all constraints -- the solution set, if nontrivial,')
    print('is never an isolated point. This is Task 3/4\'s core claim,')
    print('shown here on a generic random system, not a Cl(10)xE8 one.')
else:
    print('\n(This random draw happened to force the trivial solution only --')
    print('rerun with a different seed; the general claim is about what')
    print('happens whenever a nonzero solution exists, per Task 2\'s proof')
    print('that the conditions are homogeneous, which holds regardless.)')

print('\n' + '=' * 72)
print('Result: generic linear-algebra fact confirmed on a stand-in system.')
print('Does NOT establish dim(M_D)=6 or 3 for Cl(10)xE8 specifically --')
print('see PHASE_Z1_SPECTRAL_TRIPLE_MODULI_RESULT.md Task 3 for the')
print('honest L1/L2 split on that separate claim.')
print('=' * 72)
