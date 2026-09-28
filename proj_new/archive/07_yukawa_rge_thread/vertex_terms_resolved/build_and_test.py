import numpy as np
from itertools import combinations, permutations
import math

np.set_printoptions(precision=6, suppress=True, linewidth=140)

G = [np.load(f'gamma_{i}.npy') for i in range(10)]
I32 = np.eye(32, dtype=complex)
data = np.load('so10_generators.npz')
Gamma_F = data['Gamma_F']; P_L = data['P_L']; P_R = data['P_R']

# V: 16-dim chiral (L) basis
w, v = np.linalg.eigh(P_L @ P_L.conj().T)
idx = np.argsort(-w.real)[:16]
V = v[:, idx]

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

# C
A_stack = []
for a in range(10):
    A = np.kron(G[a].T, I32) + np.kron(I32, G[a].T)
    A_stack.append(A)
A_stack = np.vstack(A_stack)
U, s, Vh = np.linalg.svd(A_stack, full_matrices=False)
C_mat = Vh[-1].reshape(32, 32)
C_mat = C_mat / np.max(np.abs(C_mat))

# 10, 120
M10 = [V.conj().T @ (C_mat @ G[a]) @ V for a in range(10)]
idx3 = list(combinations(range(10), 3))
gamma3 = {t: gamma_prod(t) for t in idx3}
M120 = [V.conj().T @ (C_mat @ gamma3[t]) @ V for t in idx3]

# 126: self-dual 5-forms, GREEDY (non-canonical) basis as in original script
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

# GREEDY basis (as original script)
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

# ORTHONORMAL basis via QR/SVD of P_sd's column space (canonical-ish, still a choice, but orthonormal)
Usvd, ssvd, Vhsvd = np.linalg.svd(P_sd)
onb = Usvd[:, :126]   # orthonormal basis for the self-dual (rank 126) subspace
gamma5_sd_onb = [sum(onb[kk, jj]*gamma5_list[kk] for kk in range(n5)) for jj in range(126)]
M126_onb = [ (V.conj().T @ (C_mat @ g5) @ V) / np.sqrt(2) for g5 in gamma5_sd_onb ]

def check(name, Mlist):
    n_ = len(Mlist)
    # tr(M_k^dagger M_l) - should be 16 delta_kl (Frobenius/Hermitian pairing)
    G_dag = np.array([[np.trace(Mlist[i].conj().T @ Mlist[j]) for j in range(min(n_,6))] for i in range(6)])
    # tr(M_k M_l) - undaggered bilinear pairing - the one that matters for Sigma M X M
    G_bil = np.array([[np.trace(Mlist[i] @ Mlist[j]) for j in range(min(n_,6))] for i in range(6)])
    print(f'--- {name} ---')
    print('tr(M_k^dag M_l), k,l=0..5 (expect ~16*delta):')
    print(np.round(G_dag,3))
    print('tr(M_k M_l), k,l=0..5 (undaggered bilinear -- is it diagonal?):')
    print(np.round(G_bil,3))
    offdiag = G_bil - np.diag(np.diag(G_bil))
    print(f'max |off-diag tr(M_kM_l)| (first 6x6) = {np.max(np.abs(offdiag)):.4f}, max diag = {np.max(np.abs(np.diag(G_bil))):.4f}')
    print()

check('126 GREEDY (Gram-Schmidt-ish, non-orthonormal source)', M126_greedy)
check('126 ORTHONORMAL (SVD basis)', M126_onb)

def T_of_R(Mlist):
    S = sum(M @ M.conj().T for M in Mlist)
    d = np.diag(S)
    off = S - np.diag(d)
    return d.real, np.max(np.abs(off))

print('T(126) check (Sigma M_k M_k^dagger, should be dim(R)*I):')
d, off = T_of_R(M126_onb)
print('diag range:', d.min(), d.max(), 'max offdiag:', off)

def vertex_lambda_undaggered(Mlist_b, X):
    S = sum(M @ X @ M for M in Mlist_b)
    return S

# test lambda(126,126) in ONB basis for component 0
X0 = M126_onb[0].conj().T
S0 = vertex_lambda_undaggered(M126_onb, X0)
ratio = S0 / M126_onb[0]
finite = np.abs(M126_onb[0])>1e-6
print('lambda(126,126) test in ONB basis, component 0:')
print('ratio S/M126[0] where |M126[0]| significant:', ratio[finite][:10])
print('is it a clean constant?', np.std(ratio[finite].real), np.std(ratio[finite].imag))

# same test in greedy basis for comparison
X0g = M126_greedy[0].conj().T
S0g = vertex_lambda_undaggered(M126_greedy, X0g)
ratiog = S0g / M126_greedy[0]
finiteg = np.abs(M126_greedy[0])>1e-6
print()
print('lambda(126,126) test in GREEDY basis, component 0:')
print('ratio S/M126[0]:', ratiog[finiteg][:10])
print('is it a clean constant?', np.std(ratiog[finiteg].real), np.std(ratiog[finiteg].imag))
