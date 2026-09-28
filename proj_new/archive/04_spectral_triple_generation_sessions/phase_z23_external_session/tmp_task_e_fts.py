from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from collections import Counter, defaultdict
from math import factorial
import sympy as sp

# ---------- E8 root system (shared machinery) ----------
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

assert close(alpha[1:]) == R8

# ---------- E7 and the 56 weights ----------
e7 = close(alpha[1:8])
assert len(e7) == 126
b7 = gram_schmidt(sorted(e7))
a1 = {r for r in R8 if all(dot(r,s) == 0 for s in e7)}
b1 = gram_schmidt(sorted(a1))
W56v = set()
for r in R8:
    p7 = project(r, b7)
    p1 = project(r, b1)
    if norm2(p7) == F(3,2) and norm2(p1) == F(1,2):
        W56v.add(p7)
assert len(W56v) == 56

def labels(w):
    v = tuple(dot(w, alpha[i]) for i in range(1,8))
    assert all(x.denominator == 1 for x in v)
    return tuple(int(x) for x in v)

WL = {labels(w) for w in W56v}
print("56 weights of E7 (from E8 -> E7xA1): 56 distinct; integer Dynkin labels OK")

A = [[int(dot(alpha[i],alpha[j])) for j in range(1,8)] for i in range(1,8)]
AL = {i: tuple(A[i-1]) for i in range(1,8)}

assert all(tuple(-x for x in w) in WL for w in WL)
print("56 is self-dual (28 opposite pairs) OK")

dom = [w for w in WL if all(x >= 0 for x in w)]
assert len(dom) == 1
highest = dom[0]
def reflect(w, i):
    nn = w[i-1]
    return tuple(w[j] - nn*AL[i][j] for j in range(7))
orbit = {highest}
changed = True
while changed:
    changed = False
    for w in list(orbit):
        for i in range(1,8):
            v = reflect(w, i)
            if v in WL and v not in orbit:
                orbit.add(v); changed = True
assert orbit == WL
print("the 56 weights form the single Weyl orbit of", highest, "(56 elements) OK")

idx = {w: k for k, w in enumerate(sorted(WL))}
weights = sorted(WL)
n = 56

# ---------- explicit E7 Chevalley action on the 56 ----------
def act_e(i, w):
    v = tuple(w[j] + AL[i][j] for j in range(7))
    return idx[v] if v in idx else None
def act_f(i, w):
    v = tuple(w[j] - AL[i][j] for j in range(7))
    return idx[v] if v in idx else None

def op_e(i):
    M = [[0]*n for _ in range(n)]
    for w in weights:
        j = act_e(i, w)
        if j is not None:
            M[j][idx[w]] = 1
    return M
def op_f(i):
    M = [[0]*n for _ in range(n)]
    for w in weights:
        j = act_f(i, w)
        if j is not None:
            M[j][idx[w]] = w[i-1]
    return M
def op_h(i):
    return [[w[i-1] if a == b else 0 for b in range(n)] for a, w in enumerate(weights)]

def mm(A, B):
    return [[sum(A[r][k]*B[k][c] for k in range(n)) for c in range(n)] for r in range(n)]
def sc(k, A):
    return [[k*x for x in row] for row in A]
def addm(A, B):
    return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def subc(A, B):
    return [[a-b for a,b in zip(r,s)] for r,s in zip(A,B)]
def iszero(A):
    return all(x == 0 for row in A for x in row)

