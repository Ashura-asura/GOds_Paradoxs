"""
Z35 - TIE-COLLAPSE MECHANISM: FROM EMPIRICAL LAW TO STRUCTURAL THEOREM
Rule-2 pre-registered (2026-08-02), BEFORE any run. Nothing in DECISION is
tuned after output. Bugs recorded, not hidden (Rule 8).

Question (from Z34, open): WHY does extremal exchange create twin
structures? Z34 showed |Aut| jumps = twin-class restructuring events,
gated by sparse (R,A) tie shells. Z35 defines the twin potential

    Theta(G) = sum_i C(|C_i|, 2)

over twin classes C_i (u,v twins iff identical neighborhoods), and asks
whether Theta is (H1) a reliable pre-jump observable, (H2) more predictive
of jumps than the (R,A) tie shell, (H3) tightly coupled to |Aut| growth,
and whether it is (MONO) a hidden invariant.

DEFINITIONS (fixed):
  * transient = steps t < tau, tau = first canon-revisit (Z33/Z34 protocol)
  * jump J: step (g0 -> g1) with aut(g1) >= 4 * aut(g0)   [Z34 threshold]
  * Theta-bins (fixed): 0,1,2,3,4,5-9,10+
  * tau-shell = joint (R,A) from tau_of() (Z33)

HYPOTHESES + DECISION RULES (fixed before runs):
  H1 (twin potential rises on jumps): P(dTheta>0 | J) >= 0.9 in EVERY
     selector -> pass. Reject if P(dTheta>0 | J) < 0.5 in any selector
     (prompt's rejection threshold).
  H2 (Theta more predictive than tie shell): on pooled steps,
     I(J; Theta_bin) > I(J; tau) AND I(J; Theta | tau) > I(J; tau | Theta)
     -> pass; and no mode shows the strictly reversed ordering.
  H3 (Aut is a readout): Spearman rho(dTheta, log(aut1/aut0)) >= 0.7 in
     every selector -> pass.
  MONOTONICITY: near-monotone iff P(dTheta<0) <= 0.02 in EVERY selector
     (transient steps only); chain-level frac with any dTheta<0 reported.

  CONTROLS (adversarial, Rule 4):
    A  degree-preserving null: per sampled state (every 3rd transient
       step of main-cell chains), 30 double-edge rewires + 10
       configuration-model graphs with the SAME degree sequence.
       Rule-intrinsic iff extremal per-step P(dTheta>0) >= 3 * max(null
       per-attempt positive rates).
    B  reversed extremal rule (remove max-ds edge, add min-ds non-edge,
       random within extremal sets): 300 chains. Kills twin growth iff
       P(dTheta>0) <= 0.1 AND P(dTheta<0) >= 0.3.
    C  canon-independence: (C1) 300 random chains, fixed 40 steps, ZERO
       canon() calls -> no-canon P(dTheta>0) must be >= 0.9 * the
       canon-stopped random-mode rate; (C2) deterministic modes run with
       canon-relabel at every step (EX keys only; INV -> keep state) ->
       collapse must not inflate twins: P_C2(dTheta>0) <= P_raw + 0.01
       per mode.

  DECISION TABLE (fixed):
    A (hidden invariant):     H1 pass AND near-monotone AND B passes
    B (stochastic nucleation):H1 pass AND (H2 or H3 pass) AND not A
    C (Z34 was correlation):  H1 rejected, or neither H2 nor H3 passes

CELLS:
  (10,15) full: random 500, lex 200, entropy 200, autmin 200
  (8,12):       random 200, lex/entropy/autmin 100
  (12,20):      random 200, lex/entropy 100, autmin 80
  (14,28):      random 200, lex/entropy 100, autmin 50
  (16,32):      random 200, lex/entropy 100, autmin 50

AMENDMENT 1 (pre-registration fix, 2026-08-02, declared BEFORE the
(12,20)/(14,28)/(16,32) cells ran; the (10,15) main cell and the (8,12)
cell ran at their ORIGINAL budgets):
  Cause: the exact-|Aut| counter (Z32) costs ~0.5-2s per call on
  high-symmetry transient-end states at N>=12 (benchmark: one (12,20)
  state with |Aut|=362880 = 9! took 1.78s to count; transients are short
  (tau ~ 12) but each chain pays 1-2 such calls). At the original
  budgets the N>=12 cells would take 1-2 hours of wall time.
  Fix (budget-only amendment; NO decision threshold, hypothesis, or
  observable definition changes): N>=12 cell chain budgets reduced to
    (12,20): random 80, lex/entropy 40, autmin 20
    (14,28): random 50, lex/entropy 25, autmin 12
    (16,32): random 50, lex/entropy 25, autmin 12
  The generalization question is qualitative (does the mechanism
  survive), and the decisive cell (10,15) keeps its full budget.

AMENDMENT 2 (harness optimization only, 2026-08-02, declared BEFORE the
(12,20)/(14,28)/(16,32) cells ran; NO statistical change - all exact
counters, thresholds, and pre-registered decisions are untouched):
  Target hardware: i7-1165G7 (4C/8T mobile), 16GB RAM.
  1. |Aut| is computed ONCE per state and carried forward (previously
     computed twice per adjacent pair; the pair endpoint was recounted
     on the next iteration). Removes ~50% of exact-counter calls.
  2. Disk-backed |Aut| cache (SQLite, phase-local file) keyed by
     (N, EX-canonical-key). EX canon keys are exact isomorphism
     invariants (Z27 L1), so a hit returns the true |Aut|. States whose
     canon key is the INV fallback (WL-proxy key, L2 by Z25-b/Z27) BYPASS
     the disk cache entirely - a proxy-key collision would corrupt a
     cache hit, and that failure mode is forbidden, not accepted.
     Per-chain commits (atomicity), in-memory edge-set memo unchanged.
  3. Per-cell flush of results JSON (already per-stage), explicit
     gc.collect() between cells, and peak RSS probed via ctypes
     GetProcessMemoryInfo (printed, not asserted).
  4. No threading is added: the harness remains strictly single-core,
     which also satisfies the thermal-envelope constraint by
     construction (no parallel pool exists to over-allocate).

AMENDMENT 3 (exact fast |Aut| counter, 2026-08-02, declared BEFORE the
(16,32) cell ran; validated against the Z32 counter before any use):
  Cause: at (16,32) the original Z32 backtracking counter would take
  40-70 min per cell (measured: (12,20) 409s, (14,28) 1411s; dominant
  cost = enumerating ALL automorphisms of high-symmetry transient-end
  states, e.g. |Aut|=362880 took 1.78s; states like 4xK4 with
  |Aut|=24^4*4! ~ 8e8 are infeasible for it).
  Exact identity used (no approximation, no proxy):
    |Aut(G)| = (prod_c class_size_c!) x |Aut(Q)|, where Q is the twin
    quotient graph: one vertex per twin class, colored by class size,
    with self-loops exactly on clique classes. Proof: the twin relation
    is automorphism-invariant and internal class permutations lift to
    automorphisms freely (class interior is uniform: all-adjacent or
    none); any lift is a class-size-preserving automorphism of Q.
    |Aut(Q)| is then computed by connected-component decomposition:
    |Aut(Q)| = prod_comp aut(comp) x prod_iso-class (mult)!.
    The twin quotient collapses the factorial-mass states to near-rigid
    small quotients; component decomposition collapses clone states
    (4xK4-like) to O(1) per iso class.
  Validation (before use): v2 must EQUAL the original counter on the
  Z32 closed-form cases (C10=20, Petersen=120, K5+5iso=14400, rigid=1,
  2xC5=800) plus C3/C4/C5/K2x3/K3x2/2xC4/4xK4/star+5iso closed forms and
  on >=1000 uniform random graphs per cell (10,15),(12,20),(16,32).
  100% agreement required; any mismatch aborts the swap.
  The Z32 counter code is NOT modified; v2 is a separate exact function.
  The disk cache key (N, EX canon key) is unchanged - both counters are
  exact, so cached values remain valid.

No fitting. No ML. Exact statistics only.
"""
import sys, time, math, random, json, collections, statistics, sqlite3, gc

