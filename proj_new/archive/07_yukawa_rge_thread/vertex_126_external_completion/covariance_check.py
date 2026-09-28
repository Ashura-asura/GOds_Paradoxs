import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

data = np.load('M_matrices.npz')
M10 = list(data['M10']); M120 = list(data['M120'])
M126_greedy = list(data['M126_greedy']); M126_onb = list(data['M126_onb'])

gendata = np.load('so10_generators.npz')
P_L = gendata['P_L']

# rebuild V (same construction as compute script)
w, v = np.linalg.eigh(P_L @ P_L.conj().T)
idx = np.argsort(-w.real)[:16]
V = v[:, idx]

def restrict(Sigma32):
    return V.conj().T @ Sigma32 @ V

# grab a couple of generators
gen_keys = ['Sigma_0_1', 'Sigma_2_5', 'Sigma_4_7']
Ts = [restrict(gendata[k]) for k in gen_keys]

def rep_rotation_matrix(T, Mlist):
    """Solve [T, M_a] = sum_c R_ac M_c using the tr(M_c^dag . )/16 orthogonality projector."""
    n = len(Mlist)
    R = np.zeros((n, n), dtype=complex)
    for a in range(n):
        comm = T @ Mlist[a] - Mlist[a] @ T
        for c in range(n):
            R[a, c] = np.trace(Mlist[c].conj().T @ comm) / 16.0
    # residual: how well does comm reconstruct from the M-basis (checks Mlist spans closed subspace)
    resid = 0.0
    for a in range(n):
        comm = T @ Mlist[a] - Mlist[a] @ T
        recon = sum(R[a, c] * Mlist[c] for c in range(n))
        resid = max(resid, np.max(np.abs(comm - recon)))
    return R, resid

def vertex_sum(Mb_list, Xdag):
    S = np.zeros_like(Xdag)
    for Mb in Mb_list:
        S = S + Mb @ Xdag @ Mb
    return S

def check_covariance(T, Mb_list, Ma_list, label):
    n = len(Ma_list)
    R, resid_rep = rep_rotation_matrix(T, Ma_list)
    # build S_a for all a
    Slist = [vertex_sum(Mb_list, Ma_list[a].conj().T) for a in range(n)]
    max_cov_resid = 0.0
    for a in range(n):
        lhs = T @ Slist[a] - Slist[a] @ T          # [T, S_a]
        rhs = sum(R[a, c] * Slist[c] for c in range(n))  # sum_c R_ac S_c
        max_cov_resid = max(max_cov_resid, np.max(np.abs(lhs - rhs)))
    print(f"{label}: generator-closure residual (M-basis) = {resid_rep:.3e}, "
          f"covariance residual [T,S_a] vs sum R_ac S_c = {max_cov_resid:.3e}")
    return max_cov_resid

print("=== Sanity: known nonzero case lambda(10,10) = -8, check covariance ===")
for gk, T in zip(gen_keys, Ts):
    check_covariance(T, M10, M10, f"(10,10) under {gk}")

print("\n=== Case A: lambda(10,126)=0, covariance of S_a (should be identically zero => trivially covariant) ===")
for gk, T in zip(gen_keys, Ts):
    check_covariance(T, M10, M126_greedy, f"(10,126) greedy under {gk}")
    check_covariance(T, M10, M126_onb, f"(10,126) onb under {gk}")

print("\n=== Case B: lambda(120,126)=0, covariance of S_a ===")
for gk, T in zip(gen_keys, Ts):
    check_covariance(T, M120, M126_greedy, f"(120,126) greedy under {gk}")
    check_covariance(T, M120, M126_onb, f"(120,126) onb under {gk}")

print("\n=== Direct magnitude check: max|S_a| itself for case A/B (confirms identically zero, not just 'proportional to zero') ===")
for Mb_list, Ma_list, label in [(M10, M126_greedy, "10->126 greedy"),
                                  (M10, M126_onb, "10->126 onb"),
                                  (M120, M126_greedy, "120->126 greedy"),
                                  (M120, M126_onb, "120->126 onb")]:
    mx = 0.0
    for Ma in Ma_list:
        S = vertex_sum(Mb_list, Ma.conj().T)
        mx = max(mx, np.max(np.abs(S)))
    print(f"{label}: max|S_a| entrywise over all a = {mx:.3e}")
