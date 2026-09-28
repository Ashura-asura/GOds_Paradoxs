# Z42 Audit Report

## Rule 1 — no numerology
No new numbers were fit. The branching table (Task 1) is a cited
standard result. The invariant classification (Task 2) is a cited
classical theorem, cross-checked numerically rather than fit. The
freedom count (Task 4) is dimension arithmetic (9 complex Yukawa
params, 10 physical target params per sector, 1 physical dof
delivered), not a fit to any experimental value — no SM mass, mixing
angle, or CKM/PMNS value appears anywhere in this phase's scripts or
results.

## Rule 3 — distinguish L1/L2/L3
- Task 1 (branching + dimension check): **L1**, exact integer
  arithmetic, assertion-gated.
- Task 2 (δ/ε invariance, generic-tensor failure): **L1** for the
  numerical checks themselves (machine/MC precision, explicit error
  values reported); the *general* FFT claim they support is a cited
  classical theorem, not re-proved here — labeled as such.
- Task 3 (potential is a function of `|φ|²` only; flatness of minimum):
  **L1** for the numerical minimization check; the general "no cubic
  invariant exists" claim rests on Task 2.
- Task 4 (freedom counting): **L1**, arithmetic, no fitted inputs.
- Task 5 (no-go theorem): **L2**, explicitly — stated as such in
  `z42_no_go_test.py`'s own output. Not claimed as a from-scratch
  machine-verified proof.

## Rule 9 — discriminating power
Task 5's theorem is not a restatement of Z39 (which covered one
invariant) or Z40 (which covered several concrete cases). It rules out
an entire infinite family at once — "any polynomial invariant of any
degree built from E8 structure constants, restricted to flavor
indices" — via the representation-content argument in Task 1 combined
with the classical FFT. This has discriminating power: it forecloses
an entire future search direction ("try a higher-order invariant") in
one step, rather than adding one more data point to a pattern.

## Honest failure/limitation log
- The Weyl FFT is cited, not machine-verified from scratch in this
  environment — flagged in every file that depends on it.
- Only the `E6 × SU(3)_f` branching was examined; other E8 maximal
  subgroups were not. This is a real gap, named explicitly, not
  glossed over.
- The non-factorized (NCG) route remains completely untested by this
  phase, as by every phase before it that has flagged it.
- Task 4's "10 physical parameters per sector" figure uses the
  standard SM parameter count (6 masses + 3 mixing angles + 1 phase);
  this is textbook, not derived in this repo, and is cited as such
  rather than presented as a novel result of this phase.

## Verdict
Z42 is recorded as **closed negative, generalized** — it does not
reverse any prior finding, and it does not open a materially new line
(per this phase's own instruction: "do not create another phase unless
Z42 reveals a genuinely new mathematical object or obstruction"). It
sharpens the existing obstruction from case-by-case to general, and
narrows the remaining open surface to exactly two named, already-
flagged escape routes.
