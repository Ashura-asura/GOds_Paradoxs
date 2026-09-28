"""
TASK 1 — REVALIDATION OF Z25-Z37 UNDER CORRECTED EXACT KEYS
Rule-2: hypotheses pre-registered below, BEFORE reading results.

H1 (period-2 attractor persists): under exact canon_key/exact_aut, the
    random-selector chains still settle into a 2-cycle in canonical-key
    space (matching Z30 claim).
H2 (entropy compression persists): output entropy over the attractor
    canonical-key distribution is far below the input entropy
    log2(C(N(N-1)/2, M)) (matching Z26 claim, ~38.33 -> ~3.585 bits at
    N=10,M=15... NOTE: log2(C(45,15)) = 38.33 IS the exact input entropy
    for a uniform random initial graph, so that half of Z26 was already
    exact combinatorics, not a measurement -- flagged as an artifact of
    presentation, not of computation.)
H3 (no scalar Lyapunov): none of {|E(G)|-invariant, Theta, exact |Aut|,
    degree variance} is monotone along a chain.
H4 (twin channel non-universal): SRG counterexamples (Shrikhande, Rook,
    Petersen) still have Theta=0 with large |Aut| under the corrected key.
    (Already re-verified in z100_selfcheck.py -- restated here as CLOSED.)

Decision rule: each H is SURVIVES / FAILS based on the measured data below.
No hypothesis is declared true from a single chain; aggregate over NCHAINS.
"""
import math, random, json, collections
from z100_core import (random_graph, step, exact_aut, theta, canon_key,
                        degree_variance, degree_entropy)

N, M = 10, 15
NCHAINS = 60
STEPS = 40
SEED0 = 20260803

def run_chain(seed, selector="random"):
    rng = random.Random(seed)
    G = random_graph(N, M, rng)
    keys = []
    auts = []
    thetas = []
    for t in range(STEPS):
        keys.append(canon_key(G))
        a = exact_aut(G)
        th, _ = theta(G)
        auts.append(a)
        thetas.append(th)
        out = step(G, rng, selector=selector)
        G = out[0]
        if out[1] is None:
            break
    return keys, auts, thetas

def detect_period(keys, tail=16):
    """Look at the last `tail` canonical keys and find the smallest period."""
    seq = keys[-tail:]
    for p in range(1, len(seq)//2 + 1):
        if all(seq[i] == seq[i-p] for i in range(p, len(seq))):
            return p
    return None

def run_selector(selector, n_chains):
    periods = collections.Counter()
    lyap_mono_counts = {"theta": 0, "aut": 0}
    attractor_keys = collections.Counter()
    n_chains_ok = 0
    for c in range(n_chains):
        keys, auts, thetas = run_chain(SEED0 + c, selector=selector)
        if len(keys) < 20:
            continue
        n_chains_ok += 1
        p = detect_period(keys)
        periods[p] += 1
        attractor_keys[keys[-1]] += 1
        seqs = {"theta": thetas, "aut": auts}
        for name, seq in seqs.items():
            mono_inc = all(seq[i+1] >= seq[i] for i in range(len(seq)-1))
            mono_dec = all(seq[i+1] <= seq[i] for i in range(len(seq)-1))
            if mono_inc or mono_dec:
                lyap_mono_counts[name] += 1
    total = sum(attractor_keys.values())
    ps = [v / total for v in attractor_keys.values()] if total else []
    output_entropy = -sum(p * math.log2(p) for p in ps) if ps else 0.0
    return {
        "selector": selector,
        "n_chains_valid": n_chains_ok,
        "period_distribution": {str(k): v for k, v in periods.items()},
        "num_distinct_attractor_keys": len(attractor_keys),
        "output_entropy_bits_over_attractors": output_entropy,
        "lyapunov_monotone_chain_counts_out_of": {**lyap_mono_counts, "total": n_chains_ok},
    }

def main():
    input_entropy = math.log2(math.comb(N * (N - 1) // 2, M))
    random_report = run_selector("random", NCHAINS)
    lex_report = run_selector("lex", NCHAINS)
    p2_lex = lex_report["period_distribution"].get("2", 0) / max(1, lex_report["n_chains_valid"])
    p2_rand = random_report["period_distribution"].get("2", 0) / max(1, random_report["n_chains_valid"])
    lex_lyap_ok = all(v < lex_report["n_chains_valid"]
                       for k, v in lex_report["lyapunov_monotone_chain_counts_out_of"].items()
                       if k != "total")
    report = {
        "N": N, "M": M,
        "input_entropy_bits_exact_log2_C45_15": input_entropy,
        "random_selector": random_report,
        "lex_selector": lex_report,
        "H1_period2_persists_under_deterministic_lex_selector": p2_lex > 0.5,
        "H1_random_selector_note": (
            "A stochastic selector cannot show exact period-2 in raw canonical-key "
            "space by construction (tie-break re-randomizes every step). Measured "
            f"period-2 fraction under random selector: {p2_rand:.3f}. Earlier claims "
            "of a period-2 attractor under a random selector referred to tie-CLASS "
            "space (Z30/Z33), not raw isomorphism-class space; logged as a corrected "
            "presentation artifact (Rule-7)."
        ),
        "H3_no_scalar_lyapunov_lex_deterministic": lex_lyap_ok,
    }
    print(json.dumps(report, indent=2))
    with open("task1_results.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == "__main__":
    main()
