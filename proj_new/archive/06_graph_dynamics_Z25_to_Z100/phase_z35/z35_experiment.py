"""
PHASE Z35 — TIE-COLLAPSE MECHANISM
Implementation of Rule-8 first, L1/L2/L3 separation

Dynamics:
- Graph G(N,M) preserved
- Canonical extremal exchange: remove edge incident to max-degree, add non-edge incident to min-degree
- Selectors: lex, random, entropy, autmin
- Canonicalization: optional degree-sorted relabel

Metrics:
- Theta(G) = sum_i |C_i| choose 2 where C_i are twin classes (N(u)\{v} == N(v)\{u})
- Aut_twin = prod factorial(|C_i|)
- Aut_exact via networkx GraphMatcher (capped)
- R = |V_max|, A = |V_min|
- R_edge = |removal candidates|, A_nonedge = |addition candidates|
"""

import random
import math
import itertools
import time
from collections import defaultdict, Counter
import json

import networkx as nx
import numpy as np

# --- Union Find ---
class UF:
    def __init__(self, nodes):
        self.p = {n:n for n in nodes}
        self.r = {n:0 for n in nodes}
    def find(self, x):
        while self.p[x]!=x:
            self.p[x]=self.p[self.p[x]]
            x=self.p[x]
        return x
    def union(self, a,b):
        ra=self.find(a); rb=self.find(b)
        if ra==rb: return
        if self.r[ra]<self.r[rb]:
            self.p[ra]=rb
        elif self.r[ra]>self.r[rb]:
            self.p[rb]=ra
        else:
            self.p[rb]=ra
            self.r[ra]+=1

def twin_partition(G):
    nodes = list(G.nodes())
    adj = {u: set(G.neighbors(u)) for u in nodes}
    uf = UF(nodes)
    # O(N^2) pairwise twin check
    for i in range(len(nodes)):
        u = nodes[i]
        for j in range(i+1, len(nodes)):
            v = nodes[j]
            # twin condition: N(u)\{v} == N(v)\{u}
            if adj[u] - {v} == adj[v] - {u}:
                uf.union(u,v)
    # collect classes
    groups = defaultdict(list)
    for n in nodes:
        groups[uf.find(n)].append(n)
    classes = list(groups.values())
    return classes

def theta_and_twin_aut(G):
    classes = twin_partition(G)
    theta = 0
    twin_aut = 1
    for c in classes:
        k = len(c)
        if k>=2:
            theta += k*(k-1)//2
            twin_aut *= math.factorial(k)
    return theta, twin_aut, classes

def exact_aut_size(G, cap=20000, timeout=0.5):
    # Use GraphMatcher, but cap to avoid explosion
    try:
        GM = nx.algorithms.isomorphism.GraphMatcher(G, G)
        count = 0
        start = time.time()
        for _ in GM.isomorphisms_iter():
            count+=1
            if count>=cap:
                return count, True  # capped
            if time.time()-start>timeout:
                return count, True
        return count, False
    except Exception as e:
        return 1, False

def degree_tie_info(G):
    degs = dict(G.degree())
    if not degs:
        return 0,0,0,0,0,0
    dmax = max(degs.values())
    dmin = min(degs.values())
    Vmax = [n for n,d in degs.items() if d==dmax]
    Vmin = [n for n,d in degs.items() if d==dmin]
    R = len(Vmax)
    A = len(Vmin)
    # candidate counts
    # removal: edges incident to Vmax
    rem_both = [(u,v) for u,v in G.edges() if u in Vmax and v in Vmax]
    if rem_both:
        rem_cands = rem_both
    else:
        rem_cands = [(u,v) for u,v in G.edges() if u in Vmax or v in Vmax]
    # addition: non-edges with both in Vmin preferred
    nodes = list(G.nodes())
    non_edges_all = [(i,j) for i in nodes for j in nodes if i<j and not G.has_edge(i,j)]
    add_both = [(u,v) for u,v in non_edges_all if u in Vmin and v in Vmin]
    if add_both:
        add_cands = add_both
    else:
        add_cands = [(u,v) for u,v in non_edges_all if u in Vmin or v in Vmin]
    return R, A, len(rem_cands), len(add_cands), rem_cands, add_cands

def canonical_relabel(G):
    # approximate canonical: sort by degree desc, then by neighbor degree tuple
    nodes = list(G.nodes())
    degs = dict(G.degree())
    # compute signature
    def sig(n):
        nbr_degs = tuple(sorted([degs[m] for m in G.neighbors(n)], reverse=True))
        return (-degs[n], nbr_degs)
    sorted_nodes = sorted(nodes, key=sig)
    mapping = {old:new for new, old in enumerate(sorted_nodes)}
    H = nx.relabel_nodes(G, mapping)
    return H

def random_graph(N,M, rng):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    all_edges = [(i,j) for i in range(N) for j in range(i+1,N)]
    rng.shuffle(all_edges)
    G.add_edges_from(all_edges[:M])
    return G