Ei = [op_e(i) for i in range(1,8)]
Fi = [op_f(i) for i in range(1,8)]
Hi = [op_h(i) for i in range(1,8)]
ok = True
for i in range(7):
    if not iszero(subc(subc(mm(Ei[i],Fi[i]), mm(Fi[i],Ei[i])), Hi[i])):
        ok = False
    for j in range(7):
        if i == j: continue
        if not iszero(subc(subc(mm(Hi[i],Ei[j]), mm(Ei[j],Hi[i])), sc(A[j][i], Ei[j]))):
            ok = False
        if not iszero(subc(subc(mm(Hi[i],Fi[j]), mm(Fi[j],Hi[i])), sc(-A[j][i], Fi[j]))):
            ok = False
        if i < j:
            C = subc(mm(Ei[i],Ei[j]), mm(Ei[j],Ei[i]))
            D = subc(mm(Fi[i],Fi[j]), mm(Fi[j],Fi[i]))
            if A[i][j] == 0:
                if not iszero(C) or not iszero(D):
                    ok = False
            else:
                for (E, E2) in ((Ei[i],Ei[j]), (Ei[j],Ei[i]), (Fi[i],Fi[j]), (Fi[j],Fi[i])):
                    CE = subc(mm(E,subc(mm(E,E2),mm(E2,E))), mm(subc(mm(E,E2),mm(E2,E)),E))
                    if not iszero(CE):
                        ok = False
print("Serre relations on the 56 module:", "ALL VERIFIED" if ok else "FAILED")
assert ok

# ---------- E7-invariant symplectic form J ----------
pairs_opp = [w for w in weights if w < tuple(-x for x in w)]
vars_ = [sp.Symbol(f'c{k}') for k in range(len(pairs_opp))]
def Jpoly(a, b):
    na = tuple(-x for x in a)
    if b == na:
        if a < na:
            return vars_[pairs_opp.index(a)]
        else:
            return -vars_[pairs_opp.index(na)]
    return sp.Integer(0)
eqs = []
for i in range(7):
    for a in range(n):
        ja = act_e(i+1, weights[a])
        if ja is None: continue
        for b in range(n):
            lhs = Jpoly(weights[ja], weights[b])
            jb = act_e(i+1, weights[b])
            if jb is not None:
                lhs = lhs + Jpoly(weights[a], weights[jb])
            if lhs != 0:
                eqs.append(lhs)
sol = list(sp.linsolve(eqs, *vars_))
assert len(sol) == 1
solv = sol[0]
Jc = {pairs_opp[k]: sp.nsimplify(solv[k]) for k in range(len(pairs_opp))}
nh = tuple(-x for x in highest)
scale = Jc[min(highest, nh)]
Jc = {p: v/scale for p, v in Jc.items()}
def sigma(w):
    nw = tuple(-x for x in w)
    if w < nw:
        return sp.nsimplify(Jc[w])
    return -sp.nsimplify(Jc[nw])
sigs = {w: sigma(w) for w in weights}
vals = set(sigs.values())
print("invariant skew form J: unique up to scale; sigma(w) = J(v_w, v_-w) in", vals)
assert vals <= {sp.Integer(1), sp.Integer(-1)}

def Jv(a, b):
    na = tuple(-x for x in a)
    if b == na:
        return sigs[a]
    return sp.Integer(0)
ok = True
for i in range(7):
    for a in range(n):
        for b in range(n):
            ja = act_e(i+1, weights[a]); jb = act_e(i+1, weights[b])
            lhs = sp.Integer(0)
            if ja is not None: lhs += Jv(weights[ja], weights[b])
            if jb is not None: lhs += Jv(weights[a], weights[jb])
            if lhs != 0: ok = False
print("J-invariance under all e_i, f_i (21 generators):", "OK" if ok else "FAIL")
assert ok

# ---------- the quartic: solve for the unique E7-invariant ----------
# NOTE: W(E7) acts on the 56 with signs (sigma(w) in {+1,-1}), so coefficients are
# NOT constant on monomial W-orbits. Solve the full linear system over all monomials.
mons = []
for m in combinations_with_replacement(weights, 4):
    s = tuple(sum(m[j][k] for j in range(4)) for k in range(7))
    if s == (0,)*7:
        mons.append(m)
print("torus-invariant quartic monomials:", len(mons))
mon_idx = {m: k for k, m in enumerate(mons)}
nm = len(mons)
from fractions import Fraction
# polarization mult factor for the multiset of 4 indices
def mult4(t):
    cc = Counter(t)
    p = 1
    for v in cc.values():
        p *= factorial(v)
    return p

