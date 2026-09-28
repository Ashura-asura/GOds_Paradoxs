import sys, random, json
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

def mom2(e): 
    d = E.degrees(e); return sum(v*v for v in d.values())
def tri(e):  return E.k_cycle(e, 3)

rows = {}
for name, p in [("b", 0.0), ("c", 1.0)]:
    rng = random.Random(1000)
    g = set()
    while len(g) < 15:
        a, b = rng.randrange(E.N), rng.randrange(E.N)
        if a != b: g.add(tuple(sorted((a, b))))
    seq = []
    for step in range(12):
        seq.append((mom2(g), tri(g)))
        g = set(E.T(frozenset(g), p, rng))
    rows[name] = seq
print(json.dumps(rows, indent=2))
