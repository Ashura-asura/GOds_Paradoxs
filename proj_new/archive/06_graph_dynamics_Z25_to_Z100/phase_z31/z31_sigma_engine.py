"""
Z31 - TIE-SHELL LAW ENGINE: sigma(N,M) as a property of state space itself.

PHASE 1 - full quotient measurement (no dynamics, no selector):
  Burnside weighting. For f on unlabeled graphs:
    sum_{[g]} f([g]) = sum_{labeled g} f(g) / |Aut(g)| / N! * N! ??? careful:
  Orbit-stabilizer: |orbit of g| = N! / |Aut(g)|. Each unlabeled class
  [g] contains N!/|Aut| labeled copies, so
    sum_{[g]} f([g]) = sum_{labeled g} f(g) * |Aut(g)| / N!.
  With UNIFORM labeled sampling:
    E_lab[ f * |Aut| ] = (1/|G_NM|) sum_lab f |Aut|
                       = N! / |G_NM| * sum_[g] f([g])
    E_lab[ |Aut| ]     = N! / |G_NM| * |Q_NM|
  =>  sigma-unweighted-on-quotient histogram  =  E_lab[ f*|Aut| ]/E_lab[|Aut|].
  N=6: exhaustive enumeration (all 2^15 labeled graphs partitioned by M).
  N=7,8,10,12: uniform labeled Monte-Carlo, weights |Aut|.

  For each graph: rem-extremum size |R| (argmin degree-sum edges),
                  add-extremum size |A| (argmax degree-sum nonedges).

PHASE 2 - scaling: cells (N, M) with rho = 2M/(N(N-1)) in {0.3, 0.5};
  compare sigma shapes across N at fixed rho.

PHASE 3 - shell prediction WITHOUT dynamics: for ER-like G(N,M),
  edge degree-sums d_a+d_b ~ approx N(2m_bar, s^2) with
  m_bar = 2M(N-1)/C(N,2)... we use plug-in normal approx:
    E|R| ~ M * P(S = Smin) via extreme-value of M iid normals at the min,
    E|A| ~ (C(N,2)-M) * P(S = Smax) over nonedges.
  Implemented as a simple 1-D normal/order-statistic estimator; compared
  to measured means as ratio predicted/observed.

PHASE 4 - dynamic verification at (10,15), random selector: distance
  D_sigma(G_t) = 0 if (|R|,|A|) in support(sigma_(10,15) measured) else 1
  (support indicator: tau seen with weighted freq > 0.5% of mass).
  Report mean D_sigma over t = 0..40 averaged over 60 runs.

PHASE 5 - selector removal: attractor tau-distributions for selectors
  {lex, random, entropy, autmin} at (10,15), 120 runs each; pairwise
  total-variation distance of the tau histograms.
"""
import sys, math, random, json, collections, itertools
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

def set_N(n):
    E.N = n
    E._MEMO.clear(); E._AUT.clear(); E._KC.clear()

def tau_of(e, p=0.0):
    N = E.N
    d = E.degrees(e)
    ed = set(e)
    nonedge = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    sc_r = min(ds(x) for x in ed)
    sc_a = max(ds(x) for x in nonedge)
    R = sum(1 for x in ed if ds(x) == sc_r)
    A = sum(1 for x in nonedge if ds(x) == sc_a)
    return R, A

# ---------------- Phase 1 ----------------
def exact_N6():
    N = 6
    set_N(N)
    pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]
    hist = collections.defaultdict(lambda: collections.defaultdict(float))
    wnorm = collections.defaultdict(float)
    for mask in range(1 << 15):
        e = frozenset(pairs[i] for i in range(15) if mask >> i & 1)
        M = len(e)
        if M == 0 or M == 15:
            continue
        aut = E.aut_size(e)
        R, A = tau_of(e)
        hist[M][(R, A)] += aut
        wnorm[M] += aut
    out = {}
    for M in sorted(hist):
        tot = wnorm[M]
        n_unlab = tot / 720.0     # sum |Aut| over labeled / 6! = #unlabeled
        out[M] = dict(n_unlabeled_check=round(n_unlab, 2),
                      top=[(str(k), round(v / tot, 4))
                           for k, v in sorted(hist[M].items(),
                                              key=lambda kv: -kv[1])[:6]])
    return out

