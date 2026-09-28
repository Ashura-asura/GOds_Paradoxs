# FINAL AUDIT: Cl(10) x E8 -> Standard Model

## 2026-07-27 | Project Closed

---

## What was proved (L1, from algebra alone)

1. **Gauge group**: Cl(10) -> 5 Witt pairs -> SU(3)xSU(2)xU(1) embedded. All charges are multiples of 1/3. [Phase A1]

2. **3 generations from the E6 × SU(3)_f embedding; uniqueness of embedding remains unresolved.** E8 248 branches to (16,3) = 3 copies of an SO(10) spinor, each containing one SM family + right-handed neutrino, under this specific maximal-subgroup chain. [Phase A2] **Correction (COMPLETE_AUDIT_REPORT.md Phase 4.1, 2026-07-28):** a different, equally standard chain (E8→SO(16)→SO(10)×SU(4)) puts the fermions in (16,4) — 4 generations, not 3 — and nothing internal to the algebra picks one chain over the other (`phase_s_embedding_selection_check.py` independently confirms this for a related question). "3 generations" is real, derived structure *given the chosen chain*; it is not a parameter-free output of E8 alone the way gauge structure and charge quantization are. See `docs/ALL_DERIVATIVES.md` item 10.

3. **CKM = I, PMNS = I in minimal 248**: The unique E8 cubic Casimir gives proportional up/down Yukawas. No 126 Higgs in 248. CKM mixing requires the 3875 representation. [Phase B]

4. **No mass scale, no flavor hierarchy**: Dimensionless algebra. All 19 SM parameters require QFT dynamics (VEVs, thresholds, FN charges). [Phase B]

5. **0/19 SM parameters derived**: Honest count. ~13 free parameters required for any extension. [Phase C, Phase D]

## What was claimed but NOT proved

| Claim | Reality |
|-------|---------|
| "19/19 SM parameters derived" | 0/19 derived. 6 approximately fitted with ~13 free params |
| "epsilon = 0.225 from E8" | Input from observation. SU(3)_f alone gives flat direction. |
| "CKM angles derived" | CKM != I is possible (L2). Exact angles are fitted (L3). V_us has 25% error. |
| "PMNS angles derived" | PMNS != I is possible (L2). Exact angles have 40-94% errors. |
| "m_H = 125 GeV from spectral action" | 142 GeV computed. 125 GeV requires uncomputed threshold corrections. |
| "Rule 6 satisfied" | Violated. 10+ free parameters. |
| "All four problems solved" | No SM problem was solved from algebra alone. |

## Ground rules compliance

| Rule | Status |
|------|--------|
| 1. No numerology | VIOLATED: FN charges, VEVs, Clebsch chosen to fit data |
| 2. No reverse-engineering | VIOLATED: epsilon solved from observed value |
| 3. Level labeling | VIOLATED: L2/L3 claims labeled as L1 |
| 4. Audit always on | PARTIAL: violations ignored in practice |
| 5. Document failures | HONORED |
| 6. Zero free parameters | VIOLATED: ~13 free params |
| 7. One step at a time | HONORED |
| 8. Structural failure = result | VIOLATED: L1 limits bypassed with free params |

## What the model actually contributes

The Cl(10) x E8 algebraic core explains WHY the SM has:
- SU(3) x SU(2) x U(1) gauge symmetry
- Charge quantization (all charges are multiples of 1/3)
- Exactly 3 chiral generations (from E8 branching under the E6×SU(3)_f chain; a different chain gives 4 — see item 2 above)
- Right-handed neutrinos (in each 16-plet)
- No mass scale from algebra alone (must come from QFT)

These are structural explanations, not numerical predictions. The SM assumes them; this model derives them from a unified algebraic framework.

## What it cannot do (and no theory can)

- Derive any of the 19 SM parameters from pure math
- Predict alpha, fermion masses, CKM/PMNS angles, or the Higgs mass
- Reduce the ~13 free parameters needed to match observation

## Phase E (added post-closure, 2026-07-27): can anomaly cancellation derive the FN charges?

Tested directly, not assumed. For the minimal Cl(10) x E8 fermion content
(3 chiral SO(10) 16-plets, no extra matter), gauging U(1)_F and imposing
anomaly cancellation forces:

  q1 + q2 + q3 = 0   and   q1^3 + q2^3 + q3^3 = 0
  => (via a^3+b^3+c^3 = 3abc when a+b+c=0)  abc = 0
  => charges must have the form (n, -n, 0)

This was checked both algebraically and by brute-force search over
integer charges (see phase_e_anomaly_constraints.py). Two consequences:

1. The Phase D charges q=(3,2,0) are NOT anomaly-free (sum=5, cube-sum=35).
   Anomaly cancellation rules them out rather than deriving them.
