"""
PHASE Z36 — WHERE DOES SYMMETRY COME FROM?
Honest decomposition, no faking

Experiments:
1. Z25b attractor graphs (from extremal dynamics)
2. Shrikhande graph (16,6,2,2) Aut=192
3. Rook graph (16,6,2,2) Aut=1152
4. Random regular graphs
5. SRG samples (Petersen etc)

Metrics per graph:
- |Aut| exact via VF2
- twin contribution Theta, twin_aut
- component contribution
- quotient automorphism Aut(G/twins)
- degree spectrum
- adjacency spectrum
- common-neighbor distribution
"""

import random, math, itertools, time
from collections import Counter, defaultdict
import json

import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher
import numpy as np

# --- Twin utilities ---
def twin_partition(G):
    adj = {u:set(G.neighbors(u)) for u in G.nodes()}
    parent = {n:n for n in G.nodes()}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb:
            parent[rb]=ra
    nodes=list(G.nodes())
    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            u,v=nodes[i],nodes[j]
            if adj[u]-{v} == adj[v]-{u}:
                union(u,v)
    groups=defaultdict(list)
    for n in nodes:
        groups[find(n)].append(n)
    return list(groups.values())

def theta_twin_aut(G):
    classes=twin_partition(G)
    theta=sum(len(c)*(len(c)-1)//2 for c in classes)
    twin_aut=1
    for c in classes:
        twin_aut*=math.factorial(len(c))
    return theta, twin_aut, classes

def quotient_graph(G, classes):
    # classes: list of lists
    # Map node -> class idx
    node_to_class={}
    for idx,cls in enumerate(classes):
        for n in cls:
            node_to_class[n]=idx
    Q=nx.Graph()
    Q.add_nodes_from(range(len(classes)))
    # For each edge in G, add edge between classes if different
    for u,v in G.edges():
        cu=node_to_class[u]
        cv=node_to_class[v]
        if cu!=cv:
            Q.add_edge(cu,cv)
    # For self loops? Determine if class is clique or independent
    # If any internal edge, then class is clique (true twins)
    # Store as node attribute for colored Aut
    for idx,cls in enumerate(classes):
        # check if clique
        internal_edges=0
        for i in range(len(cls)):
            for j in range(i+1,len(cls)):
                if G.has_edge(cls[i],cls[j]):
                    internal_edges+=1
        is_clique = (internal_edges == len(cls)*(len(cls)-1)//2)
        is_independent = (internal_edges==0)
        Q.nodes[idx]['size']=len(cls)
        Q.nodes[idx]['clique']=is_clique
        Q.nodes[idx]['independent']=is_independent
    return Q

def exact_aut_size(G, cap=5000, timeout=5):
    try:
        GM=GraphMatcher(G,G)
        c=0
        t0=time.time()
        for _ in GM.isomorphisms_iter():
            c+=1
            if c>=cap:
                return c, True, time.time()-t0
            if time.time()-t0>timeout:
                return c, True, time.time()-t0
        return c, False, time.time()-t0
    except Exception as e:
        return 1, False, 0

def colored_aut_size(Q):
    # For quotient with colored nodes by size and clique type, we need to consider automorphisms preserving colors
    # Brute force for small Q (Q size <=16) using GraphMatcher with node_match
    def node_match(n1,n2):
        return n1['size']==n2['size'] and n1['clique']==n2['clique']
    try:
        GM=GraphMatcher(Q,Q,node_match=node_match)
        c=sum(1 for _ in GM.isomorphisms_iter())
        return c
    except:
        return 1

def component_decomposition(G):
    comps=list(nx.connected_components(G))
    if len(comps)<=1:
        return {"num_components":1, "component_sym_factor":1, "is_connected":True, "components":[]}
    # Build subgraphs
    subgraphs=[]
    for comp in comps:
        sg=G.subgraph(comp).copy()
        # relabel to 0..k-1 for iso check
        sg2=nx.convert_node_labels_to_integers(sg)
        subgraphs.append((sg2, len(comp)))
    # Group by isomorphism
    groups=[]
    used=[False]*len(subgraphs)
    for i in range(len(subgraphs)):
        if used[i]: continue
        group=[i]
        used[i]=True
        for j in range(i+1,len(subgraphs)):
            if used[j]: continue
            if nx.is_isomorphic(subgraphs[i][0], subgraphs[j][0]):
                group.append(j)
                used[j]=True
        groups.append(group)
    # component symmetry factor = product factorial(|group|) * (Aut(comp))^{|group|}
    factor=1
    details=[]
    for g in groups:
        k=len(g)
        # Aut of representative
        rep=subgraphs[g[0]][0]
        aut_rep,_ ,_=exact_aut_size(rep, cap=1000, timeout=1)
        factor*=math.factorial(k) * (aut_rep**k)
        details.append({"group_size":k, "representative_nodes":subgraphs[g[0]][1], "aut_rep":aut_rep})
    return {"num_components":len(comps), "component_sym_factor":factor, "is_connected":False, "groups":details}

def spectrum_metrics(G):
    # adjacency spectrum
    try:
        A=nx.to_numpy_array(G)
        eig=np.linalg.eigvals(A)
        eig=sorted(np.real(eig), reverse=True)
        # spectral gap, etc.
        return {"eigenvalues":eig, "spectral_radius":eig[0] if eig else 0, "num_distinct":len(set([round(x,6) for x in eig]))}
    except Exception as e:
        return {"eigenvalues":[],"spectral_radius":0,"num_distinct":0}

def common_neighbor_metrics(G):
    N=G.number_of_nodes()
    lam=Counter()
    mu=Counter()
    for u,v in itertools.combinations(G.nodes(),2):
        com=len(list(nx.common_neighbors(G,u,v)))
        if G.has_edge(u,v):
            lam[com]+=1
        else:
            mu[com]+=1
    return {"lambda_dist":dict(lam), "mu_dist":dict(mu)}

def analyze_graph(G, name=""):
    theta,twin_aut,classes=theta_twin_aut(G)
    Q=quotient_graph(G, classes)
    aut_exact,capped,dt=exact_aut_size(G, cap=5000, timeout=5)
    # quotient aut (colored)
    q_aut=colored_aut_size(Q) if len(Q)<=12 else 1 # cap for large Q
    # For uncolored quotient aut
    q_aut_uncolored,_,_=exact_aut_size(Q, cap=5000, timeout=2) if len(Q)<=12 else (1,False,0)
    comp_info=component_decomposition(G)
    spec=spectrum_metrics(G)
    cn=common_neighbor_metrics(G)
    degs=Counter([d for _,d in G.degree()])
    return {
        "name":name,
        "N":G.number_of_nodes(),
        "M":G.number_of_edges(),
        "Aut_exact":aut_exact,
        "Aut_capped":capped,
        "Aut_time_s":dt,
        "Theta":theta,
        "twin_aut":twin_aut,
        "num_twin_classes":len(classes),
        "twin_class_sizes":sorted([len(c) for c in classes], reverse=True),
        "quotient_N":Q.number_of_nodes(),
        "quotient_M":Q.number_of_edges(),
        "quotient_aut_colored":q_aut,
        "quotient_aut_uncolored":q_aut_uncolored,
        "component_info":comp_info,
        "degree_dist":dict(degs),
        "spectrum":spec,
        "common_neighbors":cn
    }

# --- Generators ---
def build_shrikhande():
    G=nx.Graph()
    G.add_nodes_from(range(16))
    def id_of(x,y): return (x%4)*4 + (y%4)
    S = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)]
    for x in range(4):
        for y in range(4):
            u = id_of(x,y)
            for dx,dy in S:
                v = id_of(x+dx, y+dy)
                if u < v:
                    G.add_edge(u,v)
    return G

