"""
TASK 4 — SYMMETRY CHANNEL PHASE DIAGRAM
Pre-registered classification rule (applied to each ATTRACTOR graph, i.e.
the graph reached after the lex-selector chain settles into its 2-cycle;
we take the lower-canonical-key member of the cycle):

  Channel = TWIN        if Theta > 0
  Channel = COMPONENT   if Theta == 0 and #components > 1
  Channel = QUOTIENT    if Theta == 0, connected, and Aut(Q_colored) > 1
                         (i.e. all the automorphism comes from permuting
                         the twin-free quotient itself -- here Q==G since
                         Theta==0, so this really means |Aut(G)| > 1 with
                         no twins: a genuinely non-trivial connected,
                         twin-free automorphism)
  Channel = TRIVIAL     if Theta == 0 and |Aut(G)| == 1
  Channel = ALGEBRAIC   flagged separately (see note) when QUOTIENT-channel
                         graphs are additionally regular (candidate SRG-like
                         structure) -- distinguished from generic QUOTIENT
                         because it needs spectral confirmation (Task 5),
                         not claimed automatically here.
"""
import random, json, collections
from z100_core import (random_graph, step, exact_aut, theta, canon_key,
                        num_components)
import networkx as nx

SEED0 = 3141592
NCHAINS_PER_CELL = 25
STEPS = 40


def run_to_attractor(N, M, seed):
    rng = random.Random(seed)
    G = random_graph(N, M, rng)
    keys = []
    graphs = []
    for t in range(STEPS):
        keys.append(canon_key(G))
        graphs.append(G.copy())
        out = step(G, rng, selector="lex")
        G = out[0]
        if out[1] is None:
            return None
    # find period-2 cycle in tail, return the lower-key member
    tail = keys[-8:]
    for p in (1, 2):
        if all(tail[i] == tail[i - p] for i in range(p, len(tail))):
            cyc = graphs[-p:] if p > 0 else [graphs[-1]]
            best = min(cyc, key=lambda g: canon_key(g))
            return best
    return graphs[-1]


def classify(G):
    th, classes = theta(G)
    ncomp = num_components(G)
    a = exact_aut(G)
    is_regular = len(set(d for _, d in G.degree())) == 1
    if th > 0:
        return "TWIN", th, a, ncomp, is_regular
    if ncomp > 1:
        return "COMPONENT", th, a, ncomp, is_regular
    if a > 1:
        return "QUOTIENT" + ("*algebraic-candidate" if is_regular else ""), th, a, ncomp, is_regular
    return "TRIVIAL", th, a, ncomp, is_regular


def main():
    cells = []
    for N in (6, 8, 10, 12):
        maxM = N * (N - 1) // 2
        for frac, label in [(0.2, "sparse"), (0.5, "medium"), (0.8, "dense")]:
            M = max(N - 1, round(frac * maxM))
            if M >= maxM:
                continue
            cells.append((N, M, label))

    results = {}
    for (N, M, label) in cells:
        counts = collections.Counter()
        n_ok = 0
        for c in range(NCHAINS_PER_CELL):
            G = run_to_attractor(N, M, SEED0 + hash((N, M, c)) % 100000)
            if G is None:
                continue
            n_ok += 1
            ch, th, a, ncomp, reg = classify(G)
            counts[ch] += 1
        key = f"N={N},M={M}({label},rho={M/(N*(N-1)/2):.2f})"
        dominant = counts.most_common(1)[0][0] if counts else None
        results[key] = {"n_valid": n_ok, "channel_counts": dict(counts), "dominant": dominant}
        print(key, dict(counts), "-> dominant:", dominant)

    with open("task4_results.json", "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