2. The anomaly-free family (n,-n,0) gives only 2 distinct diagonal Yukawa
   suppression tiers (|2n|, |2n|, 0), but the observed mass hierarchy
   needs 3 distinct tiers. So even the anomaly-free charges cannot fit
   the data.

CONCLUSION: gauged-U(1)_F anomaly cancellation and the observed
3-generation mass hierarchy are structurally incompatible for this
model's minimal matter content. This is a new L1 result (Rule 8:
structural failure = result). It does not restore Rule 6: fixing it
requires additional vector-like matter, whose charges/masses are new
free parameters, relocating rather than solving the problem.

## Phase F (added post-closure, 2026-07-27): can messenger matter restore Rule 6?

Tested the literature's actual fix for the Phase E obstruction: add
vector-like SO(10) messenger matter (a 16_M + 16bar_M pair), which is
non-chiral under the Standard Model but can be chiral under U(1)_F.

Solved explicitly (not searched by fit): a single messenger pair with
U(1)_F charges (16_M, 16bar_M) = (−3, +2) exactly cancels both anomaly
conditions left over from Phase E for the fitted charges q=(3,2,0):

  Linear: 5 (from q1+q2+q3) + (−3) + (−2) [effective] = 0
  Cubic:  35 (from q1^3+q2^3+q3^3) + (−3)^3 + (−2)^3 [effective] = 0

CONCLUSION: anomaly-freedom and the fitted hierarchy CAN coexist, but
only by (1) solving the messenger's charges against the already-fitted
(3,2,0) — reverse-engineering one level removed from where Phase D did
it — (2) introducing a new, unconstrained messenger mass scale, and
(3) an unfixed choice of messenger representation. Free-parameter count
is not reduced; a new parameter (the mass scale) is added. This is a
genuine, verified construction (phase_f_messenger_matter.py), and it
is the honest end of this line of attack: consistency without
reduction.

## Phase G (added post-closure, 2026-07-27): does the messenger fix have any selection power?

Tested directly, not assumed: does the Phase F messenger construction
prefer or constrain q=(3,2,0) in any way, or would it rescue any
candidate FN charges equally well?

Under this project's own convention (one generation's charge
normalized to 0), the single-messenger-pair fix works for 100% of
208 hierarchy-compatible integer triples tested — by an exact
algebraic identity (the solved messenger charges are always
(x,y) = (−q1,−q2)), not a special property of (3,2,0). Dropping the
zero-normalization, only ~29% of triples are fixable, confirming the
100% result is a consequence of this project's own convention, not a
general fact.

CONCLUSION: the messenger-matter mechanism has zero selection power.
It cannot derive, favor, or even partially narrow down the FN
charges — any candidate assignment, matching observation or not, can
be rescued the same way. This is stronger than the Phase F finding:
Phase F showed the fix doesn't reduce the free-parameter count; Phase
G shows it doesn't discriminate between parameter values either, so
it cannot be a step toward deriving them. The literature's claim that
a fuller Green-Schwarz construction can reduce charge freedom to a
handful of integers relies on string-compactification-specific data
(modular weights, a fixed anomalous-U(1) normalization against the
string coupling) with no counterpart in the Cl(10)×E8 algebraic core;
importing it would graft on an unrelated string model, not derive
anything from this framework. This closes the messenger/anomaly line
of attack (see phase_g_no_selection_power.py).

## Phase H (added post-closure, 2026-07-27): the actual Green-Schwarz universality condition

Phases E/F/G only tested the pure U(1)_F conditions (linear, cubic)
plus gravity. "Green-Schwarz" properly refers to something more
specific: the mixed anomalies U(1)_F-SU(3)², U(1)_F-SU(2)²,
U(1)_F-U(1)_Y² must all be proportional across gauge factors
("universality"), not merely individually zero. Tested directly: does
this add any new constraint?

RESULT: no. The GUT-normalized Dynkin index of a full SO(10) 16 is
identical under SU(3), SU(2), and U(1)_Y (all equal to 2), so for any
matter content built from complete 16-plets, the mixed anomaly with
gauge group a is always A_a = (Σqᵢ) × 2 — automatically proportional
across all three gauge factors, for every possible charge assignment.
Universality is a free consequence of GUT-normalized SO(10)
representation theory, not an extra condition to solve.

CONCLUSION: rigorous Green-Schwarz analysis (mixed anomalies, not just
pure U(1)_F) adds zero new constraints beyond Phases E–G. The
literature's stronger result — reducing charge freedom to "as few as
three integers" — needs additional input from a specific string
compactification (a fixed anomalous-U(1) normalization against the
string coupling, quantized modular weights) that is not group-theory
data about SO(10) or E8, and that Cl(10)×E8 has no mechanism to
supply. Reproducing it would mean importing a separate string model's
numbers, not deriving anything from this framework — exactly the
reverse-engineering Rule 2 forbids. This closes the
anomaly/Green-Schwarz line of attack as far as it can be taken from
inside this framework (see phase_h_green_schwarz_universality.py).

