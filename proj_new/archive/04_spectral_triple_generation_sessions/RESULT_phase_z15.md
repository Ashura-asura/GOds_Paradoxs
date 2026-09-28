# Phase Z15 — non-minimal (adjoint) flavon: does it actually derive
# anything? (this session)

## Question

Z14 left one door open: Theorem B-3's `ε=0` no-go only covers a
**single flavon in the fundamental `3`** of `SU(3)_f`. The standard
non-minimal alternative in flavor-model building is a flavon in the
**adjoint `8`** — its invariant ring has *two* independent Casimirs
(`tr(Φ²)`, `tr(Φ³)`), not one, so a generic potential in two
invariants generically *does* have a minimum away from `Φ=0`. Does
this actually evade B-3's no-go, and if so, does it derive anything —
or does it just relocate the freedom, per this project's own repeated
finding for every other flavor mechanism tried?

## Method

**Step 1 — what survives the correct low-energy symmetry.** An
adjoint VEV `Φ` is gauge-equivalent to a diagonal matrix, breaking
`SU(3)_f -> U(1)xU(1)` (its Cartan subalgebra — generators indices
`{2,7}` in `build_su3f_generators()`'s convention, confirmed diagonal
by direct check). Below the flavon scale, the 6 broken generators'
gauge bosons are massive and no longer impose an *exact* order-one
condition — only the 2 unbroken Cartan generators do, at leading
order. Reran Z9/Z10's method with the `su(3)_F` generator loop
restricted to the 2x2=4 Cartan pairs instead of the full 8x8=64.

**Step 2 — honest parameter accounting**, per `POST_AUDIT_TARGET.md`'s
repeated instruction: count every new free parameter this scenario
introduces (flavon potential couplings, residual freedom, whatever's
needed to restore realistic mixing) and net it against whatever Step 1
saves, rather than reporting Step 1 alone.

## Result — Step 1

```
channel   full-8 su(3)_F (real)   Cartan-only (real)   Cartan-only (complex)
M10       2                       6                     3
M120      0                       0                     0
M126      2                       6                     3
```

Sanity check passed first (full-8 case reproduces Z9/Z10 exactly).
Under Cartan-only symmetry, the surviving null space for `M10`/`M126`
is **exactly the 3 diagonal entries** (`Y_11, Y_22, Y_33`, each fully
complex) — every off-diagonal generator-space direction is killed.
`M120` stays forced to exactly zero (its off-diagonal entries all
carry nonzero net Cartan charge too, generically). This is precisely
the textbook Froggatt–Nielsen "diagonal at leading order" structure —
a real, qualitatively different, and non-trivial outcome from Theorem
B-3's fundamental-flavon case, where nothing broke at all.

## Result — Step 2 (the accounting that actually matters)

What this scenario costs, itemized, none of it derived from Cl(10)×E8:

1. **The adjoint flavon's own potential.** A renormalizable
   `SU(3)_f`-invariant potential for an octet has (up to field
   rescaling) at least 2 independent real couplings beyond the overall
   scale (a cubic-to-quartic coupling ratio, since the invariant ring
   has exactly 2 generators `tr(Φ²)`,`tr(Φ³)` for 3 eigenvalues
   constrained to sum to zero). These 2 numbers are exactly what fix
   *which* diagonal direction (which eigenvalue ratios) the vacuum
   picks — nothing in Cl(10)×E8 supplies them.
2. **The 3 surviving diagonal complex parameters per channel are
   exactly as free as before.** Going from 6 to 3 complex parameters
   per channel is real, but the 3 that remain are *not* fixed by
   anything in this construction — same status as the original 6, just
   fewer of them.
3. **Realistic CKM/PMNS mixing needs the off-diagonal entries back.**
   An exactly-diagonal Yukawa in a shared basis for up- and down-type
   quarks gives exactly CKM=I — the same failure mode Theorem B-1
   already recorded for minimal 248, and the same one Item 11's
   `diag(a,b,b)` texture was excluded for (~40σ against `θ13`). Getting
   nonzero mixing requires reintroducing the off-diagonal entries as
   FN-suppressed, higher-dimension operators from integrating out the
   massive broken-generator bosons — which needs (a) the overall
   flavon-VEV-to-cutoff ratio `ε` and (b) an undetermined O(1) Wilson
   coefficient per suppressed operator. Both are exactly the free,
   fitted quantities Phases D/E already identified and recorded as not
   derivable in this framework — this phase doesn't reopen that
   question, it just shows it's unavoidable here too, by a different
   route.

**Net: not a reduction.** The freedom doesn't disappear, it moves —
from "6 complex Yukawa entries" to "2 flavon-potential couplings + 3
still-free diagonal complex entries + ε + O(1) coefficients per
suppressed off-diagonal entry." Counted honestly, the second list is
at least as large as the first, generally larger once the mixing
sector is included.

## Verdict — L1 (the accounting), and a genuine addition to the
failure map, not a repeat of Theorem B-3

This is a different failure mode from Theorem B-3 (which found the
mechanism can't even turn on). Here the mechanism *does* turn on and
*does* produce the qualitatively right structure (diagonal-then-
suppressed-mixing) — and still nets to zero derived parameters, for
the same reason every other row in `MECHANISM_FAILURE_MAP.md` nets to
zero: the symmetry-breaking sector's own freedom is at least as large
as what the symmetry removes. This is worth recording as its own row,
distinct from B-3, precisely because it's a *closer* attempt that
still fails the same net test — which is more informative than another
mechanism that fails for an unrelated reason.

## Answer to the direct question this phase was asked to resolve

**No. No Standard Model free parameter has been derived by this
scenario, or by anything else attempted through Z15.** Status remains
0/19 (0/23 with neutrinos). This closes the "non-minimal flavon" door
Z14 left open — negatively, but on its own genuine, checked terms
rather than by assumption.

## Next step

None recommended within this specific line (`SU(3)_f`-breaking flavon
sectors, minimal or adjoint). Both realistic options this project's
own methodology would consider standard (fundamental triplet: Theorem
B-3; adjoint octet: this phase) have now been checked and both net to
zero. A further non-minimal attempt (e.g. two flavons, or a flavon in
a still larger representation) would need to be motivated by something
other than "try the next representation" to be worth the same
accounting exercise again — per Rule 9, the burden is on any new
candidate to show upfront why it would plausibly net differently, not
on this project to keep testing representations exhaustively.
