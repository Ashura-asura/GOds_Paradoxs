import numpy as np
from itertools import combinations, permutations
import math

np.set_printoptions(precision=6, suppress=True, linewidth=140)

G = [np.load(f'gamma_{i}.npy') for i in range(10)]
I32 = np.eye(32, dtype=complex)
data = np.load('so10_generators.npz')
Gamma_F = data['Gamma_F']; P_L = data['P_L']; P_R = data['P_R']
Sigma_ab = None
# generators: try to find 45 antisymmetric SO(10) generators in the npz
print("npz keys:", list(data.keys()))

# V: 16-dim chiral (L) basis
w, v = np.linalg.eigh(P_L @ P_L.conj().T)
idx = np.argsort(-w.real)[:16]
V = v[:, idx]
print("V dagger V = I16 check:", np.max(np.abs(V.conj().T @ V - np.eye(16))))

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
        for ii in perm:
            prod = prod @ G[ii]
        result = result + sign * prod
    return result / math.factorial(k)

# C via SVD method (same as project scripts)
A_stack = []
for a in range(10):
    A = np.kron(G[a].T, I32) + np.kron(I32, G[a].T)
    A_stack.append(A)
A_stack = np.vstack(A_stack)
U, s, Vh = np.linalg.svd(A_stack, full_matrices=False)
C_mat = Vh[-1].reshape(32, 32)
C_mat = C_mat / np.max(np.abs(C_mat))
C_inv = np.linalg.inv(C_mat)
C_err = max(np.max(np.abs(C_mat @ G[a] @ C_inv + G[a].T)) for a in range(10))
print("C build err:", C_err)

# ---- 10, 120 ----
M10 = [V.conj().T @ (C_mat @ G[a]) @ V for a in range(10)]
idx3 = list(combinations(range(10), 3))
gamma3 = {t: gamma_prod(t) for t in idx3}
M120 = [V.conj().T @ (C_mat @ gamma3[t]) @ V for t in idx3]

# ---- 126: self-dual 5-forms ----
n, k = 10, 5
forms5 = list(combinations(range(n), k))
n5 = len(forms5)
def eps_sign(tup):
    if len(set(tup)) != n: return 0
    parity = 1
    for i in range(n):
        for j in range(i+1, n):
            if tup[i] > tup[j]: parity *= -1
    return parity
Hodge = np.zeros((n5, n5))
for i, fi in enumerate(forms5):
    for j, fj in enumerate(forms5):
        val = eps_sign(tuple(fj) + tuple(fi))
        if val != 0: Hodge[i, j] = float(val)
P_sd = (np.eye(n5) - 1j*Hodge)/2
gamma5_list = [gamma_prod(t) for t in forms5]

# GREEDY basis (matches original project script / Gram-Schmidt)
sd_cols = []
for cidx in range(n5):
    vv = P_sd[:, cidx]
    if np.linalg.norm(vv) > 1e-10:
        vv = vv/np.linalg.norm(vv)
        indep = all(abs(np.vdot(ex, vv)) < 0.99 for ex in sd_cols)
        if indep:
            sd_cols.append(vv)
        if len(sd_cols) == 126: break
gamma5_sd_greedy = [sum(vv[kk]*gamma5_list[kk] for kk in range(n5) if abs(vv[kk])>1e-12) for vv in sd_cols]
M126_greedy = [ (V.conj().T @ (C_mat @ g5) @ V) / np.sqrt(2) for g5 in gamma5_sd_greedy ]

# ORTHONORMAL / SVD basis (independent basis choice for basis-independence check)
Usvd, ssvd, Vhsvd = np.linalg.svd(P_sd)
onb = Usvd[:, :126]
gamma5_sd_onb = [sum(onb[kk, jj]*gamma5_list[kk] for kk in range(n5)) for jj in range(126)]
M126_onb = [ (V.conj().T @ (C_mat @ g5) @ V) / np.sqrt(2) for g5 in gamma5_sd_onb ]

print("\n=== Normalization checks (Hermitian pairing tr(M_a^dag M_b) = 16 delta_ab) ===")
def norm_check(name, Mlist):
    n_ = len(Mlist)
    Gd = np.array([[np.trace(Mlist[i].conj().T @ Mlist[j]) for j in range(n_)] for i in range(n_)])
    diag = np.diag(Gd)
    offdiag = Gd - np.diag(diag)
    print(f"{name}: diag range ({diag.real.min():.6f},{diag.real.max():.6f}), max|offdiag|={np.max(np.abs(offdiag)):.3e}")
    return Gd

