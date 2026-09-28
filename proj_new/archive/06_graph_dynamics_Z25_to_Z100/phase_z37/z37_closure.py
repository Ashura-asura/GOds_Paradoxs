"""Z37+ Formal Closure Program harness.

Pre-registered 2026-08-03 in phase_z37/Z37_PREREGISTRATION.md (Rule-2) before any run.
Tasks:
  t1  tie-collapse theorem formalization (iso-invariance, counterexamples, tau*)
  t2  twin formation probability law (feature MI ranking)
  t3  scaling window (16,32)..(40,80)
  t4  jump partition twin/quotient
  t5  algebraic symmetry activation predictors (zoo + atlas)
  t6  exact Burnside shell law (N=6, N=7 exhaustive)

Conventions identical to Z35: jump = ratio>=4; |Aut| = aut_size_exact_v2 (Amend 3);
Theta = twin_potential; canon = z25b_engine_v2 (EX exact / INV deterministic);
selectors = z33.step_mode with Amendment-4 patch; RNG = SEED0+131*s+991*len(mode).
"""
import sys, time, math, random, json, statistics, itertools, collections
sys.path.insert(0, "phase_z35")
sys.path.insert(0, "phase_z25")
sys.path.insert(0, "phase_z33")

import z25b_engine_v2 as E
import z33_symmetry_drift as Z33
import z35_tie_collapse_theorem as Z
from z32_stationary_vs_burnside import pairs_from_idx

SEED0 = Z.SEED0
JUMP = Z.JUMP_RATIO
RES = r"phase_z37\results"
import os
os.makedirs(RES, exist_ok=True)


def patched():
    import z33_symmetry_drift as _M
    if getattr(_M, "aut_size_exact", None) is not Z.aut_size_exact_v2:
        _M.aut_size_exact = Z.aut_size_exact_v2


def rand_graph(N, M, rng):
    totp = N * (N - 1) // 2
    return frozenset(pairs_from_idx(rng.sample(range(totp), M), N))


def twin_aut(g):
    _, sizes, _ = Z.twin_potential(g)
    ta = 1
    for c in sizes:
        for k in range(2, c + 1):
            ta *= k
    return ta


def rng_for(mode, s):
    return random.Random(SEED0 + 131 * s + 991 * len(mode))


def run_chain(N, M, mode, s, cap, seed=None, collect=None):
    """Generic chain runner. seed = optional starting frozenset. collect = fn(state)->dict.
    Cycle detection uses INV keys (iso-class cycles): EX keys are NOT iso-invariant for
    asymmetric graphs (Rule-8, 2026-08-03), so EX-based tau would be a labeled-state
    revisit time, not an iso-class revisit time."""
    Z.set_N(N)
    rng = rng_for(mode, s)
    e = seed if seed is not None else rand_graph(N, M, rng)
    states = [e]
    keys = [E.invariant_key(e)]
    seen = {keys[0]}
    tau = None
    for t in range(1, cap + 1):
        e = Z33.step_mode(e, mode, rng)
        c = E.invariant_key(e)
        if c in seen:
            tau = t
            break
        seen.add(c)
        states.append(e)
        keys.append(c)
    if tau is None:
        tau = cap
        converged = False
    else:
        converged = True
    return states, keys, tau, converged, rng


