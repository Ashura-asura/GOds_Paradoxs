"""
Z30 CONTROL — before interpreting Experiment 1-3, verify harness fidelity.

(A) The engine's own T at p=0 with its own RNG protocol must reproduce the
    known Z25-b result: period exactly 2, every seed. If not, the harness
    (not the dynamics) is broken and all Z30 numbers are suspect.

(B) My 'lex' selector from z30_tie_dynamics must be REPLACED by the true
    tie-break: pick rem[0], add[-1] from the FULL sorted (tie-broken) lists,
    exactly as z25b_engine_v2.T does with rng.random() >= p. Check that this
    reproduces period 2 as well (sanity: an off-engine re-implementation
    must match the engine bit-for-bit in periods).
"""
import sys, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

N = E.N
M = 15

def seed_graph(s):
    rng = random.Random(9000 + 97 * s)
    e = set()
    while len(e) < M:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b:
            e.add(tuple(sorted((a, b))))
    return frozenset(e)

# (A) direct engine call, faithfully reproducing z25b main() RNG protocol
periodsA = collections.Counter()
for s in range(40):
    g = seed_graph(s)
    eng_rng = random.Random(20260802 + 7919 * s + 1000 * 0)   # p=0 -> +0
    r = E.run(g, 0.0, eng_rng, max_steps=256)
    periodsA[r["period"] if r["converged"] else "NONCONV"] += 1

# (B) manual re-implementation of the engine's tie-break, raw labeled
def engine_exact_step(e, p, rng):
    edges = set(e)
    d = E.degrees(edges)
    rem = sorted(edges, key=lambda x: (d[x[0]] + d[x[1]], x))
    nonedges = [(a, b) for a in range(N) for b in range(a + 1, N)
                if (a, b) not in edges]
    add = sorted(nonedges, key=lambda x: (d[x[0]] + d[x[1]], x))
    if rng.random() < p:
        eo, ei = rem[-1], add[0]
    else:
        eo, ei = rem[0], add[-1]
    edges.discard(eo); edges.add(ei)
    return frozenset(edges)

def manual_run(seed, p, max_steps=256):
    rng = random.Random(20260802 + 7919)   # arbitrary but FIXED protocol
    e = set(seed); hist = {}
    for t in range(max_steps):
        c = E.canon(frozenset(e))
        if c in hist:
            return t - hist[c]
        hist[c] = t
        e = set(engine_exact_step(frozenset(e), p, rng))
    return "NONCONV"

periodsB = collections.Counter()
for s in range(40):
    periodsB[manual_run(seed_graph(s), 0.0)] += 1

print(json.dumps({"A_engine_own_T_p0": dict(periodsA),
                  "B_manual_lex_fullsort_p0": dict(periodsB)}, indent=2))
