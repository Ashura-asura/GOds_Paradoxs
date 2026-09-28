"""
Z100 TASK 2 -- Prove or destroy the twin mechanism.

Candidate theorem (Z35, restated by the Z25->Z100 closure prompt):
  In sparse extremal exchange regimes, Aut jumps are caused PRIMARILY by
  twin-class restructuring, i.e.
      Delta Aut(G) > 0  =>  Delta Theta(G) > 0
  where Theta = sum_i C(|C_i|,2) over twin classes C_i.

Method (per the prompt: find the first counterexample, not a correlation):
  Run the real engine (phase_z25/z25b_engine_v2.py, post-canon-fix) across
  three density regimes (sparse / medium / dense) at several N, many seeds,
  many steps. At every step where Aut(G) increases, check whether Theta
  also increased. Record every counterexample found, not just the rate.
"""
import sys, os, random, itertools, collections, json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'phase_z25'))
import z25b_engine_v2 as eng


def twin_classes(N, edges):
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
    return list(sizes.values())


def theta(N, edges):
    return sum(k * (k - 1) // 2 for k in twin_classes(N, edges))


def run_cell(N, M, seed, steps, p=0.0):
    eng.N = N
    rng = random.Random(seed)
    pairs = list(itertools.combinations(range(N), 2))
    e = frozenset(rng.sample(pairs, M))
    prev_aut = eng.aut_size(e)
    prev_theta = theta(N, e)
    counterexamples = []
    n_jumps = 0
    for t in range(steps):
        e2 = frozenset(eng.T(set(e), p, rng))
        new_aut = eng.aut_size(e2)
        new_theta = theta(N, e2)
        if new_aut > prev_aut:
            n_jumps += 1
            if not (new_theta > prev_theta):
                counterexamples.append(dict(
                    N=N, M=M, seed=seed, t=t,
                    aut_before=prev_aut, aut_after=new_aut,
                    theta_before=prev_theta, theta_after=new_theta,
                    edges_before=sorted(list(e)), edges_after=sorted(list(e2))))
        e, prev_aut, prev_theta = e2, new_aut, new_theta
    return n_jumps, counterexamples


def density_label(N, M):
    maxM = N * (N - 1) // 2
    d = M / maxM
    if d < 0.25:
        return "sparse"
    elif d < 0.5:
        return "medium"
    else:
        return "dense"


def main():
    cells = []
    for N in [8, 10, 12]:
        maxM = N * (N - 1) // 2
        for frac in [0.15, 0.35, 0.60]:
            M = max(N, round(frac * maxM))
            cells.append((N, M))

    report = {}
    all_counterexamples = []
    for N, M in cells:
        label = density_label(N, M)
        total_jumps = 0
        total_ce = 0
        cell_ce = []
        for seed in range(15):
            for p in [0.0, 0.5, 1.0]:
                nj, ce = run_cell(N, M, seed * 100 + int(p * 10), steps=80, p=p)
                total_jumps += nj
                total_ce += len(ce)
                cell_ce.extend(ce)
        key = f"N{N}_M{M}_{label}"
        report[key] = dict(density=label, N=N, M=M,
                            total_aut_jumps=total_jumps,
                            counterexamples_found=total_ce,
                            theorem_holds=(total_ce == 0))
        all_counterexamples.extend(cell_ce[:2])  # keep a couple of examples per cell if any

    print(json.dumps(report, indent=2))
    if all_counterexamples:
        with open("z100_task2_counterexamples.json", "w") as f:
            json.dump(all_counterexamples, f, indent=2)
        print(f"\n{len(all_counterexamples)} counterexample(s) saved to z100_task2_counterexamples.json")
    else:
        print("\nNo counterexamples found in any tested cell.")


if __name__ == "__main__":
    main()
