# PROPOSED MECHANISM — "The Space-Definition Hypothesis"
# Version 1.0 (2026-08-03) — Proposal only, not a result.
# Companion to the Z-series corpus. Status: UNFALSIFIED-STEREOTYPE — see §7 for
# what would make it a discovery vs. a dead end.

---

## 0. PURPOSE OF THIS FILE

This file states the mechanism we *want* to try — a concrete, code-testable
hypothesis that links the Z-corpus' measured dynamics ("edge-exchange relaxes
onto high-symmetry attractors; the twin channel is the class of the jump") to a
**definition of space itself**, i.e. to what normally stands *before* field
theory, gauge symmetry and the Higgs mechanism.

It intentionally does **not** claim "we have the answer". It claims one thing
we can run today and see: **space is the maximal-|Aut| attractor of a stated
rule, and gauge/Higgs are named pieces of that attractor's anatomy.** If the
next pre-registered experiment (L1 prototype, §6) fails its gates, the
space-direction is dead; if it passes, it is the first stone.

---

## 1. WHY "SPACE" HERE — WHAT IT MEANS

In QFT, fields live *on* a fixed spacetime; Higgs is a talk about field breaking
"inside" that space. "Nothing is explained before the Higgs" is our shorthand
for: the framework never *derives* why there is a container (space) with the
symmetries it has. The hope stated here is the opposite direction:

> **P0 (definition of space):** A spacetime at parameter (N,M,seed) is the
> *attractor class* produced by the symmetry-concentrating exchange rule
> (`phase_z25/z25b_engine_v2.py`, rule T with the declared ordering) for that
> cell. Space is therefore not an *input* of the model — it is the *stuff the
> model converges onto*. `|Aut(G_t)|` = the "amount of space" the rule has
> built up to step t.

The Z-corpus already gave the empirical bones for this:

- the rule does **not** sample the Aut-weighted law uniformly — it suppresses
  low-Aut shells and concentrates support onto the **max-Aut shell**
  (t6, Burnside exact count; TV(random vs law)=0.70–0.86);
- jumps of |Aut| are all `twin-restructuring` (Z34 H1 3.72×headline over random;
  91–99% of jumps carried by the twin channel, t4);
- θ = Σ C(|C_i|,2) twin potential is a **near-Lyapunov order parameter**
  (P(dt<0|J)=0.000, Z35);
- the only genuinely closed mechanistic identity — **tie-collapse** (Z26):
  "same representative in one (N,M,seed) run is merged degenerates under
  extremal, not local injectivity".

So the operating copy: **symmetry is produced by twin-restructure events;
the attractor set is the famous output; space = the attractor; "gauge" = the
freedom over which twins are equivalent; "Higgs-breaking" = the tie-collapse
event where one representative is canonically chosen.**

---

## 2. THE SPACE-DEFINING HYPOTHESIS — precise, though false as written

Write it as pre-registered gates (mirroring the Z35/Z37 protocol style of the
repo; labels F1..F4):

- **F1 (space is symmetry-built, not born):**
  Let τ = "the unique step t where the attractor's |Aut| jumps from an
  asymmetric majority shell(|Aut|=1) into the shell carrying ≥1 twin class".
  For the 4 declared selectors {random, lex, entropy, autmin}, with θmin over
  cells (8,12)…(16,32), test that **the all-time-max |Aut** is used in the
  Att-R strat: Att-R strat — the multiple cells revisit the *same* attractor's
  |Aut|-mass (shares shell), i.e. |Aut|Max forms a closure law across N — if
  so, that's the built space identity.
  → default: **FAIL** likely (known: no uniform closure; attractor keys are
  seed-driven, Φ26 theorem A). THIS IS THE HONEST FAILURE MODE.

**But you are pointing at a second place for space to be "defined": the
rule boundary.** Front accept:

- **F2 (space is *at* the interface):**
  At M/N = const (twin/turnover density) the rule's equilibrium states spend
  a measurable fraction of evolutions sitting **between** two attractor classes
  (period-2 shell R,A ≃ (6,2), Z30). The claim: those boundary states are the
  "vacuum"; the set of boundary states in adjacency-graph-photo is the base
  energy "metric" that matter is "on top of".
  → we can measure: fraction of steps spent in shell (R,A), and whether it
  scales at ν/ρ as N→∞ while interior-Aut (internal space) saturates.

