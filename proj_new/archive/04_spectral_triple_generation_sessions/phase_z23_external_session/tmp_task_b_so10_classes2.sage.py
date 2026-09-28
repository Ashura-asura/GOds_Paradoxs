from fractions import Fraction as F
from itertools import product
import sympy as sp

# ---------- correct E8 simple system in R^8 ----------
alpha = [None]*9
alpha[1] = (F(1,2),-F(1,2),-F(1,2),-F(1,2),-F(1,2),-F(1,2),-F(1,2),F(1,2))
alpha[2] = (F(1),F(1),F(0),F(0),F(0),F(0),F(0),F(0))
alpha[3] = (-F(1),F(1),F(0),F(0),F(0),F(0),F(0),F(0))
for i in range(4,9):
    v = [F(0)]*8; v[i-3] = F(-1); v[i-2] = F(1)
    alpha[i] = tuple(v)

R8 = set()
for i in range(8):
    for j in range(i+1, 8):
        for si in (-1,1):
            for sj in (-1,1):
                v = [F(0)]*8; v[i] = F(si); v[j] = F(sj)
                R8.add(tuple(v))
for signs in product((-1,1), repeat=8):
    if signs.count(-1) % 2 == 0:
        R8.add(tuple(F(s)/2 for s in signs))
assert len(R8) == 240

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scl(k,a): return tuple(k*x for x in a)
def addv(a,b): return tuple(x+y for x,y in zip(a,b))
def norm2(a): return dot(a,a)

def close(seed):
    S = set(seed)
    changed = True
    while changed:
        changed = False
        for r in list(S):
            for s in list(S):
                v = sub(r, scl(F(2*dot(r,s), dot(s,s)), s))
                if v not in S:
                    S.add(v); changed = True
    return S

def cartan_rows(simples):
    A = []
    for a in simples:
        row = [F(2*dot(a,b), dot(a,a)) for b in simples]
        A.append(row)
    return A

def rank_of(roots):
    vs = [list(r) for r in roots]
    M = sp.Matrix(vs)
    return M.rank()

def system_type(roots):
    n = len(roots)
    r = rank_of(roots)
    if n == 0: return f"U(1)^{r if r else 0}"
    ws = sorted(roots, key=lambda x: -sum(x))
    g = addv(sum(tuple(x[i] for x in roots) for i in range(0)) if False else tuple(sum(x[i] for x in roots) for i in range(8)), (0,)*8)
    g = tuple(sum(x[i] for x in roots) for i in range(8))
    try_g = 0
    while True:
        try_g += 1
        cand = tuple(F(sum(x[i] for x in roots)) + F(try_g, 7)*(i+1) for i in range(8))
        pos = [x for x in roots if dot(x, cand) > 0]
        if len(pos)*2 == len(roots):
            g = cand
            break
    def is_simple(r, pos):
        for s in pos:
            if s != r and sub(r, s) in roots:
                return False
        return True
    simples = [r for r in pos if is_simple(r, pos)]
    A = cartan_rows(simples)
    S = sorted(sorted(int(x) for x in row) for row in A)
    deg = [sum(1 for row in A if row[j] != 0) for j in range(len(A))]
    n4 = len(A)
    if n == 2*r: return f"A1" if r == 1 else f"(A1)^{r} x U(1)?" if n == 2*r else "?"
    known = {12: "A2/G2", 6: "A2", 30: "A5", 72: "E6", 40: "D5", 20: "D4", 12: "A3", 24: "A4", 42: "A6", 126: "E7", 56: "A7", 240: "E8", 4: "A1xA1", 2: "A1", 8: "A1xA1xA1", 18: "B2/A3?", 90: "D6", 60: "D6/B5?", 36: "B4/A4?"}
    t = known.get(n)
    if t is None:
        t = f"rank {r}, {n} roots, Cartan {S}"
    return t

# verify base
assert close(alpha[1:]) == R8, "base not closed to 240"
print("E8 base verified: 240 roots from simples; Cartan matrix:")
for row in cartan_rows(alpha[1:]):
    print("   ", [int(x) for x in row])

# ---------- D5(1): SO(16)-route (coords 1..5) = E7-route D5 ----------
d5a = set()
for i in range(5):
    for j in range(i+1, 5):
        for si in (-1,1):
            for sj in (-1,1):
                v = [F(0)]*8; v[i] = F(si); v[j] = F(sj)
                d5a.add(tuple(v))
print("\nD5(1) SO(16)/E7-route: roots =", len(d5a), "closed:", close(d5a) == d5a)

# ---------- D5(2): E6-route (E6 = {1..6}, D5 = {1..5}, node 6 = U(1)) ----------
d5b = close(alpha[1:6])
print("D5(2) E6-route: roots =", len(d5b), "closed:", close(d5b) == d5b)

