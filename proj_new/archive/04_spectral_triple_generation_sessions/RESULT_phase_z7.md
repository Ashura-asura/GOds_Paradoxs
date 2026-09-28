# Phase Z7 — the order-one condition, run for the first time on a valid D_F (this session)

## Question

`RESULT_phase_z6.md` validated the doubled construction (`H_F`, `ε`,
`J₀`) against all three real Yukawa channels. The next step named
there: re-run the order-one condition
(`[[D_F,a],J₀bJ₀⁻¹]=0` for `a` a family-gauge `su(3)_f` generator)
using **actual** `M10`/`M120` blocks in this validated space, instead
of Z2's generic random matrices or Z4's axiom-violating projection —
the original question the whole Z-series exists to answer.

## Method

Direct extension of `support/z2_hilbert_space.py`'s existing
`H_F = C^32 (x) C^3` / `E_kl` / `order_one_commutator` machinery
(unmodified), with the Cl(10) factor replaced by Z6's validated
32-dim doubled space, and the real structure's internal factor
replaced by `P` (Z6's swap matrix) in place of `C_F`.

- `D32_1 = [[0, Y10],[Y10†, 0]]`, `Y10 = M10[0]` (real, symmetric —
  the component validated in Z6).
- `D32_2 = [[0, Y120],[Y120†, 0]]`, `Y120 =` the `(0,1,2)` triple of
  `M120` (real, antisymmetric — also validated in Z6).
- `D_F_two = D32_1 ⊗ E(0,1) + D32_2 ⊗ E(1,2)` (same generation-pair
  skeleton as Z3's Test A).
- **Test A** (Z3's own naming): `a = I_32 ⊗ T_fam_a`,
  `J₀bJ₀⁻¹` built from `beta=I_32`, `T_fam_b` — pure family-gauge
  action, internal (Cl(10)-factor) part trivial. Same Gell-Mann
  `su(3)_f` generators already in the repo (`build_su3f_generators`),
  unmodified.
- Computed the full 96×96 commutator, block-normed by generation
  pair (as in Z2–Z4), **and** additionally checked whether the
  resulting operator itself still respects the grading
  (`{ε₉₆, [[D_F,a],J₀bJ₀⁻¹]} = 0`) — a check none of Z2–Z4 performed,
  since none of them had a `D_F` for which that question was even
  well-posed before Z6.

## Result

```
Block-norm matrix of [[D_F,a],J0bJ0^-1]  (generation indices k,l = 0,1,2):
[[0.     0.5    0.6614]
 [0.5    0.433  0.5   ]
 [0.6124 0.5    0.     ]]

||{eps96, [[D_F,a],J0bJ0^-1]}||  = 0.0        (exact)
||[[D_F,a],J0bJ0^-1]|| overall   = 1.4142
```

Two things worth separating:

1. **The (0,0) and (2,2) diagonal blocks are exactly zero; the (1,1)
   block is not** (0.433). Turning on the pure family generator
   induces a genuine same-generation term where the two input blocks
   overlap (generation 1 appears in both `E(0,1)` and `E(1,2)`), but
   not where they don't. This is a different, more structured pattern
   than Z3's original random-matrix run (which had all three diagonal
   blocks nonzero) — some of that earlier effect really was an
   artifact of unphysical input, consistent with what Z4 already
   suspected, but now shown on genuinely valid input rather than
   inferred by comparison.
2. **The induced commutator is exactly grading-respecting**
   (`{ε,·}=0`, to machine precision). This is the first time in the
   whole Z-series that a nonzero cross-block effect can be said to
   land in a *physically legal* place at all — Z4 showed the earlier
   candidate's induced terms were mostly orthogonal to any valid
   Yukawa direction; here, by construction (every ingredient — `D_F`,
   `a`, `J₀bJ₀⁻¹` — was built to respect `ε`), the output is
   automatically a chirality-flipping, i.e. Yukawa-type, object. It
   cannot be dismissed as unphysical noise the way Z4's result could.

## Verdict — L1 for the numbers, L2 for the physical reading

**L1**: the block pattern and the exact grading-preservation of the
result are both directly computed, reproducible facts about this
specific `D_F`/`a`/`J₀b` choice.

**L2, not yet L1**: whether this means `su(3)_f` genuinely constrains
Phase X's 6-or-3 Yukawa parameter count is *not* settled by this
alone. What's shown is that the induced (1,1) block is a legitimate
candidate Yukawa-type term — not whether it is a *new* one (a
direction outside the span of `M10`/`M120`/`M126` already counted in
Phase X, which would be a real constraint) or whether it collapses
onto a direction already included in that count (which would mean no
new constraint at all, just a consistency check passing). That
decomposition has not been done here.

## Next step

Decompose the induced (1,1) block against the full `M10⊕M120⊕M126`
basis (256 real components total across the three channels, per
Phase X's own counting) to determine whether it lies
inside that span or outside it. Inside ⇒ no new constraint, order-one
condition is automatically satisfied by the existing freedom. Outside
⇒ a genuine, first-time-demonstrated reduction in the Yukawa parameter
count from `su(3)_f`, which would be the most significant result in
the entire Z-series and should be independently re-derived (Rule 4)
before being trusted. Also repeat Test A with the `M126` channel
included (only `M10`/`M120` used this session) and run Z3's Test B
(SM generator ⊗ family generator combined) on this validated `D_F`,
which has not yet been done.

## Addendum (same session) — the proposed check was vacuous, and a real bug was found instead

Ran the "decompose against the full basis" check above. Two honest
findings, neither the one that was expected:

**1. The check as proposed cannot work, for a dimension-counting
reason missed when it was written.** `10 + 120 + 126 = 256`, which is
exactly `dim_C(Mat_16(C)) = 16×16 = 256`. Directly verified the basis
built from all 256 CG-tensor components has rank 256 — it spans
**every** 16×16 complex matrix, not a proper subspace of "already
counted" directions. That means *any* 16×16 matrix, including pure
random noise unrelated to any physics here, decomposes against this
basis with zero residual. The near-zero residual actually obtained
(`1.8e-15` relative) is therefore uninformative — it would have come
out that way regardless of what the induced block was. **This
specific check cannot distinguish "new constraint" from "no
constraint"; it was mis-specified.** Recorded here rather than quietly
dropped, per Rule 4.

**2. Root-caused a real Hermiticity problem instead, inherited from
Z2/Z3, not introduced this session.** Checking `full_A` and its
inputs directly:

```
||D_F_two - D_F_two^dagger|| = 11.31   (NOT Hermitian)
||full_A - full_A^dagger||   = 2.00    (NOT Hermitian)
```

Traced to the construction itself:
`D_F_two = M1⊗E(0,1) + M2⊗E(1,2)` — the same skeleton Z2 and Z3 both
use — includes only `E(0,1)` and `E(1,2)`, never their Hermitian-
conjugate generation partners `E(1,0)`, `E(2,1)`. A genuine Dirac
operator must be Hermitian; this was never fixed anywhere upstream,
so **every order-one condition number reported in Z2, Z3, and this
file's Test A above was computed on a non-Hermitian stand-in**, not a
valid Dirac operator, even where the internal (Cl(10)-factor) content
was itself physical.

**Fixed and reran**, adding the missing conjugate partners
(`D_F_herm = M1⊗E(0,1) + M1†⊗E(1,0) + M2⊗E(1,2) + M2†⊗E(2,1)`):

```
||D_F_herm - D_F_herm^dagger||        = 0.0   (Hermitian, confirmed)
||full_A(herm) - full_A(herm)^dagger|| = 0.0   (Hermitian, confirmed)
||{eps96, full_A(herm)}||              = 0.0   (grading still holds)

Block-norm matrix (Hermitian D_F):
[[0.     0.7071 0.9014]
 [0.7071 0.6124 0.7071]
 [0.9014 0.7071 0.    ]]
```

**Verdict on the fix**: the qualitative pattern from the original
Test A survives — (0,0) and (2,2) diagonal blocks still exactly zero,
(1,1) still nonzero, off-diagonals still populated — with different
(larger) magnitudes from the added conjugate terms, and now on a
genuinely valid (Hermitian, grading-respecting) operator rather than
an inherited stand-in.

## Corrected next step

The "is it new or old" question needs a different method than tried
here — not basis-decomposition (shown above to be vacuous by
dimension count), but treating the Yukawa CG coefficients themselves
as unknowns and asking whether the order-one condition, evaluated on
the Hermitian `D_F_herm`, forces a **linear relation among them**
(a genuine reduction in the 6-or-3 count) as opposed to being
satisfied identically for arbitrary coefficients (no reduction). That
is a distinct, larger calculation — solving a linear system in the
Yukawa coefficients, not checking span membership — and should be
treated as its own phase (Z8), built on the now-corrected Hermitian
`D_F_herm`, not on Z2/Z3's original non-Hermitian skeleton.
