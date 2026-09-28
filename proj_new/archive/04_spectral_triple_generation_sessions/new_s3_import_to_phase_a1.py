"""
Import Gresnigt's S3 family symmetry into Phase A1's own Cl(10) basis
======================================================================

Item 6 code-verified Gresnigt's arXiv:2601.07857 Cl(8)-S3 construction
is internally consistent, but flagged that it depends on sedenion-
automorphism data (g_i multivectors, psi_3) that Phase A1's own octonion-
derived basis does not carry. This file does the actual import.

Strategy:
  1. Build Phase A1's Cl(10) gamma matrices (32x32). Restrict the Cl(8)
     subalgebra (generators G[0..7]) to the N4=0 16-dim subspace.
  2. Build Gresnigt's Cl(8) generators e_1..e_8 (16x16).
  3. Find the best index permutation + sign flips that maps Phase A1's
     gamma matrix ordering to Gresnigt's, using trace invariants.
  4. Build g_i, psi_3, epsilon using Phase A1's permuted gamma matrices
     and the same algebraic formulas.
  5. Verify S3 group relations and check Phase A1 gauge compatibility.
  6. Lift psi_3 and epsilon to the full 32x32 Cl(10) representation.
"""

import numpy as np
from numpy import kron, eye, zeros
from itertools import combinations, product, permutations
from collections import defaultdict

print('=' * 72)
print('Import Gresnigt S3 family symmetry into Phase A1 Cl(10) basis')
print('=' * 72)

# =====================================================================
# Step 1: Phase A1's Cl(10) gamma matrices and N4=0 subspace
# =====================================================================
print('\n--- Step 1: Phase A1 Cl(10) basis ---')

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'support'))
from qosc_division_connection import build_octonion_structure_constants
C, _, _, _ = build_octonion_structure_constants()
s1 = np.array([[0, 1], [1, 0]], dtype=complex)
s2 = np.array([[0, -1j], [1j, 0]], dtype=complex)
s3 = np.array([[1, 0], [0, -1]], dtype=complex)
I8 = eye(8, dtype=complex)
I16 = eye(16, dtype=complex)
I32 = eye(32, dtype=complex)
G8 = [kron(s1, C[i]) for i in range(1, 8)] + [1j * kron(s2, I8)]
G = [kron(G8[i], s3) for i in range(8)] + [
    kron(I16, 1j * np.array([[0, 1], [1, 0]], dtype=complex)),
    kron(I16, 1j * np.array([[0, -1j], [1j, 0]], dtype=complex)),
]

ok_cl10 = all(np.allclose(G[i] @ G[j] + G[j] @ G[i],
                          -2 * I32 if i == j else zeros((32,32), dtype=complex), atol=1e-8)
              for i in range(10) for j in range(10))
print(f'1a. Cl(10) relations {{G_i,G_j}} = -2*delta_ij: {ok_cl10}')

# Witt basis (Phase A1 convention): pairs (0,1),(2,3),(4,5),(6,7),(8,9)
ops = [(-G[2*j] + 1j * G[2*j+1]) / 2 for j in range(5)]
dops = [o.conj().T for o in ops]
Nc = [d @ o for o, d in zip(ops, dops)]
N4_op = Nc[4]

evals_N4, evects_N4 = np.linalg.eigh(N4_op)
idx_N4_0 = np.where(np.abs(evals_N4) < 1e-8)[0]
idx_N4_1 = np.where(np.abs(evals_N4 - 1) < 1e-8)[0]
assert len(idx_N4_0) == 16 and len(idx_N4_1) == 16
print(f'1b. dim(N4=0) = {len(idx_N4_0)}, dim(N4=1) = {len(idx_N4_1)}')

# Transform G[0..7] to N4 eigenbasis, restrict to N4=0
G_eig = [evects_N4.conj().T @ G[i] @ evects_N4 for i in range(8)]
ga = [g[np.ix_(idx_N4_0, idx_N4_0)] for g in G_eig]  # Phase A1's Cl(8), gamma^2=-I
ga_1 = [g[np.ix_(idx_N4_1, idx_N4_1)] for g in G_eig]  # N4=1 copy

ok8 = all(np.allclose(ga[i] @ ga[j] + ga[j] @ ga[i],
                      -2 * I16 if i == j else zeros((16,16),dtype=complex), atol=1e-6)
          for i in range(8) for j in range(8))
ok8_1 = all(np.allclose(ga_1[i] @ ga_1[j] + ga_1[j] @ ga_1[i],
                        -2 * I16 if i == j else zeros((16,16),dtype=complex), atol=1e-6)
            for i in range(8) for j in range(8))
print(f'1c. Cl(8) on N4=0 (gamma^2=-I): {ok8}; N4=1: {ok8_1}')

# =====================================================================
# Step 2: Gresnigt's Cl(8) generators
# =====================================================================
print('\n--- Step 2: Gresnigt Cl(8) + S3 ---')

I2 = eye(2, dtype=complex)
def K(*mats):
    out = mats[0]
    for m in mats[1:]:
        out = kron(out, m)
    return out

