# Research Roadmap: What's Actually Known, and Where to Spend Time Next

**Written 2026-07-27. Hypothesis-level document — treat every item in Part 2
as a conjecture to be tested, not a claim already established.**

This document has one job: separate what this project has *actually,
purely derived* (zero free parameters, no fitting, no assertion) from
everything else — and lay out where continued effort could plausibly
lead somewhere, versus where it provably cannot (see Phases E–H).
Updated 2026-07-27 (Phase I) after actually testing, rather than just
describing, the two literature avenues (modular flavor symmetry,
entanglement-minimization) and re-grounding R1 against real published
work (spectral Pati-Salam).

---

## Part 1 — What Is Purely Derived (L1, zero free parameters)

Everything below follows from algebra alone: Clifford algebra Cl(10)
structure and/or E8 representation theory, with no numbers put in by
hand, no VEVs chosen, no charges fitted. If you remove any single one
of these results, no part of the framework's algebra changes — these
are theorems, not choices.

| # | Result | Why it's pure (no free parameters) | Source |
|---|--------|-------------------------------------|--------|
| 1 | Cl(10) → SU(3)×SU(2)×U(1), with electric charge quantized in units of 1/3 | Follows from the Witt decomposition of Cl(10) into 5 pairs; a fact about the algebra's automorphism structure, not a choice | `phase_a1_cl10_core.py` |
| 2 | E8's adjoint (248) branches to give exactly 3 copies of an SO(10) 16-plet (3 generations + right-handed neutrino) | Standard E8 branching rule; a fixed fact of the group, same for anyone who does this computation | `phase_a2_e8_core.py` |
| 3 | In the minimal 248 embedding: CKM = identity, PMNS = identity (no fermion mixing at all) | The unique E8 cubic Casimir forces proportional up/down-type Yukawas; proven, not assumed | `phase_b_structural_limits.py` |
| 4 | No mass scale and no flavor hierarchy exist in the algebra by itself | The algebra is dimensionless; a triviality, but a real and useful one — it tells you *where* physics has to enter | `phase_b_structural_limits.py` |
| 5 | The flavon-breaking parameter ε has its potential minimum exactly at ε = 0 in the minimal SU(3)-flavor setup | A genuine flat-direction theorem — the model's own algebra forbids ε from taking any nonzero value without extra input | `phase_b_structural_limits.py` |
| 6 | Gauging the horizontal U(1)_F and demanding anomaly-freedom forces FN charges into the form (n, −n, 0) | Direct consequence of `a³+b³+c³=3abc` when `a+b+c=0` — pure number theory applied to the model's own field content | `phase_e_anomaly_constraints.py` |
| 7 | Charges of the form (n, −n, 0) can only ever produce 2 distinct Yukawa-suppression tiers, never the 3 the real mass hierarchy needs | Direct algebraic consequence of #6 | `phase_e_anomaly_constraints.py` |
| 8 | The vector-like-messenger "fix" for #6/#7 has zero selection power: under this project's charge convention, it rescues 100% of candidate charge assignments via an exact identity (x,y) = (−q1,−q2) | Verified by direct computation over hundreds of candidate triples, not asserted | `phase_g_no_selection_power.py` |
| 9 | The full Green-Schwarz mixed-anomaly ("universality") condition — not just the pure U(1)_F conditions above — is automatically satisfied for any matter built from complete SO(10) 16-plets, since the GUT-normalized Dynkin index of a 16 is identical (=2) under SU(3), SU(2), and U(1)_Y | Direct computation of representation-theory indices; holds for every possible charge assignment, not a fitted case | `phase_h_green_schwarz_universality.py` |
| 10 | 0 of the Standard Model's 19 numerical parameters are derivable from this algebra; ~13 free parameters are required to reproduce them at all | An honest count, not a derivation of a number — but it is itself a rigorous, zero-free-parameter *meta-result* about the framework's limits | `phase_c_honest_accounting.py`, `phase_d_parametric_model.py` |

**What this list actually buys you:** a real, non-trivial explanation
for *why* the Standard Model has the gauge group it has, why charge
comes in thirds, and why there are exactly three generations. That is
not nothing — but it is also not new physics (1980s Clifford-algebra
results, standard E8 branching), and it stops completely at the
boundary of anything numerical.

