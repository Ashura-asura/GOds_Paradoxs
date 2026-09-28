import networkx as nx
from z100_core import exact_aut, theta, quotient_graph_aut, twin_partition

def shrikhande():
    # Cayley graph on Z4 x Z4, connection set {±(1,0), ±(0,1), ±(1,1)}
    G = nx.Graph()
    V = [(a, b) for a in range(4) for b in range(4)]
    G.add_nodes_from(V)
    S = [(1,0),(3,0),(0,1),(0,3),(1,1),(3,3)]
    for (a,b) in V:
        for (da,db) in S:
            u = ((a+da)%4,(b+db)%4)
            if u != (a,b):
                G.add_edge((a,b),u)
    return G

def rook4x4():
    G = nx.cartesian_product(nx.complete_graph(4), nx.complete_graph(4))
    return nx.convert_node_labels_to_integers(G)

def petersen():
    return nx.petersen_graph()

def kneser_check():
    return nx.petersen_graph()  # petersen == Kneser(5,2)

results = {}
for name, G, expect_aut, expect_theta in [
    ("Petersen", petersen(), 120, 0),
    ("Shrikhande", shrikhande(), 192, 0),
    ("Rook_4x4", rook4x4(), 1152, 0),
]:
    a = exact_aut(G)
    th, classes = theta(G)
    n = G.number_of_nodes(); m = G.number_of_edges()
    deg = sorted(set(d for _, d in G.degree()))
    ok_aut = (a == expect_aut)
    ok_theta = (th == expect_theta)
    results[name] = dict(n=n, m=m, degrees=deg, aut=a, expect_aut=expect_aut,
                          theta=th, expect_theta=expect_theta,
                          aut_ok=ok_aut, theta_ok=ok_theta)
    print(f"{name}: n={n} m={m} deg={deg} |Aut|={a} (expect {expect_aut}) "
          f"OK={ok_aut} | Theta={th} (expect {expect_theta}) OK={ok_theta}")

assert all(r["aut_ok"] and r["theta_ok"] for r in results.values()), "SELF-CHECK FAILED"
print("\nALL SELF-CHECKS PASSED — engine trusted for downstream tasks.")

import json
with open("selfcheck_results.json","w") as f:
    json.dump(results, f, indent=2)
