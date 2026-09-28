src = open('tmp_task_e_fts.py').read()
part = src.split('# ---------- Freudenthal triple product ----------')[0]
exec(part)
exec(src.split('# ---------- Freudenthal triple product ----------')[1].split('bad = 0')[0])

# direct check: B(Dx, x, x, x) for random x, D = D(0,0)
import random
random.seed(1)
c, s = Dmap(0, 0)
def B4(a, b, cc, d):
    t = tuple(sorted(tuple(weights[x]) for x in (a, b, cc, d)))
    if t not in Qtab_keyed and False:
        pass
    return Qval(a, b, cc, d)
# Qval is available (defined in exec part)
def Bdiag_y(ex, x):
    tot = Fr(0)
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                for d in range(n):
                    tot += ex[a]*x[b]*x[cc]*x[d]*Qval(a, b, cc, d)
    return tot

for t in range(3):
    x = [Fr(random.randint(-2,2)) for _ in range(n)]
    Dx = [Fr(0)]*n
    for m in range(n):
        if s[m] is not None and c[m] != 0:
            Dx[s[m]] += c[m]*x[m]
    print("trial", t, "B(Dx,x,x,x) =", Bdiag_y(Dx, x))
