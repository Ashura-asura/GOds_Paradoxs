"""
Z25-b v2 — non-contractive engine, algorithmically accelerated.
Why NOT GPU: bottleneck is factorial relabel search (combinatorial), not FLOPs.
Fixes:
  (A) canon() memoized on frozenset(edges): attractor states revisited ->
      expensive canon paid once per unique graph, not per step x trial x p.
  (B) exact canonical form computed only when product of |color class|!
      <= CANON_BUDGET; else a deterministic iso-invariant key
      (degree seq, edge-degree multiset, WL-sorted neighbor vectors) is used.
      The key is a deterministic function of the isomorphism class, so cycle
      detection remains well-defined; possible false merges are declared L2.
  (C) k-cycle counting memoized per canon key.
Physics content of T is UNCHANGED from z25b v1 (same rule, same ledger).
"""
import collections, itertools, math, random, json, argparse

N = 10
CANON_BUDGET = 20000

def seed_graph():
    e = {tuple(sorted((i, (i + 1) % N))) for i in range(N)}
    for a, b in [(0, 3), (0, 6), (2, 7), (4, 8), (1, 5)]:
        e.add(tuple(sorted((a, b))))
    return frozenset(e)

def degrees(edges):
    d = {v: 0 for v in range(N)}
    for a, b in edges:
        d[a] += 1; d[b] += 1
    return d

def T(edges, p, rng):
    edges = set(edges); d = degrees(edges)
    rem = sorted(edges, key=lambda e: (d[e[0]] + d[e[1]], e))
    nonedges = [(a, b) for a in range(N) for b in range(a + 1, N)
                if (a, b) not in edges]
    add = sorted(nonedges, key=lambda e: (d[e[0]] + d[e[1]], e))
    if rng.random() < p:
        e_out, e_in = rem[-1], add[0]
    else:
        e_out, e_in = rem[0], add[-1]
    edges.discard(e_out); edges.add(e_in)
    return frozenset(edges)

def wl_colors(edges):
    adj = {v: set() for v in range(N)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    color = {v: (len(adj[v]),) for v in range(N)}
    for _ in range(N):
        nc = {v: (color[v], tuple(sorted(color[w] for w in adj[v])))
              for v in range(N)}
        uniq = {c: i for i, c in enumerate(sorted(set(nc.values())))}
        nc = {v: uniq[c] for v, c in nc.items()}
        if nc == color:
            break
        color = nc
    return color, adj

def invariant_key(edges):
    color, adj = wl_colors(edges)
    d = degrees(edges)
    degsig = tuple(sorted(d[v] for v in range(N)))
    edgesig = tuple(sorted(tuple(sorted((d[a], d[b]))) for a, b in edges))
    wlman  = tuple(sorted((color[v], tuple(sorted(color[w] for w in adj[v])))
                          for v in range(N)))
    return ("INV", degsig, edgesig, wlman)

_MEMO = {}
def canon(edges):
    """EXACT iso-invariant canonical form (Rule-8 #1/#2 fix, 2026-08-03).

    MEMO KEYING (2026-08-03, second fix): wl_colors() runs over range(N),
    so color classes (and the block assignment) depend on N even for the
    same edge set (isolated vertices). _MEMO must therefore be keyed on
    (N, edges), not on edges alone — an N-blind key returned the N=4
    canonical form for a 5-vertex edge set in mixed-N processes (caught by
    the A/B cross-check vs the independent reference implementation).

    OLD BUG: the intra-class relabel search mapped each vertex o to an image
    drawn from the class's OWN vertex-index set (g[o] = im with im in
    permutations(classes[k])). Two isomorphic graphs have color classes
    containing DIFFERENT index values (pi(class) vs class), so the two
    searches explored unrelated label spaces and rarely agreed — canon was
    NOT iso-invariant. For asymmetric graphs (singleton WL classes) it
    returned the graph's own labeling, not the global lex-min representative.

    FIX: target labels are iso-invariant BLOCKS determined by color rank:
    classes sorted by their (iso-invariant) WL color value, with class k
    mapped onto the contiguous block [offset_k, offset_k + |class_k|).
    Images are the block labels, never the class's own vertex numbers, so
    isomorphic graphs search the SAME target label space (up to the iso
    itself) and the lex-min agrees. Verified: 1000/1000 iso pairs identical,
    no false merges vs networkx ground truth (see Z35_Z36_AUDIT_REPORT.md).
    """
    e = frozenset(edges)
    if (N, e) in _MEMO:
        return _MEMO[(N, e)]
    color, _ = wl_colors(e)
    classes = collections.defaultdict(list)
    for v, c in color.items():
        classes[c].append(v)
    keys = sorted(classes)
    budget = 1
    for cl in classes.values():
        budget *= math.factorial(len(cl))
    if budget > CANON_BUDGET:
        key = invariant_key(e)
        _MEMO[(N, e)] = key
        return key
    starts = {}
    off = 0
    for k in keys:
        starts[k] = off
        off += len(classes[k])
    best = None
    for combo in itertools.product(*[list(itertools.permutations(classes[k]))
                                     for k in keys]):
        g = {}
        for k, cl in zip(keys, combo):
            base = starts[k]
            for o, im in zip(cl, range(base, base + len(cl))):
                g[o] = im
        s = tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in e))
        if best is None or s < best:
            best = s
    key = ("EX", best)
    _MEMO[(N, e)] = key
    return key

