# Hypothesis Backlog — Full List [L2/L3, all speculative, updated 2026-07-28]

> **STATUS UPDATE (Phase R, 2026-07-28):** Priority 0 and items 12, 13, 14,
> 19, 21, 26, 27, 32, 34, 37/38, 40, 41, 43, 44 have been RUN — see
> `phase_r_backlog_tests.py` and the Phase R row/addendum in `README.md`.
> Marked `[DONE - Phase R]` inline below with a one-line result each. Item
> 37/38 was re-scoped from `[cheap]` to `[real]` mid-check (needs a lattice/
> group-theory package not available in this environment; only the rank
> consistency was confirmed).
>
> **STATUS UPDATE (Phase U, 2026-07-28):** Items 6, 8, 9, 17, 18, 28 have
> been RUN as `[lit]` checks — see `phase_u_literature_2026.py` and the
> Phase U section in `README.md`. Marked `[DONE - Phase U]` inline below.
> This found a directly relevant, same-algebra (Cl(10)) paper series
> published Jan–Jun 2026 that neither Phase I's original sweep nor Phase R
> caught (both predate or coincide with those publication dates). Nothing
> from Phase U is code-verified against this project's own conventions —
> `[lit] DONE` means "identified and read," not "reproduced." Everything
> else below is still genuinely unrun and open, exactly as this file
> originally described.
>
> **STATUS UPDATE (Phase V, 2026-07-28):** Items 20 and 33 have been RUN —
> see `phase_v_realtier_items.py`. Both are `[real]`-tier items that, on
> inspection, needed only this project's existing octonion code plus
> elementary number theory rather than a Lie-theory package. Both close
> negative. Item 15 was explicitly considered and NOT attempted — it needs
> a genuine weight-multiplicity engine (LiE/Sage/GAP-class), and doing it
> by hand risked exactly the kind of unverified arithmetic this project's
> rules forbid; it stays open. All other `[real]` items still need
> GAP/Magma/Sage/LiE or multi-week derivation and remain genuinely open.
>
> **STATUS UPDATE (session_new_files, 2026-07-28):** Items 5, 7, 15 (full,
> not just the adjoint-branching partial below), and 29 have been RUN —
> see `session_new_files/new_test_item5_e8_weyl_stabilizer.py`,
> `new_test_item7_s3_cohomology.py`, `new_test_item15_e6_tensor_full.py`,
> `new_test_item29_mckay_2i.py`, and one `RESULT_item*.md` per item in the
> same folder. This work used GAP 4.15.1 + HAP 1.74, so it is the first
> time this project has had the weight-multiplicity/cohomology tooling
> Phase V/W flagged as missing. Marked `[DONE - session_new_files]` inline
> below with a one-line result each. All four close negative; net effect
> on the ~13-parameter count is zero. Not yet folded into `README.md`'s
> phase table as a lettered phase — see the addendum there.
>
> **STATUS UPDATE (session_new_files, 2026-07-28, continued):** Item 6
> has now also been RUN — see
> `session_new_files/new_test_item6_gresnigt_cl10_s3_verify.py` and
> `RESULT_item6.md`. The Gresnigt paper's Cl(8)/S3 core is
> code-verified from scratch (not just read); Phase A1's own
> conventions do NOT already carry this S3 mechanism (different
> concrete construction, missing the sedenion-doubling step). Item 1
> (=R1, this project's actual open question) was explicitly considered
> and NOT attempted this session — it needs real noncommutative-
> geometry/Seeley-DeWitt tooling this environment lacks; see
> `RESULT_item1.md` for what's actually required rather than a
> fabricated attempt. Marked `[DONE - session_new_files]` /
> `[BLOCKED - session_new_files]` inline below.

> **STATUS UPDATE (Post-Audit Session, 2026-07-28):** Following
> `audit report/COMPLETE_AUDIT_REPORT.md`'s forensic re-audit, three
> corrections were made and one new result added: (1) Item 7's label
> below was downgraded from L1 to L2 (the shipped verification file
> doesn't execute — see the inline correction). (2) The "3 generations"
> claim in `README.md`, `docs/solution.md`, `docs/FINAL_AUDIT.md`, and
> `docs/ALL_THEOREMS.md` was corrected to state its dependence on the
> E6×SU(3)_f branching chain (previously stated as an unconditional L1
> fact). (3) A 19-vs-23 parameter-counting inconsistency between prose
> and `phase_c_honest_accounting.py`'s own table was documented (no
> conclusion changes either way). (4) Phase X's one L2-cited item (the
> 10-vs-126 split) was independently re-derived and upgraded to L1 — see
> `phases/phase_y_hodge_star_self_duality.py`,
> `session_new_files/RESULT_phase_y.md`, and Theorem Y-1 in
> `ALL_THEOREMS.md`. None of this changes the 0/19-or-23 bottom line or
> the ~13 free-parameter count. See `docs/POST_AUDIT_TARGET.md` and
> `docs/MECHANISM_FAILURE_MAP.md` for the current state of the open
> question and the research decision going forward.

