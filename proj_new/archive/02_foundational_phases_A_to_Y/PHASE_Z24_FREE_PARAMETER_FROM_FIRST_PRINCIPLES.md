# PHASE Z24 — Why the free parameter reappears no matter what, and the one
# untried door (a clean-room secondary analysis)

**Date.** 2026-08-02.
**Author of record.** A fresh analysis pass ("Kimi"), run outside the
original `gods_paradox/` tree. Per the owner's instruction, **nothing in
the old directories was modified**; this folder is self-contained and all
supporting scripts live alongside this file under
`session_new_files/phase_z24_free_parameter_from_first_principles/`.

**Ground rules.** This document adopts the project's own `GROUND_RULES.md`
(see `incoming_context/GROUND_RULES.md`) verbatim — in particular Rule 1
(no numerology), Rule 2 (no reverse-engineering), Rule 3 (L1/L2/L3
labeling), Rule 6 (discrete-forced ≠ continuous-free), Rule 8 (a closed
avenue is a result), and Rule 9 (discriminating power). Where this
document relies on an original-repo result it is cited as **(repo, Lx)**;
where it *re-derives* something here, the script and exact output are
named.

---

## 0. The question, restated precisely

The owner's question, after 23 recorded phases: *"I've tried everything;
the outcome is the same no matter what I do. Is there a solution — a
first-principles derivation of the free parameters?"*

The free parameter(s) at issue (per `POST_AUDIT_TARGET.md` §B–C, repo,
L1):
* **Flavor sector:** 6 complex (H ∈ {10,126}, symmetric) or 3 complex
  (H = 120, antisymmetric) Yukawa parameters; the 3-generation flavor
  index is unconstrained by gauge symmetry.
* **Everything else:** no dimensionful scale exists in Cl(10) or E8 as
  abstract algebras, so no mass, VEV, or running coupling value is
  derivable from the algebra alone (repo `PARAMETER_ACCOUNTING_RECHECK`,
  L1).

---

## 1. The answer in one paragraph

**There is no first-principles derivation of these parameters from inside
Cl(10)×E8, and this is now provable, not conjectural — because the
"it keeps failing the same way" pattern has a specific, nameable cause, and
it is a theorem, not a run of bad luck.** Every one of the ~10 distinct
mechanisms in `MECHANISM_FAILURE_MAP.md` fails by one of two lemmas, which
this document states and re-verifies computationally. The honest remaining
options are: (A) convert the dead end into the deliverable by writing the
no-go as an explicit impossibility **theorem**; (B) attempt a genuinely new
structural door *outside* the current class of constructions (generations
as an index-theoretic zero-mode multiplicity rather than a flavor-symmetry
multiplicity) — knowing in advance that this is a **relocation** of the
parameters, not an elimination, unless an additional selection principle is
also found; or (C) consolidate and publish the negative result, which is
itself a contribution. **I recommend A.** Section 5 gives A as an explicit
theorem with hypotheses, conclusions, and three cases that genuinely escape
it (so it is falsifiable, per Rule 9).

---

## 2. Lemma A — "No isolated point" (homogeneity)

**Statement.** Every axiom/condition the project has ever imposed on the
finite geometric data (the finite Dirac operator D_F, the Yukawa tensor,
the order-one condition, its twisted variants) that is **linear or
antilinear and homogeneous** in D_F has, as its solution space, a vector
space / cone. A vector space has no isolated nonzero point: if D_F is a
solution, so is λ·D_F for every scalar λ ≠ 0.

**Why this is the whole story for "no scale" and "no unique D_F."**
* Repo: Phase Z1 (order-one/reality/chirality/covariance all linear in
  D_F ⇒ solution set a line), Phase Z19 (fixed-automorphism **twisted**
  order-one still linear/homogeneous ⇒ same conclusion), Phase Z20's
  self-twist removes homogeneity but reintroduces an orbit degeneracy
  under the commutant (repo, L1).
* **Independent re-verification here** —
  `check_z24_no_scale.py` (exact sympy): the order-one double commutator
  `[[D,a],b]=0` with D an unknown symbol-matrix is confirmed

    * homogeneous (all equations satisfied at D=0): **True**,
    * linear (max degree in the D-symbols): **1**,
    * solution set is a vector space (the toy's dimension — 4 for the
      randomly chosen coefficient pair — is instance-specific, not the
      claim; the claim is the *structure*, see next two bullets),
    * whenever a nonzero solution D₀ exists, λ·D₀ is a solution for
      arbitrary λ: **confirmed**,
    * the only scale-invariantly distinguished point is the **origin**.

  → The axioms alone can never select a *normalized* or *unique* nonzero
  D_F. Any scale is an extra, external choice. (Matches repo claim; not
  just cited.)

