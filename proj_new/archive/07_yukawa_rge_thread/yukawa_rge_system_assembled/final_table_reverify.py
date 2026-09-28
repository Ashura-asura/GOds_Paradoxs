import numpy as np

np.set_printoptions(precision=6, suppress=True, linewidth=140)

data = np.load('M_matrices.npz')
M10 = list(data['M10']); M120 = list(data['M120'])
M126 = list(data['M126_greedy'])

channels = {'10': M10, '120': M120, '126': M126}

def vertex_sum(Mb_list, Xdag):
    S = np.zeros_like(Xdag)
    for Mb in Mb_list:
        S = S + Mb @ Xdag @ Mb
    return S

def lam(Rb_name, Ra_name):
    Mb_list = channels[Rb_name]
    Ma_list = channels[Ra_name]
    ratios = []
    max_resid = 0.0
    for Ma in Ma_list:
        Xdag = Ma.conj().T
        S = vertex_sum(Mb_list, Xdag)
        denom = np.trace(Ma.conj().T @ Ma)
        lam_a = np.trace(Ma.conj().T @ S) / denom
        resid = np.max(np.abs(S - lam_a * Ma))
        ratios.append(lam_a)
        max_resid = max(max_resid, resid)
    ratios = np.array(ratios)
    return ratios.mean(), ratios.std(), max_resid

print("Full lambda(R_b, R_a) table re-derivation, fresh from stored M matrices")
print(f"{'R_b\\R_a':>8} {'10':>14} {'120':>14} {'126':>14}")
for Rb in ['10', '120', '126']:
    row = []
    for Ra in ['10', '120', '126']:
        mean, std, resid = lam(Rb, Ra)
        row.append(f"{mean.real:8.4f}(±{std:.1e})")
    print(f"{Rb:>8} " + " ".join(f"{x:>14}" for x in row))

print("\nSelf-energy Schur constants T(R) = sum_a M_a M_a^dagger (should be dim(R)*I16)")
for name, Mlist in channels.items():
    T = sum(Ma @ Ma.conj().T for Ma in Mlist)
    diag = np.diag(T)
    offdiag = T - np.diag(diag)
    print(f"T({name}): diag range ({diag.real.min():.6f},{diag.real.max():.6f}), "
          f"max|offdiag|={np.max(np.abs(offdiag)):.2e}, dim({name})={len(Mlist)}")

print("\nTrace-term gauge normalization tr(M_a^dagger M_b) = 16 delta_ab within each channel (spot check a=b=0)")
for name, Mlist in channels.items():
    print(f"{name}: tr(M_0^dag M_0) = {np.trace(Mlist[0].conj().T @ Mlist[0]).real:.6f}")

print("\nSymmetry type check: M = +M^T (10,126) or M = -M^T (120)")
for name, Mlist in channels.items():
    max_sym_resid = max(np.max(np.abs(Ma - Ma.T)) for Ma in Mlist)
    max_antisym_resid = max(np.max(np.abs(Ma + Ma.T)) for Ma in Mlist)
    print(f"{name}: max|M-M^T| = {max_sym_resid:.2e}  max|M+M^T| = {max_antisym_resid:.2e}")