def build_rook():
    G=nx.Graph()
    G.add_nodes_from(range(16))
    def id_of(x,y): return x*4+y
    for x in range(4):
        for y in range(4):
            u=id_of(x,y)
            for x2 in range(4):
                for y2 in range(4):
                    v=id_of(x2,y2)
                    if u<v and (x==x2 or y==y2) and not (x==x2 and y==y2):
                        G.add_edge(u,v)
    return G

def build_petersen():
    return nx.petersen_graph()

def build_random_regular(N,d,seed):
    rng=random.Random(seed)
    # try multiple times
    for _ in range(10):
        try:
            G=nx.random_regular_graph(d,N,seed=seed)
            return G
        except:
            seed+=1
    return None

def build_attractor_graphs(num=20, N=10, M=15, steps=200):
    # Run extremal dynamics (lex selector) to get high-Aut attractors
    # Reuse simple dynamics from Z35
    def random_graph(N,M,rng):
        G=nx.Graph()
        G.add_nodes_from(range(N))
        all_edges=[(i,j) for i in range(N) for j in range(i+1,N)]
        rng.shuffle(all_edges)
        G.add_edges_from(all_edges[:M])
        return G
    def degree_tie_info(G):
        degs=dict(G.degree())
        dmax=max(degs.values())
        dmin=min(degs.values())
        Vmax=[n for n,d in degs.items() if d==dmax]
        Vmin=[n for n,d in degs.items() if d==dmin]
        return Vmax,Vmin
    attractors=[]
    for s in range(num*3): # oversample
        rng=random.Random(1000+s)
        G=random_graph(N,M,rng)
        for t in range(steps):
            degs=dict(G.degree())
            dmax=max(degs.values())
            dmin=min(degs.values())
            Vmax=[n for n,d in degs.items() if d==dmax]
            Vmin=[n for n,d in degs.items() if d==dmin]
            # removal: edge with both in Vmax if possible
            rem_cands=[(u,v) for u,v in G.edges() if u in Vmax and v in Vmax]
            if not rem_cands:
                rem_cands=[(u,v) for u,v in G.edges() if u in Vmax or v in Vmax]
            if not rem_cands:
                rem_cands=list(G.edges())
            # addition: non-edge both in Vmin if possible
            non_edges=[(i,j) for i in range(N) for j in range(i+1,N) if not G.has_edge(i,j)]
            add_cands=[(u,v) for u,v in non_edges if u in Vmin and v in Vmin]
            if not add_cands:
                add_cands=[(u,v) for u,v in non_edges if u in Vmin or v in Vmin]
            if not add_cands:
                add_cands=non_edges
            if not rem_cands or not add_cands:
                break
            rem_cands_sorted=sorted(rem_cands)
            add_cands_sorted=sorted(add_cands)
            e_rem=rem_cands_sorted[0]
            # after removal
            G_tmp=G.copy()
            G_tmp.remove_edge(*e_rem)
            # recompute add after removal for lex
            non_edges2=[(i,j) for i in range(N) for j in range(i+1,N) if not G_tmp.has_edge(i,j)]
            Vmin2=[n for n,d in dict(G_tmp.degree()).items() if d==min(dict(G_tmp.degree()).values())]
            add_cands2=[(u,v) for u,v in non_edges2 if u in Vmin2 and v in Vmin2]
            if not add_cands2:
                add_cands2=[(u,v) for u,v in non_edges2 if u in Vmin2 or v in Vmin2]
            if not add_cands2:
                add_cands2=non_edges2
            e_add=sorted(add_cands2)[0]
            if e_rem==e_add:
                continue
            G.remove_edge(*e_rem)
            if not G.has_edge(*e_add):
                G.add_edge(*e_add)
        # after steps, check Aut
        theta,_,_=theta_twin_aut(G)
        if theta>0:
            attractors.append(G.copy())
            if len(attractors)>=num:
                break
    return attractors