**Rule 6 classification.** This is a *continuous* obstruction (a real line
/ cone), not a discrete choice — so Rule 6's "forced discrete option"
loophole does not rescue it.

---

## 3. Lemma B — "Degenerate spectrum" (forced S3-type symmetry)

**Statement.** Any mechanism that (i) *produces* three generations via an
order-3 / S3-type symmetry acting on a single seed structure, and (ii)
*requires the couplings to respect* that same symmetry, forces the Yukawa
coupling into the Schur form — **with no hermiticity or symmetry assumption
needed** (full S3-invariance of a general 3×3 matrix already implies
symmetry; verified by probe below):

```
   Y  =  a·I₃  +  b·(J₃) ,      J₃ = all-ones ,
   eigenvalues = (a+2b, a−b, a−b)
```

— a **forced 2-fold degeneracy** for *all* a, b. Further: the 2-plane of
S3-*breaking* directions orthogonal to this democratic direction carries
the irreducible 2-dimensional real representation of S3 (a 120° rotation),
and therefore contains **no S3-invariant ray** — no point of it is selected
by any S3-covariant principle.

**Why this is the whole story for "same degeneracy every time."**
* Repo: Z6–Z14 (gauged SU(3)₁ order-one ⇒ Y_gen ∝ c·I₃, antisymmetric
  channel ⇒ 0; netted against Theorem B-3 the *minimal* model dynamically
  **prefers** the excluded degenerate vacuum), Z16 (sextet → SO(3)
  residual, same exclusion), Z18 (decuplet → finite Z3×Z3, kills *both*
  channels), Z22 (Gresnigt's ψ₃ reproduced; any S3-permutation-invariant
  real matrix ⇒ (a+2b, a−b, a−b)), Z23 Task A (the (H_α,H_β) breaking plane
  *is* the 120° irrep, M̄ not in its span, Tr argument is exact). (repo, L1)
* **Independent re-verification here** —
  `check_z24_s3_orbit.py` (exact sympy, no floats):
    * solving `[M,P]=0` for all 6 S3 permutation matrices over **a general
      (not-assumed-symmetric) M** returns the general invariant family with
      **exactly 2 free parameters, and it is automatically symmetric** —
      `[y8,y7]` with `M = y8·I + y7·(J−I)` (probe, 2026-08-02). Restricting
      to symmetric M from the start gives the same dimension-2 answer; the
      symmetrization step the script performed before 03:20 was a time heuristic
      that the probe has since shown to be unnecessary, not a hidden input.
      The claim is **S3-permutation invariance forces 2-fold degeneracy,
      period**;
    * exact eigenvalues `{a+3b : 1, a : 2}` ⇒ a forced 2-fold eigenvalue
      **True**;
    * the 120° rotation on the orthogonal plane has nullspace `[]` under
      (R₁₂₀ − I) ⇒ **no invariant ray** survives.

  → Both halves of Lemma B confirmed at the project's own symbolic
  standard, independently of the repo's prose.

**Rule 6 classification.** The (a,b) form is a *2-real-parameter continuum*
of couplings, not a finite discrete set — so this is a continuous
degeneracy, not a welcomed discrete selection.

---

## 4. The Master No-Go Theorem (combining the lemmas)