wt_index = {}
for k, w in enumerate(weights):
    wt_index.setdefault(w, []).append(k)
# 3-sum grouping: sum3[s] = list of (a,b,c) with w_a + w_b + w_c = s
sum3 = defaultdict(list)
for a in range(n):
    for b in range(n):
        for c in range(n):
            s = tuple(weights[a][k] + weights[b][k] + weights[c][k] for k in range(7))
            sum3[s].append((a, b, c))
# quadruples (a,b,c,d) with total weight tgt, grouped by tgt
def quads(tgt):
    res = []
    for d in range(n):
        need = tuple(tgt[k] - weights[d][k] for k in range(7))
        for (a, b, c) in sum3.get(need, ()):
            res.append((a, b, c, d))
    return res

# each equation T(a,b,c,d) = 0 is a row: sum over <=4 monomial coefficients
rows = []
def add_row(row):
    row = {c: v for c, v in row.items() if v != 0}
    if row:
        rows.append(row)
seen = set()
for i in range(7):
    tgt = tuple(-AL[i+1][j] for j in range(7))
    for (a, b, c, d) in quads(tgt):
        row = {}
        ja = act_e(i+1, weights[a])
        if ja is not None:
            t = tuple(sorted((weights[ja], weights[b], weights[c], weights[d])))
            row[mon_idx[t]] = row.get(mon_idx[t], 0) + mult4(t)
        jb = act_e(i+1, weights[b])
        if jb is not None:
            t = tuple(sorted((weights[a], weights[jb], weights[c], weights[d])))
            row[mon_idx[t]] = row.get(mon_idx[t], 0) + mult4(t)
        jc = act_e(i+1, weights[c])
        if jc is not None:
            t = tuple(sorted((weights[a], weights[b], weights[jc], weights[d])))
            row[mon_idx[t]] = row.get(mon_idx[t], 0) + mult4(t)
        jd = act_e(i+1, weights[d])
        if jd is not None:
            t = tuple(sorted((weights[a], weights[b], weights[c], weights[jd])))
            row[mon_idx[t]] = row.get(mon_idx[t], 0) + mult4(t)
        key = tuple(sorted((c, v) for c, v in row.items()))
        if key and key not in seen:
            seen.add(key)
            rows.append(row)
print("distinct E7-invariance equations:", len(rows), "(expect ~ tens of thousands, rank 1035)")

# sparse Gaussian elimination over Q: find nullspace vector(s)
import sys
from fractions import Fraction as Fr
def elim(rows, ncols):
    pivot_row = {}
    for r in rows:
        row = dict(r)
        while row:
            c = min(row)
            if c in pivot_row:
                pv = pivot_row[c][c]
                fac = row[c] / pv
                del row[c]
                for cc, v in pivot_row[c].items():
                    if cc != c:
                        nv = row.get(cc, 0) - fac * v
                        if nv != 0:
                            row[cc] = nv
                        elif cc in row:
                            del row[cc]
            else:
                pivot_row[c] = row
                break
    return pivot_row

pr = elim(rows, nm)
print("number of pivots:", len(pr), "-> nullspace dim:", nm - len(pr))
free = [c for c in range(nm) if c not in pr]
print("free monomials:", len(free))

# construct one nullspace vector: set free vars, back-substitute
def solve_vect(pr, free, choice):
    vals = {}
    for i, c in enumerate(free):
        vals[c] = choice[i]
    for c in sorted(pr, reverse=True):
        row = pr[c]
        s = Fr(0)
        for cc, v in row.items():
            if cc != c:
                s += v * vals[cc]
        vals[c] = -s / row[c]
    return vals

base = solve_vect(pr, free, [Fr(1)] + [Fr(0)]*(len(free)-1))
print("nullspace dimension:", len(free))
assert len(free) == 1, "expected the unique E7-invariant quartic"

