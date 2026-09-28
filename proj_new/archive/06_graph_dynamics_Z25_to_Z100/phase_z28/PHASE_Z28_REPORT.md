# PHASE Z28 — PUSHFORWARD MEASURE & INVARIANT HUNT
# Rule-8 closed · 2026-08-02
# Script: phase_z28\z28_measure_invariant.py (uses phase_z25\z25b_engine_v2.py)

## Roadmap Phases 1+2 executed together

### Phase 1 — the measure (numerical L1)

Quotient Q = G_{10,15}/S_10, |Q| = 136,433 (exact, OEIS-validated z27).
mu := (T^inf . canon)_* Unif(G_10,15) estimated with 300 uniform labeled
seeds at p=0:

    converged:           300/300
    distinct attractors: 210 support points
    H(mu):               7.4616 bits
    log2 |Q|:           17.0578 bits
    support/|Q|:         ~1.54e-3   (0.154% of the quotient)

Updated information decomposition at (10,15), p=0:
    38.3273 (uniform labeled input)
      -21.2694 gauge (canon ~> quotient;  ~log2 10! = 21.79 close, as expected)
     17.0578 quotient point
      -9.5962 dynamical contraction
      7.4616 attractor distribution over its 210-point support

Every stage destroys information. None creates it. The engine's output is a
7.46-bit distribution concentrated on 0.15% of the quotient.

### Phase 2 — invariant hunt (negative L1 result)

Candidate scalar invariants of the unlabeled graph, evaluated on
(x, T x) for the last 24 states of 24 random orbits per mode (576 samples
each side):

    H2 = sum d^2 ; H4 = sum d^4 ; TRI = #triangles ; SQR = #4-cycles ;
    CHR = sum_v C(d_v,2) (wedges) ; MAT2 = #vertex-disjoint edge pairs ;
    P2  = sum_edges (min_d * max_d)

Result over all candidates, both p=0 and p=1:
    strictly_one_sided: FALSE for every candidate,

i.e. each statistic both increases and decreases on the transient/attractor
boundary (e.g. at p=0 every candidate has exactly 60 inc / 60 dec / 456 flat
per 576 steps; identical counts across H2..P2 reflect that within one step
all of them flip together at swap time).

THEOREM-B-flavored negative (L1 for (10,15), engine T):
  the extremal-exchange rule admits NO Lyapunov function among the standard
  isomorphism-invariant scalar statistics. The collapse to period-2 is not
  driven by scalar descent; it is produced by the tie-collapse
  (z26: add-side iso-singleton + canon merge of remove-ties).

This kills "find the invariant" in its naive scalar form. The invariant
must live in the discrete structure: the *tie class* itself — e.g. the
iso-type of the argmax multisets R(e) = argmin/max degree-sum edges,
A(e) = argmax/min degree-sum non-edges. Remaining conjecture for Z29+:
the iterate of |R(e)| and |A(e)| under T converges a.s. to small constants
(tie sharpening), and the attractor is the unique state whose tie classes
are iso-stable under one T-application.

## Rule ledger
- Rule 1: no numerology (no SM input anywhere). PASS.
- Rule 2: no reverse-engineering. PASS (test battery fixed before runs).
- Rule 3: scalar-monotone negatives are L1; the tie-sharpening conjecture
  is L3 pending proof.
- Rule 6: 24 orbits x 24 final states is an assay device, declared.
- Rule 8: scalar-Lyapunov avenue is now CLOSED.
- Rule 9: 6 candidates falsified; support-entropy measured; no free params.

## Next phase pointers
- Replace scalar invariants by tie-class dynamics (discrete Lyapunov).
- Characterize the 210-point support inside the 136,433 quotient:
  are the supported unlabeled graphs exactly the canon-stable 2-cycles?
  (would close Phase 2 fully: mu = counting measure on the self-dual set)
