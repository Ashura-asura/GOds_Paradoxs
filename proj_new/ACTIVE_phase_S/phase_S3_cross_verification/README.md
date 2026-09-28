# Phase S3 — Independent Cross-Verification

STATUS: NOT STARTED. Blocked on S2 producing a result (positive, negative,
or underdetermined -- all three get cross-verified, not just positives).

## What to carry forward from the archived project
The archived work (`archive_pre_S/session_new_files/phase_z23_external_session/
tmp_task_c_sage_crosscheck.py` and similar files) already establishes the
right method: exact rational arithmetic (Fraction/sympy, not floating point)
for anything algebraic, cross-checked in a second independent tool (Sage/LiE
against custom implementation), and Monte Carlo only where exact methods
aren't tractable. Keep doing exactly that. This part of the prior process was
genuinely solid -- do not weaken it.

## Task
Every claim produced in S2 gets reproduced independently:
  - Algebraic claims (root systems, branching rules, invariant rings): exact
    arithmetic, second tool, exact agreement required.
  - Numerical claims where exact methods aren't tractable: Monte Carlo,
    report the sample size and tolerance explicitly, do not present a
    Monte-Carlo check as if it were a proof of completeness (it can show an
    invariant IS invariant; it cannot show a set of invariants is ALL of them
    -- that direction needs a cited theorem, as Z42 correctly did with Weyl's
    FFT).

## Gate to pass before moving to S4
No disagreement between the two independent computations left unresolved.
A disagreement is not something to log and defer -- resolve it before
proceeding, even if that means going back to S2.
