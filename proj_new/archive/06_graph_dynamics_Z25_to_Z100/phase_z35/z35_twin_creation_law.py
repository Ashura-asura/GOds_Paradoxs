"""
Z35 — TWIN CREATION LAW ENGINE
Rule-2 pre-registered (2026-08-02), BEFORE any run:

Goal: Convert Z34's causal mechanism (twin restructuring creates |Aut| jumps)
into a predictive theorem. Answer WHY and WHEN twin classes form.

Hypotheses:
  H1 LOCAL DEGREE CONVERGENCE: twin creation probability is controlled by
    degree equalization. As degree variance decreases, twin probability rises.
    P(twin event) = f(Δdegree distribution, degree multiplicity).
  H2 EXTREMAL TIE GEOMETRY: the real control variable is extremal
    multiplicity tau = (|argmin|, |argmax|). Sparse extremal sets force fewer
    exchange choices and increase neighborhood collisions. Conditioned on tau,
    degree variance adds little information.
  H3 HIDDEN GRAPH STRUCTURE: neither tau nor degree statistics explain twin
    creation. A new invariant is required.

Cell (10,15). Chains: random 150, lex/entropy/autmin 100.
For every transient step (t < tau_cycle) record:
  - degree sequence, degree variance, number of repeated degrees
  - twin classes before/after (class sizes, number of classes, twin pairs)
  - |Aut| before/after
  - R = |argmin degree-sum edges|, A = |argmax degree-sum non-edges|

Definitions:
  TwinGain = twin_pairs_after - twin_pairs_before
             (number of new twin pairs created by the swap; >= 0 always)
  JumpGain = log(|Aut(t+1)| / |Aut(t)|)
  tau = (|R|, |A|)  [the Z30/Z33/Z34 tie-shell label]

Adversarial controls (required, Rule 4):
  1. Random graph baseline: for each graph, generate K random graphs with the
     same degree sequence (configuration model). Compare twin-gain rate.
  2. Degree-preserving rewiring: for each graph, perform K double-edge swaps
     preserving degree sequence. Compare twin-gain rate.
  3. Complement graph test: for each graph, compute complement (M' = C(N,2)-M).
     Check if twin-gain pattern is mirrored or anti-mirrored.
  4. Same tau, different degree variance: within each tau bin, compare twin-gain
     across degree-variance bins.

Decision thresholds (pre-registered):
  Let H_T = H(TwinGain>0) [binary entropy, bits].
  Compute exact mutual informations from empirical histograms:
    I_tau   = I(TwinGain>0 ; tau)
    I_deg   = I(TwinGain>0 ; degree_variance_bin) +
              I(TwinGain>0 ; num_repeated_degrees)
    I_joint = I(TwinGain>0 ; tau, degree_stats)
    I_deg|tau = I_joint - I_tau
    I_tau|deg = I_joint - I_deg

  H2 wins (tie geometry): I_tau >= 2 * I_deg AND I_deg|tau < 0.1 * H_T
  H1 wins (degree convergence): I_deg >= 2 * I_tau AND I_tau|deg < 0.1 * H_T
  H3 wins (hidden): I_tau < 0.05 AND I_deg < 0.05 (bits)
  Else: mixed, report conditional tables.

No fitting. No ML black box. Exact statistics only.
"""
import sys, math, random, json, collections

sys.path.insert(0, r"C:\Users\bisha\Desktop\gods_paradox\phase_z25")
sys.path.insert(0, r"C:\Users\bisha\Desktop\gods_paradox\phase_z32")
sys.path.insert(0, r"C:\Users\bisha\Desktop\gods_paradox\phase_z33")
import z25b_engine_v2 as E
from z32_stationary_vs_burnside import aut_size_exact, pairs_from_idx  # FIX ME
from z33_symmetry_drift import step_mode, tau_of

CELL_N, CELL_M = 10, 15
NCHAINS = {"random": 150, "lex": 100, "entropy": 100, "autmin": 100}
SEED0 = 20260802
CAP = 512
RAND_K = 10           # random graphs per control sample point
REW_K = 20            # rewire swaps per graph
VAR_BINS = ["low", "med", "high"]   # tertile binning of degree variance

