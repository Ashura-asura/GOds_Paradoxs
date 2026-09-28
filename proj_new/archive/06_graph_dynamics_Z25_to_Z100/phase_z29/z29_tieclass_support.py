"""
Z29 — support characterization: does mu sit exactly on the tie-stable set?

Definitions (p-mode fixed):
  R_set(e) = extremal edges (degree-sum argmin if p=0 ... argmax if p=1)
  A_set(e) = extremal nonedges (argmax if p=0, argmin if p=1)
  tie-class tau(e) = ( sorted canon(e \ r for r in R_set),
                        sorted canon(e + a for a in A_set) )
  T chosen swap = (r*, a*) first elements after the engine's tie-break
  side-conditions for "tau maps into tau(T e)" naturality... Rule-3: we do
  NOT claim an operator on the quotient; canon merges limit tau to a
  per-state invariant. We test a one-step stability predicate instead.

Support-characterization predicates per attractor state g* (min-state of
the converged 2-cycle):
  (P1) |R_set(g*)| == 1              iso-singleton removal (trivially true)
       and |A_set(g*)| == 1          iso-singleton addition
  (P2)  g* is in the image of canon(T(.)) restricted to its own basin:
       canon(T(g_prev)) == canon(g*) where g_prev = the other cycle state
  (P3)  count-distinct-canon of neighbors:
       |{canon(g* - r + a) : r in R_set(g*), a in A_set(g*)}| == 1
       i.e. every extremal rewire lands in the same iso class
       -> the attractor state sees only ONE next move set modulo iso

Conjecture under test (L1):
  P1 or (not P1 but P3) holds for EVERY attractor in the 300-seed support
  at both p=0 and p=1.

If true: the support of mu = all canon-points lying on 2-cycles whose swap
alternates between an iso-unique pair (up to remove-tie-collapse),
closing Phase 2 of the roadmap structurally.
"""
import sys, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

N = E.N
M = 15

def extremal_sets(e, p):
    d = E.degrees(e); ed = set(e)
    nonedge = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in ed]
    rem = sorted((d[a] + d[b], (a, b)) for a, b in ed)
    add = sorted((d[a] + d[b], (a, b)) for a, b in nonedge)
    if p < 0.5:
        sc_r, sc_a = rem[0][0], add[-1][0]
    else:
        sc_r, sc_a = rem[-1][0], add[0][0]
    R = [x for s, x in rem if s == sc_r]
    A = [x for s, x in add if s == sc_a]
    return R, A

def p1_holds(g, p):
    R, A = extremal_sets(g, p)
    return len(R) == 1 and len(A) == 1, len(R), len(A)

def p2_holds(cycle_states, p):
    # g_prev = other state
    a, b = cycle_states
    return E.canon(E.T(frozenset(b), p, random.Random(0))) == E.canon(frozenset(a))

def p3_holds(g, p):
    R, A = extremal_sets(g, p)
    ed = set(g)
    keys = set()
    for r in R:
        for a in A:
            gg = set(ed)
            gg.discard(r)
            gg.add(a)
            keys.add(E.canon(frozenset(gg)))
    return len(keys) == 1, len(keys), len(R) * len(A)

def attractor_cycle(seed_idx, p):
    rng = random.Random(9000 + 97 * seed_idx)
    e = set()
    while len(e) < M:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b:
            e.add(tuple(sorted((a, b))))
    trng = random.Random(7777 + seed_idx)
    hist = {}
    seq = []
    for step in range(256):
        fk = frozenset(e)
        c = E.canon(fk)
        if c in hist:
            return fk, seq[hist[c]:]
        hist[c] = step
        seq.append(fk)
        e = set(E.T(fk, p, trng))
    return fk, seq  # nonconverged

for p in (0.0, 1.0):
    n_att = 0; P1 = P2 = P3 = 0; P13 = 0; worst_p3 = 0
    rem_sizes = collections.Counter(); add_sizes = collections.Counter()
    for s in range(300):
        g, cyc = attractor_cycle(s, p)
        n_att += 1
        h1, lr, la = p1_holds(g, p)
        rem_sizes[lr] += 1; add_sizes[la] += 1
        if h1: P1 += 1
        h3, nk, cand = p3_holds(g, p)
        if h3: P3 += 1
        worst_p3 = max(worst_p3, nk)
        if h1 or h3: P13 += 1
    keys = sorted(rem_sizes)
    keysA = sorted(add_sizes)
    out = dict(p=p, attractors=n_att,
               P1_singleton_swap=P1, P3_one_swapped_class=P3,
               P1_or_P3=P13, coverage=round(P13 / n_att, 4),
               worst_nextclass_count=worst_p3,
               rem_size_hist={str(k): rem_sizes[k] for k in keys},
               add_size_hist={str(k): add_sizes[k] for k in keysA})
    print(json.dumps(out, indent=2))
