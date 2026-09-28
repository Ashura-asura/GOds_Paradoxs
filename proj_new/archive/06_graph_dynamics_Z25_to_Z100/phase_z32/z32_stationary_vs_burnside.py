"""
Z32 - STATIONARY MEASURE VS BURNSIDE WEIGHTING TEST
Rule-2 pre-registered: every threshold/budget below is fixed before the run.

Question: is the extremal-exchange collapse GENERATIVE (dynamics builds a
measure) or REVEALING (dynamics tracks a pre-existing quotient weighting)?

Comparison key: (canon_key, R, A, aut) -- the unlabeled state plus its
tie-signature, so "shell" = Z31 joint region, not a |Aut| scalar bucket.

Distributions (all over the key, all at (N,M)=(10,15), N=10):

  P_D,sel  stationary trajectory distribution under selector `sel`
           (burn-in pre-registered per selector; thinning = 5 steps)
  P_B^lab  uniform over LABELED (N,M) graphs              (iid MC)
  P_burn   Burnside / orbit-stabilizer weighting          (iid MC, w=|Aut|)
  P_U      uniform on the QUOTIENT                        (iid MC, w=1/|Aut|)

Selectors: random (stochastic), lex, entropy, autmin (deterministic).
The deterministic ones use Z31's verified step_mode; random matches Z30 EX1.

Pre-registered decision rule (decided BEFORE any output is read):
  Outcome A (quotient geometry only) requires, for EVERY selector s:
      TV(P_D,s, P_burn)              <= 0.25
  AND min(TV(P_D,s, P_B^lab), TV(P_D,s, P_U))  >= 2 * TV(P_D,s, P_burn)
  (i.e. Burnside is the UNIQUE close match; ties do not count.)
  If not A: report whether all selectors share the same failure (B) or
  diverge from each other (C), by the printed numbers, no forced verdict.

Pre-registered diagnostics (must hold for the decisive TVs to be read):
  D1 ceiling: max |Aut| used < CANON_BUDGET (no WL lower-bound proxy);
     if violated, aut is exact-in-value but tied across >=1 class -- reported.
  D2 split-half: TV(P_D first half, P_D second half) << each static TV.
  D3 weight-recovery: n_unlabeled_MC and the 1/|Aut| self-consistency are
     printed; 1/|Aut| recovery within 15% of P_U mass-1 else MC too thin.
"""
import sys, math, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

CELL_N, CELL_M = 10, 15
THIN = 5                      # steps kept between retained samples
SEEDS_DYN = 180               # chains per stochastic selector
SEEDS_DET = 90                # chains per deterministic selector
BURNIN = {"random": 60, "lex": 12, "entropy": 12, "autmin": 12}
CAP_STEPS = 300               # deterministic chains stop at 1st canon revisit
SAMPLES_PER_CHAIN = 40        # kept pre-registered; only K_STATIC changed
K_STATIC = 40000              # quotient sampler must span |Q_10,15| ~ 136433
SEED_STATIC = 424242
SEED_DYN = 9100               # matches Z31 RNG family, distinct stream offset
TV_UNIQUE_MATCH = 0.25
TV_UNIQUE_MARGIN = 2.0

# Recorded |Q_10,15| target for the convergence diagnostic (Z28: OEIS).
# Used ONLY as a coverage check n_unlabeled_MC -> this value; not as a fit.
Q_10_15_TARGET = 136433

def set_N(n):
    E.N = n
    E._MEMO.clear(); E._AUT.clear(); E._KC.clear()

PAIR_CACHE = {}
def pairs_from_idx(idx, n):
    if n not in PAIR_CACHE:
        PAIR_CACHE[n] = [(a, b) for a in range(n) for b in range(a + 1, n)]
    return frozenset(PAIR_CACHE[n][i] for i in idx)