# normalize: coefficient of the (h,h,-h,-h) monomial = 1
hmon = tuple(sorted((highest, highest, tuple(-x for x in highest), tuple(-x for x in highest))))
sc = base[mon_idx[hmon]]
base = {k: v/sc for k, v in base.items()}
print("E7-invariant quartic solved: nonzero monomials:", sum(1 for v in base.values() if v != 0), "; sample:", {m: sp.nsimplify(base[k]) for k, m in [(mon_idx[hmon], hmon)]})

def Qval(a, b, c, d):
    t = tuple(sorted(tuple(weights[x]) for x in (a, b, c, d)))
    if t not in mon_idx:
        return Fr(0)
    return mult4(t) * base[mon_idx[t]]

# sanity: B(x,x,x,x) = 24 q(x) on random vectors
import random
random.seed(42)
def qeval(x):
    tot = Fr(0)
    for m, k in mon_idx.items():
        p = base[k]
        for w in m:
            p *= x[idx[w]]
        tot += p
    return tot
def Bdiag(x):
    tot = Fr(0)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    tot += x[a]*x[b]*x[c]*x[d]*Qval(a, b, c, d)
    return tot
for t in range(3):
    x = [Fr(random.randint(-2,2)) for _ in range(n)]
    assert Bdiag(x) == 24*qeval(x), "polarization identity failed"
print("polarization identity B(x,x,x,x) = 24 q(x): OK on random vectors")


# verification pass: with the solved coefficients, all T must vanish
ok = True
cnt_checks = 0
for i in range(7):
    tgt = tuple(-AL[i+1][j] for j in range(7))
    for (a, b, c, d) in quads(tgt):
        cnt_checks += 1
        T = Fr(0)
        ja = act_e(i+1, weights[a])
        if ja is not None: T += Qval(ja, b, c, d)
        jb = act_e(i+1, weights[b])
        if jb is not None: T += Qval(a, jb, c, d)
        jc = act_e(i+1, weights[c])
        if jc is not None: T += Qval(a, b, jc, d)
        jd = act_e(i+1, weights[d])
        if jd is not None: T += Qval(a, b, c, jd)
        if T != 0:
            ok = False
            if cnt_checks <= 5:
                print("first failure at i =", i+1, "quad", (a,b,c,d), "T =", T)
print(f"E7-invariance of q: {cnt_checks} weight-constrained checks,", "ALL ZERO (e_i . q = 0)" if ok else "FAILED")
assert ok

# ---------- Freudenthal triple product ----------
# {a,b,c} := unique vector with J({a,b,c},w) = B(a,b,c,w): {a,b,c} = sum_d B(a,b,c,d)*sigma(-d)*v(-d)
# D(p,q) . v_m = {v_p,v_q,v_m} = B(p,q,m,e)*sigma(t) * v_t,  e = -(w_p+w_q+w_m), t = -e
def Dmap(p, q):
    wpq = tuple(weights[p][k] + weights[q][k] for k in range(7))
    c = [0]*n; s = [None]*n
    for m in range(n):
        e = tuple(-weights[m][k] - wpq[k] for k in range(7))
        if e in idx:
            t = tuple(-x for x in e)
            s[m] = idx[t]
            c[m] = Qval(p, q, m, idx[e]) * sigs[t]
    return c, s

# Q-table on weight-conserving quadruples
Qtab = {}
for (a, b, c, d) in quads((0,)*7):
    Qtab[(a, b, c, d)] = Qval(a, b, c, d)
print("Q-table on weight-conserving quadruples:", len(Qtab))

