"""
Z30 — DYNAMICS OF THE CHOICE SPACE. Three experiments, all L1-numerical.

State: labeled (10,15)-graphs. Quotient Q = G/S_10 (|Q| = 136,433, exact).
tau(G) = ( |R|, |A|, |R/S_G|, |A/S_G|, |Aut(G)|, H_D = log2(|R|*|A|) ).

NO lexicographic canon is used in the DYNAMICS of Experiments 1-3.
Selection is the pure RNG (or selector) choice within the extremal ties.
Canon is used ONLY as the Level-B measuring device.

Experiment 1 — random-selector trajectories (300 runs, 4,096 steps).
  Report: attractor periods (L2-fallback via INV key), attractor count,
  tau-distribution on attractors, attractor reachability.

Experiment 2 — selector independence at p=0. 4 selectors x 200 runs:
     lex (engine's, needs raw-label trajectory for fairness = lex on
          labeled edge order), random, entropy-max, aut-min.
  Distribution-shaped metrics compared: within-cell std of mean |R|,
  mean |A|, mean H_D, period frequencies.

Experiment 3 — degeneracy entropy & branching:
  per 40 runs, record H_D(t) full trajectory to convergence (or cap),
  plus the Level-B quotient-collapse rate: # distinct canon classes among
  the full R x A successor set at t=0, t=8, t=32, attractor.
"""
import sys, random, math, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

N = E.N
M = 15

# ---- extremal tie sets ----
def ties(e, p):
    d = E.degrees(e); ed = set(e)
    nonedge = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in ed]
    rs = sorted((d[a] + d[b], (a, b)) for a, b in ed)
    asd = sorted((d[a] + d[b], (a, b)) for a, b in nonedge)
    sc_r = rs[0][0] if p < 0.5 else rs[-1][0]
    sc_a = asd[-1][0] if p < 0.5 else asd[0][0]
    R = [x for s, x in rs if s == sc_r]
    A = [x for s, x in asd if s == sc_a]
    return R, A

def orbit_lengths(edges, which):
    """|which/S_G| via canonical deletion orbit type for 'rem'; addition
    orbit type for 'add' (canon of the supergraph on N vertices)."""
    out = set()
    for (u, v) in which:
        g = set(edges)
        if edges == 'REM': pass
    return out

def orbit_count_remove(e, R):
    c = set()
    for r in R:
        g = set(e); g.discard(r)
        c.add(E.canon(frozenset(g)))
    return len(c)

def orbit_count_add(e, A):
    ed = set(e); c = set()
    for a in A:
        g = set(ed); g.add(a)
        c.add(E.canon(frozenset(g)))
    return len(c)

def tau(e, p):
    R, A = ties(e, p)
    return dict(Rsize=len(R), Asize=len(A),
                Rorbits=orbit_count_remove(e, R),
                Aorbits=orbit_count_add(e, A),
                AUT=E.aut_size(e),
                HD=math.log2(max(1, len(R) * max(1, len(A)))))

def select(R, A, mode, e, rng):
    if mode == "lex":
        return min(R), min(A)          # engine's deterministic pick
    if mode == "random":
        return rng.choice(R), rng.choice(A)
    if mode == "entropy":
        # pick the (r,a) whose outcome maximizes |R|*|A| of the next state
        best, besthd = None, -1
        for r in R:
            for a in A:
                g = set(e); g.discard(r); g.add(a)
                R2, A2 = ties(g, 0.0)
                hd = len(R2) * len(A2)
                if hd > besthd or (hd == besthd and (r, a) < best):
                    besthd, best = hd, (r, a)
        return best
    if mode == "autmin":
        # pick the (r,a) producing the least symmetric next state
        best, bestaut = None, None
        for r in R:
            for a in A:
                g = set(e); g.discard(r); g.add(a)
                au = E.aut_size(frozenset(g))
                if bestaut is None or au < bestaut or (au == bestaut and (r, a) < best):
                    bestaut, best = au, (r, a)
        return best
    raise ValueError(mode)

def succ_keys(e, R, A):
    out = set()
    for r in R:
        for a in A:
            g = set(e); g.discard(r); g.add(a)
            out.add(E.canon(frozenset(g)))
    return out

