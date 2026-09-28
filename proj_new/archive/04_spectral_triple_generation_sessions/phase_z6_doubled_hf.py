"""
Phase Z6 (this session) -- Reproducible script for RESULT_phase_z6.md.

Builds the doubled H_F = C^16 (+) C^16 scaffolding recommended in
RESULT_phase_z5.md (grading eps by construction, real structure J0 =
swap-and-conjugate) and checks the KO-dimension-type axioms against
the actual physical Yukawa tensors M10[0], M120, M126 (not generic
random matrices), plus a control run with a generic random Y.
"""
import os
import numpy as np
from itertools import combinations, permutations
import math

N = 32
I16 = np.eye(16, dtype=complex)
EPS = np.block([[I16, np.zeros((16, 16))], [np.zeros((16, 16)), -I16]])
P = np.block([[np.zeros((16, 16)), I16], [I16, np.zeros((16, 16))]])


def J0(psi):
    return P @ psi.conjugate()


def load_gammas():
    return [np.load(os.path.join(os.path.dirname(__file__), f'gamma_{i}.npy'))
            for i in range(10)]


def build_C_mat(G):
    I32 = np.eye(N, dtype=complex)
    A_stack = []
    for a in range(10):
        A = np.kron(G[a].T, I32) + np.kron(I32, G[a].T)
        A_stack.append(A)
    A_stack = np.vstack(A_stack)
    U, s, Vh = np.linalg.svd(A_stack, full_matrices=False)
    C_mat = Vh[-1].reshape(32, 32)
    return C_mat / np.max(np.abs(C_mat))


def gamma_prod(G, indices):
    k = len(indices)
    I32 = np.eye(N, dtype=complex)
    if k == 0:
        return I32
    result = np.zeros((N, N), dtype=complex)
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


def embed_doubled(Y):
    return np.block([[np.zeros((16, 16)), Y], [Y.conj().T, np.zeros((16, 16))]])


def check_component(name, Y, psi):
    D_F = embed_doubled(Y)
    anti_grading = EPS @ D_F + D_F @ EPS
    lhs = J0(D_F @ psi)
    rhs = D_F @ J0(psi)
    ok_plus = np.allclose(lhs, rhs, atol=1e-8)
    ok_minus = np.allclose(lhs, -rhs, atol=1e-8)
    print(f'--- {name} ---')
    print(f'  ||{{eps,D_F}}|| = {np.linalg.norm(anti_grading):.2e}  (grading axiom)')
    print(f'  ||Y-Y^T||={np.linalg.norm(Y - Y.T):.2e}  ||Y+Y^T||={np.linalg.norm(Y + Y.T):.2e}'
          f'  Im(Y)={np.linalg.norm(Y - Y.conj()):.2e}')
    print(f'  J0 D_F == +D_F J0 ? {ok_plus}   J0 D_F == -D_F J0 ? {ok_minus}')


def run():
    G = load_gammas()
    Gamma_F = (1j ** 5) * G[0] @ G[1] @ G[2] @ G[3] @ G[4] @ G[5] @ G[6] @ G[7] @ G[8] @ G[9]
    w, v = np.linalg.eigh(Gamma_F)
    V = v[:, w.real > 0]
    C_mat = build_C_mat(G)

    rng = np.random.default_rng(0)
    psi = rng.normal(size=32) + 1j * rng.normal(size=32)

    # J0^2 check
    print('J0^2 psi / psi (expect constant +1):', np.round((J0(J0(psi)) / psi)[:3], 4))
    # J0 vs eps
    lhs = J0(EPS @ psi)
    rhs = EPS @ J0(psi)
    print('J0(eps psi) == -eps(J0 psi) ?', np.allclose(lhs, -rhs))
    print()

    Y10 = V.conj().T @ (C_mat @ G[0]) @ V
    check_component('M10[0]', Y10, psi)

    for t in [(0, 1, 2), (0, 1, 3)]:
        Y120 = V.conj().T @ (C_mat @ gamma_prod(G, t)) @ V
        check_component(f'M120 triple {t}', Y120, psi)

    n, k = 10, 5
    forms5 = list(combinations(range(n), k))
    n5 = len(forms5)

    def eps_sign(tup):
        if len(set(tup)) != n:
            return 0
        parity = 1
        for i in range(n):
            for j in range(i + 1, n):
                if tup[i] > tup[j]:
                    parity *= -1
        return parity

    Hodge = np.zeros((n5, n5))
    for i, fi in enumerate(forms5):
        for j, fj in enumerate(forms5):
            val = eps_sign(tuple(fj) + tuple(fi))
            if val != 0:
                Hodge[i, j] = float(val)
    P_sd = (np.eye(n5) - 1j * Hodge) / 2
    gamma5_list = [gamma_prod(G, t) for t in forms5]
    Usvd, ssvd, Vhsvd = np.linalg.svd(P_sd)
    onb = Usvd[:, :2]
    for jj in range(2):
        g5 = sum(onb[kk, jj] * gamma5_list[kk] for kk in range(n5))
        Y126 = (V.conj().T @ (C_mat @ g5) @ V) / np.sqrt(2)
        check_component(f'M126 onb component {jj}', Y126, psi)

    # control: generic random Y
    Yr = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16))
    check_component('CONTROL: generic random Y', Yr, psi)


if __name__ == '__main__':
    run()
