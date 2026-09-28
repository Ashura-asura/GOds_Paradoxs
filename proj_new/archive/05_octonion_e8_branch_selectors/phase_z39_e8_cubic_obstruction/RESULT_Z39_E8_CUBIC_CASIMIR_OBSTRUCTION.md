# Phase Z39: does the E8 cubic Casimir escape the Z21 Schur obstruction?
# — closed negative for the minimal (27,3) single-flavon case

**Status: closed, L1 (pure linear algebra, exact to machine precision).
Net effect on the free-parameter count: none. This closes a candidate
escape route, it does not open one.**

## The question this phase answers

Z21 proved: if the three generations sit as a bare tensor factor C^3
under an irreducibly-acting SU(3)_f, then any generation-space operator
required to commute with that SU(3)_f is forced ∝ I_3 (Schur's Lemma),
regardless of the ambient algebra. The open question after Z21/Z22 and
the Gresnigt cross-check (RELATED_WORK.md) was: does embedding this
same SU(3)_f inside E8 change anything? Specifically — does E8's cubic
Casimir invariant (phase_a2_e8_core.py item 4, "d_ABC -> unique Yukawa
structure") supply new vacuum-selection information that a bare,
irreducibly-acting SU(3)_f does not?

## Setup

Standard branching (already in this repo): 248 = (78,1)+(1,8)+(27,3)+(27bar,3bar).
Three generations = the "3" of SU(3)_f, a bare fundamental tensored onto
the E6/Cl(10) factor -- structurally identical to Z21's H_F = C^32 x C^3.
The E8 cubic invariant restricted to (27,3)x(27,3)x(27,3) is, in flavor
space, the SU(3)_f-covariant tensor epsilon_ijk (the only rank-3
invariant available to three copies of the same "3", as opposed to a
3 and a 3bar).

## Result

**Test 1** [`e8_obstruction_test.py`]: epsilon_ijk v_i v_j v_k = 0
identically for any single flavor triplet v (antisymmetric tensor
contracted against a totally symmetric product) -- confirmed to machine
zero over 200 random complex v.

**Test 2**: the only invariant a single triplet v has access to is
|v|^2 (and functions of it), which is exactly flat over the full SU(3)_f
orbit -- confirmed numerically: random SU(3)_f rotations leave |v|^2 and
(v-dagger v)^2 fixed to 1e-9 while moving v's direction arbitrarily far
(measured overlaps 0.35-0.68 over 5 random rotations). No potential
built this way can select a direction, only a magnitude.

**Test 3** [`e8_obstruction_test2.py`]: the actual Yukawa object induced
by treating one triplet as a flavon direction phi is Y_ij(phi) =
epsilon_ijk phi_k. Its eigenvalues are (0, +i|phi|, -i|phi|) for *every*
direction of phi tested (5 random directions, machine precision). The
algebra fixes the texture -- one exact zero mode, one degenerate pair of
equal-magnitude eigenvalues -- but phi's direction (i.e. which
generation is massless) is left completely open, and the residual pair
never splits.

## Verdict

For the standard, minimal (27,3) branching, **E8's cubic Casimir does
not change the representation-theoretic conditions behind the Z21
obstruction.** It reproduces the identical failure shape already found
independently three times now:
  - this project (Z6-Z18, gauged SU(3)_f): degenerate/excluded vacuum.
  - this project (Z21, Schur's Lemma): forced-degenerate, representation-
    theoretic, no dynamics assumed.
  - Gresnigt (arXiv:2604.24795, S3 subgroup, reducible rep): one
    distinguished direction + one degenerate pair.
  - this phase (E8 cubic invariant, single flavon): one exact zero +
    one degenerate pair, direction unfixed.

Three structurally unrelated mechanisms land on the same wall. This is
stronger evidence that the obstruction is generic to "generation space
as a factor acted on by a symmetry with an accessible invariant
built from a single flavor multiplet," not an artifact of any one
implementation.

## What this does NOT close

Only the *minimal single-flavon* case was tested here, which is the
natural first case (Rule 1: no unexplained new structure) but not
exhaustive. Untested: a construction using multiple independent
E8-embedded triplets with distinct roles (not one flavon coupling to
itself via the cubic invariant). Per the pattern already established in
Z15-Z18, this class of move tends to re-import as much freedom as it
removes, but that is not demonstrated here and would need its own test
before being cited as closed.

## Rule 9 check

Non-numerological: both algebraic facts (cubic self-invariant vanishes;
quartic invariant is orbit-flat) are exact identities, not fits.
Falsifiable: a nonzero cubic self-invariant, or an SU(3)_f rotation that
failed to preserve |v|^2, would have broken this argument and it would
have said so.

## Reproducibility

`e8_obstruction_test.py`, `e8_obstruction_test2.py` -- pure numpy, no
external dependencies beyond this repo's existing conventions. Runs
clean, exact to machine precision.