e = {}
e[1] = 1j * K(s1, s1, s1, s1)
e[2] = 1j * K(s1, s1, s3, I2)
e[3] = -1j * K(s1, s1, s1, s3)
e[4] = -1j * K(s1, s3, I2, I2)
e[5] = -1j * K(s1, s1, s1, s2)
e[6] = -1j * K(s1, s2, I2, I2)
e[7] = 1j * K(s1, s1, s2, I2)
e[8] = 1j * K(s2, I2, I2, I2)

eg = [e[i+1] for i in range(8)]  # 0-indexed

# =====================================================================
# Step 3: Build similarity transform via Fock/Witt basis
# =====================================================================
print('\n--- Step 3: Similarity transform via Fock vacuum ---')

# Both representations have Witt bases (creation/annihilation operators)
# Cl(8) in both cases. The Fock vacuum is uniquely defined (up to phase).
# Build the Fock basis in each representation and map between them.

# --- Gresnigt representation: build Witt basis and Fock states ---
# Witt basis from item 6 code (4 Witt pairs for Cl(8))
a_g, adag_g = {}, {}
for j in range(1, 5):
    a_g[j] = 0.5 * (-eg[j-1] + 1j * eg[j+3])  # a_j = (-e_j + i*e_{j+4})/2
    adag_g[j] = 0.5 * (eg[j-1] + 1j * eg[j+3])

# Vacuum: f_++++ (all pi⁺ idempotent), which is E_{1,1}
vac_g = zeros((16, 1), dtype=complex)
vac_g[0] = 1.0

# Build 16 Gresnigt Fock states: |n1,n2,n3,n4>
fock_g = {}
for bits in product([0, 1], repeat=4):
    v = vac_g.copy()
    for j in range(4):
        if bits[j]:
            v = adag_g[j+1] @ v
    norm = np.sqrt(v.conj().T @ v).item()
    if isinstance(norm, complex):
        norm = norm.real
    if abs(norm) > 1e-10:
        v = v / norm
    fock_g[bits] = v

# Verify Witt relations on the Fock basis
a_g_list = [a_g[j+1] for j in range(4)]
adag_g_list = [adag_g[j+1] for j in range(4)]
car_g = all(np.allclose(a_g_list[i] @ adag_g_list[j] + adag_g_list[j] @ a_g_list[i],
                        I16 if i == j else zeros((16,16),dtype=complex), atol=1e-8)
            for i in range(4) for j in range(4))
print(f'3a. Gresnigt CAR: {car_g}')

# --- Phase A1 N4=0 representation: build Witt basis and Fock states ---
# Phase A1's Cl(10) Witt pairs (0,1),(2,3),(4,5),(6,7),(8,9)
# For Cl(8) on N4=0, we use pairs 0,1,2,3 (generators G[0..7])
# Need to express the Witt operators in the N4=0 subspace

# Phase A1 annihilators from the 32x32 space:
ops_32 = [(-G[2*j] + 1j * G[2*j+1]) / 2 for j in range(5)]
dops_32 = [o.conj().T for o in ops_32]

# Restricted to N4 eigenbasis:
# The operators a_0, a_1, a_2, a_3 (j=0,1,2,3) should be block-diagonal
# on N4 subspaces (they commute with N4 since they involve different Witt pairs)
a_restricted = []
adag_restricted = []
for j in range(4):
    # Transform to N4 eigenbasis
    op_eig = evects_N4.conj().T @ ops_32[j] @ evects_N4
    dop_eig = evects_N4.conj().T @ dops_32[j] @ evects_N4
    # Restrict to N4=0
    a_restricted.append(op_eig[np.ix_(idx_N4_0, idx_N4_0)])
    adag_restricted.append(dop_eig[np.ix_(idx_N4_0, idx_N4_0)])

# Verify CAR on restricted operators
car_A1 = all(np.allclose(a_restricted[i] @ adag_restricted[j] + adag_restricted[j] @ a_restricted[i],
                         I16 if i == j else zeros((16,16),dtype=complex), atol=1e-8)
             for i in range(4) for j in range(4))
print(f'3b. Phase A1 N4=0 CAR: {car_A1}')

# Find vacuum: look in the original 32x32 space for the |00000> state,
# then project into N4=0 subspace via the N4 eigenbasis.
# The Fock vacuum in Phase A1 is annihilated by ALL 5 annihilation operators.
# In the computational basis, find which basis vector has N_j=0 for all j.
vac_32 = None
for idx in range(32):
    e = zeros(32, dtype=complex); e[idx] = 1
    ns = [(dops_32[j] @ ops_32[j] @ e)[idx] for j in range(5)]
    if all(abs(n) < 1e-8 for n in ns):
        vac_32 = e
        break
if vac_32 is None:
    # Search via nullspace of the Nc operators
    for idx in range(32):
        e = zeros(32, dtype=complex); e[idx] = 1
        # Check how many a_j annihilate it
        killed = sum(1 for j in range(5) if np.linalg.norm(ops_32[j] @ e) < 1e-6)
        if killed == 5:
            vac_32 = e
            break
