from fractions import Fraction as F
from itertools import product

alpha = [None]*9
alpha[1] = (F(1,2),-F(1,2),-F(1,2),-F(1,2),-F(1,2),-F(1,2),-F(1,2),F(1,2))
alpha[2] = (F(1),F(1),F(0),F(0),F(0),F(0),F(0),F(0))
alpha[3] = (-F(1),F(1),F(0),F(0),F(0),F(0),F(0),F(0))
for i in range(4,9):
    v = [F(0)]*8; v[i-2] = F(-1); v[i-1] = F(1)
    alpha[i] = tuple(v)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def scl(k,a): return tuple(k*x for x in a)

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
print("R8 =", len(R8))

print("each alpha in R8 and norm 2:")
for i in range(1,9):
    print(i, alpha[i] in R8, dot(alpha[i],alpha[i]) == 2)

print("Cartan (A_ij = 2 a_i.a_j / a_i.a_i):")
for i in range(1,9):
    row = []
    for j in range(1,9):
        row.append(int(2*dot(alpha[i],alpha[j])/dot(alpha[i],alpha[i])))
    print("   ", row)

print("pairwise dots (should be in {0,-1}):")
for i in range(1,9):
    for j in range(i+1,9):
        d = dot(alpha[i],alpha[j])
        if d != 0:
            print(f"   ({i},{j}): {d}")
