# Z38 Task 1 — Hypothesis T1 ("codified space"), run + Rule 9 control

**Status: CLOSED, NEGATIVE. Rule 9 (discriminating power) fails.**

## What T1 claimed (`purposed_hypo_mechanism.md` §5)

> the twin-creation events carry an information fingerprint... the twins'
> identity in the quotient is *deterministic* — a mechanism "varies" in the
> clone set rather than exploring fundamentally. The identity counts as
> "codified space."

Stated gate: `H(token stream at jumps) < 0.8 * H(move entropy)` ⇒ T1-PASS ⇒
read as evidence the extremal rule `T` (`phase_z25/z25b_engine_v2.py`)
produces a non-arbitrary, "codified" symmetry-restructuring channel — one
plank in the broader (explicitly labeled UNFALSIFIED-STEREOTYPE)
space-definition hypothesis.

## What was actually done this session

1. `z38_hypo_step1.py` existed in the repo but had never been run here — it
   still had the original author's local Windows paths
   (`C:\Users\bisha\Desktop\...`) and no result file. Fixed the import path
   (`sys.path` relative to the file, matching the fix already applied
   elsewhere in the repo this session) and ran it for real.
2. **Result: T1 passes, strongly** — `T1_pass_share = 1.0` (31/31 and 30/30
   runs) at both tested cells, `ratio_mean` 0.446 at (10,15) and 0.412 at
   (12,18), both well under the 0.8 threshold.
3. Per `GROUND_RULES.md` Rule 9, before counting a passing gate as evidence,
   asked: *would this same gate have passed just as well under a process
   with no claimed mechanism at all?* Built `z38_hypo_step1_control.py`: same
   measurement pipeline, same two cells, but the rewrite step `T_random`
   replaces the real rule's degree-sum extremal selection with **uniform-
   random** edge removal and uniform-random non-edge addition — no ordering,
   no `p`-selector, no determinism of any kind.
4. **Control result: T1 also passes, at 100% share, with a *lower* ratio
   than the real rule** — 0.347 at (10,15), 0.311 at (12,18), vs. 0.446 /
   0.412 for the actual extremal dynamics.

## Why T1 fails Rule 9

`H_token` (entropy of the small, iso-invariant twin-partition-signature
alphabet at jump steps) and `H_move` (mean log2 of the candidate-move count
per step) are quantities of different type and different scale for
essentially any reasonable graph-rewrite process on N≈10-12 vertices: the
twin-signature alphabet is intrinsically small (a handful of integer
partitions of N), so `H_token` is bounded low almost by construction,
while `H_move` tracks a combinatorially larger candidate space and stays
high regardless of whether the *selection* among those candidates is
deterministic, extremal, or pure noise. The 0.8 threshold was never
calibrated against a null process before this session. Once it is, the
null process clears the gate *more* comfortably than the mechanism under
test — the textbook Rule 9 failure mode this project's own ground rules
warn about (identical in kind to Phase G's messenger-fix "rescuing" 100%
of 208 candidate triples, or Balmer's formula fitting hydrogen with no
mechanism).

**T1, as gated, provides zero evidence for "codified space" over
structureless random relaxation.** This does not touch F1/F2/H-2c
elsewhere in `purposed_hypo_mechanism.md` (untested), and does not reopen
or touch anything in the Z25–Z37 corpus, which used different, already
Rule-9-vetted measures (θ-Lyapunov, Burnside shell law, twin-channel share)
that this result leaves intact.

## Files

- `z38_hypo_step1.py` — original test, path bug fixed, now runs as shipped.
- `z38_hypo_step1_control.py` — new, the Rule 9 null control.
- Raw output of both: reproducible by running either file directly (no
  external dependencies beyond `phase_z25/z25b_engine_v2.py`).

## Honest next step, if anyone wants to keep pulling this thread

Not "raise the threshold until the control fails" (that's reverse-
engineering, Rule 2). A gate with real discriminating power on this
question would need to compare `H_token` against a quantity built from the
*same* alphabet under the null process — e.g., is the token *sequence*
(not just its entropy) more predictable one step ahead under rule `T` than
under `T_random`, via a proper next-token predictability test (empirical
conditional entropy `H(token_t+1 | token_t)` under each rule, compared
directly, same units, same alphabet). That test has not been run and would
be the correctly-scoped Z38 Task 2.