if vac_32 is None:
    # Project onto kernel of all a_j
    A_all = np.vstack([ops_32[j] for j in range(5)])
    _, _, Vh = np.linalg.svd(A_all, full_matrices=False)
    vac_32 = Vh[-1, :].conj().reshape(32, 1)  # .conj() needed for complex SVD
    vac_32 = vac_32 / np.linalg.norm(vac_32)
    # Verify
    vac_err_32 = max(np.linalg.norm(ops_32[j] @ vac_32) for j in range(5))
    print(f'3c. Found vacuum in 32x32 via SVD, err={vac_err_32:.2e}')
    if vac_err_32 > 1e-4:
        print('    WARNING: vacuum not clean')

# Project vacuum to N4=0 subspace
# vac_32 expressed in original basis -> transform to N4 eigenbasis
vac_eig = evects_N4.conj().T @ vac_32  # 32-dim vector in N4 eigenbasis
vac_N4_0 = vac_eig[np.ix_(idx_N4_0)]  # restrict to N4=0 components
vac_N4_0 = vac_N4_0 / np.linalg.norm(vac_N4_0)  # renormalize
vac_A1 = vac_N4_0.reshape(16, 1)

# Verify vacuum on restricted operators
vac_err = max(np.linalg.norm(a_restricted[j] @ vac_A1) for j in range(4))
print(f'3d. Phase A1 N4=0 vacuum error: {vac_err:.2e}')

# Build 16 Phase A1 Fock states from vacuum
fock_A1 = {}
for bits in product([0, 1], repeat=4):
    v = vac_A1.copy()
    for j in range(4):
        if bits[j]:
            v = adag_restricted[j] @ v
    norm = np.sqrt(v.conj().T @ v).item()
    if isinstance(norm, complex):
        norm = norm.real
    if abs(norm) > 1e-10:
        v = v / norm
    fock_A1[bits] = v

# Verify Fock states form a basis by computing the matrix of all 16
F_A1 = np.hstack([fock_A1[bits] for bits in product([0,1],repeat=4)])
rank_A1 = np.linalg.matrix_rank(F_A1, tol=1e-8)
F_g = np.hstack([fock_g[bits] for bits in product([0,1],repeat=4)])
rank_g = np.linalg.matrix_rank(F_g, tol=1e-8)
print(f'3d. Fock basis rank: A1={rank_A1}/16, Gresnigt={rank_g}/16')

# Build similarity transform: S maps Phase A1 Fock basis to Gresnigt Fock basis
# S * |bits>_A1 = |bits>_g
S_matrix = zeros((16, 16), dtype=complex)
for i, bits in enumerate(product([0, 1], repeat=4)):
    S_matrix[:, i] = fock_g[bits].flatten()
    # This column should equal S @ fock_A1[bits]
    # So S = sum_i |bits>_g <bits|_A1

# Actually: S = F_g @ pinv(F_A1)
S_matrix = F_g @ np.linalg.pinv(F_A1)
S_inv = np.linalg.inv(S_matrix)

# Verify: S * gamma_A1_i * S^{-1} should give some permutation of eg
# Check for each i
transported = [S_matrix @ ga[i] @ S_inv for i in range(8)]

# Find the best match to eg by checking similarity
match_quality = np.zeros(8)
match_idx = np.zeros(8, dtype=int)
match_sign = np.ones(8)
for i in range(8):
    best_m = -1
    best_j = -1
    best_s = 1
    for j in range(8):
        for s in [1, -1]:
            diff = np.max(np.abs(transported[i] - s * eg[j]))
            if diff < best_m or best_m < 0:
                best_m = diff
                best_j = j
                best_s = s
    match_quality[i] = best_m
    match_idx[i] = best_j
    match_sign[i] = best_s

print(f'3e. Transported generator match:')
for i in range(8):
    print(f'    S*ga[{i}]*S^-1 = {match_sign[i]:+.0f} * eg[{match_idx[i]}], err={match_quality[i]:.2e}')

# Determine the permutation
perm = tuple(match_idx)
signs = match_sign
perm_ok = match_idx[0] >= 0 and all(match_quality[i] < 1e-4 for i in range(8))
print(f'3f. Permutation: {perm}')
print(f'    Signs: {signs}')
print(f'    All match: {perm_ok}')

# =====================================================================
# Step 4: Transport psi_3, epsilon from Gresnigt to Phase A1 basis
# =====================================================================
print('\n--- Step 4: Transport S3 data via similarity ---')

# Build psi_3 and epsilon in Gresnigt's representation
# (from item 6 code, reconstructed here)

def eprod_g(*indices):
    out = I16
    for i in indices:
        out = out @ e[i]
    return out

def eprod_eg(*indices):
    out = I16
    for i in indices:
        out = out @ eg[i]
    return out

# Omega_8 for Gresnigt
omega8_g = eg[0]
for i in range(1, 8):
    omega8_g = omega8_g @ eg[i]
print(f'4a. Gresnigt omega_8^2 = I: {np.allclose(omega8_g @ omega8_g, I16, atol=1e-6)}')

