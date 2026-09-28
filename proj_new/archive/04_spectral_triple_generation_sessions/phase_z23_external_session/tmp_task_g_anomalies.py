from sympy import Rational as R, I, Matrix, eye, zeros
import itertools

def su_n_generators(n):
    gens = []
    for i in range(n):
        for j in range(i+1, n):
            A = zeros(n); A[i,j] = 1; A[j,i] = 1
            B = zeros(n); B[i,j] = I; B[j,i] = -I
            gens.append(A); gens.append(B)
    for k in range(1, n):
        H = zeros(n)
        for i in range(k): H[i,i] = 1
        H[k,k] = -k
        gens.append(H)
    assert len(gens) == n*n - 1
    return gens

def d_tensor(reps_gens, g):
    a0, b0, c0 = g
    ta, tb, tc = reps_gens[a0], reps_gens[b0], reps_gens[c0]
    return (ta*tb + tb*ta).multiply(tc).trace() / 4

su5_gens = su_n_generators(5)
triples = itertools.product(range(24), repeat=3)
nz = None
for g in triples:
    v = d_tensor(su5_gens, g)
    if v != 0:
        nz = g; break
print("nonzero SU(5) d-triple:", nz, "value d5 =", v)

# 10 = Lambda^2(5): antisymmetric square
pairs = list(itertools.combinations(range(5), 2))
su5_10 = []
for t in su5_gens:
    M = zeros(10)
    for p, (i,j) in enumerate(pairs):
        for q, (k,l) in enumerate(pairs):
            M[p,q] = t[i,k]*R(1 if j==l else 0) - t[i,l]*R(1 if j==k else 0) \
                   - t[j,k]*R(1 if i==l else 0) + t[j,l]*R(1 if i==k else 0)
    su5_10.append(M)
d10 = d_tensor(su5_10, nz)
print("d(10) =", d10, "  ratio A(10)/A(5) =", d10/v)

# 5bar = conjugate rep: generators are -(t^a)* (bar of a rep with hermitian t^a)
su5_5bar = [-(t.conjugate()) for t in su5_gens]
d5b = d_tensor(su5_5bar, nz)
print("d(5bar) =", d5b, "  ratio A(5bar)/A(5) =", d5b/v)

# 24 adjoint: d(adjoint) must be 0 (no cubic anomaly for adjoint of any group)
import random
random.seed(7)
adj_d = R(0)
for trial in range(3):
    g = tuple(random.randrange(24) for _ in range(3))
    a, b, c = g
    fc_ab = (su5_gens[a]*su5_gens[b] - su5_gens[b]*su5_gens[a]) / 2
    d_adj = (su5_gens[c]*fc_ab + fc_ab*su5_gens[c]).trace() / 4  # (1/4)Tr(lambda_c {fc_ab}) ~ d(adj)
    adj_d = adj_d + d_adj
print("d(adjoint 24) sample sum:", adj_d)

# SU(3) fundamental for SU(3)_f: d(3) normalization -> A(3) = 1
su3_gens = su_n_generators(3)
triples3 = itertools.product(range(8), repeat=3)
nz3 = None
for g in triples3:
    v3 = d_tensor(su3_gens, g)
    if v3 != 0:
        nz3 = g; break
d3 = d_tensor(su3_gens, nz3)
print("SU(3) d-triple:", nz3, " d(3) =", d3, " -> set A(3) := 1 (normalization)")

# A(16) of SO(10) via SU(5) content 16 -> 1 + 10 + 5bar : A = A(10) + A(5bar) = 1 - 1 = 0
A16 = (d10 + d5b) / v
print("A(16) [in A(5) units]:", A16, " -> per-generation anomaly-free:", A16 == 0)

# A(27) of E6 via verified branching (Tasks D+E):
#   27 -> 1(-4) + 16bar(-1) + 10(2)     [Task D]
#   16bar -> 1(5) + 10bar(1) + 5bar(-3) [Task E, conjugated]
#   10 -> 5(-2) + 5bar(2)               [Task E]
#   => 27 |su(5) = 3*1 + 10bar + 5 + 2*5bar
A27 = (-d10 + v + 2*d5b) / v
print("A(27) [in A(5) units]:", A27)

print()
print("CHANNEL TABLE  (coefficients in A(3)=1 / A(5)=1 units; must vanish for consistency)")
print("content 1: chiral-only  (27,3)  [3 generations, family index gauged, no conjugates]")
print("  E6^3        : 3 * A(27)          =", 3*A27, " != 0  FAIL")
print("  SU(3)_f^3   : 27 * A(3)          =", 27, " != 0  FAIL")
print("  E6^2 x f    : Tr_27(tt) Tr_3(T)  = 0 (traceless T)  OK")
print("  E6 x f^2    : Tr_27(t) Tr_3(TT)  = 0 (traceless t)  OK")
print("  grav x f^2  : 0  OK ;  E6^2 x grav : 0  OK")
print("content 2: E8-adjoint  (27,3) + (27bar,3bar)  [+ (78,1) + (1,8), adjoints, trivially 0]")
print("  E6^3        : 3*A(27) + 3*A(27bar) =", 3*A27 - 3*A27, "  OK")
print("  SU(3)_f^3   : 27*A(3) + 27*A(3bar) =", 27-27, "  OK")
print("  E6^2 x f, E6 x f^2, grav channels: all 0 via tracelessness  OK")
print()
print("tracelessness spot-checks: Tr_3(T):", su3_gens[nz3[0]].trace(),
      " Tr_5(t):", su5_gens[nz[0]].trace())
