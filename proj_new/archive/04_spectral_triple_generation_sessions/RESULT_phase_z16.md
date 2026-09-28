# Phase Z16: sextet flavon → forced SO(3) residual → same exclusion as Z14, reached without alignment tuning

**Status: closed, L1, negative — but a structurally different negative
from Z6–Z15, not a repeat.** Answers the question Z15's own writeup
posed ("a further attempt needs a stated reason it would net
differently, not just the next representation in line").

## The stated reason (not "next representation in line")

Every flavon mechanism tried before this phase (Theorem B-3: fundamental
`3`; Z15: adjoint `8`) required an extra step to pick out a *specific*
residual-symmetry direction: B-3's single triplet leaves the VEV
direction on the sphere a genuine flat modulus (no discriminating
power), and Z15's adjoint needs its own potential's couplings to select
*which* Cartan direction the VEV points along, a cost Z15 counted
explicitly against the mechanism's savings.

A flavon in the **sextet** (`6 = Sym²(3)` of `SU(3)_f`, i.e. a complex
symmetric 3×3 matrix `φ_ij`) is different in kind: its renormalizable
potential is a function of exactly two invariants at quartic order,
`I1 = tr(φ†φ)` and `I2 = tr((φ†φ)²)` — same *count* as the adjoint case,
but here convexity plus the permutation symmetry of the eigenvalues
`x_k` of `φ†φ` forces the **global minimum of every stable choice of
couplings** (any `λ2>0`, `λ1+λ2/3>0` — an open, generic region, not a
tuned point) to the fully democratic point `x1=x2=x3`. No additional
coupling has to be tuned to select a direction; the direction is forced
by symmetry alone, for the entire stable parameter region at once. That
is the structurally different reason this phase tests, not a re-run of
B-3/Z15 with a new Dynkin label.

## What was computed (not asserted)

1. **Potential minimization (hand-derived, checked by direct
   substitution):** with `x_k = |φ†φ|` eigenvalues, `S = Σx_k`,
   `V(x) = -m²S + λ1 S² + λ2 Σx_k²`. By QM/Cauchy–Schwarz,
   `Σx_k² ≥ S²/3` at fixed `S`, equality iff `x1=x2=x3`. For `λ2>0` this
   makes every fixed-`S` slice minimized exactly at the democratic
   point; the remaining 1-D minimization over `S` is an ordinary
   parabola. Global minimum: `x1=x2=x3=v²` for the entire
   `λ2>0, λ1+λ2/3>0` region.

2. **Stabilizer of the democratic vacuum (hand-derived + two independent
   numerical checks):** at `x1=x2=x3`, Takagi form `D=v·I`. Solving
   `U D U^T = D` for `U∈SU(3)` gives `U U^T = I`, i.e. `U` unitary *and*
   `U=U^T`-compatible-real, i.e. `U∈SO(3)` (real orthogonal, det 1).
   Confirmed two ways: (a) direct linearization at `U=I` — the
   stabilizer's Lie algebra condition `HD+DH*=0` reduces, for `D=v·I`,
   to `H+H*=0`, i.e. `H` purely built from the 3 *imaginary* Gell-Mann
   generators (`λ2,λ5,λ7`, `su3f` indices `[1,4,6]` in this repo's
   `build_su3f_generators()` convention) — exactly `so(3)`; (b) direct
   numerical check: `exp(iH)` for `H` in that span leaves `D=I`
   invariant to `3e-16`, while a generic non-`SO(3)` direction
   (`su3f[0]`) does not (`‖UDU^T-D‖≈0.42`).

3. **Closure check:** `[g0,g1] = (i/2)·g2` for `g={su3f[1],su3f[4],
   su3f[6]}`, confirming these 3 generators close into `su(2)≅so(3)`
   on their own (`phase_z16_sextet_so3.py`, `closure check` line,
   residual `0.0`).

4. **Order-one condition, SO(3)-only** (`phase_z16_sextet_so3.py`, same
   method as Z15's `run_channel_cartan_only`, restricted to the 3
   `SO(3)` generators instead of the 2 Cartan ones, run on Phase X's
   actual `M10`/`M120`/`M126` CG tensors via the Z6–Z13 chirality-
   flipping bridge):

   | channel | full 8-gen `su(3)_F` (Z13) | SO(3)-only (this phase) |
   |---|---|---|
   | M10  (symmetric)     | 1 complex | **1 complex** |
   | M120 (antisymmetric) | 0 complex | **0 complex** |
   | M126 (symmetric)     | 1 complex | **1 complex** |

   The null-space vectors for M10/M126 are, to machine precision,
   exactly `c·I3` (`Re = diag(-0.577,-0.577,-0.577)`, i.e.
   `1/√3·I3` up to sign/phase) — matching a direct Schur's-lemma
   argument: `SO(3)`'s defining representation stays irreducible over
   `C`, so any matrix commuting with the full `so(3)` action is forced
   to `c·I3` for complex `c`, and no matrix that is also required
   antisymmetric (the `120` channel) can be nonzero. The numeric
   null-space and the group-theory argument agree exactly — Rule 4's
   two-independent-methods bar.

## The result, stated plainly

**`SO(3)` alone (3 of `su(3)_f`'s 8 generators) already forces the
identical constraint the full 8-generator `su(3)_F` forces in Z13.**
Fewer generators, same collapse: `Y_gen ∝ c·I3` for both symmetric
channels, `Y_gen=0` for the antisymmetric one.

This is **not an escape from Z14's exclusion — it is the same
exclusion, reached by a smaller, dynamically-forced (not
hand-selected) unbroken subgroup.** Z14 found that unbroken `SU(3)_f`
predicts degenerate-or-zero fermion masses, excluded by observation.
This phase finds that a *generic* sextet-flavon vacuum — forced by
stability alone, not by tuning which direction the VEV points — lands
on a residual symmetry (`SO(3)`) that is already large enough, on its
own, to impose that same excluded prediction. Unlike Z15's adjoint
case, there is no extra "which direction" cost to net against the
saving, because there is no direction to choose: the sextet's
democratic vacuum is the *only* stable minimum. Netting is trivial
here specifically because the mechanism has no free knob left to net
against — and the answer is still excluded.

## Rule 9 check

Would this mechanism have "explained" a different answer just as well?
No: a generic (non-democratic) residual, e.g. the Cartan `U(1)×U(1)`
Z15 tested, gives a genuinely different answer (3 complex parameters,
not 1) — so the specific prediction here (`c·I3`, fully degenerate) is
a real, falsifiable consequence of *this* mechanism, not a template
that would fit any outcome. It is simply the wrong falsifiable
consequence (excluded by data), which is exactly the kind of negative
this project's Rule 8 records with full weight.

## What this adds to the project's total picture

`docs/MECHANISM_FAILURE_MAP.md`'s closing line said the two standard
non-minimal flavon choices (fundamental, adjoint) both net to zero, and
a further attempt needs a stated reason to expect a different outcome.
This phase supplies that reason (forced vs. chosen residual symmetry)
and finds it does *not* produce a different outcome — if anything, it
shows Z14's exclusion is more robust than it looked: it does not
require the full `SU(3)_f` to survive unbroken, only a 3-generator
subgroup that a very ordinary (renormalizable, generic-coupling)
extension produces on its own. That is new information, even though
the bottom line (0/19 derived) does not move.

## What remains open

- This closes the "generic single-sextet, renormalizable potential"
  case only. A potential including the dimension-6 operator
  `tr((φ†φ)³)` (non-renormalizable, needs its own UV justification and
  adds a parameter) could in principle lift the `x1=x2=x3` degeneracy —
  not attempted here; doing so honestly requires stating and netting
  that operator's own coefficient per Rule 2/6, the same standard every
  other row in the failure map is held to.
- Multi-flavon configurations (e.g. sextet + fundamental, or two
  fundamentals) were considered but not computed in this session: a
  quick hand check (two generic fundamentals span a 2-dim subspace and
  generically break `SU(3)_f` to the *trivial* group, i.e. zero
  unbroken generators) shows that route gives *less* order-one
  constraint than either B-3 or this phase, not more — recorded here so
  a future session doesn't re-spend time on it without a reason it
  would behave differently.