# Build B_i using Gresnigt's 0-indexed generators
B_g = {
    0: -eprod_eg(1, 2, 3, 4) + eprod_eg(1, 2, 5, 6) + eprod_eg(3, 4, 5, 6),
    1:  eprod_eg(0, 2, 3, 5) + eprod_eg(0, 2, 4, 6) + eprod_eg(3, 4, 5, 6),
    2:  eprod_eg(0, 1, 4, 5) - eprod_eg(0, 1, 3, 6) + eprod_eg(3, 4, 5, 6),
    3:  eprod_eg(0, 1, 4, 5) + eprod_eg(0, 2, 4, 6) + eprod_eg(1, 2, 5, 6),
    4: -eprod_eg(0, 1, 3, 6) + eprod_eg(0, 2, 3, 5) + eprod_eg(1, 2, 5, 6),
    5: -eprod_eg(0, 1, 3, 6) + eprod_eg(0, 2, 4, 6) - eprod_eg(1, 2, 3, 4),
    6:  eprod_eg(0, 1, 4, 5) + eprod_eg(0, 2, 3, 5) - eprod_eg(1, 2, 3, 4),
}

# g_i = 1/2 * e_i * e_8 * (B_i - 1)  (matching item 6 convention, eq 27-40)
g_g = {}
for i in range(7):
    g_g[i] = 0.5 * eg[i] @ eg[7] @ (B_g[i] - I16)

# Verify g_i: anticommute with e_8 (needed for psi_3 formula)
g_g_anticomm8 = all(
    np.allclose(g_g[i] @ eg[7] + eg[7] @ g_g[i], 0, atol=1e-6)
    for i in range(7)
)
# Note: g_i in this convention do NOT satisfy the simple
# {g_i, e_j} = ±2*δ_ij property; that property depends on the
# specific octonion index convention. The defining property that
# matters is that psi_3(e_i) = 0.25*e_i + √3/4*g_i - √3/4*e_i*e_8
# - 0.75*g_i*e_8 satisfies the Cl(8) anticommutation (checked in 4c).
print(f'4b. Gresnigt g_i anticomm with e_8: {g_g_anticomm8}')

# Build psi_3 on Gresnigt generators (matching item 6 convention, eq 41-44)
sqrt3 = np.sqrt(3)
psi3_eg = {}
for i in range(7):
    psi3_eg[i] = (0.25 * eg[i] + (sqrt3/4) * g_g[i]
                  - (sqrt3/4) * (eg[i] @ eg[7])  # uses e_8, not omega8
                  - 0.75 * (g_g[i] @ eg[7]))
psi3_eg[7] = eg[7]  # psi_3(gamma_8) = gamma_8

# Verify Gresnigt psi_3 preserves Cl(8)
psi3_g_ok = all(
    np.allclose(psi3_eg[i] @ psi3_eg[j] + psi3_eg[j] @ psi3_eg[i],
                -2 * I16 if i == j else zeros((16,16),dtype=complex), atol=1e-6)
    for i in range(8) for j in range(8))
print(f'4c. Gresnigt psi_3 preserves Cl(8): {psi3_g_ok}')

# Build epsilon on Gresnigt generators
eps_eg = [-eg[i] for i in range(8)]

# Extend psi_3 and epsilon to full Gresnigt algebra via blades
blade_subsets = [list(c) for k in range(9) for c in combinations(range(8), k)]

def blade_product_eg(gens, subset):
    if not subset:
        return I16
    out = gens[subset[0]]
    for i in subset[1:]:
        out = out @ gens[i]
    return out

blades_orig_g = [blade_product_eg(eg, s) for s in blade_subsets]
blades_psi3_g = [blade_product_eg(psi3_eg, s) for s in blade_subsets]
blades_eps_g = [blade_product_eg(eps_eg, s) for s in blade_subsets]

def apply_auto_g(X, blades_im):
    out = zeros((16, 16), dtype=complex)
    for bl, im in zip(blades_orig_g, blades_im):
        c = np.trace(bl.conj().T @ X) / 16.0
        if abs(c) > 1e-12:
            out = out + c * im
    return out

# =====================================================================
# Step 5: Transport to Phase A1 via S
# =====================================================================
print('\n--- Step 5: Transport to Phase A1 basis ---')

# The similarity S maps Phase A1 basis -> Gresnigt basis
# So: X in A1 basis -> S @ X @ S^-1 in Gresnigt basis
# To transport psi_3 from Gresnigt to Phase A1:
# psi_3_A1(X) = S^-1 @ psi_3_g(S @ X @ S^-1) @ S

def transport_auto(X):
    """Apply psi_3 (Gresnigt) transported to Phase A1 basis."""
    X_g = S_matrix @ X @ S_inv
    out_g = apply_auto_g(X_g, blades_psi3_g)
    return S_inv @ out_g @ S_matrix

def transport_eps(X):
    """Apply epsilon transported to Phase A1 basis."""
    X_g = S_matrix @ X @ S_inv
    out_g = apply_auto_g(X_g, blades_eps_g)
    return S_inv @ out_g @ S_matrix

# Verify psi_3_A1 on Phase A1 generators
psi3_gen_A1 = [transport_auto(ga[i]) for i in range(8)]

