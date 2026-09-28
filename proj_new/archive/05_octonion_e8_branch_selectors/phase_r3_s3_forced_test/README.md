# Phase R3: Is S3 forced by Cl(10), or selected?

**Status: OPEN, and DOWNGRADED on self-review. Task 1 (group-theory
scaffolding) done, L1, and correct as far as it goes — but see
`interpretation.md`'s [R3-R1 correction]: this phase's `S5 -> S3xS2`
construction (partitioning one spinor's 5 Cartan directions) is very
likely the color/weak split (already-derived gauge structure, Phase A),
NOT the generation-replication mechanism (Z22's `psi_3`, which acts on
the whole algebra, not one spinor's Cartan directions). This phase's
result is probably not load-bearing for "why 3 generations." The
corrected next question is scoped in `interpretation.md`. No update to
project-level status (still 0/19).**

## Why this phase exists

The Z44 audit (external review, see `../CHANGELOG.md` entry below)
identified the make-or-break question for the Cl(10) intrinsic
automorphism route: `Aut(Witt structure) = S5` is asserted, and S3 is
wanted as the source of "3 generations." The audit's own framing of the
danger: if S3 is picked because "it works," that's another Rule 1/Rule
2 violation dressed up as group theory. This phase is the cheap
falsifier the audit called for.

## What was actually computed (L1, `scripts/r3_automorphism_check.py`)

1. The full automorphism group of a bare Witt decomposition into 5
   hyperbolic planes (forgetting all physics) is the hyperoctahedral
   group `(Z2)^5 : S5`, order 3840.
2. Imposing chirality-invariance (fixing the sign of
   `Gamma = e_1 f_1 ... e_5 f_5`) cuts this to `(Z2)^4 : S5`, order
   1920 -- this is exactly `Weyl(D5)`, the Weyl group of Spin(10). Not
   a new result; confirmed here as the correct starting point.
3. **The load-bearing check:** `S3 x S2`, the stabilizer in `S5` of a
   3-vs-2 block partition of the five planes, has order 12 and is
   confirmed (standard fact, checked here) to be a maximal subgroup of
   `S5`.
4. **The problem:** there are `C(5,3) = 10` distinct 3-vs-2 partitions
   of five objects, all conjugate under `S5`. Each gives an equally
   valid `S3 x S2` subgroup. Nothing in the bare Witt/chirality
   structure singles out any one of the 10 over the other 9.
5. For contrast: the stabilizer of a bare 3-subset with the remaining 2
   axes left unstructured ("3+1+1") is `S3` alone, order 6 -- also
   contains "an S3," but is not tied to any doublet/triplet pattern at
   all, so it is a strictly weaker and less useful fact than it might
   look.

## The actual verdict on the S3/S5 question

**S3 x S2 is A maximal subgroup of S5 -- this part is real and checked.
It is NOT uniquely forced by the Witt decomposition + chirality alone.**
Ten equally good copies exist. Picking one of the ten out of Cl(10)'s
bare structure requires an additional input: a specific linear
functional on the 5 Cartan directions (concretely: whichever one
reduces to hypercharge / the SU(5) color-triplet-vs-weak-doublet split
under some embedding chain) that is NOT visible in the Witt
decomposition by itself.

This is precisely the failure mode the audit warned about, now located
exactly rather than argued about: the open question is not "does S3
sit inside S5" (yes, trivially, in ten ways) but **"is there a
Cl(10)-intrinsic reason (not an SU(5)-embedding choice made to match
the SM) that selects one 3-vs-2 partition over the other nine?"**

That question is not answered here. See `interpretation.md`.

## Rule 9 check (discriminating power)

Would this same argument have "explained" a different generation count
equally well? Yes, trivially -- the identical stabilizer construction
would produce an `S4 x S1` (order 24, no S3) for a hypothetical 4-vs-1
split, or `S2 x S3` again but rooted at any of the other nine
3-subsets, with zero ability to prefer 3 over any other partition size.
**Zero discriminating power as it stands.** This phase is recorded
under Rule 8 (a precisely located structural gap is a real result) --
it is not recorded as a positive derivation, and must not be rounded up
to one.
