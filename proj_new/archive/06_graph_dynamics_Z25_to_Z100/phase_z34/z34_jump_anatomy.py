"""
Z34 - JUMP ANATOMY: what creates |Aut| jumps?
Rule-2 pre-registered (2026-08-02), BEFORE any run:

Z33 result to explain: transient |Aut|(t) is a staircase - 58% of steps change
|Aut| by 0, and rare very large upward jumps carry the whole positive mean;
jumps concentrate in sparse-tie (R,A) shells. Z33 could not say WHAT a jump is
structurally. Z34 decomposes each jump.

Pre-registered hypothesis space (fixed before runs):
  H1 TWIN CREATION: jumps coincide with creation/merger of twin classes.
     Definition (twins): u,v are twins iff for all w not in {u,v},
     (u~w) <=> (v~w).  This is an equivalence relation; a class of size c
     contributes >= c! to |Aut|.  Twin factor TF(g) = prod_c |c|!
  H2 COMPONENT CLONING: jumps coincide with the swap producing isomorphic
     connected components (k identical copies contribute k!; with internal
     aut^ k).  Clone factor CF(g) = prod over component-iso-classes of
     (multiplicity)!.
  H3 RICH STRUCTURE: neither TF nor CF explains the jump mass; the jump
     requires a new invariant (recorded as H1/H2 failure, Rule 8).

Measured per transient step (t < tau, same stopping as Z33):
    aut_t, aut_{t+1} (exact counter), twin-class multiset signature,
    component iso-class multiset, R_t, A_t (tie sizes).
Jump set: J = {steps with aut_{t+1}/aut_t >= 4}  (pre-registered threshold;
reason: aut ratio 2-3 can arise from a single twin merger; >=4 requires a
factorial-scale event).

EPIDEMIOLOGY REDESIGN (unit-test finding, recorded per Rule 8 before main run):
a multiplicative coverage test TF*CF vs aut is ill-posed because twins and
isomorphic-singleton-components overlap (star+5iso: true aut = 4!*5! = 2880,
naive TF*CF = 345600). A clean decomposition needs the weighted-reduced-graph
theorem. Rather than run a fragile identity, the experiment uses EVENT
INDICATORS per step:
    E_twin     = twin-class multiset changed (any split/merge/size change)
    E_tmax     = max twin-class size strictly increased
    E_clone    = some component iso-class gained a member (mult+1 somewhere)
    E_cnum     = number of connected components changed
A step may fire several events. The diagnostic quantity per selector is the
event rate ON jump set J vs OFF J (all other transient pairs), plus the
fraction of jump log-mass accompanied by >=1 event.

Additionally recorded: mean (R,A) on J vs non-J (causal gate test from the
original plan - does sparse tie gating imply jumps, or merely correlate?).

Decision (fixed before runs):
  H1 (twins):    rate(E_twin | J) >= 0.5 AND rate(E_twin | J)/rate(E_twin | not-J) >= 3
                 in ALL FOUR selectors (universality; else Z33's no-D reopens).
  H2 (clones):   mirrors on E_clone.
  BOTH coupled:  each >= 0.5 rate on J but joint coverage + ratio pattern shows
                 co-firing dominates (corr(E_twin,E_clone | J) reported).
  H3 (residual): neither event family reaches the gate; fraction of J with
                 NO event is reported as the unexplained residual mass.
"""
import sys, math, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z32")
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z33")
import z25b_engine_v2 as E
from z32_stationary_vs_burnside import aut_size_exact, pairs_from_idx
from z33_symmetry_drift import step_mode, tau_of

CELL_N, CELL_M = 10, 15
JUMP_RATIO = 4.0
NCHAINS = {"random": 150, "lex": 100, "entropy": 100, "autmin": 100}
SEED0 = 20260802
CAP = 512
RATE_GATE, RATE_RATIO = 0.5, 3.0

def set_N(n):
    E.N = n
    E._MEMO.clear(); E._AUT.clear(); E._KC.clear()

# ---- twin factor -----------------------------------------------------------
def twin_factor(g):
    """TF(g) = prod_c c! over twin classes.  u,v twins iff for all w not in
    {u,v}: adj(u,w) == adj(v,w).  Equivalence via union-find (transitive:
    u~v, v~w twins => u~w twins on every vertex outside {u,v,w})."""
    n = E.N
    edges = set(g)
    nb = [0] * n
    for a, b in edges:
        nb[a] |= (1 << b); nb[b] |= (1 << a)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for u in range(n):
        for v in range(u + 1, n):
            diff = nb[u] ^ nb[v]
            if diff & ~((1 << u) | (1 << v)) == 0:
                union(u, v)
    classes = collections.defaultdict(int)
    for u in range(n):
        classes[find(u)] += 1
    tf = 1
    maxc = 1
    for c in classes.values():
        f = 1
        for k in range(2, c + 1): f *= k
        tf *= f
        maxc = max(maxc, c)
    return tf, maxc

