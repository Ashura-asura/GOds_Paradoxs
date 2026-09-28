# RESULT: Task G — E6xSU(3)_f anomaly/consistency of the (27,3) family assignment

Status: CLOSED (L1, exact arithmetic on explicit generators)
Ground rules: Rule 3 (L1), Rule 6 (no free parameters), Rule 8 (structural failure = result),
Rule 9 (discriminating power check below)
Date: 2026-08-02 (Phase Z23 external session, after Task F)

## 1. Question
Task C established E8 -> E6xA2: 248 = (78,1) + (1,8) + (27,3) + (27bar,3bar), i.e. the
three-generation content sits in the (27,3) piece (one 27 per A2-fundamental "family 3").
Task: anomaly/consistency check of this (27,3) family assignment: (a) is a standalone
chiral E6xSU(3)_f theory with content (27,3) consistent? (b) is the actual E8-adjoint
content (27,3) + (27bar,3bar) consistent in every channel? (c) is each generation
anomaly-free at the SO(10) level (16bar), so that "exactly 3" is anomaly-safe?

## 2. Method (from first principles, exact)
Explicit matrix generators with sympy exact Rational arithmetic (tmp_task_g_anomalies.py):
  - SU(5) defining rep (24 generators, Tr-normalized basis), the 10 = Lambda^2(5)
    (10x10 antisymmetric-square matrices), the 5bar (conjugate rep: generators -(t^a)*),
    SU(3) fundamental (8 generators).
  - Cubic anomaly coefficient d^{abc}_R = (1/4) Tr_R({t^a,t^b} t^c); ratios of the tensor
    at fixed nonzero triples are basis-independent, so all coefficients below are exact.
  - A(3 of SU(3)) = 1 (normalization); everything else in A(5 of SU(5)) units.

## 3. Results
  A(10)/A(5)  = +1        (2-index antisymmetric of SU(5))
  A(5bar)/A(5)= -1        (conjugate)
  A(adjoint)  = 0         (adjoint of any group is anomaly-free; spot-checked)
  A(16 of SO(10)) via verified Task E content 16 -> 1 + 10 + 5bar:  = 0 - 1 + 1 = 0  EXACT
  A(27 of E6) via verified Task D+E content
      27 -> 1(-4) + 16bar(-1) + 10(2);  16bar -> 1 + 10bar + 5bar;  10 -> 5 + 5bar
      => 27|su(5) = 3*1 + 10bar + 5 + 2*5bar:
      A(27) = -A(10) + A(5) + 2*A(5bar) = -1 + 1 - 2 = -2   != 0   (E6 27 is genuinely anomalous)

## 4. Channel-by-channel table (exact)
  Content 1: chiral-only (27,3) [three generations, family index gauged, no conjugates]
    E6^3        : 3 * A(27)          = -6    != 0   FAIL
    SU(3)_f^3   : 27 * A(3)          =  27   != 0   FAIL
    E6^2 x f    : Tr_27(t t) Tr_3(T) = 0 (Tr_3(T) = 0, traceless)            OK
    E6 x f^2    : Tr_27(t)  Tr_3(TT) = 0 (Tr_27(t) = 0, traceless)           OK
    grav channels: 0                                                          OK
  => a standalone chiral E6xSU(3)_f GUT with only (27,3) is EXCLUDED (two pure-cubic
     anomalies cannot be canceled by any adjustment; no mixed anomaly to rescue it).

  Content 2: actual E8-adjoint content (27,3) + (27bar,3bar) [+ (78,1), (1,8) adjoints]
    E6^3        : 3*A(27) + 3*A(27bar) = 0                                   OK
    SU(3)_f^3   : 27*A(3) + 27*A(3bar)  = 0                                   OK
    E6^2 x f, E6 x f^2, grav: all 0 via tracelessness                        OK
  => the E8-adjoint content is anomaly-free in EVERY channel. This is forced by the
     vector-like completion (27bar,3bar) which is ALREADY present in the 248
     (Task C) — no extra matter required. Expected (adjoint of E8 is real), now
     verified channel by channel with explicit coefficients.

  Content 3: per generation at SO(10) level: A(16bar) = 0 (A(16) computed exactly).
  => "exactly 3 generations" is anomaly-safe at every level of the chain
     E8 -> E6xA2 -> [E6 -> SO(10)xU(1)]: each 16bar is individually anomaly-free, so
     no cancellation between generations is needed.

## 5. Rule 9 — discriminating power
  Tested claim: "(27,3) is the three-generation assignment".
  Discriminates: chiral-only (27,3) [FAILS: E6^3 = -6, SU(3)_f^3 = 27] vs
  E8-adjoint (27,3)+(27bar,3bar) [PASSES all channels]. Both numbers are exact
  (no fitting, Rule 6). Also: A(27) != 0 proves E6's 27 is complex-anomalous,
  killing any claim that a chiral 27-only model is automatically safe.

## 6. Verdict
  The (27,3) family assignment is consistent if and only if the conjugate sector
  (27bar,3bar) is present — which it is, in the E8 adjoint (Task C). The three
  generations themselves are anomaly-free per generation (A(16bar) = 0), so the
  "3" requires no exotic cancellations. A standalone chiral (27,3) E6xSU(3)_f GUT
  is structurally excluded (Rule 8: structural failure = result, documented).
  No new physics; consistency confirmed for the E8-embedded picture.

## Files
  - tmp_task_g_anomalies.py (sympy exact; all checks passed)
