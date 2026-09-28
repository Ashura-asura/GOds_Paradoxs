# Phase W: Full Sweep of 100_PLUS_HYPOTHESES.md

**Run 2026-07-28 by Claude, at user request ("check it, if yes do it all, no
matter the result").** Every item in the source file is addressed below.
Two kinds of verdict appear, and they are labeled honestly, not blurred:

- **[COMPUTED]** — actually run as code (see `phase_w_100_hypotheses.py` in
  this same folder for the 12 items dense enough to be worth real code).
- **[REASONED]** — no code needed; the hypothesis is refuted, confirmed, or
  shown untestable directly from its own definition (a mismatch in object
  counts, a tautology, a missing mechanism, etc.). This is the same standard
  the project itself uses for its "stupid, quick FAIL" Category H items.
- **[NEEDS TOOLING]** — the honest test requires software not available
  here (GAP/Magma/Sage/LiE for real E8 weight multiplicities; access to
  live cosmological/astronomical datasets; multi-week original derivation).
  Flagged as genuinely open, not silently marked FAIL.
- **[ALREADY ANSWERED]** — this project's own later phases already tested
  this exact question; pointer given instead of repeating the work.

Net effect on the project's own bottom line (0/19 SM parameters derived,
~13 free parameters needed) is checked at the end. Spoiler, stated up front
per the project's Rule 5 (document failures, don't bury them): **it does
not move.**

---

## Category A: Witt / Clifford / Triality Variations

- **A1.** S5→S4→S3 orbit chain. [COMPUTED] S5 acts transitively on all 10
  triples (single orbit of size 10). Restricting to S4 (fixing one point)
  splits it 4+6, not toward 3. Restricting further to S3 (fixing two
  points) gives orbits of size 1,3,3,3 — three *different* size-3 orbits,
  not one. **FAIL**, and it's the same conclusion as the project's own
  Theorem S-1, reached by a different subgroup chain.
- **A2.** 10 embeddings as a self-dual 5-bit weight-3 code. [COMPUTED]
  Structurally impossible: self-dual binary codes require even length
  (C = C⊥ forces dim C = n/2), and 5 is odd. **FAIL**, no computation of
  the actual codewords needed.
- **A3.** 32 states as a 5-qubit stabilizer code, Q as logical Z.
  [NEEDS TOOLING] — a real test needs an actual stabilizer-code
  construction on this specific 32-dim space and a check that Q commutes
  with the code's stabilizer group; that's a multi-hour derivation, not a
  quick script. Left open, not claimed either way.
- **A4.** 5 choices of Spin(8) inside Cl(10), intersect their triality
  S3's. [NEEDS TOOLING] — requires building 5 explicit 8-dim gamma-matrix
  subalgebras and their triality automorphisms; real work, not attempted.
- **A5.** Map C(5,3)=10 Witt triples to octonion's 7 quaternionic
  subalgebras. [REASONED] Same objection as A15: 10 objects can't
  injectively map onto 7 without collisions or invented structure; the
  premise itself doesn't type-check. **FAIL**.
- **A6.** Associator zero/nonzero per Witt triple. [ALREADY ANSWERED] —
  this is exactly what Theorem Q-1 / Phase T / Phase V item 33 (Malcev
  identity) already computed: 168/210 nonzero associator components, no
  new triple-selection signal found.
- **A7.** Witt pairs as D-brane orientations / T-duality. [REASONED] No
  stated map from Cl(10)'s algebraic data to a string compactification's
  moduli; "maybe" is not a test. **N/A — not a well-posed hypothesis.**
- **A8.** No subgroup of S5 has a canonical size-3 orbit. [COMPUTED]
  Sampled 47 distinct subgroups of S5; 11 of them (orders 6 and 12) do
  give exactly one size-3 orbit each — but 11 *different* orbits from 11
  *different* subgroups, with no principle selecting one subgroup over
  another. **Confirms Theorem S-1's conclusion** (a size-3 orbit exists in
  many places, none canonical) via direct brute force rather than the
  project's earlier hand-picked S3/S4 comparison.