# ---- components ------------------------------------------------------------
def components(g):
    """List of (canon_key, size, relabeled_sub_edgeset) per component."""
    n = E.N
    edges = set(g)
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    seen = [False] * n
    out = []
    for s in range(n):
        if seen[s]:
            continue
        stack = [s]; seen[s] = True; verts = []
        while stack:
            x = stack.pop(); verts.append(x)
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True; stack.append(y)
        verts.sort()
        lab = {v: i for i, v in enumerate(verts)}
        sub = frozenset((lab[a], lab[b]) for a, b in edges
                        if a in lab and b in lab)
        out.append((E.canon(sub), len(verts), sub))
    return out

EVENT_NOTE = (
    "Epistemic redesign after unit-test: twins and isomorphic-singleton-"
    "components DOUBLE-COUNT |Aut| mass (e.g. star+5iso true aut 2880 = "
    "4!*5!, naive TF*CF_full = 345600 overshoots by 120). Root cause: two "
    "isolated vertices are simultaneously a twin class and a cloned "
    "component. A clean multiplicative decomposition requires the weighted-"
    "reduced-graph theorem (TF(g)*|Aut|(twin-quotient)); rather than stack a "
    "second fragile identity, the experiment switches to EVENT indicators: "
    "for each jump step, record booleans [twin-class count changed], [max "
    "twin-class size grew], [a component iso-class gained a member], "
    "[component-internal aut changed where computable].  Verdict reads event "
    "co-occurrence frequencies conditioned on J vs non-J, not multiplicative "
    "coverage. Thresholds adapted: H1 = twin-event rate on J is >= 3x the "
    "rate off J AND covers >= 0.5 of J; H2 mirror; H3 = neither gate opens."
)

def events(g0, g1):
    """Event indicators between consecutive labeled states."""
    t0 = collections.Counter()
    t0max = 0
    # twin signature multiset via the union-find classes
    def twin_class_sizes(g):
        n = E.N
        edges = set(g)
        nb = [0] * n
        for a, b in edges:
            nb[a] |= (1 << b); nb[b] |= (1 << a)
        parent = list(range(n))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for u in range(n):
            for v in range(u + 1, n):
                diff = nb[u] ^ nb[v]
                if diff & ~((1 << u) | (1 << v)) == 0:
                    if find(u) != find(v):
                        parent[find(u)] = find(v)
        cnt = collections.Counter(find(u) for u in range(n))
        return sorted(cnt.values())
    s0, s1 = twin_class_sizes(g0), twin_class_sizes(g1)
    ev_twin_grew = (max(s1) > max(s0))
    ev_twin_count_changed = (len(s1) != len(s0))
    ev_tf_changed = ev_twin_grew or ev_twin_count_changed
    c0 = collections.Counter(ck for ck, _, _ in components(g0))
    c1 = collections.Counter(ck for ck, _, _ in components(g1))
    ev_clone_gained = any(c1[k] > c0.get(k, 0) for k in c1)
    ev_comp_count_changed = (sum(c1.values()) != sum(c0.values()))
    return dict(twin_grew=ev_twin_grew,
                twin_class_set_changed=ev_tf_changed,
                clone_gained=ev_clone_gained,
                comp_count_changed=ev_comp_count_changed)

