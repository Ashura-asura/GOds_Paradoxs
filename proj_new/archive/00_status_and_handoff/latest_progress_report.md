# LATEST PROGRESS REPORT — Z25 → Present (2026-08-03)
# Consolidated arc: tie-collapse mechanism, canon-bug fix, and full downstream re-derivation

---

## 0. TL;DR

The Z25–Z37 program closed one mechanistic question — *why does extremal edge
exchange concentrate onto a small high-symmetry attractor?* — at four levels:
engine (Z25/Z25b), information (Z26–Z29), geometry (Z30–Z32), mechanism
(Z33/Z34), structural theorem (Z35), regime decomposition (Z36), formal closure
(Z37+). On 2026-08-03 an audit found the harness `canon()` was **not
iso-invariant**; a third-party "fix" was chat-only (no artifact). The fix was then
**implemented in-repo and verified**, and **every canon-keyed downstream number
was re-derived**. Net result: **no foundational verdict reversed** (outcome B,
twin-channel mechanism, Control D, N-scalability, concentration < generation),
but several headline numbers changed (H2 gate FAIL→PASS; twin-law info ranking
flipped; Z33 τ collapse; Z37 EX-artifacts 1395→0).

---

## 1. THE ENGINE AND THE BUG (Z25 / Z25-b)

### Z25 — Relational origin engine (FAILED)
Conservative rule was contractive (witness edges accumulate, never replace) →
72/72 trials collapse to period-1 fixed points, no emergent ratios, no generative
surplus. Rule-8 closed as a mechanism failure.

### Z25-b — four hard questions (PARTIAL)
`z25b_engine_v2.py` (declared engine): edge exchange ordered by endpoint
degree-sum, tie-broken lexicographically, balance-vs-contrast by scalar p;
canonicalization via WL color refinement + budget-capped exact search.

- Q1 (universal ratios): **No.** Attractor ratios fragment across seeds, and M.
- Q2 (robustness): partial — robust only at "concentration behavior" level.
- Q3 (generative surplus): **No** — dynamics by construction permutes inside a
  finite orbit; seed graph + (N,M) are unaccounted inputs; the dynamics
  compresses information rather than generating it.
- Q4 (no hidden tuning): **Yes** — no energy/potential/symmetry term.

### THE BUG (discovered in audit 2026-08-03, fixed in-repo)
`canon()` picked canonical-label images from the color class's **own
vertex-index numbers**. Two encoded copies `g, π(g)` have classes with different
index sets → they searched disjoint label spaces → asymmetric (trivial-aut)
graphs returned their *own labeling*, never a global representative. Consequence
was exactly the measured EX-key artifact: **1395 of 2500 (56%)** encoded
successor pairs got different EX keys at (10,15).

**Second latent bug** caught by a cross-check vs an independent reference
(`canon_fixed.py`, left at the repo root — no artifact previously existed):
`_MEMO/_AUT/_KC` were keyed on `frozenset(edges)` only, but `wl_colors()` is
N-dependent (isolated vertices); a mixed-N process reused the N=4 canonical form
of a 5-vertex edge set. **Fix:** memo keys now `(N, edges)` / `(N, edges, k)`;
cross-check → **0 / 880 mismatches** (including 43 both-fallback cases).

The fix made to BOTH in-repo engines: images are iso-invariant contiguous label
blocks ordered by sorted WL-color rank; lex-min over intra-class permutation
freedom of the blocks. `z25_relational_engine.py` already did a full `N!` scan
(correct, untouched).

---

## 2. INFORMATION ACCOUNTING (Z26/Z27) — canon-independent core

- **Z26 Theorem A:** basin is seed-driven — 12 random seeds → 12 distinct
  attractor keys; the attractor is a function of (N, M, seed), no
  graph-independent canonical identity. (Re-verified under the fixed canon:
  the conclusion is about INV-key iso-classes and holds.)
- **Z26 Theorem B — no-free-lunch (L1, intact):** I_state = log2 C(45,15) =
  38.33 bits; H_output = 3.5850 bits = log2(12) ⇒ I_output < I_input by ~20×;
  dynamics concentrates, does not generate.
- **Z26 period-2 mechanism (intact):** projection hypothesis disproved
  (T² ≠ T on 24/24); real cause is a level-set boundary (2-point attractor,
  the exchange oscillates around the boundary of a monotone objective).
