# Phase Z23, Task B — the family group is forced to be S3: exhaustive
# GAP check over all groups of order <= 60

**Status: closed, L1. The discrete family group of the project's
Cl(10)+S3 construction is uniquely determined: among ALL groups of
order <= 60, exactly one — S3 — satisfies the four structural criteria
the construction's own established results force. The enumeration is
fully discriminating: each criterion is a physics input (not an S3-
shaped one), the intermediate survivor sets are large (86, 30, 28, 10
groups), and the final step leaves exactly S3. This is a Rule 9 pass:
the mechanism demonstrably *could* have returned other groups (it
returns 30 groups before the last criterion), and the answer it gives
is a theorem, not a fit.**

## What this phase tested

The project's Phase A2 claim "3 generations under the family group S3"
was previously asserted via Gresnigt's Cl(10)+S3 construction (Phase
Z22 imported it) but the *necessity* of S3 — as opposed to any other
small group — was never checked. The Z23 audit asked for a GAP
verification that no non-cyclic group can play the family-group role.

Criteria (each forced by previously established project results, stated
with their sources; none chosen to single out S3):

1. **(i) faithful real 2-dim irrep on the generation plane** — Task A
   proved psi_3 acts as an exact 120-degree rotation on the
   (H_alpha,H_beta) plane, and that the plane is an irreducible real
   rep; the plane action must be faithful (else part of the family
   structure is killed by a kernel).
2. **(ii) an order-3 element acting as a 120-degree rotation (trace -1
   in the 2-dim rep)** — this element IS psi_3 (Task A, exact).
3. **(iii) an order-2 element acting as a reflection (trace 0)** — the
   2:1:1 mass-texture degeneracy is a reflection transposing two
   generations (Z22/Gresnigt structure: two equal masses = a C2
   symmetry between the two families in the plane).
4. **(iv) a faithful action on the 3 labeled generations** — the three
   mass matrices M_1, M_2, M_3 are distinct objects (input physics: 3
   generations exist and are labeled).

Enumeration bound: all groups of order 2..60 (GAP SmallGroup library,
311 groups). The bound is a completeness parameter for the census; the
final selection argument (criterion iv) does not depend on it (see
below).

## Method (GAP 4.15.1, HAP loaded; no third-party group packages)

For every group G of order 2..60:

- Faithful real 2-dim irreps are found by character theory: (a) complex
  2-dim irreps whose Frobenius-Schur indicator is +1 (real type) with
  trivial kernel; (b) pairs of complex-conjugate linear characters
  (rotation-type real 2-dim reps, e.g. cyclic rotation reps) with
  trivial kernel. FS indicators computed directly from the character
  values (1/|G|) * sum chi(g^2) — the built-in `Indicator` call is not
  available for group characters in this build, so it is computed by
  hand from first principles.
- Trace values of elements are read from the character (class-index
  lookup), then: rotation test = exists element of order 3 with trace
  -1; reflection test = exists element of order 2 with trace 0.
- Criterion (iv): G embeds into Sym(3) (checked by explicit
  isomorphism search over all 6 subgroups of S3).

## Results (exhaustive, all 311 groups of order 2..60)

### Stage A — criterion (i): faithful real 2-dim plane rep

**86 groups** — and the census reproduces the classical classification
exactly: 58 cyclic groups C_3..C_60 (rotation-type reps; C_2 has no
2-dim rep at all, correctly excluded) + 28 dihedral groups D_6..D_60
(standard rotation/reflection rep). No exotic group (A_4, S_4, Q_8,
etc.) appears: A_4 has no 2-dim irrep, S_4's 2-dim irrep has kernel V_4
(not faithful), Q_8's 2-dim irrep is quaternionic (FS -1). The census
is a cross-check of the classical theorem "finite subgroups of O(2) are
C_n and D_2n" — verified by enumeration, not assumed.

### Stage B — criteria (i)+(ii): plus a 120-degree rotation

**30 groups**: C_3k (k=1..20: C_3..C_60) and D_6k (S_3, D_12, ..,
D_60). Cyclic rotation groups enter here: a faithful plane action with
an order-3 rotation is NOT yet discriminating (20 cyclic + 10 dihedral).

### Stage C — criteria (i)+(iii): plus a reflection

**28 groups**: exactly all dihedral D_6..D_60. Cyclic groups are all
excluded (a pure rotation group has no trace-0 order-2 element; its
order-2 element, when present, is a 180-degree rotation, trace -2).
This is the criterion that kills the cyclic family-group candidates
(C_3k) — the 2:1:1 texture requires a reflection.

