# RESULT — Completion of the One-Loop Yukawa Vertex Coefficients into β(Y126):
# λ(10,126) and λ(120,126), Both Exactly Zero — By Selection Rule, Confirmed by CG Numerics

**Status: L1, complete.** This closes the gap explicitly flagged in
`vertex_terms_resolved/RESULT_126_VERTEX_TERM_RESOLVED.md` Section 4:
*"a full accounting would need λ(10,126) and λ(120,126) too (R_b∈{10,120}
real, R_a=126 external) ... it needs the same real-rep Schur machinery
already used for the −8,4,48,8 table, just with a complex external
leg."* That machinery is applied here.

Frozen and **not** revisited: `λ(126,10)=0`, `λ(126,120)=0`,
`λ(126,126)=0` (internal 126, from the U(1)-selection-rule /
Lagrangian-reduction argument). The present document concerns the
**reverse** assignment — real internal rep (10 or 120), complex
external leg (126) — which is a structurally different, and legitimate,
computation (real `R_b` means no reality-type obstruction on the
`Σ_b M_b (·) M_b` map itself).

============================================================
## 1. Method
============================================================

Two independent derivations, cross-checked against each other:

**(A) U(1) rephasing selection rule (L1, no numerics needed).** Same
spurion charge assignment already established and frozen:
`Y_126 → e^{+iα}Y_126` charge `+1`, `Y_126^† ` charge `−1`, `Y_10`,
`Y_120`, fermions charge `0`. `β(Y_a)` must carry the same charge as
`Y_a`.

**(B) Explicit Cl(10) CG construction (L1, numerical, machine
precision).** Built `M_a^{(10)}`, `M_{[abc]}^{(120)}`, `M_k^{(126)}`
exactly as in `RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md` / Layer 0 (with
the `1/√2` self-dual normalization fix applied, giving
`tr(M_a^†M_b)=16δ_ab` in every channel — reverified below), from the
project's `gamma_0..9.npy` and `so10_generators.npz`. Computed
```
S_a^{(10→126)}  = Σ_{b∈10}  M_b^{(10)}  M_a^{(126)†}  M_b^{(10)}
S_a^{(120→126)} = Σ_{b∈120} M_b^{(120)} M_a^{(126)†}  M_b^{(120)}
```
for every component `a` of 126, tested the Schur ratio
`λ_a = tr(M_a^†S_a)/tr(M_a^†M_a)`, and the max entrywise residual
`‖S_a − λ_a M_a‖`. Repeated in two independently-constructed 126 bases
(greedy Gram–Schmidt and SVD/orthonormal) to test basis-independence,
and checked generator covariance directly. Scripts:
`compute_126_external.py`, `covariance_check.py` (this folder).

============================================================
## 2. Explicit formulas / the selection-rule argument
============================================================

Vertex term for **external** `a ∈ 126`: `2 Y^b (Y^{126})^† Y^b`. Its
required charge (to match `β(Y_126)`) is `+1`. For `b` ranging over a
**real** internal channel (`10` or `120`, charge `0` each use of `Y^b`):

```
charge[ Y^b (Y^{126})^†  Y^b ] = 0  +  (−1)  +  0   =  −1
```

`−1 ≠ +1` (the charge `β(Y_126)` must carry). **Selection-rule
verdict: forbidden, forced to vanish**, for both `R_b=10` and
`R_b=120`. This is a strict extension of the same argument already used
to kill the internal-126 cases; it was not previously applied to this
(real-internal, complex-external) pairing because Section 4 of the
prior document treated it as an open Schur-type computation rather than
re-running the charge argument. It turns out the charge argument
already settles it, with the CG computation below serving as an
independent, non-redundant confirmation (Rule 9: this argument
correctly does *not* forbid the surviving `Y_126 Y_126^†Y_126` term,
charge `+1−1+1=+1` ✓, so it retains discriminating power here too).

============================================================
## 3. Computed λ(10,126) and λ(120,126)
============================================================

**λ(10,126) = 0** (exact, to machine precision)
**λ(120,126) = 0** (exact, to machine precision)

Both are **identically zero matrices** `S_a ≡ 0` for every component
`a` of 126 — not merely "proportional to `M_a` with a zero
coefficient" found by a possibly-degenerate ratio, but directly:
`max|S_a|` entrywise, over all 126 components, in both the greedy and
SVD 126 bases:

| Map | max entrywise \|S_a\| |
|---|---|
| 10 → 126, greedy basis | 6.99e-15 |
| 10 → 126, SVD/onb basis | 6.66e-15 |
| 120 → 126, greedy basis | 3.84e-14 |
| 120 → 126, SVD/onb basis | 3.84e-14 |

All at the noise floor of the underlying gamma-matrix construction
(consistent with the ~1e-13–1e-15 floor quoted throughout the earlier
documents). This numerically confirms the selection-rule prediction
exactly, independent of it.

============================================================
## 4. Residual / error table
============================================================

