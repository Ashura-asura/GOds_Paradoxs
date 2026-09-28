"""
Z29 residual: self-reinforcement fraction.

The attractor swap is one point in a large tie-space (R x A). Test:
what fraction of the full tie-space (R x A) maps back onto the attractor's
own 2-cycle (the two canon classes of its states), vs escapes?

If the fraction is high, the 2-cycle survives tie-collapse numerically
because MOST extremal rewires stay in its two classes (coarse stability).
If the fraction is low, the cycle is a measure-zero point kept only by the
engine's specific tie-break rule -> Rule-8 row closes cleanly.
"""
import sys, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

N = E.N
M = 15

def extremal_sets(e, p):
    d = E.degrees(e); ed = set(e)
    nonedge = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in ed]
    rem = sorted((d[a] + d[b], (a, b)) for a, b in ed)
    add = sorted((d[a] + d[b], (a, b)) for a, b in nonedge)
    if p < 0.5:
        sc_r, sc_a = rem[0][0], add[-1][0]
    else:
        sc_r, sc_a = rem[-1][0], add[0][0]
    return [x for s, x in rem if s == sc_r], [x for s, x in add if s == sc_a]

def attractor_cycle(seed_idx, p):
    rng = random.Random(9000 + 97 * seed_idx)
    e = set()
    while len(e) < M:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b:
            e.add(tuple(sorted((a, b))))
    trng = random.Random(7777 + seed_idx)
    hist = {}; seq = []
    for step in range(256):
        fk = frozenset(e); c = E.canon(fk)
        if c in hist:
            return seq[hist[c]:]
        hist[c] = step; seq.append(fk)
        e = set(E.T(fk, p, trng))
    return None

for p in (0.0, 1.0):
    fracs = []
    stay_pairs = 0; tot_pairs = 0
    for s in range(120):
        cyc = attractor_cycle(s, p)
        if not cyc or len(cyc) != 2:
            continue
        a, b = cyc
        ka, kb = E.canon(a), E.canon(b)
        ok = 0; tot = 0
        for g in (a, b):
            R, A = extremal_sets(g, p)
            ed = set(g)
            for r in R:
                for ad in A:
                    gg = set(ed); gg.discard(r); gg.add(ad)
                    k = E.canon(frozenset(gg))
                    tot += 1
                    if k == ka or k == kb:
                        ok += 1
        if tot:
            fracs.append(ok / tot)
            stay_pairs += ok; tot_pairs += tot
    fracs.sort()
    n = len(fracs)
    out = dict(p=p,
               attractors_used=n,
               mean_stay_fraction=round(sum(fracs) / n, 4),
               median_stay_fraction=round(fracs[n // 2], 4),
               frac_ge_half=round(sum(1 for f in fracs if f >= 0.5) / n, 4),
               tie_space_total_pairs=tot_pairs,
               stay_pairs=stay_pairs)
    print(json.dumps(out, indent=2))
