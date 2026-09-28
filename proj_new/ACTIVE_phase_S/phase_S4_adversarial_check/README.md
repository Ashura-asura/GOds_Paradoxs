# Phase S4 — Adversarial Self-Check

STATUS: NOT STARTED. Blocked on S3. Only meaningful if S2/S3 produced a
POSITIVE result -- a negative or underdetermined S2 result should already
have stopped the thread per S2's gate.

## Objective
Spend at least as long trying to break the S2/S3 positive result as was
spent building it. Write a real answer, not a checklist tick, for each item.

## The four failure modes (carried over from this thread's O3 audit)

### Failure Mode 1 -- chosen, not derived
Did N_g=3 emerge because SU(3)_f (or whatever family structure) was chosen
with dimension 3 going in? Trace every place a "3" appears in S1's
construction and check whether it was assumed anywhere before the axioms
were applied.

### Failure Mode 2 -- representation-label coincidence
Does the result just relabel "(16,3) has a 3 in it" as if that were a
derivation? A representation label matching the target number is not the
same as the axioms excluding other numbers.

### Failure Mode 3 -- non-dynamical triality
If triality is doing any work in the construction: does it provide an actual
operator/constraint, or just three objects that happen to exist
mathematically? ("Three colors exist" is not "three particle generations.")
This is exactly where Boyle 2020/2026 (see S0) stops short -- check whether
S2's construction has actually gone further than that paper or just
reproduced its same suggestive-but-unproven step.

### Failure Mode 4 -- residual family symmetry
After the construction, is there still an unbroken GL(3) or U(3) acting on
the generation index? If so, the axioms haven't actually distinguished N=3
from N=anything -- they've just picked a convenient representation of a
still-unconstrained symmetry.

## Gate to pass before moving to S5
Written answer to "how would I convince myself this is wrong" for each of
the four modes above -- not just "checked, doesn't apply." If any answer is
weak, that is itself the result -- write it up as the actual finding and
reconsider whether S5 is warranted yet.
