# RESULT — The Missing 126_H Vertex Terms in β(Y10), β(Y120):
# Not a Missing Clebsch Tensor. Exactly Zero, by a Selection Rule —
# and a Correction to the Previous Session's λ(126,126)=6.

**Status: L1, complete.** This resolves the item marked "(c) formally
unavailable" in `RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md` Layer 2.3. It
also **retracts** that same document's λ(126,126)=6 entry, which is
shown below to be a basis artifact, not an SO(10) invariant. Filed as
its own result per Rule 4/8 ("Phase M corrects Phase L"), not a silent
edit.

Rules at risk this session: Rule 1 (the retracted λ=6 is *exactly* the
failure mode Rule 1 warns about — a clean-looking exact number with no
forcing mechanism); Rule 9 (checked explicitly below — the argument that
zeroes these terms would *not* have zeroed a charge-neutral term, so it
has discriminating power, it isn't a template that kills everything).

============================================================
## 0. What was asked, and why the premise needed checking first
============================================================

The task assumed a nonzero trilinear CG tensor in `10⊗120⊗126` (or
similar) must exist and just needs constructing. Before building
anything, I checked whether the Machacek–Vaughn vertex term
`2 Y^b Y^{a†} Y^b` can ever structurally produce such an object at all.

**It can't.** The term has one summed index (`b`), appearing twice, with
a single external label `a` that never multiplies against a second copy
of a different representation. There is no term in the MV formula of
the schematic form `Y_10 Y_120 Y_126` (three *different* reps
contracted together) — only `Y^b (Y^a)^† Y^b`, i.e. `R_b` paired with
itself, sandwiching a fixed external matrix. So no invariant in
`10⊗120⊗126` is ever needed by this piece of the formula, for *any*
external/internal combination. What's actually needed is an answer to
a narrower question: does `Σ_{b∈126} M_b (·) M_b`, applied to
`X = M_a^†` for `a ∈ {10, 120, 126}`, reduce to a multiple of `M_a`?
That's the question Layer 2.3 of the earlier document tried to answer
and got stuck on for `a=10,120` — and, it turns out, should have also
gotten stuck on for `a=126`, but didn't, for a specific reason found
below.

============================================================
## 1. The clean argument: a U(1) selection rule (L1, no numerics needed)
============================================================

126_H is a genuinely complex field: `Φ_k`, `k=1..126`, with
`Φ ≠ Φ*` as an SO(10) statement (126 ≇ 126̄, already established). The
Yukawa Lagrangian piece is `L ⊃ −(1/2) Y_126 ψψ Φ + h.c.`. This term,
and hence the whole theory restricted to this coupling, is invariant
under the **rephasing** `Φ → e^{iα}Φ`, `Y_126 → e^{−iα}Y_126`, with
every other field (10_H, 120_H, fermions) uncharged. Treat `Y_126` as a
spurion carrying charge `+1` under this U(1), `Y_126^†` charge `−1`,
everything else charge `0`.

`β(Y_a)` is the coefficient of a term that must itself carry the same
charge as `Y_a`: charge `0` for `a∈{10,120}` (real fields, no phase
freedom), charge `+1` for `a=126`. Every operator appearing in `β(Y_a)`
must therefore be built from equal net powers matching that charge.

Check the vertex term `2 Y^b (Y^a)^† Y^b` for `b` ranging over 126's
components: it uses `Y_126` **twice** and `Y_126^†` **zero** times, so
it carries charge `+2` regardless of what `a` is. For `a=10,120` (need
charge 0) this is forbidden outright. For `a=126` (need charge `+1`) it
is *also* forbidden — `+2 ≠ +1`. Compare with the terms that **are**
present and are fine: `Y2(F)` (`ΣY^{b†}Y^b`, charge 0 always) and the
self-energy/trace terms built from it, and `Y_126 Y_126^† Y_126`
(charge `+1−1+1=+1`, correctly charge-neutral relative to `a=126`) —
these survive the same selection rule that kills the vertex term.

**Conclusion (L1): the Y_126-internal-loop contribution to the vertex
term is exactly zero in β(Y_10), β(Y_120), *and* β(Y_126).** Not
"unavailable" — forced to vanish, with the forcing mechanism stated
(Rule 1 satisfied), and the mechanism would *not* have zeroed a
charge-matched term (Rule 9 satisfied: e.g. it correctly leaves
`Y_126Y_126^†Y_126` alone).

============================================================
## 2. Independent cross-check: direct Lagrangian reduction (L1)
============================================================

Same conclusion, derived a second, independent way, with no group
theory at all — by literally decomposing the complex field into MV's
real-scalar language and re-summing.

Write `Φ_i = (φ^1_i + iφ^2_i)/√2`. Matching
`L ⊃ −(1/2)Y_126,i ψψΦ_i + h.c.` to MV's real form
`L = −(1/2)Σ_a Y^a ψψφ_a + h.c.` fixes, uniquely:
```
Y^{(1)}_i = Y_126,i / √2         Y^{(2)}_i = i · Y_126,i / √2
```
(Cross-check: `Σ_i[(Y^1_i)^†Y^1_i + (Y^2_i)^†Y^2_i] = Σ_i Y_126,i^†Y_126,i`
— reproduces the expected `Y2(F)` contribution exactly, confirming the
parametrization is right.)

Now evaluate the vertex sum over 126's real components for **any**
fixed external matrix `Y_ext`:
```
Σ_{i,s=1,2} Y^{(s)}_i  Y_ext^†  Y^{(s)}_i
 = Σ_i [ (Y_i/√2) Y_ext^† (Y_i/√2)  +  (iY_i/√2) Y_ext^† (iY_i/√2) ]
 = Σ_i (1/2)[ Y_i Y_ext^† Y_i  −  Y_i Y_ext^† Y_i ]
 = 0   exactly, term by term in i.
```
The `i²=−1` from the second (imaginary) real component exactly cancels
the first. This holds for *any* `Y_ext` — i.e. regardless of whether
the external leg `a` is 10, 120, or 126 itself. Same answer as Section
1, by completely different reasoning. This is the standard
"holomorphic" non-renormalization structure familiar from SUSY-type
Yukawa RGEs (a coupling from a genuinely complex/holomorphic vertex
never appears un-conjugated twice in a physical beta function).

============================================================
## 3. Why the earlier session got λ(126,126)=6: a basis artifact
============================================================

This matters enough to show explicitly, since it's a real Rule 1
failure worth recording plainly, not glossing over (Rule 5).

`Σ_{k∈126} M_k (·) M_k` is SO(10)-invariant **only if** the bilinear
pairing `tr(M_k M_l)` (undaggered — a genuine symmetric bilinear form
on the representation, not the Hermitian `tr(M_k^†M_l)` pairing) is
itself SO(10)-invariant. That requires 126 to admit an invariant
symmetric bilinear form, i.e. requires 126 to be self-dual (real or
pseudoreal) as a representation. It isn't — that's the whole point of
Layer 2.3's original finding, and it's correct. So `tr(M_kM_l)` for the
actual 126 CG tensors has **no reason to be diagonal**, and whether
`Σ M_kXM_k` looks like "a clean scalar times X" is purely an accident
of which basis was used for the 126 index — it is not a physical,
basis-independent quantity at all.

Built the 126 CG tensors two ways this session, both valid, related by
a unitary change of basis on the 126 label (verified: both give
`Σ_k M_k M_k^† = 126·I₁₆` exactly, i.e. both are equally good CG
tensors — `T(126)=126` *is* basis-independent, as it must be, since
`Σ M_k⊗M_k^*` is always invariant for any rep):

- **Greedy/Gram–Schmidt basis** (what the original script builds):
  `tr(M_kM_l)` came out **exactly diagonal**, `±16δ_kl`, to machine
  precision. In this basis, `Σ_kM_kXM_k` at `X=M_0^†` gives a
  spotlessly clean ratio, exactly `6.000000` on every nonzero
  component, std dev `~1e-14`. This is what the earlier session found
  and reported.
- **Orthonormal SVD basis** for the identical 126-dimensional subspace
  (an equally legitimate CG tensor set — same `T(126)=126`, same
  physics): `tr(M_kM_l)` is a **generic, non-diagonal, complex
  symmetric matrix** (off-diagonal entries of order 1–4, comparable to
  the diagonal). `Σ_kM_kXM_k / M_0` is **not** a constant — component
  values range wildly (std dev ≈ 10, no plateau at all).

Same representation, same physical CG tensor up to basis, two wildly
different "λ" values (one suspiciously clean, one garbage) — conclusive
proof `Σ_{k∈126}M_kXM_k` is not a well-defined SO(10) quantity, and
that the earlier `λ(126,126)=6` was the Rule-1 failure mode by name: a
clean number from a specific, non-canonical, arbitrary choice
(the greedy Gram–Schmidt selection of self-dual eigenvectors), with no
mechanism forcing it — it isn't there in a differently-valid basis for
the exact same object. **Retracted.**

The Section 1/2 selection-rule answer (exactly 0) is, by construction,
basis-independent — it was derived without ever picking a 126 basis at
all.

============================================================
## 4. Updated complete β(Y10), β(Y120), β(Y126)
============================================================

Replacing the three "(unavailable, R_b=126)" / "λ=6" placeholders with
the derived value **0** (L1, Sections 1–2), and correcting Layer 4's
own β(Y126) entry (its `+2·6 Y126 Y126†Y126` piece is retracted — that
term does not exist; only the already-present self-energy/trace terms
survive):

```
16π² β(Y_10)  = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_10}
              + 16 Y_10 tr(Y_10†Y_10)
              + 2[ −8 Y_10 Y10†Y10  +  48 Y_120 Y10†Y_120 ]
              − 3 g² {C₂(16), Y_10}

16π² β(Y_120) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_120}
              + 16 Y_120 tr(Y_120†Y_120)
              + 2[ 4 Y_10 Y120†Y_10  +  8 Y_120 Y120†Y_120 ]
              − 3 g² {C₂(16), Y_120}

16π² β(Y_126) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_126}
              + 16 Y_126 tr(Y_126†Y_126)
              − 3 g² {C₂(16), Y_126}
```

Note what happened to β(Y_126): the `2Y^bY^{a†}Y^b` vertex term
contributes **nothing at all** now, from any internal channel
(10, 120, or 126) — 10 and 120 vertex-loop terms into `a=126` were
never computed/claimed in the earlier document either (the table only
covered `R_a∈{10,120}` against all `R_b`, and `R_a=126` against
`R_b=126`); a full accounting would need `λ(10,126)` and `λ(120,126)`
too (`R_b∈{10,120}` real, `R_a=126}` external — those *are* legitimate
Schur-type computations, since `R_b` is real, and are not addressed by
this note). That is flagged here as a genuine remaining gap, distinct
in kind from the one just closed: it needs the same real-rep Schur
machinery already used for the `−8,4,48,8` table, just with a complex
external leg, not a new invariant-tensor construction.

============================================================
## 5. Answers to the requested output list
============================================================

- **Allowed tensor products:** none. The MV vertex term never forms a
  three-different-representation contraction; it only ever needs
  `R_b ⊗ R_b` (paired with itself) for whichever channel is internal.
  No `10⊗120⊗126`-type object is used anywhere in this beta-function
  term, for any external leg.
- **Invariant multiplicities:** `126⊗126` (undaggered pairing) contains
  **zero** singlets — 126 not self-dual — confirmed both representation-
  theoretically (Section 1) and by the direct numerical basis-dependence
  test (Section 3, decisive: the "invariant" changes under a change of
  basis, so it isn't one).
- **Explicit CG construction:** not applicable — there is nothing to
  construct; the correct statement is a proof of non-existence via a
  charge/selection-rule argument (Rule 8: a closed avenue, recorded with
  full weight), reinforced by an independent Lagrangian-level derivation.
- **Resulting λ coefficients:** `λ(126,10) = 0`, `λ(126,120) = 0`,
  `λ(126,126) = 0`, all exact, all L1. (`λ(126,126)=6` from the prior
  session is retracted.)
- **Updated β(Y10), β(Y120), β(Y126):** Section 4.

No fixed-point analysis performed, per the task instructions.
