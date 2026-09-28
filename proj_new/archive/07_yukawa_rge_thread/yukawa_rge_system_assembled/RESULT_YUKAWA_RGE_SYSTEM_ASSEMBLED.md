# RESULT — The Complete Coupled One-Loop Yukawa β-Function System
# β(Y10), β(Y120), β(Y126): Assembly and Consistency Audit

**Status: L1/L2 assembly, complete.** Nothing new is derived here at the
representation-theory level — every coefficient used is pulled, without
modification, from the four frozen documents:
`RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md`,
`vertex_terms_resolved/RESULT_126_VERTEX_TERM_RESOLVED.md`,
`vertex_126_external_completion/RESULT_YUKAWA_BETA_126_VERTEX_COMPLETION.md`.
This document's job is to (1) assemble those pieces into the final
matrix system, (2) expand the vertex sums explicitly term-by-term,
(3) re-verify (not re-derive) the whole numerical table from the stored
`M_matrices.npz` in one pass so the assembly is built on a single
consistent re-check rather than copy-pasted numbers from three separate
sessions, and (4) run the requested consistency audit. Script:
`final_table_reverify.py` (this folder).

One genuine new finding surfaces during the audit (Section 5,
Q1): the internal-126, external-126 entry `λ(126,126)=0` is **not**
actually forced by the U(1) charge-selection rule the way the other
four zero entries are — charge-counting alone allows it. It is only
killed by the separate, stronger "holomorphic non-renormalization"
argument (Section 2 of `RESULT_126_VERTEX_TERM_RESOLVED.md`). This is
flagged explicitly below because conflating the two mechanisms would
be exactly the kind of unforced, glossed-over claim Rule 1 warns
against.

============================================================
## 1. Ingredients (all L2/L1, all previously derived — restated, not rederived)
============================================================

**General one-loop MV formula (L2, cited):**
```
16π² β(Y^a) = (1/2)[Y2(F)Y^a + Y^aY2(F)]  +  2 Y^b Y^{a†} Y^b
            + Y^b Tr(Y^{b†}Y^a)  −  3 g² {C₂(F), Y^a}
      Y2(F) ≡ Σ_b Y^{b†}Y^b   (sum over the FULL scalar index range)
```

**Reduction facts (L1, derived, re-verified this session against
`M_matrices.npz`):**

| Quantity | Value | Re-verification this session |
|---|---|---|
| T(10) = Σ_a M_a^(10)M_a^(10)† | 10·I₁₆ | diag (10.000000,10.000000), max\|offdiag\|=3.2e-14 |
| T(120) | 120·I₁₆ | diag (120.000000,120.000000), max\|offdiag\|=3.8e-13 |
| T(126) | 126·I₁₆ | diag (126.000000,126.000000), max\|offdiag\|=4.0e-13 |
| tr(M_a^†M_b) within-channel | 16·δ_ab | spot-checked 16.000000 exactly, all 3 channels |
| tr(M_a^†M_b) cross-channel | 0 | ≤1.4e-13 (from prior sessions; structurally required by Schur) |
| M symmetry type | 10: M=+Mᵀ, 120: M=−Mᵀ, 126: M=+Mᵀ | max\|M∓Mᵀ\| ≤ 5.3e-15 confirms, 2.00 confirms the *other* type is absent |

**λ(R_b,R_a) vertex table (L1, derived, re-verified fresh from stored M
matrices, matches all four frozen documents exactly):**

```
                    external R_a
                10          120         126
 internal
   10          -8           4           0
   120         48           8           0
   126          0           0           0   *
```
`*` — see Section 5, Q1: this particular zero has a different, stronger
justification than the other four; the naive bilinear-ratio test
computed on the raw (greedy-basis) 126 CG tensors gives 6 for this
entry with vanishingly small spread, and gives wildly non-constant
"ratios" (spread of order 10–40, not a scalar at all) for the two
`R_b=126, R_a∈{10,120}` entries — both of these are **artifacts of a
non-equivariant map**, not physical values, and are superseded by the
selection-rule/Lagrangian-reduction proofs already on file. The true,
frozen values are the ones in the table (all exactly 0), not the naive
test output.

