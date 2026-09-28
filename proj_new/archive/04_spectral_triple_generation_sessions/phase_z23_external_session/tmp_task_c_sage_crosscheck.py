from fractions import Fraction as F
from itertools import product
import sympy as sp
from collections import Counter

# ---------- E8 root system ----------
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

# ---------- Result A: E8 -> D8 -> D5 x A3 (Sage cross-check of Task C Result 3) ----------
d8 = set()
for i in range(8):
    for j in range(i+1, 8):
        for si in (-1,1):
            for sj in (-1,1):
                v = [F(0)]*8; v[i] = F(si); v[j] = F(sj)
                d8.add(tuple(v))
assert len(d8) == 112
d5 = set(r for r in d8 if r[5] == 0 and r[6] == 0 and r[7] == 0)
a3 = set(r for r in d8 if r[0] == 0 and r[1] == 0 and r[2] == 0 and r[3] == 0 and r[4] == 0)
d5_5 = set(r[:5] for r in d5)
a3_3 = set(r[5:] for r in a3)
assert len(d5) == 40 and len(a3) == 12
cnt = Counter()
for r in R8:
    p5 = r[:5]
    pC = r[5:]
    assert norm2(p5) + norm2(pC) == 2
    k5 = 'root' if p5 in d5_5 else ('zero' if norm2(p5) == 0 else ('spin' if norm2(p5) == F(5,4) else ('vec' if norm2(p5) == F(1) else ('hspin' if norm2(p5) == F(3,4) else 'other'))))
    kC = 'root' if pC in a3_3 else ('zero' if norm2(pC) == 0 else ('vec' if norm2(pC) == F(1) else ('hspin' if norm2(pC) == F(3,4) else 'other')))
    cnt[(k5, kC)] += 1
print("=== A. E8 -> D8 -> D5xA3: 248 = 120 + 128 root split (LiE Task C Result 3 cross-check) ===")
for (k5, kC), n in sorted(cnt.items()):
    print(f"   ({k5:5s}, {kC:5s}) x {n}")
print("   240 = 40 + 12 + 60 + 64 + 64; with 8 Cartan -> 248 = (45,1)+(1,15)+(10,6)+(16,4bar)+(16bar,4)")

# ---------- Result B: E8 -> E7 x A1 ----------
e7 = close(alpha[1:8])
a1 = {r for r in R8 if all(dot(r,s) == 0 for s in e7)}
assert len(e7) == 126 and len(a1) == 2
b7 = gram_schmidt(sorted(e7))
b1 = gram_schmidt(sorted(a1))
cnt = Counter()
for r in R8:
    p7 = project(r, b7)
    p1 = project(r, b1)
    assert norm2(p7) + norm2(p1) == 2
    cnt[(norm2(p7), norm2(p1))] += 1
print("\n=== B. E8 -> E7xA1: 248 -> (133,1)+(56,2)+(1,3) (Item 11 chain start) ===")
for (n7, n1), n in sorted(cnt.items()):
    print(f"   |E7-part|^2={n7}, |A1-part|^2={n1}  x{n}   ({'126 -> (133,1)' if (n7,n1)==(2,0) else ('2 -> (1,3)' if (n7,n1)==(0,2) else '112 -> (56,2)')})")

# ---------- Result C: E7 -> E6 x U(1); is there an E6 x SU(2) x SU(2)? ----------
e6 = close(alpha[1:7])
assert len(e6) == 72
# centralizer of E6 within the E7-span: roots of E7 orthogonal to all of E6
c_e6_in_e7 = {r for r in e7 if all(dot(r, s) == 0 for s in e6)}
print("\n=== C. E7 -> E6 x U(1) vs the 'E6xSU(2)xSU(2)' label (Item 11) ===")
print("   C(E6 in E7) roots:", len(c_e6_in_e7), "-> torus (U(1) direction), NOT an A1")
print("   hence E7 does NOT contain E6 x SU(2) (regular): the chain is E8 > E7xSU(2) > E6xU(1)xSU(2).")
b6 = gram_schmidt(sorted(e6))
# U(1) direction: the component of alpha7 orthogonal to the E6-span
u1_dir = tuple(alpha[7])
for b in b6:
    u1_dir = sub(u1_dir, scl(F(dot(u1_dir, b), dot(b, b)), b))