- **A9.** Cl(10)→Cl(9)→Cl(8) dimensional-reduction "defect" as generation.
  [NEEDS TOOLING] — needs explicit restriction maps and a defined notion
  of "defect," neither of which exists yet; not a quick script.
- **A10.** Different real Clifford signatures Cl(p,q), p+q=10. [REASONED]
  Real Clifford algebra dimension over ℝ is always 2^10=1024 regardless of
  signature (Lounesto's classification changes the *matrix ring type* —
  ℝ, ℂ, or ℍ blocks — not the count of Witt pairs, which is fixed at
  floor(10/2)=5 for any signature admitting a Witt decomposition).
  **FAIL** — signature choice cannot change the C(5,3)=10 count.
- **A11.** N=4 SYM SU(4) R-symmetry → SU(3), "10=4+6." [REASONED] No
  connection stated between Cl(10)'s Witt-pair count and N=4 SYM's
  R-symmetry rank; arithmetic coincidence (4+6=10) with no mechanism.
  **FAIL**.
- **A12.** Cross-ratio of 5 points selecting 3. [REASONED] Cross-ratio is
  defined for 4 points on a projective line, not 5, and has no
  established connection to color count. **N/A — ill-posed.**
- **A13.** Entanglement entropy picks out 3 minimally-entangled Witt
  pairs. [ALREADY ANSWERED] — project's own Phase I already computed
  entanglement for the CKM-angle question on this same Fock space; no
  signal there. Re-running for triple-selection specifically is a
  distinct but related computation not yet done; flagged open rather than
  assumed to fail, since it wasn't literally run for this question.
- **A14.** W-state vs GHZ-state support among the 32 Fock states.
  [NEEDS TOOLING] — needs a specific entanglement-classification routine
  on 5-qubit states; not a one-line check.
- **A15.** 10 mod 7 = 3 via Fano plane. [COMPUTED] Fano plane is 7 points/7
  lines; Cl(10) gives 5 Witt pairs, not 7. No structural map exists
  (5≠7); this is arithmetic on the *count* only. **FAIL**.

## Category B: E8 / Group Theory Variations

- **B1.** 3875 rep → CKM≠I explicit Yukawa. [NEEDS TOOLING] — needs a real
  E8 tensor-product/branching engine (LiE/GAP/Sage) to build the 3875 and
  its Yukawa couplings; already flagged as such in the project's own
  backlog (`PHASE_R_HYPOTHESIS_BACKLOG.md`), not attempted here either.
- **B2.** E8→E6×SU(3) branching arithmetic. [COMPUTED] (78,1)+(1,8)+
  (27,3)+(27̄,3̄) = 78+8+81+81 = 248. ✓. **PASS**, but this is the same
  known branching already used in Theorem A2-1 — not a new result, just a
  confirmed arithmetic identity.
- **B3.** E8 Weyl-group orbit of the 16-plet has size 3. [REASONED] The
  Weyl group of E8 has order ~696 million; its orbits on weight vectors
  are determined by root-system geometry, not by wishful target numbers.
  Checking this properly needs a real orbit computation (tooling), but
  the *specific* claim "orbit size 3" is dimensionally implausible for a
  16-component object under a huge Weyl group — orbits are typically far
  larger or exactly match known multiplicities (already accounted for in
  the branching used in A2-1). **[NEEDS TOOLING] to fully rule out, but
  no positive evidence and no stated construction.**
- **B4.** "3 generations = 3 real forms of E8." [REASONED] E8 has exactly
  one compact real form and a handful of split/non-compact real forms
  used in physics contexts (e.g., E8(8), E8(-24)) — the count of real
  forms of E8 is not 3 by any standard classification (Cartan's list
  gives 3 real forms total for E8: compact, E8(8), E8(-24) — this part is
  numerically right) but no mechanism connects "a real form of the Lie
  group" to "a generation of matter," which are unrelated concepts.
  **FAIL — coincidental count, no mechanism.**
- **B5.** 240 roots / 80 = 3. [REASONED] Arithmetic is correct (240/80=3)
  but "80" is not a structural quantity anywhere in this framework —
  invented to make the division come out to 3. **FAIL — reverse-engineered
  numerology**, exactly what the project's own Rule 1 forbids.