**What continued work on charges/anomalies/messengers cannot do:**
items 6–9 above are not "not yet solved" — they are *proven closed*.
Time spent trying to extend the messenger-matter or gauged-U(1)_F
route further, within this framework, is time spent re-deriving a
result that's already nailed down. That door is shut; move to Part 2.

---

## Part 2 — Where To Actually Focus (hypothesis-level roadmap)

Everything below is a **conjecture about a possible research direction**,
ranked by how much it could plausibly change the picture in Part 1 —
not a promise that it works. Treat each "first step" as something you
could sit down and start on now, honestly, without pretending it's
already solved.

### R1 — Give the framework dynamics (highest leverage, updated 2026-07-27)

**The core problem:** everything in Part 1 comes from pure
representation theory — group elements and branching rules, no action,
no equations of motion. A framework with no dynamics *cannot*, in
principle, output a number. This is the actual root cause of every
failure in Phases B–H, not a gap that better bookkeeping can close.

**Update — this direction is better-grounded than first thought.**
A literature check (2026-07-27, Phase I) found that Chamseddine,
Connes, and van Suijlekom already extended the spectral-action /
noncommutative-geometry Standard Model specifically to **Pati-Salam
unification**:
- "Beyond the Spectral Standard Model: Emergence of Pati-Salam
  Unification," JHEP 11 (2013) 132.
- "Grand Unification in the Spectral Pati-Salam Model," JHEP 11 (2015)
  011 — includes an explicit one-loop gauge-coupling running and
  unification analysis.

Pati-Salam (SU(4)×SU(2)×SU(2)) is a maximal subgroup in the very
SO(10)-breaking chain this project's own Cl(10)→SO(10) embedding
passes through. This changes the shape of R1: the honest first step
is no longer "build a spectral triple from scratch" — it's **"check
whether the existing, published spectral Pati-Salam construction's
finite algebra and Hilbert space matches the fermion content
Cl(10)×E8 already derives."** That's a well-posed comparison, not a
new invention.

**Concrete first steps (tractable now, not a finished project):**
1. Study the actual spectral Pati-Salam construction (the two papers
   above) well enough to extract its finite algebra `A_F`, Hilbert
   space `H_F`, and Dirac operator `D_F`.
