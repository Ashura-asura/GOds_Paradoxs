"""
Z27  universality sweep (Possibility 4) + exact quotient sizes.

PART 1 (mechanism universality): for (N,M) in {(8,12),(10,15),(12,18)}
run the witness-free conservative exchange at p in {0,1}, 8 random seeds
each, and certify on every visited state:
  - add-extremum iso-uniqueness      (the Z26 asymmetry)
  - rem-extremum iso-uniqueness
  - period distribution
  - distinct attractors across seeds + their n3/n4 ratios
Checks which structural facts survive N.

PART 2 (exact quotient sizes via Polya, pair-action of S_N):
  validated internally: N=10,M=15 -> 136,433 and N=10 total -> 12,005,168
  then computes (8,12) and (12,18).
"""
import sys, math, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

# ---------- mechanism sweep ----------
def extremal_iso(e, p, N):
    d = E.degrees(e); ed = set(e)
    nonedge = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in ed]
    rem = sorted((d[a] + d[b], (a, b)) for a, b in ed)
    add = sorted((d[a] + d[b], (a, b)) for a, b in nonedge)
    if p < 0.5:
        sc_r, sc_a = rem[0][0], add[-1][0]
        R = [x for s, x in rem if s == sc_r]; A = [x for s, x in add if s == sc_a]
    else:
        sc_r, sc_a = rem[-1][0], add[0][0]
        R = [x for s, x in rem if s == sc_r]; A = [x for s, x in add if s == sc_a]
    def n_iso(cands, remove):
        ks = set()
        for (u, v) in cands:
            gg = set(ed)
            if remove: gg.discard((u, v))
            else: gg.add((u, v))
            ks.add(E.canon(frozenset(gg)))
        return len(ks)
    return n_iso(R, True), n_iso(A, False)

def orbit(N, M, p, s):
    E.N = N; E._MEMO.clear(); E._AUT.clear(); E._KC.clear()
    rng = random.Random(4000 + 97 * s)
    e = set()
    while len(e) < M:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b: e.add((min(a, b), max(a, b)))
    trng = random.Random(7000 + s)
    hist = {}; states = []
    ru = au = tot = 0; period = -1
    for step in range(200):
        fk = frozenset(e); c = E.canon(fk)
        if c in hist:
            period = step - hist[c]; states = states[hist[c]:]; break
        hist[c] = step; states.append(fk)
        r_iso, a_iso = extremal_iso(fk, p, N)
        ru += (r_iso == 1); au += (a_iso == 1); tot += 1
        e = set(E.T(fk, p, trng))
    n3 = min(E.k_cycle(g, 3) for g in states) if states else None
    n4 = min(E.k_cycle(g, 4) for g in states) if states else None
    return dict(period=period, add_unique_frac=(au / tot if tot else None),
                rem_unique_frac=(ru / tot if tot else None),
                key=E.canon(states[0]) if states else None,
                n3=n3, n4=n4)

sweep = {}
for N, M in [(8, 12), (10, 15), (12, 18)]:
    for p in (0.0, 1.0):
        runs = [orbit(N, M, p, s) for s in range(8)]
        conv = [r for r in runs if r["period"] > 0]
        keys = collections.Counter(r["key"] for r in conv)
        ratios = sorted({(r["n3"], r["n4"]) for r in conv})
        sweep[f"N{N}_M{M}_p{p}"] = dict(
            periods=sorted({r["period"] for r in conv}),
            add_unique_mean=round(sum(r["add_unique_frac"] for r in conv) / max(1, len(conv)), 3),
            rem_unique_mean=round(sum(r["rem_unique_frac"] for r in conv) / max(1, len(conv)), 3),
            n_attractors=len(keys), n_seeds=len(conv),
            ratio_pairs=[list(t) for t in ratios])
print(json.dumps(sweep, indent=2))

# ---------- exact quotient sizes ----------
def partitions(n, mx=None):
    if mx is None: mx = n
    if n == 0: yield []; return
    for f in range(min(n, mx), 0, -1):
        for rest in partitions(n - f, f):
            yield [f] + rest

def edge_cycle_sparse(cyc):
    cnt = {0: 1}
    mults = collections.Counter()
    for r in cyc:
        if r == 1: continue
        if r % 2: mults[r] += (r - 1) // 2
        else:
            mults[r] += (r - 2) // 2; mults[r // 2] += 1
    for i in range(len(cyc)):
        for j in range(i + 1, len(cyc)):
            r, s = cyc[i], cyc[j]
            g = math.gcd(r, s); mults[(r * s) // g] += g
    for L, k in mults.items():
        for _ in range(k):
            cnt = collections.Counter({d + L: v for d, v in cnt.items()}) + collections.Counter(cnt)
    return cnt

def class_size(cyc, n):
    c = collections.Counter(cyc); den = 1
    for L, m in c.items(): den *= (L ** m) * math.factorial(m)
    return math.factorial(n) // den

def unlabeled(N, M):
    tot = 0; tot_all = 0
    maxM = N * (N - 1) // 2
    for cyc in partitions(N):
        cs = class_size(cyc, N); poly = edge_cycle_sparse(cyc)
        tot += cs * poly.get(M, 0)
        tot_all += cs * sum(poly.get(k, 0) for k in range(maxM + 1))
    f = math.factorial(N)
    return tot // f, tot_all // f

u10_15, t10 = unlabeled(10, 15)
assert u10_15 == 136433, u10_15
assert t10 == 12005168, t10
quot = {}
for N, M in [(8, 12), (10, 15), (12, 18)]:
    u, t = unlabeled(N, M)
    quot[f"{N},{M}"] = dict(unlabeled_M=u, unlabeled_total=t,
        I_labeled=round(math.log2(math.comb(N*(N-1)//2, M)), 4),
        I_quotient=round(math.log2(u), 4),
        gauge_bits=round(math.log2(math.comb(N*(N-1)//2, M)) - math.log2(u), 4))
print(json.dumps(quot, indent=2))

