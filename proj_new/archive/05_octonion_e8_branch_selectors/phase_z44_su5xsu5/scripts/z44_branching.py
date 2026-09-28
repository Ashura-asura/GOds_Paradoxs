"""
Z44 Task 1 -- exact branching construction.

Step A: E8 > SU(5)_A x SU(5)_B, adjoint 248.
  Source: Slansky (1981) Table 24 (same source already used for O2).
  248 = (24,1) + (1,24) + (5,10bar) + (5bar,10) + (10,5bar) + (10bar,5)

Step B: break SU(5)_A > SU(3)_c x SU(2)_L x U(1)_Y via the standard
Georgi-Glashow embedding, leaving SU(5)_B COMPLETELY UNTOUCHED (per
the Z44 brief -- "leave the second SU(5) untouched initially").
  Source: Georgi & Glashow (1974); branching of 5, 5bar, 10, 10bar,
  24 of SU(5) under SU(3)xSU(2)xU(1) is standard textbook material
  (e.g. Slansky Table 33, or any GUT textbook), reproduced here and
  checked by direct dimension arithmetic, not just asserted.

Every dimension claim below is checked in code (L1: arithmetic
verified here). The BRANCHING RULES THEMSELVES (which SM multiplet
comes from which SU(5) rep, and its hypercharge) are cited from the
standard GUT literature, not re-derived from SU(5) root system here
-- so their provenance is L2, exactly as Slansky's E8 table was L2 in
O2. This is flagged explicitly so it propagates correctly into the
audit report.
"""

import json
from math import comb

# ---------------------------------------------------------------
# Step A: E8 > SU(5)_A x SU(5)_B
# ---------------------------------------------------------------
E8_BRANCHING = [
    ("(24,1)", 24, 1, "adjoint of SU(5)_A"),
    ("(1,24)", 1, 24, "adjoint of SU(5)_B"),
    ("(5,10bar)", 5, 10, "bifundamental"),
    ("(5bar,10)", 5, 10, "bifundamental"),
    ("(10,5bar)", 10, 5, "bifundamental"),
    ("(10bar,5)", 10, 5, "bifundamental"),
]

# ---------------------------------------------------------------
# Step B: standard SU(5) > SU(3) x SU(2) x U(1) branching rules
# (Georgi-Glashow). Hypercharge normalized so that the SM lepton
# doublet has Y = -1/2 (GUT-normalized values shown; overall
# normalization does not affect anything counted in this phase).
# ---------------------------------------------------------------
SU5_BRANCHING = {
    "5":     [("(3,1)", 3, -1/3), ("(1,2)", 2, 1/2)],
    "5bar":  [("(3bar,1)", 3, 1/3), ("(1,2)", 2, -1/2)],
    "10":    [("(3,2)", 6, 1/6), ("(3bar,1)", 3, -2/3), ("(1,1)", 1, 1)],
    "10bar": [("(3bar,2)", 6, -1/6), ("(3,1)", 3, 2/3), ("(1,1)", 1, -1)],
    "24":    [("(8,1)", 8, 0), ("(1,3)", 3, 0), ("(1,1)", 1, 0),
              ("(3,2)", 6, -5/6), ("(3bar,2)", 6, 5/6)],
}


def check_su5_branchings():
    out = {}
    for rep, pieces in SU5_BRANCHING.items():
        total = sum(d for _, d, _ in pieces)
        expected = 24 if rep == "24" else int(rep.replace("bar", ""))
        out[rep] = {"pieces": pieces, "total": total, "matches_expected": total == expected}
    return out


def check_e8_branching():
    total = sum(a * b for _, a, b, _ in E8_BRANCHING)
    return {"pieces": E8_BRANCHING, "total": total, "matches_248": total == 248}


def apply_su5A_breaking():
    """
    For every E8>SU(5)_AxSU(5)_B piece, replace the SU(5)_A label by its
    SU(3)xSU(2)xU(1) branching, leaving the SU(5)_B label as a single,
    UNSPLIT block (this is the literal computational meaning of
    "leave the second SU(5) untouched").
    """
    out = []
    for label, dimA, dimB, kind in E8_BRANCHING:
        # figure out which SU(5)_A rep this piece uses
        if label in ("(24,1)",):
            a_rep = "24"
        elif label in ("(1,24)",):
            a_rep = None  # SU(5)_A singlet, nothing to break
        elif label == "(5,10bar)":
            a_rep = "5"
        elif label == "(5bar,10)":
            a_rep = "5bar"
        elif label == "(10,5bar)":
            a_rep = "10"
        elif label == "(10bar,5)":
            a_rep = "10bar"
        else:
            raise ValueError(label)

        if a_rep is None:
            out.append({
                "original_piece": label,
                "SM_pieces": [("SU(5)_A singlet", 1)],
                "SU5_B_block_dim": dimB,
                "SU5_B_block_touched": False,
            })
            continue

        sm_pieces = [(name, d) for name, d, _y in SU5_BRANCHING[a_rep]]
        out.append({
            "original_piece": label,
            "SM_pieces": sm_pieces,
            "SU5_B_block_dim": dimB,
            "SU5_B_block_touched": False,  # by construction -- see z44_structure_check.py
        })
    return out


if __name__ == "__main__":
    results = {
        "su5_branching_dimension_checks": check_su5_branchings(),
        "e8_branching_dimension_check": check_e8_branching(),
        "su5A_broken_pieces": apply_su5A_breaking(),
    }
    with open("results_z44_branching.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