- **Z26 uniqueness-by-singleton DISPROVED:** remove-side is tie-degenerate
  (96/136), add-side is iso-singleton everywhere (0/136) → would-be uniqueness
  is a **tie-collapse** theorem (merging degenerate extremal choices under a
  fixed canonicalization), not local injectivity.
- **Z27:** `canon()` is exactly the orbit projection onto the unlabeled
  quotient. |Q_10,15| = 136,433, total unlabeled 12,005,168 (OEIS A000088(10))
  — counted exactly by Pólya enumeration, **canon-independent** and
  therefore intact after the canon fix. Information decomposition: gauge loss
  21.27 bits, dynamical contraction 17.06−3.585 = 13.47 bits; neither generates.
- **Z26/Z27 delivered facts + Control D** (twin-free algebraic seeds): all
  gates hold under the fixed canon as well.

---

## 3. INVARIANT HUNT & GEOMETRY (Z28–Z32)

- **Z28:** no scalar Lyapunov among standard invariants (strictly-one-sided =
  FALSE for every candidate on 1,152 steps). Closed.
- **Z29:** tie-class fixed point falsified at 0–1% (attractor states are the
  *most* tie-degenerate); coarse self-reinforcement refuted (4–7%). Closed.
- **Z30:** period-2 is a *selector*-level attractor sitting in a tie-degeneracy
  shell τ = (|R|,|A|) ≃ (6,2); verified control re-implementation, harness bug
  (faulty lex tie-break→ period-24 artifact) superseded.
- **Z30/Z31:** σ(N,M) = Burnside-weighted (Aut-weighted) tie-shell law is a
  stable limit law (Poisson-like peak at (1,1), N-independent for N≥10 at fixed
  ρ). Naive first-moment shell estimator fails; Aut-aware Burnside weighting is
  the correct one.
- **Z32 correction:** WL-proxy |Aut| was anti-correlated in the
  symmetry-rich regime (reads 10! instead of true 20 on C10) — replaced by an
  exact backtracking counter, validated 3817/3817 graphs (Petersen=120, C10=20,
  Shrikhande=192, Rook=1152, etc.). Outcome A (pure quotient geometry +
  bookkeeping) **refuted**: attractor |Aut| region ~900–17,280 sits ~10⁹ away
  from the uniform-labeled and Burnside masses (P(a labeled draw hits an
  attractor class) ≈ 2×10⁻⁵ per 40k draws).
- **Z33 — front-loaded staircase (outcome B):** every selector climbs from
  |Aut|=1 seed to end-transient 48–1440 in τ≈8–12 steps, but median drift is 0
  and the whole positive-mean is built on rare large jumps (decile
  [0,0,0,7,64,10032]). After the canon fix the headline numbers **re-collapsed**
  at (10,15): τ 12/9/8/8 → **7/7/7/6**, entropy fold 48→1440 (all folds now
  1440; τ* = 7 in Z35/Z37 as well — the three now coincide).
- **Z34 jump anatomy:** the only mechanism that carries |Aut| jumps is **twin
  restructuring** (H1: rate ratio 3.72× random, 3.57× autmin — over the 3× gate;
  2.57× lex, 2.31× entropy narrowly miss), **component cloning is a universal
  non-discriminator** (ratio ≈ 1.0: fires on ~100% of ALL steps, so it explains
  nothing), and H3 (unexplained residual) is refuted for this cell (<0.4% of
  J steps carry no event). Sparse-tie gating is real but weaker than the twin cue.

**Mechanism chain (Z26→Z34):** degree-sum extremization → vertices pushed to
equal degree → neighborhoods become more similar → twin classes form or merge →
|Aut| jumps by a factorial factor → a front-loaded staircase trace aboard the
Aut-weighted tie shell.

---

## 4. STRUCTURAL THEOREM / REGIME SPLIT (Z35/Z36) — the affected phases

### Z35 — twin potential as near-Lyapunov order parameter (OUTCOME B)
Exact-|Aut| protocol, gates pre-registered. Main cell (10,15) re-derived with
the **fixed canon** (ledger 8.14):

