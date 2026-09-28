# Z35 Control D — Pre-registration (Rule-2, declared BEFORE any run)

**Date:** 2026-08-03
**Phase:** phase_z35, post-hoc Control D for the exact-|Aut| jump framework
**Motivation:** Z36 (standalone) found twin-free algebraic graphs (Shrikhande Theta=0,
|Aut|=192; Rook 1152; Petersen 120; complement-Shrikhande 192) with high |Aut| and NO twin
channel. Z35's mechanism says |Aut| jumps in the extremal framework are twin-mediated
(P(dt<0|J)=0.000; H1 pass). Control D asks: **do twin-free algebraic seeds nucleate |Aut|
jumps under the same exact-|Aut| extremal protocol, and are any such jumps twin-mediated?**

## Protocol (fixed before runs)

- Seeds (fixed graphs, not sampled; each verified Theta=0, |Aut| exact):
  - `shrikhande`   N=16 M=48, |Aut|=192
  - `rook`         N=16 M=48, |Aut|=1152
  - `comp_shrikh`  N=16 M=72 (complement of Shrikhande), |Aut|=192
  - `petersen`     N=10 M=15, |Aut|=120
- Selectors: random (50 chains/seed), lex (1 chain/seed), entropy (1 chain/seed),
  autmin (1 chain/seed). Deterministic selectors = 1 chain each (deterministic given seed).
- Cap: CAP_D = 256 steps (converged = canon-key cycle within cap; else recorded capped).
- RNG: same formula as main protocol, `random.Random(SEED0 + 131*s + 991*len(mode))`, s per
  chain within a seed.
- Per step: |Aut| via Amendment-3 v2 counter (aut_size_exact_v2), cache enabled; Theta via
  twin_potential; jump = a1 >= 4.0 * a0 (JUMP_RATIO, identical to main protocol).
- Amendment-4 patch applied (z33 autmin candidate evaluation -> v2 counter) so autmin chains
  are bit-identical to the main protocol's autmin.
- Theta(seed)=0 and |Aut|(seed) are asserted at t=0 for every chain (fail-fast if violated).

## Hypotheses / gates (decided before runs)

- **G1** (jump nucleation): P(jump at first step t=0 | all chains) <= 0.05.
  Twin-free algebraic seeds do NOT nucleate |Aut| jumps in the first exchange.
- **G2** (twin mediation): P(any step with jump and dtheta <= 0) <= 0.05 across all chains.
  If a jump ever occurs, it coincides with Theta increase (same claim as main cell's
  P(dt<0|J)=0.000).
- **G3** (measurement, no gate): median and distribution of tau_first = first step with
  Theta>0 (does extremal dynamics create twins from SRG seeds?), and tau_half = first step
  with |Aut| <= |Aut|_0/2 (decay of algebraic symmetry), per seed and selector.
- **G4** (measurement, no gate): chain endpoint stats — P(end Theta=0), median end |Aut|,
  P(chain reaches |Aut|=1 at some point).

## Decision (pre-registered)

- PASS: G1 and G2 hold -> twin channel is the only jump channel in the extremal framework;
  algebraic symmetry does not generate |Aut| jumps there; Z35 outcome B unchanged (Control D
  recorded as a strengthening fact, ledger entry).
- FAIL on G1 or G2 -> mechanism claim needs revision: jumps at Theta=0 exist and/or jumps
  can occur without Theta increase; report the numbers honestly and reassess outcome B.

## Outputs

- `phase_z35/z35_control_d.py` (harness, pre-registration embedded in this file's docstring
  header in spirit; full text here)
- `phase_z35/z35_control_d_results.json` (per-chain records + aggregates)
- L1 table + L2 note + ledger 8.12 in `PHASE_Z35_REPORT.md`