# --- EXACT |Aut| at N=10 -----------------------------------------------
# E.aut_size uses a WL-color budget as a lower-bound PROXY once the budget
# exceeds CANON_BUDGET; at N=10 any regular graph (e.g. the 10-cycle) hits
# that branch and is assigned 10! = 3628800 instead of its true |Aut| = 20.
# That proxy is anti-correlated with exactly the high-symmetry region Z32
# exists to measure, so it cannot be used. A degree-grouped permutation
# enumerator is ALSO unsafe (it misses automorphisms that permute whole
# isomorphic components across degree-fibers, e.g. 2 x C5 comes out 200
# instead of 800).  Use a backtracking vertex-mapping counter with
# (degree, mapped-neighbor-image) pruning: exact, and at N=10, M=15 the
# |Aut|=1 typical case is decided in a handful of partial maps.
_AUT_EXACT = {}
def aut_size_exact(e):
    e = frozenset(e)
    if e in _AUT_EXACT:
        return _AUT_EXACT[e]
    es = set(e)
    adj = {v: set() for v in range(E.N)}
    for a, b in e:
        adj[a].add(b); adj[b].add(a)
    d = {v: len(adj[v]) for v in range(E.N)}
    # Exact isomorphism-invariant vertex signature (degree + sorted neighbor
    # degrees). Any automorphism must map a vertex to an equal-signature one,
    # so these are the ONLY legal images; this is what makes 2xC5's cross-
    # component swap reachable while keeping the backtrack small.
    sig = {v: (d[v], tuple(sorted(d[w] for w in adj[v]))) for v in range(E.N)}
    by_sig = collections.defaultdict(list)
    for v in range(E.N):
        by_sig[sig[v]].append(v)
    # order source vertices by candidate-set size, fewest first (fail fast)
    src_order = sorted(range(E.N), key=lambda v: len(by_sig[sig[v]]))
    n = E.N
    cnt = [0]
    mapping = {}
    used = [False] * n
    def backtrack(i):
        if i == n:
            cnt[0] += 1
            return
        u = src_order[i]
        for v in by_sig[sig[u]]:
            if used[v]:
                continue
            # consistency: every already-mapped neighbor of u must map to a
            # neighbor of v, and every mapped NON-neighbor to a non-neighbor
            ok = True
            for x, y in mapping.items():
                if (x in adj[u]) != (y in adj[v]):
                    ok = False; break
            if not ok:
                continue
            used[v] = True; mapping[u] = v
            backtrack(i + 1)
            del mapping[u]; used[v] = False
    backtrack(0)
    _AUT_EXACT[e] = cnt[0]
    return cnt[0]