**Read this first.** Every item below is an untested conjecture inside this project,
not a promise. Several turned out to already be published by other researchers —
those are marked LITERATURE EXISTS, with citations, so you compare against real
results instead of re-deriving them blind. One item is not a hypothesis at all: it's
a foundational check this project owes itself before anything else on this list.
Everything else is genuinely unrun, tagged by how much work it takes: **[cheap]**
(a day or less, mostly code), **[real]** (needs real math/reading first),
**[lit]** (a literature check, not a derivation).

---

## PRIORITY 0 — do this before anything else on this list

**0. Distler–Garibaldi check.** [DONE - Phase R: PASS, foundation check] Distler & Garibaldi (Comm. Math. Phys., 2010) proved
that Garrett Lisi's E8-based "theory of everything" — which places Standard Model
fermions directly in E8's 248-dimensional adjoint representation — necessarily gives
a **non-chiral** spectrum (mirror fermions with opposite charges), which real physics
rules out. This project's fermions instead come from the SO(10) **16** via
E6's 27 ⊃ 16 (Phase A2), a different, standard, chiral GUT assignment used since the
1970s — not the adjoint-248 route Lisi used. The no-go theorem's hypothesis (fermions
as adjoint components) likely doesn't apply here, but "likely" has never been checked
in this project's own code. **Concrete task:** verify explicitly, using Phase A2's
actual branching, that no part of the fermion content is realized as an E8-adjoint
component, closing off any possibility that this project silently inherits Lisi's
chirality problem. Do this first — it's a foundation check, not a new avenue.

---

## A. Alternative dynamics (the R1 problem, from different angles)