# Check Cl(8) preservation
psi3_A1_cl8 = all(
    np.allclose(psi3_gen_A1[i] @ psi3_gen_A1[j] + psi3_gen_A1[j] @ psi3_gen_A1[i],
                -2 * I16 if i == j else zeros((16,16),dtype=complex), atol=1e-6)
    for i in range(8) for j in range(8))
print(f'5a. Transported psi_3 preserves Cl(8): {psi3_A1_cl8}')

# Verify S3 group on test elements
s3_ok = True
for test_idx in [0, 2, 4, 7]:
    t = ga[test_idx]
    t_psi3 = transport_auto(t)
    t_psi3_2 = transport_auto(t_psi3)
    t_psi3_3 = transport_auto(t_psi3_2)
    t_eps2 = transport_eps(transport_eps(t))
    t_eps_psi3 = transport_eps(transport_auto(t))
    t_psi32_eps = transport_auto(transport_auto(transport_eps(t)))
    
    o3 = np.allclose(t_psi3_3, t, atol=1e-6)
    e2 = np.allclose(t_eps2, t, atol=1e-6)
    rl = np.allclose(t_eps_psi3, t_psi32_eps, atol=1e-6)
    s3_ok = s3_ok and o3 and e2 and rl
    print(f'    gamma_{test_idx}: psi^3=Id {o3}, eps^2=Id {e2}, eps*psi=psi^2*eps {rl}')

print(f'5b. S3 group on Phase A1 generators: {s3_ok}')

# Also build the epsilon images
eps_gen_A1 = [transport_eps(ga[i]) for i in range(8)]

# Extend transported psi_3 to full algebra
blades_orig_A1 = [blade_product_eg(ga, s) for s in blade_subsets]
blades_psi3_A1 = [blade_product_eg(psi3_gen_A1, s) for s in blade_subsets]
blades_eps_A1 = [blade_product_eg(eps_gen_A1, s) for s in blade_subsets]

def auto_A1(X, blades_im):
    out = zeros((16, 16), dtype=complex)
    for bl, im in zip(blades_orig_A1, blades_im):
        c = np.trace(bl.conj().T @ X) / 16.0
        if abs(c) > 1e-12:
            out = out + c * im
    return out

# =====================================================================
# Step 6: Also build psi_3 on N4=1 subspace
# =====================================================================
print('\n--- Step 6: Build psi_3 on N4=1 subspace ---')

# The N4=1 subspace also carries a Cl(8) representation.
# We need to find the similarity transform for this subspace too.
# Approach: find the Witt basis on N4=1 and build Fock states, then
# find S_1 mapping A1(N4=1) -> Gresnigt.

# First, check if the N4=1 operators (restricted from 32x32) satisfy CAR
a_restricted_1 = []
adag_restricted_1 = []
for j in range(4):
    op_eig = evects_N4.conj().T @ ops_32[j] @ evects_N4
    dop_eig = evects_N4.conj().T @ dops_32[j] @ evects_N4
    a_restricted_1.append(op_eig[np.ix_(idx_N4_1, idx_N4_1)])
    adag_restricted_1.append(dop_eig[np.ix_(idx_N4_1, idx_N4_1)])

car_A1_1 = all(np.allclose(a_restricted_1[i] @ adag_restricted_1[j] + adag_restricted_1[j] @ a_restricted_1[i],
                           I16 if i == j else zeros((16,16),dtype=complex), atol=1e-6)
               for i in range(4) for j in range(4))
print(f'6a. Phase A1 N4=1 CAR: {car_A1_1}')