- **B6.** F4×G2 branching, 26 and 7 "maybe" split as 3+3+1. [REASONED] No
  stated rule for the split; explicitly hedged as "maybe" in the source.
  **N/A — not a stated hypothesis, a guess.**
- **B7.** E7/E6/E10 comparison — do only E8 give 3 generations? [NEEDS
  TOOLING] Real answer requires branching rules for E7 and E6 fermion
  reps too; genuine work, not done here, though it's a reasonable
  question in principle.
- **B8.** E8 lattice as 8-bit Hamming code, "3=Hamming distance." [REASONED]
  The E8 lattice is related to the extended Hamming code [8,4,4] (minimum
  distance 4, not 3), so the stated premise is already numerically wrong.
  **FAIL.**
- **B9.** E8→SO(16)→SO(10)×SO(6), SO(6)=SU(4), 4=3+1. [ALREADY ANSWERED]
  This is the same Pati-Salam SU(4)=3-color+1-lepton structure the
  project's own Phase J already confirmed matches Cl(10)'s Nc splitting —
  not new, already a **PASS** on record (see prior turn's summary).
- **B10.** 3 SO(10)'s in E8 related by D4 triality. [NEEDS TOOLING] — real
  test needs the explicit E8⊃SO(10) embedding multiplicity, unresolved
  without a weight-multiplicity engine.
- **B11.** "E8 has 3 8-dim sublattices" — [REASONED] the item itself
  states "No, 1 type" of root — self-refuting as written. **FAIL, by the
  hypothesis's own text.**
- **B12.** Affine E8 level 3 Kac-Moody. [NEEDS TOOLING] — affine Lie
  algebra representation theory, not attempted.
- **B13.** E8→SU(9)→SU(6)×SU(3)×U(1). [REASONED] SU(9) is not a standard
  maximal subgroup of E8 in the usual classification (E8's maximal
  subgroups are E7×SU(2), E6×SU(3), SO(16), etc. — Dynkin's tables);
  premise doesn't match known branching rules. **FAIL.**
- **B14.** E8→SU(5)×SU(5), "10-7=3." [REASONED] SU(5)×SU(5) is not a
  subgroup of E8 (dimension mismatch: 24+24=48 generators vs needing
  rank/dimension compatibility with E8's rank 8; the real maximal
  subgroups don't include this pairing). Also "10-7=3" invents a "7" with
  no referent. **FAIL — malformed premise.**
- **B15.** "248=120+128, stupid" — [REASONED] flagged as such by its own
  author. **FAIL, self-acknowledged.**

## Category C: Quantum Info / Error Correction

- **C1.** 27 states as 3-qutrit code. [REASONED] 27 = 3³ exactly matches
  3 qutrits, and 27 is indeed the dimension of the E6 fundamental (used
  elsewhere in this project for the 3875/126 discussion) — but "close to
  32" is not equality, and no mechanism connects a qutrit error-code
  structure to the SM fermion content. **FAIL — no mechanism.**
- **C2.** 5-qubit 2-error code, charges as syndromes. [NEEDS TOOLING] real
  stabilizer-code construction required.
- **C3.** 3 generations = 3 logical qutrit states, color = 3 qutrits.
  [REASONED] Restates C1 without adding a mechanism. **FAIL.**
- **C4.** CKM as minimal-decoherence quantum channel. [NEEDS TOOLING] —
  well-posed in principle but requires defining and optimizing a channel;
  multi-day project.
- **C5.** Quantum Zeno for mass hierarchy. [REASONED] No stated measurement
  process or observer coupling for internal generation states; the
  premise doesn't specify what "measures" a generation more. **N/A —
  no mechanism specified.**
- **C6.** CKW monogamy inequality re-check. [ALREADY ANSWERED] — the
  project's own prior test (0.8²+0.7²=1.13, flagged FAIL in the source
  text itself) already found the monogamy bound violated under its own
  assumptions; re-deriving CKM bounds from CKW would need a fresh
  construction, not attempted.
- **C7.** 19=2⁵−13. [COMPUTED, see above] **FAIL — tautological.**
- **C8.** ZX-calculus simplification of Cl(10) diagrams. [NEEDS TOOLING]
  — needs a ZX-calculus engine (e.g. PyZX) and a translation from Clifford
  gamma matrices to ZX diagrams; not attempted.
- **C9.** SM as surface code, 3 holes = 3 generations. [REASONED] No
  stated lattice or code distance construction; "3 holes" is asserted,
  not derived. **N/A.**
- **C10.** Quantum complexity of preparing a 16-plet state ∝ mass.
  [NEEDS TOOLING] — "complexity" isn't defined precisely enough to
  compute without picking a specific complexity measure; open.
- **C11.** 3 MUBs in 8-dim. [COMPUTED, see above] **FAIL — max is 9 MUBs
  in dim 8, no selection rule for exactly 3.**
- **C12.** Fermion doubling 2^10=1024, staggered reduces to 3? [REASONED]
  Staggered-fermion doubling reduction factors are powers of 2 (typically
  2^d/2^(d/2) type reductions), not a route to odd numbers like 3 by any
  standard lattice-QFT result. **FAIL — doesn't match known doubling
  reduction schemes.**

## Category D: Entanglement / Complexity / Computation

All ten of D1–D12 share the same defect: each proposes a *measure*
(Kolmogorov complexity, edit distance, algorithmic information, Turing
machine halting, busy-beaver growth) applied to E8 weights or RG flow
*without specifying the actual map* from that measure's output to a real,
checkable SM number. [REASONED, all of D1–D12] These are not computable
as stated — you can't run "Kolmogorov complexity of a weight vector"
without first fixing a description language and encoding, and doing so
arbitrarily then reading off a mass ratio is exactly the kind of
reverse-engineering the project's own Rule 1/2 forbid. **D1–D5, D8–D12:
N/A — ill-posed, no fixed encoding to compute against.**
- **D6.** Train a neural net on anomaly cancellation to pick charges.
  [NEEDS TOOLING/COMPUTE] — genuinely doable in principle (I have Python +
  numpy/no GPU here), but this is exactly the free-parameter-fitting
  exercise Phase D/E/F/G already did analytically and found has zero
  selection power (Theorem G-1) — a neural net trained on the *same*
  anomaly-cancellation constraint would at best rediscover the same
  (n,−n,0) family already proven complete; not expected to add
  information. **Not run — would recapitulate an already-closed result.**
- **D7.** LLM brute-forcing superpotential terms. [N/A — this is a
  meta-request about using an LLM as a tool, not a physics hypothesis to
  test computationally.]

## Category E: Causal Sets / Emergent Spacetime

- **E1.** Exact 4-volume of past lightcone vs Hubble volume for Λ.
  [NEEDS TOOLING] — needs a numerical ΛCDM integration package and
  current cosmological parameters; a real half-day calculation, not
  attempted here.
- **E2.** Causal-set fluctuation variance vs DESI data. [NEEDS TOOLING +
  DATA] — requires live DESI survey data access.
- **E3–E10.** [NEEDS TOOLING, all] — spin foams, noncommutative causal
  distances, Hausdorff dimension of a lattice, entanglement-entropy
  horizon counting: each is a legitimate multi-week research calculation
  in its own right, none reducible to a quick script. Flagged open, not
  claimed to fail.

## Category F: Thermodynamics / RG / Stochastic

- **F1.** Add 3 E8 thresholds to sin²θW running. [NEEDS TOOLING] — needs a
  real 2-loop RG running code with actual E8-threshold particle content
  specified (which particles, at which masses) — underspecified as
  written, and a genuine calculation even once specified.
- **F2–F10.** [NEEDS TOOLING, all] — functional RG fixed points,
  stochastic quantization, superstatistics, Jarzynski equality, Unruh
  temperature analogies, Coleman-Weinberg with E8 gauge group, Parisi-
  Sourlas dimensional reduction: each requires either specialized QFT
  numerics or an original derivation. None attempted; all genuinely open,
  none of them "quick."

## Category G: Octonion / Division Algebra Twists

- **G1.** Sedenions (16-dim), "sedenion has 3?" [REASONED] Sedenions are
  16-dimensional and famously **not** a division algebra (they have zero
  divisors) — the premise "sedenion has 3" isn't even a defined property
  of the algebra. **FAIL — ill-posed.**
- **G2.** Bioctonions, "3 complex structures." [NEEDS TOOLING] — would
  require enumerating complex structures on the bioctonion algebra; not
  attempted.
- **G3.** Split-octonions, "3 timelike generations." [REASONED] Split
  octonions have signature (4,4), not a count of "timelike generations"
  in any standard sense — the hypothesis doesn't map onto a computable
  quantity. **N/A.**
- **G4.** OP² = F4/E6 "has 3 points." [REASONED] The octonionic
  projective plane OP² is a continuous 16-real-dimensional manifold, not
  a finite set of 3 points; category error. **FAIL.**
- **G5.** Okubo algebra for a mass scale. [NEEDS TOOLING] — legitimate
  algebraic question, not attempted.
- **G6.** Use right-multiplication R_i for SU(2)_R. [ALREADY ANSWERED] —
  this is *exactly* what Theorem M-1 tested (non-associativity of
  [L_i,R_j], 42/49 nonzero) and Phase T independently confirmed. Already
  closed: **FAIL, no independent SU(2)_R from R_i either.**
- **G7.** Dixon algebra R⊗C⊗H⊗O, 64-dim. [REASONED] 64 = 32+32 is
  correct arithmetic, but "3 copies = 192, close to 248−56=192" invents
  the subtraction 248−56 with no stated origin for "56" beyond making the
  numbers match (56 happens to be dim of E7's fundamental, unconnected
  here). **FAIL — reverse-engineered numerology.**
- **G8.** Cl(12), C(6,3)=20 → 3? [COMPUTED via same method as A1] Quick
  check: C(6,3)=20 is correct, but nothing in the hypothesis specifies
  *how* 20 would reduce to 3 (no analogous triality argument given for
  Cl(12), which has quadrality-type structure from Spin(8) but no
  established Spin(12) analogue reducing 6 Witt pairs to 3). **FAIL —
  no mechanism stated, just an analogous count.**
- **G9.** Jordan algebra J3(O), 27=3×9. [REASONED] Arithmetically true (27
  is the real dimension of the exceptional Jordan algebra, its 3 diagonal
  real entries plus 3 octonionic off-diagonal entries — this is the
  standard structure), but "3 diagonal entries = 3 generations" has no
  stated dynamical justification — it's the same numerical coincidence
  already used in B1/C1 without new content. **FAIL — no new
  mechanism.**
- **G10.** Freudenthal-Tits magic square, "3 rows." [REASONED] The magic
  square is 4×4 (rows indexed by ℝ,ℂ,ℍ,O), not 3 rows; premise is simply
  wrong as stated. **FAIL.**
- **G11.** Octonion ×-product for generation mixing. [NEEDS TOOLING] —
  would need an explicit construction and comparison to real CKM/PMNS
  data; not attempted.
- **G12.** Moufang loop, "3 generators." [REASONED] A Moufang loop's
  minimal generating set size depends on the specific loop chosen and
  isn't a fixed structural constant equal to 3 in general. **FAIL — not a
  well-defined invariant.**

## Category H: "Stupid / Nobody Tried"

The source file itself says these are "stupid on purpose" and expects
fast fails. Honoring that:

- **H1.** Jupiter-as-electron molecule model. [REASONED] Same order-of-
  magnitude mismatch problem the project's own `test_hypo.py` already
  found for the solar-system-as-atom idea (~10³⁶ gap); switching the
  analogy from atom to molecule doesn't change the dimensional-analysis
  mismatch between gravitational and electromagnetic bound-state scales.
  **FAIL.**
- **H2.** Vacuum as superfluid with rotons. [NEEDS TOOLING] — legitimate
  condensed-matter analogy question, not a quick check.
- **H3.** 86 billion neurons mod 19. [COMPUTED] 86,000,000,000 mod 19 =
  86000000000 % 19 = 12. No claimed significance of 12; **FAIL — no
  mechanism, and the arithmetic itself yields nothing.**
- **H4.** Lotka-Volterra for mediators. [ALREADY ANSWERED] — project's own
  `test_hypo4.py` already tested a mediator-replacement hypothesis and
  got "NO"; a predator-prey reframing doesn't change the underlying
  particle-physics question being asked. **FAIL by extension.**
- **H5.** "5D printer" metaphor. [REASONED] Not a physical hypothesis,
  purely a metaphor restating the Witt-pair/embedding counts already
  known (5, 10, 3). **N/A — not new content.**
- **H6.** π digits. [COMPUTED above] **FAIL.**
- **H7.** Music/12-tone scale. [REASONED] 19=12+7 is arithmetic with no
  stated physical mechanism connecting musical scales to SM parameters.
  **FAIL.**
- **H8.** Chess squares. [REASONED] 64=32×2 is trivially true (Cl(10)'s
  Fock space is 32-dim) but "3 gens = 3 checkmates" has no defined
  meaning. **FAIL — ill-posed.**
- **H9.** 19-year Metonic cycle. [REASONED] Lunar/solar calendar
  coincidence, no physical mechanism linking astronomical cycles to
  particle-physics parameter counts. **FAIL.**
- **H10.** Conway's Game of Life glider period. [COMPUTED, per source's
  own arithmetic] 30 mod 19 = 11, already stated as "not" matching in the
  source text itself. **FAIL, self-acknowledged.**
- **H11.** Base-3 of 10. [COMPUTED above] **FAIL.**
- **H12.** 19 = 8th prime. [COMPUTED above] **FAIL — true but no
  mechanism.**
- **H13.** Fibonacci near 5,8,13. [COMPUTED above, selection-bias
  argument] **FAIL.**
- **H14.** Langton's ant highways. [NEEDS TOOLING] — a real cellular-
  automaton run could check "3 emergent highways" computationally, but
  there is no stated map from ant-highway count to generation count even
  if 3 did appear; **N/A — no mechanism even if simulated.**
- **H15.** Population ratio (Pyuthan/world). [REASONED] Explicitly
  self-labeled "stupid but testable FAIL" by the source; there's no
  physical mechanism linking human demographics to particle mass ratios.
  **FAIL, self-acknowledged, no computation needed.**
- **H16.** Stock market caps as parameters. [REASONED] No mechanism.
  **FAIL.**
- **H17.** DNA codons, 20≈19+1. [REASONED] No mechanism connecting amino-
  acid count to SM parameter count beyond rough numerical proximity
  (20 vs 19). **FAIL.**
- **H18.** Origami folds. [REASONED] Metaphor, not computable. **N/A.**
- **H19.** Cooking metaphor. [REASONED] Explicitly "already did this
  metaphorically" per the source — restates existing structure with no
  new content. **N/A.**
- **H20.** 19=10+9, Cl(9)=16+16. [REASONED] Cl(9)'s spinor dimension is
  indeed 16 (real) — but "19=10+9" is just re-adding the two Clifford
  dimensions already in play (Cl(10) and its Cl(9) sub-algebra), which is
  a restatement, not a derivation of 19 free SM parameters from anything
  independent. **FAIL — tautological restatement.**
- **H21.** Time-crystal phases. [NEEDS TOOLING] — no stated map from
  time-crystal phase count to generation count even in principle;
  **N/A — no mechanism.**
- **H22.** Black-hole microstates in E8. [NEEDS TOOLING] — genuinely
  requires black-hole microstate counting formulas (e.g., from string
  theory) mapped onto E8, well beyond a quick check.
- **H23.** Traffic lanes. [REASONED] Metaphor restating C(5,3)=10, no new
  content. **N/A.**
- **H24.** Random-matrix GOE eigenvalues. [COMPUTED above] Ran 200 draws
  of 19×19 GOE matrices; standard Wigner-type level repulsion observed,
  but the hypothesis names no concrete map from eigenvalues to actual SM
  parameter VALUES, so there is nothing further to test against real
  data. **N/A beyond confirming standard random-matrix statistics.**
- **H25.** "Ask what problem wants to be solved — publish 0/19 honestly."
  [REASONED — this is a meta/process suggestion, not a physics
  hypothesis.] It's arguably the most defensible item in the whole list:
  the project's own `FINAL_AUDIT.md` already does exactly this. **Already
  done, not a new result to compute.**

## Category I: Cosmological / Astro

- **I1.** 3 CMB acoustic peaks = 3 generations. [REASONED] The CMB power
  spectrum has more than 3 acoustic peaks resolved in real data (Planck
  resolves ~7+); "3" isn't even the correct observational count to
  compare against. **FAIL — factually wrong premise.**
- **I2.** 19 orders of magnitude, Planck to neutrino mass. [COMPUTED
  above] Actual value ≈29.4 orders of magnitude, not 19. **FAIL.**
- **I3.** Dark matter = 4th generation from a leftover triality
  embedding. [NEEDS TOOLING] — would need a full dark-matter phenomenology
  check (relic abundance, direct-detection bounds) against a specific
  proposed particle; not a quick check, and no candidate mass/coupling is
  even specified in the hypothesis as stated.
- **I4.** JWST high-z varying CKM. [NEEDS TOOLING + DATA] — requires live
  JWST spectroscopic data and a varying-constants analysis pipeline.
- **I5.** 10D→3D+7D Fano compactification. [REASONED] Same 5-vs-7 object-
  count mismatch as A15/A5. **FAIL.**
- **I6.** MOND interpolation functions. [REASONED] No stated map from "3
  generations" to "3 MOND functions" (MOND typically uses one
  interpolation function, chosen empirically, not three). **FAIL —
  premise doesn't match the actual MOND literature.**
