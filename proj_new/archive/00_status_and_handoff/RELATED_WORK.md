# RELATED WORK — Graph-Dynamics Thread (Z25–Z38)
Status: 2026-08-03. Fills the OPEN CROSS-CUTTING GAP in PROJECT_STATE_HANDOFF.md.
Everything here upholds GROUND_RULES.md: every claim carries an L1/L2/L3 label
(Rule 3); no claim of novelty is made without stating what it would have had to
fail to reproduce (Rule 9); closed avenues are reported as results (Rule 8).

Scope: the extremal edge-exchange dynamics (phase_z25/z25b_engine_v2.py and
relatives), its symmetry-attractor results (Z30–Z36), the canonicalization
layer (WL color refinement, EX/INV canon, twin/tie analysis), and Z37's
exact orbit-counting / Burnside comparison (t6, z37_closure.py).

---

## 0. What this section does and does not claim

- **This documents prior art and positions the repo's results against it.**
  It does not argue that the repo's dynamics is "new to the world". Where the
  repo's process is a specific special case of something already studied, that
  is stated (L2, cited). Where the repo measures something not addressed by
  that work, the difference is stated, checked against the baseline, and
  labelled honestly (L1 where forward-derived here, L3 where unproven).
- Baseline for any "the dynamics selects symmetry" claim is the classical
  null: **uniformly random graphs are almost surely asymmetric
  (Erdős–Rényi)**. Every symmetry-related headline in this repo is only
  meaningful as a *statistical deviation from that null*.

---

## 1. Baseline: random graphs are almost surely asymmetric
Reference: Erdős, P., Rényi, A., "Asymmetric graphs", Acta Math. Acad. Sci.
Hungar. 14, 295–315 (1963). [L2 — verified against the cited paper and the
standard statement in the literature, not re-derived here.]

- Statement (ER 1963, Thm 1): for a graph drawn uniformly at random on n
  labeled vertices, the probability that its automorphism group is trivial
  (a.s. no non-identity automorphism) → 1 as n → ∞. Generalized by
  Bollobás ("Rigid iterations"): almost all graphs are *rigid*.
- Companion complements: almost all **trees** have automorphism group of size
  ≥ 2 ("almost all trees are symmetric"); the countably-infinite random
  graph (Rado graph) is automorphism-transitive.
- **Positioning of this repo (L1, Z32/Z35 separates):** the repo measures
  |Aut| of graph states reached by *extremal edge exchange at fixed (N,M)*,
  not sampled uniformly. Z32 **refuted** the trivial alternative
  ("outcome A" = pure quotient geometry + bookkeeping selector; TV from both
  static reference layouts = 1.0): the attractor states the dynamics reaches
  sit at |Aut| = 1,440 / 2,880 / 17,280 (mean ~900–2,300; uniform random
  draws at the same (10,15) never exceed |Aut|=48 in 40,000), with a
  labeled-draw probability ≈ 2×10⁻⁵ — if the dynamics
  sampled the ER/Latin uniform ensemble, a.s. asymmetric states would
  dominate, which is not what is observed (Z32–Z33 front-loaded staircase).
  The comparison is the *null baseline*, not evidence of a conflict: a rule
  that maintains M and prefers extremal exchanges is not the uniform model,
  so ER's a.s.-asymmetry does not anti-predict its attractor; it sets the
  default expectation the rule must beat. That it beats it (twin
  formation P(E)≈0.08, near-constant across cells; twin-driven
  jump-staircase) is the fact to be explained.

## 2. Symmetry formation in self-organizing networks (preferential growth)

Reference: MacArthur, B. D., & Anderson, J. W., "Symmetry and
Self-Organization in Complex Systems", arXiv:cond-mat/0609274 (2006).
[L2 — verified against the arXiv abstract and letter text.]

- Result: real-world complex systems (biological regulatory networks, the
  Internet) display conspicuously rich automorphism groups, in contrast to the
  classical ER baseline of §1. Growth with **preferential attachment** in
  *tree-like* growth (k=1 new edges per new vertex) drives automorphism
  growth (exponential, a ~ σ(α)^N; σ(α) increases with the exclusiveness α),
  whereas k ≥ 2 (branching) drives asymmetry at large N. Uses nauty for
  automorphism computation.
