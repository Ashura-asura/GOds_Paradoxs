"""
Z100 Task 6 -- Burnside shell law.

Question: what measure does the extremal dynamics follow?
  (a) uniform labeled:      P(G) proportional to 1            (over labeled graphs)
  (b) uniform quotient:     P(class) proportional to 1         (over iso-classes)
  (c) Aut-weighted:         P(G) proportional to Aut(G)        (over labeled graphs)

Orbit-counting identity to verify independently first (claimed exactly true,
t6 in the existing corpus): for a fixed (N,M), summing 1/|Aut(G)| over ALL
labeled graphs G with that edge count equals the number of isomorphism
classes (Burnside/Cauchy-Frobenius lemma applied to S_N acting on graphs).
This is a textbook fact, not something to take on faith -- verify by brute
force at small N where exhaustive enumeration is feasible, THEN test
whether the actual T-dynamics' visited-state histogram is closer to
uniform-labeled, uniform-class, or Aut-weighted.
"""
import sys, os, itertools, random, collections, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'phase_z25'))
import z25b_engine_v2 as eng


def all_labeled_graphs(N, M):
    pairs = list(itertools.combinations(range(N), 2))
    for combo in itertools.combinations(pairs, M):
        yield frozenset(combo)


def canon_key_bruteforce(N, edges):
    """Exact N! canonical form -- ground truth, independent of eng.canon()."""
    best = None
    for perm in itertools.permutations(range(N)):
        relabeled = frozenset(tuple(sorted((perm[a], perm[b]))) for a, b in edges)
        key = tuple(sorted(relabeled))
        if best is None or key < best:
            best = key
    return best


def verify_burnside_identity(N, M):
    """Correct orbit-counting identity: orbit(G) size = N!/Aut(G) (orbit-
    stabilizer, Stab(G) under S_N relabeling = Aut(G)). So
    sum_G 1/orbit(G) = sum_G Aut(G)/N! = n_classes.
    Equivalently (the repo's t6 'duality' claim): every isomorphism class
    C satisfies sum_{G in C} Aut(G) = N! exactly (constant across classes,
    independent of Aut(G) itself), because |C| = N!/Aut(G) members each
    contributing Aut(G). Check BOTH forms independently."""
    eng.N = N  # BUG FIX: aut_size reads the module-level eng.N; must be set
    # explicitly per call, or it silently reuses whatever N a previous call
    # left behind (caught by the per-class-mass sanity check below).
    graphs = list(all_labeled_graphs(N, M))
    Nfact = 1
    for i in range(1, N + 1):
        Nfact *= i
    classes = collections.defaultdict(list)
    for g in graphs:
        classes[canon_key_bruteforce(N, g)].append(g)
    n_classes = len(classes)

    sum_aut_over_Nfact = sum(eng.aut_size(g) for g in graphs) / Nfact
    identity1_holds = abs(sum_aut_over_Nfact - n_classes) < 1e-9

    per_class_mass = {}
    for key, members in classes.items():
        mass = sum(eng.aut_size(g) for g in members)
        per_class_mass[key] = mass
    all_equal_Nfact = all(abs(m - Nfact) < 1e-9 for m in per_class_mass.values())

    return dict(N=N, M=M, n_labeled=len(graphs), n_classes=n_classes, Nfact=Nfact,
                sum_aut_over_Nfact=sum_aut_over_Nfact,
                identity1_orbit_count_holds=identity1_holds,
                identity2_per_class_mass_equals_Nfact=all_equal_Nfact,
                per_class_masses_sample=dict(list(per_class_mass.items())[:3]))


def empirical_distribution(N, M, steps=4000, seed=0, p=0.0, burn_in=200):
    eng.N = N
    rng = random.Random(seed)
    pairs = list(itertools.combinations(range(N), 2))
    e = frozenset(rng.sample(pairs, M))
    counts = collections.Counter()
    for t in range(steps):
        e = frozenset(eng.T(set(e), p, rng))
        if t >= burn_in:
            counts[canon_key_bruteforce(N, e)] += 1
    return counts


def compare_to_laws(N, M, empirical_counts):
    eng.N = N  # same bug fix as above
    graphs = list(all_labeled_graphs(N, M))
    classes = collections.defaultdict(list)
    for g in graphs:
        classes[canon_key_bruteforce(N, g)].append(g)

    class_aut = {}
    for key, members in classes.items():
        class_aut[key] = eng.aut_size(members[0])

    total_labeled = len(graphs)
    n_classes = len(classes)
    sum_aut_weighted = sum(class_aut[k] for k in classes)

    laws = {}
    for key in classes:
        size = len(classes[key])
        laws.setdefault(key, {})
        laws[key]['uniform_labeled'] = size / total_labeled
        laws[key]['uniform_quotient'] = 1.0 / n_classes
        laws[key]['aut_weighted'] = class_aut[key] / sum_aut_weighted

    total_emp = sum(empirical_counts.values())
    tv = {}
    for law_name in ['uniform_labeled', 'uniform_quotient', 'aut_weighted']:
        tv_dist = 0.0
        seen_classes = set(empirical_counts.keys()) | set(laws.keys())
        for key in seen_classes:
            p_emp = empirical_counts.get(key, 0) / total_emp if total_emp else 0.0
            p_law = laws.get(key, {}).get(law_name, 0.0)
            tv_dist += abs(p_emp - p_law)
        tv[law_name] = tv_dist / 2.0

    top_visited = empirical_counts.most_common(3)
    top_report = [dict(aut=class_aut.get(k, None), visits=v) for k, v in top_visited]

    return dict(n_classes=n_classes, total_labeled=total_labeled,
                tv_distances=tv, top_visited_classes=top_report,
                max_aut_in_atlas=max(class_aut.values()))


def main():
    report = {}

    print("=== Step 1: independent verification of the Burnside orbit identity ===")
    for N, M in [(5, 4), (5, 6), (6, 6), (6, 8)]:
        r = verify_burnside_identity(N, M)
        report[f"identity_N{N}_M{M}"] = r
        print(r)

    print("\n=== Step 2: does the T-dynamics follow uniform-labeled, uniform-quotient, or Aut-weighted? ===")
    for N, M in [(5, 4), (5, 6), (6, 6), (6, 8)]:
        for p in [0.0, 1.0]:
            emp = empirical_distribution(N, M, steps=3000, seed=42, p=p, burn_in=200)
            cmp = compare_to_laws(N, M, emp)
            key = f"dynamics_N{N}_M{M}_p{p}"
            report[key] = cmp
            print(key, cmp['tv_distances'], "top:", cmp['top_visited_classes'])

    def stringify_keys(obj):
        if isinstance(obj, dict):
            return {str(k): stringify_keys(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [stringify_keys(v) for v in obj]
        return obj

    with open("z100_task6_results.json", "w") as f:
        json.dump(stringify_keys(report), f, indent=2, default=str)


if __name__ == "__main__":
    main()