**Main table (10,15) — old buggy-canon (→ after-fix):**
| selector | n steps | P(J) | P(dt>0\|J) | ρ |
|---|---|---|---|---|
| random | 2919 (was 5631) | 0.391 (0.230) | 0.997 | 0.943 |
| lex | 1184 (was 1720) | 0.410 (0.325) | 1.000 | 0.939 |
| entropy | 1135 (was 1375) | 0.401 (0.331) | 0.998 | 0.910 |
| autmin | 1091 (was 1411) | 0.409 (0.316) | 0.998 | 0.959 |

- n_steps total: 6329 (was 10137); **P(dt<0|J) = 0.000 everywhere**.
- **H1 (P(dt>0|J)>0.9 everywhere): PASS after fix (already passing); H3
  (ρ 0.87–0.98): PASS; H2 (θ dominance over the (R,A) shell): FAIL→**PASS** after
  the fix — I(J;θ)=0.2436→**0.1929** now beats I(J;τ)=0.2777→**0.1381**,
  and I(J;θ|τ)=0.1762→0.2692 > I(J;τ|θ)=0.2103→0.2144.
- Controls: A (degree-preserving null) and C1 (no-canon) unchanged (canon-free);
  C2 (canon every step) lex P_pos 0.243→0.421 (n_inv_steps=0, no inflation,
  gate still passes — relabeling is the pre-registered chain definition, not a
  hidden driver); Control B (reversed extremal) n 3106→2162, coupling destroyed
  (P(dt>0|J)=0.431) — direction necessary.
- Other cells re-derived: (8,12) 2848→1708 steps, τ 5–7→4–5; (12,20) and
  (14,28) essentially unchanged (τ 11, 14–15); **(16,32) is the cleanest
  sanity check**: random/lex/autmin are bit-identical to the old run (same n,
  n_J frozen), entropy 453→451 (n_J 146 frozen) — tall sparse graphs are
  asymmetric with virtually no iso-class revisits, so the canon fix cancels to
  almost nothing there.
- **Decision: OUTCOME B unchanged** — stochastic symmetry nucleation:
  Theta = Σ C(|C_i|,2) is a near-Lyapunov order parameter (predicts every
  jump, P(dt<0|J)=0.000, rho 0.87–0.98), the jump factor is exactly the
  Amendment-3 identity.

### Control D (twin-free algebraic seeds)
G1 P(jump at t=0) = 0.000 (0/212) **PASS**; G2 P(jump & dθ≤0) = 0.0313 (32/1022,
all dθ=0) **PASS**; median τ_half = 0 (every chain dips to |Aut|=1) then twin
channel re-nucleates to end |Aut| = 3,110,400 (Shrikhande ≡ Rook canonical
endpoint). Algebraic channel is static; **twin channel is the sole jump channel**.

### Z36 — 4-channel decomposition (recorded as an entry, not merged)
Shrikhande (θ=0, Aut=192) breaks Theta-universality; honest decomposition:
|Aut(G)| = twin_aut × Aut(colored quotient) with a component factor when
disconnected, plus an **algebraic residual** when Theta=0 (regular + ≤3 distinct
spectrum / concentrated λ,μ signature). In an audit this was recorded as a
restatement of phase_z35 Amendment 3 — cross-tool agreement 18/18, plus two
corrections (random-regular Z2 exception, `Complement_Shrikhande_16_72` label
typo) already in its Addendum.

---

## 5. FORMAL CLOSURE THEOREMS (Z37+, `z37_closure.py`) — re-derived under fix

- **t1 — iso-invariance of tie / τ***: candidate sets (R,A) are iso-invariant
  (V1: 0/600); lex tie-break is NOT well-defined on the quotient (1105/2500
  iso-counterexamples where lex successors differ) — but after the canon fix
  the EX-key **artifacts** (the real bug) are **0/2500** (was 1395), while the
  genuine counterexamples remain 1105 (those are label-dependent, not a bug).
  INV-key τ* passes 0/1500; τ* chains: median period **7** at (10,15),
  200/200 converge.
- **t2: twin-formation law** — P(E)≈0.08, near-constant across cells; top-3 MI
  features TH0 (twin potential) > R/A/FREEDOM > DEGVAR. H_T2 falsified
  (CN_ADD not dominant). Minimal sufficient set {TH0, DEGVAR, A}.
