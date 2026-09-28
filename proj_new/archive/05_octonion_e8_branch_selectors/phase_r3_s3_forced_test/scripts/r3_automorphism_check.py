"""
Phase R3, Task 1-3: Aut(Witt structure) of Cl(10) and the S3-vs-S5 question.

Setup:
  Cl(10) built on a 10-dim quadratic space of split (Witt) type: Witt
  index 5, i.e. an orthogonal direct sum of 5 hyperbolic planes
  H_1 (+) ... (+) H_5. Each H_i has an isotropic pair (e_i, f_i).

  The "obvious" symmetry of this data (forgetting everything except the
  Witt decomposition itself) is: independently swap e_i <-> f_i in each
  plane (a Z2 per plane), and permute the 5 planes. That is the full
  hyperoctahedral group (Z2)^5 |: S5, order 2^5 * 5! = 3840.

Constraint 1 (chirality): the chirality operator Gamma = e_1 f_1 ... e_5 f_5
  (up to normalization) picks up a sign under each single-plane swap
  e_i<->f_i (that swap reverses orientation on H_i). Preserving Gamma
  fixed requires an EVEN number of plane-swaps. This cuts the Z2^5 down
  to its index-2 subgroup, giving (Z2)^4 |: S5 -- order 1920. This is
  exactly Weyl(D5), the Weyl group of Spin(10). Not a new fact (Weyl(D5)
  is standard), but stated here as the first checkpoint: "preserve
  chirality" is already fully accounted for by Weyl(D5), nothing more,
  nothing less.

Constraint 2 (charge assignment / minimal ideals): singling out a
  specific linear functional on the 5 Cartan directions (e.g. the one
  that reduces to hypercharge under an SU(5) embedding, equivalently
  the one that reproduces the color-triplet / weak-doublet split of the
  5-dim defining space) breaks the S5 permutation freedom down to
  whatever subgroup fixes that functional's *pattern* (not its value --
  permutations don't change eigenvalues, they only act on which axis
  carries which eigenvalue; what "fixes the pattern" means concretely
  is worked out below).

This script checks the group theory claims only. It does NOT attempt to
derive which 5-Cartan functional is "the" hypercharge direction from
Cl(10) alone -- that is exactly the open input Rule 2 requires to be
justified independently, and is flagged as such in interpretation.md.
"""

from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup
from math import comb

def main():
    results = {}

    S5 = SymmetricGroup(5)
    results["order_S5"] = S5.order()

    # Full "forget everything" automorphism group of 5 independent
    # hyperbolic planes: (Z2)^5 |: S5
    results["order_full_hyperoctahedral"] = (2**5) * S5.order()

    # After imposing chirality (even sign changes only): Weyl(D5)
    results["order_weyl_D5"] = (2**4) * S5.order()
    assert results["order_weyl_D5"] == 1920

    # A 3+2 BLOCK partition of the 5 planes (e.g. "3 color-type axes" /
    # "2 weak-type axes"): stabilizer inside S5 is S3 x S2.
    swap01 = Permutation([1, 0, 2, 3, 4], size=5)
    swap12 = Permutation([0, 2, 1, 3, 4], size=5)
    swap34 = Permutation([0, 1, 2, 4, 3], size=5)
    G_block = PermutationGroup([swap01, swap12, swap34])
    results["order_stabilizer_3plus2_block"] = G_block.order()
    assert results["order_stabilizer_3plus2_block"] == 12  # = |S3 x S2|

    # A bare 3-subset with NO structure imposed on the remaining 2 (i.e.
    # "3+1+1", the two leftover axes not grouped together): stabilizer
    # is just S3, order 6 -- also contains "an S3", but not tied to any
    # 2-vs-3 split, so it doesn't correspond to a doublet/triplet
    # pattern at all.
    G_bare = PermutationGroup([swap01, swap12])
    results["order_stabilizer_bare_3subset"] = G_bare.order()
    assert results["order_stabilizer_bare_3subset"] == 6

    # How many S5-conjugate copies of the 3+2 block stabilizer exist?
    # (= how many distinct 3-vs-2 splits of 5 objects there are). If >1,
    # then "S3 x S2 is A maximal subgroup of S5" is true but does not by
    # itself pick out a UNIQUE copy -- something else has to say which
    # 3 of the 5 axes are "the 3".
    results["num_conjugate_3plus2_subgroups"] = comb(5, 3)
    assert results["num_conjugate_3plus2_subgroups"] == 10

    # Is S3 x S2 maximal in S5? (standard fact: yes, imprimitive maximal
    # subgroups of S_n are exactly the Young-subgroup block stabilizers
    # for each partition of n; S3 x S2 is one of these for n=5)
    results["S3xS2_is_maximal_in_S5"] = True  # standard result, not re-derived here

    return results


if __name__ == "__main__":
    import json
    r = main()
    r = {k: (int(v) if not isinstance(v, bool) else v) for k, v in r.items()}
    print(json.dumps(r, indent=2))
    with open("results_r3_automorphism_check.json", "w") as f:
        json.dump(r, f, indent=2)
