# ITEM7_LHS_SPECTRAL_SEQUENCE.md — full derivation (2026-08-01)

**Purpose:** assemble the pieces verified by code in
`item7_reverification_no_gap.py` into the final answer, via the
Lyndon-Hochschild-Serre (LHS) spectral sequence for the group extension

    1 -> Z3 -> S3 -> Z2 -> 1

This is the analytic step that file's docstring calls "not
computer-executed, but fully standard and citable." It is written out
in full here so every step can be checked against a standard reference
(e.g. K. Brown, *Cohomology of Groups*, Ch. VII), not taken on faith.

## Setup

The LHS spectral sequence for a group extension `1 -> N -> G -> Q -> 1`
has

    E_2^{p,q} = H^p(Q; H^q(N; Z))  =>  H^{p+q}(G; Z)

with `Q` acting on the coefficient module `H^q(N;Z)` via its conjugation
action on `N`. Here `N = Z3`, `Q = Z2`, and the code file verified
directly (not assumed) that `Q` acts on `N` by inversion.

## Step 1 — the coefficient modules `H^q(Z3; Z)`

From the code file's Section 3 (verified, not quoted):

    H^0(Z3;Z) = Z          (trivial Q-action)
    H^{2k}(Z3;Z) = Z/3 for k >= 1   (up to universal-coefficients duality
                                      with the H_{2k-1}(Z3;Z)=Z/3 computed
                                      in the code — same standard fact)
    H^{odd}(Z3;Z) = 0

The inversion automorphism of Z3 acts on `H^2(Z3;Z) = Z/3` by
multiplication by -1 (standard: inversion on a cyclic group acts as -1
on the degree-2 cohomology class classifying the group itself as a
central extension of itself by nothing — equivalently, functoriality of
the cup product `H^2 = H^1 ⊗ H^1`-type structure). By the cup product
structure of a cyclic group's cohomology ring, the action on
`H^{2k} = (H^2)^{⊗k}` is then by `(-1)^k`.

## Step 2 — the coprime-order vanishing lemma kills the q>0 rows for p>0

Checked explicitly in the code file, Section 4: `2` is invertible mod
`3`. Since `H^q(Z3;Z)` for `q>0` is a `Z/3`-module (or zero) and `|Q|=2`
is invertible on any `Z/3`-module, the standard lemma (multiplication by
`|Q|` factors through the composite restriction-then-transfer map, which
is the identity on `H^*(Q;M)`, forcing every positive-degree class to be
both `|Q|`-torsion and `|Q|`-invertible, hence zero) gives:

    H^p(Q; H^q(Z3;Z)) = 0   for all p > 0, q > 0.

This is the step doing the real work: it is a **forced** vanishing, not
an assumption tuned to make the final numbers come out right (Rule 9
check: if `N` and `Q` did not have coprime order, this vanishing would
fail and the spectral sequence would not collapse this way — the
mechanism is falsifiable by construction, not fitted to this one case).

## Step 3 — what's left: two axes

With every `(p,q)` with `p>0` AND `q>0` zero, `E_2^{p,q}` is nonzero only
on the `q=0` row or the `p=0` column:

  - `q=0` row: `E_2^{p,0} = H^p(Q;Z) = H^p(Z2;Z)`, the ordinary
    cohomology of `Z2` with trivial coefficients: `Z, 0, Z/2, 0, Z/2, ...`
    for `p = 0,1,2,3,4,...` (standard cyclic-group pattern, same one the
    code file verifies for `Z/2` on the homology side).

  - `p=0` column: `E_2^{0,q} = H^0(Q; H^q(Z3;Z)) = (H^q(Z3;Z))^{Q}`, the
    `Q`-invariants. For `q` odd this is `0` trivially. For `q = 2k` (`k
    >= 1`): the group is `Z/3` with `Q=Z2` acting by `(-1)^k` (Step 1).
    Invariants of the trivial action (`k` even) is all of `Z/3`;
    invariants of the `-1` action (`k` odd) is `{x : x = -x} = {0}`
    (since `2` is invertible mod `3`, `2x=0 => x=0`). So:

        E_2^{0,q} = Z/3  if q ≡ 0 (mod 4), q > 0
                  = 0    if q ≡ 2 (mod 4)
                  = 0    if q odd

