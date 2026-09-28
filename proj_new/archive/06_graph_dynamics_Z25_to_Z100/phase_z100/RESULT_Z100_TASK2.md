# Z100 Task 2 — "Aut jumps are caused primarily by twin restructuring"

**Status: Strict form FALSIFIED (expected — matches Z36's own prior finding).
Statistical form: real counterexample rate measured, density-dependent,
and quantitatively inconsistent with the repo's own headline 91–99%
twin-share number for the cells actually tested here. Flagged, not
silently reconciled.**

## What was tested

Candidate theorem, stated as a strict implication (per the audit prompt's
own wording): `ΔAut(G) > 0 ⇒ ΔTheta(G) > 0`, where `Theta = Σ C(|C_i|,2)`
over twin classes. Swept 9 (N,M) cells across sparse/medium/dense density,
15 seeds × 3 selectors (p=0,0.5,1.0) × 80 steps each, using the real
post-canon-fix engine (`phase_z25/z25b_engine_v2.py`, unmodified).

## Result

**Every cell produced counterexamples** — steps where `Aut` strictly
increased with `Theta` unchanged or decreased:

| cell | density | Aut jumps | counterexamples | non-twin share |
|---|---|---|---|---|
| N8,M8 | medium | 608 | 187 | 30.8% |
| N8,M10 | medium | 770 | 228 | 29.6% |
| N8,M17 | dense | 557 | 297 | 53.3% |
| N10,M10 | sparse | 614 | 169 | 27.5% |
| N10,M16 | medium | 603 | 186 | 30.8% |
| N10,M27 | dense | 590 | 165 | 28.0% |
| N12,M12 | sparse | 736 | 188 | 25.5% |
| N12,M23 | medium | 342 | 57 | 16.7% |
| N12,M40 | dense | 278 | 36 | 12.9% |

Sanity-checked before trusting any of this: `aut_size` verified against
four hand-known cases (K4→24, empty-4→24, one-edge-4→4, path-4→2, all
exact), and one saved counterexample was independently recomputed from
its raw edge lists from scratch, outside the sweep script, confirming
Aut 2→4 with Theta flat at 1.

## What this does and doesn't overturn

**Does not overturn anything new.** Z36 already found the strict/universal
form of this claim false (Shrikhande/Rook/Petersen: Theta=0 but Aut>1) and
already concluded a multi-channel decomposition (twin/quotient/component/
algebraic) is required. This result is an independent confirmation of that
same conclusion from a different angle (dynamical trajectories under `T`,
not static graph atlas lookups) — Rule 6 preference for counterexamples
satisfied, and it points the same direction the repo already pointed.

**Does flag something worth reconciling, not silently absorbing:**
`latest_progress_report.md` reports the twin channel carrying "91–99% of
jumps" (t4, Z37). The non-twin share measured here — 13% to 53% depending
on cell — is higher than that range in most of the 9 cells tested,
sometimes by a large margin (dense N8 cell: 53% non-twin vs. the reported
1–9%). Two honest candidate explanations, **neither confirmed here**:

1. `t4`'s 91–99% figure was measured on the project's specific canonical
   cells (e.g. (10,15), (16,32)) with the exact-|Aut| protocol and
   `INV`-keyed chains from `phase_z35`/`phase_z37`; this sweep used
   different, broader (N,M) cells chosen for density coverage, not
   matched to those canonical cells.
2. `Theta` here is computed from raw (uncolored) twin classes; Z36's own
   multi-channel decomposition (`|Aut(G)| = twin_aut × Aut(colored
   quotient) × component factor × algebraic residual`) implies some of
   what this script counts as "non-twin" is actually quotient-channel or
   component-channel Aut growth that a colored-quotient-aware Theta would
   correctly attribute — i.e., this measurement may be under-crediting
   the twin channel by using a cruder Theta than Z35/Z37 use, not
   over-crediting non-twin channels.

**This is not resolved here.** Re-running this exact sweep on the
project's own canonical cells with the project's own exact `INV`-keyed
Theta (not the raw twin-partition Theta used above) is the correctly
scoped next step before concluding anything quantitative — presenting
the discrepancy without that reconciliation would itself be a Rule 1/9
violation (comparing two differently-defined quantities and calling the
gap a finding).

## Files

- `z100_task2_twin_causality.py` — the sweep, reproducible, uses the
  unmodified `z25b_engine_v2.T` and `aut_size`.
- `z100_task2_counterexamples.json` — 18 saved raw counterexamples
  (edge lists before/after), independently spot-verifiable.
