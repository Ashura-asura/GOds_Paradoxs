"""
Z33 - SYMMETRY DRIFT LAW
Rule-2 pre-registered (2026-08-02), BEFORE any run:
  cell (N,M), budgets, windows, and all four Outcome A/B/C/D tests are
  fixed below in DECISION. Nothing in DECISION is tuned after output.

Question (from Z32, open): is the high-|Aut| endpoint GENERATIVE (the
exchange rule itself pushes |Aut| up along the transient) or a SEED/basin
artifact (trajectories merely begin near symmetry and the attractor is a
selection of the start)?

Method (transient-respecting, unlike Z32's cycle-only sampling):
  For each selector, run a chain from a uniform-labeled (10,15) seed.
  Stop at first canon-revisit (= cycle entry). Record (R, A, |Aut|) at
  EVERY step t, plus the hit-time tau. Drift quantities use only pairs
  (t -> t+1) with t < tau, i.e. strictly inside the transient; post-cycle
  steps are EXCLUDED from the drift means/medians to avoid survivorship
  bias (a chain that reached its cycle is not counted as "still drifting").

Logged per (selector, t<tau):
    (R_t, A_t, aut_t),  dAut_t = aut_{t+1} - aut_t,  dlog_t = ln(aut_{t+1}/aut_t)
    orbit_t = N! / aut_t

Two known statistical artifacts, both pre-empted:
  * Trap 1 (survivorship): drift per WINDOW uses only steps whose entire
    window precedes tau, and each chain contributes all qualifying steps
    irrespective of length. At (10,15) transients are ~8-15 steps, so the
    t>=30 window is structurally sparse; its emptiness is reported, not
    imputed. This asymmetry is itself part of the A-vs-B reading.
  * Trap 2 (log-scale artifact): |Aut| >= 1 always, so from any aut=1
    state dlog >= 0 trivially; a bounded walk would show E[dlog]>0 with NO
    arithmetic ascent. DECISION reads dlog ONLY as geometric-mean step
    multiplier next to the ARITHMETIC mean and median of dAut; a run with
    E[dlog] >> 0 while E[dAut] <= 0 and median(dAut) <= 0 is labeled the
    boundary-repulsion artifact, not symmetry ascent. In DECISION terms it
    is scored as C, never as A or B.

Canonicalization: canon() is used ONLY to detect cycle entry (set the hit
time tau), exactly as Z25b/Z28-Z32 do. The measured state object is the
LABELED edge-set itself and its exact |Aut| - no WL proxy anywhere.

Drift null model (Outcome C needs a quantitative edge, not a feeling):
  Under a fair random walk on log|Aut| at fixed structure, upward and
  downward steps should be ~symmetric AWAY from boundaries, so the
  sign test for A vs C uses a one-sided binomial on P(dAut > 0) EXCLUDING
  all states with aut_t = 1 (the lower bound). Including boundary states
  would make A trivially true by reflection and is disallowed for the
  sign test (this is the operational form of Trap 2).

DECISION (fixed before runs; any |Aut| handling already validated in Z32):
  A (generative ascent):   for every selector, E[dAut] > 0 AND one-side
       sign test p < 0.05 in EVERY nonempty window AND the log-artifact
       screen (above) does not trigger.
  B (symmetry basin):      E[dAut] > 0 and sign test p < 0.05 in the early
       window, decaying to |E| within noise or sign p >= 0.05 in the
       latest nonempty window, for every selector.
  C (correlated endpoint): sign-median |E[dAut]| within noise in every
       window AND sign test p >= 0.05, OR the Trap-2 screen triggers;
       plus a stated numeric null drift from the boundary-rc corrected
       sign test.
  D (selector-defined flow): any pair of nonempty windows shows opposite
       signs of E[dAut] across selectors, or pairwise sign tests split.
  First satisfied wins; ties logged. All four May be reported as "no
  clean outcome" with the table, per Rule 8.
"""
import sys, math, random, json, collections, statistics
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25")
sys.path.insert(0, r"C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z32")
import z25b_engine_v2 as E
from z32_stationary_vs_burnside import aut_size_exact, pairs_from_idx

