# Phase R8 Dependency Graph

```
Phase A1 (existing, frozen)
  octonions O + structure constants (Fano plane)
  |
  |-- already used for: Cl(10) gammas, SU(3)_c/SU(2)_L generators (R7)
  |-- ALSO sufficient (derivable, not yet extracted) for: G2 = Der(O), 14-dim
  |
  X   <-- BOTTLENECK: nothing in this project builds the Jordan
  |       product (a o b = (ab+ba)/2) on 3x3 Hermitian octonionic
  |       matrices. This operation is not expressible in Cl(10)'s
  |       Clifford/CAR-algebra formalism; it is a genuinely different
  |       algebraic structure built on the SAME underlying octonions.
  |
  J3(O)  <-- MISSING: exceptional (Albert) Jordan algebra, 27-dim
  |          (must be newly constructed; uses Phase A1's octonions as
  |          raw material but needs the Jordan product, not present)
  |
  |-- F4 = Der(J3(O)), 52-dim         (follows automatically once J3(O) exists)
  |-- O0 (x) J3(O)0, 182-dim          (follows automatically: O0 already
  |                                    present, J3(O)0 follows from J3(O))
  |
  E8 = G2 (+) F4 (+) (O0 (x) J3(O)0) = 14 + 52 + 182 = 248
       (mechanical magic-square sum, no further new ingredients needed
       once J3(O) exists)

ALTERNATE EQUIVALENT ROUTES (same bottleneck, repackaged):
  J3(O) --> FTS(J3(O)), 56-dim (Tits' Freudenthal Triple System)
                --> E7 = Der(FTS) (+) FTS
                      --> E8 (one further grading step)
  J3(O)-data --> Kantor pair/triple system formulation (Truini)
                      --> same E8, different bookkeeping

DOWNSTREAM RISK (not this phase's question, flagged for later):
  E8 (once built) --> embedding SM gauge group + gravity + 3 chiral
                       generations into ONE copy of E8's adjoint
                       --> Distler-Garibaldi dimension bound
                           (-1 eigenspace <= 128-dim, need >= ~192)
                       --> known obstruction, applies regardless of
                           HOW E8 was constructed
```

**Single point of failure across every route: J3(O).** Every arrow
downstream of it is mechanical (definitional or direct-sum
bookkeeping); every arrow upstream of it (Phase A1's octonions) is
already present and frozen.
