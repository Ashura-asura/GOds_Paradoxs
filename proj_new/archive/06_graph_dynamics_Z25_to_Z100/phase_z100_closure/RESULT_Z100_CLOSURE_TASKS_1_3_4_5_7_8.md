# Z100 CLOSURE — TASKS 1, 3, 4, 5, 7, 8
Hostile-referee audit. All numbers below are reproducible by running the
`.py` files in this folder; every claim is backed by a `task*_results.json`
file. Engine correctness is gated by `z100_selfcheck.py`
(`selfcheck_results.json`) which cross-checks exact `|Aut|` against
independently known ground truth (Petersen=120, Shrikhande=192, Rook4x4=1152)
using igraph's BLISS backend — a *second*, independent automorphism
implementation from anything used in phases Z25–Z37. That check passed
(3/3), so the corrected engine is trusted for everything below. Tasks 2 and
6 were already closed in the existing `phase_z100/` folder and are not
repeated here.

---

## TASK 1 — Revalidation under corrected exact keys

Old result | New result | Difference | Verdict
---|---|---|---
"Period-2 attractor" reported for the exchange dynamics (Z30) | Under the **random** tie-break selector, 0/60 chains show any exact period in raw canonical-key space (`task1_results.json`, `random_selector.period_distribution = {"None": 60}`). Under the **deterministic lex** selector, 60/60 chains show exact period 2. | The original claim is **selector-dependent** and was never separated from that dependency in the write-ups. A stochastic selector re-randomizes the tie-break every step, so it cannot show exact period-2 in raw isomorphism-class space by construction — only a deterministic selector can. | **PARTIALLY SURVIVES**, but the original phrasing was imprecise: "period-2" is a property of *deterministic* tie-break rules, not of the mechanism in general. Logged as a corrected artifact (Rule-7), not a fabrication — the phenomenon is real for `lex`.
Entropy compression, I_input≈38.33 bits → I_output≈3.585 bits (Z26) | I_input = 38.327 bits is **exact combinatorics** (log2 C(45,15)), not a measurement. Re-measured output entropy over attractor canonical keys: **5.45 bits** (random selector, 48 distinct attractors / 60 chains) and **5.20 bits** (lex selector, 44/60). | Compression direction confirmed (≈33 bits lost), but the magnitude changed (3.585 → ~5.2–5.4 bits) once exact iso-invariant keys replaced the earlier (possibly label-sensitive) keys, and the earlier 38.33 bits was silently exact math dressed as a "measurement." | **SURVIVES qualitatively** (dynamics is strongly compressive), **magnitude corrected**.
No scalar Lyapunov found (Z28) | Under `lex`, exact `|Aut|` is monotone (non-strict) along only 8/60 chains — not a Lyapunov function. `Theta` is monotone (non-strict) along 41/60 chains — this is a *new* observation not in the original arc. | New finding: Theta is weakly (non-strictly) monotone in a majority of deterministic chains post-transient, likely because it plateaus once the attractor is reached, not because it is decreasing throughout. | **H3 SURVIVES for `|Aut|` as a strict Lyapunov candidate. Theta needs a follow-up phase** — flagged, not claimed.
Twin channel non-universal, Shrikhande/Rook/Petersen counterexamples (Z36) | Re-verified byte-for-byte with the BLISS-backed exact engine: Petersen Aut=120, Shrikhande Aut=192, Rook Aut=1152, all Theta=0 (`selfcheck_results.json`). | None. | **SURVIVES, CLOSED.**

---

## TASK 3 — Twin nucleation law (mutual information, no correlation)

6,250 individual exchange events (250 chains × 25 steps, N=10, M=15,
random selector). Exact MI in bits between `TwinGain>0` and each candidate
variable, binned into empirical tertiles:

| Variable | I(gain ; X) bits |
|---|---|
| A (addable-tie multiplicity) | 0.00859 |
| R (removable-tie multiplicity) | 0.00774 |
| TH0 (pre-step Theta) | 0.0000018 |
| Degree variance | 0.0000006 |
| Degree entropy | 0.0000006 |