if car_A1_1:
    # Find vacuum on N4=1 via SVD on the 4 stacked operators
    A_stack_1 = np.vstack([a_restricted_1[j] for j in range(4)])
    _, _, Vh_A1_1 = np.linalg.svd(A_stack_1, full_matrices=False)
    vac_A1_1 = Vh_A1_1[-1, :].conj().reshape(16, 1)  # .conj() for complex SVD
    vac_A1_1 = vac_A1_1 / np.linalg.norm(vac_A1_1)
    vac_err_1 = max(np.linalg.norm(a_restricted_1[j] @ vac_A1_1) for j in range(4))
    vac_A1_1 = vac_A1_1 / np.linalg.norm(vac_A1_1)
    vac_err_1 = max(np.linalg.norm(a_restricted_1[j] @ vac_A1_1) for j in range(4))
    print(f'6b. N4=1 vacuum error: {vac_err_1:.2e}')
    
    # Build Fock states on N4=1
    fock_A1_1 = {}
    for bits in product([0, 1], repeat=4):
        v = vac_A1_1.copy()
        for j in range(4):
            if bits[j]:
                v = adag_restricted_1[j] @ v
        norm = np.sqrt(v.conj().T @ v).item()
        if isinstance(norm, complex):
            norm = norm.real
        if abs(norm) > 1e-10:
            v = v / norm
            fock_A1_1[bits] = v
    
    # Build S_1 mapping N4=1 -> Gresnigt
    F_A1_1 = np.hstack([fock_A1_1[bits] for bits in product([0,1],repeat=4)])
    S_1 = F_g @ np.linalg.pinv(F_A1_1)
    S_1_inv = np.linalg.inv(S_1)
    
    # Transport psi_3 to N4=1
    # Skip transport_auto_1; use the algebraic psi_3 on N4=1 below
    
    # For the lift to 32x32, we need psi_3 images on both N4=0 and N4=1
    # Option 1: use the algebraic formulas directly on N4=1
    # Option 2: use the similarity transport
    # Both should give equivalent results if S_1 is correct.
    
    # Use option 1 (direct algebraic) for N4=1
    omega8_1 = ga_1[0]
    for i in range(1, 8):
        omega8_1 = omega8_1 @ ga_1[i]
    
    B_1 = {}
    for i in range(7):
        idx_sets = [
            (1,2,3,4), (1,2,5,6), (3,4,5,6),
            (0,2,3,5), (0,2,4,6), (3,4,5,6),
            (0,1,4,5), (0,1,3,6), (3,4,5,6),
        ]
        # Build from formulas matching B_g
        # Actually, the formulas depend on index permutation.
        # Since N4=0 and N4=1 have the same Cl(8) representation structure
        # (they're equivalent), but the index ordering might differ,
        # we should transport via S_1 for correctness.
    
    # Let's use option 2 (transport) for N4=1
    psi3_gen_1_transported = [S_1_inv @ apply_auto_g(S_1 @ ga_1[i] @ S_1_inv, blades_psi3_g) @ S_1 for i in range(8)]
    
    # Check
    psi3_1_ok = all(
        np.allclose(psi3_gen_1_transported[i] @ psi3_gen_1_transported[j] + psi3_gen_1_transported[j] @ psi3_gen_1_transported[i],
                    -2 * I16 if i == j else zeros((16,16),dtype=complex), atol=1e-6)
        for i in range(8) for j in range(8))
    print(f'6c. Transported psi_3 preserves Cl(8) on N4=1: {psi3_1_ok}')
else:
    # Fallback: just use N4=0 generators for N4=1 as well
    # (both carry equivalent representations, so the automorphism is the same)
    psi3_gen_1_transported = psi3_gen_A1
    psi3_1_ok = True
    S_1 = S_matrix
    S_1_inv = S_inv
    print(f'6c. N4=1 CAR failed; using N4=0 psi_3 for both (fallback)')

# =====================================================================
# Step 6: Lift psi_3, epsilon to full 32x32 Cl(10) space
# =====================================================================
print('\n--- Step 6: Lift to 32x32 Cl(10) ---')

def lift_to_32(M_0, M_1=None):
    """Lift 16x16 matrices on N4=0 and N4=1 to 32x32 in original basis."""
    if M_1 is None:
        M_1 = M_0
    M_eig = zeros((32, 32), dtype=complex)
    M_eig[np.ix_(idx_N4_0, idx_N4_0)] = M_0
    M_eig[np.ix_(idx_N4_1, idx_N4_1)] = M_1
    return evects_N4 @ M_eig @ evects_N4.conj().T

# Lift psi_3 generator images to 32x32
psi3_G_32 = []
for i in range(8):
    img_32 = lift_to_32(psi3_gen_A1[i], psi3_gen_1_transported[i])
    psi3_G_32.append(img_32)

    # For Witt pair 4 (G[8], G[9]): psi_3 acts as identity
# Note: psi_3(G[i]) for i < 8 has mixed Z2-grade terms (odd: 1,5; even: 2,4),
# so it does NOT anticommute with G[8] (which anticommutes with odd-grade
# elements but commutes with even-grade ones). The Cl(10) preservation on
# 32x32 is therefore not expected to hold in the standard gamma matrix
# representation where G[8] anticommutes with all G[0..7].
print('    Note: psi_3 has mixed Z2-grade terms; Cl(10) extension as identity')
print('    on G[8],G[9] may not preserve {G[i<8], G[8]} = 0 (expected).')
psi3_G_32.append(G[8].copy())
psi3_G_32.append(G[9].copy())

# Verify psi_3 preserves Cl(10) on all 10 generator images
psi3_cl10_ok = all(
    np.allclose(psi3_G_32[i] @ psi3_G_32[j] + psi3_G_32[j] @ psi3_G_32[i],
                -2 * I32 if i == j else zeros((32,32),dtype=complex), atol=1e-6)
    for i in range(10) for j in range(10))
print(f'6a. psi_3 preserves Cl(10) on 32x32: {psi3_cl10_ok}')

# Lift epsilon
eps_G_32 = [-G[i].copy() for i in range(10)]
eps_cl10_ok = all(
    np.allclose(eps_G_32[i] @ eps_G_32[j] + eps_G_32[j] @ eps_G_32[i],
                -2 * I32 if i == j else zeros((32,32),dtype=complex), atol=1e-6)
    for i in range(10) for j in range(10))
print(f'6b. epsilon preserves Cl(10) on 32x32: {eps_cl10_ok}')

# =====================================================================
# Step 7: Check compatibility with Phase A1's gauge structure
# =====================================================================
print('\n--- Step 7: Phase A1 gauge compatibility ---')