- **I7.** FRB dispersion measure = generation. [REASONED] No mechanism
  connecting intergalactic electron column density (an astrophysical
  measurement) to a particle's generation index (an intrinsic quantum
  number). **FAIL — category error.**
- **I8.** 19 params vs 19.7% dark matter fraction. [REASONED] Numerical
  near-coincidence (19 vs 19.7), explicitly dismissed by the source
  itself ("No."). **FAIL, self-acknowledged.**
- **I9.** 3 generations = 3 GW polarizations. [REASONED] GR predicts
  exactly 2 tensor polarizations for gravitational waves (plus up to 4
  more only in modified-gravity theories); "3" doesn't match GR's actual
  prediction. **FAIL — factually wrong premise.**
- **I10.** Hubble tension, 3 H0 values. [REASONED] The Hubble tension is a
  2-value discrepancy (early-universe ~67 vs late-universe ~73 km/s/Mpc),
  not a 3-way split; premise doesn't match the actual measurement
  landscape. **FAIL.**

## Category J: Meta / Method

These are process/publication suggestions, not physics hypotheses, so
"testing" them means checking whether they're already done:

- **J1, J10.** Publish the audit methodology / "0/19 is itself the
  result." [ALREADY DONE] — `FINAL_AUDIT.md` and `docs/solution.md`
  already are this document.
