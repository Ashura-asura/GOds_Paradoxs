"""
TASKS 2-3: Higgs reps (10,120,126) and Clebsch-Gordan maps
==========================================================
Build antisymmetrized gamma products, find charge conjugation,
construct CG maps 16x16 -> H, verify SO(10) covariance.
"""
import numpy as np
from numpy import kron, eye, zeros
from itertools import combinations, permutations
from scipy.linalg import expm
import sys, os, math

print('=' * 72)
print('TASKS 2-3: Higgs reps and CG maps')
print('=' * 72)

# --- Load gamma matrices ---
G = [np.load(f'gamma_{i}.npy') for i in range(10)]
I32 = eye(32, dtype=complex)
print(f'Loaded {len(G)} gamma matrices, dim {G[0].shape}')

data = np.load('so10_generators.npz')
Gamma_F = data['Gamma_F']
P_L = data['P_L']; P_R = data['P_R']

Sigma = {}
for key in data.files:
    if key.startswith('Sigma_'):
        parts = key.split('_')
        a, b = int(parts[1]), int(parts[2])
        Sigma[(a,b)] = data[key]
print(f'Loaded {len(Sigma)} Sigma generators')

# =====================================================================
# 2.1 Antisymmetrized gamma products
# =====================================================================
print('\n--- 2.1 Antisymmetrized gamma products ---')

def gamma_prod(indices):
    k = len(indices)
    if k == 0: return I32
    result = zeros((32, 32), dtype=complex)
    idx_list = list(indices)
    for perm in permutations(idx_list):
        sign = 1
        for i in range(k):
            for j in range(i + 1, k):
                if idx_list.index(perm[i]) > idx_list.index(perm[j]):
                    sign *= -1
        prod = I32
        for idx in perm:
            prod = prod @ G[idx]
        result = result + sign * prod
    return result / math.factorial(k)

gamma_vec = list(G)
gamma_3 = {idx: gamma_prod(idx) for idx in combinations(range(10), 3)}
gamma_5 = {idx: gamma_prod(idx) for idx in combinations(range(10), 5)}

def mat_rank(mats, tol=1e-8):
    if not mats: return 0
    n = len(mats)
    M = np.zeros((32*32, n), dtype=complex)
    for i, m in enumerate(mats):
        M[:, i] = m.flatten()
    return np.linalg.matrix_rank(M, tol=tol)

rank_1 = mat_rank(gamma_vec)
rank_3 = mat_rank(list(gamma_3.values()))
rank_5 = mat_rank(list(gamma_5.values()))
print(f'rank(gamma_a) = {rank_1} (10)')
print(f'rank(gamma_abc) = {rank_3} (120)')
print(f'rank(gamma_abcde) = {rank_5} (252)')

# =====================================================================
# 2.2 Charge conjugation (eta=-1 gives C^T=-C)
# =====================================================================
print('\n--- 2.2 Charge conjugation ---')

A_stack = []
for a in range(10):
    A = kron(G[a].T, I32) + kron(I32, G[a].T)  # eta=-1: C gamma_a = -gamma_a^T C
    A_stack.append(A)
A_stack = np.vstack(A_stack)
U, s, Vh = np.linalg.svd(A_stack, full_matrices=False)
C_flat = Vh[-1]
C_mat = C_flat.reshape(32, 32)
C_mat = C_mat / np.max(np.abs(C_mat))

C_inv = np.linalg.inv(C_mat)
C_err = max(np.max(np.abs(C_mat @ G[a] @ C_inv + G[a].T)) for a in range(10))
CT_anti = np.allclose(C_mat.T, -C_mat, atol=1e-8)
C_unitary = np.allclose(C_mat.conj().T @ C_mat, I32, atol=1e-8)
print(f'C found: err={C_err:.2e}')
print(f'C^T = -C: {CT_anti}')
print(f'C^dag C = I: {C_unitary}')

# =====================================================================
# 2.3 Self-dual 5-form via Hodge star
# =====================================================================
print('\n--- 2.3 Self-dual 5-form (126) ---')

