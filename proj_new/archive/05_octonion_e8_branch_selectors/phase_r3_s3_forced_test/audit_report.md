# Phase R3 Audit

| Claim | Label | Basis |
|---|---|---|
| Aut(bare 5-plane Witt decomposition) = (Z2)^5 : S5, order 3840 | L1 | direct construction |
| Chirality-preserving subgroup = Weyl(D5), order 1920 | L1 | standard fact, re-verified by construction here |
| Stabilizer of a 3-vs-2 block partition = S3 x S2, order 12 | L1 | checked in code, `scripts/r3_automorphism_check.py` |
| S3 x S2 is maximal in S5 | L2 | standard classification of maximal subgroups of S_n (imprimitive/Young-subgroup type); cited, not re-derived |
| There are 10 conjugate copies, none distinguished by Witt+chirality data alone | L1 | checked in code |
| **S3 is "forced" by Cl(10)** | **not established** | this phase explicitly does NOT claim L1/L2/L3 support for this -- see README verdict |
| **[R3-R1] This phase's S3xS2 answers the color/weak split, not the generation-replication question** | L2 | cross-checked against `phase_z22_gresnigt_import/gresnigt_generations.py`; psi_3's order-3 is imported from Gresnigt's explicit formula, not derived here or in Z22 |

## Rule 1 check
No numerology here -- the 3-vs-2 shape match to color/weak is noted but
explicitly NOT claimed as evidence, since the mechanism that produces
"a 3 and a 2" would produce any other partition pair with identical
ease (Rule 9 failure, documented in README).

## Rule 5 (failures documented)
The central hoped-for result of this phase -- a unique, intrinsically
forced S3 -- was NOT obtained. This is recorded with the same
prominence as the positive group-theory findings, per Rule 5.

## Rule 7 (no forward assumption)
Phase R4 (searching Z1-Z20 for an independent tie-breaker) is proposed
but explicitly not run or assumed to succeed.

## What this phase closes and does not close
- Closes: the naive reading of "S3 x S2 is a maximal subgroup of S5,
  therefore S3 is natural here" as sufficient justification. It is
  necessary-looking but not sufficient; ten symmetric copies exist.
- Does not close: the R3/R4 route as a whole. That depends on a search
  of the frozen phases not performed in this session.