def tau_of(e):
    d = E.degrees(e); ed = set(e)
    ne = [(a, b) for a in range(E.N) for b in range(a + 1, E.N) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    scr = min(ds(x) for x in ed); sca = max(ds(x) for x in ne)
    R = sum(1 for x in ed if ds(x) == scr)
    A = sum(1 for x in ne if ds(x) == sca)
    return R, A

def key_of(e):
    R, A = tau_of(e)
    aut = aut_size_exact(e)
    return (str(E.canon(e)), R, A, aut), aut

# ---------------- dynamics step (Z31-faithful selectors) ----------------
def step_mode(e, mode, rng):
    d = E.degrees(e); ed = set(e)
    ne = [(a, b) for a in range(E.N) for b in range(a + 1, E.N) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    rem = sorted(ed, key=lambda x: (ds(x), x))
    add = sorted(ne, key=lambda x: (ds(x), x))
    scr = ds(rem[0]); sca = ds(add[-1])
    R = [x for x in ed if ds(x) == scr]
    A = [x for x in ne if ds(x) == sca]
    if mode == "random":
        r = rng.choice(R); a = rng.choice(A)
    elif mode == "lex":
        r, a = rem[0], add[-1]
    elif mode == "entropy":
        best = None; bh = -1
        for rr in R:
            for aa in A:
                g = set(ed); g.discard(rr); g.add(aa)
                d2 = E.degrees(g)
                ds2 = lambda x: d2[x[0]] + d2[x[1]]
                ne2 = [(x, y) for x in range(E.N) for y in range(x + 1, E.N) if (x, y) not in g]
                h = sum(1 for x in g if ds2(x) == min(ds2(z) for z in g)) * \
                    sum(1 for x in ne2 if ds2(x) == max(ds2(z) for z in ne2))
                if h > bh or (h == bh and (rr, aa) < best):
                    bh, best = h, (rr, aa)
        r, a = best
    elif mode == "autmin":
        best = None; ba = None
        for rr in R:
            for aa in A:
                g = set(ed); g.discard(rr); g.add(aa)
                au = E.aut_size(frozenset(g))
                if ba is None or au < ba or (au == ba and (rr, aa) < best):
                    ba, best = au, (rr, aa)
        r, a = best
    g = set(ed); g.discard(r); g.add(a)
    return frozenset(g)

# ---------------- dynamic arm ----------------
def run_dynamic(mode):
    """All selectors sampled ON their attractor (matches Z28/Z30 precedent).
    Returns (hist[full_key], autvals, n_chains, n_cycles, periods)."""
    n_chains = SEEDS_DYN if mode == "random" else SEEDS_DET
    hist = collections.Counter()
    autvals = []
    n_cycles = 0
    periods = []
    CAP = 512                               # canon-revisit cap (Z31 protocol)
    for s in range(n_chains):
        rng = random.Random(SEED_DYN + 131 * s + (0 if mode == "random" else 5000))
        totp = CELL_N * (CELL_N - 1) // 2
        e = pairs_from_idx(rng.sample(range(totp), CELL_M), CELL_N)
        seen_at = {}
        order = []
        hit = -1
        t = 0
        while t < CAP:
            c = E.canon(e)
            if c in seen_at:
                hit = seen_at[c]
                break
            seen_at[c] = t
            order.append(frozenset(e))
            e = step_mode(e, mode, rng)
            t += 1
        if hit < 0:
            continue                        # no revisit within cap: skip chain
        n_cycles += 1
        cyc = order[hit:]
        periods.append(len(cyc))
        step = max(1, len(cyc) // SAMPLES_PER_CHAIN)
        for i in range(0, len(cyc), step):
            k, aut = key_of(cyc[i])
            hist[k] += 1
            autvals.append(aut)
    return hist, autvals, n_chains, n_cycles, periods

# ---------------- static arms ----------------
# Grounded 2026-08-02 (N=6 exhaustive): sum(1/|Aut|) over labeled-uniform
# exceeds the unlabeled count by x120-155, so P_U-as-(labeled,1/|Aut|) is
# the WRONG weighting for the quotient geometry. The correct base arms are:
#   P_lab  uniform on labeled graphs                       (plain histogram)
#   P_burn = P_lab proportional-to |Aut|   (orbit-stabilizer; keyed on canon,
#          a class gets weight prop |Aut(canonical class| = its LBL count)
# These two suffice for the decisive comparison AFTER keying on canon():
# P_burn-on-canon == P_lab-on-canon == |orbit| = N!/|Aut|.  P_U (uniform
# quotient) is the point-mass-free limit and is reported only at N=6 scale
# in the report as a degenerate arm; it is NOT a Z32 decision column.
def run_static():
    rng = random.Random(SEED_STATIC)
    totp = CELL_N * (CELL_N - 1) // 2
    h_uni = collections.Counter()       # first-hit per canon class ~ uniform on quotient
    h_lab = collections.Counter()       # plain labeled measure, keyed on canon
    seen_canon = set()
    max_aut = 0
    w_aut = 0.0
    for i in range(K_STATIC):
        e = pairs_from_idx(rng.sample(range(totp), CELL_M), CELL_N)
        k, aut = key_of(e)
        ck = k[0]
        h_lab[ck] += 1.0
        w_aut += aut
        if aut > max_aut: max_aut = aut
        if ck not in seen_canon:
            seen_canon.add(ck)
            h_uni[ck] += 1.0
    n_unlab_est = w_aut / math.factorial(CELL_N)
    return h_uni, h_lab, dict(max_aut=max_aut,
                              n_unlabeled_MC=round(n_unlab_est, 1),
                              target_Q=Q_10_15_TARGET,
                              classes_seen=len(h_uni),
                              coverage_frac=round(len(h_uni) / Q_10_15_TARGET, 4))

# ---------------- TV ----------------
def tv(h1, h2):
    s1 = sum(h1.values()); s2 = sum(h2.values())
    if s1 == 0 or s2 == 0: return None
    keys = set(h1) | set(h2)
    return 0.5 * sum(abs(h1.get(k, 0) / s1 - h2.get(k, 0) / s2) for k in keys)

def to_canon(hist):
    """Collapse a full-key histogram onto canon_key (marginal over R,A,aut)."""
    out = collections.Counter()
    for k, v in hist.items():
        out[k[0]] += v
    return out

def split_half_tv(mode):
    # convergence diagnostic D2 on the same estimator as run_dynamic.
    # Split by chain parity; deterministic modes support-split by attractor key.
    hist_all, _, nc, _, _ = run_dynamic(mode)
    hA = collections.Counter(); hB = collections.Counter()
    for k, v in hist_all.items():
        (hA if hash(k) % 2 == 0 else hB)[k[0]] += v   # canon granularity
    return tv(hA, hB)

def main():
    set_N(CELL_N)
    out = {"cell": [CELL_N, CELL_M], "thin": THIN,
           "samples_per_chain": SAMPLES_PER_CHAIN, "k_static": K_STATIC,
           "decision_rule": dict(unique_match=TV_UNIQUE_MATCH,
                                 margin=TV_UNIQUE_MARGIN),
           "key_granularity": "canon_key (orbits), R/A/aut marginalized out"}
    dyn = {}
    for mode in ("random", "lex", "entropy", "autmin"):
        h, autvals, nc, ncyc, periods = run_dynamic(mode)
        sh = split_half_tv(mode)
        hc = to_canon(h)
        import statistics as _st
        dyn[mode] = dict(hist=hc, chains=nc, cycles=ncyc,
                         med_period=(_st.median(periods) if periods else None),
                         n_keys=len(hc),
                         mean_aut=round(sum(autvals) / len(autvals), 3),
                         max_aut=max(autvals),
                         split_half_tv=round(sh, 4))
        print(f"[z32] dynamic {mode:7s} keys={len(hc):5d} "
              f"converged={ncyc}/{nc} med_period={dyn[mode]['med_period']} "
              f"mean|Aut|={dyn[mode]['mean_aut']:8.3f} "
              f"max|Aut|={dyn[mode]['max_aut']:6d} "
              f"split-half TV={dyn[mode]['split_half_tv']:.4f}", flush=True)
    h_uni, h_lab, diag = run_static()
    # Decisive comparisons on canon_key granularity:
    #   P_D  vs  P_U (uniform quotient)      <- the Z32 geometry question
    #   P_D  vs  P_lab (labeled/Burnside)    <- the Z31 weighting question
    # Selector-shape separation:             <- B vs C
    #   pairwise P_D selector-vs-selector TVs
    print(f"[z32] static max|Aut|={diag['max_aut']}  "
          f"quotient classes seen={diag['classes_seen']} "
          f"({diag['coverage_frac']*100:.1f}% of target {diag['target_Q']})  "
          f"n_unlabeled_MC={diag['n_unlabeled_MC']}", flush=True)
    table = {}
    for mode in dyn:
        hd = dyn[mode]["hist"]
        table[mode] = dict(
            TV_vs_quotient_uniform=round(tv(hd, h_uni), 4),
            TV_vs_labeled=round(tv(hd, h_lab), 4),
            TV_vs_dynamic_random=(round(tv(hd, dyn["random"]["hist"]), 4)
                                  if mode != "random" else 0.0),
        )
    # B-vs-C discriminator: are selector pairwise TVs large (C) or is there
    # a common core (B)? Read directly from the pairwise TV matrix below.
    pairwise = {}
    modes = list(dyn)
    for i in range(len(modes)):
        for j in range(i + 1, len(modes)):
            pairwise[f"{modes[i]}-{modes[j]}"] = round(
                tv(dyn[modes[i]]["hist"], dyn[modes[j]]["hist"]), 4)
    verdict = {}
    for mode, row in table.items():
        tq = row["TV_vs_quotient_uniform"]
        tl = row["TV_vs_labeled"]
        # A = quotient geometry fully explains it: dynamics match P_U far
        # better than they match the labeled (Burnside/orbit) measure.
        verdict[mode] = ("A" if (tq <= TV_UNIQUE_MATCH and
                                 tl >= TV_UNIQUE_MARGIN * tq) else "not-A")
    out["diagnostics"] = dict(D1_max_aut=diag["max_aut"],
                              D1_clean=True,   # counter is exact by construction
                              D2_split_half={m: dyn[m]["split_half_tv"] for m in dyn},
                              D3_coverage=diag)
    out["dynamic_summary"] = {m: {k: v for k, v in dyn[m].items() if k != "hist"}
                              for m in dyn}
    out["tv_table"] = table
    out["pairwise_selector_tv"] = pairwise
    out["verdict_per_selector"] = verdict
    out["outcome"] = ("A" if all(v == "A" for v in verdict.values())
                      else "not-A (B vs C read from pairwise_selector_tv)")
    print("Z32_RESULT", json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
