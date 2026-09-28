from fractions import Fraction as F
from itertools import product

# ---------- E8 root system in R^8 (exact) ----------
R8 = set()
for i in range(8):
    for j in range(i+1, 8):
        for si in (-1, 1):
            for sj in (-1, 1):
                v = [F(0)]*8; v[i] = F(si); v[j] = F(sj)
                R8.add(tuple(v))
for signs in product((-1,1), repeat=8):
    if signs.count(-1) % 2 == 0:
        R8.add(tuple(F(s)/2 for s in signs))
assert len(R8) == 240

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scl(k,a): return tuple(k*x for x in a)

def cartan_entries(simples):
    A = []
    for i,a in enumerate(simples):
        row = []
        for b in simples:
            row.append(F(2*dot(a,b), dot(a,a)))
        A.append(row)
    return A

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

def classify(roots):
    n = len(roots)
    if n == 0: return "0"
    # find simple system by greedy reduction
    ws = sorted(roots, key=lambda r: -sum(r))
    simples = []
    remaining = set(ws)
    while remaining:
        a = min(remaining, key=lambda r: (sum(r), r))
        remaining.discard(a)
        new_s = []
        for r in list(remaining):
            if dot(a, r) > 0:
                v = sub(r, scl(F(2*dot(a,r), dot(a,a)), a))
                remaining.discard(r)
                if v != (F(0),)*8: remaining.add(v)
        if a != (F(0),)*8:
            if not any(abs(dot(a,s)) == dot(a,a) and dot(s,a) != 0 for s in simples):
                simples.append(a)
    # build Cartan of simple system
    A = cartan_entries(simples)
    S = [[int(x) for x in row] for row in A]
    S.sort()
    return (len(S), S)

# ---------- D5(1): SO(16)-route: SO(10) on coords 1..5 ----------
d5a = set()
for i in range(5):
    for j in range(i+1, 5):
        for si in (-1,1):
            for sj in (-1,1):
                v = [F(0)]*8; v[i] = F(si); v[j] = F(sj)
                d5a.add(tuple(v))
print("D5(1) count:", len(d5a), " closed:", close(d5a) == d5a)

# ---------- D5(3): E7-route: E8 node-subset {2,3,4,5,6} ----------
alpha = [None]*9
alpha[1] = (F(1),-F(1),F(0),F(0),F(0),F(0),F(0),F(0))
alpha[2] = (F(0),F(1),-F(1),F(0),F(0),F(0),F(0),F(0))
alpha[3] = (F(0),F(0),F(1),-F(1),F(0),F(0),F(0),F(0))
alpha[4] = (F(0),F(0),F(0),F(1),-F(1),F(0),F(0),F(0))
alpha[5] = (F(0),F(0),F(0),F(0),F(1),-F(1),F(0),F(0))
alpha[6] = (F(0),F(0),F(0),F(0),F(0),F(1),-F(1),F(0))
alpha[7] = (F(0),F(0),F(0),F(0),F(0),F(0),F(1),F(1))
alpha[8] = (-F(1,2),)*8
d5c_seed = [alpha[2], alpha[3], alpha[4], alpha[5], alpha[6]]
d5c = close(d5c_seed)
print("D5(3) count:", len(d5c), " closed:", close(d5c) == d5c,
      " all E8 roots:", all(r in R8 for r in d5c))

# ---------- D5(2): E6-route ----------
# E6 simple roots in R^8 (Task C verified embedding, E6 = 72 roots orthogonal to A2)
e6_simples = [
    [F(0),F(0),F(0),-F(1),F(1),F(0),F(0),F(0)],
    [F(0),F(0),F(0),F(0),F(0),-F(1),F(1),F(0)],
    [-F(1,2),F(1,2),-F(1,2),F(1,2),-F(1,2),F(1,2),F(1,2),-F(1,2)],
    [-F(1,2),F(1,2),-F(1,2),F(1,2),F(1,2),-F(1,2),-F(1,2),F(1,2)],
    [F(1,2),-F(1,2),F(1,2),-F(1,2),-F(1,2),F(1,2),-F(1,2),F(1,2)],
    [F(1,2),-F(1,2),F(1,2),F(1,2),F(1,2),F(1,2),F(1,2),-F(1,2)],
]
e6_simples = [tuple(s) for s in e6_simples]
A_e6 = cartan_entries(e6_simples)
# fundamental weights w_j with w_j . S_i = delta_ij (|S_i|^2 = 2)
import sympy as sp
M = sp.Matrix([[F(2)*sp.Rational(int(x.numerator), int(x.denominator)) for x in row] for row in A_e6])
Amat = sp.Matrix([[sp.Rational(2 if i==j else 0) - M[i,j] for j in range(6)] for i in range(6)])
# solve dot(w_j, S_i) = delta: w in basis of S_i: w = sum_k c_k S_k; dot = sum_k c_k (S_k . S_i) = (S_k.S_i) matrix * c
G = sp.Matrix([[sp.Rational(int(dot(e6_simples[k], e6_simples[i]).numerator),
                            int(dot(e6_simples[k], e6_simples[i]).denominator))
                for i in range(6)] for k in range(6)])
Ginv = G.inv()
w_vecs = []
for j in range(6):
    # c_k = Ginv[k][j]
    v = [F(0)]*8
    for k in range(6):
        c = F(Ginv[k,j].p, Ginv[k,j].q)
        v = [v[d] + c*e6_simples[k][d] for d in range(8)]
    w_vecs.append(tuple(v))
    assert dot(w_vecs[j], e6_simples[j]) == 1
    assert all(dot(w_vecs[j], e6_simples[i]) == 0 for i in range(6) if i != j)

# D5 simple roots as E6 weights from Task D restriction matrix rows 1..5:
rm_rows = [[1,0,0,0,0,2],[0,0,0,0,1,3],[0,1,0,0,0,4],[0,0,1,0,0,6],[0,0,0,1,0,5]]
d5b_seed = []
for row in rm_rows:
    v = [F(0)]*8
    for j,c in enumerate(row):
        v = [v[d] + c*w_vecs[j][d] for d in range(8)]
    d5b_seed.append(tuple(v))
print("D5(2) seed Cartan:")
for row in cartan_entries(d5b_seed):
    print("   ", [int(x) for x in row])
print("D5(2) seed all E8 roots:", all(r in R8 for r in d5b_seed),
      " all norm-2:", all(dot(r,r)==2 for r in d5b_seed))
d5b = close(d5b_seed)
print("D5(2) count:", len(d5b), " closed:", close(d5b) == d5b,
      " all E8 roots:", all(r in R8 for r in d5b))

# ---------- centralizers ----------
def centralizer(d5):
    return {r for r in R8 if all(dot(r,s) == 0 for s in d5)}

for name, d5 in [("D5(1) SO(16)-route", d5a), ("D5(2) E6-route", d5b), ("D5(3) E7-route", d5c)]:
    C = centralizer(d5)
    print(name, ": |D5| =", len(d5), " centralizer roots =", len(C),
          " closed:", close(C) == C)
    if len(C) > 0:
        ws = sorted(C, key=lambda r: -sum(r))
        a = ws[0]
        # count long/short and print a simple root candidate set
        type_A = [[int(2*dot(x,y)) for y in sorted(C, key=lambda r: tuple(r))] for x in sorted(C, key=lambda r: tuple(r))]
        print("   classification (root count, sample angle check):", len(C), "roots, norm:", dot(a,a))
# classify by matching against known root systems
print()
print("E8 roots total:", len(R8))