1. **[real] [UPDATED 2026-07-28, Phase Z/Z1: the "is it worth attempting"
   question is now closed at L1, distinct from the original blocked
   status.** Phase Z confirmed no NCG-specific tooling exists (generic
   Clifford-algebra packages don't supply order-one/KO-dimension/
   Seeley-DeWitt machinery). Phase Z1 then asked the sharper question —
   not "can we compute a4," but "could *any* D_F built this way ever be
   unique" — and proved no: order-one, reality, chirality, and gauge
   covariance are all linear/homogeneous in D_F, so the solution set is
   always a vector space, never an isolated nonzero point. This doesn't
   just leave item 1 blocked for lack of tooling; it shows the route
   cannot reach Case A (unique D_F) even with perfect tooling. See
   `docs/PHASE_Z_SPECTRAL_TRIPLE_RESULT.md` and
   `docs/PHASE_Z1_SPECTRAL_TRIPLE_MODULI_RESULT.md`. What's still open:
   whether the surviving freedom is exactly Phase X's 6-or-3 (L2,
   argued, not independently computed — needs actual J/Γ construction
   for Phase A1's Fock space) or something larger.]**
   Build a spectral-action-style Dirac operator directly from Cl(10)'s own
   Witt-pair structure — not imported from CCvS — and check whether its heat-kernel
   a4 term fixes the ratio g1:g2:g3 at the unification scale, rather than assuming
   GUT normalization by hand.
2. **[cheap]** Use E8's own Casimir invariants (not CCvS, not Cl(10)) as the basis for
   a toy potential on the SU(3)_f flavon field, and check whether this specific
   invariant (not the generic |φ|² one Theorem 3 already ruled out) has a nonzero
   minimum for ε.
3. **[real]** Modular-Hamiltonian / KMS-state approach: assign a thermal state to
   Phase A1's Fock vacuum and check whether its modular operator's eigenvalue
   spectrum gives a natural (unfitted) ordering across the 3 generations.
4. **[cheap]** Purely combinatorial: build the E8 root-lattice Voronoi adjacency
   graph and check graph-distance patterns between generation-labeling roots for any
   structure resembling a 3-tier hierarchy.

## B. Discrete subgroups as family symmetry

5. **[real] [DONE - session_new_files, CLOSED NEGATIVE, L1]** Find the actual
   stabilizer subgroup of one E6 27 inside the full E8 Weyl group (order
   696,729,600) and compute its induced action on the SU(3)_f triplet. If
   nontrivial and irreducible, check for forced texture zeros. **Result:**
   the stabilizer projects to W(A2)=S3 (order 6) acting on the SU(3)_f
   triplet as 3 = 1⊕2. S3 invariance forces a *democratic* Yukawa
   structure Y=aI+bJ — no entries forbidden, no texture zeros, no
   generation hierarchy. See `session_new_files/RESULT_item5.md`.
6. **[LITERATURE EXISTS, DONE - Phase U] [CODE-VERIFIED - session_new_files,
   2026-07-28, L2]** Discrete family symmetry from Clifford
   algebra: Gourlay & Gresnigt, *"Algebraic realisation of three fermion generations
   with S3 family and unbroken gauge symmetry from Cl(8),"* Eur. Phys. J. C 84 (2024)
   1129. **Update:** the same group has since published the direct Cl(10) sequel —
   N. Gresnigt, *"Electroweak Structure and Three Fermion Generations in Clifford
   Algebra with S3 Family Symmetry,"* arXiv:2601.07857 (2026-01, v2 2026-04) — 3
   generations from S3 acting on Cl(10)'s own Witt-basis minimal left ideals, the
   SAME base algebra as this project's Phase A1, via a mechanism independent of this
   project's E8-branching route. A Higgs/Yukawa follow-up also exists (arXiv:2604.24795,
   2026-04/06): Type-II-like, algebraically-fixed, non-diagonal Yukawa structure, no
   absolute mass values claimed. Identified and read, and NOW
   code-verified from scratch against this project's own conventions —
   see `session_new_files/new_test_item6_gresnigt_cl10_s3_verify.py` and
   `RESULT_item6.md`. **Result:** the paper's Cl(8)/S3 core is confirmed
   internally consistent, exactly as published. Phase A1's own Cl(10)
   construction does NOT already carry this S3 mechanism — it depends on
   sedenion-automorphism data (Cayley-Dickson doubling) Phase A1 never
   builds. Importing it into Phase A1's own conventions is identified as
   the concrete next step, not yet attempted.
