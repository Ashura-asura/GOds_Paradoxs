# Ground Rules — Cl(10)×E8 → Standard Model Project

**Version 2, 2026-07-28.** Rules 1–8 are the project's original rules,
carried over unchanged in substance (only Rule 6 gets a clarifying note,
not a new requirement). Rule 9 is new. Nothing here is retroactive —
it doesn't change any phase's already-recorded result, it governs what
counts as valid going forward.

These rules outrank any individual phase's conclusions. If a future
phase's result and these rules conflict, the rules win and the phase
gets corrected, the way Phase M corrected Phase L.

---

### Rule 1 — No numerology
A match between two numbers is not evidence unless a stated mechanism
forces the match. If you can't say *why* the algebra produces this
number rather than a neighboring one, it's numerology, no matter how
suggestive the coincidence looks. (See Phase W, Category H/most of B/G,
for what "no mechanism" looks like in practice — dozens of true
arithmetic facts, zero explanatory content.)

### Rule 2 — No reverse-engineering
Parameters must be fixed *before* comparing to observation, or the
comparison is meaningless. If a value is chosen, scanned, or solved-for
specifically to make the output match a known experimental number, it
is fitted, not derived — regardless of how the fitting is dressed up
(a "VEV ratio," a "Clebsch coefficient," a "solved messenger charge").

### Rule 3 — Level labeling
Every claim gets one label:
- **L1** — proved from algebra alone, zero free parameters, forward-computed.
- **L2** — verified against real, cited literature or data, but not
  independently re-derived here.
- **L3** — conjecture, fitted, or dependent on an unproven assumption.

A claim keeps its true label even under pressure to round it up. Rounding
L3 up to L2 (or L2 up to L1) is the single most common failure mode this
project has caught in itself (see `adversarial_audit_2026.md`).

### Rule 4 — Adversarial audit always on
Every phase is written assuming a hostile, competent reviewer will check
it line by line — because, in this project's own history, one has. A
result that hasn't survived that scrutiny is provisional, not final.

### Rule 5 — Document failures
A structural failure is written down in the same place, with the same
prominence, as a success. Nothing gets quietly dropped when it stops
being convenient (`FINAL_AUDIT.md` and this file's own Phase W addendum
are the record of this rule being followed, including against this
project's own earlier drafts).

### Rule 6 — Zero free (continuous) parameters, with a discrete/continuous distinction made explicit
The original rule: nothing may be tuned to a real-number value to make
the output fit data. **Clarification, not a weakening:** this rule is
about *continuous* free parameters (masses, angles, couplings — anything
that could in principle take any real value and gets picked to match
observation). It does not forbid results that are *forced to be one of
finitely many discrete options* by an independent consistency condition
— "exactly 3 generations" from E8 branching is not a free parameter in
this sense, because no real number was chosen; a representation-theory
fact forced a specific integer. When recording a result, state explicitly
which kind it is. Conflating the two — presenting a scanned real number as
if it were a forced discrete fact — is a Rule 1/2 violation under a
different name.

### Rule 7 — One provable step at a time
Each phase builds on the previous one's actually-established results,
not on what a later phase hopes turns out to be true. No phase gets to
assume the success of a phase that hasn't been run yet.

### Rule 8 — Structural failure = result
A provably closed avenue is a real result, not a null one. "This route
cannot work, and here is the specific mechanism that blocks it" is
exactly as valuable, and gets recorded with exactly as much weight, as a
positive derivation. Most of Phases E–V and all of Phase W are Rule 8 in
action.

---

### Rule 9 — Discriminating power (new, 2026-07-28)

A mechanism that reproduces a known value only counts as an explanation
of that value if it would plausibly have *failed* to reproduce a wrong
one. Before accepting any construction — reverse-engineered or
otherwise — that matches a known number, ask:

> **Would this same mechanism have "explained" a different answer just
> as well?**

If yes, it has zero discriminating power and is a template, not a
derivation, regardless of how rigorous the machinery producing it looks.
This is not a new standard invented for this document — it is exactly
what Phase G already tested (the vector-like-messenger fix "rescues"
100% of 208 candidate charge triples tested, including ones that don't
match observation), stated here as an explicit, reusable rule so it gets
applied automatically to every future construction instead of being
rediscovered case by case.

**Worked distinction, for calibration:** Balmer's formula fit hydrogen's
known spectral lines with no mechanism — pure reverse-engineering, and by
itself it explains nothing (Rule 9 fails). Bohr's model explained *why*
the formula holds, and it passed Rule 9 the moment it predicted spectral
lines that hadn't been fit — the unobserved Lyman/Paschen series, and the
ionized-helium spectrum via the same constant rescaled by charge. The
test isn't whether reverse-engineering happened first (it almost always
does, historically) — it's whether what comes after has been checked for
the ability to have been wrong.

---

## How these rules are meant to be used

1. Before starting a new phase, state which of Rules 1–9 the phase is
   testing or is at risk of violating.
2. On completion, label every claim per Rule 3, and if the phase reverse-
   engineers anything (even provisionally, to explore a direction), run
   the Rule 9 check on it before writing a conclusion.
3. If a phase corrects an earlier one, the correction is filed as its own
   phase (Phase M correcting Phase L is the template), not as a silent
   edit to the earlier file.
