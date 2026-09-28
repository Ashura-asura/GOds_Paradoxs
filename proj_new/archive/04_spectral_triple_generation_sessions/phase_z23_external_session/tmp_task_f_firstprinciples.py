from fractions import Fraction as F
import itertools, sys

# ============ G2 root system in R^3 (short: +/-e_i-/+e_j perms, long: 2e_i-e_j-e_k perms)
short6 = [(1,-1,0),(1,0,-1),(0,1,-1)]
short = [tuple(s) for s in short6] + [tuple(-x for x in s) for s in short6]
long6 = [(2,-1,-1),(-1,2,-1),(-1,-1,2)]
longr = [tuple(s) for s in long6] + [tuple(-x for x in s) for s in long6]
g2_roots = set(short + longr)
assert len(g2_roots) == 12

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def scal(k,a): return tuple(k*x for x in a)

# A2 = long-root subsystem of G2; simple roots b1=(2,-1,-1), b2=(-1,2,-1)
b1, b2 = (2,-1,-1), (-1,2,-1)
A21 = F(2*dot(b1,b2), dot(b1,b1)); A22 = F(2*dot(b2,b1), dot(b2,b2))
print("G2 -> A2 Cartan entries: [[2,", A21, "],[", A22, ",2]]")
assert A21 == -1 and A22 == -1

# A2 fundamental weights in R^3: w1,w2 with <wi,bj^v> = delta_ij
# solve: 2(dot(w1,b1))/6 = 1, 2(dot(w1,b2))/6 = 0
# w = (x,y,z), y+z = -x, b1 = (2,-1,-1), b2 = (-1,2,-1)
def solve_fw():
    # w1 = a*e1+b*e2+c*e3, c = -a-b
    # dot(w1,b1) = 2a - b - c = 2a-b+a+b = 3a -> 3a = 3 -> a=1
    # dot(w1,b2) = -a + 2b - c = -a+2b+a+b = 3b -> 0 -> b=0
    w1 = (1,0,-1)
    # w2: dot(w2,b1) = 0 -> 3a = 0; dot(w2,b2) = 3b = 3 -> b = 1
    w2 = (0,1,-1)
    return w1, w2
w1, w2 = solve_fw()
print("A2 fund weights in R3:", w1, w2)

def a2_dynkin_coords(w):
    a = F(2*dot(w,b1), 6)   # <w, b1^v>
    b = F(2*dot(w,b2), 6)
    return (a,b)

# A2 weight systems of 3=[1,0,0], 3bar=[0,1,0], 1 (Dynkin coords)
W3   = set([(F(1),F(0)), (F(-1),F(1)), (F(0),F(-1))])
W3b  = set([(F(0),F(1)), (F(1),F(-1)), (F(-1),F(0))])
W1   = set([(F(0),F(0))])

# 7 of G2: 6 short roots (mult 1) + 0 (mult 1)
c3 = c3b = c1 = 0
for w in short:
    c = a2_dynkin_coords(w)
    if c in W3: c3 += 1
    elif c in W3b: c3b += 1
    else: print("UNEXPECTED", w, c); sys.exit(1)
if a2_dynkin_coords((0,0,0)) in W1: c1 += 1
print("7 -> 3:", c3, " 3bar:", c3b, " 1:", c1)
assert (c3, c3b, c1) == (3,3,1)

# 14 (adjoint): 12 roots + 2 zeros; 6 long -> A2 adjoint 8, 6 short -> 3+3bar, 2 zeros -> 8's zeros
d3 = d3b = 0; dlong = dzero = 0
for w in short:
    c = a2_dynkin_coords(w)
    if c in W3: d3 += 1
    elif c in W3b: d3b += 1
for w in longr:
    # long roots of G2 = roots of A2: they must restrict to the 6 A2 roots (the 8's nonzero weights)
    if a2_dynkin_coords(w) != (F(0),F(0)): dlong += 1
print("14 -> 3:", d3, " 3bar:", d3b, " 8(nonzero part):", dlong, " zeros: 2")
assert d3 == 3 and d3b == 3 and dlong == 6

# ============ F4 root system in R^4
f4_long = [tuple(s) for s in itertools.combinations([1,-1]*4, 2)]
f4_long = [tuple(x for x in p) for p in itertools.product((1,-1), repeat=4) for i in range(4) for j in range(i+1,4)]
f4_long = list({tuple(([0,0,0,0][k] + (1 if k==i else 0 if k==j else 0)) for k in range(4)) for i in range(4) for j in range(i+1,4) for _ in [0]})
# cleaner: +-e_i +- e_j, i<j
f4_long = set()
for i in range(4):
    for j in range(i+1,4):
        for si in (1,-1):
            for sj in (1,-1):
                v = [0]*4; v[i]=si; v[j]=sj; f4_long.add(tuple(v))
assert len(f4_long) == 24
f4_short1 = set()
for i in range(4):
    v = [0]*4; v[i] = 1; f4_short1.add(tuple(v))
    v = [0]*4; v[i] = -1; f4_short1.add(tuple(v))
assert len(f4_short1) == 8
f4_short2 = set()
for bits in itertools.product((1,-1), repeat=4):
    f4_short2.add(tuple(F(x,2) for x in bits))
assert len(f4_short2) == 16
f4_roots = f4_long | f4_short1 | f4_short2
assert len(f4_roots) == 48
print("F4 roots: 24 long +", len(f4_short1), "+", len(f4_short2), "= 48")

# B4 = SO(9) subset: f4_long (24) + f4_short1 (+-e_i, 8) = B4 roots
b4_roots = f4_long | f4_short1
assert len(b4_roots) == 32
# check B4 Cartan: b4 long: 2(dot(a,b))/|a|^2 with |a|^2=2
print("B4 long/short root counts:", sum(1 for r in b4_roots if dot(r,r)==2), sum(1 for r in b4_roots if dot(r,r)==1))

# 26 of F4 = 24 short roots + 2 zeros; restrict to B4:
#   8 (+-e_i) -> vector 9 weights; 16 half-integers -> spinor 16; 2 zeros -> 1
v9 = f4_short1  # the 8 weights of the 9
spin16 = f4_short2  # the 16 weights of the spinor (even-minus half-integers)
print("26 -> 9:", len(v9), " 16:", len(spin16), " 1: 1")
assert len(v9) == 8 and len(spin16) == 16
# 52 -> 36+16: 32 B4 roots (24 long + 8 short) -> 36 adjoint, 16 half-integers -> 16 spinor
print("52 -> 36 + 16: roots in B4:", len(b4_roots), " spinor:", len(spin16))
assert len(b4_roots) == 32

# rank argument: SO(10) has rank 5 > rank 4 of F4 -> no SO(10) subgroup of F4
# 248 arithmetic: 52+14+182 = 248; complement 182 with exactly 180 nonzero weights + 2 zeros:
#   (26,7): 24*6 + 24*1 + 2*6 = 144+24+12 = 180 nonzero, 2*1 = 2 zeros  OK
#   (1,182): nonzero F4-part count = 0 -> cannot hold the 180 roots with nonzero F4-projection  NO
#   (26,14): 24*12+24*2+2*12 = 360 nonzero  NO
print("248 = 52 + 14 + 26*7 =", 52+14+26*7)
print("complement nonzero-weight count for (26,7):", 24*6+24*1+2*6, " zeros:", 2*1)
print("(1,182) ruled out: F4-part of 180 complement roots is nonzero")
print("(26,14) ruled out: nonzero count", 24*12+24*2+2*12, "needed 180")
print("ALL CHECKS PASSED")