# ---- exact twin-class info for a labeled graph g -------------------------
def twin_info(g):
    """Return (class_sizes_sorted, num_classes, num_twin_pairs).
    u,v twins iff for all w not in {u,v}: adj(u,w)=adj(v,w)."""
    n = E.N
    edges = set(g)
    nb = [0] * n
    for a, b in edges:
        nb[a] |= (1 << b)
        nb[b] |= (1 << a)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for u in range(n):
        for v in range(u + 1, n):
            diff = nb[u] ^ nb[v]
            if diff & ~((1 << u) | (1 << v)) == 0:
                union(u, v)
    classes = collections.Counter(find(u) for u in range(n))
    sizes = sorted(classes.values())
    twin_pairs = sum(c * (c - 1) // 2 for c in sizes)
    return sizes, len(sizes), twin_pairs

# ---- degree statistics ---------------------------------------------------
def degree_stats(g):
    degrees = list(E.degrees(g).values())
    n = len(degrees)
    mean = sum(degrees) / n
    variance = sum((d - mean) ** 2 for d in degrees) / n
    freq = collections.Counter(degrees)
    num_repeated = sum(1 for c in freq.values() if c > 1)
    return variance, num_repeated, degrees

# ---- adversarial control primitives --------------------------------------
ALL_PAIRS = [(a, b) for a in range(CELL_N) for b in range(a + 1, CELL_N)]

def random_graph_same_deg(degrees, rng, max_tries=200):
    """Configuration model: random simple graph with given degree sequence."""
    n = len(degrees)
    target_m = sum(degrees) // 2
    for _ in range(max_tries):
        stubs = []
        for v, d in enumerate(degrees):
            stubs.extend([v] * d)
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i + 1]
            if a == b:
                ok = False; break
            e = (min(a, b), max(a, b))
            if e in edges:
                ok = False; break
            edges.add(e)
        if ok and len(edges) == target_m:
            return frozenset(edges)
    return None

def rewire_degree_preserving(g, rng, n_swaps=REW_K):
    """Double-edge swap preserving degree sequence."""
    edges = set(g)
    edge_list = list(edges)
    for _ in range(n_swaps):
        if len(edge_list) < 2:
            break
        i, j = rng.sample(range(len(edge_list)), 2)
        e1, e2 = edge_list[i], edge_list[j]
        a, b = e1
        c, d = e2
        # two possible rewirings
        cands = []
        for x, y in [(a, c), (a, d), (b, c), (b, d)]:
            if x == y:
                continue
            continue
        # try (a,c),(b,d) swap
        for swap in [((min(a,c),max(a,c)),(min(b,d),max(b,d))),
                     ((min(a,d),max(a,d)),(min(b,c),max(b,c)))]:
            ne1, ne2 = swap
            if ne1 in edges or ne2 in edges:
                continue
            if ne1 == ne2:
                continue
            if e1 == ne1 or e1 == ne2 or e2 == ne1 or e2 == ne2:
                continue
            # valid rewiring
            edges.discard(e1); edges.discard(e2)
            edges.add(ne1); edges.add(ne2)
            edge_list = list(edges)
            break
    return frozenset(edges)

def complement_graph(g):
    s = set(g)
    return frozenset(e for e in ALL_PAIRS if e not in s)

# ---- information theory helpers (exact, histogram-based) -----------------
def bin_entropy(counts):
    n = sum(counts)
    if n == 0: return 0.0
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / n
            h -= p * math.log2(p)
    return h

def mutual_info(joint_counter, x_marg, y_marg, n):
    mi = 0.0
    for (x, y), c in joint_counter.items():
        if c > 0:
            p_xy = c / n
            p_x = x_marg[x] / n
            p_y = y_marg[y] / n
            mi += p_xy * math.log2(p_xy / (p_x * p_y))
    return mi