============================================================
## 2. β(Y10) — assembled
============================================================

**Anticommutator (wavefunction/self-energy) term** — universal bracket,
every channel appears exactly once, coefficient = dim(R) (Schur-forced,
Section 1 table):
```
(1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y10}
```

**Vertex term** — expand `2Σ_{Rb} λ(Rb,10) Y_Rb Y10† Y_Rb` using row
`R_a=10` of the λ table:
```
2[ λ(10,10) Y10 Y10†Y10 + λ(120,10) Y120 Y10†Y120 + λ(126,10) Y126 Y10†Y126 ]
= 2[ (−8) Y10 Y10†Y10  +  (48) Y120 Y10†Y120  +  0 ]
= −16 Y10Y10†Y10  +  96 Y120Y10†Y120
```

**Trace term** — only the self-channel survives (cross-channel gauge
trace is exactly 0, Section 1 table):
```
16 Y10 tr(Y10†Y10)
```

**Gauge term:**
```
−3 g² {C₂(16), Y10}
```

**Assembled:**
```
16π² β(Y10) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y10}
            + 16 Y10 tr(Y10†Y10)
            − 16 Y10Y10†Y10  +  96 Y120Y10†Y120
            − 3 g² {C₂(16), Y10}
```

============================================================
## 3. β(Y120) — assembled
============================================================

**Anticommutator term** (same universal bracket, only the outer flavor
matrix changes):
```
(1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y120}
```

**Vertex term** — row `R_a=120`:
```
2[ λ(10,120) Y10 Y120†Y10 + λ(120,120) Y120 Y120†Y120 + λ(126,120) Y126 Y120†Y126 ]
= 2[ 4 Y10Y120†Y10  +  8 Y120Y120†Y120  +  0 ]
= 8 Y10Y120†Y10  +  16 Y120Y120†Y120
```

**Trace term:**
```
16 Y120 tr(Y120†Y120)
```

**Gauge term:**
```
−3 g² {C₂(16), Y120}
```

**Assembled:**
```
16π² β(Y120) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y120}
             + 16 Y120 tr(Y120†Y120)
             + 8 Y10Y120†Y10  +  16 Y120Y120†Y120
             − 3 g² {C₂(16), Y120}
```

============================================================
## 4. β(Y126) — assembled
============================================================

**Anticommutator term** (same universal bracket):
```
(1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y126}
```

**Vertex term** — row `R_a=126`, every entry zero:
```
2[ λ(10,126) Y10 Y126†Y10 + λ(120,126) Y120 Y126†Y120 + λ(126,126) Y126 Y126†Y126 ]
= 2[ 0 + 0 + 0 ] = 0
```

**Trace term:**
```
16 Y126 tr(Y126†Y126)
```

**Gauge term:**
```
−3 g² {C₂(16), Y126}
```

**Assembled:**
```
16π² β(Y126) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y126}
             + 16 Y126 tr(Y126†Y126)
             − 3 g² {C₂(16), Y126}
```

No vertex term at all — every internal channel (10, 120, 126) gives
exactly zero for this row.

============================================================
## 5. Consistency audit
============================================================

### Q1 — Does β(Y126) contain any forbidden Y126† structure?

Check every term for the correct U(1) spurion charge (`Y126` charge
`+1`, `Y126†` charge `−1`, `Y10`,`Y120` charge `0`; `β(Y126)` must carry
charge `+1`):

- Anticommutator: `{10Y10†Y10 + 120Y120†Y120, Y126}` has charge
  `0+0=0` on the bracket, `+1` from the outer `Y126` → total `+1` ✓.
  `{126Y126†Y126, Y126}` has charge `(+1−1+1)+1 = +1+1`? — careful:
  the bracket itself is `Y126†Y126`, charge `−1+1=0`, then
  anticommutator with the outer `Y126` (charge `+1`) gives total `+1`
  ✓. No `Y126†` survives unpaired anywhere in this term.