7. **[real] [DONE - session_new_files, CLOSED NEGATIVE, L2 — corrected 2026-07-28,
   was mislabeled L1]** Compute the H³ group-cohomology class ('t Hooft
   anomaly) of whatever finite group turns up in #5, acting on the fermion
   Fock space. A nonzero class would forbid specific Yukawa terms by
   consistency — texture zeros for free. **Result:** H³(S3,U(1))=Z/6Z (via
   GAP/HAP), but the specific 3-generation permutation representation is
   real/orthogonal with c₂=0, i.e. the trivial anomaly class. Zero anomaly
   forbids nothing. See `session_new_files/RESULT_item7.md`. **Correction
   (COMPLETE_AUDIT_REPORT.md, Phase 3/4.3):** the shipped file
   `new_test_item7_s3_cohomology.py` does not execute (SyntaxError); its
   printed "output" is a hand-transcribed external GAP session, not a
   computation reproduced inside this repository. The underlying group-
   theory facts are standard and check out, but per Rule 3 an external
   result merely narrated here is L2, not L1 — contrast with Item 6, which
   really does run a from-scratch, in-repo computation and is correctly
   labeled L2 (its own honest ceiling, since it verifies literature, not
   this project's own axioms). Re-open only if the GAP session is actually
   re-run and its transcript captured in this repository.

## C. Exceptional/Jordan-algebra structures

8. **[LITERATURE EXISTS, DONE - Phase U]** *"Fermion mass ratios from the exceptional
   Jordan algebra,"* arXiv:2508.10131 (2025) — already computes mass ratios from J3(O)'s
   cubic form. **Update:** two direct sequels since found — Gupta Teli & Singh,
   arXiv:2605.24866 (2026-05) promotes the rigid parameter-free delta^2=3/8 point to a
   fitted "spectral moduli space" (global log-fit to 6 mass ratios, best-fit exponent
   p~1, explicitly NOT a parameter-free replacement for the rigid version); and
   arXiv:2607.00412 (~2026-06) extends this to CKM/PMNS mixing via a "Fritzsch-type"
   ansatz its own authors call a bridge, not a theorem. Net: this sub-field is moving
   toward fitted models, the same direction Phase D already went — not toward a
   free lunch this project missed. Read, not code-reproduced.
9. **[real]** Freudenthal triple system (two J3(O) copies, natural home of E7) — none
   of the papers found in Phase U use this specific structure either. Still open.

## D. Alternative branching chains

10. **[real]** E8 → SO(16)/Z2 → SO(10)×SO(6) → SO(10)×SU(4): does the SU(4)
    (replacing SU(3)_f) give a non-flat flavon potential?
11. **[real]** E8 → E7×SU(2) → E6×SU(2)×SU(2): does the extra SU(2) here (distinct
    from Phase L/M's dead-end SU(2)_R) offer a PMNS-mixing mechanism?
12. **[cheap]** Cl(12) or Cl(14) [DONE - Phase R: negative, no generation mechanism found] instead of Cl(10): does a bigger Clifford algebra's
    own Witt-pair counting force exactly 3 generations structurally, independent of
    the E8 branching this project currently relies on for "3"?

## E. Blind numerical scans (compute first, compare second — the only honest order)

13. **[cheap]** All dimensionless ratios among E8's own numbers [DONE - Phase R: no meaningful hit] (Coxeter number 30,
    dim 248, rank 8, root count 240, Weyl group order 696,729,600) — computed blind,
    logged in full, *then* checked against SM values, with every miss reported
    alongside every hit.
14. **[cheap]** Same exercise with Cl(10)'s own numbers [DONE - Phase R: 1 coincidence within 1%, not meaningful (multiple comparisons)] (32 states, 5 Witt pairs,
    C(5,3)=10, C(5,2)=10, 2^10=1024).

## F. Untested representation-theory claims currently taken on faith

15. **[real] [DONE - session_new_files, CLOSED NEGATIVE, L1] [was PARTIAL - see
    tests/new_test_item15_e6su3_branching.py: the ADJOINT branching
    (78+8+162=248, zero room left for 126/3875) was computed directly from
    the root system, not cited. The remaining general tensor-product /
    weight-multiplicity question — does 27⊗27⊗27 contain a 126 or 3875 —
    has now also been run, via the Weyl dimension formula over all 83
    dominant weights at Dynkin level ≤3:
    `session_new_files/new_test_item15_e6_tensor_full.py`. Neither 126 nor
    3875 is an achievable E6 irrep dimension at all (126 is an SO(10)
    dimension, 3875 an E8 one) — see
    `session_new_files/RESULT_item15.md`. One narrower sub-question stays
    open: branching each 27⊗27⊗27 summand to SO(10) directly, which still
    needs LiE/Sage-class branching-rule tooling this environment lacks.]**
    Phase B's CKM=I/PMNS=I result (126/3875 absent from minimal 248) has
    never actually been branched and checked with real multiplicities in this
    project's own code — currently cited from literature, not computed. Do it once,
    properly. **Considered in Phase V and explicitly NOT attempted:** this needs a
    real weight-multiplicity engine (what LiE/Sage/GAP compute for tensor-product
    decomposition), which this environment doesn't have; doing the arithmetic by
    hand risked producing an unverified result dressed up as a computed one. Stays
    open, correctly scoped to "needs the right software," not silently resolved by
    Phase A2's dimension-counting (which is a different, weaker check than this
    item asks for).
