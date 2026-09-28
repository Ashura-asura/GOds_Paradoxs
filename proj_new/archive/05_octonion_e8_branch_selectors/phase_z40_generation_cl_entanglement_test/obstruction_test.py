"""
Master runner for Phase Z40. Runs Tasks 1-3's scripts as subprocesses
(so each remains independently reproducible on its own), collects their
JSON outputs, and prints the final verdict in the requested format.
Task 4 is a written derivation (no_go_attempt.md); Task 5 is OPEN and
is reported as such, not computed.
"""
import subprocess
import json
import sys

SCRIPTS = ["commutant_solver.py", "e8_branching_analysis.py", "yukawa_search.py"]

for script in SCRIPTS:
    print(f"\n{'#'*72}\n# running {script}\n{'#'*72}")
    result = subprocess.run([sys.executable, script], capture_output=False)
    if result.returncode != 0:
        print(f"WARNING: {script} exited with code {result.returncode}")

combined = {}
for fname in ["task1_commutant_results.json", "task2_e8_branching_results.json",
              "task3_yukawa_search_results.json"]:
    try:
        with open(fname) as f:
            combined[fname] = json.load(f)
    except FileNotFoundError:
        combined[fname] = None

with open("results.json", "w") as f:
    json.dump(combined, f, indent=2)

print("\n\n" + "=" * 72)
print("PHASE Z40 -- FINAL VERDICT")
print("=" * 72)
print("""
CLOSED:
  - Minimal single-triplet E8 flavon mechanism (phase_z39): confirmed
    equivalent to the pre-existing Z6-Z21 / Gresnigt degeneracy.
  - Factorization/commutant assumption behind Z21: independently
    reconfirmed, not merely carried over (Task 1).
  - Two-triplet same-rep outer product: rank 1, cannot hierarchy.

SURVIVES (representation-theoretically real, but costs back matching
freedom):
  - Conjugate-pair (3,3bar) sums at rank 3: needs as many independent
    flavon directions as an unconstrained Yukawa matrix has parameters.
  - Adjoint (1,8) flavon at rank 3: needs free potential coefficients.
  - The E8-Weyl-derived S3 (Task 2) as the one algebraically-selected
    discrete symmetry -- matches Gresnigt/Z22's S3 via an independent
    route, but known to cap at partial (not full) degeneracy lifting.

OPEN (needs tooling this environment lacks):
  - Task 5: genuine non-factorized H_generation subset of
    H_Cl(10) (x) H_E8. Untried from any angle. No claim made.

NEXT MINIMAL EXPERIMENT:
  Test whether applying the E8-Weyl S3 (Task 2) to a genuine Cl(10)xE8
  joint construction -- rather than Cl(10) alone, which is all Gresnigt
  and this project's own Z22 have tested -- changes Z22's symmetric-
  function degeneracy argument. Cheapest test that could distinguish
  "Cl(10)xE8 differs from Cl(10) alone" before attempting Task 5 in full.
""")