H-2c: physical (must be run) — **the twin channel emits "boson" degrees of
freedom**: if the rule-field (graced at every jump on a given pair (a,b), twin
twin-x) writes the fraction `P(twin-X | jump)` uniformly as (start mass) only
as a counting function of feeding "order params" — equals what a gauge boson
would do: interactions couple always to the shortest action twin-pair.

---

## 3. WHAT WE ARE *NOT* CLAIMING (disclaimer, to be quoted)

Because this repo is a disciplined protocol, this document must state the
limits explicitly:

1. We do **not** claim this is- a `QCD`‑or-EW-theory with coupling
   constants. There are no numbers yet, only qualitative structure.
2. The word "Higgs" appears **only** at the level of the analogy:
   "tying a canonical representative breaks a tie-degenerate group action" —
   which is the common denominator of SSB. It is a *structural* parallel, not
   a physics coupling candidate. The current attractor dynamics produce
   |Aut| — the quantity already measured (twin channel, θ) — a number with
   the dimension of a **field-次 / "space". No mass dimension exists.
3. The paper's value in this direction is **NOT** that the model "contains"
   a step duality — that would be trivial and they doinned our own
   conclusion § Q4-… (Z25-b: the dynamics compresses information rather than
   generating it; concentration < 20× generation gap). "Space from the graph"
   as a *compile:* the task is to concede the graph-space as *classical
   lakebed* — not the "origin of particles".
4. If the attractor-set-to-set identity F1 fails (expected on our own
   literature), the hypothesis has **another** path to be a real space-model —
   via F2 (the interface). We commit to not claiming "derivation" until both
   are falsifiability.

---

## 4. MAPPING TABLE — code ↔ particle-physics-intent

A spec table which maps what our measures mean ("AT = atom" is intentionally
left empty; the *draft* mapping is given, entire intent to run):

| Z-file / measure | meaning today (proven) | proposed meaning | status |
|---|---|---|---|
| N, M (vertex/edge count) | parameter cell (scale, density) | "spacetime size / content" | conceptual |
| rule T (extremal exchange) | deterministic driver (Z25-b) | "the space-defining law" | claimed |
| |Aut(G)| | symmetry mass; | "amount of space / of vacuum structure" | candidate |
| θ = ΣC(|C_i|,2) twin potential | near-Lyapunov; predicts all jumps (Z35) | order parameter (like φ) | candidate |
| twin channel / twins | how ∂|Aut| jumps (Z34Z35Z37) | the "carrier / field substance" | analogy |
| tie-collapse (Z- {dede}) | merged degenerates are canonical (Zπ36) | **breaking event** (SSB analog) | structural |
| attractor set | class of the end state | "spacetime / vacuum set" | claimed |
| quotient |Q|=136,433 @(10,15) | after-gauge of reachable graph | counted physical state-count candidate |
| Aut-weighted law (t6) | dynamics over-selects max-Aut shell | statistically-selected space | candidate |

---

## 5. THE FIRST IMPLANTABLE EXPERIMENT (today, can close soon)

This is the one we can actually run, **gated and falsifiable**:

**LEN — "signature-encoding of space" (Lead Experiment §N):**
> Hypothesis T1: the twin-creation events carry an information fingerprint that
> counts as "gauge exchange": over a relaxation run, the cumulative
> (twin→quotient block) token stream ℬ (jump at t ⇒ look at t, t+1) …
> gives that the entropy rate I(token-group|pair of jumps…) is **less than**
> the exchange rate (crossing counter), i.e. the twins' identity in the quotient
> is *deterministic* — a mechanism "varies" in the clone set rather than
> exploring fundamentally. The identity counts as "codified space".

If instead we find twin-restructure always {: random walk} in the quotient
(I(twin)=Qualitative), **T1 → FAIL** and the space-direction is retgut alone a
combinatorial curiosity (we then say so in report-alongside).

- The server- a continuation today of the existing runs, no new canvas.
- **Ready artifacts to reuse:** `phase_z25/z25b_engine_v2.py` (engine),
  `phase_z37/z37_closure.py` (τ/chains), `phase_z35/` exact-|Aut| protocol,
  136,433 Q-count.

---

## 6. THE BRIDGE TO HIGGS — the "before-Higgs" placement

Higgs mechanism semantics we are claiming(/hoping) to fulfil:

1. **Background = space**: in the model, background = the attractor class at
   (N,M) (F1 tested, likely exotic).
2. **Fields = space-fluctuation channels**: after "fixing" the quotient, the
   decorated degrees of freedom — twins / tie-classes — become the only
   quickly excitable freedom. That is the only natural "light" channel.
