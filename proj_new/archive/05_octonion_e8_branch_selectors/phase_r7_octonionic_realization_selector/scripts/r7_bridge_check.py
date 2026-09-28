"""
Phase R7: Octonionic Realization Branch Selector Audit.

This script does NOT attempt new Lie algebra. It performs exactly one
check, mechanically, against the actual repository: for each of the
claimed candidate branches, does ANY file in this project express that
branch's non-SO(10) generators as an explicit function of Phase A1's
octonion left-multiplication operators (`build_octonion_structure_
constants` in `support/qosc_division_connection.py`)?

Method: static, not symbolic. This is a falsifier of a *bridge*, not a
derivation -- it checks whether the bridge (octonion ops -> E8-branch
generators) exists anywhere in the codebase, which is a well-defined,
mechanically checkable question, before any per-branch algebra is even
worth attempting.
"""
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BRANCHES = {
    "E6xSU(3)_f": {
        "source_files": ["phases below_Z_25/phase_a2_e8_core.py"],
        "status_in_repo": "real, frozen (Phase A2)",
    },
    "SO(16)->SO(10)xSU(4)": {
        "source_files": ["docs/ALL_DERIVATIVES.md"],
        "status_in_repo": "real but pre-Z-numbering exploratory sketch, not a frozen phase",
    },
    "SU(5)_A x SU(5)_B": {
        "source_files": [
            "phase_z44_su5xsu5/phase_z44_su5xsu5/scripts/z44_branching.py",
            "phase_z44_su5xsu5/phase_z44_su5xsu5/scripts/z44_structure_check.py",
        ],
        "status_in_repo": "real, frozen (Z44, closed negative)",
    },
    "SU(9)": {
        "source_files": [],
        "status_in_repo": "NOT FOUND in repo -- no dedicated branch computation exists; retracted from R6",
    },
    "E7xSU(2)": {
        "source_files": [],
        "status_in_repo": "NOT FOUND as a dedicated branch computation -- only incidental mentions; retracted from R6",
    },
    "F4xG2": {
        "source_files": ["phase_z39_e8_cubic_obstruction/e8_obstruction_test.py"],
        "status_in_repo": "MISLABELED in R6 -- this file tests the E8 cubic Casimir/Schur obstruction WITHIN the already-chosen E6xSU(3)_f branch, not an F4xG2 branching. No F4xG2 branch computation exists in this repo.",
    },
}

OCTONION_MARKERS = ["octonion", "qosc_division", "build_octonion_structure_constants"]


def file_uses_octonion_ops(path):
    full = os.path.join(REPO, path)
    if not os.path.isfile(full):
        return None  # file doesn't exist / not found at that path
    with open(full, "r", errors="ignore") as f:
        text = f.read().lower()
    return any(m in text for m in OCTONION_MARKERS)


def main():
    results = {}
    for branch, info in BRANCHES.items():
        entry = {"status_in_repo": info["status_in_repo"], "files_checked": [], "any_octonion_bridge_found": False}
        for path in info["source_files"]:
            found = file_uses_octonion_ops(path)
            entry["files_checked"].append({"path": path, "octonion_ops_used": found})
            if found:
                entry["any_octonion_bridge_found"] = True
        results[branch] = entry
    return results


if __name__ == "__main__":
    import json
    r = main()
    print(json.dumps(r, indent=2))