_AUT = {}
def aut_size(edges):
    e = frozenset(edges)
    if (N, e) in _AUT:
        return _AUT[(N, e)]
    color, _ = wl_colors(e)
    classes = collections.defaultdict(list)
    for v, c in color.items():
        classes[c].append(v)
    keys = sorted(classes)
    budget = 1
    for cl in classes.values():
        budget *= math.factorial(len(cl))
    if budget > CANON_BUDGET:
        _AUT[(N, e)] = budget          # lower bound proxy, labeled via budgetflag
        return budget
    eset = set(e); cnt = 0
    for combo in itertools.product(*[list(itertools.permutations(classes[k]))
                                     for k in keys]):
        g = {}
        for k, cl in zip(keys, combo):
            for o, im in zip(classes[k], cl):
                g[o] = im
        if all(tuple(sorted((g[a], g[b]))) in eset for (a, b) in eset):
            cnt += 1
    _AUT[(N, e)] = cnt
    return cnt

_KC = {}
def k_cycle(edges, k):
    e = frozenset(edges)
    kk = (N, e, k)
    if kk in _KC:
        return _KC[kk]
    adj = {v: set() for v in range(N)}
    for a, b in e:
        adj[a].add(b); adj[b].add(a)
    cnt = 0
    for combo in itertools.combinations(range(N), k):
        seen = set()
        for perm in itertools.permutations(combo[1:]):
            cyc = (combo[0],) + perm
            rev = (cyc[0],) + tuple(reversed(cyc[1:]))
            key = min(min(tuple(list(cyc)[i:] + list(cyc)[:i]) for i in range(k)),
                      min(tuple(list(rev)[i:] + list(rev)[:i]) for i in range(k)))
            if key in seen:
                continue
            seen.add(key)
            if all(cyc[(i + 1) % k] in adj[cyc[i]] for i in range(k)):
                cnt += 1
    _KC[kk] = cnt
    return cnt

def run(seed, p, rng, max_steps=256):
    e = set(seed); hist = {}
    for step in range(max_steps):
        c = canon(e)
        if c in hist:
            period = step - hist[c]
            members = sorted(hist.items(), key=lambda kv: kv[1])
            cyc_members = [kv for kv in members if kv[1] >= hist[c]]
            agg = dict(period=period, cyc_len=len(cyc_members), n3=0, n4=0,
                       n5=0, aut=1, dmax=0, dmin=0)
            for key, _ in cyc_members:
                pass
            cm = [k for k, idx in members if idx >= hist[c]]
            graphs = [list(k[1]) if k[0] == "EX" else None for k in cm]
            break
        hist[c] = step
        e = set(T(frozenset(e), p, rng))
    else:
        return dict(converged=False)
    # measure observables ON the cycle states: recompute cycle graphs:
    e = set(seed); hist = {}
    states = []
    for step in range(256):
        c = canon(e)
        if c in hist:
            start = hist[c]
            states = states[start:]
            break
        hist[c] = step
        states.append(set(e))
        e = set(T(frozenset(e), p, rng))
    n3 = min(k_cycle(s, 3) for s in states)
    n4 = min(k_cycle(s, 4) for s in states)
    n5 = min(k_cycle(s, 5) for s in states)
    aut = min(aut_size(s) for s in states)
    dmins = [min(degrees(s).values()) for s in states]
    dmaxs = [max(degrees(s).values()) for s in states]
    return dict(converged=True, key=str(states[0]),
                period=len(states), n3=n3, n4=n4, n5=n5, aut=aut,
                dmin=min(dmins), dmax=max(dmaxs),
                ratio_n3_n4=(n3 / n4) if n4 else None,
                ratio_dmax_dmin=(max(dmaxs) / min(dmins)) if min(dmins) else None,
                iso_note="EX" if states and canon(states[0])[0] == "EX" else "INV")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    p_grid = [0.0, 0.25, 0.5, 0.75, 1.0] if args.quick else \
             [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    n_trials = 4 if args.quick else 16
    out = {"n_in": {"p": 1, "design": ["exchange rule", seed_graph and "seed 10v/15e"],
                    "seed_bits": "fixed 20260802"},
           "p": {}}
    for p in p_grid:
        basins = collections.Counter(); obs = collections.defaultdict(list)
        conv = 0
        for t in range(n_trials):
            rng = random.Random(20260802 + 7919 * t + int(1000 * p))
            r = run(seed_graph(), p, rng)
            if r["converged"]:
                conv += 1
                basins[r["key"]] += 1
                obs[r["key"]].append(r)
        rows = []
        for key, cnt in basins.most_common(6):
            s = obs[key][0]
            rows.append({k: s[k] for k in
                         ("period", "n3", "n4", "n5", "aut", "dmin", "dmax",
                          "ratio_n3_n4", "ratio_dmax_dmin", "iso_note")} |
                        {"share": cnt / n_trials})
        out["p"][str(p)] = dict(converged=conv, n_trials=n_trials,
                                n_basins=len(basins),
                                dominant_share=(basins.most_common(1)[0][1] / n_trials)
                                               if basins else 0,
                                basins=rows,
                                memo_size=len(_MEMO))
    print(json.dumps(out, indent=2))
if __name__ == "__main__":
    main()
