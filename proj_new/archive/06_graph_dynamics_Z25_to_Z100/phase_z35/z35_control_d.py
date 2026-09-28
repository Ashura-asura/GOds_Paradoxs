"""Z35 Control D — twin-free algebraic seeds in the exact-|Aut| jump framework.

Pre-registered 2026-08-03 (Rule-2) in phase_z35/z35_control_d.md BEFORE any run:

Seeds (fixed, Theta=0, |Aut| exact): shrikhande(16,48)=192, rook(16,48)=1152,
comp_shrikh(16,72)=192, petersen(10,15)=120.
Selectors: random 50 chains/seed; lex/entropy/autmin 1 chain/seed (deterministic).
Cap 256 steps; jump = a1 >= 4*a0; |Aut| via Amendment-3 v2 counter, EX-key SQLite cache;
Amendment-4 patch applied (z33 autmin -> v2 counter, identical values -> identical chains).

Gates (decided before runs):
  G1: P(jump at first step t=0 | all chains) <= 0.05
  G2: P(any step with jump and dtheta <= 0) <= 0.05
  G3/G4: measurements (tau_first twin creation, tau_half decay, endpoints).
"""
import sys, time, math, random, json, statistics
sys.path.insert(0, "phase_z35")
sys.path.insert(0, "phase_z25")
sys.path.insert(0, "phase_z33")

import z25b_engine_v2 as E
import z33_symmetry_drift as Z33
from z32_stationary_vs_burnside import pairs_from_idx
import z35_tie_collapse_theorem as Z

SEED0 = Z.SEED0
CAP_D = 256
JUMP_RATIO = Z.JUMP_RATIO
OUT = r"phase_z35\z35_control_d_results.json"


def build_seeds():
    seeds = {}
    # Shrikhande SRG(16,6,2,2)
    edges = set()
    for x in range(4):
        for y in range(4):
            u = (x % 4) * 4 + (y % 4)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]:
                v = ((x + dx) % 4) * 4 + ((y + dy) % 4)
                if u < v:
                    edges.add((u, v))
    seeds["shrikhande"] = frozenset(edges)
    # Rook 4x4 (16,48)
    edges = set()
    for x in range(4):
        for y in range(4):
            u = x * 4 + y
            for x2 in range(4):
                for y2 in range(4):
                    v = x2 * 4 + y2
                    if u < v and (x == x2 or y == y2):
                        edges.add((u, v))
    seeds["rook"] = frozenset(edges)
    # Complement of Shrikhande (16,72)
    sh = seeds["shrikhande"]
    allp = frozenset((a, b) for a in range(16) for b in range(a + 1, 16))
    seeds["comp_shrikh"] = frozenset(allp - sh)
    # Petersen (10,15)
    pe = set()
    for i in range(5):
        pe.add((i, (i + 1) % 5))
        pe.add((5 + i, 5 + ((i + 2) % 5)))
        pe.add((i, 5 + i))
    seeds["petersen"] = frozenset(pe)
    return seeds


def run_chains(seed_g, N, seed_name, rng_seed_base):
    Z.set_N(N)
    out_chains = []
    modes = [("random", 50), ("lex", 1), ("entropy", 1), ("autmin", 1)]
    seed_idx = {"shrikhande": 1, "rook": 2, "comp_shrikh": 3, "petersen": 4}
    for mode, nch in modes:
        for s in range(nch):
            rng = random.Random(SEED0 + 131 * s + 991 * len(mode) + 57 * seed_idx[seed_name])
            e = seed_g
            th0_seed, _, _ = Z.twin_potential(e)
            assert th0_seed == 0, f"{seed_name}: seed Theta != 0"
            a0_seed = Z.aut_size_exact_v2(e)
            states = [e]
            keys = [E.canon(e)]
            seen = {keys[0]}
            tau = None
            for t in range(1, CAP_D):
                e = Z33.step_mode(e, mode, rng)
                c = E.canon(e)
                if c in seen:
                    tau = t
                    break
                seen.add(c)
                states.append(e)
                keys.append(c)
            if tau is None:
                tau = CAP_D  # capped
            auts = []
            for k in range(len(states)):
                auts.append(Z.aut_size_exact_v2(states[k]))
            th_traj = [Z.twin_potential(g)[0] for g in states]
            steps = []
            for i in range(len(states) - 1):
                a0, a1 = auts[i], auts[i + 1]
                th0, th1 = th_traj[i], th_traj[i + 1]
                steps.append({
                    "t": i, "aut0": a0, "aut1": a1,
                    "jump": a1 >= JUMP_RATIO * a0,
                    "theta0": th0, "theta1": th1, "dtheta": th1 - th0,
                })
            tau_first = next((st["t"] + 1 for st in steps if st["theta1"] > 0), None)
            tau_half = next((st["t"] for st in steps if st["aut1"] <= a0_seed / 2), None)
            out_chains.append({
                "seed": seed_name, "mode": mode, "s": s,
                "tau": tau, "capped": tau >= CAP_D,
                "seed_aut": a0_seed, "end_aut": auts[-1],
                "min_aut": min(auts),
                "any_aut1": any(a == 1 for a in auts),
                "end_theta": th_traj[-1],
                "any_theta_gt0": any(th > 0 for th in th_traj[1:]),
                "tau_first_theta": tau_first,
                "tau_half": tau_half,
                "n_jumps": sum(1 for st in steps if st["jump"]),
                "steps": steps,
            })
    return out_chains