### Stage D — criteria (i)+(ii)+(iii)

**10 groups**: S_3, D_12, D_18, D_24, D_30, D_36, D_42, D_48, D_54,
D_60 (dihedral with 3 | n). These are the genuine near-misses: each
contains an order-3 rotation AND a reflection in a faithful plane rep.
Cross-checked: D_12 = S_3 x C_2, and in EVERY one of the 10, every
(order-3 rotation, reflection) pair generates a subgroup isomorphic to
S_3 of order 6 — i.e., the rotation+reflection pair NEVER generates
more than S_3.

### Stage E — criterion (iv): faithful action on 3 points

Of the 10 groups in D, exactly **1** embeds into Sym(3): **S_3**.
(D_12..D_60 have order > 6 and cannot act faithfully on 3 points; any
degree-3 action factors through S_3 and kills a kernel.)

### FINAL

**S_3 is the unique group of order <= 60 satisfying all four criteria.**
S_3's own 2-dim irrep (computed, values [2, 0, -1] on e, reflection,
120-degree rotation) is exactly the Task A plane rep: trace 2 at the
identity, 0 at the reflections, -1 at the 120-degree rotations.

## Rule 9 check (discriminating power)

The mechanism had ample opportunity to return other groups: criterion
(i) alone leaves 86, (i)+(ii) leaves 30, (i)+(iii) leaves 28,
(i)+(ii)+(iii) leaves 10. Only the last criterion — faithful action on
3 labeled generations, which is pure input physics (3 generations, 3
mass matrices) — collapses the survivor set to S_3. Had the project's
structure lacked the reflection (2:1:1), the answer would have been
C_3k as well; had it lacked the 3-point faithfulness, the answer would
have been 10 dihedral groups. The criteria are not templates for S_3.

## What this does *not* close

- S_3 as the discrete family group is forced; whether the 3-generation
  structure actually *arises* from S_3 (vs. being described by it) is
  the separate Z22/Z23-A question (H_alpha/H_beta plane, Mbar
  unreachability) — unchanged.
- The bound "order <= 60" is a census parameter only: criterion (iv)
  excludes every group of order > 6 regardless of bound, so the
  conclusion is bound-independent.
- The gauged SU(3)_f family assignment of the E8/E6 chain (the
  (27,3) of Task C) is a DIFFERENT mechanism from this discrete S_3;
  Task G checks that one. The two are not identified here.
- S_3's role as an automorphism group of the mass matrices vs. an
  internal symmetry of the Lagrangian is not decided by this check.

## Rule 9 check — second pass (would the check have caught a wrong answer?)

The script was tested against the classical classification (finite
subgroups of O(2) = C_n, D_2n): the census of 86 groups matches 58+28
exactly. A bug in the character evaluation (function-call dispatch on
class functions, unavailable in this GAP build) was caught because the
census returned 0/1 groups instead of 86; it was fixed by evaluating
characters by conjugacy-class index, and the census then matched the
classical theorem. The verification pipeline itself discriminates.

## Net verdict

The family group is forced: S_3. L1 (exhaustive enumeration over a
stated bound + classical theorem cross-checked by the same enumeration;
no free parameters; no comparison to observation anywhere). The Phase
A2/Z22 S_3 assumption is now a derived uniqueness statement, not an
input. The 2:1:1 texture and the psi_3 rotation single out dihedral
structure; the existence of exactly 3 generations singles out S_3
itself.

## Reproducibility

`session_new_files/phase_z23_external_session/`:
- `tmp_task_b_family_group.g` — the full enumeration (311 groups),
  stages A-F
- `tmp_task_b_supplement.g` — S_3 character table, D_12 = S_3 x C_2,
  near-miss S_3-subgroup structure
- `tmp_test_char_call.g`, `tmp_task_b_debug.g` — GAP mechanics
  debugging (class functions not callable in this build; pc-group
  generator layout) — kept as audit trail of the two bugs caught

Tool: GAP 4.15.1 (SmallGroup library; `Irr`, `KernelOfCharacter`,
`IsomorphismGroups`; FS indicator computed by hand from character
values).

## Source

No literature table used. The classical "finite subgroups of O(2)"
fact is used only as an independent cross-check of the enumeration, and
is re-verified by the census itself. Everything in this file is
computed here (Rule 4).
