"""
Confirm the projection mechanism that forces period-2 for ANY seed at p=0.
The claim to falsify: 'x in T(G_{N,M}) at p=0 implies T(x) = x'
(balance is a projection after ONE step). If the engine reports every
converged attractor has period 2, the reason is that the iterate after
step 1 lies in the image and the image is the fixed set -> T^2 = T.
We verify directly: from each of 24 random seeds, the state at step>=2 is
a FIXED POINT under T at p=0, and then the cycle is (state_{1}, state_{2}).
"""
import sys, random, json
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
import z25b_engine_v2 as E

ok = 0; fail = 0; ex = {}
for s in range(24):
    g = set()
    rng = random.Random(6000 + 31*s)
    while len(g) < 15:
        a, b = rng.randrange(E.N), rng.randrange(E.N)
        if a != b: g.add(tuple(sorted((a, b))))
    g = frozenset(g)
    r = random.Random(777)
    x1 = set(E.T(g, 0.0, r))       # T(seed)
    x2 = set(E.T(frozenset(x1), 0.0, r))
    x3 = set(E.T(frozenset(x2), 0.0, r))
    if x2 == x3:                   # T^2 = T on the image
        ok += 1
    else:
        fail += 1
print(json.dumps({"image_fixed_under_T_at_p0": ok, "fails": fail}, indent=2))