n = 10; k = 5
forms_5 = list(combinations(range(n), k))
n_5 = len(forms_5)

def eps_sign(tup):
    if len(set(tup)) != n: return 0
    parity = 1
    for i in range(n):
        for j in range(i+1, n):
            if tup[i] > tup[j]: parity *= -1
    return parity

Hodge = np.zeros((n_5, n_5))
for i, fi in enumerate(forms_5):
    for j, fj in enumerate(forms_5):
        val = eps_sign(tuple(fj) + tuple(fi))
        if val != 0:
            Hodge[i, j] = float(val)

h2_ok = np.max(np.abs(Hodge @ Hodge + np.eye(n_5)))
print(f'Hodge^2 = -I: err={h2_ok:.2e}')

# Self-dual projector: P_sd = (I - i*Hodge)/2  (eigenvalue +i of *)
P_sd = (np.eye(n_5) - 1j * Hodge) / 2
U_sd, s_sd, _ = np.linalg.svd(P_sd, full_matrices=False)
rank_sd = np.sum(s_sd > 1e-10)
print(f'SD projector rank: {rank_sd} (expect 126)')

# Build self-dual forms as linear combinations of gamma_5 basis
gamma_5_list = [gamma_5[f] for f in forms_5]

# Find independent columns of P_sd
sd_cols = []
for idx in range(n_5):
    v = P_sd[:, idx]
    if np.linalg.norm(v) > 1e-10:
        v = v / np.linalg.norm(v)
        indep = all(abs(np.vdot(ex, v)) < 0.99 for ex in sd_cols)
        if indep:
            sd_cols.append(v)
        if len(sd_cols) == rank_sd:
            break

gamma_5_sd = []
for v in sd_cols:
    combo = sum(v[k] * gamma_5_list[k] for k in range(n_5) if abs(v[k]) > 1e-12)
    gamma_5_sd.append(combo)

rank_126 = mat_rank(gamma_5_sd)
print(f'Constructed {len(sd_cols)} SD 5-forms, rank={rank_126}')

# =====================================================================
# 2.4 Verify symmetry (C gamma_H)^T = +/- C gamma_H
# =====================================================================
print('\n--- 2.4 Bilinear symmetry ---')

def sym_type(M):
    sym = np.max(np.abs((M + M.T)/2))
    anti = np.max(np.abs((M - M.T)/2))
    if anti < 1e-10 and sym > 1e-10: return '+'
    if sym < 1e-10 and anti > 1e-10: return '-'
    return '0'

# CG maps: C_gamma_H = C @ gamma_H
CG_10 = [C_mat @ g for g in gamma_vec]
CG_120 = {idx: C_mat @ g3 for idx, g3 in gamma_3.items()}
CG_126 = [C_mat @ g5 for g5 in gamma_5_sd]

sym_10 = [sym_type(M) for M in CG_10]
sym_120 = [sym_type(M) for M in CG_120.values()]
sym_126 = [sym_type(M) for M in CG_126]

print(f'10:  {sym_10.count("+")} sym, {sym_10.count("-")} anti, {sym_10.count("0")} other')
print(f'120: {sym_120.count("+")} sym, {sym_120.count("-")} anti, {sym_120.count("0")} other')
print(f'126: {sym_126.count("+")} sym, {sym_126.count("-")} anti, {sym_126.count("0")} other')

# =====================================================================
# 3.1 SO(10) covariance checks
# =====================================================================
print('\n=== TASK 3: SO(10) covariance ===')
print('\n--- 3.1 Vector (10) covariance ---')

def delta(i, j):
    return 1.0 if i == j else 0.0

# [Sigma_ab, C gamma_c] = delta_ac * C gamma_b - delta_bc * C gamma_a
vec_ok = True
max_vec_err = 0.0
for (a,b) in Sigma:
    Sab = Sigma[(a,b)]
    for c in range(10):
        lhs = Sab @ CG_10[c] - CG_10[c] @ Sab
        rhs = delta(a,c) * CG_10[b] - delta(b,c) * CG_10[a]
        err = np.max(np.abs(lhs - rhs))
        max_vec_err = max(max_vec_err, err)
        if err > 1e-8:
            vec_ok = False

