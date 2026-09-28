"""
Try alternative approaches to find U_psi3
=========================================
Previous attempt on 32x32 failed (nullspace dim=0).
Try:
1. Solve on N4=0 subspace (16x16) where psi_3 preserves Cl(8)
2. Solve on N4=1 subspace separately
3. Direct-sum to get 32x32 U
4. If that fails, try finding U in Gresnigt's rep then transport
"""
import numpy as np
from numpy import kron, eye, zeros
from itertools import product, combinations

print('=' * 72)
print('U_psi3: alternative construction')
print('=' * 72)

# Rebuild everything needed
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'support'))
from qosc_division_connection import build_octonion_structure_constants
C, _, _, _ = build_octonion_structure_constants()
s1 = np.array([[0,1],[1,0]], dtype=complex)
s2 = np.array([[0,-1j],[1j,0]], dtype=complex)
s3 = np.array([[1,0],[0,-1]], dtype=complex)
I2 = eye(2, dtype=complex); I8 = eye(8, dtype=complex)
I16 = eye(16, dtype=complex); I32 = eye(32, dtype=complex)

def K(*mats):
    out = mats[0]
    for m in mats[1:]:
        out = kron(out, m)
    return out

# Phase A1 gamma matrices
G8 = [kron(s1, C[i]) for i in range(1, 8)] + [1j * kron(s2, I8)]
G = [kron(G8[i], s3) for i in range(8)] + [
    kron(I16, 1j * np.array([[0,1],[1,0]], dtype=complex)),
    kron(I16, 1j * np.array([[0,-1j],[1j,0]], dtype=complex)),
]

# N4 subspace
ops = [(-G[2*j] + 1j * G[2*j+1]) / 2 for j in range(5)]
dops = [o.conj().T for o in ops]
N4_op = dops[4] @ ops[4]
evals_N4, evects_N4 = np.linalg.eigh(N4_op)
idx_N4_0 = np.where(np.abs(evals_N4) < 1e-8)[0]
idx_N4_1 = np.where(np.abs(evals_N4 - 1) < 1e-8)[0]

G_eig = [evects_N4.conj().T @ G[i] @ evects_N4 for i in range(8)]
ga = [g[np.ix_(idx_N4_0, idx_N4_0)] for g in G_eig]
ga_1 = [g[np.ix_(idx_N4_1, idx_N4_1)] for g in G_eig]

# Gresnigt generators
e = {}
e[1] = 1j * K(s1, s1, s1, s1)
e[2] = 1j * K(s1, s1, s3, I2)
e[3] = -1j * K(s1, s1, s1, s3)
e[4] = -1j * K(s1, s3, I2, I2)
e[5] = -1j * K(s1, s1, s1, s2)
e[6] = -1j * K(s1, s2, I2, I2)
e[7] = 1j * K(s1, s1, s2, I2)
e[8] = 1j * K(s2, I2, I2, I2)
eg = [e[i+1] for i in range(8)]

# Similarity transform (from earlier code)
a_g, adag_g = {}, {}
for j in range(1, 5):
    a_g[j] = 0.5 * (-eg[j-1] + 1j * eg[j+3])
    adag_g[j] = 0.5 * (eg[j-1] + 1j * eg[j+3])

vac_g = zeros((16, 1), dtype=complex); vac_g[0] = 1.0
fock_g = {}
for bits in product([0,1],repeat=4):
    v = vac_g.copy()
    for j in range(4):
        if bits[j]: v = adag_g[j+1] @ v
    norm = np.sqrt(v.conj().T @ v).item()
    if isinstance(norm, complex): norm = norm.real
    if abs(norm) > 1e-10: v = v / norm
    fock_g[bits] = v

ops_32 = [(-G[2*j] + 1j * G[2*j+1]) / 2 for j in range(5)]
dops_32 = [o.conj().T for o in ops_32]
a_restricted, adag_restricted = [], []
for j in range(4):
    op_eig = evects_N4.conj().T @ ops_32[j] @ evects_N4
    dop_eig = evects_N4.conj().T @ dops_32[j] @ evects_N4
    a_restricted.append(op_eig[np.ix_(idx_N4_0, idx_N4_0)])
    adag_restricted.append(dop_eig[np.ix_(idx_N4_0, idx_N4_0)])