2. Check directly whether Cl(10)'s existing Witt-pair structure
   (already coded in `phase_a1_cl10_core.py`) and its derived 3×16
   fermion content (Part 1, item #2) match `A_F`/`H_F` as used in
   that construction, or need translation/extension. This is a real
   yes/no comparison you can work through, not a matter of opinion.
3. If it matches (even partially): the existing spectral Pati-Salam
   gauge-coupling-unification analysis becomes something to check
   against this project's own Phase C/D free-parameter count directly
   — does adopting it change which of those ~13 parameters remain
   free, or just relabel them?
4. If it doesn't match: that mismatch is itself real, honest
   information about where Cl(10)×E8 diverges from finite geometries
   already known to produce a working spectral action — document it
   in the same spirit as Phases E–H.

**Honest scale-setting (revised):** verifying/adopting an existing
peer-reviewed construction is a smaller lift than building new
mathematics from zero, but it is still real technical work — reading
and correctly reproducing 2013–2015-level NCG papers, then doing a
careful representation-theoretic comparison. Plan in weeks-to-months,
not phases-per-day. Building anything beyond that (an actual new
result specific to Cl(10)×E8, e.g. deriving the E8 piece the Pati-Salam
papers don't have) remains genuine open research with no guaranteed
payoff.

### R2 — Replace fitted VEVs with a derived potential minimum

**Hypothesis:** once (and only once) R1 produces an actual scalar
potential from the spectral action — not before — the free parameters
in Phase D (ε, φ₁₂₆'s VEV, the SO(10) Clebsch coefficients) become
candidates for *minimization* rather than *fitting*.

**Why this can't be done first:** doing this without R1's action in
hand means inventing a potential by hand to get the answer you want —
which is exactly Ground Rule 1 (no numerology) and Rule 2 (no
reverse-engineering) territory. This step is only meaningful as a
consequence of R1 succeeding, not a parallel track.

**First step, if R1 succeeds:** take whichever potential terms the
spectral action actually generates (not ones chosen for convenience),
solve for their minima symbolically, and *only then* compare the
result to the observed ε ≈ 0.225, VEV ratios, etc. If the minimization
requires additional unmotivated terms to reach the observed values,
that's Phase-E/G-style evidence the derivation isn't real — document
it as such rather than adding the term quietly.

### R3 — Gravity

**Hypothesis:** this is less a separate research track than a
by-product to check for. The entire appeal of the spectral-action
approach (R1) is that gravity is not optional or bolted on — the a4
heat-kernel term is generically the Einstein-Hilbert action. If R1
produces a working spectral triple at all, the honest next step is
simply to check whether that term appears with the right sign and
structure, using the *same* Dirac operator, no separate assumptions.
If R1 doesn't get built, this question doesn't arise yet — don't
attempt gravity in isolation from an algebra with no dynamics; it will
only produce another free-parameter patch.

### R4 — Anomaly/Green-Schwarz done "for real" (now DONE, closed)

Update (2026-07-27): done, not just recommended against. Phase H
implemented the actual Green-Schwarz condition — mixed anomaly
universality across gauge groups, not just the pure U(1)_F checks in
Phase E/F/G — by computing the GUT-normalized Dynkin index of a full
SO(10) 16 under SU(3), SU(2), and U(1)_Y. All three came out equal (=2),
which means universality is automatically satisfied for any matter
built from complete 16-plets, adding zero constraint beyond what was
already tested. This is now a closed, verified result
(`phase_h_green_schwarz_universality.py`), not an untested option.

What remains genuinely out of reach is the literature's stronger
result (charge freedom reduced to as few as three integers), which
needs actual string-compactification data — fixed modular weights, a
string-coupling-normalized anomalous U(1) — that Cl(10)×E8 has no
mechanism to supply. Pursuing that further means importing a separate
string-theoretic model wholesale, not extending this one. **Recommend:
do not invest further time here** unless the actual goal shifts to
string model-building for its own sake, independent of Cl(10)/E8.

### R5 — Demand one falsifiable number before calling anything solved

Whatever comes out of R1–R2 (if anything does), the actual test of
whether this has become physics rather than bookkeeping is simple: it
must produce **at least one number — a mass ratio, a mixing angle, a
coupling relation — that emerges before you look at data**, which can
then be checked and potentially falsified. Anything that requires
checking the answer first to know which of several free choices to
make does not count, no matter how elegant the derivation looks.
Apply Phase E/F/G-level skepticism to any future "success" here too.

---

## Priority order, plainly stated

1. **R1** — the only direction with a real chance of changing anything
   in Part 1, and now better-grounded (2026-07-27): an existing,
   peer-reviewed spectral Pati-Salam construction is a concrete
   candidate to check against, not a blank page. Real work, genuinely
   uncertain payoff, but the only door that isn't already closed.
2. **R2, R3** — meaningful only as consequences of R1 succeeding; not
   independent projects.
3. **R4** — done and closed for this framework (Phases G-H, verified). Skip.
4. **Modular flavor symmetry** — tested (2026-07-27, Phase I): real
   SO(10)+A4-modular models exist in the literature (Ding, King, Lu
   2021), so this isn't "never connected to SO(10)" — but the modulus
   and discrete group are string-compactification data, the same root
   blocker as R4/Phase H. Same verdict: not derivable from Cl(10)×E8
   alone. Skip unless the goal shifts to string model-building.
5. **Entanglement-minimization** — tested (2026-07-27, Phase I): the
   Thaler–Trifinopoulos calculation was reproduced independently
   (Cabibbo angle ≈6°, matching the published result). It uses the
   same SM charges Cl(10)×E8 already derives, but its only other input
   (sin²θ_W) isn't derived by this framework either, and even the
   GUT-scale value doesn't change the result meaningfully. A genuinely
   interesting, self-contained principle — but it does not connect to
   or reduce this project's free parameters. Skip for this project's
   purposes; worth knowing about on its own terms.

**The honest summary: everything provable without dynamics has now
been proven (Part 1, including its negative results in Phases E–H).
The only route left that isn't a dead end is giving the algebra an
actual action — R1 — and that is real, slow, uncertain research, not
a phase you can close in a day.**

## Phase J addendum (2026-07-27): R1's first real check, done

Requested directly: can the string-compactification root cause be
fixed, can entanglement-minimization be connected after all, and can
R1 be pushed further right now? Answers, in order:

1. **Root cause (Phases H/I) is not fixable from inside this
   framework — structural, not a stopping point more effort removes.**
   Cl(10)×E8 as used here is rigid representation theory: fixed
   algebras, fixed branching rules, no moduli, no compact geometry, no
   flux. String-compactification data only exists inside an actual
   string construction — a specific Calabi–Yau or orbifold with chosen
   flux. Supplying it means building or importing an entire second
   theory, then checking whether one particular choice reproduces the
   SM. That choice would itself be a free input, not a derivation —
   exactly the reverse-engineering Rule 2 forbids. Marked "skip," not
   "TODO": there is no version of "try harder" that stays inside this
   project.
2. **Entanglement-minimization still doesn't connect, on its own
   terms.** Forcing a connection would mean deriving sin²θ_W from
   Cl(10)×E8, never attempted here before and not completed in this
   pass — flagged below as a genuinely new, untested, bounded lead,
   not claimed as done.
3. **R1 got real, new work: `phase_j_r1_dimension_check.py`.**
   Checked whether the CCvS spectral Pati-Salam Hilbert space (16
   states per generation, cited from JHEP 11 (2015) 011) matches what
   Cl(10)×E8 already derives. Result: yes, on representation content —
   the standard SO(10)→Pati-Salam branching 16=(4,2,1)+(4̄,1,2)
   reproduces the 16-dimensional generation, and Pati-Salam's SU(4)
   3-color-plus-1-lepton split is the same split already present in
   Cl(10)'s own color-occupation number Nc (Phase A1), nothing new
   grafted on. A genuine, previously-untested positive structural
   match — the first one found for R1.

   **Not yet checked, honestly scoped rather than skipped:**
   - Whether Cl(10)×E8's SU(2)_L-only construction (no SU(2)_R was
     ever built here) is compatible with CCvS's left algebra M2(H),
     which carries both SU(2)_L and SU(2)_R. Dimension-counting can't
     answer this; needs the actual unitary-group structure worked
     through.
   - CCvS's scalar/Higgs content and Yukawa structure (their Table 1)
     — the one place an existing, peer-reviewed dynamical framework
     could supply what Phases B/C found missing. Real, substantial
     work; not attempted yet.
   - **New candidate lead**: does Cl(10)'s own generator normalization
     (SU(3)_c, SU(2)_L, U(1)_Y all built from the same Witt-pair
     algebra) reproduce the standard GUT tree-level sin²θ_W = 3/8
     automatically, the way any properly-normalized SO(10)/SU(5)
     embedding does? If yes, that's a real derived number (RG running
     to the EW scale is a fixed, standard calculation, not a new free
     parameter) — and it's the exact input entanglement-minimization
     is missing. NOT tested. The most concrete next step in this
     roadmap.

## Phase L addendum (2026-07-27): R1's SU(2)_R question — resolved

Directly checked, using the real CCvS algebra confirmed from the
primary source (arXiv:1304.8050: 𝒜 = ℍ_R⊕ℍ_L⊕M₄(ℂ), i.e. TWO separate
quaternion algebras, each with unitary group SU(2) — genuinely two
independent SU(2)'s, not one bigger group as an earlier, imprecise
source summary had suggested).

Computed directly with Cl(10)'s own gamma matrices (Phase A1's Witt
pair {3,4}, the same 4-real-dimensional subspace already used to build
SU(2)_L): the standard SO(4)=SU(2)×SU(2) self-dual/anti-self-dual
decomposition (textbook Lie theory, not new physics) was constructed
explicitly and checked. Result: **confirmed**. T⁽⁺⁾ and T⁽⁻⁾ each
independently satisfy the su(2) commutation relations (opposite
orientations, as expected for self-dual vs anti-self-dual generators),
and they commute with each other — a genuine, mutually-commuting
SU(2)×SU(2), built from Cl(10)'s own algebra with no new assumptions
and no import from outside. This resolves the SU(2)_R compatibility
question flagged in Phase J: Cl(10) is group-theoretically compatible
with CCvS's ℍ_R⊕ℍ_L requirement.

