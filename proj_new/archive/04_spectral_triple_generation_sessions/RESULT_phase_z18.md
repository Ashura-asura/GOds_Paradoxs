# Phase Z18: decuplet flavon — a "clock" (Z3×Z3) stabilizer kills both
# Yukawa channels, generically, without needing to solve the potential

**Status: closed, L1 (the group-theory claim) conditional on an explicitly
flagged L3 vacuum-form assumption. Negative, but a genuinely new route to
the exclusion, not a repeat of Z14/Z16's mechanism.**

## What's new here

Every non-minimal flavon tested so far (Z15 adjoint-`8`, Z16 sextet-`6`,
Z17 fundamental+adjoint portal) landed on a vacuum with a **continuous**
residual stabilizer (`U(1)²`, `SO(3)`, `U(1)`), and getting there required
either solving a potential explicitly (Z16's Cauchy–Schwarz argument) or
accepting an unproven "generic hierarchical vacuum" ansatz (Z15). This
phase tests the **decuplet** (`10 = Sym³(3)`, dimension 10) — untested
representation — and finds a stabilizer of a structurally different kind:
a **finite** group, `Z3 × Z3` (order 9), that requires *no potential
minimization argument at all* to establish, because it follows from
`ω³ = 1` alone.

## Construction and what's actually proved (L1)

For `g = diag(ω^p, ω^q, ω^r) ∈ SU(3)_f` with `ω = e^{2πi/3}` and
`p+q+r ≡ 0 (mod 3)` — 9 elements, the standard "clock" subgroup — acting
on the decuplet sends each monomial `e_i³ → ω^{3p_i} e_i³ = e_i³`
*exactly*, for any `p_i`, since `ω³ = 1` trivially. Consequently **every**
vacuum of the "diagonal cubic" form `φ = a·e₁³ + b·e₂³ + c·e₃³`, for
*any* nonzero complex `a, b, c` (a 3-complex-parameter family, not a
single special point), is stabilized by the full `Z3×Z3` exactly —
verified directly (`phase_z18_decuplet_clock_stabilizer.py`, residual
`6×10⁻¹⁵`, machine precision, and provable in closed form).

Running the same invariance test Z14–Z17 used (`gᵀYg = Y` for every `g`
in the residual group) on this finite `Z3×Z3`, for **both** the
symmetric channel (`Sym²(3)`, dim 6 — the M10/M126 target) and the
antisymmetric channel (`Λ²(3)`, dim 3 — the M120 target):

| channel | dim before | invariant dim under Z3×Z3 |
|---|---|---|
| Sym²(3) (M10, M126) | 6 complex | **0** |
| Λ²(3) (M120) | 3 complex | **0** |

Both computed by direct linear-algebra null-space extraction (full rank,
6 and 3 respectively, singular values well clear of tolerance — see
script output). **The entire Yukawa freedom in both channels is forced
to exactly zero**, for the whole 3-parameter vacuum family, not just a
special point.

## What is NOT proved (flagged, per Rule 4/8 precedent — Z2 Task 4, Item 1 addendum)

This does **not** show the decuplet's actual renormalizable potential is
minimized at a diagonal-cubic point. Unlike the sextet (Z16), whose
potential has a single quartic invariant and a clean Cauchy–Schwarz
argument, the decuplet's invariant theory (ternary cubics) has **two**
independent classical invariants (the Aronhold `S` and `T` invariants),
so the general SU(3)_f-invariant quartic potential needs more than one
coupling and was **not constructed or minimized in this session** — this
is exactly the kind of unproven-vacuum-selection gap the project has
flagged before rather than glossed over (see Z15's own "generic
hierarchical vacuum" caveat for the closest precedent). It is possible
the true minimum is a generic point with **trivial** stabilizer instead
(diagonal-cubic vacua are a natural, motivated guess — every previous
flavon's forced/generic vacuum in this project has also been of
"diagonal in some basis" type — but a guess, not a proof).

## Rule 9 check

Would this mechanism have "explained" a different answer? **No point in
flavor space is selected at all** — the result (Y=0) is identical across
the entire 3-parameter `(a,b,c)` vacuum family, so it has zero
discriminating power over *which* diagonal-cubic vacuum occurs, and is
honestly reported as an exclusion, not a derivation. Passes Rule 9 as a
negative result in the same sense Z2's Task 5 did.

## Net verdict

**Status remains 0/19.** Not progress on the 6-or-3 target — a third,
structurally independent route (after Z14's unbroken-`su(3)_F` and Z16's
forced-`SO(3)`) to the same "degenerate-or-zero" exclusion family, this
time requiring no potential-solving to establish and covering the
*antisymmetric* channel as well (Z14/Z16 only directly addressed the
symmetric channels). This strengthens the pattern already stated in
`docs/MECHANISM_FAILURE_MAP.md`'s summary: **every tested residual
symmetry big enough to be "generic" or "forced" in some sense has so far
either fully collapsed the Yukawa freedom (Z14, Z16, this phase) or left
it at a cost that nets to zero (Z15, Z17).** The genuinely open gap this
phase leaves is the same one Priority 1 in `docs/POST_AUDIT_TARGET.md`
already names — the decuplet's actual vacuum requires real invariant-
theory tooling (Aronhold covariants) this environment doesn't have any
more than the NCG/Seeley-DeWitt tooling Priority 1 needs; it should not
be attempted by hand in a single session per the same reasoning already
on record there.

## Reproducibility

`session_new_files/phase_z18_decuplet_clock_stabilizer.py` — runs clean,
no external dependencies beyond numpy, both channel checks included.
