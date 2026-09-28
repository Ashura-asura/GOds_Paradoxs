"""
Drop this file in the kimi_Gods_paradox repo root (same folder as GROUND_RULES.md,
alongside phase_z25/, phase_z26/, ... phase_z37/).

Fixes the two path problems in this repo's scripts:
  1. Hardcoded absolute paths baked to one machine/username
     (e.g. a raw string literal of the full original Windows folder path),
     which break the moment the folder is moved, renamed, or opened on a
     different machine.
  2. Bare relative paths (e.g. "phase_z25"), which only resolve correctly if
     Python happens to be launched with the repo root as the current working
     directory -- breaks if you `cd` into a phase_z* folder and run the
     script from there, or run it from an IDE with a different cwd.

Usage -- add this as the FIRST import, before any phase_z* module import,
in any script:

    import pathfix        # must come before "import z25b_engine_v2" etc.
    import z25b_engine_v2 as E
    ...

What it does: finds its own location on disk (which is reliable regardless
of cwd), then inserts every phase_z*/ and support-style subfolder it finds
next to itself onto sys.path, deduplicated, so every script's imports
resolve the same way no matter where you launch python from or where the
repo folder lives.
"""
import sys, os, glob

_ROOT = os.path.dirname(os.path.abspath(__file__))

def _add(p):
    p = os.path.abspath(p)
    if p not in sys.path:
        sys.path.insert(0, p)

# repo root itself (for top-level helper modules, if any)
_add(_ROOT)

# every phase_z* directory found next to this file
for d in sorted(glob.glob(os.path.join(_ROOT, "phase_z*"))):
    if os.path.isdir(d):
        _add(d)

# a couple of other conventional subfolders some scripts expect on path
for name in ("support", "session_new_files"):
    d = os.path.join(_ROOT, name)
    if os.path.isdir(d):
        _add(d)

RESULTS_DIR = os.path.join(_ROOT, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)
