# Phase S1 — Precise Claim Formalization

STATUS: NOT STARTED. This is real mathematical work that has not been done.
This file is a template/checklist, not a result.

## Gate to pass before moving to S2
You must be able to state, in one sentence, an observation that would refute
the claim -- before writing any construction code.

## Required sections (fill in for real, do not skip)

### 1. Exact definition of "Cl(10)/octonion/E8 data"
Pick ONE concrete recipe. Candidates already implicit in the archived work:
  (a) The 32-dim Fock space from phase_a1_cl10_core.py, with its Witt-pair
      structure, taken as the Hilbert space H directly.
  (b) The 27-dim J3(O) Albert algebra (not yet built anywhere in the archive
      per R8's own audit -- would need to be constructed first).
  (c) Something else -- state it precisely.
Do not leave this as "we'll figure out which as we go." Pick one. If S2
suggests a different choice works better, that is a new S1, not a patch to S2.

### 2. Exact statement of each of the five axioms, in terms of (1)'s objects
- Reality (J^2 = 1)
- First-order condition
- Orientability (grading gamma)
- Poincare duality
- KO-dimension 6 (epsilon, epsilon', epsilon'' = (1,1,-1))
Write each as a checkable equation on the specific H, A, D, J, gamma from (1),
not as prose.

### 3. What "N_g" means concretely in this construction
In Chamseddine-Connes, N_g is a literal tensor-product multiplicity bolted on
by hand. In this construction, where does the analogous multiplicity live?
Name the specific subspace or index. If you cannot name it precisely, you are
not ready for S2 -- this is usually where circularity sneaks in (see S4).

### 4. Falsifiability statement
One sentence: "This claim is false if ___."

## Explicit warning carried over from this thread's audit
Do not let N=3 enter through the back door via which representations you
choose to keep, discard, or label as "the SM sector." That is the single most
common failure mode in this literature (see S0 table, Boyle 2020 caveat).