A_all = np.vstack([ops_32[j] for j in range(5)])
_, _, Vh = np.linalg.svd(A_all, full_matrices=False)
vac_32 = Vh[-1,:].conj().reshape(32, 1) / np.linalg.norm(Vh[-1,:])
vac_eig = evects_N4.conj().T @ vac_32
vac_N4_0 = vac_eig[np.ix_(idx_N4_0)]
vac_A1 = (vac_N4_0 / np.linalg.norm(vac_N4_0)).reshape(16, 1)

fock_A1 = {}
for bits in product([0,1],repeat=4):
    v = vac_A1.copy()
    for j in range(4):
        if bits[j]: v = adag_restricted[j] @ v
    norm = np.sqrt(v.conj().T @ v).item()
    if isinstance(norm, complex): norm = norm.real
    if abs(norm) > 1e-10: v = v / norm
    fock_A1[bits] = v

F_g = np.hstack([fock_g[bits] for bits in product([0,1],repeat=4)])
F_A1 = np.hstack([fock_A1[bits] for bits in product([0,1],repeat=4)])
S = F_g @ np.linalg.pinv(F_A1)
S_inv = np.linalg.inv(S)

# psi_3 in Gresnigt rep
def eprod_eg(*indices):
    out = I16
    for i in indices: out = out @ eg[i]
    return out

B_g = {
    0: -eprod_eg(1,2,3,4)+eprod_eg(1,2,5,6)+eprod_eg(3,4,5,6),
    1: eprod_eg(0,2,3,5)+eprod_eg(0,2,4,6)+eprod_eg(3,4,5,6),
    2: eprod_eg(0,1,4,5)-eprod_eg(0,1,3,6)+eprod_eg(3,4,5,6),
    3: eprod_eg(0,1,4,5)+eprod_eg(0,2,4,6)+eprod_eg(1,2,5,6),
    4: -eprod_eg(0,1,3,6)+eprod_eg(0,2,3,5)+eprod_eg(1,2,5,6),
    5: -eprod_eg(0,1,3,6)+eprod_eg(0,2,4,6)-eprod_eg(1,2,3,4),
    6: eprod_eg(0,1,4,5)+eprod_eg(0,2,3,5)-eprod_eg(1,2,3,4),
}

g_g = {}
for i in range(7):
    g_g[i] = 0.5 * eg[i] @ eg[7] @ (B_g[i] - I16)

sqrt3 = np.sqrt(3)
psi3_eg = {}
for i in range(7):
    psi3_eg[i] = (0.25*eg[i] + (sqrt3/4)*g_g[i] - (sqrt3/4)*(eg[i]@eg[7]) - 0.75*(g_g[i]@eg[7]))
psi3_eg[7] = eg[7]

# Transport to Phase A1
blade_subsets_8 = [list(c) for k in range(9) for c in combinations(range(8), k)]
blades_orig_g = []
blades_psi3_g = []
for s in blade_subsets_8:
    bl = I16; im = I16
    for i in s: bl = bl @ eg[i]; im = im @ psi3_eg[i]
    blades_orig_g.append(bl)
    blades_psi3_g.append(im)

def apply_auto_g(X, bim):
    out = zeros((16,16), dtype=complex)
    for bl, im in zip(blades_orig_g, bim):
        c = np.trace(bl.conj().T @ X) / 16.0
        if abs(c) > 1e-12: out = out + c * im
    return out

psi3_gen_A1 = [S_inv @ apply_auto_g(S @ ga[i] @ S_inv, blades_psi3_g) @ S for i in range(8)]

# =====================================================================
# Attempt 1: Solve for U in Gresnigt rep (16x16)
# =====================================================================
print('\n--- Attempt 1: U in Gresnigt representation (16x16) ---')

# Solve U @ eg[i] = psi3_eg[i] @ U for i=0..7
A_U_g = np.vstack([np.kron(psi3_eg[i].T, I16) - np.kron(I16, eg[i]) for i in range(8)])
_, s_g, Vh_g = np.linalg.svd(A_U_g, full_matrices=False)
null_g = np.sum(s_g < 1e-6)
print(f'Gresnigt rep nullspace: {null_g}')

