# Z37+ FORMAL CLOSURE PROGRAM — PRE-REGISTRATION (Rule-2, 2026-08-03, BEFORE any run)

Converts the Z25–Z36 empirical mechanism into theorem-level structure. Six tasks, one
deliverable: `phase_z37/PHASE_Z37_Z38_FORMAL_CLOSURE.md`.

Global conventions (identical to Z35): jump = |Aut| ratio >= 4.0; |Aut| via Amendment-3 v2
counter (validated 3817/3817); Theta via twin_potential; canon via z25b_engine_v2 (EX exact /
INV deterministic-iso-invariant; key type always recorded); selectors from z33 step_mode with
Amendment-4 patch; RNG formula SEED0 + 131*s + 991*len(mode) per chain.

---

## TASK 1 — Formalize the tie-collapse theorem

**Attempted theorem.** Let T_tau be the extremal exchange operator with tie-break tau on
labeled G(N,M), and c the graph-isomorphism canon (Z27: c(g1)=c(g2) iff iso). Claims:

- 1A (set-level iso-invariance): the extremal candidate SETS R(g), A(g) are iso-invariant.
- 1B (well-definedness on quotient): the quotient map Phi = c ∘ T_tau is well-defined iff
  tau is iso-invariant (if tau depends on vertex labels, iso copies can map to different
  quotient states).
- 1C (collapse): under an iso-invariant tau, quotient orbits are periodic with short period;
  the "collapse" is then (i) the quotient projection (always true, Z27), (ii) tie-break
  selection of a cycle inside the tie shell (Z30), (iii) dynamics: chains from uniform seeds
  concentrate on few attractor classes.
- Separation A/B/C: A = quotient projection; B = label-dependent tie-break (lex) makes the
  collapse selector-specific; C = genuine dynamics tested by support concentration under the
  iso-invariant tie-break tau* (lex on canon keys of candidate edges).