cnt = Counter()
for r in e7:
    p6 = project(r, b6)
    p1 = scl(F(dot(r, u1_dir), dot(u1_dir, u1_dir)), u1_dir)
    assert norm2(p6) + norm2(p1) == 2
    cnt[(norm2(p6), norm2(p1))] += 1
print("   E7 126 roots by (|E6-part|^2, |U(1)-part|^2):")
for (n6, n1), n in sorted(cnt.items()):
    print(f"      ({n6}, {n1}) x{n}    ({'72 = 133|E6' if (n6,n1)==(2,0) else '54 = 27 + 27bar under E6xU(1)'})")

# ---------- Result D: E8 -> E6 x U(1) x A1 full classification ----------
cnt = Counter()
b1l = gram_schmidt(sorted(a1))
for r in R8:
    p6 = project(r, b6)
    p1 = project(r, b1l)
    p_u = scl(F(dot(r, u1_dir), dot(u1_dir, u1_dir)), u1_dir)
    assert norm2(p6) + norm2(p_u) + norm2(p1) == 2
    cnt[(norm2(p6), norm2(p_u), norm2(p1))] += 1
print("\n=== D. E8 -> E6 x U(1) x SU(2): 240 roots by (|E6|^2, |U(1)|^2, |SU(2)|^2) ===")
tot = 0
for (n6, nu, n1), n in sorted(cnt.items()):
    print(f"      ({n6}, {nu}, {n1}) x{n}")
    tot += n
print(f"   total roots {tot} + 8 Cartan = 248  [240 = 72 + 2 + 108 + 54 + 4;")
print("   the (0,3/2,1/2) x4 are the roots of the (1,2,2) pieces (the '1+1' content of 56 -> 27+27bar+1+1),")
print("   the (1,2,2) non-root entries are among the 8 Cartan: 248 = 240 + 8]")

# ---------- Result E: SU(4) 'flavon' (4 of the SO(16)-route C(D5) = A3): quartic invariants ----------
print("\n=== E. SU(4) 'flavon' (4 of C(D5(1)) = A3): exact quartic invariant theory ===")
x0, p1v, p2v, p3v = sp.symbols('x p1 p2 p3')
ph = [p1v, p2v, p3v, x0]
from itertools import permutations
eps = 0
terms = 0
for sig in permutations(range(4)):
    s = 1
    for i in range(4):
        for j in range(i+1,4):
            if sig[i] > sig[j]: s = -s
    eps += s*sp.prod([ph[k] for k in sig])
    terms += 1
print("   candidate holomorphic quartic eps^{ijkl} phi_i phi_j phi_k phi_l =", eps)
print(f"   ({terms} terms, sum of signs = 0: identically zero for a single field)")
print("   tensor-singlet count 4(x)4(x)4bar(x)4bar: (6+10)x(6bar+10bar) has 2 singlets,")
print("   but on ONE field: phi^phi = 0 (antisym part) and sym(phi(x)phi) = phi.phi,")
print("   so both singlets collapse to (phi^dag phi)^2.")
print("   invariant ring of the SU(4) fundamental: C[|phi|^2] (SU(4) transitive on S^7)")
print("   -> quartic 'flavon' potential V4 = lambda (|phi|^2)^2 : ONE term, no 3+1 split,")
print("   no order-3 structure: 4 -> 3+1 under SU(4) > SU(3)xU(1) is exact but unstabilized")
print("   by any SU(4)-invariant quartic. The 3-generation structure cannot arise from the")
print("   4 alone; it requires the group reduction SU(4) -> SU(3)xU(1) (a spectator U(1)),")
print("   i.e. the SO(16)-route does not support a non-cyclic 3-generation mechanism at the")
print("   flavon-potential level (consistent with Task B: only the E6-route hosts SU(3)_f).")