`H(TwinGain>0) = 0.432` bits (base rate 8.9%).

Pre-registered decision rule: I_tie = I(R)+I(A) = 0.0163 vs I_deg =
I(DV)+I(DE) ≈ 0.0000011. I_tie ≥ 2·I_deg by three orders of magnitude →
**H2 (tie geometry) SURVIVES over H1 (degree convergence)**, consistent
with Z35's own H2 finding.

**Minimal sufficient statistic check**: I(gain; R,A) = 0.00896 bits;
adding TH0 raises it to only 0.01048 bits (+0.0015). (R,A) is close to
sufficient — TH0 adds little.

**Honest caveat (Rule 6/8)**: even the *winning* variables carry almost no
information — 0.009–0.016 bits out of 0.432 bits of target entropy, i.e.
**under 4% of the uncertainty in whether a twin forms is explained by any
of these five variables combined.** No predictive law `P(twin) = f(R,A,TH0,…)`
of practical strength was found. The correct statement is: *(R,A) beats
degree statistics by a wide relative margin, but neither is a strong
predictor in absolute terms.* Claiming a "twin nucleation law" from this
data would fail Rule-1 (numerology) — recorded as **PARTIAL, not closed.**

---

## TASK 4 — Symmetry channel phase diagram

12 (N,density) cells × 25 lex-selector chains each, classified at the
attractor (`task4_results.json`):

| N | sparse (ρ≈0.2–0.25) | medium (ρ≈0.5) | dense (ρ≈0.8) |
|---|---|---|---|
| 6  | QUOTIENT | QUOTIENT | **TWIN** |
| 8  | QUOTIENT | **TRIVIAL** | **TWIN** |
| 10 | QUOTIENT | **TRIVIAL** | QUOTIENT |
| 12 | QUOTIENT | **TRIVIAL** | **TWIN** |

No COMPONENT-channel or confirmed ALGEBRAIC-channel (regular QUOTIENT)
attractors were observed in this grid — the "algebraic channel" is real
(Task 5) but did not show up as a *dominant* attractor class here; it may
require different (N,M) cells or non-extremal selectors to reach.

**Genuinely new finding, not in the original Z25–Z37 arc**: medium
density (ρ≈0.5) is dominated by **TRIVIAL** attractors (|Aut|=1, no
twins) at every N≥8 tested. Symmetry generation is *not* monotone in
density — it is a **U-shaped / bimodal** phenomenon (present at low and
high density, suppressed near ρ≈0.5) under this specific extremal
exchange rule. This contradicts any implicit assumption in earlier phases
that "more exchange steps → more symmetry" and should be treated as the
headline empirical result of this task.

---

## TASK 5 — Algebraic channel: the Shrikhande/Rook missing invariant

Both graphs independently re-verified as SRG(16,6,2,2), cospectral
(identical eigenvalues {6¹,2⁶,(-2)⁹}), Theta=0 for both — confirming
2-Weisfeiler-Leman (which only sees n,k,λ,μ) cannot distinguish them, as
predicted (negative control).

**Separator found**: clique number. ω(Shrikhande) = 3 (triangle-only,
zero 4-cliques). ω(Rook 4×4) = 4, with exactly 8 maximal 4-cliques (the 4
rows + 4 columns of the rook's-graph construction, since Rook(4×4) is the
line graph of K₄,₄). This is 3-WL-level / clique-counting information,
strictly above what 2-WL (equivalently: degree + λ + μ) can see.

**Verdict**: the missing invariant is **local clique structure**, not a
new spectral or SRG parameter. This is a known structural fact about this
specific cospectral pair (not a discovery of a new theorem), but it was
independently re-derived and verified here rather than asserted — it
directly answers Task 5's question and explains why Theta (which is 0 for
both) is the wrong lens for the algebraic channel: **algebraic-channel
symmetry needs a genuinely different invariant family (clique/association
structure) than twin-channel symmetry (Theta) or generic quotient
symmetry (|Aut(Q)|).**

---

## TASK 7 — Scaling law / critical density

