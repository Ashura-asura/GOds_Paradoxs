"""
TASK 1 (flavor-selection phase): invariant subspaces of Sym^2(3) and
Lambda^2(3) under finite subgroups of SU(3)_f, acting via the triplet rep.

Method: build the finite group by closure from generators, compute the
group-averaged projector (1/|G|) sum_g rho(g) (x) rho(g) on C^3 (x) C^3,
restrict to the symmetric/antisymmetric sector, read off rank.
"""
import numpy as np


def invariant_count(gens, max_order=300):
    I = np.eye(3, dtype=complex)
    group = [I]
    frontier = [I]

    def key(M):
        return tuple(np.round(M.flatten(), 6))

    seen = {key(I)}
    while frontier:
        new_frontier = []
        for M in frontier:
            for g in gens:
                M2 = g @ M
                k = key(M2)
                if k not in seen:
                    seen.add(k)
                    group.append(M2)
                    new_frontier.append(M2)
        frontier = new_frontier
        if len(group) > max_order:
            print("truncated, order too large")
            break
    order = len(group)

    Swap = np.zeros((9, 9))
    idx = lambda i, j: 3 * i + j
    for i in range(3):
        for j in range(3):
            Swap[idx(i, j), idx(j, i)] = 1
    Sym_proj = (np.eye(9) + Swap) / 2
    Anti_proj = (np.eye(9) - Swap) / 2

    Avg = np.zeros((9, 9), dtype=complex)
    for g in group:
        Avg += np.kron(g, g)
    Avg /= order

    Sym_inv = Sym_proj @ Avg @ Sym_proj
    Anti_inv = Anti_proj @ Avg @ Anti_proj

    rank_sym = np.linalg.matrix_rank(Sym_inv, tol=1e-6)
    rank_anti = np.linalg.matrix_rank(Anti_inv, tol=1e-6)
    return order, rank_sym, rank_anti


if __name__ == "__main__":
    results = {}

    P12 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]], dtype=complex)
    P123 = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], dtype=complex)
    results['S3 (permutation 3)'] = invariant_count([P12, P123])

    S_a4 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=complex)
    T_a4 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    results['A4 (triplet)'] = invariant_count([S_a4, T_a4])

    a_ = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]], dtype=complex)
    b_ = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    c_ = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]], dtype=complex)
    results['S4 (triplet)'] = invariant_count([a_, b_, c_])

    w = np.exp(2j * np.pi / 3)
    Z3_clock = np.diag([1, w, w ** 2]).astype(complex)
    Z3_shift = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    results['Delta(27)'] = invariant_count([Z3_clock, Z3_shift])

    for name, (order, rs, ra) in results.items():
        print(f"{name}: |G|={order}, dim Sym^2(3)^G = {rs} (of 6), "
              f"dim Lambda^2(3)^G = {ra} (of 3)")
