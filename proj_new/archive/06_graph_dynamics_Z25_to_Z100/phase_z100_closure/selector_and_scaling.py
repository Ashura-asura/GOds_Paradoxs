import random, json, math, time
from z100_core import (random_graph, step, exact_aut, theta, canon_key,
                        degree_entropy, extremal_removable_edges,
                        extremal_addable_nonedges)
import networkx as nx

SEED0 = 99001

def entropy_step(G, rng):
    """Deterministic selector: among tied extremal removable/addable pairs,
    pick the (r,a) combo that MINIMIZES resulting degree entropy."""
    R = extremal_removable_edges(G)
    A = extremal_addable_nonedges(G)
    if not R or not A:
        return G, None, None, None, None
    best = None
    best_ent = None
    for r in R:
        for a in A:
            if a == r:
                continue
            H = G.copy()
            H.remove_edge(*r)
            if not H.has_edge(*a):
                H.add_edge(*a)
            e = degree_entropy(H)
            if best_ent is None or e < best_ent or (e == best_ent and (r, a) < best):
                best_ent = e
                best = (r, a)
    if best is None:
        return G, None, None, None, None
    r, a = best
    H = G.copy()
    H.remove_edge(*r)
    if not H.has_edge(*a):
        H.add_edge(*a)
    return H, r, a, len(R), len(A)


def run_selector_cmp(N, M, seed, selector, steps=40):
    rng = random.Random(seed)
    G = random_graph(N, M, rng)
    keys = []
    for t in range(steps):
        keys.append(canon_key(G))
        if selector == "entropy":
            out = entropy_step(G, rng)
        else:
            out = step(G, rng, selector=selector)
        G = out[0]
        if out[1] is None:
            break
    th, _ = theta(G)
    return keys, th, exact_aut(G)


def compare_selectors():
    N, M = 10, 15
    NCHAINS = 30
    out = {}
    for sel in ("lex", "entropy"):
        attractors = set()
        thetas_pos = 0
        for c in range(NCHAINS):
            keys, th, a = run_selector_cmp(N, M, SEED0 + c, sel)
            if len(keys) < 20:
                continue
            attractors.add(keys[-1])
            if th > 0:
                thetas_pos += 1
        out[sel] = {"n_distinct_attractors": len(attractors),
                     "frac_twin_positive": thetas_pos / NCHAINS}
    print("Selector comparison (N=10,M=15,30 chains):", json.dumps(out, indent=2))
    return out


def n16_feasibility():
    N, M = 16, 40  # rho ~= 0.33
    t0 = time.time()
    rng = random.Random(SEED0 + 5000)
    G = random_graph(N, M, rng)
    steps_done = 0
    for t in range(30):
        out = step(G, rng, selector="lex")
        G = out[0]
        steps_done += 1
        if out[1] is None:
            break
    a = exact_aut(G)
    th, _ = theta(G)
    dt = time.time() - t0
    print(f"N=16 feasibility: {steps_done} steps in {dt:.2f}s "
          f"({dt/max(1,steps_done)*1000:.1f} ms/step incl. exact |Aut|+Theta), "
          f"final |Aut|={a}, Theta={th}")
    return {"N": N, "M": M, "steps": steps_done, "seconds": dt,
            "ms_per_step": dt / max(1, steps_done) * 1000,
            "final_aut": a, "final_theta": th}


if __name__ == "__main__":
    report = {"selector_comparison": compare_selectors(),
              "n16_feasibility": n16_feasibility()}
    with open("selector_and_scaling_results.json", "w") as f:
        json.dump(report, f, indent=2)