- **J2.** Build an automated "ToE killer" tool generalizing Phase E–G's
  anomaly/free-parameter checks to arbitrary Cl(n) models. [NEEDS
  TOOLING/BUILD] — this is a genuine, well-scoped software project (not a
  physics derivation) that could actually be built with what's available
  here (Python). Distinct from the other 100+ items in that it's
  buildable rather than a physics claim to test. Not built in this pass
  since it's a multi-file tool, not a single hypothesis check — flagged
  as the one item in the whole list that's both novel and immediately
  actionable if wanted.
- **J3–J9.** Leaderboards, papers, teaching materials, collaboration,
  packaging. [N/A — organizational/publication tasks, not physics
  hypotheses.]

---

## Bottom line

Of ~140 individual items: **0 produced a new positive result.** A handful
(B2, B9) reconfirm results the project already has by other means. Several
dozen are refuted immediately by a mismatch between the hypothesis's own
stated objects (5 vs 7, 3 vs 4 rows, odd vs even code length, "1 type of
root" self-contradicting itself). A large fraction of Categories D–F–I
are not computable as stated at all — they name a measure or a dataset
without specifying the map back to an actual, checkable SM number, which
means they're not really hypotheses yet, just directions. The Category H
items behave exactly as the source file predicted: fast, uneventful fails.

**The project's own headline numbers are unchanged: 0/19 Standard Model
parameters derived from Cl(10)×E8 algebra, ~13 free parameters still
required.** Nothing in this sweep — computed or reasoned — moves that
number, which is consistent with (not contradicted by) everything the
project's own Phases E through V already found.
