import random
from fractions import Fraction as F
src = open('tmp_task_e_fts.py').read()
marker = '# E7-invariance: for each simple e_i, T(a,b,c,d) = 0 for all quadruples with total weight -alpha_i'
head = src.split(marker)[0]
mid = src.split(marker)[1].split('eqs = []')[0]
exec(head)
exec(mid)

random.seed(5)
# Build the coefficient matrix of the linear system by evaluating B(e_i x, x, x, x) as linear form in q0,q1,q2
# For random x, B(e_i x,x,x,x) = sum_j q_j * coeff_j. Collect rows.
def Bcoeff(evec, x):
    c = [F(0)]*3
    for a in range(n):
        for b in range(n):
            for c2 in range(n):
                for d in range(n):
                    t = tuple(sorted(tuple(weights[x]) for x in (a, b, c2, d)))
                    if t in orb_of_mon:
                        cc = Counter(t)
                        mult = 1
                        for v in cc.values():
                            mult *= factorial(v)
                        c[orb_of_mon[t]] += evec[a]*x[b]*x[c2]*x[d]*mult
    return c

rows = []
for trial in range(200):
    for i in range(7):
        x = [F(random.randint(-2,2)) for _ in range(n)]
        ei = Ei[i]
        ex = [sum(ei[r][c]*x[c] for c in range(n)) for r in range(n)]
        rows.append(Bcoeff(ex, x))
print("rows:", len(rows))
from sympy import Matrix
M = Matrix([[r[j] for j in range(3)] for r in rows])
print("rank of random-sampling system:", M.rank())
ns = M.nullspace()
print("nullspace dim:", len(ns))
if ns:
    v = ns[0]
    print("null vector:", [sp.nsimplify(x) for x in v])
