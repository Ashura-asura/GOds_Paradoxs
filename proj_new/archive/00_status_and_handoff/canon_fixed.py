"""
Fixed canonical-form function for z25b_engine_v2's graph representation.

Root cause of the original bug (confirmed independently):
  canon() partitioned vertices into WL-color classes, then searched
  permutations *within each class using the class's own original vertex
  index values as the target label set*. For an isomorphic copy g' = pi(g),
  the WL classes are pi(class_c(g)) -- a *different* set of index values --
  so the two searches explore unrelated label spaces and generally produce
  different "canonical" outputs, even though g and g' are isomorphic.

Fix: assign canonical *positions* to classes first (by sorted color rank,
contiguous integer blocks), independent of original vertex labels, then
search only the intra-class permutation freedom for the lexicographically
smallest edge list under that fixed canonical position scheme. Two
isomorphic graphs now search the same target-label space, since the block
structure depends only on the (iso-invariant) sorted list of class sizes
per color rank.
"""
import collections, itertools, math

def wl_colors(edges, N):
    adj = {v: set() for v in range(N)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    color = {v: (len(adj[v]),) for v in range(N)}
    for _ in range(N):
        nc = {v: (color[v], tuple(sorted(color[w] for w in adj[v]))) for v in range(N)}
        uniq = {c: i for i, c in enumerate(sorted(set(nc.values())))}
        nc = {v: uniq[c] for v, c in nc.items()}
        if nc == color:
            break
        color = nc
    return color, adj

CANON_BUDGET = 20000

def canon_fixed(edges, N):
    e = frozenset(edges)
    color, _ = wl_colors(e, N)
    classes = collections.defaultdict(list)
    for v, c in color.items():
        classes[c].append(v)
    keys = sorted(classes)              # canonical color rank order
    # canonical target-label blocks, purely a function of class sizes in rank order
    blocks = {}
    pos = 0
    for k in keys:
        sz = len(classes[k])
        blocks[k] = list(range(pos, pos + sz))
        pos += sz
    budget = 1
    for k in keys:
        budget *= math.factorial(len(classes[k]))
    if budget > CANON_BUDGET:
        # iso-invariant fallback (deterministic key, may merge distinct classes -- declared L2).
        # Signature must include ALL N vertices (isolated vertices get degree 0) and N itself:
        # depending only on edge-endpoint counts ties the signature to the edge SET and silently
        # drops isolates (empty graph -> (), 1 edge -> (1,1) at ANY N), which reproduces the
        # cross-N merge bug fixed in the engine's memo keying.
        degs = [0] * N
        for a, b in e:
            degs[a] += 1; degs[b] += 1
        degsig = (N, tuple(sorted(degs)))
        return ("FIXED-FALLBACK", degsig, budget)
    best = None
    for combo in itertools.product(*[list(itertools.permutations(blocks[k])) for k in keys]):
        g = {}
        for k, cl_targets in zip(keys, combo):
            for orig_v, target in zip(classes[k], cl_targets):
                g[orig_v] = target
        s = tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in e))
        if best is None or s < best:
            best = s
    return ("FIXED-EX", best)
