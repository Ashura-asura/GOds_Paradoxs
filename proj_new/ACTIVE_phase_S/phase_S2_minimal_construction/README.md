# Phase S2 — Minimal Construction

STATUS: NOT STARTED. Blocked on S1 being completed first (per MASTER_ROADMAP
gating rule). Do not write construction code until S1's four sections are
filled in for real.

## Objective once unblocked
Build the smallest possible version of S1's chosen construction:
  - Reuse the existing 32-dim Cl(10) machinery from
    `archive_pre_S/phases below_Z_25/phase_a1_cl10_core.py` if S1 chose
    option (a); do not jump straight to the full 248-dim E8.
  - Check the five axioms from S1 section 2, one at a time, in order of
    which is cheapest to falsify first (usually: KO-dimension signs, then
    grading/orientability, then reality, then first-order, then Poincare
    duality last -- it's typically the most expensive check).

## Gate to pass before moving to S3
One of these three, clearly written up:
  (a) All five axioms pass, uniquely, at N=3 (and only N=3) -- proceed to S3.
  (b) A specific axiom fails at N=3 or fails to select N=3 uniquely -- name
      which one, write up as a negative result, and STOP THE THREAD. This is
      a valid, complete, useful outcome per MASTER_ROADMAP.
  (c) The construction is underdetermined (multiple N values pass, or the
      axioms don't constrain N at all) -- name precisely what additional
      structure would be needed to break the degeneracy. This is also a
      valid stopping point, not a reason to keep adding ad hoc structure
      until something sticks.

## Explicit rule
Do not add complexity (moving from 32-dim to full 248-dim E8, or importing
additional structure not in S1's definition) to rescue a failing minimal
case. If the minimal case fails, that is the answer.