def main():
    t0 = time.time()
    import z33_symmetry_drift as _M
    if getattr(_M, "aut_size_exact", None) is not Z.aut_size_exact_v2:
        _M.aut_size_exact = Z.aut_size_exact_v2
        print("[ctrlD] Amendment 4 applied (autmin -> v2, exact, chains unchanged)")
    seeds = build_seeds()
    expected = {"shrikhande": (16, 192), "rook": (16, 1152),
                "comp_shrikh": (16, 192), "petersen": (10, 120)}
    all_chains = []
    for name, g in seeds.items():
        N, aut_exp = expected[name]
        Z.set_N(N)
        a0 = Z.aut_size_exact_v2(g)
        th0 = Z.twin_potential(g)[0]
        print(f"[ctrlD] seed {name:12s} N={N} M={len(g)} |Aut|={a0} (exp {aut_exp}) Theta={th0}", flush=True)
        assert a0 == aut_exp and th0 == 0
        chains = run_chains(g, N, name, 0)
        all_chains.extend(chains)
        n_conv = sum(1 for c in chains if not c["capped"])
        print(f"[ctrlD]   {name}: {len(chains)} chains, {n_conv} converged", flush=True)

    steps_all = [st for c in all_chains for st in c["steps"]]
    n0 = len(all_chains)
    j0 = [c["steps"][0] for c in all_chains if c["steps"]]
    p_jump_t0 = sum(1 for st in j0 if st["jump"]) / len(j0) if j0 else 0.0
    jumps = [st for st in steps_all if st["jump"]]
    n_jumps = len(jumps)
    p_jump_dtheta_le0 = sum(1 for st in jumps if st["dtheta"] <= 0) / n_jumps if n_jumps else 0.0
    tf = [c["tau_first_theta"] for c in all_chains if c["tau_first_theta"] is not None]
    th = [c["tau_half"] for c in all_chains if c["tau_half"] is not None]
    med = lambda xs: statistics.median(xs) if xs else None
    agg = {
        "n_chains": n0, "n_steps": len(steps_all), "n_jumps": n_jumps,
        "P_jump_t0": p_jump_t0,
        "P_jump_dtheta_le0": p_jump_dtheta_le0,
        "P_any_jump": sum(1 for c in all_chains if c["n_jumps"] > 0) / n0,
        "P_any_theta_gt0": sum(1 for c in all_chains if c["any_theta_gt0"]) / n0,
        "P_end_theta0": sum(1 for c in all_chains if c["end_theta"] == 0) / n0,
        "P_any_aut1": sum(1 for c in all_chains if c["any_aut1"]) / n0,
        "median_tau_first_theta": med(tf),
        "tau_first_theta_dist": sorted(tf)[:10],
        "median_tau_half": med(th),
        "tau_half_dist": sorted(th)[:10],
        "end_aut_median": med([c["end_aut"] for c in all_chains]),
        "end_aut_dist": sorted([c["end_aut"] for c in all_chains])[:12],
        "min_aut_median": med([c["min_aut"] for c in all_chains]),
        "tau_median": med([c["tau"] for c in all_chains]),
        "G1_pass": p_jump_t0 <= 0.05,
        "G2_pass": (n_jumps == 0) or (p_jump_dtheta_le0 <= 0.05),
        "wall_s": round(time.time() - t0, 1),
    }
    out = {"protocol": "z35_control_d.md", "cap": CAP_D, "jump_ratio": JUMP_RATIO,
           "seeds": {n: {"N": expected[n][0], "Aut": expected[n][1]} for n in seeds},
           "aggregates": agg, "chains": all_chains}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print("[ctrlD] G1:", "PASS" if agg["G1_pass"] else "FAIL",
          "P(jump t=0) =", p_jump_t0)
    print("[ctrlD] G2:", "PASS" if agg["G2_pass"] else "FAIL",
          "P(jump & dtheta<=0) =", p_jump_dtheta_le0, f"({n_jumps} jumps)")
    print("[ctrlD] median tau_first_theta:", med(tf), "| median tau_half:", med(th),
          "| P(any theta>0):", agg["P_any_theta_gt0"], "| P(end theta=0):", agg["P_end_theta0"])
    print(f"[ctrlD] saved {OUT} | wall {agg['wall_s']}s")


if __name__ == "__main__":
    main()
