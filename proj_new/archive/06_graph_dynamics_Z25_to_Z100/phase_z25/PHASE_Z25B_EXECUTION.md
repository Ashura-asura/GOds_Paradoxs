# PHASE Z25-b — FOUR HARD QUESTIONS — EXECUTION REPORT

**Status:** Rule-8 CLOSED · 2026-08-02
**Location:** `C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z25\`
**Engines:** `z25b_engine_v2.py` (declared engine), `z25b_seed_sweep.py`, `z25b_edgecount_sweep.py`
**Scope:** all artifacts in the isolation folder; `gods_paradox` untouched.

GPU was offered by the user. Declined: the bottleneck is a combinatorial
(vertex-relabeling) search, not floating-point. Correct fix was memoized
canonicalization + WL-restricted relabel search; full grid now runs in seconds.

Design changes vs Z25 (all admitted as design inputs, Rule 9):
1. witness/permutation machinery REPLACED by conservative edge exchange
   (non-monotone structure, always-M conserved) -> multiple recurrent classes
   can coexist.
2. canonicalization via WL color refinement + budget-capped exact search
   (deterministic INV key fallback when search budget exceeded; fallback is
   a deterministic iso-invariant so cycle detection stays well-defined).
3. observables measured WITHIN each attractor cycle (min over cycle states).

Engine T (unchanged between v1/v2): edge exchange by endpoint degree-sum
ordering, tie-broken lexicographically; balance vs contrast chosen by scalar p.

## The four hard questions — data

### Q1. Does the attractor produce non-trivial universal ratios?
**No.** No ratio survives as a universal across the seed sweep:
- p=0 (M=15 seeds): ratios concentrate at {2/5 (5/6 share), 2/3 (1/6)}, and
  at M=10 / M=35 the attractor flips entirely (n3/n4 undefined at M=10 —
  0-cycles; 0.2292 at M=35). So the attracted value is graph/EULER-density
  controlled, not a constant of the dynamics.
- p=1: across 12 random (10,15)-seeds, 8 distinct basins with ratios
  {0, 1/2, 2/3, 3/4, 1, 3, undef} — nothing universal.

### Q2. Are the ratios robust across initial seeds?
**Partially, and only in a seed-conditioned sense.** Everything observed is a
period-2 attractor. Within a fixed (N, M, topology-anchor) family at p=0 the
dominant basin is robust (share 5/6), but ACROSS seed graphs the attractor set
fragments (12 seeds -> 12 distinct keys, n_basins=12, dominant share 1/12).
So robustness is real only at the level of "concentration behavior," not of
"same output."

### Q3. Does one small input generate more information than it contains?
**Criterion sharpened mid-investigation (declared):** witness-free conservative
dynamics can only permute within a finite orbit; N_out bits <= log2(#reachable
states) <= encoding of (rule + seed + p). On that sharpened criterion:
- Rule/p contain ~no bits beyond the ledger declaration.
- The dynamics output bits are bounded by the state-space entropy and the
  output ratios are rational-informative but not novel: every ratio observed
  is recomputable from the seed's own counts after a period-2 collapse.
So the surplus claim is **not met**: useful compression at best (a "coin" that
concentrates mass on structurally-allowed attractors), not generation. This
echoes, one level up, the Z24 homogeneity lemma: nothing nonlinear is being
added by T; T only projects.

### Q4. Does A8 (no hidden tuning) survive?
**Yes.** Verified structurally:
- No energy / potential / symmetry term in T; balance-vs-contrast rule is
  a fixed counting rule.
- No SM number anywhere in the code paths.
- p does not select among universals — at best it shifts basin shares, and
  the endpoints collapse the ratio spectrum.

## Verdict

PARTIAL (revised from engine's raw print label).

Structure emerges (stable attractors, computed Aut groups as large as 1440,
non-trivial local ratios). But:
- universality fails (Q1),
- robustness across seed graphs fails (Q2),
- generative-surplus fails under the sharpening (Q3),
and the ledger "N_in=1 -> N_out" claim collapses because the observed outputs
are seed-conditioned — the seed graph + (N, M) are themselves unaccounted
inputs carrying the actual selection information.

This is the relational-engine instance of the Z24 Master No-Go: invariant-/
counting-driven dynamics do not add selection information; they expose the
information already encoded in boundary conditions (here: the seed graph,
N, M, and the exchange rule's degree convention).

## Rule compliance log
- Rule 1 no numerology: PASS.
- Rule 2 no reverse engineering: PASS (T fixed before runs).
- Rule 3 L-labeling: L1 = numeric tables above; L2 = diagnosis of
  concentration-as-compression; the min-over-cycle invariant choice is an
  assay convention declared here.
- Rule 6: seed graph & (N,M) are design bits, declared.
- Rule 8: closed avenue recorded.
- Rule 9: ledger after Q3 sharpening = N_in >= N_out.

## Visualization data (for the user's plotting step)
All raw numbers are in the run logs above. For a basin-landscape figure:
x=p, y=basin share, z=ratio_n3_n4; or a histogram of attractor ratios across
seeds at p=0 vs p=1 — both directly formed from the tables printed in runs.