sys.path.insert(0, r"C:\Users\bisha\Desktop\gods_paradox\phase_z25")
sys.path.insert(0, r"C:\Users\bisha\Desktop\gods_paradox\phase_z32")
sys.path.insert(0, r"C:\Users\bisha\Desktop\gods_paradox\phase_z33")
import z25b_engine_v2 as E
import z32_stationary_vs_burnside as Z32
from z32_stationary_vs_burnside import aut_size_exact, pairs_from_idx
from z33_symmetry_drift import step_mode, tau_of

SEED0 = 20260802
CAP = 512
JUMP_RATIO = 4.0
H1_GATE = 0.9
H1_REJECT = 0.5
H3_RHO = 0.7
MONO_FRAC = 0.02
CTRLB_POS = 0.1
CTRLB_NEG = 0.3
CTRLA_RATIO = 3.0
CTRLC_FACTOR = 0.9
CTRLC2_INFLATE = 0.01

THETA_BIN_EDGES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 9), (10, 10 ** 9)]
THETA_BIN_LABELS = ["0", "1", "2", "3", "4", "5-9", "10+"]

MAIN_CELL = (10, 15)
MAIN_CHAINS = {"random": 500, "lex": 200, "entropy": 200, "autmin": 200}
OTHER_CELLS = [(8, 12), (12, 20), (14, 28), (16, 32)]
OTHER_CHAINS = {(8, 12): {"random": 200, "lex": 100, "entropy": 100, "autmin": 100},
                (12, 20): {"random": 80, "lex": 40, "entropy": 40, "autmin": 20},
                (14, 28): {"random": 50, "lex": 25, "entropy": 25, "autmin": 12},
                (16, 32): {"random": 50, "lex": 25, "entropy": 25, "autmin": 12}}

REW_K = 30
CF_K = 10
NCHAIN_B = 300
NCHAIN_C1 = 300
NCHAIN_C2 = 100
HORIZON_C1 = 40
C2_MODES = ("lex", "entropy", "autmin")


def set_N(n):
    E.N = n
    E._MEMO.clear(); E._AUT.clear(); E._KC.clear()
    Z32._AUT_EXACT.clear()