**Computational verification (budgets):**
- V1: 200 random (10,15) states x 3 random permutations each: verify R,A identical under iso.
- V2: 500 states x 5 perms: search for lex counterexample c(T_lex g) != c(T_lex g'); only EX
  canon keys used (INV keys recorded separately, not counted as counterexamples).
- V3: 500 states x 3 perms under tau*: verify Phi well-defined (expect 0 violations).
- V4: 200 chains from uniform seeds under tau* at (10,15), cap 64: period distribution and
  endpoint support size (vs lex support).
- GATE: V2 expected to FIND counterexamples (lex is label-dependent) -> B confirmed; V3
  expected 0 -> 1A/1B confirmed for iso-invariant tau*.

---

## TASK 2 — Twin formation probability law

**Event:** E = theta1 > theta0 on one exchange step (twin gain).

**Cells/budgets:** (10,15): random 400 chains, cap 128. (16,32): random 200 chains, cap 128.

**Features per step (no curve fitting, no invented combos):** R = |R|, A = |A|, FREEDOM =
|R|*|A|, DEGVAR = variance of the degree sequence, DU,DV = degrees of the added pair
endpoints, CN_ADD = common neighbors of the added pair (before adding), CN_REM = common
neighbors of the removed pair, TH0 = theta before the step.

**Procedure:** mutual information I(E; f) per feature (8-bin equal-count binning, exact
entropy from counts); ranking; then greedy forward selection: add feature maximizing joint
MI (2D histogram), stop when the incremental gain < 5% of H(E). Report minimal sufficient
set.

**Hypothesis H_T2:** I(E; CN_ADD) is the largest single feature MI (neighborhood-overlap
mechanism, per Z26's "neighborhoods become more similar"). NOT a gate; recorded either way.
Gate: report only; no accept/reject — Task 2 is a measurement task.

---

## TASK 3 — Scaling window

**Cells:** (16,32),(20,40),(24,48),(30,60),(40,80). Budgets (random/lex/entropy/autmin):
(16,32),(20,40): 30/5/5/5; (24,48): 25/4/4/3; (30,60),(40,80): 20/3/3/2. Caps: 256 at
N<=24, 192 at (30,60), 160 at (40,80). autmin chains use Amendment-4 patched counter.

**Metrics per chain:** tau (cycle-entry step), t_nucl (first step with theta1 > theta0),
log-slope of |Aut| vs t over the transient (OLS on t < tau), endpoint canon key.

**Per cell:** median tau, median t_nucl, median slope, endpoint support (#distinct keys),
selector divergence (TV between endpoint distributions over selectors).

**Question (pre-registered interpretation):** median tau as a function of N. Fit
tau ~ const, tau ~ a*N, tau ~ a*exp(bN) on the 5 medians; report all three fits' r^2 and
the implied exponent. No gate; honest report.

---

## TASK 4 — Quotient-channel jump partition

**Identity used:** |Aut(G)| = twin_aut x q_aut EXACTLY (Amendment 3; twin_aut = prod
|C_i|!, q_aut = aut // twin_aut — integrality verified per state; violations = theorem
failure, counted). Component factor is subsumed in q_aut (isolated vertices are twins).

**Cells/budgets:** (10,15): random 300 + lex 100 chains, cap 128. (16,32): random 200 + lex
50, cap 128. (24,48): random 100 + lex 25, cap 128.

**Per jump:** twin_factor = twin_aut1/twin_aut0, q_factor = (aut1/aut0)/twin_factor.
Class: T (twin_factor >= 4), Q (q_factor >= 4 and twin_factor < 4), M (both >= 4),
S (neither, product >= 4).

**Question:** Q-jump share per cell — grows/decays with N? Pre-registered interpretation:
if Q-share >= 5% at (24,48) or rising with N -> quotient channel is a second nucleation
mechanism; if decaying -> finite-size residual (Control D found 3.1% dtheta=0 quotient jumps
at (16,48) seeds; main cell P(dt>0|J)=0.998 tail 0.2% is the same class).

---

## TASK 5 — Algebraic symmetry activation theory

**Goal:** predict |Aut(Q)| for twin-free graphs WITHOUT computing |Aut|.

**Zoo (deterministic constructions):** C_n (n=5..10), Petersen, Shrikhande, Rook 4x4,
complement-Shrikhande, Heawood (14,21), hypercube Q4, K4,4, K3,3, rook 3x3, Kneser KG(6,2),
triangular T(6) = line graph of K6, circulants C16(1,3,5), octahedron, icosahedron,
dodecahedron, prism C5xK2, complete graph K5. Plus networkx graph atlas N<=7 (1253 graphs)
— only twin-free members used for the algebraic-channel tests.

**Features (no Aut):** num_distinct_eigenvalues, max eigenvalue multiplicity, WL-depth
(refinement rounds to stable coloring), diameter, girth, is_regular, distance-regular flag
(intersection-array check), common-neighbor concentration (distinct lambda values, distinct
mu values).

**Reference |Aut|:** v2 counter (validation only).

**Rules under test (pre-registered):**
- R1: (regular AND num_distinct <= 3) => |Aut| >= N.
- R2: (WL-depth <= 2 AND regular) => |Aut| >= 2.
- R3: (twin-free AND |Aut| >= 2) => num_distinct <= N/2 + 1 (algebraic channel implies
  spectral compression).
**Gate:** a rule survives only with 0 counterexamples over atlas-twin-free + zoo. All
violations recorded as Rule-8 entries.

---

## TASK 6 — Burnside shell law (exact, no sampling)

**Exact exhaustive enumeration** (canon + shell (R,A) + |Aut| per orbit rep):
- N=6, ALL M (2^15 = 32768 labeled states).
- N=7, M in {9,10,11} (999,362 labeled states).
All 8-bin shell laws computed exactly on the QUOTIENT: sigma_q (uniform over orbits),
sigma_l (uniform over labeled), sigma_a (Aut-weighted = labeled draw weight, proportional to
|Aut|).

**Validation:** sampled Aut-weighted estimator at (7,10): 20,000 labeled draws vs exhaustive
truth (TV distance).

**Dynamics comparison:** run the extremal dynamics at (6,9),(7,10),(7,11): random 100
chains, cap 64. Record attractor shell (|R|,|A|) distribution and endpoint |Aut| median.

**Question:** does the dynamics converge to the shell of max-Aut-DENSITY (mean |Aut| over
orbit reps) or to the shell of max Burnside PROBABILITY density (sigma_q or sigma_a mode)?
Compare attractor shell vs both; pre-registered interpretation: whichever shell the
attractor occupies (with TV <= 0.2 to its law's peak bin) wins.

---

## DELIVERABLE
`phase_z37/PHASE_Z37_Z38_FORMAL_CLOSURE.md` — sections: proven / falsified / theorem
candidates / counterexamples / scaling / final mechanism diagram / remaining unknowns.
Ledger entries (Rule-8) for every failed hypothesis and every counterexample found.

## RULES HELD
Rule-1 no numerology (fits reported with r^2 and sample sizes, never as "laws" without
gates); Rule-2 this document precedes all runs; Rule-3 L1/L2/L3 separated in the report;
Rule-4 failures recorded equally; Rule-5 no conjecture upgraded without adversarial tests
(the gates above ARE the adversarial tests).