def converge(seed_rng, p, mode, sel_rng, max_steps=4096,
             canon_measure_points=(0, 8, 32, 999999)):
    e = set()
    while len(e) < M:
        a, b = seed_rng.randrange(N), seed_rng.randrange(N)
        if a != b:
            e.add(tuple(sorted((a, b))))
    e = frozenset(e)
    hist = {}
    traj_HD = []
    S0 = S8 = S32 = None
    att_period = None; att_moment = None
    for t in range(max_steps + 1):
        if t in canon_measure_points:
            c = E.canon(e)
            if c in hist:
                att_period = t - hist[c]
                att_moment = t
                break
            hist[c] = t
        R, A = ties(e, p)
        tau_t = dict(Rsize=len(R), Asize=len(A),
                     HD=math.log2(max(1, len(R) * max(1, len(A)))))
        traj_HD.append(tau_t["HD"])
        if t == 0: S0 = len(succ_keys(e, R, A))
        if t == 8: S8 = len(succ_keys(e, R, A))
        if t == 32: S32 = len(succ_keys(e, R, A))
        r, a = select(R, A, mode, set(e), sel_rng)
        g = set(e); g.discard(r); g.add(a)
        e = frozenset(g)
    cyc_tau = None
    if att_period is not None:
        cyc_tau = tau(e, p)
    return dict(period=att_period, steps=att_moment,
                S0=S0, S8=S8, S32=S32,
                final_tau=cyc_tau, HD_traj=traj_HD)

# ============ Experiment 1 =====================================
res1 = collections.Counter(); tau_att = collections.Counter()
period_c = collections.Counter()
for s in range(300):
    seed_rng = random.Random(9000 + 97 * s)
    sel_rng = random.Random(555 + s)
    r = converge(seed_rng, 0.0, "random", sel_rng)
    if r["period"] is not None:
        res1["converged"] += 1
        period_c[r["period"]] += 1
        t = r["final_tau"]
        tau_att[(t["Rsize"], t["Asize"], t["Rorbits"], t["Aorbits"])] += 1
    else:
        res1["nonconverged"] += 1
print("EXPERIMENT 1: random selector, 300 seeds, 4096-step cap")
print(json.dumps(dict(convergence=dict(res1),
                      periods=dict(period_c),
                      distinct_attractor_tau=len(tau_att),
                      tau_histogram_top10=[(str(k), v) for k, v in tau_att.most_common(10)]),
                 indent=2))

# ============ Experiment 2 =====================================
sel_stats = {}
for mode in ("lex", "random", "entropy", "autmin"):
    collect = collections.defaultdict(list)
    nsr = 200
    for s in range(nsr):
        seed_rng = random.Random(9000 + 97 * s)
        sel_rng = random.Random(555 + s)
        r = converge(seed_rng, 0.0, mode, sel_rng)
        if r["final_tau"] is not None:
            collect["Rsize"].append(r["final_tau"]["Rsize"])
            collect["Asize"].append(r["final_tau"]["Asize"])
            collect["HD"].append(r["final_tau"]["HD"])
            collect["period"].append(r["period"])
    means = {k: sum(v) / len(v) for k, v in collect.items() if v}
    sds = {k: (sum((x - means[k])**2 for x in v) / len(v)) ** 0.5
           for k, v in collect.items() if v}
    sel_stats[mode] = dict(n=len(collect["Rsize"]),
                           mean={k: round(means[k], 3) for k in means},
                           sd={k: round(sds[k], 3) for k in sds},
                           period_freq=dict(collections.Counter(collect["period"])))
print("EXPERIMENT 2: selector independence, p=0, 200 seeds each")
print(json.dumps(sel_stats, indent=2))

# ============ Experiment 3 =====================================
row = {}
for s in range(40):
    seed_rng = random.Random(4242 + 41 * s)
    sel_rng = random.Random(777 + s)
    r = converge(seed_rng, 0.0, "random", sel_rng)
    row[s] = dict(period=r["period"], steps=r["steps"],
                  S0=r["S0"], S8=r["S8"], S32=r["S32"],
                  HD0=r["HD_traj"][0],
                  HD_end=r["HD_traj"][-1],
                  HD_min=min(r["HD_traj"]), HD_max=max(r["HD_traj"]),
                  HD_len=len(r["HD_traj"]))
S0v = [v["S0"] for v in row.values()]
S8v = [v["S8"] for v in row.values() if v["S8"]]
S32v = [v["S32"] for v in row.values() if v["S32"]]
per = [v["period"] for v in row.values() if v["period"]]
out3 = dict(n=40,
            converged=sum(1 for v in row.values() if v["period"] is not None),
            mean_future_classes_t0=round(sum(S0v) / len(S0v), 3) if S0v else None,
            mean_future_classes_t8=round(sum(S8v) / len(S8v), 3) if S8v else None,
            mean_future_classes_t32=round(sum(S32v) / len(S32v), 3) if S32v else None,
            period_freq=dict(collections.Counter(per)),
            HD0_mean=round(sum(v["HD0"] for v in row.values()) / 40, 3),
            HDend_mean=round(sum(v["HD_end"] for v in row.values()) / 40, 3))
print("EXPERIMENT 3: degeneracy-entropy trajectory + quotient-collapse")
print(json.dumps(out3, indent=2))