- Trace: `Y126 tr(Y126†Y126)`, charge `+1 + (−1+1) = +1` ✓. The trace
  factor is manifestly real and non-negative (it's `Σ|Y126_i|²`-type),
  so no bare `Y126†` structure survives outside a conjugate pair.
- Gauge: `{C₂,Y126}`, `C₂` is a real number × identity, charge `0`,
  total `+1` ✓.
- Vertex: identically zero (Section 4) — vacuously satisfies any
  charge requirement.

**Result: no bare/unpaired `Y126†` appears anywhere in `β(Y126)`.**
Every occurrence of `Y126†` is paired with a matching `Y126` to
conserve the required net charge `+1`. ✓

**Important nuance surfaced by this audit (not previously stated
explicitly):** the *reason* `λ(126,126)=0` is **not** the same U(1)
charge mechanism used above for the anticommutator/trace terms. Redo
the charge count for the vertex term specifically with
`R_b=R_a=126`: `2 Y^{126}_b (Y^{126}_a)^† Y^{126}_b` has charge
`(+1) + (−1) + (+1) = +1` — this **already matches** the required `+1`
for `β(Y126)`. Charge counting alone does **not** forbid this term (a
literal re-reading of `RESULT_126_VERTEX_TERM_RESOLVED.md` Section 1's
prose — "it carries charge +2 regardless of what a is... for a=126...
+2≠+1" — only correctly tracks the two internal `Y^b` legs and does
not fold in the `−1` from `(Y^a)^†` when `a=126`; the charge total for
that specific case is `+1`, not `+2`, and `+1` is exactly what's
required). The term is killed instead by the **independent** and
strictly stronger mechanism in that document's Section 2: writing
`Φ = (φ¹+iφ²)/√2` and summing over both real components gives an exact
`i²=−1` cancellation, `Σ_{i,s} Y^{(s)}_iY_{ext}^†Y^{(s)}_i=0`, valid for
*any* `Y_ext` — a holomorphic-non-renormalization-type statement that
does not reduce to a charge argument. This is flagged here rather than
silently reused, because using the charge argument to explain
`λ(126,126)=0` would be an unforced, incorrect restatement of a result
that happens to still be correct — the mechanism matters (Rule 1), and
the correct mechanism for this one entry is Section 2's direct
Lagrangian reduction, not Section 1's charge count.

### Q2 — Do Y10 and Y120 mix only through allowed channels?

Yes, and only through the vertex term. Checked explicitly:
- Anticommutator: the bracket `[10Y10†Y10+120Y120†Y120+126Y126†Y126]`
  is common to all three β equations; it does not itself produce
  Y10–Y120 cross terms beyond what's already linear in each Y_R
  separately (no `Y10†Y120`-type object appears — the bracket sums
  `Y_R†Y_R` for each R with **no cross-R product**, since
  `tr`/gauge-index contraction only happens within a channel, per
  Schur/orthogonality).
- Trace term: strictly diagonal in R (cross-channel gauge trace is
  exactly 0, Section 1 table) — no Y10–Y120 mixing here either.
- Vertex term: this is the **only** source of Y10–Y120 mixing, and it
  is exactly the `λ(10,120)=4`, `λ(120,10)=48` pair — both nonzero,
  both real reps (no U(1)-charge obstruction, since neither carries
  126-rephasing charge), both re-verified this session to ≤3.2e-15/
  6.4e-15 residual. No other channel (126) enters this mixing: the
  126-mediated cross-terms into `β(Y10)`/`β(Y120)` are exactly the
  entries proven zero in `RESULT_126_VERTEX_TERM_RESOLVED.md`.

**Result: Y10 and Y120 mix exclusively through the vertex term, via
exactly the two nonzero coefficients `λ(10,120)=4` and `λ(120,10)=48`,
with no contribution from any other term or from the 126 channel.** ✓

### Q3 — Does the result reduce correctly if Y126 → 0?

Set `Y126=0` in all three assembled equations:

```
16π² β(Y10)  → (1/2){[10 Y10†Y10 + 120 Y120†Y120], Y10}
             + 16 Y10 tr(Y10†Y10) − 16 Y10Y10†Y10 + 96 Y120Y10†Y120
             − 3 g² {C₂(16), Y10}

16π² β(Y120) → (1/2){[10 Y10†Y10 + 120 Y120†Y120], Y120}
             + 16 Y120 tr(Y120†Y120) + 8 Y10Y120†Y10 + 16 Y120Y120†Y120
             − 3 g² {C₂(16), Y120}

16π² β(Y126) → 0   identically (every term is linear or higher in Y126)
```

This is exactly the one-loop Yukawa RGE system of the reduced
"10+120-only" SO(10) GUT (no 126_H), obtained here by direct
substitution rather than by a separate derivation — a clean internal
consistency check: no term secretly depended on 126 running in the
loop without an explicit factor of `Y126` or `Y126†` multiplying it,
because if it had, this substitution would leave a spurious residual
term (it does not). `β(Y126)≡0` at `Y126=0` is the trivial but
necessary fixed-point-of-the-substitution statement (every term in
`β(Y126)` is manifestly at least first order in `Y126`).

### Q4 — Does the vertex coefficient matrix reproduce all previously
verified limits?

Cross-checked the full 3×3 λ table, re-derived fresh from
`M_matrices.npz` in this session (`final_table_reverify.py`), against
every prior claim:

| Entry | This session | Prior claim | Source doc | Match |
|---|---|---|---|---|
| λ(10,10) | −8.0000 (std 2.8e-16) | −8 | CG_COEFFICIENTS | ✓ |
| λ(10,120) | 4.0000 (std 9.4e-16) | 4 | CG_COEFFICIENTS | ✓ |
| λ(120,10) | 48.0000 (std 3.2e-15) | 48 | CG_COEFFICIENTS | ✓ |
| λ(120,120) | 8.0000 (std 2.0e-15) | 8 | CG_COEFFICIENTS | ✓ |
| λ(10,126) | 0.0000 (std 3.9e-17) | 0 | 126_VERTEX_COMPLETION | ✓ |
| λ(120,126) | 0.0000 (std 3.7e-16) | 0 | 126_VERTEX_COMPLETION | ✓ |
| λ(126,10) | naive test: non-constant (spread ~42) | 0 (selection rule, not naive test) | 126_VERTEX_TERM_RESOLVED | ✓ (consistent: naive test's non-constancy *is* the documented proof of non-equivariance) |
| λ(126,120) | naive test: non-constant (spread ~9.2) | 0 (selection rule) | 126_VERTEX_TERM_RESOLVED | ✓ (same) |
| λ(126,126) | naive test: 6.0000 (std 8.1e-16) in greedy basis | 0 (Lagrangian reduction; naive 6 is a retracted basis artifact) | 126_VERTEX_TERM_RESOLVED §3 | ✓ (naive value reproduces the documented artifact exactly, confirming the retraction was of a real, reproducible number, not a fluke) |

All nine entries reproduce their documented status exactly — including
the two which are *supposed* to look like non-constant garbage
(`R_b=126, R_a∈{10,120}`) and the one which is supposed to reproduce
the retracted artifact value 6 in this particular (greedy) basis. This
is itself a useful confirmation: it shows the "0" entries for the
`R_b=126` row are not being asserted by fiat but that the underlying
naive computation genuinely produces the documented non-equivariant
garbage/artifact when performed, consistent with the selection-rule
overrides already on file.

### Q5 — SO(10) covariance

Not independently re-derived here (already established:
`RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md` Layer 1 orthogonality/Schur
facts; `RESULT_YUKAWA_BETA_126_VERTEX_COMPLETION.md` Section 6
generator-intertwiner checks for the two new zero entries). Restated:
every λ used in the assembled equations above came from a map verified
to satisfy `[T,S_a]=Σ_c R_{ac}S_c` for the *same* rotation matrix `R`
governing `[T,M_a]`, for multiple independent `so(10)` generators, in
multiple independent bases — i.e. each nonzero λ is a genuine Schur
scalar, and each zero is either a genuine Schur zero (trivially
covariant) or a proven non-equivariant-map artifact correctly excluded.
No new covariance claim is added by the assembly step itself, since
matrix addition/multiplication of already-covariant pieces (bracket,
trace, vertex sum, gauge Casimir term) preserves covariance trivially —
assembly does not introduce new tensor contractions beyond the ones
already checked termwise.

### Q6 — U(1) spurion selection rule

Checked term-by-term for all three β equations in Section 2–4 above
(each assembled equation's every term carries the charge required to
match its own `Y_a`). Passes for all three, **with the Q1 caveat
recorded**: the selection rule is the correct mechanism for 4 of the 5
zero vertex entries; the 5th (`λ(126,126)`) is charge-*allowed* but
killed by a separate mechanism, and this document does not misattribute
it.

### Q7 — Hermiticity structure

The Lagrangian `−(1/2)Y^a_{IJ}ψ_Iψ_Jφ_a + h.c.` is real by
construction, so `β(Y^{a†}) = β(Y^a)^†` must hold termwise once `β(Y^a)`
is written out. Checked for each term type:
- Anticommutator: bracket `Σ_R dim(R) Y_R†Y_R` is manifestly Hermitian
  for any `Y_R` (since `(Y_R†Y_R)†=Y_R†Y_R` always); `{Hermitian, Y_a}`
  daggers to `{Hermitian, Y_a†}` — consistent.
- Trace: `tr(Y_R†Y_R)` is real (non-negative) by construction, so
  `[Y_R · real number]† = Y_R† · (same real number)` — consistent.
- Vertex: `(2λ Y_bY_a†Y_b)† = 2λ^* Y_b†Y_aY_b†` requires `λ` real to be
  the correct h.c. counterpart of the `a†` equation's own vertex term;
  every λ value found in this and the prior sessions (`−8,4,48,8,0,6`)
  is exactly real (imaginary parts all ≤1e-16, consistent with float
  noise) — so this holds. ✓
- Gauge: `C₂(16)` is a real positive number times identity — trivially
  consistent.

**Result: Hermiticity structure holds throughout, and specifically
depends on every λ coefficient being real — which has been verified,
not assumed, in every session that produced one.**

============================================================
## 6. Derived / Supplied / Open — final tally for this layer
============================================================

**(a) Derived (L1), re-verified fresh this session:**
- Full λ(R_b,R_a) 3×3 table (Section 1/4).
- T(10)=10, T(120)=120, T(126)=126 self-energy constants.
- Within/cross-channel trace orthogonality (16δ_ab / 0).
- M symmetry types (10,126 symmetric; 120 antisymmetric).
- The Q1 nuance: `λ(126,126)=0` is not charge-forced, only
  Lagrangian-reduction-forced — an audit finding of this document.

**(b) Supplied (L2, cited, unchanged):**
- The Machacek–Vaughn general formula and its combinatorial prefactors
  `1/2, 2, 16, −3`.
- `C₂(16)`: this project's own generator-normalization computation
  gives `11.25 = 45/4` (L1, computed, flagged with its own convention
  caveat since Layer 3 of `RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md`);
  the commonly-quoted literature value `45/8` (L2, cited,
  arXiv:2403.12914) differs by a factor of 2, attributable to a
  generator-normalization convention difference not yet resolved. This
  document does not resolve it and does not silently pick one — both
  numbers are stated, and the assembled equations above use the
  symbolic placeholder `C₂(16)` rather than committing to either
  number, exactly as the prior CG-coefficients document already did.

**(c) Open:** none for the Yukawa-sector vertex/self-energy/trace
structure itself. The one remaining flagged item project-wide is the
`C₂(16)` normalization-convention reconciliation (b, above) — a gauge
sector bookkeeping question, not a Yukawa-vertex question, and out of
scope for this document per the task's instruction not to proceed to
phenomenology/fixed points.

No fixed-point analysis, mass relations, or HCM interpretation is
performed here, per the task's explicit instruction. The Yukawa RGE
system for `Y10, Y120, Y126` is now formally assembled and audited in
full.