16. **[real]** Test E8×E8 (heterotic-string-motivated, two copies) instead of a
    single E8 — genuinely unused in this project. Check whether it reopens CKM≠I in
    a computed, not-fitted way.

## G. Literature and cross-checks (recurring, not one-time)

17. **[lit, DONE - Phase U]** Re-run Phase I's literature search monthly. New papers
    in this exact space are appearing roughly every few months right now (see items
    6, 8, and the "already published" list below) — this field is more active than
    Phase I's 2026-07-27 snapshot suggested. **Result:** confirmed and then some —
    found a same-algebra (Cl(10)) S3 family-symmetry paper series (item 6 update)
    published within the weeks around this project's own closure date, missed by
    Phase I. This item stays formally open as "recurring" — one search is a snapshot,
    not a subscription — but the 2026-07-28 pass is logged done.
18. **[lit, DONE - Phase U]** Search specifically for a Cl(10)-specific (not generic
    SO(10)) sin²θ_W or Cabibbo-angle derivation, to independently validate/refute
    Phase K. **Result:** none found. The Cl(10)-S3 papers (item 6 update) don't
    address sin²θ_W or Cabibbo running; the J3(O) papers (item 8 update) address
    Cabibbo-like angles but via a division-algebra construction unconnected to
    Cl(10)'s Witt-pair generator normalization. Phase K's conclusion stands
    unchallenged.
19. **[cheap]** Check directly (not assumed) whether Phase O's causal-set N [DONE - Phase R: negative, no natural expression found] has any
    natural expression in Cl(10)'s 32-state Fock space or E8's 240/248 numbers.

## H. Genuinely speculative, flagged as such

20. **[real, DONE - Phase V]** p-adic norms (p=3) on the FN charge structure — a
    different number system entirely. **Result:** tested directly. The 3-adic
    valuation is undefined at q3=0 (breaking the 3-tier ordering entirely) and
    reproduces Phase E's exact 2-tier degeneracy on the anomaly-free (n,-n,0)
    family, since v_3(n)=v_3(-n) always. No escape from Phase E's structural
    result found. Also not statistically meaningful as posed (3 data points,
    same caveat as items 21/41). See `phase_v_realtier_items.py`.
21. **[cheap]** Random-matrix statistics on the E8 Cartan matrix [DONE - Phase R: not applicable, no ensemble exists for a single fixed matrix] eigenvalues against
    GUE/GOE universality classes — exploratory only, log honestly either way.

## I. Follow-ups contingent on earlier items

22. **[real]** If #5 finds a real finite family symmetry: check whether its Casimir
    eigenvalues, used as FN charges instead of chosen integers, reproduce or rule
    out (3,2,0).
23. **[real]** If #8/#9 produces a canonical scale: check whether it can supply
    Phase F's messenger mass, closing that thread's "adds a free scale" objection.
24. **[real]** If #10 or #11 survives: redo Phase C's 0/19 accounting under that
    chain specifically.
25. **[cheap]** If any of #1–#4 produces even a toy nonzero action: immediately
    re-run Phase B's CKM=I proof under it — that proof depended on the *minimal*
    248 having no dynamics.

## J. Signature/dimension variants

26. **[cheap]** Cl(1,9) — Lorentzian, not Euclidean. [DONE - Phase R: confirmed, survives via complexification] Check whether charge
    quantization survives the different real form.
27. **[cheap]** Cl(9) and Cl(11) against Cl(10) [DONE - Phase R: confirmed, 10 is structurally distinguished (even dim)] directly — is 10 dimensions actually
    necessary, or do neighbors work equally well?

## K. McKay correspondence (E8 ↔ binary icosahedral group)

