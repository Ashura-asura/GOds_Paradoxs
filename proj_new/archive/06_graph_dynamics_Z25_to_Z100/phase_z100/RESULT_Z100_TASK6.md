# Z100 Task 6 — Burnside shell law

**Status: Step 1 (the exact algebraic identity) independently CONFIRMED, L1.
Step 2 (does the dynamics follow it) — inconclusive at the N tested, for a
specific, stated reason (chain absorption), not a clean pass or fail.**

## Step 1 — the Burnside/orbit-stabilizer duality itself

Claim under test (t6, `latest_progress_report.md`): "σ_q == σ_a exactly
(uniform-over-orbits = Aut-weighted labeled, Burnside duality)."

**My first attempt at coding this independently was wrong twice, and I'm
recording both mistakes rather than only the fixed version:**

1. First bug: I tested `Σ 1/Aut(G) = n_classes`. Wrong identity — orbit
   size is `N!/Aut(G)` (orbit–stabilizer, with `Stab(G) = Aut(G)` under the
   `S_N` relabeling action), so the correct identity is `Σ Aut(G)/N! =
   n_classes`, not `Σ 1/Aut(G)`. Caught because the numbers weren't even
   close (off by factors in the thousands).
2. Second bug, after fixing the formula: still failed, with per-class
   automorphism-mass values like 14400 and 86400 instead of the expected
   constant `N!`. Cause: `eng.aut_size()` reads a module-level global
   `eng.N` rather than taking N as an argument, and I never set it before
   calling it in this function — so it silently reused whatever `N` a
   previous call had left behind (10, the module's default) while
   permuting 5- and 6-vertex graphs. `14400 = 120²` was the tell.

**After both fixes, exact on all 4 tested cells** ((5,4), (5,6), (6,6),
(6,8)): `Σ Aut(G)/N!` equals `n_classes` exactly (6, 6, 21, 24 — floating
point exact, not approximate), and every single isomorphism class's total
automorphism mass equals `N!` exactly (120 or 720, verified per-class, not
just in aggregate). This is a real, independent, from-scratch confirmation
of the exact mathematical fact `t6` is built on — not a re-run of their
code, a from-scratch brute-force `N!`-canonicalization computation of my
own doing the same check by a different route.

## Step 2 — does the actual T-dynamics follow any of the three laws?

Tested three candidate measures against the empirical visited-state
distribution (3000 steps, 200 burn-in, at each of the 4 cells above,
p=0 and p=1):
- uniform-labeled: `P(G) ∝ 1`
- uniform-quotient: `P(class) ∝ 1`
- Aut-weighted: `P(G) ∝ Aut(G)` (equivalent to uniform-quotient by Step 1's
  identity, restated at the labeled-graph level)

**Result: total-variation distance to all three laws is large (0.48–0.98)
and does not consistently favor Aut-weighted over the other two** — in 3 of
8 runs Aut-weighted has the *worst* fit of the three, not the best.

**Why, honestly:** at these small N, the post-burn-in empirical
distribution is almost totally absorbed into 1–2 isomorphism classes out
of the 6–24 available (e.g. N5,M4,p=0: single class gets all 2800 visits).
The chain isn't mixing enough at this N/step count for a TV-distance
comparison against any smooth "law" to mean much — it's comparing a
near-point-mass to three smooth distributions, and which one it happens to
be closer to is largely which class it got trapped in, not evidence about
which law governs the dynamics in general.

**This is consistent with, not a clean re-derivation of,** the corpus's
own already-recorded finding (`latest_progress_report.md` §5, t6: "dynamics
vs law TV=0.70–0.86 → dynamics does NOT sample the law, it over-selects the
max-Aut shell"). My numbers are noisier and in a wider range because of
much smaller N (5–6 vs. their N=10–24) and a single seed per cell rather
than their full protocol — this is a directionally-consistent sanity check,
not an independent re-derivation of their specific TV numbers.

## Honest bottom line

- **Real, new, independently-verified result:** the exact orbit-counting
  identity underlying `t6` is correct — checked from scratch, bugs and all,
  not assumed.
- **Not a new result on whether dynamics follows the law:** the small-N
  test here is too close to chain-absorption to add information beyond
  what the corpus's own larger-N protocol already established. Extending
  this to N≥10 with the corpus's actual multi-seed protocol (not attempted
  here — computationally heavier, needs the real `phase_z35`-style exact-
  |Aut| harness rather than this session's brute-force `N!` canon) would be
  the correctly-scoped next step, not a small-N rerun with more seeds.

## Files

- `z100_task6_burnside_shell.py` — both steps, reproducible, bug fixes
  left visible in the code comments rather than silently removed.
- `z100_task6_results.json` — raw output of both steps, all 4 cells.