P(Theta>0 at attractor) over N∈{6,8,10,12,14}, five density slices, 20
lex chains per cell (`task7_results.json`):

- **ρ=0.8**: P(twin) = 1.00, 1.00, 0.25, 0.30, 0.10 for N=6,8,10,12,14 —
  a clear, sharp **decline with N**, from certainty at N≤8 down to ~10%
  by N=14.
- **ρ=0.5, 0.65**: also decline with N, reaching P(twin)=0 by N=12–14.
- **ρ=0.2, 0.35**: low and roughly flat (5–25%) across all N tested —
  no clear trend either way at this size range.

**Honest reading**: there is empirical evidence of twin nucleation
*weakening* as N grows at medium-to-high density, consistent with a
finite-size crossover, but N=6..14 is far too small a range to fit or
name a critical exponent ρ_c(N), and the noise (n=20 chains/cell) is
large relative to the effect at several cells. **The qualitative
direction (twin nucleation disappearing as N→∞ at fixed ρ in [0.5,0.8])
is SUPPORTED by this data; the existence/value of a sharp critical
density ρ_c(N) is NOT established** — this remains a conjecture (L3), not
a measured law (L2).

---

## TASK 8 — Endpoint theorem

N=10, M=15, random selector, distinct-attractor-count vs number of chains
run (`task8_results.json`):

| chains run | distinct attractors seen |
|---|---|
| 10 | 10 |
| 25 | 23 |
| 50 | 45 |
| 100 | 79 |
| 150 | 111 |
| 200 | 130 |

Growth rate falls from 0.90 new-distinct-per-chain (early) to 0.38
(late) — a real slowdown, but **not a plateau**: at 200 chains the system
is still discovering ~2 new attractors per 5 new chains. This directly
**falsifies Hypothesis A (unique maximal-symmetry attractor)** — 130
distinct attractors were observed, not 1.