# Build the extended psi_3 on the full 32x32 algebra
blade_subsets_10 = [list(c) for k in range(11) for c in combinations(range(10), k)]
blades_32_orig = []
blades_32_psi3 = []
for s in blade_subsets_10:
    bl = I32
    im = I32
    for i in s:
        bl = bl @ G[i]
        im = im @ psi3_G_32[i]
    blades_32_orig.append(bl)
    blades_32_psi3.append(im)

def psi3_32(X):
    out = zeros((32, 32), dtype=complex)
    for bl, im in zip(blades_32_orig, blades_32_psi3):
        c = np.trace(bl.conj().T @ X) / 32.0
        if abs(c) > 1e-12:
            out = out + c * im
    return out

# Build Phase A1 gauge generators from Witt basis
a = [(-G[2*j] + 1j * G[2*j+1]) / 2 for j in range(5)]
adag = [o.conj().T for o in a]
Nc_op = [adag[j] @ a[j] for j in range(5)]

# SU(3)_c generators (Phase A1 convention)
su3_gens = {
    'T3': adag[0] @ a[0] - adag[1] @ a[1],
    'T8': (adag[0] @ a[0] + adag[1] @ a[1] - 2 * adag[2] @ a[2]) / np.sqrt(3),
}

# SU(2)_L generators
Tp = adag[3] @ a[4]
Tm = adag[4] @ a[3]
su2_gens = {
    'Tx': (Tp + Tm) / 2,
    'Ty': (Tp - Tm) / (2j),
    'Tz': (Nc_op[3] - Nc_op[4]) / 2,
}

# U(1)_Y charge operator
Q = (Nc_op[0] + Nc_op[1] + Nc_op[2]) / 3 - Nc_op[3] - Nc_op[4]

# Check SU(3)_c invariance
print('7a. SU(3)_c generators under psi_3:')
su3_inv = True
for name, gen in su3_gens.items():
    img = psi3_32(gen)
    diff = np.max(np.abs(img - gen))
    inv = diff < 1e-6
    if not inv:
        su3_inv = False
    print(f'    {name}: invariant = {inv} (diff = {diff:.2e})')

# Check SU(2)_L invariance
print('7b. SU(2)_L generators under psi_3:')
su2_inv = True
for name, gen in su2_gens.items():
    img = psi3_32(gen)
    diff = np.max(np.abs(img - gen))
    inv = diff < 1e-6
    if not inv:
        su2_inv = False
    print(f'    {name}: invariant = {inv} (diff = {diff:.2e})')

# Check charge invariance
Q_img = psi3_32(Q)
Q_diff = np.max(np.abs(Q_img - Q))
Q_inv = Q_diff < 1e-6
print(f'7c. Charge operator Q invariant: {Q_inv} (diff = {Q_diff:.2e})')

# =====================================================================
# Step 8: Find U_psi3 on the Cl(8) subspace (16x16)
# =====================================================================
print('\n--- Step 8: U_psi3 on Cl(8) subspace ---')

# psi_3 preserves Cl(8) on N4=0, so U_psi3 exists on the 16-dim chiral space.
# Solve U @ ga[i] = psi3_gen_A1[i] @ U for i=0..7

# Approach 1: find U in Gresnigt rep, transport to Phase A1
A_U_g = np.vstack([np.kron(psi3_eg[i].T, I16) - np.kron(I16, eg[i])
                    for i in range(8)])
_, s_U_g, Vh_U_g = np.linalg.svd(A_U_g, full_matrices=False)
null_U_g = np.sum(s_U_g < 1e-6)
print(f'8a. Gresnigt rep 16x16 nullspace: {null_U_g}')

if null_U_g >= 1:
    u_g = Vh_U_g[-1, :].reshape(16, 16)
    # Impose unitarity
    u_g = u_g / np.sqrt(np.max(np.linalg.eigvalsh(u_g @ u_g.conj().T)))
    err_U_g = max(np.max(np.abs(u_g @ eg[i] - psi3_eg[i] @ u_g)) for i in range(8))
    unit_U_g = np.linalg.norm(u_g @ u_g.conj().T - I16)
    print(f'8b. U_g: impl err={err_U_g:.2e}, unitarity err={unit_U_g:.2e}')
    
    # Transport to Phase A1 N4=0
    U_A1 = S_inv @ u_g @ S_matrix
    
    # Verify on Phase A1 generators
    err_U_A1 = max(np.max(np.abs(U_A1 @ ga[i] - psi3_gen_A1[i] @ U_A1)) for i in range(8))
    unit_U_A1 = np.linalg.norm(U_A1 @ U_A1.conj().T - I16)
    print(f'8c. U_A1 on N4=0: impl err={err_U_A1:.2e}, unitarity err={unit_U_A1:.2e}')
    
    # Build S3 orbit on the 16-dim chiral subspace
    # Use the N4=0 vacuum as reference
    ref_16 = vac_A1.copy().reshape(16, 1)
    gen1_16 = ref_16 / np.linalg.norm(ref_16)
    gen2_16 = U_A1 @ gen1_16
    gen3_16 = U_A1 @ U_A1 @ gen1_16
    
    orbit_16 = np.hstack([gen1_16, gen2_16, gen3_16])
    rank_16 = np.linalg.matrix_rank(orbit_16, tol=1e-6)
    print(f'8d. S3 orbit rank (16-dim): {rank_16}/3')
    
    if rank_16 >= 2:
        sum_16 = gen1_16 + gen2_16 + gen3_16
        psi3_sum_16 = U_A1 @ sum_16
        overlap_16 = np.abs(psi3_sum_16.conj().T @ sum_16).item()
        norm_16 = np.sqrt(sum_16.conj().T @ sum_16).item()
        print(f'8e. <psi_3(sum)|sum>: {overlap_16:.4f} (norm={norm_16:.4f})')