28. **[LITERATURE EXISTS, mixed history, DONE - Phase U]** Furey & Hughes, *"Three
    generations and a trio of trialities,"* Physics Letters B 865 (2025) 139473 —
    covers triality-based generation structure directly. **Result:** read directly.
    Mechanism is division-algebra triality (tri(C)+tri(H)+tri(O)), not an E8-adjoint
    embedding — two generations from a triality pair (Psi_+, Psi_-), a third from a
    separate "Cartan factorization." **Caution stands, unresolved:** this general
    direction has a documented bad history — Garrett Lisi's 2007 E8 theory used
    triality for exactly this purpose and was formally shown by Distler & Garibaldi
    (2010) to require non-chiral mirror fermions (see Priority 0). The text found in
    this search does not address chirality/Distler-Garibaldi one way or the other for
    THIS specific construction. Since it is not an E8-adjoint-248 placement, this
    project's own Phase R Priority-0 check does not automatically transfer or clear
    it. Logged as genuinely open, not assumed safe.
29. **[real] [DONE - session_new_files, CLOSED NEGATIVE, L2]** The McKay quiver
    of the binary icosahedral group 2I (order 120, corresponds to E8's extended
    Dynkin diagram) for a natural node assignment of generations — check
    against #28's construction for overlap before starting. **Result:** the
    quiver's 9 nodes (dims 1,2,3,4,5,6,4,3,2, McKay 1980, L2 cited not
    re-derived) have trivial automorphism group — no Z₃ symmetry, no natural
    split into 3 sets of 3. No overlap with #28's division-algebra triality
    construction (different structures, both merely "relate to E8"). See
    `session_new_files/RESULT_item29.md`.

## L. Hyperbolic Kac-Moody extensions

