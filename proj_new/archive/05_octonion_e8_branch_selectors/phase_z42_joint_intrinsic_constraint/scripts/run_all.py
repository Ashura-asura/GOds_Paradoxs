"""Run all Z42 scripts in dependency order, from a clean environment."""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = [
    "z42_representation.py",
    "z42_invariant_search.py",
    "z42_vacuum_analysis.py",
    "z42_freedom_count.py",
    "z42_no_go_test.py",
]

if __name__ == "__main__":
    for s in SCRIPTS:
        print(f"\n=== running {s} ===")
        r = subprocess.run([sys.executable, os.path.join(HERE, s)], cwd=HERE)
        if r.returncode != 0:
            print(f"FAILED at {s} -- stopping.")
            sys.exit(1)
    print("\nAll Z42 scripts completed and self-verified.")