Sanity re-check of the already-known real–real entries with the same
code path (confirms the machinery itself is correct before trusting its
zero result on the new pairing):

| R_b \ R_a | λ computed | expected | max residual ‖S_a−λM_a‖ | std of λ across components |
|---|---|---|---|---|
| 10 → 10   | −8.000000 | −8 | 6.41e-15 | 2.8e-16 |
| 10 → 120  | 4.000000  | 4  | 6.41e-15 | 9.4e-16 |
| 120 → 10  | 48.000000 | 48 | 3.55e-14 | 3.2e-15 |
| 120 → 120 | 8.000000  | 8  | 3.20e-14 | 2.0e-15 |

New results, this document:

| R_b \ R_a | λ computed | max residual ‖S_a−λM_a‖ (λ=0 convention) | max\|S_a\| direct |
|---|---|---|---|
| 10 → 126 (greedy)  | 0 | 7.03e-15 | 6.99e-15 |
| 10 → 126 (onb)     | 0 | 6.67e-15 | 6.66e-15 |
| 120 → 126 (greedy) | 0 | 3.84e-14 | 3.84e-14 |
| 120 → 126 (onb)    | 0 | 3.84e-14 | 3.84e-14 |

Normalization control (`tr(M_a^†M_b)=16δ_ab`), all four channels used:

| Channel | diag range | max\|off-diag\| |
|---|---|---|
| M10  | (16.000000, 16.000000) | 2.59e-15 |
| M120 | (16.000000, 16.000000) | 6.44e-15 |
| M126 greedy | (16.000000, 16.000000) | 6.41e-15 |
| M126 onb    | (16.000000, 16.000000) | 8.84e-15 |

Cross-channel orthogonality (`tr(M_a^{(10)†}M_b^{(126)})`,
`tr(M_a^{(120)†}M_b^{(126)})`): max |·| = 6.44e-15 and 6.41e-15
respectively — exact zero, as required for 10, 120, 126 to be distinct
irreducible summands.

Control against the disallowed alternative `Σ M_b X M_b^†` (Rule/check
4 of the Validation Requirements): computed both
`S_correct = Σ M_b (M_0^{(126)})^† M_b` and
`S_wrong = Σ M_b M_0^{(126)} M_b^†` for `R_b=10`; `max|S_correct −
S_wrong| = 2.0` exactly — the two constructions are demonstrably
different operations (both individually evaluate to ≈0 for this
particular pairing, which is itself further evidence of the
selection-rule origin of the vanishing, since `S_wrong` uses the
opposite charge assignment and is not expected to cancel by the same
mechanism — its coincidental smallness here was checked and is **not**
a generic feature: `S_wrong` is the same order of magnitude as the
individual terms summed, ~2, not systematically suppressed the way
`S_correct` is at the 1e-14 floor). This confirms the script uses the
required MV structure `Σ M_b X M_b`, not the incorrect
`Σ M_b X M_b^†`.

============================================================
## 5. Basis-independence proof
============================================================

Repeated the entire Case A/B computation with two 126 bases related by
an arbitrary unitary rotation on the 126 label (both individually valid
CG tensor sets, both satisfying `Σ_k M_k M_k^† = 126·I_16` exactly,
i.e. both pass the same `T(126)=126` check used in the prior session):

- **Greedy Gram–Schmidt basis** (the one built by the original
  `task2_3_higgs_reps.py` construction).
- **SVD/orthonormal basis** for the identical 126-dim self-dual
  subspace (an independently, non-arbitrarily constructed alternative).

Result: `λ(10,126)=0` and `λ(120,126)=0` in **both** bases, each to the
same ~1e-14 floor (Section 3/4 tables). This is the expected behavior
for a basis-independent statement, and is the opposite of what happened
with the retracted `λ(126,126)=6` (Section 3 of
`RESULT_126_VERTEX_TERM_RESOLVED.md`), where the two bases gave wildly
different numbers — that was the signature of a **non**-equivariant
map being tested; here, both bases giving the same answer (zero) is the
signature of the map genuinely being (trivially) equivariant, matching
the selection-rule prediction that this map is identically the zero
operator regardless of basis.

============================================================
## 6. Covariance verification
============================================================

For three independent `so(10)` generators (`Σ_{01}`, `Σ_{25}`, `Σ_{47}`
from `so10_generators.npz`, restricted to the 16-dim chiral block via
`T = V^†ΣV`):

1. **Sanity (nonzero case, `λ(10,10)=−8`).** Verified
   `[T, M_a^{(10)}] = Σ_c R_{ac} M_c^{(10)}` for the rotation matrix `R`
   extracted via the `tr(M_c^†·)/16` projector (closure residual
   1.7e-15), then verified `[T, S_a] = Σ_c R_{ac} S_c` using the
   **same** `R` (covariance residual 1.3–1.4e-14) — confirming the
   covariance-check methodology correctly detects a genuine intertwiner
   when one is present.
