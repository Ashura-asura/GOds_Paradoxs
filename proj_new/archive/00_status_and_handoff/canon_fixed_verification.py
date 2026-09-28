"""Standalone, re-runnable verification of canon_fixed.py's iso-invariance and
soundness. Run: python3 canon_fixed_verification.py
No dependency on the original repo's z25b_engine_v2 -- self-contained."""
import random
import networkx as nx
from canon_fixed import canon_fixed

def rand_graph(N, M, rng):
    pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]
    return frozenset(rng.sample(pairs, M))

def main():
    N = 10
    bad, tot = 0, 0
    rng = random.Random(42)
    for s in range(1000):
        g = rand_graph(N, 15, random.Random(1000 + s))
        perm = list(range(N)); rng.shuffle(perm)
        gp = frozenset(tuple(sorted((perm[a], perm[b]))) for a, b in g)
        tot += 1
        if canon_fixed(g, N) != canon_fixed(gp, N):
            bad += 1
    print(f"iso-invariance: {bad}/{tot} mismatches (want 0)")

    diff_bad, diff_tot = 0, 0
    for s in range(300):
        g1 = rand_graph(N, 15, random.Random(5000 + s))
        g2 = rand_graph(N, 15, random.Random(9000 + s))
        if not nx.is_isomorphic(nx.Graph(list(g1)), nx.Graph(list(g2))):
            diff_tot += 1
            if canon_fixed(g1, N) == canon_fixed(g2, N):
                diff_bad += 1
    print(f"soundness: {diff_bad}/{diff_tot} false merges on non-iso pairs (want 0)")

if __name__ == "__main__":
    main()