30. **[real]** E9 (E8's affine extension) appears in real supergravity billiards
    literature (Damour, Henneaux, Nicolai). Check whether it supplies actual
    dynamics ("time") that static E8 structurally lacks.
31. **[real]** E10 (conjectured M-theory symmetry) — check root multiplicities
    beyond the E8 subalgebra for generation structure.

## M. Non-associativity

32. **[cheap]** Compute the associator [DONE - Phase R: zero on matrix ops as posed; nonzero on raw octonion units (contrast test run)] [a,b,c]=(ab)c−a(bc) on fermion states directly
    — check if it's zero within a generation, nonzero across generations. Not
    covered by the triality/Jordan-algebra literature above, which mostly works with
    associative constructions built *from* octonions rather than the
    non-associativity itself.
33. **[real, DONE - Phase V]** Malcev-algebra structure (correct non-Lie analog for
    octonions) — its own independent Casimir-like invariant. **Result:** the Malcev
    identity is confirmed directly on this project's own octonion structure
    constants (first check of this fact in this repo, though the underlying result
    is 60+ years old). The induced trace-form invariant tr(ad_x ad_y) is proportional
    to the identity on the 7-dim imaginary-octonion basis — the unique G2-invariant
    form, carrying no extra structure (no distinguished 3-dim subspace, no eigenvalue
    splitting) that could be read as "3 generations." Closed, negative. See
    `phase_v_realtier_items.py`.

## N. Modular structure of the E8 lattice

34. **[cheap]** E8 lattice theta function [DONE - Phase R: computed exactly, no SM match] (weight-4 modular form for SL(2,Z)) —
    parameter-free coefficient sequence, computed blind, then compared to mass
    ratios.

## O. Real numerics

35. **[real]** Actual lattice-gauge simulation seeded with Cl(10)'s charges —
    nonperturbative RG flow, replacing Phase K's 1-loop estimate.
36. **[real]** Instanton-counting (Nekrasov partition function) for an E8 gauge
    theory — check saddle points against the fitted (3,2,0).

## P. Wildcards (genuinely not found anywhere in the literature search)

37. **[cheap]** The Leech lattice has a known construction [PARTIAL - Phase R: rank consistency confirmed; automorphism search re-scoped to [real], needs external software] (Turyn) from **three
    mutually orthogonal copies of the E8 lattice**. This is different from every
    published triality/Cl(8) construction above, which all get "3" from *within* one
    E8 — not from 3 separate E8 lattices combining into a bigger one. Check whether
    treating generations as 3 orthogonal E8 sublattices gives independent,
    uncorrelated charge structure.
38. **[cheap]** Check the Leech lattice's automorphism group [PARTIAL - Phase R: see item 37 note] (Conway group Co0/Co1)
    for an order-3 element permuting those 3 E8 sublattices — a discrete symmetry
    source outside the entire Cl(8)/S3/triality literature cluster.
39. **[real]** Monster-moonshine-adjacent structures at the 26D bosonic string /
    vertex-algebra level — near-certain dead end, genuinely unexplored by anyone in
    this specific sub-field, worth one honest negative-result log entry.
40. **[cheap, "stupid" tier [DONE - Phase R: closed trivially, all E8 root lengths equal], exactly as requested]** Continued-fraction expansion of
    ratios between E8 root lengths against the observed mass hierarchy — deliberately
    silly, cheap to falsify in an hour.
41. **[cheap, "stupid" tier]** Benford's Law [DONE - Phase R: not meaningfully testable, only 8 data points] against the full list of E8 Casimir
    eigenvalues / structure constants — a generic-vs-structured sanity check, not a
    derivation either way.
42. **[real]** Renormalization-group fixed-point *counting* (not embedding): how
    many RG-relevant operators does Cl(10)'s specific field content allow, as a pure
    counting problem independent of any group-theoretic assignment.

## Q. Meta

43. **[cheap]** Leverage ranking [DONE - Phase R: see README Phase R addendum for full ranking]: of everything above, which single success would
    reduce Phase C's ~13 free parameters the most? Do this before starting any of
    them individually.
44. **[cheap]** Pairwise consistency check [DONE - Phase R: no contradictions found among items run]: for any two mechanisms you pursue,
    verify they don't silently contradict each other before adopting both.

---

## Already published — read before repeating

- Gourlay & Gresnigt, *S3 family symmetry from Cl(8)*, Eur. Phys. J. C 84 (2024) 1129
  — overlaps item 6.
- Furey & Hughes, *Three generations and a trio of trialities*, Phys. Lett. B 865
  (2025) 139473 — overlaps item 28.
- *Fermion mass ratios from the exceptional Jordan algebra*, arXiv:2508.10131 (2025)
  — overlaps items 8–9.
- Dray, Manogue, Wilson, *Octions: An E8 description of the standard model*, J.
  Math. Phys. 63 (2022) 081703 — alternative E8 construction, worth reading for
  context even where it doesn't overlap a specific item.
- Distler & Garibaldi, *There is no "Theory of Everything" inside E8*, Comm. Math.
  Phys. (2010) — the no-go theorem behind Priority 0.

**Found by Phase U (2026-07-28 live search), not in the original list:**
- Gresnigt, *Electroweak Structure and Three Fermion Generations in Clifford Algebra
  with S3 Family Symmetry*, arXiv:2601.07857 (2026) — direct Cl(10) sequel to item 6's
  Cl(8) paper; same base algebra as this project's Phase A1.
- Gresnigt, *Higgs Sector and Flavour Structure in an Algebraic Three-Generation Model
  with S3 Family Symmetry*, arXiv:2604.24795 (2026) — Yukawa-sector follow-up to the
  above.
- Gupta Teli & Singh, *Fermion Mass Hierarchies and the Exceptional Jordan Algebra*,
  arXiv:2605.24866 (2026) — fitted sequel to item 8's rigid J3(O) paper.
- Gupta Teli et al., *Fermion Mixing Matrices and the Exceptional Jordan Algebra*,
  arXiv:2607.00412 (2026) — CKM/PMNS extension of the above.

## How to actually use this list

Same rules as every phase before it: compute, don't assume; log negative results
with the same weight as positive ones; check the literature list above before
spending real time on items 6, 8, 9, or 28; do Priority 0 first regardless of
anything else. Most of the rest will close, the way fifteen previous attempts
already did in this project. That's still the only way any of them count as real.
