import numpy as np
from itertools import combinations, permutations
import math

G = [np.load(f'gamma_{i}.npy') for i in range(10)]
I32 = np.eye(32, dtype=complex)
data = np.load('so10_generators.npz')
Gamma_F = data['Gamma_F']
P_L = data['P_L']; P_R = data['P_R']

print("Gamma_F^2 = I:", np.max(np.abs(Gamma_F@Gamma_F - I32)))
print("P_L+P_R=I:", np.max(np.abs(P_L+P_R-I32)))
print("rank P_L:", np.linalg.matrix_rank(P_L), "rank P_R:", np.linalg.matrix_rank(P_R))

# Build V: 32x16 orthonormal basis of P_L eigenspace
w, v = np.linalg.eigh(P_L @ P_L.conj().T)  # P_L should be a projector (Hermitian idempotent)
# check hermiticity
print("P_L hermitian?", np.max(np.abs(P_L - P_L.conj().T)))
idx = np.argsort(-w.real)[:16]
V = v[:, idx]
# orthonormality
print("V†V=I16:", np.max(np.abs(V.conj().T@V - np.eye(16))))
# confirm it's the P_L eigenspace
print("P_L V = V:", np.max(np.abs(P_L@V - V)))

def gamma_prod(indices):
    k = len(indices)
    if k == 0: return I32
    result = np.zeros((32, 32), dtype=complex)
    idx_list = list(indices)
    for perm in permutations(idx_list):
        sign = 1
        for i in range(k):
            for j in range(i + 1, k):
                if idx_list.index(perm[i]) > idx_list.index(perm[j]):
                    sign *= -1
        prod = I32
        for idx_ in perm:
            prod = prod @ G[idx_]
        result = result + sign * prod
    return result / math.factorial(k)

# charge conjugation via SVD method (eta=-1)
A_stack = []
for a in range(10):
    A = np.kron(G[a].T, I32) + np.kron(I32, G[a].T)
    A_stack.append(A)
A_stack = np.vstack(A_stack)
U, s, Vh = np.linalg.svd(A_stack, full_matrices=False)
C_flat = Vh[-1]
C_mat = C_flat.reshape(32, 32)
C_mat = C_mat / np.max(np.abs(C_mat))
C_inv = np.linalg.inv(C_mat)
C_err = max(np.max(np.abs(C_mat @ G[a] @ C_inv + G[a].T)) for a in range(10))
print("C build err:", C_err)
print("[Gamma_F, C] commutator norm:", np.max(np.abs(Gamma_F@C_mat - C_mat@Gamma_F)))
print("{Gamma_F, C} anticommutator norm:", np.max(np.abs(Gamma_F@C_mat + C_mat@Gamma_F)))

def blocks(M):
    # LL, LR, RL, RR blocks of V†MV*, but M acts 32x32; project properly
    LL = V.conj().T @ M @ V
    return LL

# Need P_R basis too
w2, v2 = np.linalg.eigh(P_R @ P_R.conj().T)
idx2 = np.argsort(-w2.real)[:16]
Vr = v2[:, idx2]
print("Vr†Vr=I16:", np.max(np.abs(Vr.conj().T@Vr - np.eye(16))))
print("P_R Vr = Vr:", np.max(np.abs(P_R@Vr - Vr)))

def all_blocks(M, name):
    LL = V.conj().T @ M @ V
    LR = V.conj().T @ M @ Vr
    RL = Vr.conj().T @ M @ V
    RR = Vr.conj().T @ M @ Vr
    print(f"{name}: |LL|={np.max(np.abs(LL)):.3e}  |LR|={np.max(np.abs(LR)):.3e}  |RL|={np.max(np.abs(RL)):.3e}  |RR|={np.max(np.abs(RR)):.3e}")

CG_10_0 = C_mat @ G[0]
CG_10_3 = C_mat @ G[3]
print()
print("=== Cgamma_a (vector, a=0,3) ===")
all_blocks(CG_10_0, "Cgamma_0")
all_blocks(CG_10_3, "Cgamma_3")

g012 = gamma_prod((0,1,2))
CG_120_012 = C_mat @ g012
print()
print("=== Cgamma_abc (3-form, (0,1,2)) ===")
all_blocks(CG_120_012, "Cgamma_012")

# also directly check anticommutator with Gamma_F for these specific matrices
print()
print("--- anticommutator with Gamma_F (should be 0 if grade is odd, per Clifford parity) ---")
for name, M in [("Cgamma_0", CG_10_0), ("Cgamma_3", CG_10_3), ("Cgamma_012", CG_120_012)]:
    ac = np.max(np.abs(Gamma_F@M + M@Gamma_F))
    co = np.max(np.abs(Gamma_F@M - M@Gamma_F))
    print(f"{name}: anticommutator={ac:.3e}  commutator={co:.3e}")
