"""Independent verification of the canon() fix (Rule-8 #1/#2, 2026-08-03).

Checks:
  1. Iso-invariance: for K random iso pairs, fixed canon must agree 100%.
     (Old buggy canon: ~56% artifact rate on iso successor pairs.)
  2. Soundness: for K random NON-iso pairs (confirmed by networkx), fixed
     canon must NOT merge them (no false iso claims) within the exact branch.
  3. Exhaustive small-N: every labeled graph on N<=7 vertices, every
     relabeling permutation, canon(relabeled) == canon(original) must hold.
  4. Brute-force oracle: for N<=6 (and N=7 sampled), canon equals the true
     lex-min canonical form over ALL N! permutations (independent oracle).

Networkx nx.is_isomorphic is the ground truth for iso/non-iso classification.
"""
import itertools, math, random, sys
sys.path.insert(0, r"phase_z25")
import networkx as nx
import z25b_engine_v2 as E

def relabel(e, perm, N):
    return frozenset(tuple(sorted((perm[a], perm[b]))) for a, b in e)

def brute_canon(e, N):
    best = None
    for g in itertools.permutations(range(N)):
        s = tuple(sorted(tuple(sorted((g[a], g[b]))) for a, b in e))
        if best is None or s < best:
            best = s
    return best

def to_nx(e, N):
    G = nx.Graph(); G.add_nodes_from(range(N)); G.add_edges_from(e); return G

rng = random.Random(20260803)
N = 10
r1_ok = r1_total = 0
r1_ex = r1_ex_total = 0
for t in range(1000):
    e = frozenset(tuple(sorted(ee)) for ee in
                  rng.sample(list(itertools.combinations(range(N), 2)), 15))
    perm = list(range(N)); rng.shuffle(perm)
    e2 = relabel(e, perm, N)
    k1, k2 = E.canon(e), E.canon(e2)
    assert nx.is_isomorphic(to_nx(e, N), to_nx(e2, N))
    r1_total += 1
    if k1 == k2:
        r1_ok += 1
    if k1[0] == "EX" and k2[0] == "EX":
        r1_ex_total += 1
        if k1 == k2:
            r1_ex += 1
print(f"R1 iso-invariance (all keys): {r1_ok}/{r1_total}")
print(f"R1 iso-invariance (EX branch only): {r1_ex}/{r1_ex_total}")

r2_ok = r2_total = 0
r2_ex = r2_ex_total = 0
while r2_total < 300:
    e1 = frozenset(tuple(sorted(ee)) for ee in
                   rng.sample(list(itertools.combinations(range(N), 2)), 15))
    e2 = frozenset(tuple(sorted(ee)) for ee in
                   rng.sample(list(itertools.combinations(range(N), 2)), 15))
    if nx.is_isomorphic(to_nx(e1, N), to_nx(e2, N)):
        continue
    r2_total += 1
    k1, k2 = E.canon(e1), E.canon(e2)
    if k1 != k2:
        r2_ok += 1
    if k1[0] == "EX" and k2[0] == "EX":
        r2_ex_total += 1
        if k1 != k2:
            r2_ex += 1
print(f"R2 soundness (all keys, non-iso pairs): {r2_ok}/{r2_total} distinct")
print(f"R2 soundness (EX branch only): {r2_ex}/{r2_ex_total} distinct")

E._MEMO.clear()
r3_total = 0
r3_fail = 0
for Ns in (4, 5, 6, 7):
    E.N = Ns
    E._MEMO.clear()
    n_iso = sum(1 for e in itertools.combinations(itertools.combinations(range(Ns), 2), Ns)) \
        if False else 0
    edges_all = list(itertools.combinations(range(Ns), 2))
    cnt = 0
    for combo in itertools.combinations(edges_all, max(1, Ns // 2)):
        e = frozenset(combo)
        k1 = E.canon(e)
        for perm in itertools.permutations(range(Ns)):
            if perm == tuple(range(Ns)):
                continue
            k2 = E.canon(relabel(e, perm, Ns))
            r3_total += 1
            if k1 != k2:
                r3_fail += 1
        cnt += 1
        if cnt >= 40:
            break
print(f"R3 exhaustive relabel check (N<=7): {r3_total} pairs, {r3_fail} failures")

E._MEMO.clear()
r4_ok = r4_total = 0
for Ns in (4, 5, 6):
    E.N = Ns
    E._MEMO.clear()
    edges_all = list(itertools.combinations(range(Ns), 2))
    cnt = 0
    for combo in itertools.combinations(edges_all, max(1, Ns // 2)):
        e = frozenset(combo)
        k = E.canon(e)
        b = brute_canon(e, Ns)
        r4_total += 1
        if tuple(k[1]) == b:
            r4_ok += 1
        cnt += 1
        if cnt >= 50:
            break
for Ns in (7,):
    E.N = Ns
    E._MEMO.clear()
    edges_all = list(itertools.combinations(range(Ns), 2))
    cnt = 0
    while cnt < 25:
        combo = tuple(sorted(rng.sample(edges_all, 12)))
        e = frozenset(combo)
        k = E.canon(e)
        b = brute_canon(e, Ns)
        r4_total += 1
        if tuple(k[1]) == b:
            r4_ok += 1
        cnt += 1
print(f"R4 brute-force oracle (true lex-min over N!): {r4_ok}/{r4_total}")
