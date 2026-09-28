import sys, json, collections, random
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E
N = E.N

def random_seed_graph(M, s):
    rng = random.Random(s)
    while True:
        e = set()
        while len(e) < M:
            a = rng.randrange(N); b = rng.randrange(N)
            if a != b:
                e.add(tuple(sorted((a, b))))
        fg = frozenset(e)
        d = collections.Counter()
        for a, b in fg:
            d[a] += 1; d[b] += 1
        if len(d) == N and min(d.values()) >= 1:
            return fg

out = {}
for p in (0.0, 1.0):
    basins = collections.Counter(); ex = {}
    nonconv = 0
    for s in range(12):
        g = random_seed_graph(15, 9000 + 97 * s)
        rng = random.Random(20260802 + s)
        r = E.run(g, p, rng, max_steps=256)
        if r["converged"]:
            basins[r["key"]] += 1; ex[r["key"]] = r
        else:
            nonconv += 1
    rows = []
    for key, cnt in basins.most_common(8):
        s0 = ex[key]
        rows.append({k: s0.get(k) for k in ("period", "n3", "n4", "n5", "aut",
                     "dmin", "dmax", "ratio_n3_n4", "ratio_dmax_dmin")} |
                    {"share": cnt / 12})
    out[str(p)] = dict(n_basins=len(basins), nonconverged=nonconv,
                       dominant_share=(basins.most_common(1)[0][1] / 12) if basins else 0,
                       rows=rows)
print(json.dumps(out, indent=2))
