import json, sys
sys.path.insert(0, 'phase_z35')
import z35_tie_collapse_theorem as Z

src = open(r'phase_z36\z36_experiment.py', encoding='utf-8').read()
src = src.split('# --- Run ---')[0]
ns = {}
exec(compile(src, 'z36_experiment_prologue', 'exec'), ns)
build_attractor_graphs = ns['build_attractor_graphs']

def to_fs(G):
    return frozenset(tuple(sorted((u, v))) for u, v in G.edges())

res = json.load(open(r'phase_z36\z36_results.json'))
ref = {r['name']: r for r in res}

attr = build_attractor_graphs(num=15, N=10, M=15, steps=200)
print(f'regenerated {len(attr)} attractors')
fails = 0
for i, G in enumerate(attr):
    Z.set_N(G.number_of_nodes())
    g = to_fs(G)
    th, sizes, _ = Z.twin_potential(g)
    twin_aut = 1
    for c in sizes:
        for k in range(2, c + 1):
            twin_aut *= k
    aut = Z.aut_size_exact_v2(g)
    r = ref[f'Z25b_attractor_{i}']
    ok_aut = aut == r['Aut_exact']
    ok_th = th == r['Theta']
    ok_ta = twin_aut == r['twin_aut']
    qid = aut % twin_aut == 0 and (aut // twin_aut) == r['quotient_aut_colored'] if r['quotient_aut_colored'] != 1 or r['quotient_N'] <= 12 else aut % twin_aut == 0
    status = 'PASS' if (ok_aut and ok_th and ok_ta) else 'FAIL'
    if status == 'FAIL':
        fails += 1
    print(f'  {status} attractor_{i:2d}: v2_Aut={aut} vs json={r["Aut_exact"]} | v2_Theta={th} vs json={r["Theta"]} | v2_twin_aut={twin_aut} vs json={r["twin_aut"]} | Aut/twin={aut//twin_aut} vs q_colored={r["quotient_aut_colored"]}')
print(f'\nRESULT: {len(attr)-fails}/{len(attr)} attractors fully consistent across tools')
