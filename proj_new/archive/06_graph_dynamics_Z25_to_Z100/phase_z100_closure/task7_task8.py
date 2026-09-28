"""
TASK 7 — SCALING LAW (twin survival vs N at fixed density slices)
TASK 8 — ENDPOINT THEOREM TEST (unique attractor vs finite attractor family)

Task 7 pre-registration:
  For fixed density rho in {0.2, 0.35, 0.5, 0.65, 0.8}, sweep N in
  {6,8,10,12,14} (exact automorphism/enumeration tractable range) and
  measure P(Theta>0 at attractor). Look for a density band where this
  probability visibly falls with N (candidate finite-size signature of
  rho_c(N)). This is NOT a proof of an N->infinity limit -- flagged
  honestly as small-N empirical evidence only (Rule 8: cannot survive a
  minimal counterexample means CLOSE the strong claim, not silently keep
  it).

Task 8 pre-registration:
  H_A: unique maximal-symmetry attractor exists (all chains converge to
       ONE canonical class regardless of seed).
  H_B: finite attractor family, size roughly stable as chain count grows
       (distinct-attractor-count curve saturates rather than growing
       linearly with number of chains run).
  Falsifier for H_A: >1 distinct attractor canonical key observed.
  Test for H_B: run increasing numbers of chains at a fixed cell and track
  cumulative distinct-attractor count; fit whether it is still growing
  near-linearly at the end (no saturation -> H_B not supported either) or
  flattening (supports H_B).
"""
import random, json, collections
from z100_core import random_graph, step, theta, canon_key, exact_aut

SEED0 = 271828


def run_to_attractor_theta(N, M, seed, steps=40):
    rng = random.Random(seed)
    G = random_graph(N, M, rng)
    keys, graphs = [], []
    for t in range(steps):
        keys.append(canon_key(G))
        graphs.append(G.copy())
        out = step(G, rng, selector="lex")
        G = out[0]
        if out[1] is None:
            return None, None
    tail = keys[-8:]
    for p in (1, 2):
        if all(tail[i] == tail[i - p] for i in range(p, len(tail))):
            cyc = graphs[-p:]
            best = min(cyc, key=lambda g: canon_key(g))
            th, _ = theta(best)
            return th, canon_key(best)
    th, _ = theta(graphs[-1])
    return th, canon_key(graphs[-1])


def task7():
    results = {}
    for rho_label, rho in [("sparse_0.2", 0.2), ("lowmed_0.35", 0.35),
                            ("medium_0.5", 0.5), ("medhigh_0.65", 0.65),
                            ("dense_0.8", 0.8)]:
        row = {}
        for N in (6, 8, 10, 12, 14):
            maxM = N * (N - 1) // 2
            M = max(N - 1, min(maxM - 1, round(rho * maxM)))
            n_twin, n_ok = 0, 0
            for c in range(20):
                th, key = run_to_attractor_theta(N, M, SEED0 + hash((N, M, c)) % 99991)
                if th is None:
                    continue
                n_ok += 1
                if th > 0:
                    n_twin += 1
            row[N] = {"M": M, "P_twin": n_twin / n_ok if n_ok else None, "n_ok": n_ok}
        results[rho_label] = row
        print(rho_label, row)
    with open("task7_results.json", "w") as f:
        json.dump(results, f, indent=2)
    return results


def task8():
    N, M = 10, 15
    checkpoints = [10, 25, 50, 100, 150, 200]
    seen = set()
    curve = []
    idx = 0
    for target in checkpoints:
        while idx < target:
            th, key = run_to_attractor_theta(N, M, SEED0 + 777 + idx)
            if key is not None:
                seen.add(key)
            idx += 1
        curve.append({"n_chains": target, "distinct_attractors": len(seen)})
    print("Task8 growth curve:", curve)
    # crude saturation check: compare growth in the last third vs first third
    first = curve[len(curve)//3]["distinct_attractors"]
    last = curve[-1]["distinct_attractors"]
    mid = curve[2*len(curve)//3]["distinct_attractors"]
    growth_rate_early = first / checkpoints[len(curve)//3]
    growth_rate_late = (last - mid) / (checkpoints[-1] - checkpoints[2*len(curve)//3])
    report = {
        "N": N, "M": M,
        "growth_curve": curve,
        "growth_rate_early_distinct_per_chain": growth_rate_early,
        "growth_rate_late_distinct_per_chain": growth_rate_late,
        "H_A_unique_attractor": len(seen) == 1,
        "saturating": growth_rate_late < 0.5 * growth_rate_early,
    }
    if report["H_A_unique_attractor"]:
        verdict = "H_A SURVIVES (unique attractor) -- would be extraordinary, double-check"
    elif report["saturating"]:
        verdict = "H_B SUPPORTED (finite attractor family, growth curve flattening)"
    else:
        verdict = "NEITHER H_A NOR H_B SUPPORTED -- distinct-attractor count still growing near-linearly; no evidence yet of a finite endpoint family at this N,M"
    report["verdict"] = verdict
    print(json.dumps(report, indent=2))
    with open("task8_results.json", "w") as f:
        json.dump(report, f, indent=2)


if __name__ == "__main__":
    task7()
    task8()