2. **Case A/B (`λ(10,126)=λ(120,126)=0`).** Same test: closure residual
   for the 126 generator action itself is 2.8–3.2e-15 in both bases (as
   expected — 126 is a bona fide SO(10) irrep regardless of the vertex
   question); the covariance residual `‖[T,S_a] − Σ_c R_{ac}S_c‖` is
   5.3–5.5e-14, at the same numerical floor as `S_a` itself. Since
   `S_a ≡ 0` (Section 3), `[T,S_a]=0` trivially and `Σ_c R_{ac}S_c=0`
   trivially — the zero map is unconditionally SO(10)-covariant
   (transforms into itself under every generator), so this is not a
   vacuous check but the expected, consistent outcome: **the intertwiner
   condition is satisfied because there is no nonzero tensor to violate
   it.**

============================================================
## 7. Updated complete β(Y126)
============================================================

Combining this result with the frozen internal-126 zeros
(`λ(126,10)=λ(126,120)=λ(126,126)=0`, from
`RESULT_126_VERTEX_TERM_RESOLVED.md`) and the newly-derived
`λ(10,126)=λ(120,126)=0`: **the entire MV vertex term
`2Σ_b Y^b Y^{126†}Y^b` vanishes identically for every internal channel**
— `b∈10`, `b∈120`, and `b∈126` all give exactly zero. `β(Y126)` has
**no vertex-term contribution whatsoever**, from any channel:

```
16π² β(Y_126) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_126}
              + 16 Y_126 tr(Y_126†Y_126)
              − 3 g² {C₂(16), Y_126}
```

This is **unchanged from Section 4 of
`RESULT_126_VERTEX_TERM_RESOLVED.md`** — that document already wrote
`β(Y126)` with no vertex term present, because it had already shown the
`b∈126` piece vanishes for `a=126`. The present result shows the two
previously-open entries `λ(10,126)`, `λ(120,126)` (which that document
correctly flagged as *not yet computed*, distinct from the closed
`b∈126` cases) **also** vanish, so the displayed formula for `β(Y126)`
required no further edit — but the reason it required no edit is now
established rather than assumed, and the two coefficients are no
longer an open gap.

For completeness, `β(Y_10)` and `β(Y_120)` (unaffected by this
document — they only involve `R_a∈{10,120}`, and the `R_b=126`
internal contributions to them were already closed at zero in
`RESULT_126_VERTEX_TERM_RESOLVED.md`):

```
16π² β(Y_10)  = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_10}
              + 16 Y_10 tr(Y_10†Y_10)
              + 2[ −8 Y_10 Y10†Y10  +  48 Y_120 Y10†Y_120 ]
              − 3 g² {C₂(16), Y_10}

16π² β(Y_120) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_120}
              + 16 Y_120 tr(Y_120†Y_120)
              + 2[ 4 Y_10 Y120†Y_10  +  8 Y_120 Y120†Y_120 ]
              − 3 g² {C₂(16), Y_120}
```

============================================================
## 8. Clear separation of derived vs. supplied vs. open
============================================================

**(a) Derived this session (L1, from explicit Cl(10) CG construction +
selection-rule argument, machine precision or exact):**
- `λ(10,126) = 0` — selection-rule-forced, CG-confirmed (residual
  ≤7.0e-15).
- `λ(120,126) = 0` — selection-rule-forced, CG-confirmed (residual
  ≤3.9e-14).
- Basis-independence of both (Section 5).
- Generator-covariance consistency of both (Section 6).
- Re-verified normalization `tr(M_a^†M_b)=16δ_ab` in all four channels
  used (Section 4).

**(b) Externally supplied (L2, cited, not re-derived this session):**
- The Machacek–Vaughn general one-loop formula itself and its
  combinatorial prefactors `(1/2), 2, 16, −3` (Layer 2.1/Layer 3 of
  `RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md`).
- `T(R)=dim(R)` self-energy Schur constants, the `−8,4,48,8` real–real
  vertex table, and the `λ(126,·)=0` internal-126 selection rule —
  carried over unmodified from the two prior result documents, not
  recomputed from scratch here (only re-used as machinery/sanity
  checks, Section 4 table, top half).
- `C₂(16)=11.25` gauge Casimir (Layer 3 of the CG-coefficients
  document) — untouched by this document.

**(c) Still open:** none identified for the vertex term
`2Y^bY^{a†}Y^b` across `{10,120,126}×{10,120,126}` — all nine
`(R_b,R_a)` entries are now either a nonzero Schur-forced number
(`−8,4,48,8`) or a selection-rule-forced exact zero (the remaining
five entries, all confirmed above or in the frozen documents). The
fermion self-energy and scalar-trace terms were already fully closed
in Layers 2.2–2.2 of `RESULT_YUKAWA_BETA_CG_COEFFICIENTS.md` and are
not revisited. The gauge term's normalization-convention caveat
(Layer 3, `C₂(16)` vs. the literature's `45/8`) remains flagged but is
outside this document's scope. No fixed-point analysis was performed,
per the task instructions.