**Honest scope limit**: this confirms the *group theory* is
compatible. It does NOT yet show that Phase A1's specific fermion
charge assignment (built from the simpler U(1)×SU(2) embedding)
matches CCvS's exact (2,1,4)+(1,2,4) content under this new SO(4)
basis — the two constructions are different bases of the same Cl(10)
algebra, and reconciling them (checking Phase A1's derived SM charges
come out the same way under T⁽⁺⁾/T⁽⁻⁾) is the concrete next step, not
yet done. See `phase_l_su2r_check.py`.

## Phase M (2026-07-27): Phase L corrected, not just extended

Direct follow-up, exactly the reconciliation Phase L left open: do
Phase L's T⁽⁺⁾/T⁽⁻⁾ actually work as independent physical symmetries
of Phase A1's real fermion representation, not just as abstract
algebra? Checked directly:

- **T⁽⁺⁾ does not fully commute with total fermion number N_tot** — it
  mixes states across different N_tot sectors, so it cannot act as an
  internal symmetry of one fixed-chirality 16-plet at all.
- **T⁽⁻⁾ does commute with N_tot**, but its Casimir operator
  (T_x²+T_y²+T_z²) is **identical, eigenvalue-for-eigenvalue**, to
  Phase A1's original SU(2)_L Casimir. It is not a new, independent
  SU(2)_R — it is the same physical SU(2)_L symmetry in a rotated
  generator basis.

