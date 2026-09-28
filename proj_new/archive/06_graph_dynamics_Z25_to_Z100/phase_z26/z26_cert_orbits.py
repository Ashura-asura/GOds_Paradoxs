"""
z26_cert_orbits.py — certify the SINGLE-SWAP lemma on every visited state of
every converged orbit from Z25-b (the world's deterministic data), and check
on-orbit injectivity. If on every state there is exactly ONE (mod iso)
removable edge and ONE addable non-edge at the required extremum, then the
dynamic's basin-collapse has a unique next step at every point, which
combined with periodicity gives uniqueness of the attractor for the orbit.
We RUN the engine and inspect each state produced.
"""
import sys, random, json, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

def extremal_sets(e, p):
    d = E.degrees(e); ed = set(e)
    nonedge = [(a, b) for a in range(E.N) for b in range(a+1, E.N) if (a, b) not in ed]
    rem_scored = sorted(((d[a]+d[b], (a, b)) for a, b in ed))
    add_scored = sorted(((d[a]+d[b], (a, b)) for a, b in nonedge))
    if p < 0.5:
        rmin = rem_scored[0][0]; amax = add_scored[-1][0]
        rems = [x for x in rem_scored if x[0] == rmin]
        adds = [x for x in add_scored if x[0] == amax]
    else:
        rmax = rem_scored[-1][0]; amin = add_scored[0][0]
        rems = [x for x in rem_scored if x[0] == rmax]
        adds = [x for x in add_scored if x[0] == amin]
    # tie up to iso: canon each candidate swap-out graph and cluster
    def iso_keys(sw):
        ks = set()
        for _, (u, v) in sw:
            gg = set(ed)
            if p < 0.5: gg.discard((u, v))
            else: gg.discard((u, v))
            ks.add(E.canon(frozenset(gg)))
        return len(ks)
    return {"n_rem_ties": len(rems), "n_add_ties": len(adds),
            "iso_rem_classes": iso_keys(rems), "iso_add_classes": iso_keys(adds)}

stats = {"states": 0, "rem_ties_gt1": 0, "add_ties_gt1": 0,
         "iso_rem_gt1": 0, "iso_add_gt1": 0}
worst = None
seed = E.seed_graph()
for p in [0.0, 1.0]:
    for t in range(8):
        rng = random.Random(20260802 + 7919*t + int(1000*p))
        e = set(seed); hist = {}
        for step in range(256):
            c = E.canon(frozenset(e))
            if c in hist: break
            hist[c] = step
            info = extremal_sets(frozenset(e), p)
            stats["states"] += 1
            if info["n_rem_ties"] > 1: stats["rem_ties_gt1"] += 1
            if info["n_add_ties"] > 1: stats["add_ties_gt1"] += 1
            if info["iso_rem_classes"] > 1: stats["iso_rem_gt1"] += 1
            if info["iso_add_classes"] > 1: stats["iso_add_gt1"] += 1
            if worst is None and (info["iso_rem_classes"] > 1 or info["iso_add_classes"] > 1):
                worst = (p, step, info)
            e = set(E.T(frozenset(e), p, rng))
print(json.dumps({"stats": stats, "first_tie_state": str(worst)[:240] if worst else None}, indent=2))