def conditional_entropy(joint_counter, x_marg, n):
    """H(Y|X) = sum_{x,y} p(x,y) log2 p(x)/p(x,y)"""
    h = 0.0
    for (x, y), c in joint_counter.items():
        if c > 0:
            p_xy = c / n
            p_x = x_marg[x] / n
            h -= p_xy * math.log2(p_x / p_xy)
    return h

def variance_tertile_bins(values):
    """Assign each value to low/med/high based on empirical tertiles."""
    s = sorted(values)
    if len(s) < 3:
        return ["med"] * len(values)
    t1 = s[len(s) // 3]
    t2 = s[2 * len(s) // 3]
    bins = []
    for v in values:
        if v <= t1:
            bins.append("low")
        elif v <= t2:
            bins.append("med")
        else:
            bins.append("high")
    return bins

def set_N(n):
    E.N = n
    E._MEMO.clear(); E._AUT.clear(); E._KC.clear()

def main():
    set_N(CELL_N)
    all_steps = []       # per-step records across all modes
    control_records = [] # sampled adversarial control records
    
    print("[z35] collecting transient steps...", flush=True)
    for mode in ("random", "lex", "entropy", "autmin"):
        for s in range(NCHAINS[mode]):
            rng = random.Random(SEED0 + 131 * s + 991 * len(mode))
            totp = CELL_N * (CELL_N - 1) // 2
            e = pairs_from_idx(rng.sample(range(totp), CELL_M), CELL_N)
            seen = {E.canon(e)}
            states = [(e, 0)]  # (graph, t)
            for t in range(1, CAP):
                e = step_mode(e, mode, rng)
                c = E.canon(e)
                if c in seen:
                    break
                seen.add(c)
                states.append((e, t))
            if len(states) < 3:
                continue
            # record per-step data
            for i in range(len(states) - 1):
                g0, t0 = states[i]
                g1, t1 = states[i + 1]
                a0 = aut_size_exact(g0)
                a1 = aut_size_exact(g1)
                sizes0, nc0, tp0 = twin_info(g0)
                sizes1, nc1, tp1 = twin_info(g1)
                deg_var, num_rep, degrees = degree_stats(g0)
                R, A = tau_of(g0)
                
                all_steps.append({
                    "mode": mode, "chain": s, "t": t0,
                    "aut_before": a0, "aut_after": a1,
                    "jump_gain": math.log(a1 / a0) if a0 > 0 else float('inf'),
                    "twin_pairs_before": tp0,
                    "twin_pairs_after": tp1,
                    "twin_gain": tp1 - tp0,
                    "twin_gain_bool": (tp1 > tp0),
                    "twin_class_sizes_before": sizes0,
                    "twin_class_sizes_after": sizes1,
                    "num_classes_before": nc0,
                    "num_classes_after": nc1,
                    "tau_R": R, "tau_A": A,
                    "degree_variance": deg_var,
                    "num_repeated_degrees": num_rep,
                    "degrees": degrees,
                })
                
                # adversarial controls on sampled subset
                if (t0 % 3 == 0) or mode == "random":
                    # 1. Random graph baseline
                    null_gains = []
                    for _ in range(RAND_K):
                        gr = random_graph_same_deg(degrees, random.Random(SEED0 + 50*s + t0 + len(mode)*1000))
                        if gr is not None:
                            _, _, tp_r = twin_info(gr)
                            null_gains.append(tp_r - tp0)
                    if null_gains:
                        control_records.append({
                            "type": "random_baseline",
                            "twin_gain_mean": sum(null_gains) / len(null_gains),
                            "twin_gain_frac_pos": sum(1 for x in null_gains if x > 0) / len(null_gains),
                            "twin_gain_bool": any(x > 0 for x in null_gains),
                        })
                    
                    # 2. Degree-preserving rewiring
                    rewire_gains = []
                    for k in range(REW_K):
                        gr = rewire_degree_preserving(g0, random.Random(SEED0 + 70*s + k + t0*3 + len(mode)*2000))
                        _, _, tp_r = twin_info(gr)
                        # also need twin_info of "rewired g1" to get a gain...
                        # Actually, compute twin_pairs on the rewired version of g0
                        rewire_gains.append(tp_r)
                    if rewire_gains:
                        # mean twin_pairs on rewired graphs with same degrees as g0
                        control_records.append({
                            "type": "rewiring_null_twinpairs",
                            "mean_twin_pairs": sum(rewire_gains) / len(rewire_gains),
                            "observed_twin_pairs": tp0,
                        })
                    
                    # 3. Complement graph
                    gc0 = complement_graph(g0)
                    gc1 = complement_graph(g1)
                    _, _, tp_c0 = twin_info(gc0)
                    _, _, tp_c1 = twin_info(gc1)
                    control_records.append({
                        "type": "complement",
                        "twin_gain_complement": tp_c1 - tp_c0,
                        "observed_twin_gain": tp1 - tp0,
                    })
    
    total = len(all_steps)
    n_jump = sum(1 for r in all_steps if r["twin_gain_bool"])
    print(f"[z35] {total} transient steps collected, {n_jump} with TwinGain>0", flush=True)
    
    # ---- compute binning for degree variance ----
    all_vars = [r["degree_variance"] for r in all_steps]
    var_bins = variance_tertile_bins(all_vars)
    for r, vb in zip(all_steps, var_bins):
        r["var_bin"] = vb
    
    # ---- mutual information analysis ----
    tg = [r["twin_gain_bool"] for r in all_steps]
    tau_vals = [(r["tau_R"], r["tau_A"]) for r in all_steps]
    deg_var_vals = [r["var_bin"] for r in all_steps]
    num_rep_vals = [r["num_repeated_degrees"] for r in all_steps]
    
    n = len(all_steps)
    H_T = bin_entropy([sum(tg), n - sum(tg)])
    
    # I(TwinGain>0 ; tau)
    joint_tau = collections.Counter(zip(tg, tau_vals))
    x_marg_tau = collections.Counter(tg)
    y_marg_tau = collections.Counter(tau_vals)
    I_tau = mutual_info(joint_tau, x_marg_tau, y_marg_tau, n)
    
    # I(TwinGain>0 ; degree_variance_bin)
    joint_var = collections.Counter(zip(tg, deg_var_vals))
    y_marg_var = collections.Counter(deg_var_vals)
    I_var = mutual_info(joint_var, x_marg_tau, y_marg_var, n)
    
    # I(TwinGain>0 ; num_repeated_degrees)
    joint_rep = collections.Counter(zip(tg, num_rep_vals))
    y_marg_rep = collections.Counter(num_rep_vals)
    I_rep = mutual_info(joint_rep, x_marg_tau, y_marg_rep, n)
    
    I_deg = I_var + I_rep
    
    # I(TwinGain>0 ; tau, degree_stats) [joint]
    joint_joint = collections.Counter(zip(zip(tg, tau_vals), zip(deg_var_vals, num_rep_vals)))
    # Actually, need joint over all three: (tg, tau, var_bin, num_rep)
    # I(X ; Y1, Y2) where X=tg, Y=(tau, var_bin, num_rep)
    xy_counter = collections.Counter()
    x_counter = collections.Counter()
    y_counter = collections.Counter()
    for i in range(n):
        x = tg[i]
        y = (tau_vals[i], deg_var_vals[i], num_rep_vals[i])
        xy_counter[(x, y)] += 1
        x_counter[x] += 1
        y_counter[y] += 1
    I_joint = mutual_info(xy_counter, x_counter, y_counter, n)
    
    I_deg_given_tau = I_joint - I_tau
    I_tau_given_deg = I_joint - I_deg
    
    print(f"[z35] H(TwinGain>0) = {H_T:.4f} bits", flush=True)
    print("[z35] I_tau        = {:.4f} bits".format(I_tau), flush=True)
    print("[z35] I_var        = {:.4f} bits".format(I_var), flush=True)
    print("[z35] I_rep        = {:.4f} bits".format(I_rep), flush=True)
    print("[z35] I_deg(total) = {:.4f} bits".format(I_deg), flush=True)
    print("[z35] I_joint      = {:.4f} bits".format(I_joint), flush=True)
    print("[z35] I_deg|tau    = {:.4f} bits".format(I_deg_given_tau), flush=True)
    print("[z35] I_tau|deg    = {:.4f} bits".format(I_tau_given_deg), flush=True)
    
    # ---- P(TwinGain>0 | tau) ----
    tau_tg = collections.defaultdict(lambda: collections.Counter())
    for i in range(n):
        tau_tg[tau_vals[i]][tg[i]] += 1
    
    # ---- P(TwinGain>0 | var_bin) ----
    var_tg = collections.defaultdict(lambda: collections.Counter())
    for i in range(n):
        var_tg[deg_var_vals[i]][tg[i]] += 1
    
    # ---- adversarial control summaries ----
    null_records = [r for r in control_records if r["type"] == "random_baseline"]
    comp_records = [r for r in control_records if r["type"] == "complement"]
    
    obs_rate = n_jump / n
    null_rate = sum(r["twin_gain_frac_pos"] for r in null_records) / len(null_records) if null_records else None
    null_mean = sum(r["twin_gain_mean"] for r in null_records) / len(null_records) if null_records else None
    
    comp_gains = [r["twin_gain_complement"] for r in comp_records]
    obs_gains = [r["observed_twin_gain"] for r in comp_records]
    comp_mean = sum(comp_gains) / len(comp_gains) if comp_gains else None
    obs_mean = sum(obs_gains) / len(obs_gains) if obs_gains else None
    
    # ---- same-tau different-variance ----
    # within each tau, compare twin_gain across var bins
    same_tau_diff_var = {}
    for tau_val, counter in tau_tg.items():
        key = f"tau={tau_val}"
        same_tau_diff_var[key] = dict(
            n=counter[True] + counter[False],
            frac_twin_gain=counter[True] / (counter[True] + counter[False]) if (counter[True]+counter[False]) > 0 else 0,
        )
    
    # ---- decision ----
    H2_wins = I_tau >= 2 * I_deg and I_deg_given_tau < 0.1 * H_T
    H1_wins = I_deg >= 2 * I_tau and I_tau_given_deg < 0.1 * H_T
    H3_wins = I_tau < 0.05 and I_deg < 0.05
    
    verdict = "H3 (hidden)" if H3_wins else \
              "H1 (degree convergence)" if H1_wins else \
              "H2 (tie geometry)" if H2_wins else \
              "mixed - see tables"
    
    result = {
        "cell": [CELL_N, CELL_M],
        "n_steps": n,
        "n_jump_twin": n_jump,
        "twin_rate": round(n_jump / n, 4),
        "H_T": round(H_T, 4),
        "I_tau": round(I_tau, 4),
        "I_var": round(I_var, 4),
        "I_rep": round(I_rep, 4),
        "I_deg": round(I_deg, 4),
        "I_joint": round(I_joint, 4),
        "I_deg_given_tau": round(I_deg_given_tau, 4),
        "I_tau_given_deg": round(I_tau_given_deg, 4),
        "H2_wins": H2_wins,
        "H1_wins": H1_wins,
        "H3_wins": H3_wins,
        "verdict": verdict,
        "P_twin_given_tau_top": dict(sorted(
            {str(k): round(v[True]/(v[True]+v[False]),4) for k,v in tau_tg.items()}.items(),
            key=lambda x: -x[1])[:5]),
        "P_twin_given_varebin": {k: round(v[True]/(v[True]+v[False]),4) for k,v in var_tg.items()},
        "control_null_mean_twin_gain": round(null_mean, 4) if null_mean else None,
        "control_null_rate": round(null_rate, 4) if null_rate else None,
        "control_obs_rate": round(obs_rate, 4),
        "complement_mean_twin_gain": round(comp_mean, 4) if comp_mean else None,
        "observed_mean_twin_gain": round(obs_mean, 4) if obs_mean else None,
    }
    print("\nZ35_RESULT", json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