# ---------- D5(3): E7-route ----------
e7 = close(alpha[1:8])
print("E7 = <a1..a7>: roots =", len(e7), " closed:", close(e7) == e7, " (126 expected)")
print("  C(E7) in E8 (roots orthogonal to all E7 roots):")
c_e7 = {r for r in R8 if all(dot(r,s) == 0 for s in e7)}
print("   ", len(c_e7), "roots =", system_type(c_e7))
# regular D5 subdiagrams of E7:
d5_1_in_e7 = close(alpha[2:7])  # {2..6} = coords 1..5
d5_2_in_e7 = close(alpha[1:6])  # {1..5}
print("  D5 in E7 via {2..6}:", len(d5_1_in_e7), "roots, equals D5(1):", d5_1_in_e7 == d5a)
print("  D5 in E7 via {1..5}:", len(d5_2_in_e7), "roots, equals D5(2):", d5_2_in_e7 == d5b)

# ---------- centralizers ----------
def centralizer(d5):
    return {r for r in R8 if all(dot(r,s) == 0 for s in d5)}

print("\n=== centralizers ===")
for name, d5 in [("D5(1) SO(16)/E7-route", d5a), ("D5(2) E6-route", d5b)]:
    C = centralizer(d5)
    print(f"{name}: |D5| = {len(d5)}, C(D5) = {len(C)} roots, type {system_type(C)}")
    print("   C roots:", sorted(C))

# ---------- 248 branching via orthogonal projection ----------
def gram_schmidt(vecs):
    basis = []
    for v in vecs:
        w = tuple(v)
        for b in basis:
            w = sub(w, scl(F(dot(w,b), dot(b,b)), b))
        if dot(w,w) != 0:
            basis.append(w)
    return basis

def project(v, basis):
    p = tuple(F(0) for _ in range(8))
    for b in basis:
        p = addv(p, scl(F(dot(v,b), dot(b,b)), b))
    return p

def weight_class(v, roots):
    n2 = norm2(v)
    if v == (F(0),)*8: return "zero"
    if v in roots: return "root"
    if n2 == F(1): return "vec"
    if n2 == F(5,4): return "spin"
    if n2 == F(3,4): return "hspin"
    return f"other({n2})"

print("\n=== 248 branching: D5 x C(D5) ===\n")
for name, d5 in [("D5(1) SO(16)/E7-route", d5a), ("D5(2) E6-route", d5b)]:
    C = centralizer(d5)
    b5 = gram_schmidt(sorted(d5))
    bC = gram_schmidt(sorted(C))
    counts = {}
    for r in R8:
        p5 = project(r, b5)
        pC = project(r, bC)
        assert dot(p5, pC) == 0 and norm2(addv(p5, pC)) == norm2(r)
        k5 = weight_class(p5, d5)
        kC = weight_class(pC, C)
        counts[(k5, kC)] = counts.get((k5, kC), 0) + 1
    print(name, "  [248 -> D5 x C] root decomposition:")
    tot = 0
    for (k5, kC), n in sorted(counts.items()):
        print(f"    ({k5:6s}, {kC:6s}) x {n}")
        tot += n
    print("    total roots:", tot)

# ---------- E6 27 branching under D5(2) ----------
e6 = close(alpha[1:7])
print("\nE6 = <a1..a6>: roots =", len(e6), "(72 expected)")
# fundamental weight L1 of E6: L1 . a_j = delta_1j
G = sp.Matrix([[sp.Rational(int(dot(alpha[k], alpha[i]).numerator), int(dot(alpha[k], alpha[i]).denominator)) for i in range(1,7)] for k in range(1,7)])
Ginv = G.inv()
L1 = [F(0)]*8
for k in range(6):
    c = F(Ginv[k,0].p, Ginv[k,0].q)
    L1 = [L1[d] + c*alpha[k+1][d] for d in range(8)]
L1 = tuple(L1)
# Weyl orbit of L1 = the 27 weights
orbit = {L1}
changed = True
while changed:
    changed = False
    for w in list(orbit):
        for a in e6:
            v = sub(w, scl(F(2*dot(w,a), dot(a,a)), a))
            if v not in orbit:
                orbit.add(v); changed = True
print("E6 orbit of L1 (27):", len(orbit))
b5 = gram_schmidt(sorted(d5b))
from collections import Counter
wc = Counter()
for w in orbit:
    p5 = project(w, b5)
    wc[weight_class(p5, d5b)] += 1
print("27 -> D5(2):", dict(wc), " (expect 16 spin + 10 vec + 1 zero)")

print("\n=== summary ===")
print("D5(1) (SO(16)-route == E7-route {2..6}): 40 roots, C =", system_type(centralizer(d5a)))
print("D5(2) (E6-route {1..5}): 40 roots, C =", system_type(centralizer(d5b)))
print("D5(1) == D5(2) (conjugate-identical subalgebras)? ", d5a == d5b)
print("C(D5(1)) = {+-e_i+-e_j, 6<=i<j<=8} (the SO(16)-position A3)")
print("C(D5(2)) = {+-(e_i+e_8), +-(e_i-e_j), i,j in {5,6,7}} (twisted A3 containing the")
print("           family A2 = C(E6) of the maximal E8 > E6 x SU(3))")
