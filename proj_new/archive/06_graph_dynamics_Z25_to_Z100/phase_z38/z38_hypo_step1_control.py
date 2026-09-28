"""
Z38 CONTROL — Rule 9 check on T1 (purposed_hypo_mechanism.md, GROUND_RULES.md
Rule 9: "would this mechanism explain a wrong answer just as well?").

z38_hypo_step1.py found T1 (H_token/H_move < 0.8) PASSES at ratio ~0.41-0.45,
100% of runs, both tested cells. Before that counts as evidence of "codified
space," this control asks: does a rule with NO extremal/deterministic
structure at all -- pure uniform-random edge exchange -- pass the same gate?
If yes, T1 has zero discriminating power (Rule 9 fails) and the low ratio is
just H_token/H_move's normalization, not a property of the dynamics.
"""
import random, itertools, math, collections, json, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'phase_z25'))
import z25b_engine_v2 as eng
from z38_hypo_step1 import twin_classes, cands, shannon, measure


def T_random(edges, N, rng):
    """Null model: uniform-random edge removed, uniform-random non-edge added.
    No degree-sum extremization, no p-selector -- the opposite of eng.T."""
    edges = set(edges)
    e_out = rng.choice(list(edges))
    nonedges = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in edges]
    e_in = rng.choice(nonedges)
    edges.discard(e_out); edges.add(e_in)
    return frozenset(edges)


def run_tokens_random(N, M, seed, steps=120):
    rng = random.Random(seed)
    pairs = list(itertools.combinations(range(N), 2))
    e = frozenset(rng.sample(pairs, M))
    tokens, jump, exbits, shells = [], [], [], []
    prev = None
    for _ in range(steps):
        sig = twin_classes(N, e)
        tokens.append(sig)
        R, A, rc, ac = cands(e, N)
        shells.append((R, A))
        ex = rc * ac
        exbits.append(math.log2(ex) if ex > 0 else 0.0)
        jump.append(1 if prev is not None and sig != prev else 0)
        prev = sig
        e = T_random(e, N, rng)
    return tokens, jump, exbits, shells


def main():
    results = {}
    for N, M in [(10, 15), (12, 18)]:
        runs = []
        for s in range(24):
            r = run_tokens_random(N, M, 2000 + 7 * s, 120)
            m = measure(r)
            if m is not None:
                Htok, Hmov, ratio, ok, nj, dtok = m
                runs.append(dict(seed=s, H_token=Htok, H_move=Hmov,
                                  ratio=ratio, T1_pass=ok, n_jump=nj,
                                  distinct_tokens=dtok))
        passes = sum(1 for r in runs if r["T1_pass"])
        Ht = sum(r["H_token"] for r in runs) / len(runs)
        Hm = sum(r["H_move"] for r in runs) / len(runs)
        results[f"{N}_{M}"] = dict(runs=len(runs),
                                    T1_pass_share=(passes / len(runs)) if runs else 0.0,
                                    pass_count=passes,
                                    H_token_mean=Ht, H_move_mean=Hm,
                                    ratio_mean=(Ht / Hm if Hm else 0.0))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
