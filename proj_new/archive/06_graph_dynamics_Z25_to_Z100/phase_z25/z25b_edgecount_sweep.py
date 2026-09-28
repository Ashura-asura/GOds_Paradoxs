import sys, json, random, collections
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

def rg(M, s):
    r = random.Random(s)
    e = set()
    while len(e) < M:
        a, b = r.randrange(E.N), r.randrange(E.N)
        if a != b: e.add(tuple(sorted((a, b))))
    return frozenset(e)

out = {}
for label, M in [("M=10 sparse", 10), ("M=15", 15), ("M=35 dense", 35)]:
    cnts = []
    basins = collections.Counter(); ex = {}
    for s in range(6):
        g = rg(M, 555 + s * 131)
        r = E.run(g, 0.0, random.Random(7000 + s), max_steps=256)
        if r["converged"]:
            basins[r["key"]] += 1; ex[r["key"]] = r
    rows = [{k: ex[kk].get(k) for k in ("period","n3","n4","n5","aut","dmin",
            "dmax","ratio_n3_n4","ratio_dmax_dmin")} | {"share": basins[kk]/6}
            for kk, _ in basins.most_common(5)]
    out[label] = dict(n_basins=len(basins), rows=rows)
print(json.dumps(out, indent=2))