- **t3: scaling** — median τ* (random selector): 19,25,34,45,64.5 at
  N=16,20,24,30,40 ⇒ **τ ∝ N, r²=0.999** (linear; exponential rejected);
  endpoint support collapses → 1 for N≥20; TV(random vs lex)=0.000 there.
- **t4: quotient-channel share** — twin channel T carries 91–99% of jumps;
  Q-share decays 0.76%→0.06% with N (finite-size residual, <1% at (24,48));
  Amendment-3 identity verified on 4,011 states (0 violations).
- **t5: algebraic activation rule** — **R1 survives**: regular with ≤3 distinct
  eigenvalues ⇒ aut ≥ N (0/389 violations across 368 twin-free atlas + 21 zoo);
  R2 has the single degenerate N=1 counterexample; R3 falsified (197/368).
- **t6: exact Burnside shell law** — orbit counts forward-computed for
  N=6 (32,768 labeled) and N=7 M∈{9,10,11} (999,362 labeled);
  **σ_q == σ_a exactly** (uniform-over-orbits = Aut-weighted labeled,
  Burnside duality); dynamics vs law TV=0.70–0.86 → dynamics does NOT sample the
  law, it over-selects the max-Aut shell (support 1 at large N).

---

## 6. THE CANON FIX — VERIFICATION SUMMARY

| Check | Method | Result |
|---|---|---|
| R1 iso-invariance | 1,000 random (10,15) iso pairs (random perm) | **1000/1000** same key (EX+all subscores) |
| R2 soundness | 300 networkx-non-iso pairs | **300/300** distinct (0 false merges) |
| R3 exhaustive relabel | N≤7, 40 graphs/cell, every perm applied | **235,425 relabeled pairs, 0 failures** |
| R4 brute oracle | true `N!` lex-min on 135 checks | 3/135 equal — expected (block-constrained lex-min is a valid iso-label, not always the global minimum); iso-class equality holds in all 135 |
| A/B vs reference | 880 graphs N=4..14 vs `canon_fixed.py` | **0 mismatches** (incl. 43 joint-fallback) |
| Third-party verifier | `canon_fixed_verification.py` (root) | 0/1000 + 0/300 |