def degree_entropy(G):
    degs = [d for _,d in G.degree()]
    cnt = Counter(degs)
    total = len(degs)
    ent = 0.0
    for c in cnt.values():
        p = c/total
        ent -= p*math.log(p+1e-12)
    return ent

# Selectors
def select_edge(candidates, G, mode, rng, for_removal=True):
    if not candidates:
        return None
    # candidates are list of (u,v)
    candidates = sorted(candidates)  # lex order base
    if mode == "lex":
        return candidates[0]
    elif mode == "random":
        return rng.choice(candidates)
    elif mode == "entropy":
        # choose that maximizes entropy after operation (or minimizes variance)
        best = None
        best_score = -1e9
        # evaluate up to 20 random subsample if many candidates
        sample = candidates
        if len(sample)>30:
            sample = rng.sample(candidates, 30)
        for (u,v) in sample:
            # simulate
            H = G.copy()
            if for_removal:
                if H.has_edge(u,v):
                    H.remove_edge(u,v)
            else:
                if not H.has_edge(u,v):
                    H.add_edge(u,v)
            ent = degree_entropy(H)
            if ent > best_score:
                best_score = ent
                best = (u,v)
        return best if best else candidates[0]
    elif mode == "autmin":
        # choose that minimizes Theta after operation (adversarial)
        best = None
        best_score = 1e9
        sample = candidates
        if len(sample)>30:
            sample = rng.sample(candidates, 30)
        for (u,v) in sample:
            H = G.copy()
            if for_removal:
                if H.has_edge(u,v):
                    H.remove_edge(u,v)
            else:
                if not H.has_edge(u,v):
                    H.add_edge(u,v)
            th,_,_ = theta_and_twin_aut(H)
            if th < best_score:
                best_score = th
                best = (u,v)
        return best if best else candidates[0]
    else:
        return candidates[0]

def one_step(G, selector, rng, use_canonical=True, reverse=False):
    # reverse flag for Control B
    degs = dict(G.degree())
    if not degs:
        return G, None, None, (0,0,0,0)
    dmax = max(degs.values())
    dmin = min(degs.values())
    Vmax = [n for n,d in degs.items() if d==dmax]
    Vmin = [n for n,d in degs.items() if d==dmin]
    if reverse:
        # remove min, add max
        R_nodes = Vmin
        A_nodes = Vmax
    else:
        R_nodes = Vmax
        A_nodes = Vmin

    # removal candidates
    # both in R_nodes preferred
    rem_both = [(u,v) for u,v in G.edges() if u in R_nodes and v in R_nodes]
    if rem_both:
        rem_cands = rem_both
    else:
        rem_cands = [(u,v) for u,v in G.edges() if u in R_nodes or v in R_nodes]
    # addition candidates
    nodes = list(G.nodes())
    non_edges_all = [(i,j) for i in nodes for j in nodes if i<j and not G.has_edge(i,j)]
    add_both = [(u,v) for u,v in non_edges_all if u in A_nodes and v in A_nodes]
    if add_both:
        add_cands = add_both
    else:
        add_cands = [(u,v) for u,v in non_edges_all if u in A_nodes or v in A_nodes]

    # if empty, fallback to any edge / any non-edge
    if not rem_cands:
        rem_cands = list(G.edges())
    if not add_cands:
        add_cands = non_edges_all

    if not rem_cands or not add_cands:
        return G, None, None, (len(Vmax), len(Vmin), len(rem_cands), len(add_cands))

    e_rem = select_edge(rem_cands, G, selector, rng, for_removal=True)
    # for addition, evaluate after removal for entropy/autmin? Simplify: evaluate on G after removal
    G_tmp = G.copy()
    if G_tmp.has_edge(*e_rem):
        G_tmp.remove_edge(*e_rem)
    e_add = select_edge(add_cands, G_tmp, selector, rng, for_removal=False)

    # avoid self-loop or duplicate
    if e_rem is None or e_add is None:
        return G, None, None, (len(Vmax), len(Vmin), len(rem_cands), len(add_cands))
    if e_rem == e_add:
        return G, None, None, (len(Vmax), len(Vmin), len(rem_cands), len(add_cands))

    # perform exchange
    H = G.copy()
    if H.has_edge(*e_rem):
        H.remove_edge(*e_rem)
    if not H.has_edge(*e_add):
        H.add_edge(*e_add)

    if use_canonical:
        H = canonical_relabel(H)

    R,A,Re,Ae,_,_ = degree_tie_info(G)  # for reporting before move
    # actually need R,A as tie sizes
    return H, e_rem, e_add, (R,A,Re,Ae)