norm_check("M10", M10)
norm_check("M120", M120)
norm_check("M126_greedy", M126_greedy)
norm_check("M126_onb", M126_onb)

print("\n=== Cross-channel orthogonality (10-126, 120-126) ===")
def cross(name, A, B):
    mx = max(abs(np.trace(a.conj().T @ b)) for a in A for b in B)
    print(f"{name}: max|tr(A^dag B)| = {mx:.3e}")
cross("10 x 126_greedy", M10, M126_greedy)
cross("120 x 126_greedy", M120, M126_greedy)

# ---- Case A: S_a = sum_{b in 10} M_b^(10) M_a^(126)^dagger M_b^(10) ----
print("\n" + "="*70)
print("CASE A: internal 10, external 126 (using greedy 126 basis)")
print("="*70)

def vertex_sum(Mb_list, Xdag):
    S = np.zeros_like(Xdag)
    for Mb in Mb_list:
        S = S + Mb @ Xdag @ Mb
    return S

def analyze_case(Mb_list, Ma_list, label):
    ratios = []
    max_resid = 0.0
    for a_idx, Ma in enumerate(Ma_list):
        Xdag = Ma.conj().T
        S = vertex_sum(Mb_list, Xdag)
        # project ratio via trace against Ma (Schur candidate scalar)
        denom = np.trace(Ma.conj().T @ Ma)
        if abs(denom) < 1e-14:
            continue
        lam_a = np.trace(Ma.conj().T @ S) / denom
        resid = np.max(np.abs(S - lam_a * Ma))
        ratios.append(lam_a)
        max_resid = max(max_resid, resid)
    ratios = np.array(ratios)
    print(f"{label}: lambda per-component -> mean={ratios.mean():.6f}, std={ratios.std():.3e}, "
          f"min={ratios.real.min():.6f}, max={ratios.real.max():.6f}")
    print(f"  max residual ||S_a - lambda*M_a|| over all a = {max_resid:.3e}")
    return ratios, max_resid

ratiosA, residA = analyze_case(M10, M126_greedy, "lambda(10,126) [greedy basis]")

print("\n" + "="*70)
print("CASE B: internal 120, external 126 (using greedy 126 basis)")
print("="*70)
ratiosB, residB = analyze_case(M120, M126_greedy, "lambda(120,126) [greedy basis]")

print("\n" + "="*70)
print("BASIS INDEPENDENCE CHECK: repeat with SVD/orthonormal 126 basis")
print("="*70)
ratiosA_onb, residA_onb = analyze_case(M10, M126_onb, "lambda(10,126) [SVD/onb basis]")
ratiosB_onb, residB_onb = analyze_case(M120, M126_onb, "lambda(120,126) [SVD/onb basis]")

print("\n" + "="*70)
print("SANITY: recompute known real-real entries to confirm machinery matches prior session")
print("="*70)
analyze_case(M10, M10, "lambda(10,10) [expect -8]")
analyze_case(M10, M120, "lambda(10,120) [expect 4]")
analyze_case(M120, M10, "lambda(120,10) [expect 48]")
analyze_case(M120, M120, "lambda(120,120) [expect 8]")

print("\n" + "="*70)
print("CONTROL: verify we are NOT accidentally computing sum M_b X M_b^dagger")
print("="*70)
def vertex_sum_wrong(Mb_list, X):
    S = np.zeros_like(X)
    for Mb in Mb_list:
        S = S + Mb @ X @ Mb.conj().T
    return S
# for a=0 in 126, compare correct vs wrong construction
X0 = M126_greedy[0].conj().T
S_correct = vertex_sum(M10, X0)
S_wrong = vertex_sum_wrong(M10, M126_greedy[0])
print("max|S_correct - S_wrong| (should generally differ, confirming distinctness):",
      np.max(np.abs(S_correct - S_wrong)))

np.savez('M_matrices.npz',
         M10=np.array(M10), M120=np.array(M120),
         M126_greedy=np.array(M126_greedy), M126_onb=np.array(M126_onb))
print("\nSaved M matrices to M_matrices.npz")