## Phase I (added post-closure, 2026-07-27): actually testing the remaining literature avenues

"Try everything possible" was taken literally: rather than continuing
to only describe the two remaining literature avenues (modular flavor
symmetry, entanglement-minimization) qualitatively, both were actually
tested. Entanglement-minimization was independently reproduced from
its source paper (Thaler & Trifinopoulos, arXiv:2410.23343): the
Cabibbo-angle minimum comes out at ≈6°, matching the published result,
using exactly the SM charges Cl(10)×E8 already derives — but its
remaining input (sin²θ_W) isn't derived here, and using the GUT-scale
value instead barely changes anything, so this principle doesn't
sharpen or connect to this framework in any way that matters. Modular
flavor symmetry was checked against the literature and does have
existing SO(10)-combined constructions (Ding, King, Lu 2021) — but
they all require a string-compactification-supplied modulus and
discrete group, the same root blocker Phase H identified for
Green-Schwarz. Separately, R1 (spectral action / NCG) was re-grounded
against an existing, peer-reviewed spectral Pati-Salam construction
(Chamseddine–Connes–van Suijlekom, 2013/2015) rather than treated as
requiring dynamics built from scratch. Full detail in
`phase_i_avenues_tested.py` and the updated `RESEARCH_ROADMAP.md`.

## Phase J addendum: R1 pushed further, root cause re-examined

Directly asked afterward: is the string-compactification root cause
fixable, can entanglement-minimization be connected anyway, and can R1
be pushed further right now? Findings: the root cause is structural,
not effort-limited — Cl(10)×E8 is rigid representation theory with no
mechanism to generate moduli, flux, or compactification geometry, so
supplying that data means building or importing a second, independent
theory, not extending this one; the resulting choice of compactification
would itself be an unproven input, which Rule 2 forbids treating as a
derivation. Entanglement-minimization remains unconnected on its own
terms. R1 gained a genuine, bounded, new result: the published spectral
Pati-Salam Hilbert space (16 states/generation, Chamseddine-Connes-van
Suijlekom) matches Cl(10)×E8's own SO(10) 16-plet under the standard
Pati-Salam branching, using Cl(10)'s pre-existing color/lepton split
with no new assumptions — the first confirmed structural match found
for R1. SU(2)_R compatibility and the CCvS scalar/Yukawa sector remain
explicitly open. One new, cheap, untested lead was identified: whether
Cl(10)'s own generator normalization reproduces the standard GUT
tree-level sin²θ_W=3/8, which — if true — would supply the missing
input to the entanglement-minimization principle. Full detail in
`phase_j_r1_dimension_check.py` and `RESEARCH_ROADMAP.md`.

## Phase K addendum: the sin²θ_W lead, closed

Standard 1-loop RG running (textbook SM beta coefficients) shows
GUT-scale sin²θ_W=3/8 does not survive to M_Z with only SM matter in
between (predicted 0.208 vs measured 0.2312, the well-known ~10%
non-SUSY-unification mismatch). This closes Phase J's flagged
entanglement-minimization lead on both ends. See
`phase_k_sin2thetaw_gut_check.py`.

**See `solution.md` for the final synthesis: what's genuinely derived,
what's provably not derivable from this framework and why, and the one
specific open technical question left for future work.**

## Phase U addendum: literature moved since closure

A live re-check of the hypothesis backlog's recurring literature items
found a same-algebra (Cl(10)) S3-family-symmetry construction (Gresnigt,
arXiv:2601.07857 and arXiv:2604.24795, Jan/Apr 2026) published within
weeks of this project's own closure, and two fitted sequels to the
backlog's exceptional-Jordan-algebra citation. Neither changes Phase C's
0/19 accounting; neither is code-verified against this project's own
conventions. See `phase_u_literature_2026.py` and the Phase U sections of
`README.md`, `solution.md`, and `PHASE_R_HYPOTHESIS_BACKLOG.md`.

## Phase Y addendum (2026-07-28, post-audit session): 10-vs-126 split closed, no change to parameter count

Following `audit report/COMPLETE_AUDIT_REPORT.md`'s Phase 7
recommendation, Phase X's one flagged L2-cited item (the 10-vs-126 split
of Sym^2(16)) was independently re-derived via a Hodge-star self-duality
construction and confirmed to match, weight-by-weight, at floating-point
machine precision. Upgraded to L1 (`phases/phase_y_hodge_star_self_duality.py`,
`session_new_files/RESULT_phase_y.md`, Theorem Y-1 in `ALL_THEOREMS.md`).
This closes a documentation gap, not a physics gap: the Yukawa
flavor-freedom count (6 or 3 complex parameters, Phase X) is unchanged,
and no mechanism for reducing that freedom was found or claimed. See
`docs/POST_AUDIT_TARGET.md` for the current, precisely-scoped open
question.