**Corrected status**: Cl(10)×E8, in this specific fermionic
representation, does not contain a genuine second, independent SU(2)
next to SU(2)_L. Phase L's SO(4)=SU(2)×SU(2) decomposition is real
algebra — that computation stands — but it does not survive contact
with the actual 16-plet representation as two *distinguishable*
physical symmetries. **Phase J's SU(2)_R compatibility question, which
Phase L reported as resolved, is reopened as unresolved.** This
specific route (self-dual/anti-self-dual split of Cl(10)'s own pair
{3,4}) is now a checked, closed dead end for it — not "we didn't
find it," but "we found it, and it collapses onto what was already
there." See `phase_m_reconciliation.py`.

**Updated honest summary: two of three requests (compactification
data, entanglement connection) have hard structural answers — not
"not yet," but "not from here." R1 gained one confirmed structural
match and two precisely-scoped open sub-problems, one of which
(sin²θ_W normalization) is new, cheap to test, and could reopen the
entanglement-minimization question if it succeeds.**

## Phase K addendum (2026-07-27): the sin²θ_W lead, closed

Tested directly with standard, textbook 1-loop RG running (SM beta
coefficients, not new physics): GUT-scale sin²θ_W=3/8 does not survive
down to M_Z with only SM matter in between. Predicted 0.208 vs
measured 0.2312 — the well-known ~10% non-SUSY-unification mismatch
that has motivated SUSY GUTs for decades. This closes the
entanglement-minimization reconnection attempt on both ends: the value
doesn't survive running, and (Phase I) even the un-run value barely
moved the Cabibbo-angle prediction anyway. See
`phase_k_sin2thetaw_gut_check.py` and `solution.md` for the full
closing synthesis.

## Phase U addendum (2026-07-28): the hypothesis-backlog leverage ranking, sharpened

A live literature re-check (Phase U, see `phase_u_literature_2026.py`)
found that PHASE_R_HYPOTHESIS_BACKLOG.md's item 6 (Cl(8) S3 family
symmetry) has a direct Cl(10) sequel — N. Gresnigt, arXiv:2601.07857 and
arXiv:2604.24795 (2026) — using the SAME base algebra as this project's own
Phase A1, via an S3-on-Witt-ideals mechanism independent of this project's
E8-branching route. This replaces "read a related-but-different-algebra
paper and guess whether it transfers" with a concrete, tool-available next
step: implement that construction directly against Phase A1's own Cl(10)
code and check by computation whether it reproduces Phase A1's charge
assignment. This is now the highest-leverage unfinished item this project
has identified for itself — sharper than, and superseding, Phase R's item-43
ranking (which pointed at the same paper family but the Cl(8) version).
Not attempted here; Phase U is a literature check, not a derivation.
