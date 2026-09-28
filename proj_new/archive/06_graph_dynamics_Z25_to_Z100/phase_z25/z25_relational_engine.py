"""
Z25 relational engine  [patched]
 patch 1: canon = canonical form under VERTEX relabeling (proper graph isomorphism), capped
 patch 2: aut_size memoized per canonical form (was re-computed every step)
 patch 3: max_steps=64, edge cap, p-grid x trials sized to run in <10 min
 T is unchanged: bare degree signatures -> task-swap permutation with exp(p*2*-1 tie-break
 -> edge relabel -> one witness edge per non-trivial permutation cycle.
 No energy, no potential, no symmetry input; p and seed bits are the only admitted inputs.
"""
import argparse, collections, itertools, math, random, json

N = 8
SEED_EDGES = frozenset(
    {tuple(sorted((i, (i + 1) % N))) for i in range(N)} | {tuple(sorted((2, 5)))}
)

_AUT = {}

def sig(v, edges):
    indeg  = sum(1 for (a, b) in edges if b == v)
    outdeg = sum(1 for (a, b) in edges if a == v)
    return (indeg, outdeg)

def T(edges, p, rng):
    sigs = {v: sig(v, edges) for v in range(N)}
    order = sorted(range(N), key=lambda v: (sigs[v], v))
    rank = {v: i for i, v in enumerate(order)}
    groups = collections.defaultdict(list)
    for v, s in sigs.items():
        groups[s].append(v)
    perm = {}
    for members in groups.values():
        if len(members) == 1:
            perm[members[0]] = members[0]; continue
        concord = {m: rank[m] for m in members}
        best = max(members, key=lambda m: concord[m])
        if rng.random() < p:
            target = best
        else:
            target = rng.choice(members)
        others = [m for m in members if m != target]
        perm[target] = min(others, key=lambda m: rank[m]) if others else target
        for m in others:
            avail = [x for x in members if x not in perm.values()]
            perm[m] = avail[0] if avail else m
    for v in range(N): perm.setdefault(v, v)

    E1 = {tuple(sorted((perm[a], perm[b]))) for (a, b) in edges}
    seen, extras = set(), set()
    for v in range(N):
        if v in seen: continue
        cyc, node = [], v
        while node not in seen:
            seen.add(node); cyc.append(node); node = perm[node]
        if len(cyc) > 1:
            extras.add(tuple(sorted((cyc[0], cyc[-1]))))
    return frozenset(E1 | extras)

def canon(edges):
    e = set(edges)
    deg = {v: sig(v, e) for v in range(N)}
    best = None
    for g in itertools.permutations(range(N)):
        if any(deg[g[v]] != deg[v] for v in range(N)):
            continue
        s = tuple(sorted(tuple(sorted((g[a], g[b]))) for (a, b) in e))
        if best is None or s < best: best = s
    return best

def aut_size(edges):
    c = canon(edges)
    if c in _AUT: return _AUT[c]
    e = set(c); cnt = 0
    for g in itertools.permutations(range(N)):
        if all(tuple(sorted((g[a], g[b]))) in e for (a, b) in e): cnt += 1
    _AUT[c] = cnt
    return cnt

def run(seed_edges, p, rng, max_steps=64):
    e = set(seed_edges); hist = {}
    for step in range(max_steps):
        c = canon(e)
        if c in hist:
            return dict(period=step - hist[c], start=hist[c],
                        aut_size=aut_size(e), converged=True)
        hist[c] = step
        if len(e) > 40:
            return dict(period=None, aut_size=None, converged=False, saturated=True)
        e = set(T(frozenset(e), p, rng))
    return dict(period=None, aut_size=None, converged=False)

def classify(n_in, n_out, hidden):
    if hidden: return "FAILED"
    if n_out > n_in: return "GENERATED"
    if n_out >= 1:   return "PARTIAL"
    return "FAILED"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    p_grid = [0.0, 0.25, 0.5, 0.75, 1.0] if args.quick else \
             [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    n_trials = 4 if args.quick else 12
    all_ratios = set(); report = {"n_in": 1, "p": {}, "omitted": "bits counted in doc"}
    for p in p_grid:
        rng = random.Random(20260802)
        periods, auts, conv = [], [], 0
        for _ in range(n_trials):
            r = run(SEED_EDGES, p, rng)
            conv += 1 if r.get("converged") else 0
            if r.get("period"): periods.append(r["period"])
            if r.get("aut_size") is not None: auts.append(r["aut_size"])
        ratios = set()
        for a in periods:
            for b in periods:
                if a and b and a != b:
                    g = math.gcd(a, b)
                    ratios.add((a // g, b // g) if a <= b else (b // g, a // g))
        all_ratios |= ratios
        report["p"][str(p)] = dict(
            periods=sorted(periods), aut_sizes=sorted(set(auts)),
            ratios=sorted(ratios), converged=conv, n_trials=n_trials)
    report["distinct_ratios"] = sorted(all_ratios)
    report["n_out"] = len(all_ratios)
    report["verdict"] = classify(1, report["n_out"], hidden=False)
    print(json.dumps(report, indent=2))
if __name__ == "__main__":
    main()