CELL_N, CELL_M = 10, 15
NCHAINS = {"random": 200, "lex": 120, "entropy": 120, "autmin": 120}
SEED0 = 20260802
CAP = 512
WINDOWS = [(0, 9), (10, 29), (30, 10 ** 9)]       # early / mid / late
TAU_LABEL = {0: "t=0-9", 1: "t=10-29", 2: "t=30+"}
BIN_P = 0.05                                       # sign-test threshold

def set_N(n):
    E.N = n
    E._MEMO.clear(); E._AUT.clear(); E._KC.clear()

def step_mode(e, mode, rng):
    d = E.degrees(e); ed = set(e)
    ne = [(a, b) for a in range(E.N) for b in range(a + 1, E.N) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    rem = sorted(ed, key=lambda x: (ds(x), x))
    add = sorted(ne, key=lambda x: (ds(x), x))
    scr = ds(rem[0]); sca = ds(add[-1])
    R = [x for x in ed if ds(x) == scr]
    A = [x for x in ne if ds(x) == sca]
    if mode == "random":
        r = rng.choice(R); a = rng.choice(A)
    elif mode == "lex":
        r, a = rem[0], add[-1]
    elif mode == "entropy":
        best = None; bh = -1
        for rr in R:
            for aa in A:
                g = set(ed); g.discard(rr); g.add(aa)
                d2 = E.degrees(g)
                ds2 = lambda x: d2[x[0]] + d2[x[1]]
                ne2 = [(x, y) for x in range(E.N) for y in range(x + 1, E.N) if (x, y) not in g]
                h = sum(1 for x in g if ds2(x) == min(ds2(z) for z in g)) * \
                    sum(1 for x in ne2 if ds2(x) == max(ds2(z) for z in ne2))
                if h > bh or (h == bh and (rr, aa) < best):
                    bh, best = h, (rr, aa)
        r, a = best
    elif mode == "autmin":
        best = None; ba = None
        for rr in R:
            for aa in A:
                g = set(ed); g.discard(rr); g.add(aa)
                au = aut_size_exact(frozenset(g))
                if ba is None or au < ba or (au == ba and (rr, aa) < best):
                    ba, best = au, (rr, aa)
        r, a = best
    g = set(ed); g.discard(r); g.add(a)
    return frozenset(g)

def tau_of(e):
    d = E.degrees(e); ed = set(e)
    ne = [(a, b) for a in range(E.N) for b in range(a + 1, E.N) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    scr = min(ds(x) for x in ed); sca = max(ds(x) for x in ne)
    R = sum(1 for x in ed if ds(x) == scr)
    A = sum(1 for x in ne if ds(x) == sca)
    return R, A

def sign_test_p(k_pos, n):
    # one-sided P(X >= k_pos) for X ~ Bin(n, 0.5), exact in log-space so it
    # does not overflow for large n.  Returns None for n=0.
    if n == 0:
        return None
    from math import comb, log
    terms = [comb(n, i) for i in range(k_pos, n + 1)]
    m = max(terms)
    return math.exp(log(sum(t / m for t in terms)) + log(m) - n * log(2.0))

def window_of(t):
    for i, (lo, hi) in enumerate(WINDOWS):
        if lo <= t <= hi:
            return i
    return None

def main():
    set_N(CELL_N)
    out = {"cell": [CELL_N, CELL_M], "cap": CAP,
           "windows": [f"{lo}-{hi if hi < 10**9 else 'end'}" for lo, hi in WINDOWS],
           "bin_p": BIN_P,
           "note": "drift uses only t < tau (pre-cycle); boundary aut=1 "
                   "states excluded from sign tests (Trap-2 operationalization)"}
    per_mode = {}
    for mode in ("random", "lex", "entropy", "autmin"):
        rng_master = random.Random(SEED0 + 97 * len(mode))
        # per-(R,A) conditional drift: (R,A) -> list of dAut (t<tau pairs)
        cond = collections.defaultdict(list)
        # per-window lists
        win_d = [[] for _ in WINDOWS]        # dAut
        win_dl = [[] for _ in WINDOWS]       # dlog
        win_pos = [0] * len(WINDOWS)         # sign-test counts, aut_t>1 only
        win_nsig = [0] * len(WINDOWS)
        win_orbit = [[] for _ in WINDOWS]
        taus = []
        start_auts = []
        end_auts = []                        # aut at tau-1 (last transient)
        n_conv = 0
        for s in range(NCHAINS[mode]):
            rng = random.Random(SEED0 + 131 * s + len(mode) * 7919)
            totp = CELL_N * (CELL_N - 1) // 2
            e = pairs_from_idx(rng.sample(range(totp), CELL_M), CELL_N)
            aut_prev = aut_size_exact(e)
            prev_state = e
            seen = {E.canon(e)}
            tau = None
            states = [(e, aut_prev)]
            for t in range(1, CAP):
                e = step_mode(e, mode, rng)
                c = E.canon(e)
                aut_cur = aut_size_exact(e)
                if c in seen:
                    tau = t
                    break
                seen.add(c)
                states.append((e, aut_cur))
                aut_prev = aut_cur
            if tau is None:
                continue
            n_conv += 1
            taus.append(tau)
            start_auts.append(states[0][1])
            end_auts.append(states[-1][1])
            # drift pairs, strictly inside transient (i -> i+1, i+1 <= tau-1)
            for i in range(len(states) - 1):
                t = i
                st_t, aut_t = states[i]
                st_n, aut_n = states[i + 1]
                w = window_of(t)
                d = aut_n - aut_t
                dl = math.log(aut_n / aut_t)
                cond[tau_of(st_t)].append(d)
                if w is not None:
                    win_d[w].append(d)
                    win_dl[w].append(dl)
                    win_orbit[w].append(math.factorial(CELL_N) / aut_t)
                    if aut_t > 1:
                        win_nsig[w] += 1
                        if d > 0:
                            win_pos[w] += 1
        per_mode[mode] = dict(
            converged=f"{n_conv}/{NCHAINS[mode]}",
            tau_median=statistics.median(taus) if taus else None,
            tau_range=[min(taus), max(taus)] if taus else None,
            start_aut_median=statistics.median(start_auts) if start_auts else None,
            end_transient_aut_median=statistics.median(end_auts) if end_auts else None,
            fold_change_transient=round(
                statistics.median(end_auts) / statistics.median(start_auts), 2)
                if start_auts and end_auts else None,
            windows={}
        )
        for w in range(len(WINDOWS)):
            d = win_d[w]; dl = win_dl[w]
            if not d:
                per_mode[mode]["windows"][TAU_LABEL[w]] = dict(n=0)
                continue
            npos = sum(1 for x in d if x > 0)
            nneg = sum(1 for x in d if x < 0)
            pval = sign_test_p(win_pos[w], win_nsig[w])
            per_mode[mode]["windows"][TAU_LABEL[w]] = dict(
                n=len(d),
                mean_dAut=round(sum(d) / len(d), 4),
                median_dAut=statistics.median(d),
                frac_pos=round(npos / len(d), 4),
                frac_neg=round(nneg / len(d), 4),
                mean_dlog=round(sum(dl) / len(dl), 6),
                geomean_step_mult=round(math.exp(sum(dl) / len(dl)), 5),
                median_orbit=round(statistics.median(win_orbit[w]), 1),
                sign_test_p_excl_boundary=(round(pval, 4) if pval is not None else None),
                n_for_sign=win_nsig[w],
            )
        # conditional drift by (R,A) shell, top shells by sample count
        cond_summ = []
        for shell, ds in sorted(cond.items(), key=lambda kv: -len(kv[1]))[:8]:
            if len(ds) >= 10:
                cond_summ.append(dict(
                    shell=list(shell), n=len(ds),
                    mean_dAut=round(sum(ds) / len(ds), 4),
                    frac_pos=round(sum(1 for x in ds if x > 0) / len(ds), 4)))
        per_mode[mode]["cond_drift_top_shells"] = cond_summ
        print(f"[z33] {mode:7s} conv={n_conv}/{NCHAINS[mode]} "
              f"tau~{per_mode[mode]['tau_median']} steps "
              f"|Aut| start={per_mode[mode]['start_aut_median']} "
              f"-> end_transient={per_mode[mode]['end_transient_aut_median']} "
              f"(x{per_mode[mode]['fold_change_transient']})", flush=True)
    out["per_mode"] = per_mode
    print("Z33_RESULT", json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