```
──────────────────────────────────────────────────────────────────────
THEOREM (no-go, assembled).  Consider any construction C whose
  (H1) gauge/matter content is the representation theory of Cl(10)×E8;
  (H2) the three "generations" are three copies of a representation that
       are permuted by a residual group G_gen containing an order-3/S3
       factor OR are a trivial spectator tensor factor C^3 on which the
       gauge/algebra action is generation-blind;
  (H3) the Yukawa/Dirac data are constrained only by conditions that are
       (anti)linear and homogeneous in that data (order-one, reality,
       chirality, gauge-covariance, fixed twists), or by RG equations
       equivariant under the family-basis group U(3);
  (H4) no external dimensionful input is supplied.
Then:
  (C1) No dimensionful SM parameter is derivable.            [Lemma A   + repo B-2, L1]
  (C2) The flavor coupling cannot be an isolated point:
         • homogeneous conditions ⇒ solution set is a cone;   [Lemma A, verified here]
         • U(3)-equivariant RG ⇒ fixed points form U(3)
           orbits: dim U(3)=9 a priori, so the degeneracy is UP TO
           9 real directions (smaller at special points where the
           stabilizer is non-discrete — the qualitative "no isolated
           point" claim is unaffected).              [verified here]
  (C3) Under (H2), the symmetric flavor coupling is forced
       to the 2-fold-degenerate form of Lemma B; and the
       S3-breaking plane contains no covariantly-selected ray. [Lemma B, verified here]
  (C4) Therefore the 6-or-3 complex Yukawa parameters are not
       reduced to a point, relations, or a scale by any
       construction in class (H1)–(H4).
──────────────────────────────────────────────────────────────────────
```

**Independent re-verification of the RG half of (C2) here** —
`check_z24_u3_equivariance.py` (numpy, generic Haar-ish U, seeded RNG, no
tuned entries): for the three monomial types that appear in a 1-loop
gauge-Yukawa beta function — trace term `tr(Y†Y)·Y`, cubic `Y Y† Y`, gauge
`−k·Y` — the transformation law `β(UᵀYU) = Uᵀβ(Y)U` holds to ~1e-14 in
both the symmetric and antisymmetric channels. Hence **β(Y*)=0 ⇔
β(UᵀY*U)=0**: RG fixed points come in U(3) orbits ⇒ an isolated point is
structurally impossible on the RG route too. (This matches the repo's
Task-1 equivariance claim; here it is *re-derived from the transformation
law*, not cited.)

**Status of the theorem.** The claim is explicitly scoped:

> **Claim (what is proven).** Constructions in the class (H1)–(H4) cannot
> reduce the SM free parameters. Both structural escape doors and the
> auditor's basis-dependent carve-out are closed as Rule-8 results.
>
> **What is NOT claimed.** No statement that first principles in general
> can never yield the SM parameters — that sentiment would require closing
> *every* conceivable mechanism, including ones with no known incognito
> relation to (H1)–(H4). The theorem is a sharp **class impossibility
> result**, exactly the kind that narrows future search.

L1 for (C1), (C3), and the homogeneity half of (C2); L1-conditional-on-
standard-NCG/RG-structure for the U(3)-orbit half of (C2) (verified here at
machine precision for the 1-loop monomials; 2-loop extension cannot change
the conclusion because the Higgs-VEV obstruction Task-4 is independent of
loop order). **Net SM parameter reduction: 0/19 (or 0/23).** Consistent
with every row of `MECHANISM_FAILURE_MAP.md`.

---

## 5. The theorem is falsifiable — its three escape hatches

Per Rule 9, the theorem above is only worth stating because it can be
wrong in a *specific* way. Exactly one of the following must hold to evade
it, and each is sharply checkable:

