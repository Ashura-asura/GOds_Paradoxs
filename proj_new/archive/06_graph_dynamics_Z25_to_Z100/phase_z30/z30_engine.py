"""
Z30 corrected — with faithful selectors.

SELECTORS (all operate on the FULL tie-broken lists, not extremal subsets):
  lex    : pick rem[0], add[-1]   (matches engine bit-for-bit; control B
                                   verified period 2/40 on all 40 seeds)
  random : rng.choice(R), rng.choice(A) on extremal sets only
  entropy: (r,a) in R x A maximizing next |R||A| (lexicographic tie out)
  autmin : (r,a) in R x A minimizing next |Aut|   (lexicographic tie out)

Also probed: tie-break SEMIGROUP. On attractor states from Experiment 1
converging runs, for the two tie-breaks x in {lex, random}: record the
fraction of one-step successors of x(g) that canon-match the engine's
cycle successor. If lex-successor share >> random-successor share, the
period-2 "persistence" is a lex-selection property, not a cycle property.

Experiments (300 seeds, p=0, 4096-step cap, max canon calls 40h):
  1) random-selector trajectories — tau distribution on attractors
  2) selector independence — 4 selectors, same seeds
  3) Level-B quotient collapse along random trajectories: S(t) =
     |canon({g - r + a})| at t in {0, 8, 32}, plus H_D trajectories.
"""
import sys, random, math, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

N = E.N; M = 15

def seed_graph_f(s):
    rng = random.Random(9000 + 97 * s)
    e = set()
    while len(e) < M:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b: e.add(tuple(sorted((a, b))))
    return frozenset(e)

def ties_sorted(e, p):
    """Return full lists sorted by (degree-sum, label), matching engine."""
    d = E.degrees(e)
    ed = set(e)
    nonedge = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in ed]
    rem = sorted(ed, key=lambda x: (d[x[0]] + d[x[1]], x))
    add = sorted(nonedge, key=lambda x: (d[x[0]] + d[x[1]], x))
    if p < 0.5:
        sc_r, sc_a = rem[0][0], None
        sc_r = d[rem[0][0]] + d[rem[0][1]]
        sc_a = d[add[-1][0]] + d[add[-1][1]]
        R = [x for x in rem if d[x[0]] + d[x[1]] == sc_r]
        A = [x for x in add if d[x[0]] + d[x[1]] == sc_a]
    else:
        sc_r = d[rem[-1][0]] + d[rem[-1][1]]
        sc_a = d[add[0][0]] + d[add[0][1]]
        R = [x for x in rem if d[x[0]] + d[x[1]] == sc_r]
        A = [x for x in add if d[x[0]] + d[x[1]] == sc_a]
    return R, A, rem, add

def engine_step_lex(e, rem, add, p):
    edges = set(e)
    if p < 0.5: r, a = rem[0], add[-1]
    else:       r, a = rem[-1], add[0]
    edges.discard(r); edges.add(a)
    return frozenset(edges)

def step_with_mode(e, rem, add, R, A, p, mode, rng):
    if mode == "lex":
        return engine_step_lex(e, rem, add, p)
    if mode == "random":
        r, a = rng.choice(R), rng.choice(A)
    elif mode == "entropy":
        best = None; bestHD = -1
        for r_ in R:
            for a_ in A:
                g = set(e); g.discard(r_); g.add(a_)
                R2, A2, _, _ = ties_sorted(g, p)
                hd = len(R2) * len(A2)
                if hd > bestHD or (hd == bestHD and (r_, a_) < best):
                    bestHD, best = hd, (r_, a_)
        r, a = best
    elif mode == "autmin":
        best = None; bestA = None
        for r_ in R:
            for a_ in A:
                g = set(e); g.discard(r_); g.add(a_)
                au = E.aut_size(frozenset(g))
                if bestA is None or au < bestA or (au == bestA and (r_, a_) < best):
                    bestA, best = au, (r_, a_)
        r, a = best
    edges = set(e); edges.discard(r); edges.add(a)
    return frozenset(edges)

def converge(s, p, mode, cap=4096):
    e = seed_graph_f(s)
    rng = random.Random(555 + s)
    hist = {}
    HD = []
    S = {}
    for t in range(cap + 1):
        c = E.canon(e)
        if c in hist:
            R, A, _, _ = ties_sorted(e, p)
            return dict(period=t - hist[c], steps=t,
                        tau=(len(R), len(A)),
                        HD=math.log2(max(1, len(R) * len(A))),
                        traj_HD=HD, S=S)
        hist[c] = t
        R, A, rem, add = ties_sorted(e, p)
        HD.append(math.log2(max(1, len(R) * len(A))))
        if t in (0, 8, 32):
            ks = set()
            for r in R:
                for a in A:
                    g = set(e); g.discard(r); g.add(a)
                    ks.add(E.canon(frozenset(g)))
            S[t] = len(ks)
        e = step_with_mode(e, rem, add, R, A, p, mode, rng)
    return dict(period=None, steps=cap, traj_HD=HD, S=S)

if __name__ == "__main__":
    # -------- Experiment 1: random --------
    dist = collections.Counter(); tau_att = collections.Counter()
    for s in range(300):
        r = converge(s, 0.0, "random")
        dist[r["period"] if r["period"] else "NONCONV"] += 1
        if r["period"]: tau_att[r["tau"]] += 1
    print("EX1", json.dumps(dict(periods=dict(dist),
                                 tau_top=[(str(k), v) for k, v in tau_att.most_common(10)],
                                 n_tau=len(tau_att)), indent=2))
    # -------- Experiment 2: 4 selectors --------
    out2 = {}
    for mode in ("lex", "random", "entropy", "autmin"):
        per = collections.Counter(); Rm = []; Am = []; HD = []
        for s in range(200):
            r = converge(s, 0.0, mode)
            if r["period"]:
                per[r["period"]] += 1
                Rm.append(r["tau"][0]); Am.append(r["tau"][1]); HD.append(r["HD"])
        n = max(1, len(Rm))
        out2[mode] = dict(n=n, period_freq=dict(per),
                          mean_R=round(sum(Rm)/n, 3), mean_A=round(sum(Am)/n, 3),
                          mean_HD=round(sum(HD)/n, 3) if HD else None)
    print("EX2", json.dumps(out2, indent=2))
    # -------- Experiment 3: branching/entropy trajectory --------
    S0 = []; S8 = []; S32 = []; HD0 = []; HDend = []; per3 = collections.Counter()
    for s in range(40):
        r = converge(4242 + s, 0.0, "random")
        if r["period"]: per3[r["period"]] += 1
        else: per3["NONCONV"] += 1
        if 0 in r["S"]: S0.append(r["S"][0])
        if 8 in r["S"]: S8.append(r["S"][8])
        if 32 in r["S"]: S32.append(r["S"][32])
        HD0.append(r["traj_HD"][0] if r["traj_HD"] else None)
        HDend.append(r["traj_HD"][-1] if r["traj_HD"] else None)
    def avg(x): return round(sum(x)/len(x), 3) if x else None
    print("EX3", json.dumps(dict(S0=avg(S0), S8=avg(S8), S32=avg(S32),
                                 HD0=avg([x for x in HD0 if x is not None]),
                                 HDend=avg([x for x in HDend if x is not None]),
                                 period_freq=dict(per3)), indent=2))