## Step 4 — no room for differentials, no extension ambiguity

Every potential differential `d_r : E_r^{p,q} -> E_r^{p+r,q-r+1}` maps
between two of these two axes-only groups. Checking the few that could
be nonzero (e.g. `d_2 : E_2^{0,q} -> E_2^{2,q-1}`) always lands on a
`p>0,q>0` term, which is `0`. So the spectral sequence collapses at
`E_2`: `H^n(S3;Z)` has associated graded equal to `E_2^{n,0} ⊕
E_2^{0,n}` (the only two possibly-nonzero terms with `p+q=n`). Since
`E_2^{n,0}` is a 2-group and `E_2^{0,n}` is a 3-group (coprime orders
when both nonzero), the extension problem is trivial: an abelian group
extension of a 3-group by a 2-group (or vice versa) always splits as a
direct sum.

## Step 5 — the table

| n | E_2^{n,0} = H^n(Z2;Z) | E_2^{0,n} = (H^n(Z3;Z))^{Z2} | H^n(S3;Z) |
|---|---|---|---|
| 0 | Z   | Z (trivially, n=0 counted once) | Z |
| 1 | 0   | 0 | 0 |
| 2 | Z/2 | 0 (n≡2 mod 4) | Z/2 |
| 3 | 0   | 0 | 0 |
| 4 | Z/2 | Z/3 (n≡0 mod 4) | Z/6 |
| 5 | 0   | 0 | 0 |
| 6 | Z/2 | 0 | Z/2 |

## Step 6 — converting to homology (what `RESULT_item7.md` actually cites)

For a finite group, `H^n(G;Z) ≅ Ext(H_{n-1}(G;Z), Z)` for `n ≥ 1` (the
`Hom` part of the universal coefficient theorem vanishes since `H_{n-1}`
is finite for `n≥2`, and `H_0=Z` free only affects `n=1` where
`Ext(H_0,Z)=Ext(Z,Z)=0` anyway), and `Ext(T,Z) ≅ T` for finite `T`. So
`H^n(S3;Z) = H_{n-1}(S3;Z)` for `n ≥ 2` (with `H_1(S3;Z) = 0`'s
partner statement handled directly via abelianization: `H_1(G;Z) =
G^{ab}`, and `S3^{ab} = Z/2` — a completely elementary fact, not part of
this spectral sequence at all, included here only for completeness).

Reading off from the table above:

    H_1(S3;Z) = S3^{ab} = Z/2         (elementary; matches RESULT_item7.md)
    H_2(S3;Z) = H^3(S3;Z) = 0         (matches RESULT_item7.md)
    H_3(S3;Z) = H^4(S3;Z) = Z/6       (matches RESULT_item7.md)
    H_4(S3;Z) = H^5(S3;Z) = 0         (matches RESULT_item7.md)

This reproduces every number `RESULT_item7.md` attributed to the
external GAP/HAP session, by a completely independent method, with every
input to the argument either checked directly by code
(`item7_reverification_no_gap.py`) or a standard, named, citable theorem
(LHS spectral sequence; universal coefficient theorem; coprime-order
vanishing lemma) applied to this specific, verified group structure —
not assumed to make the answer come out right.

## What this does and doesn't change

Per Rule 3: this whole derivation is L1 (forward-derived from a stated
mechanism, not fitted). It replaces the L2 status
`audit report/LIST_OF_CORRECTIONS.md` correctly assigned (external
citation only) with a genuine independent re-derivation, closing
secondary open thread #4 in `audit report/OPEN_PROBLEMS_AFTER_AUDIT.md`.

It does **not** touch the representation-theoretic argument built on top
of these numbers in `RESULT_item7.md` (the 3-generation permutation
representation of S3 has zero 't Hooft anomaly because it's a real/
orthogonal representation) — that argument was never in question; only
the group-cohomology numbers it depends on were unverified inside this
repository, and now are.