Downstream artifacts all re-derived and saved (results/backups in
`phase_z35/`), ledgers updated (8.14), docs amended (`Z35_Z36_AUDIT_REPORT.md`,
`PHASE_Z35_REPORT.md`, `PHASE_Z33_REPORT.md` addendum, `PHASE_Z37_Z38_FORMAL_CLOSURE.md`
entries #1/#2), and the curated re-derivation lives in `CANON_FIX_FULL_REPORT.md` at root.

---

## 7. CHANGED-CORRECTED NUMBERS (summary table)

| Quantity | OLD | NEW (fixed canon) |
|---|---|---|
| Z37 t1 EX-key artifacts on iso pairs | 1395/2500 | **0/2500** |
| Z37 t1 genuine lex counterexamples | 1105 | 1105 (unchanged, canon-independent) |
| Z35 main n_steps | 10137 | **6329** |
| Z35 τ median | 8–10 | **7** (all modes; entropy→7, autmin→6) |
| Z35 H2 info gate | FAIL (τ>θ) | **PASS** (θ>τ: 0.1929 vs 0.1381; given: 0.2692 vs 0.2144) |
| Z35 Control B | n 3106 | 2162 |
| Z35 C2 lex | 0.243 | 0.421 |
| Z35 (8,12) | 2848 steps, τ 5–7 | 1708, τ 4–5 |
| Z35 (16,32) | — | random/lex/autmin bit-identical; entropy n 453→451 |
| Z35 Control D | G2 0.0311 / 1029 jumps / 5047 | G2 0.0313 / 1022 jumps / 4736 |
| twin-law I_tau vs I_deg | I_tau 0.3762 > I_deg 0.2468 | **I_deg 0.2227 > I_tau 0.1188**; P(Twin|var) now monotone 0.26/0.79/0.83 |
| Z33 (10,15) τ | 12/9/8/8 | 7/7/7/6 (folds 48→1440) |
| Z26 / Z27 | H_out 3.585 = log2(12); |Q_10,15|=136,433 | unchanged (canon-independent) |

**Not changed:** outcome B; H1/H3 gates; σ-limit-law and Burnside duality;
Shrikhande=192 and Rook=1152 (exact against the reference counter); Control-D's
twin-sole-channel verdict; the 91–99% twin-share; concentration < generation
(≈20× information gap).

**Caveats still open & factual, unchanged:**
- Z36 random-regular 15 rows are networkx-version-dependent (not reproducible);
- Z36 colored-quotient cap hides residual for qN>12;
- t1 τ* heavy tail past 64; exact id of the endpoint class; density-sweep slope
  (M/N dependence of the 1.92 slope) remain open research items.

---

## 8. WHERE THINGS STAND — DOCS / ARTIFACTS

| Item | Location |
|---|---|
| Full canon-fix report (curated, re-derived tables) | `CANON_FIX_FULL_REPORT.md` (repo root) |
| Z35/Z36 audit + canon-fix | `Z35_Z36_AUDIT_REPORT.md` (root) |
| Z35 phase report (ledger 8.1–8.14, L1 table) | `phase_z35/PHASE_Z35_REPORT.md` |
| Control D protocol/results | `phase_z35/z35_control_d.md`, `z35_control_d_results.json` |
| Twin-law re-run + backup | `phase_z35/z35_twin_creation_law_rerun.json`, `…_results_original_pre-canonfix.json` |
| Fix engines | `phase_z25/z25b_engine_v2.py`, `phase_z25/z25b_relational_engine.py` |
| Reference & verifier (cross-checked) | `canon_fixed.py`, `canon_fixed_verification.py` (root) |
| Z33 addendum | `phase_z33/PHASE_Z33_REPORT.md` |
| Z37 closure / prereg | `phase_z37/PHASE_Z37_Z38_FORMAL_CLOSURE.md`, `Z37_PREREGISTRATION.md`, `results/*.json` |
| Related work (ER 1963, MacArthur–Anderson, Burnside process) | `RELATED_WORK.md` (root) — closes the OPEN CROSS-CUTTING GAP |

The Z37 closure has absorbed the t1 EX-artifact fix, so the Z37 numbers above
(t1/t2/t3/t4/t5/t6) are all **after** the canon fix. Everything canon-keyed is
re-derived and verified; only the honest research questions in §7's caveats
(τ* tail behavior, exact identity of the endpoint class, density-dependence of
the τ∝N slope) remain genuinely open.
---

## Z42 addendum (2026-08-03) — Cl(10)×E8 intrinsic constraint, generalized no-go

Full detail: `phase_z42_joint_intrinsic_constraint/`.

**TL;DR:** extends Z39 (E8 cubic Casimir, single flavon, closed
negative) and Z40 (multi-flavon Cases A–C, closed negative) from
"tested for these specific invariants/cases" to a general L2 theorem:
under the standing `E8 ⊃ E6 × SU(3)_f` branching assumption, **no
order** of E8 structure constants can produce a non-degenerate
3-generation Yukawa texture from a single SU(3)_f flavon, because (1)
the full adjoint 248's SU(3)_f content is exhausted at `{1,3,3̄,8}`
(new check — previous phases checked only the `(27,3)` matter piece),
and (2) the classical First Fundamental Theorem of SU(3) invariant
theory (Weyl 1939) means that representation content alone fixes the
entire invariant ring as generated by `δ` and `ε`, at any degree.

Freedom count (new, not previously tabulated): a single-flavon
construction delivers ≈1 physical real degree of freedom against a
≈10-parameter physical target per fermion sector (6 masses + 3 mixing
angles + 1 phase) — an order-of-magnitude shortfall, not a near-miss.

**Net effect: Thread 1 status unchanged at 0/19 SM parameters
derived.** This phase closes the "try another E8 invariant" branch of
the search generally rather than case-by-case. It does not open a new
research direction on its own. Two escape routes remain, both already
flagged in prior sessions and not attempted here: (a) non-factorized
generation space (NCG/spectral-triple route, Priority 1, needs tooling
this environment lacks), (b) alternative E8 maximal-subgroup chains
other than E6×SU(3)_f (never tested at any phase).

Per Z42's own instructions, no Z43 phase is opened unless one of those
two reveals a genuinely new mathematical object.