# --- Run ---
results=[]

# 1. Z25b attractors
print("Generating Z25b attractors...")
attr_graphs=build_attractor_graphs(num=15, N=10, M=15, steps=200)
print(f"Got {len(attr_graphs)} attractors")
for i,g in enumerate(attr_graphs):
    res=analyze_graph(g, name=f"Z25b_attractor_{i}")
    results.append(res)
    print(f"  attractor {i}: N=10 M=15 Theta={res['Theta']} twin_aut={res['twin_aut']} Aut={res['Aut_exact']}")

# 2. Shrikhande
print("\nShrikhande...")
Gs=build_shrikhande()
res=analyze_graph(Gs, name="Shrikhande_16_48")
results.append(res)
print(res)

# 3. Rook
print("\nRook...")
Gr=build_rook()
res=analyze_graph(Gr, name="Rook_16_48")
results.append(res)
print(res)

# 4. Random regular
print("\nRandom regular...")
for d in [3,4,6]:
    for seed in range(5):
        G=build_random_regular(16,d,seed+100)
        if G is None: continue
        res=analyze_graph(G, name=f"RandomRegular_N16_d{d}_seed{seed}")
        results.append(res)
        print(f"  d={d} seed={seed} Aut={res['Aut_exact']} Theta={res['Theta']}")

# 5. SRG samples
print("\nSRG samples...")
# Petersen
Gp=build_petersen()
res=analyze_graph(Gp, name="Petersen_10_15")
results.append(res)
print(f"Petersen Aut={res['Aut_exact']} Theta={res['Theta']}")

# Also Clebsch complement? Try SRG(16,10,6,6) = complement of Shrikhande
Gc=nx.complement(Gs)
res=analyze_graph(Gc, name="Complement_Shrikhande_16_80")
results.append(res)
print(f"Complement Shrikhande Aut={res['Aut_exact']}")

# Save
with open("/mnt/data/z36_results.json","w") as f:
    json.dump(results,f,indent=2)
print("\nSaved to /mnt/data/z36_results.json")
