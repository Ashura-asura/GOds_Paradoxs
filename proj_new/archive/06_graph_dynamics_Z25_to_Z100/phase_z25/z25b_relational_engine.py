"""
Z25-b relational engine — NON-CONTRACTIVE variant.
Implements the three changes mandated by PHASE_Z25_EXECUTION.md section 5:
  (1) witness/permutation machinery REMOVED; updates are EDGE EXCHANGES
      (non-monotone structure, conserved edge count) -> multiple recurrent
      classes can coexist instead of one rigid global attractor;
  (2) canonicalization runs on the full (witness-free) graph via WL color
      refinement + restricted relabeling search;
  (3) ratio observables are measured WITHIN each attractor, not across
      one-attractor-per-p slices.
Admitted inputs (Rule 9 ledger):
  - scalar p in [0,1]: probability of the "balance" exchange vs "contrast".
  - RNG seed (statistical device only; fixed constant, documented).
  - N=10 vertices, M=15 edges: the seed graph's own content (declared design
    bits, not dynamical inputs).
Rule: remove/add by endpoint degree-sum ordering, tie-broken lexicographically.
Balance mode: remove max degree-sum edge, add min degree-sum nonedge.
Contrast mode: remove min degree-sum edge, add max degree-sum nonedge.
NO energy, NO potential, NO symmetry input; Aut() and ratios are outputs.
"""
import collections, itertools, math, random, json, argparse

N = 10
M_SEED = 15

def seed_graph():
    e = {tuple(sorted((i, (i + 1) % N))) for i in range(N)}
    extra = [(0, 3), (0, 6), (2, 7), (4, 8), (1, 5)]
    for a, b in extra:
        e.add(tuple(sorted((a, b))))
    return frozenset(e)   # exactly 15 edges

def degrees(edges):
    d = {v: 0 for v in range(N)}
    for a, b in edges:
        d[a] += 1; d[b] += 1
    return d

def T(edges, p, rng):
    edges = set(edges)
    d = degrees(edges)
    rem = sorted(edges, key=lambda e: (d[e[0]] + d[e[1]], e))
    nonedges = [(a, b) for a in range(N) for b in range(a + 1, N)
                if (a, b) not in edges]
    add = sorted(nonedges, key=lambda e: (d[e[0]] + d[e[1]], e))
    if rng.random() < p:          # balance
        e_out, e_in = rem[-1], add[0]
    else:                          # contrast
        e_out, e_in = rem[0], add[-1]
    edges.discard(e_out)
    edges.add(e_in)
    return frozenset(edges)

# ----- canonical form: WL refinement then restricted relabel search -----
def wl_colors(edges):
    adj = {v: set() for v in range(N)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    color = {v: (len(adj[v]),) for v in range(N)}
    prev = -1
    for _ in range(N):
        nc = {v: (color[v], tuple(sorted(color[w] for w in adj[v])))
              for v in range(N)}
        uniq = {c: i for i, c in enumerate(sorted(set(nc.values())))}
        nc = {v: uniq[c] for v, c in nc.items()}
        if len(set(nc.values())) == prev:
            color = nc; break
        prev = len(set(color.values()))
        color = nc
    return color

def canon(edges):
    """EXACT iso-invariant canonical form (Rule-8 #1/#2 fix, 2026-08-03).

    Same fix as z25b_engine_v2.canon: images must be iso-invariant target
    blocks (class rank -> contiguous block), NOT the class's own vertex
    indices (old code made isomorphic graphs search different label spaces).
    """
    color = wl_colors(edges)
    classes = collections.defaultdict(list)
    for v, c in color.items():
        classes[c].append(v)
    keys = sorted(classes)
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
        s = tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in edges))
        if best is None or s < best:
            best = s
    return best