* **Escape Door 1 — break (H3): a nonlinear / D_F-covariant condition.**
  A twist or selection rule built from D_F's *own* spectral data (a
  self-referential / modular twist) breaks homogeneity. Phase Z20 found
  the canonical candidate (Ad e^{iD}) replaces line-degeneracy with a
  commutant-orbit degeneracy. One non-twist realization of the same escape
  was **built and forward-tested this session**
  (`check_z24_door1_selfconsistent.py` + `_hessian.py`): make $D_F$ a
  stationary point of its own spectral action $V(Y)=\mathrm{Tr}\,g(YY^T)$,
  so stationarity is **cubic** (nonlinear) in $Y$.
  **★ CLOSED, this session (Rule 8).** On the S3 slice with g(x)=x²−x the
  only isolated local minimum is the democratic orbit (excluded by Theorem
  B-3); every non-degenerate orbit is a saddle (exact eigenvalue
  $1-\sqrt{17}<0$). **Generalized this session to the full 18-real-dim
  complex Yukawa manifold and the whole admissible even-quartic family**
  $S=\alpha_1\,\mathrm{Tr}M+\alpha_2\,\mathrm{Tr}M^2$ ($M=YY^\dagger$,
  α₂>0 boundedness; α₁<0 is FORCED by requiring any nonzero vacuum at
  all) — `check_z24_door1_general.py`, exact in α: the U(3)×U(3) orbit
  annihilates dS (Lie-algebra level), the reduction to the 3-dim
  singular-value moduli space is exact, the stationary set is the DISCRETE
  set of orbits labelled by k = # of nonzero singular values ∈ {0,1,2,3},
  the unique strict local minimum is k=3 = democratic (excluded), and every
  non-democratic orbit carries an explicit negative moduli-Hessian direction
  (saddle) — dynamically rejected. A qualitatively different outcome needs
  either α₁≥0 (only minimum = origin, no Yukawa at all, also excluded) or a
  basis-DEPENDENT potential not of the form f(singular values) — itself a
  free continuous external choice (Rule 1/6). The mechanism reconciles with
  Lemma B instead of defeating it: **isolation exists, but only at an
  excluded point.**

  **★ Door 1-prime (basis-dependent escape) also CLOSED this session**
  (`check_z24_door1_basis_dependent.py`): the auditor's carve-out — a
  selection potential not of the form f(singular values) — necessarily picks
  a preferred basis, i.e. a Hermitian B ∈ Herm₃, dim_R = 9 (verified exactly
  by counting independent reals). The forward test
  $S_B = \alpha_1\mathrm{Tr}M+\alpha_2\mathrm{Tr}M^2+\lambda\,\mathrm{Tr}(YBY^\dagger)$
  shows the vacuum aligns with eigenbasis(B) EXACTLY (overlap = 1.0000) in
  every run and the rank/hierarchy track B's spectrum, not anything in the
  algebra. Rule-9 ledger: to reproduce 3 SM masses one must input B's 3
  eigen-splittings + global scale inside the 9 real of B, while the
  stationary radii supply at most k+1 real — **net real parameter reduction
  = 0, and B is unconstrained by Cl(10)×E8**. The boundary cases (λ→0,
  degenerate B) fall back to the basis-INDEPENDENT closure. Together with
  Door 1-general this exhausts the class "single spectral-triple vacuum
  selection on Cl(10)×E8 with no external input": every member either
  selects democratic/excluded structure (basis-independent) or echo's its
  own input (basis-dependent).
* **Escape Door 2 — break (H2): generations not related by any order-3/S3
  symmetry at all.** If the three generations are *not* three permuted
  copies (no S3 residual at all) and *not* a spectator C^3, Lemma B does
  not apply. The one known construction of this type is generations as an
  **index-theoretic zero-mode multiplicity** of a Dirac operator on an
  internal compact geometry whose Clifford algebra is Cl(10).
  **★ TESTED AND CLOSED, this session (Rule 8).**
  `check_z24_door2_index_generations.py` builds the Atiyah–Singer index for
  $\mathrm{index}(D_{\mathcal O(k)})=\int \mathrm{ch}(\mathcal O(k))\,
  \mathrm{Td}(TK)$ on the internal target Cl(10) actually permits (compact
  CY5, holonomy SU(5)), constructing ch and Td **from first principles**
  (Newton sums; $c_1=0$ CY condition). Exact result:
  `index = (1/720)∫(c5 + 90 c2² − 2 c4 + 3k(30 c2² − c4) + …)`,
  i.e. it depends on the free topological invariants χ, ∫c₂², ∫c₄ — none
  of which Cl(10) fixes. Recovering "3" requires *choosing* an internal
  manifold+bundle whose invariants sum to 3, which **is** the free
  parameter in topological costume. Lemma B is evaded (no S3 anywhere), so
  the closure is purely Rule 6: a non-forced discrete choice. Door 2
  reduces no parameter — it relocates it.
* **Escape Door 3 — break (H4): inject a scale from outside.** Any
  dimensionful answer needs a dimensionful input the algebra lacks.
  Supplying one (compactification scale, landscape point, cosmological
  boundary condition) **is** the extra, choice-laden input — Rule 2/9 then
  applies to *that* choice. Not a derivation from first principles.

A result that claims to derive the SM parameters from Cl(10)×E8 without
going through one of these three doors is, by the theorem, making an
arithmetic or labeling error somewhere — which is exactly what every past
route turned out to be doing.

---

## 6. The untried doors, scoped with Rule 9 pre-committed and CLOSED

Both door classes were tested this session (Rule 8 closures, not
rescues). The pre-registered net-parameter ledger used for the verdicts:

