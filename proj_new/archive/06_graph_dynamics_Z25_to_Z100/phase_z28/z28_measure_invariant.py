"""
Z28 Phase 1+2 - pushforward measure on the quotient + invariant hunt.

PHASE 1 (numerical): quotient G_{10,15}/S_10 has |Q| = 136,433 unlabeled
graphs (z26/z27, validated to OEIS A000088(10) = 12,005,168). Sample 300
uniform seeds in the labeled space, converge, canonicalize attractor,
histogram on Q. mu = (T^inf . canon)_* Unif estimated; support, entropy,
concentration recorded.

PHASE 2 (invariant hunt): for each scalar invariant Phi in
 {H2, H4, TRI, SQR, CHR, MAT2, P2} and p in {0,1}, evaluate Phi(T x)-Phi(x)
 on the last 24 states of each of 24 random orbits; record sign structure.
 A Phi that is strictly one-sided everywhere is a Lyapunov/advance
 variable; also record whether attractor values are constant.
"""
import sys, random, math, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

ENT = E.N
M = 15

def deg_moment(e, k):
    return sum(v**k for v in E.degrees(e).values())

def cherries(e):
    return sum(d*(d-1)//2 for d in E.degrees(e).values())

def matchings2(e):
    m = len(e)
    return m*(m-1)//2 - cherries(e)

def triangles(e):
    return E.k_cycle(e, 3)

def squares_(e):
    return E.k_cycle(e, 4)

def minmax_prod(e):
    d = E.degrees(e)
    return sum(min(d[a], d[b])*max(d[a], d[b]) for a, b in e)

CANDS = dict(H2=lambda e: deg_moment(e, 2),
             H4=lambda e: deg_moment(e, 4),
             TRI=triangles, SQR=squares_, CHR=cherries,
             MAT2=matchings2, P2=minmax_prod)

def one_step_deltas(p, s):
    rng = random.Random(9000+97*s)
    e = set()
    while len(e) < M:
        a, b = rng.randrange(ENT), rng.randrange(ENT)
        if a != b:
            e.add(tuple(sorted((a, b))))
    trng = random.Random(7777+s)
    states = []
    for step in range(200):
        states.append(frozenset(e))
        e = set(E.T(frozenset(e), p, trng))
    out = collections.defaultdict(list)
    for x in states[-24:]:
        y = E.T(frozenset(x), p, trng)
        for name, f in CANDS.items():
            out[name].append(f(y) - f(x))
    return out

report = {}
for p in (0.0, 1.0):
    agg = collections.defaultdict(list)
    for s in range(24):
        d = one_step_deltas(p, s)
        for k, v in d.items():
            agg[k] += v
    per = {}
    for k, v in agg.items():
        up = sum(1 for q in v if q > 0)
        dn = sum(1 for q in v if q < 0)
        per[k] = dict(n=len(v), inc=up, dec=dn, flat=len(v)-up-dn,
                      strictly_one_sided=(up == 0 or dn == 0))
    report["p=%s" % p] = per
print(json.dumps(report, indent=2))

supp = collections.Counter(); n_att = 0
seedsN = 300
for s in range(seedsN):
    rng = random.Random(9000+97*s)
    e = set()
    while len(e) < M:
        a, b = rng.randrange(ENT), rng.randrange(ENT)
        if a != b:
            e.add(tuple(sorted((a, b))))
    trng = random.Random(7777+s)
    r = E.run(frozenset(e), 0.0, trng, max_steps=256)
    if r["converged"]:
        supp[r["key"]] += 1
        n_att += 1
    else:
        supp["NONCONV"] += 1
H = 0.0
for k, v in supp.items():
    q = v / seedsN
    H -= q * math.log2(q)
meas = dict(n_seeds=seedsN, n_converged=n_att,
            support_size=len(supp),
            H_pushforward=round(H, 4),
            I_quotient=round(math.log2(136433), 4))
print(json.dumps(meas, indent=2))
