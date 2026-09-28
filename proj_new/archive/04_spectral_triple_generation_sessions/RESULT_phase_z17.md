# Phase Z17: fundamental+adjoint portal alignment — redundant with Z15, not an improvement

**Status: closed, L1, negative (clarifying, not new territory).** Tests
the one genuinely new idea in the "search for SU(3)_f-charged fields"
plan (2026-08-01 external plan) that wasn't already covered by
Theorem B-3 / Z15 / Z16: a **two-flavon portal**, fundamental `φ` +
adjoint `Φ`, coupled by the renormalizable term `κ·φ†Φφ` (no new
representation needed — both fields were already separately motivated
in this project).

## Construction

`Φ = diag(a,b,c)`, `a+b+c=0`, generic distinct (Z15's own hierarchical
adjoint vacuum). The portal term `φ†Φφ = Σ|φ_i|²·Φ_ii` is extremized, at
fixed `|φ|²`, by putting all of `φ` into a single eigendirection of `Φ`
— `φ = v·e_{i*}` for whichever index extremizes, set by the sign of `κ`
(a discrete choice, not a tuned continuous parameter).

**Residual stabilizer, verified numerically** (`phase_z17_fund_
adjoint_alignment.py` console check): the pair `(Φ, φ=v·e_0)` is
stabilized by exactly the 1-parameter family `diag(0,θ,−θ)` — a single
`U(1)`, confirmed by direct exponentiation (exact to machine precision
for arbitrary `θ`) and confirmed that no other `su3f` direction
stabilizes both simultaneously.

## Order-one condition result

| channel | full-8 (Z13) | `U(1)²` (Z15) | `SO(3)` (Z16) | single `U(1)` (this phase) |
|---|---|---|---|---|
| M10  | 1 complex | 3 complex | 1 complex | **3 complex** |
| M120 | 0 complex | (structural 0) | 0 complex | **0 complex** |
| M126 | 1 complex | 3 complex | 1 complex | **3 complex** |

**The single `U(1)` reproduces Z15's `U(1)²` result exactly, with only
one generator instead of two.** This is not a coincidence needing new
machinery to explain: the order-one condition kills a Yukawa entry
`Y_ij` whenever the unbroken charge assigns generations `i,j` different
values, so *any* single unbroken `U(1)_F` with pairwise-distinct
generation charges (here `(0,1,−1)`) already forces the fully diagonal
texture — the second Cartan direction in Z15's `U(1)²` was never doing
independent work.

## Rule 9 / netting verdict

This construction does **not** escape Z14's degenerate-mass exclusion
the way it might have hoped to (it isn't excluded the way Z16's `SO(3)`
was, since diagonal ≠ degenerate — this is a real, in-principle-viable
FN-type texture), but **it buys nothing Z15 didn't already have**, and
it costs *more*: on top of the adjoint's own ≥2 potential couplings
(already counted against Z15), this construction adds a new portal
coupling `κ` and a second flavon `φ`'s own mass/quartic terms, for an
identical output (3 diagonal complex parameters, same off-diagonal-CKM/
PMNS-regeneration problem Z15 already flagged). **Dominated by Z15,
not an improvement — a strictly more expensive route to the same
already-known answer.**

## What this adds

Not a new number, but a real clarification: Z15's `U(1)²` reduction was
never using its full 2-generator structure — a single generic `U(1)_F`
suffices. This narrows what any *future* attempt needs to beat: match
or exceed the diagonal-texture reduction using strictly fewer new
parameters than Z15's adjoint sector alone requires, not just find
another field that reaches the same diagonal answer by a longer route.

## On the rest of the 2026-08-01 external plan

Steps 1–3 of that plan (find an SU(3)_f-charged field, work out its
Yukawa interaction, build a minimal extension) describe, almost
exactly, what Theorem B-3 → Z15 → Z16 → this phase already did.
Step 1's suggestion to search "supersymmetric extensions or theories
with additional gauge groups" is explicitly out of this project's
scope per `docs/solution.md` (importing a different theory's field
content to supply missing dynamics is "a different project, not an
extension of this one"). SARAH/FeynArts (step 4) are Mathematica-based
tools not available in this environment; `yukawa_rge_system_assembled/`
is this project's actual substitute and remains available for anyone
who wants to push the RGE side further. Step 5 (Rule 9 test) is exactly
what this phase and Z14/Z16 already apply.