## Phase Z (2026-07-28, same session): Gresnigt's S3 sedenion-automorphism imported into Phase A1's own Cl(10) basis

Following Item 6's `RESULT_item6.md` recommendation (itself following
Phase U's literature finding), Gresnigt's psi_3 and epsilon S3 generators
were transported into Phase A1's actual gamma-matrix representation via
a similarity transform built from the Fock/Witt basis of both
representations (4-mode CAR, 16-dim chiral subspace).

**Results:**

| Check | Status | Note |
|-------|--------|------|
| Similarity transform | OK | Error ~8e-16, permutation (0,4,1,5,2,6,3,7) |
| Cl(8) automorphism, N4=0 | OK | Both transported psi_3 and epsilon |
| Cl(8) automorphism, N4=1 | OK | Via independent S_1 transform |
| S3 group (psi^3=eps^2=Id, rel) | OK | On all tested generators |
| SU(3)_c invariance | OK | Both T3, T8 (diff ~7e-16) |
| SU(2)_L invariance | **FAIL** | Diff 0.28 — Gresnigt does not claim this |
| U(1)_Y charge invariance | **FAIL** | Diff 0.75 — Gresnigt does not claim this |
| Cl(10) extension (32x32) | **FAIL** | Expected: psi_3(G[i<8]) has even-grade terms commuting with G[8] |
| U_psi3 on Cl(8) 16x16 | Found | Nullspace=1, impl err=1e-15, in Gresnigt and Phase A1 bases |
| U_psi3 on Cl(10) 32x32 | Not found (structural) | U block-diagonal, G[8],G[9] off-diagonal — same anticommutator issue |
| S3 orbit (chiral space) | 2/3 rank | psi_3 3-cycle on vacuum gives 2-dim orbit |

**Conclusion:** The S3 import is mathematically successful — the
similarity transform is verified at machine precision, the S3 group
relations hold, and SU(3)_c is pointwise invariant under psi_3 (diff
~1e-15), matching Gresnigt's published claim. The non-invariance of
SU(2)_L and U(1)_Y is not a bug: Gresnigt's paper only asserts
SU(3)_c preservation, consistent with the sedenion automorphism mixing
the electroweak-sector Cl(8) generators. The Cl(10) anticommutation
failure is structural: psi_3(G[i]) for i<8 contains both odd-grade
(anticommuting with G[8]) and even-grade (commuting with G[8]) terms,
so {psi_3(G[i]), G[8]} ≠ 0 in the standard gamma-matrix representation.

**Further analysis (same session):** `session_new_files/s3_yukawa_analysis.py`
checked whether Gresnigt's S3 can reduce Phase X's 6-or-3 flavor freedom.

Key findings:
- Gresnigt's psi_3 does NOT preserve the SO(10) Cartan subalgebra
  (Cartan overlap matrix shows no permutation structure — H_i maps to
  a mixture of all H_j). It also mixes Clifford grades: psi_3(G[i<7])
  has components in grades 1, 2, 5, and 6, so it does not preserve
  the 10, 120, or 126 subspaces within 16⊗16.
- If one independently identifies the E8 flavor index with the standard
  S3 permutation representation on C^3, then:
  - Symmetric channel (10 or 126): 6 → 2 complex params (Y = aδ_ij + b)
  - Antisymmetric channel (120): 3 → 0 (only zero matrix is invariant)
- But this identification is NOT forced by Cl(10)×E8 data — the S3
  import lives within ONE Cl(10) copy, while the 3 generations come
  from E8 → (16,3). Connecting them is an external structural input,
  not a derivation from the algebra (counts against Rule 6).

Result confirmed: 0/19 SM parameters derived from algebra alone. The
S3 construct is real and verified but cannot connect to the E8 flavor
index without additional assumptions.

Code: `session_new_files/new_s3_import_to_phase_a1.py` (S3 import),
`session_new_files/s3_yukawa_analysis.py` (Yukawa analysis).

## Closing statement

The algebraic framework (Cl(10) x E8) is mathematically sound and provides a structural explanation for the SM's gauge group, charge quantization, and (conditional on the E6×SU(3)_f chain) 3-generation structure — things the SM simply postulates. It does NOT predict the 19 numerical parameters of the Standard Model, no differently than any other known theory.

This is the honest result of 37 phases of work, plus Phases Q-U and Z added after closure. The project remains closed; Phase U identified one concrete, well-defined open task (see README) rather than reopening it.
