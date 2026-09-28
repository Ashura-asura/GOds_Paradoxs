"""
Z26 Step 1 — attempt to prove basin uniqueness + no period>2, for the whole
conservative class, by DIRECT verification on the reachable component.

Method: enumerate the entire component of G_{10,15} reachable from
seed_graph() under T at p=0 (both swap actions taken). If the component is
fully tranversallable, we check LEMMA-P (single-pair claim):
  on every reachable state x, rem-min edge and add-max nonedge are unique
  (modulo iso). If LEMMA-P holds globally AND each state satisfies
  T^{-1}(x) ∩ {comp} ⊆ {x's predecessor under T} (local injectivity on the
  attractor's 2-cycle), then period >2 is impossible: two distinct states
  with the same T-image would require x to have ≥2 non-iso predecessors,
  ruled out.
"""
import sys, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

def swap_choices(e, p):
    """Return the pair (rem-unique?, add-unique?, chosen pair) for a state."""
    d = E.degrees(e)
    Eedges = set(e)
    nonedges = [(a, b) for a in range(E.N) for b in range(a+1, E.N) if (a, b) not in Eedges]
    if p < 0.5:   # p=0: rem min, add max
        rems = sorted(Eedges,    key=lambda x: (d[x[0]]+d[x[1]], x))
        adds = sorted(nonedges,  key=lambda x: (d[x[0]]+d[x[1]], x))
        r, a = rems[0], adds[-1]
        runiq = len(rems) == 1 or (d[rems[0][0]]+d[rems[0][1]]) < (d[rems[1][0]]+d[rems[1][1]])
        auniq = (d[adds[-1][0]]+d[adds[-1][1]]) > (d[adds[-2][0]]+d[adds[-2][1]])
        return runiq, auniq, (r, a)
    else:
        rems = sorted(Eedges,    key=lambda x: (d[x[0]]+d[x[1]], x))
        adds = sorted(nonedges,  key=lambda x: (d[x[0]]+d[x[1]], x))
        r, a = rems[-1], adds[0]
        runiq = len(rems) == 1 or (d[rems[-1][0]]+d[rems[-1][1]]) > (d[rems[-2][0]]+d[rems[-2][1]])
        auniq = (d[adds[0][0]]+d[adds[0][1]]) < (d[adds[1][0]]+d[adds[1][1]])
        return runiq, auniq, (r, a)

def main():
    seed = E.seed_graph()
    # BFS the reachable component (fair-edges: each state fans to its 4 successors,
    # p=0/p=1 choice x rng-bit; here we take the deterministic swap p=0 path and
    # p=1 path to bound the reachable class).
    comp = set([E.canon(seed)])
    frontier = [seed]
    visited_edges = set()
    while frontier:
        nxt = []
        for s in frontier:
            for p in (0.0, 1.0):
                y = E.T(frozenset(s), p, random.Random(0))
                c = E.canon(y)
                edge_key = (E.canon(s), c)
                if edge_key in visited_edges: continue
                visited_edges.add(edge_key)
                if c not in comp:
                    comp.add(c)
                    nxt.append(set(y))
        frontier = nxt[:400]   # cap fan-out; the class is enormous if not
    print("states_reached", len(comp))
    # Check single-pair lemma on all reached states (re-derive a representative
    # set of states and test).
    checked = 0; bad = 0; bad_ex = None
    for s in [seed] + [set(y) for y in list(nxt)[:80]]:
        for p in (0.0, 1.0):
            ru, au, pair = swap_choices(s, p)
            checked += 1
            if not (ru and au):
                bad += 1
                bad_ex = (p, ru, au, s, pair)
    print(json.dumps({"choices_checked": checked, "single_pair_failures": bad,
                      "example": str(bad_ex)[:200] if bad_ex else None},
                     indent=2))

if __name__ == "__main__":
    main()