def sample_sigma(N, M, K, seedbase=1):
    set_N(N)
    tot_pairs = N * (N - 1) // 2
    rng = random.Random(seedbase + 1000 * N + 37 * M)
    hist = collections.defaultdict(float)
    wsum = 0.0
    for _ in range(K):
        idx = rng.sample(range(tot_pairs), M)
        e = frozenset((a, b) for i in idx
                      for a in [divmod_inv(i, N)] for b in [0])  # placeholder
        # proper index->pair map:
        e = pairs_from_idx(idx, N)
        aut = E.aut_size(e)
        R, A = tau_of(e)
        hist[(R, A)] += aut
        wsum += aut
    return hist, wsum

PAIR_CACHE = {}
def pairs_from_idx(idx, N):
    if N not in PAIR_CACHE:
        PAIR_CACHE[N] = [(a, b) for a in range(N) for b in range(a + 1, N)]
    return frozenset(PAIR_CACHE[N][i] for i in idx)

def divmod_inv(i, N):
    return 0

p1 = {}
p1["N6_exact"] = exact_N6()
cells = [(7, 6), (8, 8), (10, 13), (12, 20),     # rho ~ 0.30
         (7, 11), (8, 14), (10, 22), (12, 33)]   # rho ~ 0.50 (ish)
for N, M in cells:
    hist, wsum = sample_sigma(N, M, 400)
    top = sorted(hist.items(), key=lambda kv: -kv[1])[:6]
    meanR = sum(k[0] * v for k, v in hist.items()) / wsum
    meanA = sum(k[1] * v for k, v in hist.items()) / wsum
    support = len(hist)
    p1[f"N{N}_M{M}_rho{round(2*M/(N*(N-1)),2)}"] = dict(
        n_tau=support, mean_R=round(meanR, 3), mean_A=round(meanA, 3),
        top=[(str(k), round(v / wsum, 4)) for k, v in top])
print("PHASE1", json.dumps(p1, indent=2))

# ---------------- Phase 3 (predict without dynamics) ----------------
def predict_RA(N, M):
    """Normal-approx extreme-count estimator."""
    tot = N * (N - 1) // 2
    # degree-sum of an edge: d_a+d_b; d_i ~ Bin(N-1, rho) approx, edges
    # share -> use mean mu_s = 2 * (N-1) * rho, var s2 = 2 * (N-1) * rho*(1-rho)
    rho = M / tot
    mu = 2 * (N - 1) * rho
    s2 = 2 * (N - 1) * rho * (1 - rho) + 2 * rho * (1 - rho)  # + shared term cov~rho(1-rho)*2
    sd = math.sqrt(max(s2, 1e-9))
    # expected count at min among M ~ M * P(one at min)  ~ exp tail:
    # approx minimum gap ~ sd * sqrt(2 ln M); count within 0.5 of min
    import math as mth
    def n_extreme(cnt, sign):
        z = sign * mth.sqrt(2 * mth.log(max(cnt, 2)))
        # P(X within 0.5 of mu + z*sd) ~ phi(z)/ (sd) ~ crude count
        val = cnt * mth.exp(-0.5 * z * z) / (mth.sqrt(2 * mth.pi) )
        return max(val, 1.0)
    return n_extreme(M, -1), n_extreme(tot - M, +1)

p3 = {}
for N, M in cells + [(6, 5), (6, 8)]:
    pr, pa = predict_RA(N, M)
    set_N(N)
    hist, wsum = sample_sigma(N, M, 300, seedbase=77)
    mr = sum(k[0] * v for k, v in hist.items()) / wsum
    ma = sum(k[1] * v for k, v in hist.items()) / wsum
    p3[f"{N},{M}"] = dict(pred_R=round(pr, 2), obs_R=round(mr, 2),
                          ratio_R=round(pr / mr, 3) if mr else None,
                          pred_A=round(pa, 2), obs_A=round(ma, 2),
                          ratio_A=round(pa / ma, 3) if ma else None)
print("PHASE3", json.dumps(p3, indent=2))

# ---------------- Phase 4: distance-to-shell ----------------
set_N(10)
hist1015, w1015 = sample_sigma(10, 15, 600, seedbase=5)
supp = {k for k, v in hist1015.items() if v / w1015 > 0.005}