bad = 0
cnt = 0
for p in range(n):
    for q in range(n):
        c, s = Dmap(p, q)
        tgt = tuple(-weights[p][k] - weights[q][k] for k in range(7))
        for (a, b, c2, d) in quads(tgt):
            cnt += 1
            T = 0
            if s[a] is not None and c[a] != 0:
                T += c[a] * Qtab.get((s[a], b, c2, d), 0)
            if s[b] is not None and c[b] != 0:
                T += c[b] * Qtab.get((a, s[b], c2, d), 0)
            if s[c2] is not None and c[c2] != 0:
                T += c[c2] * Qtab.get((a, b, s[c2], d), 0)
            if s[d] is not None and c[d] != 0:
                T += c[d] * Qtab.get((a, b, c2, s[d]), 0)
            if T != 0:
                bad += 1
                break
        if bad:
            break
    if bad:
        break
print(f"FTS: D(a,b) = {{v_a, v_b, .}} in stab(q): {cnt} T_D checks over all 3136 pairs,", "ALL ZERO" if bad == 0 else "FAILED")
assert bad == 0

# exact rank of span{D(v_p, v_q)} via weight decomposition
blocks = defaultdict(dict)
for p in range(n):
    for q in range(n):
        c, s = Dmap(p, q)
        wpq = tuple(weights[p][k] + weights[q][k] for k in range(7))
        for m in range(n):
            if s[m] is not None and c[m] != 0:
                blocks[wpq].setdefault(s[m], {})[m] = c[m]
total_rank = 0
for w, rows in blocks.items():
    if not rows: continue
    M = sp.zeros(len(rows), n)
    for ri, r in enumerate(sorted(rows)):
        for m, c in rows[r].items():
            M[ri, m] = c
    total_rank += M.rank()
print("exact rank of span{D(v_a, v_b)} (all 3136 pairs, over Q):", total_rank, "(expect 133 = dim e7)")
assert total_rank == 133

# ---------- E6 content: 56 -> 27 + 27bar + 1 + 1 (the J3(O) doubling) ----------
b6 = gram_schmidt(sorted(close(alpha[1:7])))
u1 = tuple(alpha[7])
for b in b6:
    u1 = sub(u1, scl(F(dot(u1, b), dot(b, b)), b))
cnt = Counter()
for w in W56v:
    p6 = project(w, b6)
    pu = scl(F(dot(w, u1), dot(u1, u1)), u1)
    cnt[(norm2(p6), norm2(pu))] += 1
print("56 -> E6 x U(1):", dict(sorted(cnt.items())), "(expect (4/3,1/6)x54 = 27+27bar, (0,3/2)x2 = 1+1)")

g27 = {}
for w in W56v:
    pu = scl(F(dot(w, u1), dot(u1, u1)), u1)
    if norm2(pu) == F(1,6) and pu[0] > 0:
        g27[labels(w)] = w
print("one 27-copy:", len(g27), "weights")
w27 = sorted(g27)
i27 = {w: k for k, w in enumerate(w27)}
A6 = [[AL[i][j] for j in range(6)] for i in range(6)]
def refl6(w, i):
    nn = w[i]
    return tuple(w[j] - nn*A6[i][j] for j in range(6))
mons3 = []
for m in combinations_with_replacement(w27, 3):
    s = tuple(sum(m[j][k] for j in range(3)) for k in range(6))
    if s == (0,)*6:
        mons3.append(m)
print("E6-invariant cubic monomials on the 27:", len(mons3))
mon3_idx = {m: k for k, m in enumerate(mons3)}
nm3 = len(mons3)

def act_e6(i, w):
    v = tuple(w[j] + A6[i][j] for j in range(6))
    return i27[v] if v in i27 else None
wt_index6 = {}
for k, w in enumerate(w27):
    wt_index6.setdefault(w, []).append(k)
sum3_6 = defaultdict(list)
for a in w27:
    for b in w27:
        s = tuple(a[k] + b[k] for k in range(6))
        sum3_6[s].append((a, b))
def Q3val(a, b, c):
    t = sorted((a, b, c))
    cc = Counter(t)
    mult = 1
    for v in cc.values():
        mult *= factorial(v)
    return mult * (1 if tuple(t) in mon3_idx else 0)

