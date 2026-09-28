# Phase Z3 — Gauged SU(3)_f, order-one condition (session, 2026-07-28)

## Question

Phase Z2 (Task 5) assumed `a` is generation-trivial "because SU(3)_f is
not part of the gauge algebra," and on that assumption proved the
order-one condition can't relate different generation-pair blocks of
`D_F`. Z3 tests the one thing that assumption left unexamined: what if
`a` *does* carry a genuine SU(3)_f generator? Does the order-one
condition then see cross-generation structure?

## Method

`phase_z3_family_gauge_order_one.py`, built directly on Z2's own
objects (`cl10_gamma_J.py`, `z2_hilbert_space.py` — same Γ_F/J_F, no
reimplementation). `build_su3f_generators()` already existed in the
repo but had never been plugged into `a` for the order-one test.

Two configurations, both against the same fixed `D_F` (random `M1`,
`M2` seeded into the (0,1) and (1,2) generation blocks only, so any
leakage into other blocks is attributable to `a`/`JbJ⁻¹`, not to `D_F`
itself):

- **Test A** — pure family-gauge action: internal (Cl(10)) factor
  trivial (`alpha=beta=I_32`), only the SU(3)_f generator `T_fam_a` /
  `T_fam_b` acts on the generation index.
- **Test B** — internal SM generator ⊗ family generator combined
  (`alpha = Tx + 0.3·lam3`, `beta = Y − 0.2·Tz`).

`JbJ⁻¹` is built via the correct antiunitary conjugation
(`beta' = C_F β̄ C_F⁻¹`, generation factor conjugated, not transposed —
derivation given in the script's docstring), not assumed.

## Result (from the actual run)

```
charge-conjugation solve: residual=5.35e-15 unitary=True n_null=1

Test A block-norm matrix (rows/cols = generation index k,l):
[[3.7796 3.9055 4.0635]
 [3.7169 3.9223 3.8958]
 [3.5441 3.4751 3.7208]]

Test B block-norm matrix:
[[2.7985 2.8666 2.8513]
 [2.7231 2.6106 2.6188]
 [2.6698 2.4284 2.5349]]
```

Every one of the 9 generation-pair blocks is nonzero, in both tests —
including blocks like (0,0), (2,2), (0,2) that received no direct
contribution from `M1`/`M2`. This is the opposite of Z2's result, where
every off-(input)-block entry was exactly 0. **L1**: with a genuine
`su(3)_f` generator in `a`, the order-one condition does relate
different generation-pair blocks of `D_F`. Charge-conjugation solve
is clean (residual 5.35e-15, unitary, one-dimensional null space),
so this isn't an artifact of a bad `C_F`.

## What this does *not* yet show

1. **Not checked against Phase X's actual physical subspace.** Phase X
   pinned the surviving freedom per block at 1 complex dimension
   (within the 6-or-3 count). A nonzero block-norm here only says the
   *commutator* is nonzero — it doesn't yet say the constraint lands
   inside that 1-dim physical direction rather than, e.g., forcing
   something already-fixed-by-Phase-X to move, or constraining a
   direction orthogonal to the physical one. This is the immediate
   next computation (see below).
2. **Net parameter cost not computed.** Gauging SU(3)_f is not free:
   it predicts 8 new gauge bosons that aren't observed, which need a
   symmetry-breaking flavon sector to hide. This project's own Theorem
   B-3/NT1 already proved the *minimal* single-flavon SU(3)_f-breaking
   potential doesn't even break the symmetry (ε forced to 0) — the
   same failure pattern as Froggatt-Nielsen. A real breaking sector
   would need more field content, and its own parameter count has not
   been computed here.

## Verdict (Rule 9)

**Unresolved, not closed either way.** Z3 is the first mechanism in
this project's history to produce a genuine cross-generation
constraint from the order-one condition at all — a real change from
every prior attempt (FN, messenger matter, S3, spectral-action, Z1,
Z2), which all landed at either zero selection power or a proven
impossibility. But per Rule 9 (discriminating power net of new
parameters), the likely outcome — based on the messenger-matter
precedent (Phase F/G: rescues consistency for *any* charge triple,
zero selection power) and the already-proven failure of the minimal
SU(3)_f-breaking potential — is that a working breaking sector costs
at least as much freedom as Z3 removes. That has not been proven; it
is the honest expectation, not a computed result.

## Next steps (in priority order)

1. **Project onto Phase X's physical subspace.** Take the nonzero
   block-norm result and check whether the induced constraint actually
   intersects the 1 complex dimension per block that Phase X identified
   as physical, or whether it's orthogonal to it (in which case it
   constrains nothing observable). This is a direct, cheap follow-up
   with tooling already in the repo (`z2_hilbert_space.py`,
   `phase_x_hom_g_invariant_audit.py`) — no new construction needed.
2. **Compute the SU(3)_f-breaking sector's own parameter count.** Build
   the minimal *viable* (i.e., actually-breaking, unlike the single-flavon
   case already closed) SU(3)_f breaking sector and count its free
   parameters (flavon VEVs, extra Yukawas to the flavon multiplet,
   masses of the 8 new gauge bosons). Compare directly against however
   many Yukawa parameters step 1 shows Z3 actually removes. This is the
   number that turns "likely fails net" into a proven L1 result either
   way.
3. Only if both of the above land favorably: check whether the same
   SU(3)_f generator, plugged into `a`, also produces a *specific*
   texture (not just "nonzero") — e.g., does it reproduce anything like
   the Cabibbo-angle scale, without any post-hoc fitting (Rule 2 is
   live here — no SM value may be used as an input to the construction).