def aut_size_lower(edges):
    color = wl_colors(edges)
    classes = collections.defaultdict(list)
    for v, c in color.items():
        classes[c].append(v)
    keys = sorted(classes)
    eset = set(tuple(sorted(e)) for e in edges)
    cnt = 0
    for combo in itertools.product(*[list(itertools.permutations(classes[k]))
                                     for k in keys]):
        g = {}
        for k, cl in zip(keys, combo):
            for o, im in zip(classes[k], cl):
                g[o] = im
        if all(tuple(sorted((g[a], g[b]))) in eset for (a, b) in eset):
            cnt += 1
    return cnt

def k_cycles(edges, k):
    adj = {v: set() for v in range(N)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    cnt = 0
    for combo in itertools.combinations(range(N), k):
        # cyclic arrangements up to dihedral symmetry
        seen = set()
        for perm in itertools.permutations(combo[1:]):
            cyc = (combo[0],) + perm
            rev = (cyc[0],) + tuple(reversed(cyc[1:]))
            key = min(min(tuple(cyc[i:] + cyc[:i]) for i in range(k)),
                      min(tuple(rev[i:] + rev[:i]) for i in range(k)))
            if key in seen:
                continue
            seen.add(key)
            if all(cyc[(i + 1) % k] in adj[cyc[i]] for i in range(k)):
                cnt += 1
    return cnt

def run(seed, p, rng, max_steps=512):
    e = set(seed)
    hist = {}
    for step in range(max_steps):
        c = canon(e)
        if c in hist:
            period = step - hist[c]
            d = degrees(e)
            obs = dict(
                period=period,
                n3=k_cycles(e, 3), n4=k_cycles(e, 4), n5=k_cycles(e, 5),
                aut=aut_size_lower(e),
                dmax=max(d.values()), dmin=min(d.values()),
            )
            obs["ratios"] = {
                "n3/n4": (obs["n3"] / obs["n4"]) if obs["n4"] else None,
                "dmax/dmin": (obs["dmax"] / obs["dmin"]) if obs["dmin"] else None,
            }
            return dict(converged=True, key=str(c), **obs)
        hist[c] = step
        e = set(T(frozenset(e), p, rng))
    return dict(converged=False)

def classify(n_out_ratio_kinds, universal, n_in=1):
    if not universal or n_out_ratio_kinds == 0:
        return "FAILED"
    return "GENERATED" if n_out_ratio_kinds > n_in else "PARTIAL"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    p_grid = [0.0, 0.5, 1.0] if args.quick else [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    n_trials = 6 if args.quick else 16
    out = {"n_in_declared": {"p": 1, "design_bits": ["exchange-rule",
                                                     "seed-graph(N=10,M=15)"],
                                     "rng_seed_bits": "fixed constant 20260802"},
           "p": {}}
    universal_kinds = None
    for p in p_grid:
        basins = collections.Counter()
        obs_by_basin = collections.defaultdict(list)
        for t in range(n_trials):
            rng = random.Random(20260802 + 7919 * t + int(1000 * p))
            r = run(seed_graph(), p, rng)
            if not r["converged"]:
                obs_by_basin["(no attractor)"].append(r)
                continue
            basins[r["key"]] += 1
            obs_by_basin[r["key"]].append(r)
        basin_rows = []
        for key, cnt in basins.most_common(6):
            reps = obs_by_basin[key]
            sample = reps[0]
            basin_rows.append(dict(
                basin_share=cnt / n_trials,
                period=sample["period"],
                n3=sample["n3"], n4=sample["n4"], n5=sample["n5"],
                aut=sample["aut"], dmax=sample["dmax"], dmin=sample["dmin"],
                ratio_n3_n4=sample["ratios"]["n3/n4"],
                ratio_dmax_dmin=sample["ratios"]["dmax/dmin"],
            ))
        out["p"][str(p)] = dict(
            n_basins=len(basins),
            dominant_share=(basins.most_common(1)[0][1] / n_trials) if basins else 0,
            basins=basin_rows,
        )
    # universality: kinds of ratios that are constant within every basin fold
    out["verdict_note"] = ("filled in PHASE_Z25B_EXECUTION.md after reading "
                           "basin tables; engine prints raw structure only")
    print(json.dumps(out, indent=2))
if __name__ == "__main__":
    main()
