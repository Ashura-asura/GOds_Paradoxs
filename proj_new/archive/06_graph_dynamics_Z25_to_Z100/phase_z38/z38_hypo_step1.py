"""
Z38 — HYPOTHESIS STEP 1 (T1 + F2 gates)
"Space-definition hypothesis" first falsifiable probe (purposed_hypo_mechanism.md).

T1 — "twin tokens are codified, not explorative":
    Over relaxation runs, twin-partition signatures are emitted at every step;
    a JUMP is a step where the iso-invariant twin-size spectrum changes.
    GATE T1-PASS  <=  H(token stream at jumps)  <  0.8 * H(move entropy)
    If the twin identity in the quotient were a random walk, H_token would
    saturate H_move; a low ratio says the twins' restructuring is
    deterministic/parsimonious -> "codified space".

F2 — "space at the interface" (secondary):
    Fraction of steps spent in the tie-shell where |R|,|A| are small
    (degenerate candidate sets = "boundary/vacuum"), logged per cell.
"""
import random, itertools, math, collections, json, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'phase_z25'))
import z25b_engine_v2 as eng


def twin_classes(N, edges):
    """iso-invariant twin-size spectrum (sorted class sizes), no label dependence."""
    adj = {v: set() for v in range(N)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    parent = {v: v for v in range(N)}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    for u in range(N):
        for v in range(u + 1, N):
            if adj[u] - {v} == adj[v] - {u}:
                union(u, v)
    sizes = collections.Counter(find(v) for v in range(N))
    return tuple(sorted(sizes.values()))


def cands(edges, N):
    deg = {v: 0 for v in range(N)}
    for a, b in edges:
        deg[a] += 1; deg[b] += 1
    dmax, dmin = max(deg.values()), min(deg.values())
    Vmax = [v for v, d in deg.items() if d == dmax]
    Vmin = [v for v, d in deg.items() if d == dmin]
    R, A = len(Vmax), len(Vmin)
    rem_both = [(a, b) for a, b in edges if a in Vmax and b in Vmax]
    rem_c = len(rem_both) if rem_both else sum(1 for a, b in edges
                                               if a in Vmax or b in Vmax)
    non_edges = [(a, b) for a in range(N) for b in range(a + 1, N)
                 if (a, b) not in edges]
    add_both = sum(1 for a, b in non_edges if a in Vmin and b in Vmin)
    add_c = add_both if add_both else sum(1 for a, b in non_edges
                                          if a in Vmin or b in Vmin)
    if rem_c and add_c:
        return R, A, rem_c, add_c
    return R, A, 1, 1


def run_tokens(N, M, seed, p, steps=120):
    eng.N = N
    rng = random.Random(seed)
    pairs = list(itertools.combinations(range(N), 2))
    e = frozenset(rng.sample(pairs, M))
    tokens, jump, exbits, shells = [], [], [], []
    prev = None
    for _ in range(steps):
        sig = twin_classes(N, e)
        tokens.append(sig)
        R, A, rc, ac = cands(e, N)
        shells.append((R, A))
        ex = rc * ac
        exbits.append(math.log2(ex) if ex > 0 else 0.0)
        jump.append(1 if prev is not None and sig != prev else 0)
        prev = sig
        e = frozenset(eng.T(set(e), p, rng))
    return tokens, jump, exbits, shells


def shannon(counts, total):
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def measure(run):
    tokens, jump, exbits, shells = run
    n_jump = sum(jump)
    if n_jump == 0:
        return None
    jtok = [t for t, j in zip(tokens, jump) if j]
    cnt = collections.Counter(jtok)
    H_token = shannon(cnt.values(), len(jtok))
    valid_ex = [x for x in exbits if x > 0]
    H_move = sum(valid_ex) / len(valid_ex) if valid_ex else 0.0     # mean move bits/step
    ratio = H_token / H_move if H_move > 0 else 0.0
    return H_token, H_move, ratio, ratio < 0.8, n_jump, len(cnt)


def main():
    results = {}
    for N, M in [(10, 15), (12, 18)]:
        runs = []
        for p in [0.0, 0.5, 1.0]:
            for s in range(12):
                r = run_tokens(N, M, 1000 + 7 * s, p, 120)
                m = measure(r)
                if m is not None:
                    Htok, Hmov, ratio, ok, nj, dtok = m
                    runs.append(dict(p=p, seed=s, H_token=Htok, H_move=Hmov,
                                     ratio=ratio, T1_pass=ok, n_jump=nj,
                                     distinct_tokens=dtok))
        passes = sum(1 for r in runs if r["T1_pass"])
        Ht = sum(r["H_token"] for r in runs) / len(runs)
        Hm = sum(r["H_move"] for r in runs) / len(runs)
        results[f"{N}_{M}"] = dict(runs=len(runs),
                                   T1_pass_share=(passes / len(runs)) if runs else 0.0,
                                   pass_count=passes,
                                   H_token_mean=Ht, H_move_mean=Hm,
                                   ratio_mean=(Ht / Hm if Hm else 0.0))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()