if null_g >= 1:
    # Find the best U_g that satisfies all 8 equations
    best_U_g = Vh_g[-1, :].reshape(16, 16)
    # Normalize to make unitary
    UU = best_U_g @ best_U_g.conj().T
    ev = np.linalg.eigvalsh(UU)
    scale = np.sqrt(np.max(ev))
    if scale > 1e-10:
        best_U_g = best_U_g / scale
    err_g = max(np.max(np.abs(best_U_g @ eg[i] - psi3_eg[i] @ best_U_g)) for i in range(8))
    unit_err_g = np.linalg.norm(best_U_g @ best_U_g.conj().T - I16)
    print(f'Best U_g: impl err={err_g:.2e}, unitarity err={unit_err_g:.2e}')
    
    # Transport to Phase A1: U_A1 = S^{-1} @ U_g @ S
    if err_g < 1e-4 and unit_err_g < 1e-4:
        U_A1_0 = S_inv @ best_U_g @ S
        # Verify on Phase A1 N4=0 generators
        err_A1_0 = max(np.max(np.abs(U_A1_0 @ ga[i] - psi3_gen_A1[i] @ U_A1_0)) for i in range(8))
        print(f'Transported U on N4=0: err={err_A1_0:.2e}')
        
        # Build psi_3 images on 32x32 (same psi_3 on both subspaces — equivalent reps)
        psi3_G_32 = []
        for i in range(8):
            blk = zeros((32, 32), dtype=complex)
            blk[np.ix_(idx_N4_0, idx_N4_0)] = psi3_gen_A1[i]
            blk[np.ix_(idx_N4_1, idx_N4_1)] = psi3_gen_A1[i]
            psi3_G_32.append(evects_N4 @ blk @ evects_N4.conj().T)
        psi3_G_32.append(G[8].copy())
        psi3_G_32.append(G[9].copy())
        
        # Lift U to full 32x32
        U_A1_blk = zeros((32, 32), dtype=complex)
        U_A1_blk[np.ix_(idx_N4_0, idx_N4_0)] = U_A1_0
        U_A1_blk[np.ix_(idx_N4_1, idx_N4_1)] = U_A1_0
        U_32 = evects_N4 @ U_A1_blk @ evects_N4.conj().T
        
        err_32 = max(np.max(np.abs(U_32 @ G[i] - psi3_G_32[i] @ U_32)) for i in range(10))
        unit_err_32 = np.linalg.norm(U_32 @ U_32.conj().T - I32)
        print(f'Lifted to 32x32: impl err={err_32:.2e}, unitarity err={unit_err_32:.2e}')
        
        if err_32 < 1e-4 and unit_err_32 < 1e-4:
            print('\n*** SUCCESS: U_psi3 found! ***')
            
            # Build S3 orbit from vacuum
            vac_ref = vac_32.copy()
            
            gen1 = vac_ref
            gen2 = U_32 @ gen1
            gen3 = U_32 @ U_32 @ gen1
            
            orbit = np.hstack([gen1, gen2, gen3])
            rank = np.linalg.matrix_rank(orbit, tol=1e-6)
            print(f'S3 orbit rank: {rank}/3')
            
            sum_gen = gen1 + gen2 + gen3
            psi3_sum = U_32 @ sum_gen
            overlap = np.abs(psi3_sum.conj().T @ sum_gen).item()
            print(f'<psi_3(sum)|sum> overlap: {overlap:.4f}')
        else:
            print('Lift failed: G[8],G[9] anticommutation breaks the 32x32 extension')
    else:
        print('U_g not clean enough')
else:
    print('No nullspace for U_g in Gresnigt rep')

# =====================================================================
# Attempt 2: Direct solve on Phase A1 N4=0 with SVD
# =====================================================================
print('\n--- Attempt 2: Direct solve on Phase A1 N4=0 ---')

A_U_A1 = np.vstack([np.kron(psi3_gen_A1[i].T, I16) - np.kron(I16, ga[i]) for i in range(8)])
_, s_A1, Vh_A1 = np.linalg.svd(A_U_A1, full_matrices=False)
null_A1 = np.sum(s_A1 < 1e-6)
print(f'Phase A1 N4=0 nullspace: {null_A1}')

if null_A1 >= 1:
    best_U_A1 = Vh_A1[-1, :].reshape(16, 16)
    UU = best_U_A1 @ best_U_A1.conj().T
    ev = np.linalg.eigvalsh(UU)
    scale = np.sqrt(np.max(ev))
    if scale > 1e-10:
        best_U_A1 = best_U_A1 / scale
    err_A1 = max(np.max(np.abs(best_U_A1 @ ga[i] - psi3_gen_A1[i] @ best_U_A1)) for i in range(8))
    unit_err_A1 = np.linalg.norm(best_U_A1 @ best_U_A1.conj().T - I16)
    print(f'Best U_A1: impl err={err_A1:.2e}, unitarity err={unit_err_A1:.2e}')
else:
    print('No nullspace — U does not exist even on N4=0')

print('\nDone.')
