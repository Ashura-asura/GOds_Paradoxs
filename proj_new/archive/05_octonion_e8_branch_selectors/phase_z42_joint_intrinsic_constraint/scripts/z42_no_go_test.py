"""
Z42 Task 5 -- strongest no-go theorem this phase can support.

This script does not run new numerics; it assembles the results of
z42_representation.py, z42_invariant_search.py, z42_vacuum_analysis.py,
z42_freedom_count.py into one formal statement, per Task 5's
requirement. It fails loudly (assertion error) if any prerequisite
result file is missing or any of its "confirmed" flags is False --
the theorem is not allowed to be recorded as closed on unverified
inputs.
"""

import json
import os

THEOREM = """
THEOREM (Z42, generation-space invariant-ring exhaustion)
-----------------------------------------------------------
Assumptions:
  (A1) The three fermion generations are identified with the SU(3)_f
       representation obtained from the standard branching
           E8 super_set_of E6 x SU(3)_f,
           248 = (78,1) + (1,8) + (27,3) + (27bar,3bar)
       (Slansky 1981, Table 82) -- i.e. generation space IS a bare
       tensor factor transforming as 3 (or 3bar) of SU(3)_f, per this
       project's standing construction since Z2.
  (A2) Any candidate Yukawa/vacuum-selecting coupling must be built
       from E8-covariant objects: contractions of any finite number of
       copies of the adjoint 248 and/or a bounded number of flavon
       multiplets valued in representations that themselves appear in
       248's branching.

Claim:
  Under (A1)-(A2), restricted to flavor (SU(3)_f) indices, EVERY
  invariant coupling constructible at ANY order is a polynomial in
  {delta_i^j, epsilon_ijk, epsilon^ijk} alone. Consequently:
    (a) a single SU(3)_f-covariant flavon can only produce a Yukawa
        texture Y_ij(phi) = c epsilon_ijk phi^k (+ delta-proportional
        pieces that do not depend on phi's direction), which is exactly
        antisymmetric and therefore has one exact zero eigenvalue and a
        residual exactly-degenerate pair, for ANY order of E8 structure
        used to build the coupling -- not just the cubic Casimir tested
        in Z39;
    (b) the associated SU(3)_f-invariant scalar potential is a function
        of |phi|^2 only, at any order, so minimization can never select
        a direction in flavor space, only a magnitude;
    (c) reaching a non-degenerate rank-3 texture therefore requires
        MULTIPLE independent flavons/invariant structures, at which
        point (Z40, Cases A-C, freedom-counted again in this phase's
        z42_freedom_count.py) the construction re-imports as much or
        more continuous freedom than it removes.

Proof sketch:
  Step 1 (this phase, z42_representation.py): the SU(3)_f content of
  the FULL adjoint 248 -- not just the (27,3) matter piece -- is
  exactly {1, 3, 3bar, 8}, and 8 = traceless part of 3 x 3bar
  supplies no invariant-theory generator beyond what 3, 3bar already
  give (Clebsch-Gordan dimension check 3x3bar=9=1+8, verified exactly).

  Step 2: by the First Fundamental Theorem of invariant theory for
  SL(3,C) / SU(3) (Weyl 1939, "The Classical Groups", Ch. II section 6),
  the ring of polynomial invariants of any number of copies of the
  fundamental and antifundamental representations of SU(3) is generated
  by delta and epsilon alone, with no invariant generators at any
  degree beyond these two ranks (2 and 3). This is a 85-year-old
  classical theorem, not a numerical conjecture; this phase's
  z42_invariant_search.py provides Monte Carlo confirmation at the
  degree relevant here (a generic non-epsilon rank-3 tensor is
  confirmed to fail SU(3) invariance in >95% of random trials, while
  delta/epsilon are confirmed invariant to machine precision) as a
  cross-check, not as the proof itself.

  Step 3: Steps 1-2 together mean E8's structure constants, at ANY
  order, restricted to flavor indices, cannot escape the
  delta/epsilon-generated ring. This upgrades Z39's "the cubic Casimir
  specifically doesn't help" to "no order helps."

Scope / what this does NOT cover (stated per Rule 9 and Task 5's own
"do not overclaim" instruction):
  - Does not cover representations of SU(3)_f beyond {1,3,3bar,8} --
    those simply never appear if (A1)-(A2) hold, but a flavon
    introduced BY HAND in e.g. the 6 or 10 is not covered by this
    theorem (though Rule 1, no unexplained new structure, argues
    against introducing one anyway, since it wouldn't come from E8).
  - Does not cover non-factorized generation space (Priority 1, NCG /
    spectral-triple route) -- (A1) is exactly the assumption that
    route drops. This remains the one door this project has
    consistently flagged as open and untried, now for the third time
    (Z22, Z40, this phase).
  - Does not cover alternative E8 maximal-subgroup chains other than
    E6 x SU(3)_f (e.g. SO(16), SU(9), E7 x SU(2)) -- a different
    embedding of a would-be flavor symmetry might carry different
    representation content. Not tested in this project at any phase.
"""


def assemble():
    base = os.path.dirname(os.path.abspath(__file__))
    needed = {
        "task1": "results_task1.json",
        "task2": "results_task2.json",
        "task3": "results_task3.json",
        "task4": "results_task4.json",
    }
    loaded = {}
    for key, fname in needed.items():
        path = os.path.join(base, fname)
        assert os.path.exists(path), f"Missing prerequisite: {fname} -- run its script first."
        with open(path) as f:
            loaded[key] = json.load(f)

    checks = [
        loaded["task1"]["dim_check_passed"],
        loaded["task1"]["octet_reduces_to_delta_epsilon_building_blocks"],
        loaded["task2"]["delta_invariant_confirmed"],
        loaded["task2"]["epsilon_invariant_confirmed"],
        loaded["task2"]["generic_rank3_tensor_correctly_fails_invariance"],
        loaded["task2"]["single_triplet_no_direction_selecting_invariant_confirmed"],
        loaded["task3"]["cubic_self_contraction_vanishes_confirmed"],
        loaded["task3"]["minimization_check"]["flat_along_SU3f_orbit_at_fixed_radius"],
    ]
    assert all(checks), "A prerequisite numerical check FAILED -- theorem cannot be recorded as supported."

    return {
        "theorem_text": THEOREM,
        "classification": "L2 (representation-theoretic + classical-theorem argument, "
                           "cross-checked numerically at low degree; NOT a from-scratch "
                           "machine-verified proof of Weyl's 1939 theorem itself, which "
                           "is cited rather than re-derived)",
        "net_effect_relative_to_Z39_Z40": (
            "Upgrades the obstruction from 'tested for the cubic Casimir, single "
            "flavon' (Z39) and 'tested case-by-case for 2-triplet / conjugate-pair "
            "/ adjoint flavons' (Z40) to 'holds at every order of E8 structure, for "
            "any single-flavon construction, as a consequence of the SU(3)_f "
            "representation content of the full adjoint 248 being exhausted at "
            "{1,3,3bar,8}.' Task 5 asked for the strongest supportable no-go "
            "statement; this is it."
        ),
        "all_prerequisite_checks_passed": True,
        "prerequisite_check_count": len(checks),
    }


if __name__ == "__main__":
    result = assemble()
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_task5.json"), "w") as f:
        json.dump(result, f, indent=2)
    print(result["theorem_text"])
    print(json.dumps({k: v for k, v in result.items() if k != "theorem_text"}, indent=2))
