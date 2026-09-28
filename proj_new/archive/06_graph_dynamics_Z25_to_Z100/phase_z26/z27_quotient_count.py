"""
Fixed Polya count. The error: class_size returns |class| (an integer), and
the unlabeled count is (1/|S_N|) * sum_over_classes |class| * (#fixed
M-subsets). So I must divide the accumulated sum by N! exactly.
Validation target: number of unlabeled graphs on 10 vertices is known:
  12,005,168  (OEIS A000088(10)).
I check that first (sum over all M), then extract M=15.
"""
import math
from collections import defaultdict
import sympy as sp

x = sp.Symbol('x')

def partitions(n, mx=None):
    if mx is None: mx = n
    if n == 0: yield []; return
    for first in range(min(n, mx), 0, -1):
        for rest in partitions(n - first, first):
            yield [first] + rest

def edge_cycle_poly(cyc):
    poly = sp.Integer(1)
    for r in cyc:
        if r == 1: continue
        if r % 2 == 1:
            for _ in range((r - 1)//2):
                poly *= (1 + x**r)
        else:
            for _ in range((r - 2)//2):
                poly *= (1 + x**r)
            poly *= (1 + x**(r // 2))
    for i in range(len(cyc)):
        for j in range(i + 1, len(cyc)):
            r, s = cyc[i], cyc[j]
            g = math.gcd(r, s); l = (r * s) // g
            for _ in range(g):
                poly *= (1 + x**l)
    return poly

def class_size(cyc, n):
    cnt = defaultdict(int)
    for c in cyc: cnt[c] += 1
    denom = 1
    for length, mult in cnt.items():
        denom *= (length ** mult) * math.factorial(mult)
    return math.factorial(n) // denom

def cycle_index_polynomial(N):
    tot = sp.Integer(0)
    for cyc in partitions(N):
        tot = tot + class_size(cyc, N) * sp.expand(edge_cycle_poly(cyc))
    return tot  # divide by N! at the end

def sq_free(lam): return lam  # alias

def main():
    N = 10; M = 15
    Z = cycle_index_polynomial(N)
    Z = sp.expand(Z)
    tot_coeff = sum(Z.coeff(x, k) for k in range(sp.degree(Z, x) + 1))
    n_graphs = tot_coeff // math.factorial(N)
    n_15 = Z.coeff(x, M) // math.factorial(N)
    print("unlabeled graphs N=10 (all edges):", n_graphs, " expected 12005168")
    print("unlabeled graphs N=10, M=15        :", n_15)
    labeled = math.comb(45, 15)
    I_lab = math.log2(labeled)
    I_unlab = math.log2(int(n_15))
    print(f"I_labeled   = {I_lab:.4f} bits")
    print(f"I_quotient  = {I_unlab:.4f} bits")
    print(f"relabel loss = {I_lab - I_unlab:.4f} bits  (should be ~ log2 10! = {math.log2(math.factorial(10)):.4f})")

if __name__ == "__main__":
    main()
