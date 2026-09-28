# Phase Z10 — resolving Z8/Z9's flagged modeling caveat (this session)

## Question

Both Z8 and Z9 ended by flagging the same open item and declining to
call their results final until it was resolved: was
`D_F(Y_gen) = A32 (x) Y_gen` (A32 = the already-doubled, already-
Hermitian internal Yukawa block) the right way to embed a Majorana-
type generation-space coupling into the doubled `H_F`, or does
requiring `Y_gen` Hermitian — which that ansatz needs in order for
`D_F` to come out Hermitian — hide a modeling artifact that a
construction using the real-structure/doubling machinery directly,
rather than tensoring onto an already-doubled block, would not have?

## Method

**First, pin down algebraically why the old ansatz needs
`Hermitian(Y_gen)` at all.** Expanding `A32 (x) Y_gen` block-by-block
(`A32 = [[0,Y_H],[Y_H^dagger,0]]`) shows it equals
`[[0, Y_H (x) Y_gen], [Y_H^dagger (x) Y_gen, 0]]`. For this to be a
valid Hermitian off-diagonal block matrix, the (2,1) block must be the
dagger of the (1,2) block: `Y_H^dagger (x) Y_gen =? (Y_H (x) Y_gen)^dagger
= Y_H^dagger (x) Y_gen^dagger`. Since `Y_H^dagger != 0`, this forces
`Y_gen = Y_gen^dagger`. So `Hermitian(Y_gen)` was never an independent
assumption bolted on top of a free ansatz — it's an algebraic
consequence of tensoring `Y_gen` onto the *already-doubled* `A32`,
rather than doubling the combined block directly.

**The fix**: build the off-diagonal Yukawa block in the un-doubled
48-dim (internal x generation) space first, then double *that*:

```
Y_full(Y_gen) = Y_H (x) Y_gen                        (48x48, generically non-Hermitian)
D_F_alt(Y_gen) = [[0, Y_full], [Y_full^dagger, 0]]    (96x96, Hermitian for ANY Y_gen)
```

This is Hermitian by construction for every complex `Y_gen` — no
Hermiticity constraint on `Y_gen` is needed. The only constraint kept
is the one with actual group-theoretic motivation from Z6:
`Y_gen` symmetric (`10`, `126`) or antisymmetric (`120`).

**Verified this is a legitimate Dirac operator before trusting any
parameter count from it** — checked, on a generic (non-Hermitian,
non-symmetric) test `Y_gen`, and separately on symmetric/antisymmetric
test `Y_gen`, that the axioms Z6/Z7 required still hold for
`D_F_alt`:

```
||{eps96, D_F_alt}||   = 0.0   (grading, exact, any Y_gen)
||D_F_alt - D_F_alt^dagger|| = 0.0   (Hermitian, exact, any Y_gen — confirms the algebra above)
J_F D_F psi == +D_F J_F psi   for symmetric Y_gen      (True)
J_F D_F psi == -D_F J_F psi   for antisymmetric Y_gen  (True)
```

using `J_F = (P (x) I_3) . conj(.)` on the full 96-dim `H_F`, the
direct generation-trivial extension of Z6's `J₀` — not previously
checked explicitly at the full-`H_F` level in Z8/Z9, so this closes a
second, smaller gap alongside the main one.

Then reran exactly Z9's calculation — same `su(3)_F` full 8x8=64-pair
loop, same Gram-matrix accumulation, same three channels
(`M10`, `M120`, `M126`) — with two settings: `impose_hermitian=True`
(reproduces Z9's old ansatz exactly, as a sanity check that the new
code is consistent with the old) and `impose_hermitian=False` (the new
ansatz, dropping the artificial constraint).

## Result

**Sanity check — old ansatz reproduced exactly:**

```
channel   old (Hermitian(Y_gen))
M10       1 real param  -- Y_gen = -1/sqrt(3) * I_3       [matches Z9 exactly]
M120      0
M126      1 real param  -- Y_gen = -1/sqrt(3) * I_3       [matches Z9 exactly]
```

**New ansatz (real-structure-aware, no artificial Hermiticity
constraint on `Y_gen`):**

```
channel   new (real-structure-aware)
M10       2 real params (= 1 complex) -- Y_gen = c * I_3, c complex
M120      0
M126      2 real params (= 1 complex) -- Y_gen = c * I_3, c complex
```

For `M10`/`M126` the surviving 2-dimensional real space is exactly
`span{ I_3, i*I_3 }` — i.e. one complex parameter times the identity,
not a richer texture. `M120` is still forced to exactly zero; nothing
about that changes.

## Verdict — L1

**L1.** This is a clean, fully resolved answer to the specific open
question, not a partial result with a new caveat replacing the old
one:

1. The reason the old ansatz needed `Hermitian(Y_gen)` is now
   understood algebraically (a consequence of construction order, not
   physics), not just empirically observed.
2. The corrected ansatz is independently verified to satisfy every
   axiom (Hermiticity, grading, real-structure commutation) that Z6/Z7
   established as required, for arbitrary `Y_gen` — so dropping the
   constraint isn't just "allowed because it's more permissive," it's
   required because the old constraint was never actually part of
   what makes `D_F` valid.
3. The code was cross-checked against Z9's own numbers before trusting
   the new branch (`impose_hermitian=True` reproduces Z9's `1 / 0 / 1`
   exactly), so the change in the `False` branch isn't a bug
   masquerading as a discovery.

**What changes, and what doesn't:** the parameter count goes from
`1/0/1` to `2/0/2` — an artifact of the old ansatz over-constraining
by one real parameter (the overall phase of the Yukawa coupling) that
had no business being constrained at all. **The physical conclusion
Z9 drew is unaffected and, if anything, reinforced**: unbroken
`su(3)_F` still forces the symmetric channels to be exactly
generation-blind (`Y_gen ∝ I_3`, still zero off-diagonal structure,
still no hierarchy or mixing possible) and still forces the
antisymmetric channel to vanish identically. The extra surviving
parameter is a complex overall scale/phase on a generation-blind
coupling, which carries no flavor information — it does not reopen
any possibility of hierarchy or mixing under exact `su(3)_F`. Z9's
"spontaneous breaking of `su(3)_F` is a derived necessity, not a
modeling choice" conclusion holds under the corrected construction,
now without the open modeling caveat attached to it.

## Remaining caveats (stated plainly, not swept in with the above)

- This still uses one Higgs internal direction pattern per channel
  (`M10[0]`, one `M120` triple-component, one `M126` ONB component),
  as all of Z6–Z9 did — not a sweep over the full internal moduli
  space of each channel.
- The `su(3)_F` generators used throughout (`build_su3f_generators`)
  are the standard flavor-space Gell-Mann matrices — a natural,
  standard choice, but still a choice of which group acts as the
  family symmetry, not something derived from the Cl(10)xE8
  construction itself.
- This resolves the *specific* Hermitian-vs-not modeling question
  flagged in Z8/Z9. It does not certify every other modeling decision
  made earlier in the Z-series (e.g. `J₀`'s specific form, the choice
  to use `P` as the swap/conjugation structure) — those were
  independently checked in Z6 and are not reopened here.

## Next step

With this caveat closed, the natural continuations are the ones Z9
already listed and did not yet do: sweep across the internal moduli
of each Higgs channel (not just one representative direction) to check
whether `Y_gen ∝ I_3` survives as the unique answer across the whole
internal space, or was in some way special to the one direction tested
so far.