def rand_step(e, rng):
    Nloc = 10
    d = E.degrees(e); ed = set(e)
    nonedge = [(a, b) for a in range(Nloc) for b in range(a + 1, Nloc) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    sc_r = min(ds(x) for x in ed); sc_a = max(ds(x) for x in nonedge)
    R = [x for x in ed if ds(x) == sc_r]
    A = [x for x in nonedge if ds(x) == sc_a]
    r, a = rng.choice(R), rng.choice(A)
    g = set(ed); g.discard(r); g.add(a)
    return frozenset(g)

D = []
T = 40
runs = 60
for s in range(runs):
    rng = random.Random(9100 + s)
    Nloc = 10; totp = 45
    idx = rng.sample(range(totp), 15)
    e = pairs_from_idx(idx, Nloc)
    for t in range(T):
        R, A = tau_of(e)
        D.append(0 if (R, A) in supp else 1)
        e = rand_step(e, rng)
on_shell_frac = 1.0 - sum(D) / len(D)
# time profile
prof = []
for t in range(T):
    c = 0; n = 0
    rng2 = random.Random(31337)
    # regenerate deterministically per t via replay: cheap approach
    for s in range(runs):
        rng = random.Random(9100 + s)
        idx = rng.sample(range(45), 15)
        e = pairs_from_idx(idx, 10)
        for tt in range(t + 1):
            if tt == t:
                R, A = tau_of(e)
                c += 0 if (R, A) in supp else 1
                n += 1
            else:
                e = rand_step(e, rng)
    prof.append(round(1.0 - c / n, 3))
print("PHASE4", json.dumps(dict(shell_support_size=len(supp),
                              onshell_fraction_overall=round(on_shell_frac, 4),
                              onshell_profile_every5=[prof[0], prof[4], prof[9], prof[19], prof[29], prof[39]]),
                        indent=2))

# ---------------- Phase 5: selector removal TV distances ----------------
set_N(10)

def step_mode(e, mode, rng):
    Nloc = 10
    d = E.degrees(e); ed = set(e)
    ne = [(a, b) for a in range(Nloc) for b in range(a + 1, Nloc) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    rem = sorted(ed, key=lambda x: (ds(x), x))
    add = sorted(ne, key=lambda x: (ds(x), x))
    sc_r = ds(rem[0]); sc_a = ds(add[-1])
    R = [x for x in ed if ds(x) == sc_r]
    A = [x for x in ne if ds(x) == sc_a]
    if mode == "lex":
        r, a = rem[0], add[-1]
    elif mode == "random":
        r, a = rng.choice(R), rng.choice(A)
    elif mode == "entropy":
        best = None; bh = -1
        for rr in R:
            for aa in A:
                g = set(ed); g.discard(rr); g.add(aa)
                d2 = E.degrees(g)
                ds2 = lambda x: d2[x[0]] + d2[x[1]]
                ne2 = [(x, y) for x in range(10) for y in range(x + 1, 10) if (x, y) not in g]
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

dist = {}
for mode in ("lex", "random", "entropy", "autmin"):
    h = collections.Counter()
    for s in range(120):
        rng = random.Random(8200 + s)
        idx = rng.sample(range(45), 15)
        e = pairs_from_idx(idx, 10)
        seen = {}
        for t in range(512):
            c = E.canon(e)
            if c in seen:
                R, A = tau_of(e)
                h[(R, A)] += 1
                break
            seen[c] = t
            e = step_mode(e, mode, rng)
    dist[mode] = h

def tv(h1, h2):
    keys = set(h1) | set(h2)
    s1 = sum(h1.values()); s2 = sum(h2.values())
    return 0.5 * sum(abs(h1.get(k, 0) / s1 - h2.get(k, 0) / s2) for k in keys)

modes = list(dist)
tvout = {}
for i in range(len(modes)):
    for j in range(i + 1, len(modes)):
        tvout[f"{modes[i]} vs {modes[j]}"] = round(tv(dist[modes[i]], dist[modes[j]]), 4)
print("PHASE5", json.dumps(dict(tv=tvout,
    supports={m: len(dist[m]) for m in modes}), indent=2))