def mult3(t):
    cc = Counter(t)
    p = 1
    for v in cc.values():
        p *= factorial(v)
    return p

# solve the E6-invariance linear system over all cubic monomials
rows3 = []
seen3 = set()
for i in range(6):
    tgt = tuple(-A6[i][j] for j in range(6))
    for c in w27:
        need = tuple(tgt[k] - c[k] for k in range(6))
        for (a, b) in sum3_6.get(need, ()):
            row = {}
            ja = act_e6(i, a)
            if ja is not None:
                t = tuple(sorted((w27[ja], b, c)))
                if t in mon3_idx:
                    row[mon3_idx[t]] = row.get(mon3_idx[t], 0) + mult3(t)
            jb = act_e6(i, b)
            if jb is not None:
                t = tuple(sorted((a, w27[jb], c)))
                if t in mon3_idx:
                    row[mon3_idx[t]] = row.get(mon3_idx[t], 0) + mult3(t)
            jc = act_e6(i, c)
            if jc is not None:
                t = tuple(sorted((a, b, w27[jc])))
                if t in mon3_idx:
                    row[mon3_idx[t]] = row.get(mon3_idx[t], 0) + mult3(t)
            row = {k: v for k, v in row.items() if v != 0}
            key = tuple(sorted((k, v) for k, v in row.items()))
            if key and key not in seen3:
                seen3.add(key)
                rows3.append(row)
print("distinct E6-invariance equations on the 27:", len(rows3))
pr3 = elim(rows3, nm3)
print("E6-cubic pivots:", len(pr3), "-> nullspace dim:", nm3 - len(pr3))
free3 = [c for c in range(nm3) if c not in pr3]
assert len(free3) == 1, "expected unique E6-invariant cubic"
base3 = solve_vect(pr3, free3, [Fr(1)] + [Fr(0)]*(len(free3)-1))
print("E6-invariant cubic solved: nonzero monomials:", sum(1 for v in base3.values() if v != 0))

def Q3full(a, b, c):
    t = tuple(sorted((a, b, c)))
    return mult3(t) * base3[mon3_idx[t]]

ok = True
cnt3 = 0
for i in range(6):
    tgt = tuple(-A6[i][j] for j in range(6))
    for c in w27:
        need = tuple(tgt[k] - c[k] for k in range(6))
        for (a, b) in sum3_6.get(need, ()):
            cnt3 += 1
            T = Fr(0)
            ja = act_e6(i, a)
            if ja is not None: T += Q3full(w27[ja], b, c)
            jb = act_e6(i, b)
            if jb is not None: T += Q3full(a, w27[jb], c)
            jc = act_e6(i, c)
            if jc is not None: T += Q3full(a, b, w27[jc])
            if T != 0:
                ok = False
print(f"E6-invariance of the cubic on the 27: {cnt3} weight-constrained checks,", "ALL ZERO (e_i . det = 0)" if ok else "FAILED")
assert ok

print("\n=== summary ===")
print("56 weights from E8 -> E7xA1; self-dual; one Weyl orbit; integer Dynkin labels.")
print("Explicit 56-dim E7 module over Q: Serre relations VERIFIED on the basis.")
print("Unique invariant skew form J (sigma(w) in {+1,-1}, J(h,-h) = 1).")
print("Unique invariant quartic q (1036 torus-invariant monomials, solved over Q);")
print("   E7-invariance verified by exact weight-constrained checks (e_i . q = 0).")
print("Freudenthal triple product {a,b,c} via J({a,b,c},w) = B(a,b,c,w):")
print("   D(a,b) = {v_a,v_b,.} in stab(q) for ALL 3136 basis pairs (T_D = 0);")
print("   span{D(a,b)} = e7 exactly (rank 133 over Q).")
print("56 -> E6 x U(1) = 27 + 27bar + 1 + 1 (J3(O) doubling); unique E6-invariant")
print("   cubic on the 27 (Jordan determinant structure), verified e_i . det = 0.")