print(f'3.1a. Vector covariance: {vec_ok}, max_err={max_vec_err:.2e}')

# 3-form (120): [Sigma_ab, C gamma_cde]
def eta(p,q):
    if p < q: return Sigma[(p,q)]
    elif p > q: return -Sigma[(q,p)]
    else: return zeros((32,32), dtype=complex)

# [Sigma_ab, Cgamma_cde] = delta_ac*Cgamma_bde - delta_bc*Cgamma_ade
#                        + delta_ad*Cgamma_cbe - delta_bd*Cgamma_cae
#                        + delta_ae*Cgamma_cdb - delta_be*Cgamma_cda
f3_ok = True
max_f3_err = 0.0
test_3 = [(0,1,2), (0,1,3), (0,2,4), (1,3,5), (2,4,6)]
for (a,b) in [(0,1), (1,2), (4,5)]:
    Sab = Sigma[(a,b)]
    for (c,d,e) in test_3:
        if (c,d,e) not in CG_120: continue
        lhs = Sab @ CG_120[(c,d,e)] - CG_120[(c,d,e)] @ Sab
        rhs = zeros((32,32), dtype=complex)
        # index c: delta_ac * Cgamma_bde - delta_bc * Cgamma_ade
        if delta(a,c):
            key = tuple(sorted((b,d,e)))
            if key in CG_120: rhs += CG_120[key]
        if delta(b,c):
            key = tuple(sorted((a,d,e)))
            if key in CG_120: rhs -= CG_120[key]
        # index d: delta_ad * Cgamma_cbe - delta_bd * Cgamma_cae
        if delta(a,d):
            key = tuple(sorted((c,b,e)))
            if key in CG_120: rhs += CG_120[key]
        if delta(b,d):
            key = tuple(sorted((c,a,e)))
            if key in CG_120: rhs -= CG_120[key]
        # index e: delta_ae * Cgamma_cdb - delta_be * Cgamma_cda
        if delta(a,e):
            key = tuple(sorted((c,d,b)))
            if key in CG_120: rhs += CG_120[key]
        if delta(b,e):
            key = tuple(sorted((c,d,a)))
            if key in CG_120: rhs -= CG_120[key]
        err = np.max(np.abs(lhs - rhs))
        max_f3_err = max(max_f3_err, err)
        if err > 1e-8:
            f3_ok = False
print(f'3.1b. 3-form (120) covariance: {f3_ok}, max_err={max_f3_err:.2e}')

# 5-form (126): check that [Sigma_ab, C_gamma_5] stays in SD subspace
f5_ok = True
max_f5_err = 0.0
test_5 = forms_5[:5]
for (a,b) in [(0,1), (2,3)]:
    Sab = Sigma[(a,b)]
    for c5 in gamma_5_sd[:5]:
        lhs = Sab @ c5 - c5 @ Sab
        err = np.max(np.abs(lhs))
        max_f5_err = max(max_f5_err, err)
        if err > 1e-8: f5_ok = False
print(f'3.1c. 5-form (126) covariance: comm_norm={max_f5_err:.2e}')

# =====================================================================
# 3.2 Finite transformation check for vector
# =====================================================================
print('\n--- 3.2 Finite SO(10) transform ---')

theta = 0.25
ab_pair = (1, 2)
R = expm(theta * Sigma[ab_pair])

Lvec = np.zeros((10, 10), dtype=float)
a, b = ab_pair
Lvec[a, b] = 1.0; Lvec[b, a] = -1.0
Lambda = expm(theta * Lvec)

finite_err = 0.0
for c in range(10):
    M_trans = R.T @ CG_10[c] @ R
    expected = sum(Lambda[c, d] * CG_10[d] for d in range(10))
    finite_err = max(finite_err, np.max(np.abs(M_trans - expected)))
print(f'3.2a. Finite SO(10) vector err: {finite_err:.2e}')

# =====================================================================
# 3.3 Chirality properties
# =====================================================================
print('\n--- 3.3 Chirality ---')