3. **The "nothing before Higgs" idea as an assertion** — standard framework is
   *geometric*; a geometry is an input datum, so "before the geometric area of
   the G_EM there is nothing" is trivially true. Our model's claim is that the
   **geometry itself is a consequence of the relaxor… yet the "there is
   nothing before Higgs" **actually** means "no level-2 was ever observed/已知"
   — meaning the field, its group, its ht — everything lives inside that
   attractor. So: if our attractor yields a **non-trivial** endpoint symmetry
   (a δ at +1 learnable even in the twins), then the 5th field ("space-symestry")
   is *defined* as the projection "space" onto the twins, i.e. a "first
   un-Higgsed" quantity.

So the correct statement of the hope: **there is a parametrized attractor
class that is *exactly* the "space-lattice" whose ℤ/degenerations coincide
with discrete/chromo symmetries — the Higgs would then be the *specific*
mechanism that *first* breaks that lattice's twin-dynamical "vacuum" (one
representative chosen). The priority is the opposite to the standard model:
**where physics starts, space just got a field; where physics stops, the
field is everything. Our claim: space is a building-state, Higgsfield is a
statement about its build."

---

## 6. WILL IT BE NEW or reinvention?

The codes answer we owe (§lecting to user): it is **both**, and the burden is:

1. anything scoreable we have is **standard** (canon/WL/twin/canonical labels
   all known — see §3 of `CANON_FIX_FULL_REPORT.md`: none of this is our own
   math).
2. The prevention of "fix is reinvention" is, again, the **existence of the
   mapping (attractor, twin,tie-collapse) → (vacuum, field, breaking)** — a
   mapping that the *literature stage* does not contain as a single unit.
   If that mapping holds (tested bioscription L1), the "field" is a *new
   combined vocabulary* even with only standard pieces.
3. Otherwise (F1 and T1 fail), we are left with a well-tested, reimplemented
   graph Canonicalization — in which case you would have us dispatch the
   piece back into the graph literature and stop the physics story. Which is
   not wasted work (the corpus and the endpoints are reusable).

So **"new discovery" possible ONLY if F2/T1 produce a real, reproducible
code-quantified signal that no published result predicts**. Everything else is
**confirmed complexity**; it is *not news* if we find max-Aut shells — the
corpus already published that at t4/σ6.

---

## 7. CIRCUIT / protocol summary and DONE-CRITERION

- **Done = when:** a single run file (new, `z38_hypo_step1.py`) takes
  (N,M,seed) → prints `T1 verdict`, `F2 slope`, and exits with the two gates
  PASS or FAIL, copied into a report addendum. (Code to be written only if
  asked.)
- **Non-Deluderators / negatives still respected:** tie-degeneracy (Z26)
  means "canonical representativeness" is NOT uniqueness-by-injection at all,
  so the "Higgs=breaking" analogy is tied to the *quotient* — we must print
  (i) |Q|, (ii) the twin/jump histogram — in ALL cases, so the space story is
  falsifiable by two distinct gates.
- Any claims of "origination" are battery: F1 → "space built by rule";
  otherwise "space is the residual unsampled fat" (closed).

---

## 8. FREE: the actual state of what if this fails

If T1 falls (twins perform as a combinator "uncoancestral random walk"), the
physcis pseudo is **over** for the "space-defining" reading, and Z-project
outcome is nonetheless: a K-versus-N experiment with a canon-independent core
(Φ26 фactoria: concentration < generation, Autonomous the attractor-key
share) — i.e., we keep as is a "rigorous absence of generative source" which
is its own sound result (like Q4 "no hidden tuning").

If T1 holds (+2 some slope from F2) we then need a **second independent falsifier
($ "Higgs-angle" hypothesis)**: "the twin-stream's cross-token (up/down;
drive/p H) is conserved" — then that conserved token is a *candidate* for a
"before-Higgs gauge velocity", as it is *derived* from a twin-anvmemphidentity,
not put in by hand. This is the designed second gate.

User note (marked honest): the image of "space-quantizations " and "quantization
from duals" is currently **conceptually cloudy** in our protocol; this doc is
written to be *readable* and *falsifiable*, refusing to use poetry instead of
tests.

---

*File alongside: `latest_progress_report.md` (facts), `Z35_Z36_AUDIT_REPORT.md`
(verifiable gate results), `phase_z37/` (formal closure gates). Hypothesis —
not a finding; MAJOR royalty.*