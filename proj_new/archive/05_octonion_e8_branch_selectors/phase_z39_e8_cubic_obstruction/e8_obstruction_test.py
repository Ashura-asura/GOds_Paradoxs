"""
Obstruction test: does the E8 cubic-Casimir / d_ABC structure provide
vacuum-selection information that survives the Z21 Schur obstruction,
or does it reduce to the same flat-direction problem the project's own
Z15-Z18 flavon attempts already closed negative?

Setup: in the standard E8 -> E6 x SU(3)_f branching (already in this
project's phase_a2_e8_core.py), 248 = (78,1) + (1,8) + (27,3) + (27bar,3bar).
The three generations sit in the "3" of SU(3)_f. The E8 cubic Casimir
(the unique symmetric invariant d_ABC on 248) restricted to the (27,3)
sector is, in flavor space, built from the SU(3)_f-covariant object
epsilon_ijk (the only invariant tensor SU(3)_f has access to, since the
27's transform in the SAME "3", not "3 and 3bar").

Question: can any SU(3)_f-invariant scalar potential built ONLY from a
single flavor triplet v (the direction picked out by a 27-family "Higgs"
VEV) select a preferred direction in generation space, using this
cubic structure? Or is the cubic invariant identically zero for a
single triplet, leaving only |v|^2 (which is flat over the whole SU(3)_f
orbit -- i.e. picks a magnitude, never a direction)?
"""
import numpy as np
import itertools

def epsilon(i, j, k):
    perm = (i, j, k)
    if len(set(perm)) < 3:
        return 0
    # sign of permutation of (0,1,2)
    order = [0, 1, 2]
    inversions = sum(1 for a in range(3) for b in range(a+1, 3) if perm[a] > perm[b])
    return 1 if inversions % 2 == 0 else -1

def cubic_invariant(v):
    """epsilon_ijk v_i v_j v_k -- the ONLY SU(3) cubic invariant available
    to a single triplet (a 3, not a 3bar)."""
    total = 0
    for i, j, k in itertools.product(range(3), repeat=3):
        total += epsilon(i, j, k) * v[i] * v[j] * v[k]
    return total

# Test 1: is the single-triplet cubic invariant identically zero?
rng = np.random.default_rng(0)
max_val = 0.0
for _ in range(200):
    v = rng.normal(size=3) + 1j * rng.normal(size=3)
    val = cubic_invariant(v)
    max_val = max(max_val, abs(val))
print(f"Test 1 -- |epsilon_ijk v_i v_j v_k| over 200 random complex v: max = {max_val:.3e}")
print("  (should be exactly 0 -- antisymmetric tensor contracted with")
print("   totally symmetric v_i v_j v_k always vanishes)")

# Test 2: is any SU(3)-invariant built from a single triplet v flat
# over the SU(3) orbit (i.e. depends only on |v|^2, never on direction)?
# Directly check: apply a random SU(3) rotation to v, confirm every
# invariant built from v, v^dagger only (up to quartic order) is
# unchanged in value but v's *direction* has moved arbitrarily far.

def random_su3():
    # random unitary via QR of a random complex matrix, fixed to det=1
    Z = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    Q, R = np.linalg.qr(Z)
    Q = Q @ np.diag(np.diag(R) / np.abs(np.diag(R)))
    Q = Q / (np.linalg.det(Q) ** (1/3))
    return Q

v0 = rng.normal(size=3) + 1j * rng.normal(size=3)
norm0 = np.vdot(v0, v0).real
quartic0 = norm0 ** 2  # (v^dagger v)^2, the only quartic invariant of one triplet

directions_reached = []
for _ in range(5):
    U = random_su3()
    v_rot = U @ v0
    norm_rot = np.vdot(v_rot, v_rot).real
    quartic_rot = norm_rot ** 2
    cos_angle = abs(np.vdot(v0, v_rot)) / (np.sqrt(norm0) * np.sqrt(norm_rot))
    directions_reached.append(cos_angle)
    assert abs(norm_rot - norm0) < 1e-9
    assert abs(quartic_rot - quartic0) < 1e-9

print(f"\nTest 2 -- |v|^2 and (v^dagger v)^2 invariant under SU(3)_f rotation: PASS (machine precision)")
print(f"  overlap |<v0|v_rot>|/|v0||v_rot| for 5 random SU(3) rotations of v0:")
print(f"  {[f'{c:.3f}' for c in directions_reached]}")
print(f"  (values well below 1 confirm the rotations genuinely move the direction,")
print(f"   while both invariants above stay exactly fixed)")