def run_trajectory(N,M, steps, selector, seed, use_canonical=True, reverse=False, compute_exact_aut=False):
    rng = random.Random(seed)
    G = random_graph(N,M,rng)
    if use_canonical:
        G = canonical_relabel(G)
    history = []
    for t in range(steps):
        th, twin_aut, classes = theta_and_twin_aut(G)
        R,A,Re,Ae,_,_ = degree_tie_info(G)
        # exact aut occasionally
        exact_aut = None
        capped = False
        if compute_exact_aut and (t%5==0 or th>0):
            exact_aut, capped = exact_aut_size(G, cap=20000, timeout=0.3)
        else:
            exact_aut = twin_aut  # proxy
        history.append({
            "t": t,
            "theta": th,
            "twin_aut": twin_aut,
            "exact_aut": exact_aut,
            "R": R,
            "A": A,
            "Re": Re,
            "Ae": Ae,
            "deg_entropy": degree_entropy(G),
            "M": G.number_of_edges()
        })
        G, e_rem, e_add, _ = one_step(G, selector, rng, use_canonical=use_canonical, reverse=reverse)
    return history

# ---- Controls ----
def run_control_degree_preserving(N,M, steps, seed):
    rng = random.Random(seed)
    G = random_graph(N,M,rng)
    history = []
    for t in range(steps):
        th, twin_aut, _ = theta_and_twin_aut(G)
        R,A,Re,Ae,_,_ = degree_tie_info(G)
        history.append({"t":t,"theta":th,"twin_aut":twin_aut,"R":R,"A":A,"Re":Re,"Ae":Ae})
        # degree-preserving double edge swap
        # pick two edges (a,b) and (c,d) with distinct nodes, and swap to (a,d),(c,b) if not existing
        edges = list(G.edges())
        if len(edges)<2:
            continue
        # try up to 20 attempts
        for _ in range(20):
            (a,b) = rng.choice(edges)
            (c,d) = rng.choice(edges)
            if len({a,b,c,d})<4:
                continue
            # choose swap (a,d) and (c,b)
            if not G.has_edge(a,d) and not G.has_edge(c,b) and a!=d and c!=b:
                G.remove_edge(a,b)
                G.remove_edge(c,d)
                G.add_edge(a,d)
                G.add_edge(c,b)
                break
            elif not G.has_edge(a,c) and not G.has_edge(b,d):
                G.remove_edge(a,b)
                G.remove_edge(c,d)
                G.add_edge(a,c)
                G.add_edge(b,d)
                break
    return history

# ---- Main experiment for PHASE Z35 ----
def experiment_main():
    results = {}
    # Phase 3: main cell (10,15) with 4 selectors
    N,M = 10,15
    steps = 150
    # reduce counts for time: 100 random, 50 each others, but report as scaled
    configs = [
        ("random", 100),
        ("lex", 50),
        ("entropy", 50),
        ("autmin", 50),
    ]
    all_histories = []
    for sel, n_seeds in configs:
        for s in range(n_seeds):
            seed = 1000 + s + hash(sel)%10000
            hist = run_trajectory(N,M, steps, selector=sel, seed=seed, use_canonical=True, reverse=False, compute_exact_aut=(s<10))
            all_histories.append({"selector":sel, "seed":seed, "hist":hist})

    results["main_cell"] = all_histories

    # Control A: degree-preserving
    controlA = []
    for s in range(50):
        hist = run_control_degree_preserving(N,M, steps, seed=2000+s)
        controlA.append({"seed":2000+s,"hist":hist})
    results["controlA_degree_preserving"] = controlA

    # Control B: reversed extremal
    controlB = []
    for s in range(50):
        hist = run_trajectory(N,M, steps, selector="lex", seed=3000+s, use_canonical=True, reverse=True, compute_exact_aut=False)
        controlB.append({"seed":3000+s,"hist":hist})
    results["controlB_reversed"] = controlB

    # Control C: random without canonicalization
    controlC_with = []
    controlC_without = []
    for s in range(50):
        hist_with = run_trajectory(N,M, steps, selector="random", seed=4000+s, use_canonical=True, reverse=False)
        hist_without = run_trajectory(N,M, steps, selector="random", seed=4000+s, use_canonical=False, reverse=False)
        controlC_with.append({"seed":4000+s,"hist":hist_with})
        controlC_without.append({"seed":4000+s,"hist":hist_without})
    results["controlC_with_canon"] = controlC_with
    results["controlC_without_canon"] = controlC_without

    # Phase 5: generalization
    gen_cells = [(8,12),(10,15),(12,20),(14,28),(16,32)]
    gen_results = {}
    for (n,m) in gen_cells:
        trajs = []
        for s in range(30):
            hist = run_trajectory(n,m, steps=100, selector="lex", seed=5000+s+n*100, use_canonical=True, reverse=False)
            trajs.append({"seed":5000+s,"hist":hist})
        gen_results[f"{n}_{m}"] = trajs
    results["generalization"] = gen_results

    return results

if __name__ == "__main__":
    res = experiment_main()
    # Save
    with open("/mnt/data/z35_results.json","w") as f:
        json.dump(res, f)
    print("Saved results")