def main():
    set_N(CELL_N)
    out = {"cell": [CELL_N, CELL_M], "jump_ratio": JUMP_RATIO,
           "thresholds": {"twin_event_rate_on_J": RATE_GATE,
                          "twin_event_rate_ratio": RATE_RATIO,
                          "clone_event_rate_on_J": RATE_GATE,
                          "clone_event_rate_ratio": RATE_RATIO,
                          "joint_coverage_joint": 0.9},
           "note": "event-indicator design; multiplicative coverage abandoned "
                   "(unit-test showed TF*CF double-counts singleton components)"}
    per_mode = {}
    for mode in ("random", "lex", "entropy", "autmin"):
        jump_rows = []
        nonjump_events = []
        total_pairs = 0
        n_sparse_J = 0
        n_nonj_sparse = 0
        nonjump_R = []; nonjump_A = []
        for s in range(NCHAINS[mode]):
            rng = random.Random(SEED0 + 131 * s + 991 * len(mode))
            totp = CELL_N * (CELL_N - 1) // 2
            e = pairs_from_idx(rng.sample(range(totp), CELL_M), CELL_N)
            seen = {E.canon(e)}
            states = [e]
            tau = None
            for t in range(1, CAP):
                e = step_mode(e, mode, rng)
                c = E.canon(e)
                if c in seen:
                    tau = t; break
                seen.add(c); states.append(e)
            if tau is None:
                continue
            for i in range(len(states) - 1):
                g0, g1 = states[i], states[i + 1]
                a0 = aut_size_exact(g0); a1 = aut_size_exact(g1)
                R, A = tau_of(g0)
                total_pairs += 1
                is_jump = (a1 >= JUMP_RATIO * a0)
                ev = events(g0, g1)
                if is_jump:
                    jump_rows.append(dict(a0=a0, a1=a1, R=R, A=A, **ev))
                    if R <= 2 or A <= 2:
                        n_sparse_J += 1
                else:
                    nonjump_events.append(ev)
                    nonjump_R.append(R); nonjump_A.append(A)
                    if R <= 2 or A <= 2:
                        n_nonj_sparse += 1
        nJ = len(jump_rows)
        n_nonj = len(nonjump_events)
        def ev_rate(ev_name, rows):
            if not rows:
                return None
            return sum(1 for r in rows if r.get(ev_name, False)) / len(rows)
        rate_twin_J = ev_rate("twin_class_set_changed", jump_rows)
        rate_twin_N = ev_rate("twin_class_set_changed", nonjump_events)
        rate_clone_J = ev_rate("clone_gained", jump_rows)
        rate_clone_N = ev_rate("clone_gained", nonjump_events)
        ratio_twin = (rate_twin_J / rate_twin_N) if (rate_twin_N not in (None, 0)) else None
        ratio_clone = (rate_clone_J / rate_clone_N) if (rate_clone_N not in (None, 0)) else None
        cofire = sum(1 for r in jump_rows if r["twin_class_set_changed"] and r["clone_gained"])
        joint_cov = cofire / nJ if nJ else None
        mean_RA_J = (round(sum(r["R"] for r in jump_rows) / nJ, 3),
                     round(sum(r["A"] for r in jump_rows) / nJ, 3)) if nJ else None
        mean_RA_N = (round(sum(nonjump_R) / len(nonjump_R), 3),
                     round(sum(nonjump_A) / len(nonjump_A), 3)) if nonjump_R else None
        frac_sparse_N = (n_nonj_sparse / n_nonj) if n_nonj else None
        per_mode[mode] = dict(
            n_jump=nJ, n_nonjump=n_nonj,
            jump_rate_per_pair=round(nJ / total_pairs, 5) if total_pairs else None,
            rate_twin_on_J=round(rate_twin_J, 4) if rate_twin_J is not None else None,
            rate_twin_off_J=round(rate_twin_N, 4) if rate_twin_N is not None else None,
            ratio_twin_rate=round(ratio_twin, 3) if ratio_twin is not None else None,
            rate_clone_on_J=round(rate_clone_J, 4) if rate_clone_J is not None else None,
            rate_clone_off_J=round(rate_clone_N, 4) if rate_clone_N is not None else None,
            ratio_clone_rate=round(ratio_clone, 3) if ratio_clone is not None else None,
            cofire_J=round(joint_cov, 4) if joint_cov is not None else None,
            mean_RA_on_J=mean_RA_J,
            mean_RA_off_J=mean_RA_N,
            frac_J_sparse=(round(n_sparse_J / nJ, 4) if nJ else None),
            frac_nonJ_sparse=(round(frac_sparse_N, 4) if frac_sparse_N is not None else None),
        )
        print(f"[z34] {mode:7s} jumps={nJ}/{total_pairs} "
              f"twin(J)={per_mode[mode]['rate_twin_on_J']} "
              f"ratio={per_mode[mode]['ratio_twin_rate']} "
              f"clone(J)={per_mode[mode]['rate_clone_on_J']} "
              f"ratio={per_mode[mode]['ratio_clone_rate']} "
              f"cofire={per_mode[mode]['cofire_J']} "
              f"RA(J)={mean_RA_J} RA(nonJ)={mean_RA_N} "
              f"sparseJ={per_mode[mode]['frac_J_sparse']} "
              f"sparseNonJ={per_mode[mode]['frac_nonJ_sparse']}", flush=True)
    out["per_mode"] = per_mode
    # verdict (pre-registered thresholds)
    verdict = {}
    for mode, d in per_mode.items():
        rtj = d["rate_twin_on_J"]; rto = d["rate_twin_off_J"]; rt = d["ratio_twin_rate"]
        rcj = d["rate_clone_on_J"]; rco = d["rate_clone_off_J"]; rc = d["ratio_clone_rate"]
        if d["n_jump"] == 0:
            verdict[mode] = "no jumps observed"
        elif rtj is not None and rtj >= RATE_GATE and (rt or 0) >= RATE_RATIO and \
             (rcj is None or rcj < RATE_GATE or (rc or 0) < RATE_RATIO):
            verdict[mode] = "H1 (twins)"
        elif rcj is not None and rcj >= RATE_GATE and (rc or 0) >= RATE_RATIO and \
             (rtj is None or rtj < RATE_GATE or (rt or 0) < RATE_RATIO):
            verdict[mode] = "H2 (clones)"
        elif rtj is not None and rcj is not None and rtj >= RATE_GATE and rcj >= RATE_GATE and \
             (rt or 0) >= RATE_RATIO and (rc or 0) >= RATE_RATIO:
            verdict[mode] = "H1+H2 coupled"
        elif (rtj or 0) < RATE_GATE and (rcj or 0) < RATE_GATE:
            verdict[mode] = "H3 (residual unexplained)"
        else:
            verdict[mode] = "mixed - see rates"
    out["verdict"] = verdict
    print("Z34_RESULT", json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