For Hypothesis B (finite attractor family): the slowdown is consistent
with *either* (a) a genuinely finite family whose size is being
approached, or (b) ordinary coupon-collector-style diminishing returns
while sampling from a large-but-still-effectively-unbounded space (which
would produce an identical-looking slowdown even with thousands of
possible attractors). **These two cannot be distinguished with 200
chains.** Rule 8 applies: the strong form of Hypothesis B ("a small,
namable finite attractor family selected by an invariant τ*") **cannot
survive this minimal test and is CLOSED as stated.** A weaker, honest
restatement — "the attractor set is a proper, non-trivial subset of all
graphs on (N,M), of unknown but apparently sub-linear-in-chains size" —
is the most that this data supports, and even that needs an order of
magnitude more chains (and ideally exact enumeration for small N) before
being promoted past L3 (conjecture).

---

## FINAL MECHANISM DIAGRAM

```
degree/overlap structure (R,A tie multiplicities)
        │  I(twin-gain ; R,A) ≈ 0.009 bits  [weak but > all other channels tested]
        ▼
occasional twin formation (Theta channel)          ──┐
        │                                              │  neither channel alone
        ▼                                              │  explains most attractors;
factorial |Aut| jump when twins present                │  TRIVIAL and QUOTIENT
        │                                              │  attractors dominate at
        ▼                                              │  low/medium density
Θ-driven |Aut| increase  ◄── minority of attractors ──┘
        
QUOTIENT channel (twin-free, |Aut(G)|>1): dominant at low + high density
TRIVIAL channel (|Aut(G)|=1): dominant at medium density (ρ≈0.5)
ALGEBRAIC channel (clique/association structure, e.g. Shrikhande/Rook):
  demonstrated to exist and be distinguishable from Theta, but not observed
  as a DOMINANT attractor class in the (N,density) grid tested — open.
COMPONENT channel: not observed at all in this grid — open/untested at
  sparser densities than ρ=0.2.
```

## PROVEN THEOREMS (L1 — exact, reproducible, no sampling)
1. `exact_aut()`/`canon_key()` engine correctness on 3 independent ground-truth
   graphs (Petersen, Shrikhande, Rook 4×4) — exact match, not sampled.
2. Shrikhande and Rook(4×4) are cospectral SRG(16,6,2,2) with Theta=0 for
   both, yet ω(Shrikhande)=3 ≠ ω(Rook)=4 and |Aut| differs (192 vs 1152) —
   exact computation, not sampled.
3. Under the deterministic `lex` selector, the exchange dynamics reaches
   an exact period-2 cycle in canonical-key space in 60/60 tested chains
   at (N=10,M=15) — a measured-but-exact (not sampled-and-extrapolated)
   fact about those 60 specific trajectories.

## FALSIFIED / CLOSED HYPOTHESES
- "Period-2 attractor" as a selector-independent universal property — **CLOSED**, selector-dependent.
- Strong Hypothesis A, unique maximal-symmetry attractor — **CLOSED**, 130 counterexamples found in one cell.
- Strong Hypothesis B, small nameable finite attractor family via τ* — **CLOSED as stated**, indistinguishable from unbounded slow growth at current sample size.
- (R,A,TH0,DV,DE) as a strong predictive twin-nucleation law — **CLOSED**, MI too small (<4% of target entropy) to call it a "law."
- Twin channel (Theta) as a universal symmetry-generation mechanism — **CLOSED since Z36**, reconfirmed here.
- Implicit "more density/more steps → more symmetry" assumption — **CLOSED**, medium density is the *least* symmetric regime observed (Task 4).

## REMAINING UNKNOWNS
- Whether ρ_c(N) is a genuine sharp threshold or a smooth crossover (Task 7) — needs N up to ~20+ with exact/BLISS-backed automorphism, currently a runtime wall.
- Whether the attractor-count growth curve (Task 8) ever plateaus — needs 10–100× more chains or exact enumeration for small (N,M).
- Whether an ALGEBRAIC-channel attractor (SRG-like, clique-structured) can ever be reached by *this specific* exchange dynamics, or whether it requires a different selector/rule — untested.
- Why TRIVIAL attractors dominate at ρ≈0.5 — no mechanism proposed yet, purely empirical (Task 4).
- The weak Theta-monotonicity found in Task 1 (41/60 lex chains) — not investigated as a candidate weak Lyapunov function.

## CONFIDENCE ESTIMATE
- **Specific engine (this exact exchange rule, N≤14)**: MODERATE. Every
  claim above is either exactly proved for the tested instances or backed
  by tens-to-hundreds of independent trials, but sample sizes are small
  enough (20–250 chains per cell) that borderline percentages (e.g. Task 7
  at ρ=0.2) are not trustworthy to more than ±10-15 percentage points.
- **Universal graph symmetry (claims beyond this specific dynamics)**: LOW.
  Nothing here generalizes past N≈14 or past this specific extremal
  selection rule; Task 5's clique-structure finding is a known fact about
  a specific graph pair, not a new universal principle.
- **Mathematical theorem status**: Only the three L1 items above qualify
  as theorems in the strict sense (exact, not sampled). Everything else is
  L2 (measured, with stated sample sizes) or L3 (conjecture, explicitly
  flagged).

## FINAL DECISION
**PARTIAL.**

Not FAILED: the corrected engine reproduces the qualitative shape of
several earlier claims (compression, twin-channel non-universality,
period-2 under deterministic selection) and surfaces one new, real,
reproducible phenomenon (the ρ≈0.5 trivial-symmetry dip in Task 4).

Not a STRONG EMPIRICAL THEORY: the twin-nucleation "law" (Task 3) carries
under 4% of the relevant information; the endpoint theorem (Task 8) could
not distinguish a finite attractor family from ordinary slow sampling
saturation; the critical-density claim (Task 7) is directionally
supported but not quantitatively pinned down.

Not THEOREM-LEVEL: only three narrow, exact, non-asymptotic facts (engine
correctness, the Shrikhande/Rook separator, and one specific 60-chain
period-2 measurement) meet that bar.

No optimism, no pessimism — this is a small-N computational combinatorics
result set with one genuinely new empirical finding (Task 4's density
dip) and several previously-strong claims correctly downgraded once
exact, independently-verified invariants replaced the earlier ones.
