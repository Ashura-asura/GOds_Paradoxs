"""
Z100 CORE ENGINE
================
Rule-7 applies: this file is guilty until proven otherwise. Every function
here is checked against a known ground truth before being trusted downstream
(see z100_selfcheck.py).

Exact automorphism counting uses igraph's VF2/BLISS backend
(count_automorphisms_vf2), NOT the old hand-rolled permutation search from
the Z25-Z37 arc. This is the single biggest correction going into Task 1:
several earlier phases (z32, z35 imports) relied on a custom aut_size_exact
that was never independently cross-checked against a second library.

Twin definition (kept identical to Z34/Z36 for continuity):
  u,v are twins iff adj(u) - {v} == adj(v) - {u}
  (this catches BOTH true twins (adjacent, equal closed nbhd) and false
  twins (non-adjacent, equal open nbhd) under one relation, exactly as
  phase_z36/z36_experiment.py did it.)

Theta = sum over twin classes C_i of C(|C_i|, 2)
"""
import itertools, math, random, collections
import igraph as ig
import networkx as nx
import numpy as np


# ---------------------------------------------------------------- graph IO
def nx_to_ig(G):
    n = G.number_of_nodes()
    nodes = list(G.nodes())
    idx = {v: i for i, v in enumerate(nodes)}
    edges = [(idx[u], idx[v]) for u, v in G.edges()]
    return ig.Graph(n=n, edges=edges)


def exact_aut(G):
    """Exact |Aut(G)| via BLISS (igraph). This is the corrected Task-1 key."""
    return nx_to_ig(G).count_automorphisms_vf2()


def canon_key(G):
    """True iso-invariant canonical key: BLISS canonical permutation applied
    to adjacency, serialized. Two graphs are isomorphic iff this key matches.
    This replaces any label-order-dependent 'canon()' from earlier phases."""
    h = nx_to_ig(G)
    perm = h.canonical_permutation()
    h2 = h.permute_vertices(perm)
    n = h2.vcount()
    A = [[0] * n for _ in range(n)]
    for e in h2.get_edgelist():
        A[e[0]][e[1]] = 1
        A[e[1]][e[0]] = 1
    return tuple(tuple(row) for row in A)


def twin_partition(G):
    adj = {u: set(G.neighbors(u)) for u in G.nodes()}
    nodes = list(G.nodes())
    parent = {v: v for v in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, v = nodes[i], nodes[j]
            if adj[u] - {v} == adj[v] - {u}:
                union(u, v)
    groups = collections.defaultdict(list)
    for v in nodes:
        groups[find(v)].append(v)
    return list(groups.values())


def theta(G):
    classes = twin_partition(G)
    return sum(len(c) * (len(c) - 1) // 2 for c in classes), classes


def quotient_graph_aut(G, classes):
    """Aut(Q_colored): quotient by twin classes, vertices colored by class
    size, edges by whether classes are fully-adjacent / fully-nonadjacent
    (guaranteed constant across a twin-class pair by construction)."""
    idx = {v: i for i, v in enumerate(classes)}
    rep = [c[0] for c in classes]
    h = ig.Graph(n=len(classes))
    edges = []
    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            if G.has_edge(rep[i], rep[j]):
                edges.append((i, j))
    h.add_edges(edges)
    colors = [len(c) for c in classes]
    return h.count_automorphisms_vf2(color=colors)


def degree_variance(G):
    d = [deg for _, deg in G.degree()]
    return float(np.var(d))


def degree_entropy(G):
    d = [deg for _, deg in G.degree()]
    c = collections.Counter(d)
    n = len(d)
    ps = [v / n for v in c.values()]
    return -sum(p * math.log2(p) for p in ps)


def num_components(G):
    return nx.number_connected_components(G)


# ------------------------------------------------------- exchange dynamics
def extremal_removable_edges(G):
    """Edges whose endpoint degree-sum is maximal (extremal removal rule)."""
    edges = list(G.edges())
    if not edges:
        return []
    scores = [(G.degree(u) + G.degree(v), (u, v)) for u, v in edges]
    mx = max(s for s, _ in scores)
    return [e for s, e in scores if s == mx]


def extremal_addable_nonedges(G):
    """Non-edges whose endpoint degree-sum is minimal (extremal addition rule)."""
    nodes = list(G.nodes())
    nonedges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            u, v = nodes[i], nodes[j]
            if not G.has_edge(u, v):
                nonedges.append((u, v))
    if not nonedges:
        return []
    scores = [(G.degree(u) + G.degree(v), (u, v)) for u, v in nonedges]
    mn = min(s for s, _ in scores)
    return [e for s, e in scores if s == mn]


def step(G, rng, selector="random"):
    """One conservative edge-exchange step. selector picks among tied
    extremal choices: 'random' | 'lex' | 'entropy'."""
    R = extremal_removable_edges(G)
    A = extremal_addable_nonedges(G)
    if not R or not A:
        return G, None, None
    if selector == "lex":
        r = min(R)
    elif selector == "random":
        r = rng.choice(R)
    else:
        r = rng.choice(R)
    cand_A = [a for a in A if a != r]
    if not cand_A:
        cand_A = A
    if selector == "lex":
        a = min(cand_A)
    else:
        a = rng.choice(cand_A)
    H = G.copy()
    H.remove_edge(*r)
    if not H.has_edge(*a):
        H.add_edge(*a)
    return H, r, a, len(R), len(A)


def random_graph(n, m, rng):
    nodes = list(range(n))
    all_pairs = list(itertools.combinations(nodes, 2))
    rng.shuffle(all_pairs)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(all_pairs[:m])
    return G