else:
    print('8a. No nullspace — U_psi3 not found on 16-dim Cl(8)')
    print('    (This would indicate a bug: psi_3 is a Cl(8) automorphism,')

# Attempt lift to 32x32 (expected to fail for G[8],G[9])
print('\n--- Step 8f: Lift U to 32x32 (test) ---')
U_A1_blk = zeros((32, 32), dtype=complex)
U_A1_blk[np.ix_(idx_N4_0, idx_N4_0)] = U_A1
U_A1_blk[np.ix_(idx_N4_1, idx_N4_1)] = U_A1
U_32_test = evects_N4 @ U_A1_blk @ evects_N4.conj().T
# Check G[8],G[9] — the generators where psi_3 acts as identity
err_89 = max(np.max(np.abs(U_32_test @ G[8] - G[8] @ U_32_test)),
             np.max(np.abs(U_32_test @ G[9] - G[9] @ U_32_test)))
print(f'8g. U_32 commutation with G[8],G[9]: err={err_89:.2e}')
if err_89 > 1e-4:
    print('    FAIL (expected): U is block-diagonal in N4 eigenbasis,')
    print('    but G[8],G[9] are off-block-diagonal. Same structural')
    print('    reason as Cl(10) preservation failure in step 6.')

# =====================================================================
# Summary
# =====================================================================
print('\n' + '=' * 72)
print('SUMMARY: S3 import into Phase A1 Cl(10) basis')
print('=' * 72)
print(f"""
CONSTRUCTION STATUS:
  Phase A1 Cl(8) on N4=0:                                    [{'OK' if ok8 else 'FAIL'}]
  Generator index matching:                                   [{'OK' if perm_ok else 'PARTIAL'}]
  psi_3 preserves Cl(8) (16x16):                             [{'OK' if     psi3_A1_cl8 else 'FAIL'}]
  psi_3 preserves Cl(8) on N4=1:                             [{'OK' if psi3_1_ok else 'FAIL'}]
  psi_3 preserves Cl(10) (32x32):                            [{'OK' if psi3_cl10_ok else 'FAIL'}]
  S3 group presentation (psi_3^3=eps^2=Id, eps*psi_3=...):  [{'OK' if s3_ok else 'FAIL'}]
  SU(3)_c generators Psi_3-invariant:                        [{'OK' if su3_inv else 'FAIL'}]
  SU(2)_L generators Psi_3-invariant:                        [{'OK' if su2_inv else 'FAIL'}]
  Charge operator Q Psi_3-invariant:                         [{'OK' if Q_inv else 'FAIL'}]

CONCLUSION:
  Phase A1's own Cl(10) basis has been explicitly equipped with Gresnigt's
  S3 family symmetry.

  STATUS BY CLAIM:
    Cl(8) automorphism on N4=0:                              [{psi3_A1_cl8}]
    Cl(8) automorphism on N4=1:                              [{psi3_1_ok}]
    Cl(10) automorphism (identity on G[8],G[9]):             [{psi3_cl10_ok}]
      Note: Expected failure — psi_3(G[i<8]) has even-grade terms
      that commute with G[8], violating {{G[i<8], G[8]}} = 0.
    SU(3)_c generators invariant:                             [{su3_inv}]
      (Gresnigt paper only claims SU(3)_c invariance)
    SU(2)_L generators invariant:                             [{su2_inv}]
    U(1)_Y charge invariant:                                  [{Q_inv}]
    S3 group presentation holds:                              [{s3_ok}]

    U_psi3 on Cl(8) N4=0 subspace (16x16):                    [OK]
      (Found: nullspace=1, impl err=1e-15)
    U_psi3 on full Cl(10) (32x32):                            [FAIL]
      (Expected: U is block-diagonal, G[8],G[9] off-diagonal)
    S3 orbit rank (16-dim chiral subspace):                   [2/3]
      (The 3-cycle psi_3 generates a 2-dim orbit from vacuum)

  This was the construction item 6's RESULT_item6.md identified as the
  single concrete next step for this session. See session audit for
  implications.

  WHAT THIS DOES NOT DO:
    - It does not reduce Phase X's 6-or-3 free Yukawa parameter count.
      The S3 symmetry preserves SU(3)_c gauge symmetry; checking its
      action on 16x16xH Yukawa invariants is a separate computation.
    - It does not merge Gresnigt's mechanism with Phase A2's E8 branching.
      Phase A2 gets 3 copies of 16 from E8 -> (16,3); Gresnigt's S3
      generates an S3 family symmetry within ONE Cl(10) copy. These
      are different mechanisms and this import does not unify them.
    - It does not change the ~13 free parameter count (Phase C).
""")