# ---------------- twin potential (exact) -----------------------------------
def twin_potential(g):
    """Theta(G) = sum_i C(|C_i|,2) over twin classes.
    Returns (theta, class_sizes_sorted, n_classes). u,v twins iff
    (nb[u]^nb[v]) has no bits outside {u,v}."""
    n = E.N
    edges = set(g)
    nb = [0] * n
    for a, b in edges:
        nb[a] |= (1 << b)
        nb[b] |= (1 << a)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u in range(n):
        for v in range(u + 1, n):
            diff = nb[u] ^ nb[v]
            if diff & ~((1 << u) | (1 << v)) == 0:
                ru, rv = find(u), find(v)
                if ru != rv:
                    parent[ru] = rv
    sizes = collections.Counter(find(u) for u in range(n))
    theta = sum(c * (c - 1) // 2 for c in sizes.values())
    return theta, sorted(sizes.values()), len(sizes)


def theta_bin(th):
    for i, (lo, hi) in enumerate(THETA_BIN_EDGES):
        if lo <= th <= hi:
            return THETA_BIN_LABELS[i]
    return "10+"


# ---------------- disk-backed |Aut| cache (EX keys only) --------------------
CACHE_PATH = r"C:\Users\bisha\Desktop\gods_paradox\phase_z35\z35_aut_cache.sqlite"


class AutCache:
    """SQLite cache keyed by (N, EX-canonical-key). INV-proxy keys are
    NEVER cached (a proxy collision would corrupt a hit). Exactness of
    stored values is inherited from aut_size_exact (Z32)."""

    def __init__(self, path=CACHE_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS aut "
            "(n INTEGER, ckey TEXT, aut INTEGER, PRIMARY KEY (n, ckey))")
        self.conn.commit()
        self._pending = []

    def get(self, n, ckey_s):
        row = self.conn.execute(
            "SELECT aut FROM aut WHERE n=? AND ckey=?", (n, ckey_s)).fetchone()
        if row is not None:
            return row[0]
        for pn, pc, pa in self._pending:
            if pn == n and pc == ckey_s:
                return pa
        return None

    def put(self, n, ckey_s, aut):
        self._pending.append((n, ckey_s, aut))

    def commit(self):
        if self._pending:
            self.conn.executemany(
                "INSERT OR REPLACE INTO aut (n, ckey, aut) VALUES (?,?,?)",
                self._pending)
            self.conn.commit()
            self._pending = []

    def size(self):
        row = self.conn.execute("SELECT COUNT(*) FROM aut").fetchone()
        return row[0]

    def close(self):
        self.commit()
        self.conn.close()


def peak_mem_mb():
    """Peak/current process RSS (psutil; ctypes fallback). Returns
    (peak_mb, current_mb) or (None, None) if unavailable."""
    try:
        import psutil
        p = psutil.Process()
        return p.memory_info().peak_wset / (1024.0 * 1024.0), \
               p.memory_info().rss / (1024.0 * 1024.0)
    except Exception:
        pass
    try:
        import ctypes
        from ctypes import wintypes
        class PMC(ctypes.Structure):
            _fields_ = [("cb", wintypes.DWORD),
                        ("PageFaultCount", wintypes.DWORD),
                        ("PeakWorkingSetSize", ctypes.c_size_t),
                        ("WorkingSetSize", ctypes.c_size_t),
                        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                        ("PagefileUsage", ctypes.c_size_t),
                        ("PeakPagefileUsage", ctypes.c_size_t)]
        h = ctypes.windll.kernel32.GetCurrentProcess()
        pmc = PMC()
        pmc.cb = ctypes.sizeof(PMC)
        for fn in (ctypes.windll.psapi.GetProcessMemoryInfo,
                   ctypes.windll.psapi.K32GetProcessMemoryInfo):
            try:
                if fn(h, ctypes.byref(pmc), pmc.cb):
                    return pmc.PeakWorkingSetSize / (1024.0 * 1024.0), \
                           pmc.WorkingSetSize / (1024.0 * 1024.0)
            except Exception:
                continue
    except Exception:
        pass
    return None, None


# ---------------- exact fast |Aut| (Amendment 3) ----------------------------
def _twin_classes(edges, n):
    nb = [0] * n
    for a, b in edges:
        nb[a] |= (1 << b)
        nb[b] |= (1 << a)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u in range(n):
        for v in range(u + 1, n):
            if (nb[u] ^ nb[v]) & ~((1 << u) | (1 << v)) == 0:
                ru, rv = find(u), find(v)
                if ru != rv:
                    parent[ru] = rv
    cls = {}
    for v in range(n):
        cls.setdefault(find(v), []).append(v)
    return list(cls.values())


def aut_colored_count(k, adj, color):
    """Exact |Aut| of a colored simple graph WITH self-loops (adj[u][u]=1
    allowed). Automorphisms preserve color; self-loop status is encoded in
    the vertex signature via degree (a self-loop adds 1 to the degree)."""
    deg = [sum(adj[u]) for u in range(k)]
    sig = {}
    for v in range(k):
        neigh = tuple(sorted((color[w], deg[w]) for w in range(k) if adj[v][w]))
        sig[v] = (color[v], adj[v][v], deg[v], neigh)
    by_sig = {}
    for v in range(k):
        by_sig.setdefault(sig[v], []).append(v)
    src_order = sorted(range(k), key=lambda v: len(by_sig[sig[v]]))
    cnt = [0]
    mapping = {}
    used = [False] * k
    def backtrack(i):
        if i == k:
            cnt[0] += 1
            return
        u = src_order[i]
        for v in by_sig[sig[u]]:
            if used[v]:
                continue
            ok = True
            for x, y in mapping.items():
                if adj[u][x] != adj[v][y]:
                    ok = False
                    break
            if not ok:
                continue
            used[v] = True
            mapping[u] = v
            backtrack(i + 1)
            del mapping[u]
            used[v] = False
    backtrack(0)
    return cnt[0]


def aut_quotient_components(q, adj, color):
    """Exact |Aut(Q)| = prod aut(comp) x prod over iso-classes of (mult)!.
    Iso-classes verified exactly via the union identity:
    |Aut(A u B)| = 2|Aut(A)||Aut(B)|  <=>  A ~= B (connected comps)."""
    seen = [False] * q
    comps = []
    for s in range(q):
        if seen[s]:
            continue
        stack = [s]
        seen[s] = True
        comp = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for w in range(q):
                if adj[u][w] and w != u and not seen[w]:
                    seen[w] = True
                    stack.append(w)
        lab = {v: i for i, v in enumerate(sorted(comp))}
        k = len(comp)
        ca = [[0] * k for _ in range(k)]
        for u in comp:
            for w in comp:
                ca[lab[u]][lab[w]] = adj[u][w]
        cc = tuple(color[v] for v in sorted(comp))
        comps.append((k, ca, cc))
    groups = collections.defaultdict(list)
    for k, ca, cc in comps:
        groups[(k, tuple(sorted(cc)))].append((k, ca, cc))
    total = 1
    for key, members in groups.items():
        subs = []
        for k, ca, cc in members:
            a = aut_colored_count(k, ca, cc)
            placed = False
            for sub in subs:
                sk, sca, scc, sa = sub[0]
                if a != sa:
                    continue
                uadj = [[0] * (2 * k) for _ in range(2 * k)]
                for i in range(k):
                    for j in range(k):
                        uadj[i][j] = ca[i][j]
                        uadj[k + i][k + j] = sca[i][j]
                u = aut_colored_count(2 * k, uadj, cc + scc)
                if u == 2 * a * sa:
                    sub.append((k, ca, cc, a))
                    placed = True
                    break
            if not placed:
                subs.append([(k, ca, cc, a)])
        for sub in subs:
            m = len(sub)
            f = 1
            for i in range(2, m + 1):
                f *= i
            total *= f * (sub[0][3] ** m)
    return total


def aut_size_exact_v2(g):
    """Exact |Aut(G)| = TF x |Aut(twin quotient)| (Amendment 3 identity).
    Identical output to aut_size_exact (Z32) on all validated cases."""
    n = E.N
    edges = set(g)
    classes = _twin_classes(edges, n)
    cls_sorted = [sorted(c) for c in classes]
    q = len(cls_sorted)
    idx = {}
    for i, c in enumerate(cls_sorted):
        for v in c:
            idx[v] = i
    color = tuple(len(c) for c in cls_sorted)
    adj = [[0] * q for _ in range(q)]
    for a, b in edges:
        i, j = idx[a], idx[b]
        if i == j:
            adj[i][i] = 1
        else:
            adj[i][j] = 1
            adj[j][i] = 1
    tf = 1
    for c in cls_sorted:
        for k in range(2, len(c) + 1):
            tf *= k
    if q == n and all(len(c) == 1 for c in cls_sorted):
        return aut_size_exact(g)
    return tf * aut_quotient_components(q, adj, color)


def validate_v2():
    """Amendment-3 gate: v2 must equal the original counter everywhere."""
    checks = []
    def check(g, expected=None):
        set_N(E.N)
        a_old = aut_size_exact(frozenset(g))
        a_new = aut_size_exact_v2(frozenset(g))
        ok = (a_new == a_old and (expected is None or a_old == expected))
        checks.append((ok, frozenset(g), a_old, a_new, expected))
        return ok
    import random as _r
    rng = _r.Random(20260802)
    # closed-form cases
    def cycle(n):
        return frozenset((i, (i + 1) % n) for i in range(n))
    def petersen():
        out = frozenset((i, (i + 1) % 5) for i in range(5))
        inn = frozenset((5 + i, 5 + (i + 2) % 5) for i in range(5))
        spokes = frozenset((i, 5 + i) for i in range(5))
        return out | inn | spokes
    def k_complete(n):
        return frozenset((a, b) for a in range(n) for b in range(a + 1, n))
    def k_disjoint(n, copies):
        e = set()
        for c in range(copies):
            off = c * n
            for a in range(n):
                for b in range(a + 1, n):
                    e.add((off + a, off + b))
        return frozenset(e)
    def cycle_copies(n, copies):
        e = set()
        for c in range(copies):
            off = c * n
            for i in range(n):
                e.add((off + i, off + (i + 1) % n))
        return frozenset(e)
    star5iso = frozenset((0, i) for i in range(1, 5))  # K1,4 on N=5
    cases = [
        (10, cycle(10), 20), (10, petersen(), 120),
        (10, k_complete(5), 14400),             # K5 + 5 iso on N=10
        (10, frozenset(), 3628800),             # empty N=10 -> 10!
        (10, cycle_copies(5, 2), 200),          # 2 x C5 = 10^2 * 2!
        (6, k_disjoint(2, 3), 48),              # 3 x K2
        (6, k_disjoint(3, 2), 72),              # 2 x K3
        (4, cycle(4), 8), (5, cycle(5), 10), (3, cycle(3), 6),
        (4, k_complete(4), 24), (3, k_complete(3), 6),
        (16, k_disjoint(4, 4), 24 ** 4 * 24),   # 4 x K4
        (8, cycle_copies(4, 2), 8 ** 2 * 2),    # 2 x C4 = 128
        (12, cycle_copies(6, 2), 12 ** 2 * 2),  # 2 x C6 = 288
        (15, cycle_copies(5, 3), 10 ** 3 * 6),  # 3 x C5 = 6000
        (5, star5iso, 24),                      # star K1,4: leaves 4!
    ]
    for n, g, exp in cases:
        set_N(n)
        check(frozenset(g), exp)
    # random uniform draws
    for cell, cnt in [((10, 15), 1500), ((12, 20), 1500), ((16, 32), 800)]:
        set_N(cell[0])
        totp = cell[0] * (cell[0] - 1) // 2
        for i in range(cnt):
            e = pairs_from_idx(rng.sample(range(totp), cell[1]), cell[0])
            check(e)
    nfail = sum(1 for c in checks if not c[0])
    print(f"[z35] validate_v2: {len(checks)} checks, {nfail} failures", flush=True)
    for ok, g, a_old, a_new, exp in checks:
        if not ok:
            print("  FAIL:", repr(g)[:80], "old", a_old, "new", a_new, "exp", exp, flush=True)
    return nfail == 0


# ---------------- chain collection -----------------------------------------
def collect_steps(N, M, chains, cap=CAP, prog_every=None, cache=None):
    if prog_every is None:
        prog_every = 10 if N >= 12 else 50
    set_N(N)
    steps = []
    chains_info = []
    n_hit = 0
    n_miss = 0
    for mode, nch in chains.items():
        conv = 0
        for s in range(nch):
            rng = random.Random(SEED0 + 131 * s + 991 * len(mode))
            totp = N * (N - 1) // 2
            e = pairs_from_idx(rng.sample(range(totp), M), N)
            states = [e]
            keys = [E.canon(e)]
            seen = {keys[0]}
            tau = None
            for t in range(1, cap):
                e = step_mode(e, mode, rng)
                c = E.canon(e)
                if c in seen:
                    tau = t
                    break
                seen.add(c)
                states.append(e)
                keys.append(c)
            if tau is None:
                continue
            conv += 1
            # exact |Aut| ONCE per state; disk cache on (N, EX canon key).
            # Amendment 3: exact fast counter (twin quotient), validated
            # vs aut_size_exact on 3817 graphs (100% agreement).
            auts = []
            for k in range(len(states)):
                ck = keys[k]
                if cache is not None and ck[0] == "EX":
                    cs = repr(ck)
                    a = cache.get(N, cs)
                    if a is None:
                        a = aut_size_exact_v2(states[k])
                        cache.put(N, cs, a)
                        n_miss += 1
                    else:
                        n_hit += 1
                else:
                    a = aut_size_exact_v2(states[k])
                auts.append(a)
            if cache is not None:
                cache.commit()
            th0_first = twin_potential(states[0])[0]
            th_traj = []
            for i in range(len(states) - 1):
                g0, g1 = states[i], states[i + 1]
                a0, a1 = auts[i], auts[i + 1]
                th0, cl0, nc0 = twin_potential(g0)
                th1, cl1, nc1 = twin_potential(g1)
                R, A = tau_of(g0)
                steps.append({
                    "mode": mode, "t": i,
                    "aut0": a0, "aut1": a1,
                    "logratio": math.log(a1 / a0),
                    "daut": a1 - a0,
                    "jump": a1 >= JUMP_RATIO * a0,
                    "theta0": th0, "theta1": th1,
                    "dtheta": th1 - th0,
                    "cls0": cl0, "cls1": cl1,
                    "R": R, "A": A,
                })
                th_traj.append(th0)
            th_traj.append(twin_potential(states[-1])[0])
            chains_info.append({
                "mode": mode, "tau": tau,
                "theta_start": th0_first,
                "theta_end": th_traj[-1],
                "traj": th_traj,
            })
            if (s + 1) % prog_every == 0:
                print(f"[z35] {mode:7s} {s + 1}/{nch} chains (conv {conv})", flush=True)
        print(f"[z35] cell {N},{M} mode {mode}: {conv}/{nch} converged", flush=True)
    return steps, chains_info, n_hit, n_miss


# ---------------- statistics helpers ---------------------------------------
def rankdata(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = 1.0 + (i + j) / 2.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    rx, ry = rankdata(xs), rankdata(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    cov = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    vx = sum((r - mx) ** 2 for r in rx)
    vy = sum((r - my) ** 2 for r in ry)
    if vx == 0 or vy == 0:
        return None
    return cov / math.sqrt(vx * vy)


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return cov / math.sqrt(vx * vy)


def mutual_info(joint_counter, x_marg, y_marg, n):
    mi = 0.0
    for (x, y), c in joint_counter.items():
        if c > 0:
            pxy = c / n
            px = x_marg[x] / n
            py = y_marg[y] / n
            mi += pxy * math.log2(pxy / (px * py))
    return mi


def conditional_entropy(joint_counter, x_marg, n):
    h = 0.0
    for (x, y), c in joint_counter.items():
        if c > 0:
            pxy = c / n
            px = x_marg[x] / n
            h -= pxy * math.log2(px / pxy)
    return h


def frac(rows, pred):
    n = len(rows)
    if n == 0:
        return None
    return sum(1 for r in rows if pred(r)) / n


def summarize_steps(steps):
    out = {}
    modes = sorted(set(r["mode"] for r in steps))
    for mode in modes:
        rs = [r for r in steps if r["mode"] == mode]
        n = len(rs)
        dtheta = [r["dtheta"] for r in rs]
        lr = [r["logratio"] for r in rs]
        onJ = [r for r in rs if r["jump"]]
        offJ = [r for r in rs if not r["jump"]]
        daut = [r["daut"] for r in rs]
        sp = spearman(dtheta, lr)
        pe = pearson(dtheta, daut)
        out[mode] = dict(
            n=n,
            P_dt_pos=round(frac(rs, lambda r: r["dtheta"] > 0), 4),
            P_dt_zero=round(frac(rs, lambda r: r["dtheta"] == 0), 4),
            P_dt_neg=round(frac(rs, lambda r: r["dtheta"] < 0), 4),
            mean_dt=round(sum(dtheta) / n, 4),
            P_J=round(frac(rs, lambda r: r["jump"]), 4),
            P_dt_pos_given_J=round(frac(onJ, lambda r: r["dtheta"] > 0), 4),
            P_dt_zero_given_J=round(frac(onJ, lambda r: r["dtheta"] == 0), 4),
            P_dt_neg_given_J=round(frac(onJ, lambda r: r["dtheta"] < 0), 4),
            P_dt_pos_given_notJ=round(frac(offJ, lambda r: r["dtheta"] > 0), 4),
            n_J=len(onJ),
            rho_spearman_dt_logaut=round(sp, 4) if sp is not None else None,
            rho_pearson_dt_daut=round(pe, 4) if pe is not None else None,
        )
    return out


def info_analysis(steps):
    n = len(steps)
    tg = [1 if r["jump"] else 0 for r in steps]
    thb = [theta_bin(r["theta0"]) for r in steps]
    tau = [(r["R"], r["A"]) for r in steps]
    H_T = 0.0
    for c in [sum(tg), n - sum(tg)]:
        if c > 0:
            p = c / n
            H_T -= p * math.log2(p)
    jt = collections.Counter(zip(tg, thb))
    xt = collections.Counter(tg)
    yt = collections.Counter(thb)
    I_theta = mutual_info(jt, xt, yt, n)
    jtau = collections.Counter(zip(tg, tau))
    ytau = collections.Counter(tau)
    I_tau = mutual_info(jtau, xt, ytau, n)
    xy = collections.Counter()
    yy = collections.Counter()
    xx = collections.Counter()
    for i in range(n):
        x = tg[i]
        y = (thb[i], tau[i])
        xy[(x, y)] += 1
        xx[x] += 1
        yy[y] += 1
    I_joint = mutual_info(xy, xx, yy, n)
    I_theta_given_tau = I_joint - I_tau
    I_tau_given_theta = I_joint - I_theta
    return dict(H_T=round(H_T, 4),
                I_J_theta=round(I_theta, 4),
                I_J_tau=round(I_tau, 4),
                I_J_theta_tau=round(I_joint, 4),
                I_J_theta_given_tau=round(I_theta_given_tau, 4),
                I_J_tau_given_theta=round(I_tau_given_theta, 4))


def per_mode_info(steps):
    modes = sorted(set(r["mode"] for r in steps))
    out = {}
    for mode in modes:
        rs = [r for r in steps if r["mode"] == mode]
        out[mode] = info_analysis(rs)
    return out


def theta_dist(steps, chains_info):
    modes = sorted(set(r["mode"] for r in steps))
    out = {}
    for mode in modes:
        rs = [r for r in steps if r["mode"] == mode]
        th0 = collections.Counter(theta_bin(r["theta0"]) for r in rs)
        th1 = collections.Counter(theta_bin(r["theta1"]) for r in rs)
        starts = collections.Counter(str(c["theta_start"]) for c in chains_info if c["mode"] == mode)
        ends = collections.Counter(str(c["theta_end"]) for c in chains_info if c["mode"] == mode)
        n = len(rs)
        out[mode] = dict(
            P_theta_before={k: round(v / n, 4) for k, v in sorted(th0.items())},
            P_theta_after={k: round(v / n, 4) for k, v in sorted(th1.items())},
            P_theta_chain_start={k: round(v / len([c for c in chains_info if c["mode"] == mode]), 4) for k, v in sorted(starts.items())},
            P_theta_chain_end={k: round(v / len([c for c in chains_info if c["mode"] == mode]), 4) for k, v in sorted(ends.items())},
        )
    return out


def transition_tables(steps):
    modes = sorted(set(r["mode"] for r in steps))
    out = {}
    for mode in modes:
        rs = [r for r in steps if r["mode"] == mode]
        pJ_given_theta = {}
        pJ_given_tau = {}
        for b in THETA_BIN_LABELS:
            sub = [r for r in rs if theta_bin(r["theta0"]) == b]
            if sub:
                pJ_given_theta[b] = dict(n=len(sub), P_J=round(frac(sub, lambda r: r["jump"]), 4),
                                         P_dt_pos=round(frac(sub, lambda r: r["dtheta"] > 0), 4))
        tau_groups = collections.defaultdict(list)
        for r in rs:
            tau_groups[(r["R"], r["A"])].append(r)
        for shell, sub in sorted(tau_groups.items(), key=lambda kv: -len(kv[1]))[:8]:
            pJ_given_tau[str(shell)] = dict(n=len(sub), P_J=round(frac(sub, lambda r: r["jump"]), 4),
                                            P_dt_pos=round(frac(sub, lambda r: r["dtheta"] > 0), 4))
        # cross-tab dtheta sign x jump
        cross = {}
        for ds in ("neg", "zero", "pos"):
            for jf in (False, True):
                key = f"dTheta{ds}_J{jf}"
                cross[key] = sum(1 for r in rs
                                 if (r["dtheta"] < 0) == (ds == "neg")
                                 and (r["dtheta"] == 0) == (ds == "zero")
                                 and r["jump"] == jf)
        out[mode] = dict(P_J_given_theta=pJ_given_theta,
                         P_J_given_tau=pJ_given_tau,
                         cross_tab=cross)
    return out


def chain_monotonicity(chains_info):
    modes = sorted(set(c["mode"] for c in chains_info))
    out = {}
    for mode in modes:
        cs = [c for c in chains_info if c["mode"] == mode]
        any_neg = [c for c in cs if any(b < a for a, b in zip(c["traj"], c["traj"][1:]))]
        nondec = [c for c in cs if all(b >= a for a, b in zip(c["traj"], c["traj"][1:]))]
        taus = [c["tau"] for c in cs]
        out[mode] = dict(
            n=len(cs),
            frac_chains_any_dt_neg=round(len(any_neg) / len(cs), 4),
            frac_chains_theta_nondecreasing=round(len(nondec) / len(cs), 4),
            tau_median=int(statistics.median(taus)) if taus else None,
            theta_start_median=int(statistics.median([c["theta_start"] for c in cs])),
            theta_end_median=int(statistics.median([c["theta_end"] for c in cs])),
        )
    return out


# ---------------- adversarial control primitives ---------------------------
ALL_PAIRS_CACHE = {}

def all_pairs(n):
    if n not in ALL_PAIRS_CACHE:
        ALL_PAIRS_CACHE[n] = [(a, b) for a in range(n) for b in range(a + 1, n)]
    return ALL_PAIRS_CACHE[n]


def rewire_degree_preserving(g, rng, n_swaps=REW_K):
    """Double-edge swap preserving the degree sequence (null for Control A)."""
    edges = set(g)
    edge_list = list(edges)
    for _ in range(n_swaps):
        if len(edge_list) < 2:
            break
        i, j = rng.sample(range(len(edge_list)), 2)
        e1, e2 = edge_list[i], edge_list[j]
        a, b = e1
        c, d = e2
        swapped = False
        for ne1, ne2 in [((min(a, c), max(a, c)), (min(b, d), max(b, d))),
                         ((min(a, d), max(a, d)), (min(b, c), max(b, c)))]:
            if ne1 in edges or ne2 in edges or ne1 == ne2:
                continue
            if ne1 == e1 or ne1 == e2 or ne2 == e1 or ne2 == e2:
                continue
            edges.discard(e1); edges.discard(e2)
            edges.add(ne1); edges.add(ne2)
            edge_list = list(edges)
            swapped = True
            break
        if not swapped:
            break
    return frozenset(edges)


def config_model_same_deg(degree_list, rng, max_tries=400):
    """Random simple graph with the given degree sequence (null, Control A)."""
    n = len(degree_list)
    target_m = sum(degree_list) // 2
    for _ in range(max_tries):
        stubs = []
        for v, d in enumerate(degree_list):
            stubs.extend([v] * d)
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i + 1]
            if a == b:
                ok = False
                break
            e = (min(a, b), max(a, b))
            if e in edges:
                ok = False
                break
            edges.add(e)
        if ok and len(edges) == target_m:
            return frozenset(edges)
    return None


def step_reversed(e, rng):
    """Control B: reversed extremal choice - remove MAX degree-sum edge,
    add MIN degree-sum non-edge, random within extremal sets."""
    d = E.degrees(e)
    ed = set(e)
    ne = [(a, b) for a in range(E.N) for b in range(a + 1, E.N) if (a, b) not in ed]
    ds = lambda x: d[x[0]] + d[x[1]]
    smax = max(ds(x) for x in ed)
    smin = min(ds(x) for x in ne)
    R = [x for x in ed if ds(x) == smax]
    A = [x for x in ne if ds(x) == smin]
    r = rng.choice(R)
    a = rng.choice(A)
    g = set(ed)
    g.discard(r)
    g.add(a)
    return frozenset(g)


def run_control_A(N, M, n_chains=400):
    """Sample transient states directly and measure null twin-growth rates
    (rewire / config-model with the SAME degree sequence) plus the extremal
    per-step rate ON THE SAME STATES (the clean Control-A comparison)."""
    set_N(N)
    rew = collections.Counter()
    cf = collections.Counter()
    ex = collections.Counter()
    n_sampled = 0
    n_rew_ok = 0
    n_cf_ok = 0
    for s in range(n_chains):
        rng = random.Random(SEED0 + 551 * s + 17)
        totp = N * (N - 1) // 2
        e = pairs_from_idx(rng.sample(range(totp), M), N)
        seen = {E.canon(e)}
        picked = None
        for t in range(1, 40):
            g0 = e
            e = step_mode(e, "random", rng)
            c = E.canon(e)
            if c in seen:
                break
            seen.add(c)
            if t % 3 == 0:
                picked = (g0, e)
                break
        if picked is None:
            continue
        g0, g1 = picked
        th0 = twin_potential(g0)[0]
        dth_ex = twin_potential(g1)[0] - th0
        if dth_ex > 0:
            ex["pos"] += 1
        elif dth_ex < 0:
            ex["neg"] += 1
        else:
            ex["zero"] += 1
        dg = E.degrees(g0)
        deg_list = [dg[v] for v in range(N)]
        rw_rng = random.Random(SEED0 + 771 * s)
        for k in range(REW_K):
            gr = rewire_degree_preserving(g0, rw_rng)
            if gr is not None:
                rw = twin_potential(gr)[0] - th0
                if rw > 0:
                    rew["pos"] += 1
                elif rw < 0:
                    rew["neg"] += 1
                else:
                    rew["zero"] += 1
                n_rew_ok += 1
        cf_rng = random.Random(SEED0 + 977 * s)
        for k in range(CF_K):
            gc = config_model_same_deg(deg_list, cf_rng)
            if gc is not None:
                dc = twin_potential(gc)[0] - th0
                if dc > 0:
                    cf["pos"] += 1
                elif dc < 0:
                    cf["neg"] += 1
                else:
                    cf["zero"] += 1
                n_cf_ok += 1
        n_sampled += 1
    out = dict(n_states=n_sampled,
               n_extremal_steps=n_sampled,
               P_pos_extremal_same_states=round(ex["pos"] / n_sampled, 4) if n_sampled else None,
               P_neg_extremal_same_states=round(ex["neg"] / n_sampled, 4) if n_sampled else None,
               P_zero_extremal_same_states=round(ex["zero"] / n_sampled, 4) if n_sampled else None,
               n_rewires_applied=n_rew_ok,
               P_pos_rewire=round(rew["pos"] / n_rew_ok, 4) if n_rew_ok else None,
               P_neg_rewire=round(rew["neg"] / n_rew_ok, 4) if n_rew_ok else None,
               P_zero_rewire=round(rew["zero"] / n_rew_ok, 4) if n_rew_ok else None,
               n_cf_graphs=n_cf_ok,
               P_pos_config=round(cf["pos"] / n_cf_ok, 4) if n_cf_ok else None,
               P_neg_config=round(cf["neg"] / n_cf_ok, 4) if n_cf_ok else None,
               P_zero_config=round(cf["zero"] / n_cf_ok, 4) if n_cf_ok else None)
    return out


def run_control_B(N, M, n_chains=NCHAIN_B):
    set_N(N)
    recs = []
    for s in range(n_chains):
        rng = random.Random(SEED0 + 311 * s + 5)
        totp = N * (N - 1) // 2
        e = pairs_from_idx(rng.sample(range(totp), M), N)
        seen = {E.canon(e)}
        states = [e]
        tau = None
        for t in range(1, CAP):
            e = step_reversed(e, rng)
            c = E.canon(e)
            if c in seen:
                tau = t
                break
            seen.add(c)
            states.append(e)
        if tau is None:
            continue
        for i in range(len(states) - 1):
            g0, g1 = states[i], states[i + 1]
            a0 = aut_size_exact(g0)
            a1 = aut_size_exact(g1)
            th0 = twin_potential(g0)[0]
            th1 = twin_potential(g1)[0]
            recs.append(dict(dtheta=th1 - th0, jump=a1 >= JUMP_RATIO * a0))
    n = len(recs)
    onJ = [r for r in recs if r["jump"]]
    return dict(n=n,
                P_dt_pos=round(frac(recs, lambda r: r["dtheta"] > 0), 4),
                P_dt_zero=round(frac(recs, lambda r: r["dtheta"] == 0), 4),
                P_dt_neg=round(frac(recs, lambda r: r["dtheta"] < 0), 4),
                mean_dt=round(sum(r["dtheta"] for r in recs) / n, 4),
                P_J=round(frac(recs, lambda r: r["jump"]), 4),
                P_dt_pos_given_J=round(frac(onJ, lambda r: r["dtheta"] > 0), 4),
                n_J=len(onJ),
                n_converged=n_chains)


def run_control_C1(N, M, n_chains=NCHAIN_C1, horizon=HORIZON_C1):
    """Random selector, fixed horizon, ZERO canon() calls."""
    set_N(N)
    recs = []
    for s in range(n_chains):
        rng = random.Random(SEED0 + 613 * s + 3)
        totp = N * (N - 1) // 2
        e = pairs_from_idx(rng.sample(range(totp), M), N)
        for t in range(horizon):
            g0 = e
            e = step_mode(e, "random", rng)
            th0 = twin_potential(g0)[0]
            th1 = twin_potential(e)[0]
            recs.append(th1 - th0)
    n = len(recs)
    return dict(n=n,
                P_dt_pos=round(sum(1 for x in recs if x > 0) / n, 4),
                P_dt_zero=round(sum(1 for x in recs if x == 0) / n, 4),
                P_dt_neg=round(sum(1 for x in recs if x < 0) / n, 4),
                mean_dt=round(sum(recs) / n, 4))


def run_control_C2(N, M, modes=C2_MODES, n_chains=NCHAIN_C2):
    """Deterministic modes, canon-relabel at every step (EX keys only;
    INV fallback keeps the raw state, counted and reported)."""
    set_N(N)
    out = {}
    for mode in modes:
        recs = []
        n_inv = 0
        n_steps = 0
        for s in range(n_chains):
            rng = random.Random(SEED0 + 419 * s + 7 * len(mode))
            totp = N * (N - 1) // 2
            e = pairs_from_idx(rng.sample(range(totp), M), N)
            for t in range(30):
                key = E.canon(e)
                if key[0] == "EX":
                    e = frozenset(key[1])
                else:
                    n_inv += 1
                g0 = e
                e = step_mode(e, mode, rng)
                th0 = twin_potential(g0)[0]
                th1 = twin_potential(e)[0]
                recs.append(th1 - th0)
                n_steps += 1
        n = len(recs)
        out[mode] = dict(n=n,
                         n_inv_steps=n_inv,
                         P_dt_pos=round(sum(1 for x in recs if x > 0) / n, 4),
                         P_dt_zero=round(sum(1 for x in recs if x == 0) / n, 4),
                         P_dt_neg=round(sum(1 for x in recs if x < 0) / n, 4))
    return out


# ---------------- decisions -------------------------------------------------
def decide(stats, info, info_per_mode, mono, ctrlA, ctrlB, ctrlC1, ctrlC2):
    modes = list(stats.keys())
    h1_pass = all(stats[m]["P_dt_pos_given_J"] is not None and stats[m]["P_dt_pos_given_J"] >= H1_GATE for m in modes)
    h1_reject = any(stats[m]["P_dt_pos_given_J"] is not None and stats[m]["P_dt_pos_given_J"] < H1_REJECT for m in modes)
    pooled_ok = (info["I_J_theta"] > info["I_J_tau"] and
                 info["I_J_theta_given_tau"] > info["I_J_tau_given_theta"])
    reversed_modes = [m for m, d in info_per_mode.items()
                      if d["I_J_theta"] <= d["I_J_tau"] and d["I_J_theta_given_tau"] <= d["I_J_tau_given_theta"]]
    h2_pass = pooled_ok and len(reversed_modes) == 0
    h3_pass = all(stats[m]["rho_spearman_dt_logaut"] is not None and stats[m]["rho_spearman_dt_logaut"] >= H3_RHO for m in modes)
    near_mono = all(stats[m]["P_dt_neg"] <= MONO_FRAC for m in modes)
    ctrlA_pass = None
    if ctrlA["P_pos_rewire"] is not None and ctrlA["P_pos_config"] is not None:
        null_max = max(ctrlA["P_pos_rewire"], ctrlA["P_pos_config"])
        ex = ctrlA["P_pos_extremal_same_states"]
        ctrlA_pass = (ex is not None) and (ex >= CTRLA_RATIO * null_max)
    ctrlB_pass = ctrlB["P_dt_pos"] <= CTRLB_POS and ctrlB["P_dt_neg"] >= CTRLB_NEG
    ctrlC_pass = ctrlC1["P_dt_pos"] >= CTRLC_FACTOR * stats["random"]["P_dt_pos"]
    inflate = {m: ctrlC2[m]["P_dt_pos"] - stats[m]["P_dt_pos"] for m in ctrlC2}
    ctrlC2_pass = all(v <= CTRLC2_INFLATE for v in inflate.values())
    if h1_pass and near_mono and ctrlB_pass:
        outcome = "A (twin potential is the hidden invariant)"
    elif h1_pass and (h2_pass or h3_pass):
        outcome = "B (stochastic symmetry nucleation)"
    elif h1_reject or not (h2_pass or h3_pass):
        outcome = "C (Z34 was correlation; Theta fails)"
    else:
        outcome = "undetermined - see tables"
    return dict(h1_pass=h1_pass, h1_reject=h1_reject,
                h2_pass=h2_pass, h3_pass=h3_pass,
                near_monotone=near_mono,
                ctrlA_pass=ctrlA_pass, ctrlB_pass=ctrlB_pass,
                ctrlC_pass=ctrlC_pass, ctrlC2_pass=ctrlC2_pass,
                ctrlC2_inflation={k: round(v, 4) for k, v in inflate.items()},
                outcome=outcome)


def run_cell(N, M, chains, full_stats=True, cache=None):
    print(f"\n[z35] === cell ({N},{M}) ===", flush=True)
    t0 = time.time()
    steps, chains_info, n_hit, n_miss = collect_steps(N, M, chains, cache=cache)
    stats = summarize_steps(steps)
    mono = chain_monotonicity(chains_info)
    cell_out = dict(cell=[N, M],
                    chains=chains,
                    n_steps=len(steps),
                    stats=stats,
                    monotonicity=mono,
                    cache_hits=n_hit, cache_misses=n_miss,
                    wall_s=round(time.time() - t0, 1))
    if full_stats:
        info = info_analysis(steps)
        info["per_mode_raw"] = per_mode_info(steps)
        cell_out["info"] = {k: v for k, v in info.items() if k != "per_mode_raw"}
        cell_out["info_per_mode"] = info["per_mode_raw"]
        cell_out["theta_dist"] = theta_dist(steps, chains_info)
        cell_out["transitions"] = transition_tables(steps)
    for m in stats:
        s = stats[m]
        print(f"[z35] {m:7s} n={s['n']:5d} P(dt>0)={s['P_dt_pos']:.3f} "
              f"P(dt=0)={s['P_dt_zero']:.3f} P(dt<0)={s['P_dt_neg']:.3f} "
              f"P(J)={s['P_J']:.3f} P(dt>0|J)={s['P_dt_pos_given_J']:.3f} "
              f"rho={s['rho_spearman_dt_logaut']}", flush=True)
    gc.collect()
    pk, cur = peak_mem_mb()
    print(f"[z35] cell ({N},{M}) done in {cell_out['wall_s']}s | "
          f"cache hits {n_hit} / misses {n_miss} | "
          f"peak RSS {pk:.0f}MB current {cur:.0f}MB", flush=True)
    return cell_out


RESULTS_PATH = r"C:\Users\bisha\Desktop\gods_paradox\phase_z35\z35_results.json"


def load_results():
    try:
        with open(RESULTS_PATH) as f:
            return json.load(f)
    except Exception:
        return {"phase": "Z35", "cell_main": list(MAIN_CELL),
                "seed0": SEED0, "jump_ratio": JUMP_RATIO,
                "thresholds": {"H1_gate": H1_GATE, "H1_reject": H1_REJECT,
                               "H3_rho": H3_RHO, "mono_frac": MONO_FRAC,
                               "ctrlA_ratio": CTRLA_RATIO,
                               "ctrlB_pos": CTRLB_POS, "ctrlB_neg": CTRLB_NEG,
                               "ctrlC_factor": CTRLC_FACTOR,
                               "ctrlC2_inflate": CTRLC2_INFLATE}}


def save_results(out):
    with open(RESULTS_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print("[z35] saved", RESULTS_PATH, flush=True)


def main():
    import argparse
    import time
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", action="store_true")
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--cell", action="append", help="N,M for an other-cell run")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--validate-v2", action="store_true")
    args = ap.parse_args()
    if args.validate_v2:
        ok = validate_v2()
        print("[z35] validate_v2 result:", "PASS" if ok else "FAIL", flush=True)
        return
    do_all = args.all or not (args.main or args.controls or args.cell)
    out = load_results()
    cache = AutCache()
    # Amendment 4 (harness-only): the autmin selector in z33.step_mode
    # evaluates aut_size_exact per candidate edge pair (R x A), which is the
    # dominant cost at N>=14. aut_size_exact_v2 returns IDENTICAL exact
    # values (validated 3817/3817), so every selected edge, every chain step
    # and every statistic is unchanged; only the wall time drops. z33's file
    # is not modified.
    import z33_symmetry_drift as _Z33MOD
    if getattr(_Z33MOD, "aut_size_exact", None) is not aut_size_exact_v2:
        _Z33MOD.aut_size_exact = aut_size_exact_v2
        print("[z35] Amendment 4: autmin candidate |Aut| -> aut_size_exact_v2 (exact, validated, chains unchanged)", flush=True)
    pk0, cur0 = peak_mem_mb()
    print(f"[z35] harness: cache={CACHE_PATH} | start RSS peak {pk0}MB current {cur0}MB", flush=True)

    if do_all or args.main:
        main_cell = run_cell(MAIN_CELL[0], MAIN_CELL[1], MAIN_CHAINS, full_stats=True, cache=cache)
        out["main_cell"] = main_cell
        save_results(out)

    if do_all or args.controls:
        if "main_cell" not in out:
            print("[z35] ERROR: --controls needs main_cell in results; run --main first")
            cache.close()
            return
        main_cell = out["main_cell"]
        print("\n[z35] === control A (degree-preserving null) ===", flush=True)
        ctrlA = run_control_A(MAIN_CELL[0], MAIN_CELL[1])
        out["control_A"] = ctrlA
        print("[z35] A:", json.dumps(ctrlA), flush=True)
        save_results(out)

        print("\n[z35] === control B (reversed extremal rule) ===", flush=True)
        ctrlB = run_control_B(MAIN_CELL[0], MAIN_CELL[1])
        out["control_B"] = ctrlB
        print("[z35] B:", json.dumps(ctrlB), flush=True)
        save_results(out)

        print("\n[z35] === control C1 (no-canon random, fixed horizon) ===", flush=True)
        ctrlC1 = run_control_C1(MAIN_CELL[0], MAIN_CELL[1])
        out["control_C1"] = ctrlC1
        print("[z35] C1:", json.dumps(ctrlC1), flush=True)
        save_results(out)

        print("\n[z35] === control C2 (canon-relabel each step, det modes) ===", flush=True)
        ctrlC2 = run_control_C2(MAIN_CELL[0], MAIN_CELL[1])
        out["control_C2"] = ctrlC2
        print("[z35] C2:", json.dumps(ctrlC2), flush=True)
        save_results(out)

        dec = decide(main_cell["stats"], main_cell["info"], main_cell["info_per_mode"],
                     main_cell["monotonicity"], ctrlA, ctrlB, ctrlC1, ctrlC2)
        out["decision"] = dec
        print("\n[z35] DECISION:", json.dumps(dec, indent=2), flush=True)
        save_results(out)

    if do_all:
        out["other_cells"] = {}
        for cell in OTHER_CELLS:
            c = run_cell(cell[0], cell[1], OTHER_CHAINS[cell], full_stats=False, cache=cache)
            out["other_cells"][str(cell)] = c
            save_results(out)

    if args.cell:
        if "other_cells" not in out:
            out["other_cells"] = {}
        for spec in args.cell:
            n, m = (int(x) for x in spec.split(","))
            chains = OTHER_CHAINS[(n, m)]
            c = run_cell(n, m, chains, full_stats=False, cache=cache)
            out["other_cells"][str((n, m))] = c
            save_results(out)

    pk, cur = peak_mem_mb()
    print(f"[z35] final peak RSS {pk}MB current {cur}MB | cache rows {cache.size()}", flush=True)
    cache.close()
    print("\n[z35] FINAL:", out.get("decision", {}).get("outcome", "no decision yet"), flush=True)


if __name__ == "__main__":
    main()