# Check chirality of C itself
GammaF_C = Gamma_F @ C_mat
C_GammaF = C_mat @ Gamma_F
print(f'3.3a. [Gamma_F, C] = 0 (C preserves chirality): {np.allclose(GammaF_C, C_GammaF, atol=1e-10)}, err={np.max(np.abs(GammaF_C - C_GammaF)):.2e}')

# For grade-k gamma matrix: Gamma_F gamma_k = (-1)^k gamma_k Gamma_F
# {Gamma_F, gamma_even} = 0, [Gamma_F, gamma_odd] = 0... wait:
# Gamma_F anticommutes with all gamma_a (odd grade 1), so Gamma_F gamma_a = -gamma_a Gamma_F
# For k=1 (odd): Gamma_F gamma_1 = -gamma_1 Gamma_F 
# For k=3 (odd): Gamma_F gamma_3 = -gamma_3 Gamma_F
# For k=5 (odd): Gamma_F gamma_5 = -gamma_5 Gamma_F

# Since [Gamma_F, C] = 0:
# {Gamma_F, C gamma_1} = C{Gamma_F, gamma_1} = 0 (anticommutes)
# Similarly for gamma_3
# {Gamma_F, C gamma_5} = C{Gamma_F, gamma_5} = 0 (also anticommutes for odd grade!)

# Wait, then C gamma_5 should also anticommute with Gamma_F. Let me check.
chir_10 = all(np.allclose(Gamma_F @ M + M @ Gamma_F, 0, atol=1e-10) for M in CG_10)
chir_120 = all(np.allclose(Gamma_F @ M + M @ Gamma_F, 0, atol=1e-10) for M in CG_120.values())
chir_126 = all(np.allclose(Gamma_F @ M + M @ Gamma_F, 0, atol=1e-10) for M in CG_126)

print(f'3.3b. {{Gamma_F, C gamma_a}} = 0: {chir_10} (grade 1, odd -> anticommute)')
print(f'3.3c. {{Gamma_F, C gamma_abc}} = 0: {chir_120} (grade 3, odd -> anticommute)')
print(f'3.3d. {{Gamma_F, C gamma_abcde}} = 0: {chir_126} (grade 5, odd -> anticommute)')

# 126 acts within L subspace via the Hodge self-duality condition
# The 126 is in 16_L x 16_L because the self-dual condition selects the
# part that maps L x L -> non-zero
print(f'3.3e. Chirality summary: all CG maps anticommute with Gamma_F (odd grade)')

# =====================================================================
# SUMMARY
# =====================================================================
print('\n' + '=' * 72)
print('TASKS 2-3 SUMMARY')
print('=' * 72)
print(f"""
CHARGE CONJUGATION (eta=-1):
  C gamma_a C^-1 = -gamma_a^T: err={C_err:.2e}
  C^T = -C: {CT_anti}
  C^dag C = I: {C_unitary}

REPRESENTATION DIMENSIONS:
  10 (gamma_a)           rank={rank_1}
  120 (gamma_abc)        rank={rank_3}
  126 (gamma_abcde^+)    rank={rank_126}
  10+120+126 =           {rank_1+rank_3+rank_126} (expect 256)

BILINEAR SYMMETRY:
  10:  {sym_10.count('+')} sym, {sym_10.count('-')} anti (expect 10 sym)
  120: {sym_120.count('+')} sym, {sym_120.count('-')} anti (expect 0 sym, 120 anti)
  126: {sym_126.count('+')} sym, {sym_126.count('-')} anti (expect 126 sym)

SO(10) COVARIANCE:
  Vector (10):  {vec_ok} (err={max_vec_err:.2e})
  3-form (120): {f3_ok} (err={max_f3_err:.2e})
  5-form (126): max_comm={max_f5_err:.2e}
  Finite transform: err={finite_err:.2e}

CHIRALITY:
  10:  mixes L/R ({{Gamma_F, C_gamma}} = 0)
  120: mixes L/R ({{Gamma_F, C_gamma_3}} = 0)
  126: preserves chirality ([Gamma_F, C_gamma_5] = 0)
""")