# ---------------------------------------------------------------- TASK 1
# Rule-8 discovery 2026-08-03: z25b_engine_v2.canon EX keys are NOT iso-invariant
# (asymmetric graphs: WL classes singleton -> returns own labeling, not the global
# lex-min representative). INV keys ARE iso-invariant (may merge non-iso classes,
# never separates iso classes). Task 1 therefore uses INV keys + nx.is_isomorphic
# ground truth for all iso comparisons; EX-key mismatches on iso pairs are recorded
# separately as canon-bug artifacts, never as counterexamples.
def task1():
    import networkx as nx
    Z.set_N(10)
    out = {"V1": {}, "V2": {}, "V3": {}, "V4": {}}

    # V1: iso-invariance of R,A sets (sorted-edge graphs; INV-free: tau_of is counts)
    bad1 = 0
    for s in range(200):
        g = rand_graph(10, 15, random.Random(SEED0 + s))
        R0, A0 = Z33.tau_of(g)
        rng = random.Random(SEED0 + s)
        for _ in range(3):
            perm = list(range(10))
            rng.shuffle(perm)
            gp = frozenset(tuple(sorted((perm[a], perm[b]))) for a, b in g)
            if Z33.tau_of(gp) != (R0, A0):
                bad1 += 1
    out["V1"] = {"states": 200, "perms": 3, "violations": bad1}

    # V2: lex not well-defined on quotient. Ground truth = nx.is_isomorphic of the
    # two lex successors of an iso pair; EX-key mismatch on ISO successors is the
    # canon bug (recorded, not counted); INV-key mismatch is a sound non-iso witness.
    n_iso = n_ce = n_ex_artifact = n_inv_diff = 0
    ce_example = None
    rng = random.Random(SEED0 + 7)
    for s in range(500):
        g = rand_graph(10, 15, random.Random(SEED0 + 1000 + s))
        gG = nx.Graph(list(g))
        for _ in range(5):
            perm = list(range(10))
            rng.shuffle(perm)
            gp = frozenset(tuple(sorted((perm[a], perm[b]))) for a, b in g)
            if not nx.is_isomorphic(gG, nx.Graph(list(gp))):
                continue
            n_iso += 1
            g2 = Z33.step_mode(g, "lex", rng)
            gp2 = Z33.step_mode(gp, "lex", rng)
            iso_succ = nx.is_isomorphic(nx.Graph(list(g2)), nx.Graph(list(gp2)))
            k1, k2 = E.invariant_key(g2), E.invariant_key(gp2)
            if k1 != k2:
                n_inv_diff += 1
            if not iso_succ:
                n_ce += 1
                if ce_example is None:
                    ce_example = {"g": sorted(g)[:3], "gp": sorted(gp)[:3],
                                  "lex_successor_iso": False}
            else:
                c1, c2 = E.canon(g2), E.canon(gp2)
                if c1 != c2:
                    n_ex_artifact += 1  # canon-bug artifact: iso successors, EX keys differ
    out["V2"] = {"iso_pairs_checked": n_iso, "counterexamples_nx": n_ce,
                 "inv_key_diffs_on_ce": n_inv_diff,
                 "ex_key_artifacts_on_iso_successors": n_ex_artifact,
                 "example": ce_example}

    # tau*: iso-invariant tie-break = argmin INV key over R x A successors
    def step_tau_star(g):
        d = E.degrees(g); ed = set(g)
        ne = [(a, b) for a in range(E.N) for b in range(a + 1, E.N) if (a, b) not in ed]
        ds = lambda x: d[x[0]] + d[x[1]]
        rem = sorted(ed, key=lambda x: (ds(x), x))
        add = sorted(ne, key=lambda x: (ds(x), x))
        scr = ds(rem[0]); sca = ds(add[-1])
        R = [x for x in ed if ds(x) == scr]
        A = [x for x in ne if ds(x) == sca]
        best_key, best_r, best_a = None, None, None
        for rr in R:
            for aa in A:
                g2 = frozenset((set(ed) - {rr}) | {aa})
                k = E.invariant_key(g2)
                if best_key is None or k < best_key:
                    best_key, best_r, best_a = k, rr, aa
        return best_key, best_r, best_a

    # V3: well-definedness of tau* on the quotient (iso pairs -> same INV key)
    n_v3 = n_v3bad = 0
    rng = random.Random(SEED0 + 13)
    for s in range(500):
        g = rand_graph(10, 15, random.Random(SEED0 + 2000 + s))
        gG = nx.Graph(list(g))
        for _ in range(3):
            perm = list(range(10))
            rng.shuffle(perm)
            gp = frozenset(tuple(sorted((perm[a], perm[b]))) for a, b in g)
            if not nx.is_isomorphic(gG, nx.Graph(list(gp))):
                continue
            k1, _, _ = step_tau_star(g)
            k2, _, _ = step_tau_star(gp)
            n_v3 += 1
            if k1 != k2:
                n_v3bad += 1
    out["V3"] = {"iso_pairs": n_v3, "violations": n_v3bad}

    # V4: chains under tau* and under lex (INV-key cycle detection; C-separation)
    def chain_inv(step, seed_g, cap=64):
        seen = {E.invariant_key(seed_g)}
        e = seed_g
        tau = None
        last_k = E.invariant_key(e)
        for t in range(1, cap + 1):
            if step is None:
                e = Z33.step_mode(e, "lex", random.Random(0))
                k = E.invariant_key(e)
            else:
                k, r, a = step(e)
                e = frozenset((set(e) - {r}) | {a})
            last_k = k
            if k in seen:
                tau = t
                break
            seen.add(k)
        if tau is None:
            tau = cap
        return tau, last_k

    taus, ends = [], []
    lex_taus, lex_ends = [], []
    for s in range(200):
        g = rand_graph(10, 15, random.Random(SEED0 + 3000 + s))
        t1, k1 = chain_inv(step_tau_star, g)
        t2, k2 = chain_inv(None, g)
        taus.append(t1); ends.append(k1)
        lex_taus.append(t2); lex_ends.append(k2)
    out["V4"] = {"n_chains": 200, "cap": 64,
                 "median_tau_star": statistics.median(taus),
                 "tau_star_dist": dict(collections.Counter(taus)),
                 "endpoint_support_star": len(set(ends)),
                 "median_tau_lex": statistics.median(lex_taus),
                 "tau_lex_dist": dict(collections.Counter(lex_taus)),
                 "endpoint_support_lex": len(set(lex_ends)),
                 "n_not_converged_star": sum(1 for t in taus if t >= 64),
                 "n_not_converged_lex": sum(1 for t in lex_taus if t >= 64)}
    with open(os.path.join(RES, "t1.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("[t1] V1 violations:", out["V1"]["violations"], "/600")
    print("[t1] V2 counterexamples (nx):", out["V2"]["counterexamples_nx"],
          "of", out["V2"]["iso_pairs_checked"], "iso pairs;",
          "EX artifacts:", out["V2"]["ex_key_artifacts_on_iso_successors"])
    print("[t1] V3 violations:", out["V3"]["violations"], "of", out["V3"]["iso_pairs"])
    print("[t1] V4 median tau*:", out["V4"]["median_tau_star"],
          "support*:", out["V4"]["endpoint_support_star"],
          "| median tau lex:", out["V4"]["median_tau_lex"],
          "support lex:", out["V4"]["endpoint_support_lex"])
    return out


# ---------------------------------------------------------------- TASK 2
def t2_cell(N, M, n_chains, cap):
    Z.set_N(N)
    rows = []
    for s in range(n_chains):
        rng = rng_for("random", s)
        e = rand_graph(N, M, rng)
        th0 = Z.twin_potential(e)[0]
        for t in range(cap):
            d = E.degrees(e); ed = set(e)
            ne = [(a, b) for a in range(N) for b in range(a + 1, N) if (a, b) not in ed]
            ds = lambda x: d[x[0]] + d[x[1]]
            rem = sorted(ed, key=lambda x: (ds(x), x))
            add = sorted(ne, key=lambda x: (ds(x), x))
            scr = ds(rem[0]); sca = ds(add[-1])
            R = [x for x in ed if ds(x) == scr]
            A = [x for x in ne if ds(x) == sca]
            r = rng.choice(R); a = rng.choice(A)
            nb = collections.defaultdict(set)
            for x, y in e:
                nb[x].add(y); nb[y].add(x)
            cn_add = len(nb[a[0]] & nb[a[1]])
            cn_rem = len(nb[r[0]] & nb[r[1]])
            du, dv = d[a[0]], d[a[1]]
            degs = list(d.values())
            degvar = statistics.pvariance(degs) if len(degs) > 1 else 0.0
            e2 = frozenset((set(ed) - {r}) | {a})
            th1 = Z.twin_potential(e2)[0]
            rows.append({"R": len(R), "A": len(A), "FREEDOM": len(R) * len(A),
                         "DEGVAR": degvar, "DU": du, "DV": dv,
                         "CN_ADD": cn_add, "CN_REM": cn_rem, "TH0": th0,
                         "E": 1 if th1 > th0 else 0})
            e = e2
            th0 = th1
    return rows


def hist_bin(vals, nbins=8):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    q = len(vals) // nbins
    lab = [0] * len(vals)
    b = 0
    for i, idx in enumerate(order):
        if i >= (b + 1) * q and b < nbins - 1:
            b += 1
        lab[idx] = b
    return lab


def mi(event, feat, nbins=8):
    n = len(event)
    if n == 0:
        return 0.0
    h = {}
    for e, f in zip(event, feat):
        h[(e, f)] = h.get((e, f), 0) + 1
    pe = collections.Counter(event)
    pf = collections.Counter(feat)
    H_E = -sum((c / n) * math.log2(c / n) for c in pe.values())
    H_F = -sum((c / n) * math.log2(c / n) for c in pf.values())
    H_EF = -sum((c / n) * math.log2(c / n) for c in h.values())
    return H_E + H_F - H_EF


def task2():
    out = {}
    for (N, M, nc, cap) in [(10, 15, 400, 128), (16, 32, 200, 128)]:
        rows = t2_cell(N, M, nc, cap)
        ev = [r["E"] for r in rows]
        n = len(ev)
        H_E = -sum((c / n) * math.log2(c / n) for c in collections.Counter(ev).values())
        feats = ["R", "A", "FREEDOM", "DEGVAR", "DU", "DV", "CN_ADD", "CN_REM", "TH0"]
        mis = {}
        binned = {}
        for f in feats:
            binned[f] = hist_bin([r[f] for r in rows])
            mis[f] = mi(ev, binned[f])
        ranked = sorted(mis.items(), key=lambda kv: -kv[1])
        # greedy forward selection on 2D bins
        sel = [ranked[0][0]]
        gain_hist = []
        cur_joint = mis[sel[0]]
        while len(sel) < len(feats):
            best_gain, best_f, best_joint = -1, None, -1
            for f in feats:
                if f in sel:
                    continue
                joint_bins = [b * 8 + binned[f][i] for i, b in enumerate(binned[sel[0]])]
                for other in sel[1:]:
                    joint_bins = [jb * 8 + binned[other][i] for i, jb in enumerate(joint_bins)]
                j = mi(ev, joint_bins, nbins=8 ** len(sel))
                if j > best_joint:
                    best_joint, best_f = j, f
            gain = best_joint - cur_joint
            gain_hist.append({"feature": best_f, "joint_MI": best_joint, "gain": gain})
            if best_f is None or gain < 0.05 * H_E:
                break
            sel.append(best_f)
            cur_joint = best_joint
        out[f"({N},{M})"] = {"n_steps": n, "P_E": sum(ev) / n, "H_E": H_E,
                             "MI_ranking": ranked, "selected": sel, "gains": gain_hist}
        print(f"[t2] ({N},{M}): P(E)={out[f'({N},{M})']['P_E']:.3f} H_E={H_E:.3f} "
              f"top: {ranked[:3]} selected={sel}")
    with open(os.path.join(RES, "t2.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


# ---------------------------------------------------------------- TASK 3
def task3():
    cells = [(16, 32, 30, 5, 5, 5, 256), (20, 40, 30, 5, 5, 5, 256),
             (24, 48, 25, 4, 4, 3, 256), (30, 60, 20, 3, 3, 2, 192),
             (40, 80, 20, 3, 3, 2, 160)]
    out = {}
    for (N, M, nr, nl, ne2, na, cap) in cells:
        t0 = time.time()
        budgets = {"random": nr, "lex": nl, "entropy": ne2, "autmin": na}
        per = {}
        for mode, nc in budgets.items():
            taus, tnucls, slopes, ends = [], [], [], []
            conv = 0
            for s in range(nc):
                states, keys, tau, converged, _ = run_chain(N, M, mode, s, cap)
                if converged:
                    conv += 1
                else:
                    taus.append(None)
                    continue
                taus.append(tau)
                auts = [Z.aut_size_exact_v2(g) for g in states[:tau]]
                ths = [Z.twin_potential(g)[0] for g in states[:tau]]
                tn = next((i for i in range(len(ths) - 1) if ths[i + 1] > ths[i]), None)
                tnucls.append(tn)
                xs = list(range(len(auts)))
                if len(auts) >= 3:
                    ys = [math.log(max(a, 1)) for a in auts]
                    mx = statistics.mean(xs); my = statistics.mean(ys)
                    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
                    slopes.append(slope)
                ends.append(keys[tau - 1])
            per[mode] = {"n_chains": nc, "converged": conv,
                         "endpoint_keys": ends,
                         "median_tau": statistics.median([t for t in taus if t is not None]) if any(t is not None for t in taus) else None,
                         "median_tnucl": statistics.median([t for t in tnucls if t is not None]) if tnucls else None,
                         "median_slope": statistics.median(slopes) if slopes else None,
                         "endpoint_support": len(set(ends))}
            print(f"[t3] ({N},{M}) {mode}: conv={conv}/{nc} med_tau={per[mode]['median_tau']} "
                  f"med_tnucl={per[mode]['median_tnucl']} med_slope={per[mode]['median_slope']:.4f} "
                  f"support={per[mode]['endpoint_support']}", flush=True)
        # selector divergence: TV between endpoint distributions over selectors
        endd = {m: collections.Counter(per[m]["endpoint_keys"]) for m in per}
        tvs = {}
        for a, b in itertools.combinations(list(per), 2):
            allk = set(endd[a]) | set(endd[b])
            na, nb = sum(endd[a].values()), sum(endd[b].values())
            tvs[f"{a}_vs_{b}"] = round(0.5 * sum(
                abs(endd[a].get(k, 0) / na - endd[b].get(k, 0) / nb) for k in allk), 4)
        out[f"({N},{M})"] = {"per_selector": per, "endpoint_TV": tvs,
                             "wall_s": round(time.time() - t0, 1)}
    with open(os.path.join(RES, "t3.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


# ---------------------------------------------------------------- TASK 4
def task4():
    cells = [(10, 15, 300, 100, 128), (16, 32, 200, 50, 128), (24, 48, 100, 25, 128)]
    out = {}
    for (N, M, nr, nl, cap) in cells:
        Z.set_N(N)
        jumps = []
        violations = 0
        n_states = 0
        for mode, nc in [("random", nr), ("lex", nl)]:
            for s in range(nc):
                states, keys, tau, converged, _ = run_chain(N, M, mode, s, cap)
                auts = [Z.aut_size_exact_v2(g) for g in states]
                tw = [twin_aut(g) for g in states]
                for i in range(len(states) - 1):
                    a0, a1 = auts[i], auts[i + 1]
                    ta0, ta1 = tw[i], tw[i + 1]
                    n_states += 1
                    if ta0 == 0:
                        violations += 1
                        continue
                    if a0 % ta0 != 0 or a1 % ta1 != 0:
                        violations += 1
                        continue
                    if a1 >= JUMP * a0:
                        tf = ta1 / ta0
                        qf = (a1 / a0) / tf
                        if tf >= JUMP:
                            cls = "M" if qf >= JUMP else "T"
                        else:
                            cls = "Q" if qf >= JUMP else "S"
                        jumps.append({"mode": mode, "twin_factor": tf, "q_factor": qf, "class": cls})
        c = collections.Counter(j["class"] for j in jumps)
        n_j = len(jumps)
        out[f"({N},{M})"] = {"n_jumps": n_j, "classes": dict(c),
                             "P_T": c["T"] / n_j, "P_Q": c["Q"] / n_j if n_j else 0,
                             "P_M": c["M"] / n_j, "P_S": c["S"] / n_j,
                             "identity_violations": violations, "n_states_checked": n_states}
        print(f"[t4] ({N},{M}): {n_j} jumps T={c['T']} Q={c['Q']} M={c['M']} S={c['S']} "
              f"violations={violations}", flush=True)
    with open(os.path.join(RES, "t4.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


# ---------------------------------------------------------------- TASK 5
def task5():
    import networkx as nx
    import numpy as np

    def feats(G):
        n = G.number_of_nodes()
        Z.set_N(n)
        mapping = {v: i for i, v in enumerate(G.nodes())}
        G = nx.relabel_nodes(G, mapping)
        g = frozenset(tuple(sorted((u, v))) for u, v in G.edges())
        th = Z.twin_potential(g)[0]
        aut = Z.aut_size_exact_v2(g)
        A = nx.to_numpy_array(G)
        eig = np.linalg.eigvalsh(A)
        eigr = [round(float(x), 6) for x in eig]
        nd = len(set(eigr))
        mxm = max(collections.Counter(eigr).values())
        wl = wl_depth(G)
        is_reg = len(set(d for _, d in G.degree())) == 1
        dia = nx.diameter(G) if nx.is_connected(G) else -1
        girth = None
        try:
            girth = nx.girth(G)
        except Exception:
            girth = None
        dr = is_distance_regular(G)
        lam, mu = cn_concentration(G)
        return {"N": n, "M": G.number_of_edges(), "twin_free": th == 0, "Aut": aut,
                "num_distinct": nd, "max_mult": mxm, "wl_depth": wl, "diameter": dia,
                "girth": girth, "regular": is_reg, "dist_reg": dr,
                "lam_distinct": lam, "mu_distinct": mu}

    def wl_depth(G):
        adj = {v: set(G.neighbors(v)) for v in G}
        color = {v: (len(adj[v]),) for v in G}
        r = 0
        for _ in range(G.number_of_nodes()):
            nc = {v: (color[v], tuple(sorted(color[w] for w in adj[v]))) for v in G}
            uniq = {c: i for i, c in enumerate(sorted(set(nc.values())))}
            nc = {v: uniq[c] for v, c in nc.items()}
            r += 1
            if nc == color:
                break
            color = nc
        return r

    def is_distance_regular(G):
        n = G.number_of_nodes()
        if not nx.is_connected(G):
            return False
        try:
            dist = dict(nx.all_pairs_shortest_path_length(G))
        except Exception:
            return False
        diam = nx.diameter(G)
        for d in range(diam + 1):
            ints = set()
            for u in G:
                for v in G:
                    if u >= v:
                        continue
                    if dist[u].get(v, 10 ** 9) != d:
                        continue
                    i0 = i1 = i2 = 0
                    for w in G.neighbors(u):
                        dd = dist[w].get(v, 10 ** 9)
                        if dd == d - 1:
                            i0 += 1
                        elif dd == d:
                            i1 += 1
                        elif dd == d + 1:
                            i2 += 1
                    ints.add((i0, i1, i2))
            if len(ints) > 1:
                return False
        return True

    def cn_concentration(G):
        lam = set(); mu = set()
        for u, v in itertools.combinations(G.nodes(), 2):
            c = len(set(G.neighbors(u)) & set(G.neighbors(v)))
            if G.has_edge(u, v):
                lam.add(c)
            else:
                mu.add(c)
        return len(lam), len(mu)

    zoo = [
        ("C5", nx.cycle_graph(5)), ("C6", nx.cycle_graph(6)), ("C8", nx.cycle_graph(8)),
        ("C10", nx.cycle_graph(10)),
        ("Petersen", nx.petersen_graph()),
        ("Shrikhande", shrikhande()),
        ("Rook4", rook(4)),
        ("CompShrikh", nx.complement(shrikhande())),
        ("Heawood", heawood()),
        ("Q4", nx.hypercube_graph(4)),
        ("K4,4", nx.complete_bipartite_graph(4, 4)),
        ("K3,3", nx.complete_bipartite_graph(3, 3)),
        ("Rook3", rook(3)),
        ("KG6,2", kneser(6, 2)),
        ("T6", nx.line_graph(nx.complete_graph(6))),
        ("Circulant16(1,3,5)", circulant(16, [1, 3, 5])),
        ("Octahedron", nx.octahedral_graph()),
        ("Icosahedron", nx.icosahedral_graph()),
        ("Dodecahedron", nx.dodecahedral_graph()),
        ("PrismC5K2", nx.circulant_graph(10, [1, 5])),
        ("K5", nx.complete_graph(5)),
    ]
    rows = []
    for name, G in zoo:
        try:
            rows.append({"name": name, **feats(G)})
        except Exception as ex:
            rows.append({"name": name, "error": str(ex)})
    atlas = []
    for i, G in enumerate(nx.graph_atlas_g()):
        if G.number_of_nodes() > 7:
            continue
        try:
            atlas.append({"atlas_index": i, **feats(G)})
        except Exception as ex:
            atlas.append({"atlas_index": i, "error": str(ex)})
    tw_free = [r for r in atlas if "twin_free" in r and r["twin_free"]]
    # rules (only complete rows: atlas entries with errors and zoo errors are excluded)
    def r1(r):
        return not (r["regular"] and r["num_distinct"] <= 3 and r["Aut"] < r["N"])
    def r2(r):
        return not (r["wl_depth"] <= 2 and r["regular"] and r["Aut"] < 2)
    def r3(r):
        return not (r["twin_free"] and r["Aut"] >= 2 and r["num_distinct"] > r["N"] / 2 + 1)
    def complete(r):
        return all(k in r for k in ("regular", "num_distinct", "Aut", "N", "wl_depth", "twin_free"))
    pool = [r for r in tw_free + rows if complete(r)]
    v1 = [r for r in pool if not r1(r)]
    v2 = [r for r in pool if not r2(r)]
    v3 = [r for r in pool if not r3(r)]
    # zoo-only rules (constructed graphs)
    zoo_complete = [r for r in rows if complete(r)]
    z1 = [r for r in zoo_complete if not r1(r)]
    z2 = [r for r in zoo_complete if not r2(r)]
    z3 = [r for r in zoo_complete if not r3(r)]
    out = {"zoo": rows, "atlas": atlas,
           "atlas_counts": {"total": len(atlas), "twin_free": len(tw_free),
                            "twin_free_with_aut_ge2": sum(1 for r in tw_free if r["Aut"] >= 2)},
           "rules_atlas_twinfree": {"R1_violations": len(v1), "R2_violations": len(v2), "R3_violations": len(v3),
                                    "examples": [r["name" if "name" in r else "N"] for r in (v1[:3] + v2[:3] + v3[:3])]},
           "rules_zoo": {"R1_violations": len(z1), "R2_violations": len(z2), "R3_violations": len(z3),
                         "examples": [(r.get("name", "?"), r["Aut"], r["num_distinct"]) for r in (z1[:3] + z2[:3] + z3[:3])]}}
    with open(os.path.join(RES, "t5.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"[t5] zoo {len(rows)} graphs; atlas {len(atlas)} (twin-free {len(tw_free)})")
    print(f"[t5] atlas-twin-free rule violations R1={len(v1)} R2={len(v2)} R3={len(v3)}")
    print(f"[t5] zoo rule violations R1={len(z1)} R2={len(z2)} R3={len(z3)}")
    return out


def shrikhande():
    import networkx as nx
    G = nx.Graph(); G.add_nodes_from(range(16))
    for x in range(4):
        for y in range(4):
            u = (x % 4) * 4 + (y % 4)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]:
                v = ((x + dx) % 4) * 4 + ((y + dy) % 4)
                if u < v:
                    G.add_edge(u, v)
    return G


def rook(k):
    import networkx as nx
    G = nx.Graph(); G.add_nodes_from(range(k * k))
    for x in range(k):
        for y in range(k):
            u = x * k + y
            for x2 in range(k):
                for y2 in range(k):
                    v = x2 * k + y2
                    if u < v and (x == x2 or y == y2):
                        G.add_edge(u, v)
    return G


def heawood():
    import networkx as nx
    G = nx.Graph(); G.add_nodes_from(range(14))
    for i in range(7):
        for j in (1, 2, 4):
            G.add_edge(i, 7 + ((i + j) % 7))
        G.add_edge(i, 7 + i)
    return G


def kneser(n, k):
    import networkx as nx
    sets = list(itertools.combinations(range(n), k))
    G = nx.Graph()
    G.add_nodes_from(range(len(sets)))
    for i in range(len(sets)):
        for j in range(i + 1, len(sets)):
            if not set(sets[i]) & set(sets[j]):
                G.add_edge(i, j)
    return G


def circulant(n, jumps):
    import networkx as nx
    G = nx.Graph(); G.add_nodes_from(range(n))
    for i in range(n):
        for j in jumps:
            G.add_edge(i, (i + j) % n)
    return G


# ---------------------------------------------------------------- TASK 6
# Rule-8 2026-08-03: EX-canon keys are NOT iso-invariant, so orbit identification
# via canon keys is invalid (each labeled graph of an asymmetric class would look
# like its own orbit). Orbit counts are instead computed exactly via Burnside's
# lemma: #orbits(shell) = (1/N!) * sum_{labeled g in shell} |Aut(g)| (exact, no
# canon needed). sigma_q = uniform over orbits, sigma_l = uniform over labeled,
# sigma_a = Aut-weighted labeled = labeled draw weight proportional to |Aut|.
def task6():
    out = {}
    # exhaustive enumeration
    for (N, Ms) in [(6, None), (7, [9, 10, 11])]:
        pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]
        cell_out = {}
        for M in (range(0, len(pairs) + 1) if Ms is None else Ms):
            Z.set_N(N)
            nfac = math.factorial(N)
            per_shell = collections.defaultdict(lambda: [0, 0.0])  # shell -> [n_labeled, sum_aut]
            t0 = time.time()
            cnt = 0
            for comb in itertools.combinations(pairs, M):
                g = frozenset(comb)
                if len(g) == 0:
                    sh = (0, 0)
                elif len(g) == len(pairs):
                    sh = (len(pairs), 0)
                else:
                    sh = Z33.tau_of(g)
                au = Z.aut_size_exact_v2(g)
                per_shell[sh][0] += 1
                per_shell[sh][1] += au
                cnt += 1
            n_lab_total = sum(v[0] for v in per_shell.values())
            n_orb_total = sum(v[1] for v in per_shell.values()) / nfac
            n_aut_total = sum(v[1] for v in per_shell.values())
            keyed = lambda c, n: {f"{k[0]},{k[1]}": round(v / n, 6)
                                  for k, v in sorted(c.items())}
            n_orb_shell = {k: v[1] / nfac for k, v in per_shell.items()}
            cell_out[str(M)] = {"n_labeled": cnt,
                                "n_orbits": round(n_orb_total, 3),
                                "sigma_q": keyed(n_orb_shell, n_orb_total),
                                "sigma_l": keyed({k: v[0] for k, v in per_shell.items()}, n_lab_total),
                                "sigma_a": keyed({k: v[1] for k, v in per_shell.items()}, n_aut_total),
                                "shells": sorted(per_shell.keys()),
                                "mean_aut_by_shell": {f"{k[0]},{k[1]}": round(v[1] / v[0], 3)
                                                      for k, v in sorted(per_shell.items())}}
            print(f"[t6] N={N} M={M}: {cnt} labeled, {round(n_orb_total,1)} orbits "
                  f"({len(per_shell)} shells, {round(time.time() - t0, 1)}s)", flush=True)
        out[f"N{N}"] = cell_out
    # validation: sampled Aut-weighted estimator vs exhaustive truth at (7,10)
    Z.set_N(7)
    n_draws = 20000
    est = collections.Counter()
    rng = random.Random(SEED0 + 77)
    pairs7 = [(a, b) for a in range(7) for b in range(a + 1, 7)]
    for _ in range(n_draws):
        comb = rng.sample(pairs7, 10)
        g = frozenset(comb)
        est[Z33.tau_of(g)] += Z.aut_size_exact_v2(g)
    truth = out["N7"]["10"]["sigma_l"]
    truth_a = out["N7"]["10"]["sigma_a"]
    n_est = sum(est.values())
    tv_a = 0.5 * sum(abs(v / n_est - truth_a.get(f"{k[0]},{k[1]}", 0.0))
                     for k, v in est.items())
    out["validation_N7_M10"] = {"n_draws": n_draws,
                                "TV_sampled_autweighted_vs_exact_sigma_a": round(tv_a, 6)}
    # dynamics at (6,9),(7,10),(7,11)
    dyn = {}
    for (N, M) in [(6, 9), (7, 10), (7, 11)]:
        Z.set_N(N)
        end_shells = collections.Counter()
        end_auts = []
        for s in range(100):
            states, keys, tau, conv, _ = run_chain(N, M, "random", s, 64)
            end_shells[Z33.tau_of(states[-1])] += 1
            end_auts.append(Z.aut_size_exact_v2(states[-1]))
        dyn[f"({N},{M})"] = {"attractor_shell_dist": {f"{k[0]},{k[1]}": v for k, v in sorted(end_shells.items())},
                             "median_end_aut": statistics.median(end_auts)}
        print(f"[t6] dyn ({N},{M}): shell dist {dict(end_shells.most_common(3))} "
              f"med_end_aut={statistics.median(end_auts)}", flush=True)
    out["dynamics"] = dyn
    with open(os.path.join(RES, "t6.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else "t1"
    patched()
    print(f"[z37] task {task} start {time.strftime('%H:%M:%S')}", flush=True)
    t0 = time.time()
    if task == "t1":
        task1()
    elif task == "t2":
        task2()
    elif task == "t3":
        task3()
    elif task == "t4":
        task4()
    elif task == "t5":
        task5()
    elif task == "t6":
        task6()
    print(f"[z37] task {task} done in {round(time.time() - t0, 1)}s", flush=True)