```
   parameters removed  −  parameters introduced   <   0  for failure
                                                   =
                                                   >  for genuine progress
   ─────────────────────────────────────────────────────────────
   removed:  the 6 (or 3) complex flavor Yukawas     [...if replaced]
   introduced (must count honestly):
     • choice of internal compact space / its discrete data   (≥1 discrete choice)
     • continuous geometric moduli of that space              (≥1 real, v-like)
     • the still-needed external mass/dimensionful scale      (H4 still bites)
   ─────────────────────────────────────────────────────────────
   VERDICT CONDITION: the move counts as progress ONLY IF the discrete
   geometric data are FORCED (finite set, no fit) AND the moduli are
   fixed by an independent consistency condition — else Rule 6 says the
   continuous moduli are just the Yukawas wearing a new costume.
```

**Two further structural obstructions that Door 2 cannot by itself remove**
(repo, L1, unaffected by the internal space): (i) the
`docs_new` RG analysis's Task-4 obstruction — physical CKM/PMNS need Higgs
**VEV ratios** fixed by a potential, which flavor-blind RG / geometry of
the *Yukawa* sector does not touch; (ii) any flavor-blind RG still has
U(3) orbits (Lemma-4.5 here). So Door 2, at best, addresses only the
*internal Yukawa texture* — the honest ceiling even of its best case.

---

## 7. Recommendation

**Do Option A:** promote Section 4's Master No-Go from "assembled from 10
separate phases" to a single stated theorem with the two pillars
re-verified as done here (homogeneity → cone; S3-residual → forced
degeneracy + free VEV direction), and the three falsifiable escape doors
listed. That converts 25 "same outcome" phases from a frustration into a
citable impossibility result with sharp hypotheses — which is what the
current literature (e.g. order-3/S3 generation models) actually walks
into. Then, *optionally*, run Door 2 as a single scoping session against
the Section-6 ledger, expecting a clean Rule-8 closure. **Both doors are
now closed (Rule 8); the residual option set is A (ship the impossibility
theorem) or C (inject an external dimensionful/discrete input — explicitly
not first-principles).**

**Reproducibility.** All verification is in
`session_new_files/phase_z24_free_parameter_from_first_principles/`:

| Script | Verifies | Standard |
|---|---|---|
| `check_z24_no_scale.py` | Lemma A (order-one homogeneous+linear ⇒ cone, no unique scale) | exact sympy |
| `check_z24_s3_orbit.py` | Lemma B (S3 ⇒ forced 2-fold degeneracy — *including* the general non-symmetric case, which invariance alone already forces symmetric; breaking plane = irrep, no invariant ray) | exact sympy |
| `check_z24_u3_equivariance.py` | RG half of (C2) (β exactly equivariant ⇒ U(3) orbits) | numpy ~1e-14, seeded |
| *(probe, 2026-08-02)* | non-symmetric S3 commutant also dim 2 and automatically symmetric | exact sympy, inline |
| `check_z24_door1_general.py` | Door 1 on full complex 18-dim Y, whole even-quartic admissible family: discrete k-orbits, unique min = democratic (excluded), saddles for k<3 | exact sympy in α |
| `check_z24_door1_basis_dependent.py` | Door 1′ (the auditor's basis-dependent carve-out): preferred basis B costs exactly 9 real params; vacuum aligns to eigenbasis(B) at overlap 1.0000, hierarchy follows B ⇒ net parameter reduction 0 | exact dim count + seeded numeric dynamics |

No Standard Model numerical value was inserted or matched anywhere in this
document or its scripts. All claims are forward-computed from the stated
algebra.

**Post-review corrections applied 2026-08-02 ~03:20 (this session's own
Rule-4 audit of this document):** (1) Lemma B upgraded — the script's
earlier `symmetric M` was a heuristic; a direct probe of the general 3×3
commutant shows S3-invariance alone already forces the symmetric (a,b)
form, dimension still exactly 2. (2) Lemma A's toy "solution space
dimension 4" relabeled instance-specific; the structural claim is
homogeneity+linearity (True, degree 1), which the toy demonstrates and a
chirality-flipping `[[0,T],[T†,0]]` free-form rerun confirms independently.
(3) C2's "9 real directions" clarified to "up to 9 (dim U(3)=9) real
directions, smaller at special fixed points." No conclusion changed; one
(C3/Lemma-B) got strictly stronger.