- **Difference from this repo (explicit, L1):** M&A's driver is (a) an
  **open, growing** system (N increases, new vertices/edges arrive) and (b)
  **preferential attachment** (α). This repo's mechanism is a **closed,
  fixed-(N,M)** edge-count-conserving **exchange** driven by an *extremal
  (degree-sum-driven) tie rule with a scalar p* — no growth, no new vertices,
  no preferential-attachment preference on the global degree rank that their
  model uses. The common conclusion is qualitative: both engineer dynamics
  that restructure toward more symmetric states than the uniform ensemble.
  The *driver differs*. (L1: process difference is by construction; the
  repo's symmetry-concentration numbers are forward-computed.)

## 3. Orbit-uniform sampling — Burnside process and orbit counts
Reference: Jerrum, M., "Uniform sampling modulo a group of symmetries using
Markov chain simulation", DIMACS Series in Discrete Math / LACS Report
ECS-LFCS-93-272 (1993); L. A. Goldberg & M. Jerrum, "The Burnside process
converges slowly", Combinatorics, Probability & Computing 11 (2002).
[L2 — verified against citing literature.]

- The Burnside process is a Markov chain on the underlying space X of
  the group action, sampling (after lumping to orbits G×X) uniform on the
  orbits → an MCMC algorithm for unlabeled/orbit sampling via
  Aut-stabilizer steps. Mixing is rapid in special cases, proven slowly
  occasionally (Goldberg–Jerrum).
- **Where this repo's Task 6 sits inside this literature (L3 — positioning):**
  t6 (z37_closure) compares three orbit-distributions: σ_q (uniform over
  unlabeled classes), σ_a (Aut-weighted labeled), σ_l (uniform over labeled
  states) and the dynamics' empirical distribution, establishing the
  Burnside duality σ_q == σ_a exactly at forward-computed N=6 and N=7 for
  selected M. That trio comparison *is* comparative-probability-on-orbits;
  it does not use the Burnside process as an algorithm. If the repo's
  dynamics is ever posed as a sampler, it is a specific "extremal-exchange"
  chain — not the Burnside construction — and its mixing behavior is
unexplored (L3). The terminology "Aut-weighted shell law" / "Burnside
  duality" should cite Jerrum-related work instead of using the repo's
  private σ_q/σ_a/σ_l notation without attribution; that is the purpose of
  citing this node here.
- Honest caveat: the behaviour the repo observes (dynamics over-selects the
  max-Aut shell, TV=0.70–0.86 vs the law) is *not* evidenced for small
  finite N only; it is a statement about the walk direction, not a mixing
  result about the Burnside chain.

## 4. The canonicalization layer — known prior work
- WL(1) color refinement (Weisfeiler–Leman), used as canon/INV key, is
  classical: B. Weisfeiler & A. Leman 1968; treated by Kiefer, Grohe, etc.
  (L2). The repo uses it as an iso-partition refinement; it does not claim
  new WL results.
- Practical canonical-labeling algorithms: nauty (McKay 1981),
  Traces (McKay & Piperno 2014) (L2). This repo's
  canon is a budget-capped exact lex-min over WL-blocks, does not attempt to
  compete with nauty/Traces, and only uses canon for set/dict membership
  (verified via grep across ~60 call sites — none use it for ordering).
  (L1/Repo-proceeding.)

## 5. What this repo can claim that the above cannot (honest, self-audited)
1. **Fully fixed-size, closed-strategy extremal exchange** as a
   symmetry-selector run to attractor/cycle, with state-of-|Aut| tracked
   exactly on all states (backtracking-based exact |Aut|, Z32; interchange
   validated 3817/3817). The prior-art self-organization literature is
   growth-based; this exact closed-space case with automorphism-count
   tracking is not found in the cited work. (L1 measured; novelty is a
   literature claim, L3.)
2. **Twin-restructuring as the whole jump convolution** (Z34, Z35 θ
   near-Lyapunov, twin-channel share 91–99%; Control D). No cited work that
   measures the *jump channel* decomposition of extremal-edge-exchange
   dynamics with twins identified. (L1 measured; "not in cited work" L3.)
3. **The canon-fix** (2026-08-03) belongs to isomorphism-hunting of the
   repo— retract "the algorithm is new": the fix is the *correct* use of
   WL-blocks and (N,edges) keying, both standard; the bug it fixes was a
   repo-internal error. Nothing here is a mathematical novelty; it is a
   correctness restoration, recorded as such under Rule 8.
4. **No numerology / Rule-9 check:** any "the dynamics produces symmetry"
   headline is validated only if the *same* measurement, run on a
   retained-p control (Control B reversed-extremal) or on a fixed uniform
   sampler, *fails* to reproduce it. Control B (the exact protocol's
   reversed-extremal direction) is negative — jumped coupling destroyed,
   P(dt>0|J)=0.431, ctrlB P_J gate NOT met. This is the discriminating-power
   audit the repo already applies; it is restated here so the related-work
   reading is complete.

## 6. Conclusion
Known-and-proven: WL refinement, canon-block labeling, ER asymmetry
baseline, preferential-attachment symmetry growth, Burnside/orbit-sampling
Markov chains. This repo neither claims to extend those nor, in honesty,
proves a fundamentally new class of result: its claim is bounded: a specific,
fixed-(N,M), extremal, twin-driven dynamics with exact |Aut| tracking, whose
attractor concentrates on the max-Aut shell more than classical sampling
does. No quantity here is fitted to a literature value; where a number agrees
with an external law (Burnside identity), it is forward-computed and labelled.
## 7. Thread 1 addendum (Z42, 2026-08-03) — classical invariant theory

The Z42 no-go generalization (see
`phase_z42_joint_intrinsic_constraint/`) rests on one additional cited
result not previously listed here:

- **Weyl, H. (1939), *The Classical Groups: Their Invariants and
  Representations*, Princeton University Press, Ch. II §6** — the First
  Fundamental Theorem of invariant theory for SL(n,C)/SU(n): the ring
  of polynomial invariants of any number of copies of the fundamental
  and dual representations is generated by contraction (delta) and the
  determinant tensor (epsilon) alone, with no generators at any other
  degree. This is the load-bearing citation for Z42 Task 5's theorem;
  it is cited, not re-derived (a from-scratch computer-algebra proof
  would need invariant-theory tooling this environment doesn't have —
  named explicitly as a gap in `phase_z42.../audit_report.md`).
- Branching table `E8 ⊃ E6 × SU(3)`: **Slansky, R. (1981), "Group
  Theory for Unified Model Building," Physics Reports 79(1), Table
  82.** Already implicitly used since Z6; this is the first phase to
  cite it explicitly as the source of the branching table used
  throughout.

No numerology check (Rule 9, restated per the convention in section 5
above): Z42's theorem is falsifiable in a concrete way — finding any
SU(3)_f irrep beyond {1,3,3̄,8} in a *different* E8 maximal-subgroup
branching, or a working non-factorized (NCG) construction, would
directly break its hypothesis (A1). Both are named as explicitly
untested escape routes, not swept under "closed."
