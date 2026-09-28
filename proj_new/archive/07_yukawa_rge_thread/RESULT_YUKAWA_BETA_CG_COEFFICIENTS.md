# RESULT — Explicit SO(10) Clebsch–Gordan Coefficients for the One-Loop
# 10_H + 120_H + 126_H Yukawa Beta Functions

> ⚠️ **PARTIALLY SUPERSEDED — see `## Layer 4` below for the retraction
> notice.** The **Layer 4 "Assembled beta system" table in this document
> is stale and must not be used.** Its `λ(126,126)=6` entry and its two
> `(unavailable, R_b=126)` placeholders are **retracted**, effective
> `vertex_terms_resolved/RESULT_126_VERTEX_TERM_RESOLVED.md` (retracts
> `λ(126,126)=6`) and `vertex_126_external_completion/RESULT_YUKAWA_BETA_126_VERTEX_COMPLETION.md`
> (closes the two "unavailable" entries). All three are replaced by
> `λ(126,10)=λ(126,120)=λ(126,126)=0`. Everything **else** in this
> document (Layers 0–3: the CG construction, `T(R)=dim(R)`, the
> real–real vertex table `λ(10,10)=−8, λ(10,120)=4, λ(120,10)=48,
> λ(120,120)=8`, and the `C₂(16)` normalization discussion) remains
> valid and is relied upon unchanged by every later document. For the
> current, correct, fully-assembled β-system, use
> `yukawa_rge_system_assembled/RESULT_YUKAWA_RGE_SYSTEM_ASSEMBLED.md`.
> This banner and the annotation at Layer 4 were added during a
> repository-consistency audit; see `CHANGELOG.md` at the repo root.

**Status: partial L1 derivation.** Most of the group-theory content needed
for `16π² β_a(Y10,Y120,Y126,g) = 0` is derived here from the existing
Cl(10) representation with machine-precision numerical proof (errors
~1e-13–1e-15, i.e. exact up to floating point). One structurally
well-defined piece is proved **not** to reduce to the naive invariant
tested, and is marked unavailable with the exact obstruction, per Ground
Rule 5/8. Nothing here was fit or imported; every number below is the
printed output of a script built on `RESULT_TASK2_3_CG_MAPS.md`'s gamma
matrices, re-run in this session (`/home/claude/work/build_cg.py` and
follow-on scripts).

Rules at risk this session: Rule 1 (a clean-looking number is not
evidence without the mechanism that forces it — every number below has
its derivation shown, not just quoted); Rule 3 (level labels below are
literal, not rounded up); Rule 9 will not be invoked here per the task
instructions (no success/failure discussion), but the labels make clear
which numbers are forced vs. still open.

============================================================
## Layer 0 — Bug found and fixed before any of this could be trusted
============================================================

`task2_3_higgs_reps.py` builds the self-dual 126 tensor by taking
**unit-Euclidean-norm** eigenvectors of the Hodge-star projector `P_sd`
over the 252-dim space of raw 5-index combinations, then forming
`Σ_k v_k · γ_{[i1..i5]}`. This preserves Euclidean norm of the
coefficient vector `v`, but **not** the Clifford-algebra (Frobenius
trace) norm of the resulting gamma matrix, because each self-dual
combination mixes two raw 5-forms with weight `1/√2` each — and the
Frobenius norm of that combination is √2 times too large relative to a
single raw generator.

**Direct check (this session):** for a raw, non-projected antisymmetrized
gamma product, `tr(M^†M)` restricted to the 16-dim chiral block is **16**
for every tested case — `k=1` (a single γ), `k=3`, and `k=5` all give
exactly 16, matching the full 32-dim trace of 32 (verified to 1e-14).
The **self-dual** 126 tensors built by the existing script instead give
chiral-block trace **32** — exactly double. This is a normalization
artifact of the eigenvector-construction step, not a physical fact.

**Fix:** rescale the 126 CG tensors by `1/√2`. After the fix, all three
channels have per-generator chiral trace `tr(M_a^†M_a) = 16` uniformly,
and (Layer 2 below) the self-energy Schur constant becomes exactly
`dim(R)` for all three reps — the value forced by the general projector
argument (see Layer 2). This is the same kind of found-and-fixed
normalization bug as the commutator/anticommutator fix already recorded
in `RESULT_TASK2_3_CG_MAPS.md`; it is filed here rather than as a silent
edit to that file, per the ground rules' own convention (Rule 4/"Phase M
corrects Phase L" template).

============================================================
## Layer 1 — Representation algebra (L1, derived)
============================================================

Using the existing `gamma_0..9.npy`, `so10_generators.npz`, and the same
charge-conjugation matrix `C` reconstructed by the SVD method of
`task2_3_higgs_reps.py`:

1. Built the 16-dim chiral subspace `V` (32×16, orthonormal) from the
   `P_L` eigenspace of the stored chirality operator (`Γ_F = P_R − P_L`,
   verified `Γ_F² = I`, `P_L+P_R=I`, `P_L²=P_L`, ranks 16/16 — all exact).
2. Confirmed the `C γ_a` bilinear has nonzero **LL** and **RR** chiral
   blocks and zero **LR** block (checked for `a=0,3`; max LR norm
   `3.8e-15`) — i.e. the 16⊗16 (not 16⊗16̄) contraction is the physically
   correct restriction, consistent with the standard SO(10) assignment
   16·16·10/120/126.
3. Built `M_a^{(10)} = V†(Cγ_a)V` (10 matrices), `M^{(120)}_{[abc]} =
   V†(Cγ_{abc})V` (120 matrices), `M_k^{(126)} = V†(Cγ^{sd}_{[5]})V/√2`
   (126 matrices, with the Layer-0 fix applied) — all 16×16.
4. Verified, restricted to this 16-dim block: rank({M^(10)})=10,
   rank({M^(120)})=120, rank({M^(126)})=126; symmetry type `M=+Mᵀ` for 10
   and 126, `M=−Mᵀ` for 120 (all exact to the stated tolerance).
5. Verified inter-channel orthogonality under the Frobenius trace pairing
   `tr(M_a^†M_b)`: within a channel this is `16·δ_ab` exactly (max
   off-diagonal ≤ 1e-13); **between** channels (10–120, 10–126, 120–126)
   it is exactly zero (max ≤ 1e-14) for every pair tested — the expected
   consequence of 10, 120, 126 being distinct irreducible summands of
   Sym²(16)=10⊕126 and Antisym²(16)=120, via Schur's lemma, now confirmed
   numerically rather than assumed.

============================================================
## Layer 2 — Invariant contractions (mostly L1 derived; one item L1-proved-unavailable)
============================================================

### 2.1 General one-loop Yukawa beta function (L2, external, cited)

Machacek–Vaughn's general one-loop result for a Yukawa term
`−(1/2)Y^a_{IJ}ψ_Iψ_Jφ_a + h.c.` (I,J combined flavor⊗gauge fermion
indices, a a real-scalar-component label; confirmed independently from
two citing sources this session, and consistent with the complex-field
adaptation used in Weyl-fermion GUT literature):

```
16π² β(Y^a) = (1/2)[Y2(F) Y^a + Y^a Y2(F)]  +  2 Y^b Y^{a†} Y^b
            + Y^b Tr(Y^{b†}Y^a)  −  3 g² {C₂(F), Y^a}
      Y2(F) ≡ Σ_b Y^{b†}Y^b   (sum over the FULL scalar index range)
```
Sources: Machacek & Vaughn, Nucl. Phys. B222 (1983) 83 and B236 (1984)
221 (original); reproduced verbatim in Chivukula–Simmons–Terning,
*Beta Functions of Orbifold Theories* (arXiv:hep-th/9906057) eq. 3.1, and
in Luo–Wang–Xiao, Phys. Rev. D67 (2003) 065019 (arXiv:hep-ph/0211440)
eq. 32–33. Labeled **L2**: this is standard, independently-verified
literature, not re-derived from a Feynman-diagram calculation in this
session.

### 2.2 Reduction to the flavor matrices Y_10, Y_120, Y_126 (L1, derived this session)

Writing `Y^a_{(i,m)(j,n)} = (Y_R)_{ij} (M_a^{(R)})_{mn}` for `a` a
component of `R∈{10,120,126}` (i,j = 1..3 flavor, m,n = 1..16 gauge),
each term of 2.1 was reduced using the Layer-1 orthogonality/Schur facts:

- **Fermion self-energy term** `(1/2)[Y2(F)Y^a + Y^a Y2(F)]`: since
  `Y2(F)` is manifestly SO(10)-invariant in gauge indices, Schur's lemma
  forces `Σ_{a∈R} M_a^{(R)}M_a^{(R)†} = T(R)·I₁₆`. **Computed directly**
  (after the Layer-0 fix): `T(10)=10`, `T(120)=120`, `T(126)=126` — each
  exactly equal to `dim(R)` to machine precision (diag range
  e.g. `(10.000000,10.000000)`, off-diagonal ≤4e-13). This matches the
  general projector argument `Σ_a M_a⊗M_a* = P^R ⇒ Σ_a M_aM_a† =
  (dim R/16)·16·I₁₆ = dim(R)·I₁₆`, so `T(R)=dim(R)` is not a numerical
  coincidence but the forced consequence of the CG tensors being genuine
  projector-normalized Clebsch coefficients — exactly the kind of "why
  this number and not a neighboring one" mechanism Rule 1 asks for.

  ⇒ Reduces to: `(1/2){[10·Y10†Y10 + 120·Y120†Y120 + 126·Y126†Y126], Y_R}`
  for **every** external channel R (same bracket, universal).

- **Scalar-leg (trace) term** `Y^b Tr(Y^{b†}Y^a)`: the full trace factorizes
  as flavor-trace × gauge-trace, and the gauge-trace `tr(M_b^†M_a)`
  vanishes unless b and a are the *same* component of the *same*
  irrep (Layer 1.5: exact `16δ_ab` within-channel, exact zero between
  channels). So this term contributes **only** to `β(Y_R)` from `Y_R`
  itself, with coefficient exactly 16 (no R–R′ mixing at all from this
  term — a clean, derived structural fact, not assumed):
  `16 · Y_R · tr(Y_R^†Y_R)`.

- **Vertex (1PI) term** `2 Y^b Y^{a†} Y^b`: for fixed external
  `a∈R_a`, summing `b` over `R_b` gives, again by Schur (applied to the
  map `X ↦ Σ_{b∈R_b} M_b^{(R_b)} X M_b^{(R_b)}` restricted to
  `X=M_a^{(R_a)†}`), a result proportional to `M_a^{(R_a)}` **when the
  map is genuinely SO(10)-equivariant** — verified case-by-case:

  | R_b \ R_a | 10 | 120 | 126 |
  |---|---|---|---|
  | **10**  | λ = **−8** (exact, resid ≤6e-15) | λ = **4** (exact) | λ = **0** (exact) |
  | **120** | λ = **48** (exact) | λ = **8** (exact) | λ = **0** (exact) |
  | **126** | **not Schur-consistent — see 2.3** | **not Schur-consistent — see 2.3** | λ = **6** (exact, resid ≤7e-14) |

  All the "exact" entries were checked against **every** component `a`
  in the target channel (10, 120, or 126 values of a respectively), with
  the ratio constant across all of them to ≤7e-14 — i.e. genuinely
  Schur-forced, not a fitted average.

### 2.3 The one item proved unavailable

`λ(R_b=126, R_a=10)` and `λ(R_b=126, R_a=120)` are **not** single
numbers: the map `X ↦ Σ_{b∈126} M_b X M_b` (no conjugation on the
repeated 126 index) evaluated at `X=M_a^{(10)†}` does **not** return a
multiple of `M_a^{(10)}` — the ratio `tr(M_a^†S)/tr(M_a^†M_a)` takes (at
least) two *different* exact values across the 10 components of `a`
(numerically: **126** for one component, **−14** for the other nine,
each individually flat to ≤6e-14 — i.e. this is a hard multiplicity
split, not numerical noise). By Schur's lemma this is only possible if
the tested map is **not actually an SO(10)-equivariant operator** on the
irreducible 10.

**Exact obstruction, algebraically identified (not just numerically
observed):** 126 is a genuinely **complex** SO(10) representation
(`126 ≇ 126̄`; its Hodge-self-duality eigenvalue is `+i`, forced complex
because the real Hodge operator on 5-forms squares to `−I`, verified
this session and in the earlier `RESULT_TASK2_3_CG_MAPS.md` derivation).
For a compact group, self-duality of a representation (`R≅R*`) is
equivalent to `R` being real or pseudoreal. Since 126 is neither,
`Σ_{b∈126} M_b⊗M_b` (both legs uncontracted with a conjugate) is
**not** a well-defined SO(10)-invariant tensor — there is no natural
pairing of 126 with itself, only of 126 with 126̄. The `10`/`120` cases
in the same row of the table above were consistent precisely *because*
10 and 120 are real representations (`M_a=M_a^*`), so the
conjugation ambiguity is invisible there; it is not invisible for 126.

Attempting the conjugated alternative `Σ_{b∈126} M_b X M_b^*` was also
checked and **also fails** to restore a clean Schur ratio (checked
explicitly this session — non-uniform for R_a=10, 120, **and** now also
for R_a=126, where the unconjugated version had been clean). This rules
out "just insert a conjugate" as a fix.

**What is actually needed and is not yet built:** the physical
one-loop vertex diagram with a 126_H (not 126̄_H) running in the loop and
external 10_H or 120_H legs is only nonzero if there is a genuine SO(10)
singlet in the relevant triple product — this is precisely the group
theory content of the well-known cubic Higgs-potential invariant
`10_H·120_H·126_H` (and its cousins), i.e. a genuinely **new** invariant
tensor `κ_{a b c}` living in `10⊗120⊗126` (or `120⊗120⊗126` /
`10⊗10⊗126`, whichever channel is relevant), not a bilinear sandwich of
the kind used above. **No such tensor has been constructed anywhere in
this project's files** (`RESULT_TASK2_3_CG_MAPS.md` only builds the
CG maps for 16⊗16→{10,120,126}, not the triple-Higgs invariant). Its
construction (e.g. from `tr(Γ_a^{(10)}Γ_b^{(120)}Γ_c^{(126)})`-type
Clifford-algebra contractions with the correct self-dual projector
inserted, or equivalently from `10⊗120→126̄` branching multiplicities)
is a well-defined, tractable next task, but it is a **different**
computation from the one attempted here, and was not carried out.

**Verdict:** `λ(126,10)` and `λ(126,120)` are marked **(c) formally
unavailable** — not "hard to compute" but *provably not expressible* as
the single Schur scalar the ansatz assumed, with the precise algebraic
reason (126's complex, non-self-dual reality type) identified rather
than merely observed.

============================================================
## Layer 3 — Diagram combinatorics (L2)
============================================================

The prefactors `(1/2)`, `2`, `1` (trace term), `−3` (gauge term) in
Section 2.1 are exactly the Machacek–Vaughn combinatorial factors
(symmetry factors of the three fermion-self-energy/vertex/scalar-leg
diagrams and the gauge one-loop fermion self-energy diagram) — cited,
not re-derived by direct Feynman-diagram computation in this session
(that would mean redoing the original MV loop integral, which is outside
this session's scope and unnecessary given it is standard, cross-checked
literature). Labeled **L2**.

The quadratic Casimir `C₂(16)` needed for the gauge term was computed
directly from the stored `Σ_ab` generators (45 of them), restricted to
the 16-dim chiral block: `Σ_{a<b} Σ_ab† Σ_ab = 11.25·I₁₆` exactly (diag
range `(11.25,11.25)`, off-diagonal exactly 0). This is **L1**, but its
numerical value (11.25 = 45/4, vs. the commonly quoted `C₂(16)=45/8` in
a differently-normalized generator convention) is only meaningful
**together with** whatever normalization of `g` is used for the gauge
term — flagged so it is not silently combined with a `g` defined in a
different convention.

> ⚠️ **Repository-consistency flag (added post-hoc, not resolved here):**
> `docs_new/SESSION_RESULT_2LOOP_GAUGE_YUKAWA_CLOSURE_TASKS_1_6.md`
> (a later, separate session in this repository) adopts
> `C₂(16)=45/8` by external citation (arXiv:2403.12914 Table 9) as a
> settled input, without cross-referencing or reconciling it against
> this document's own first-principles `45/4` computation above. The
> two documents therefore currently disagree, in-repo, on which value
> of `C₂(16)` is correct, and neither states the other's number. This
> is **not resolved by this flag** — resolving it requires determining
> which generator-normalization convention (this document's `Σ_ab`
> construction vs. the cited paper's) is being used consistently with
> the rest of each document's gauge-coupling definitions, which is
> outside the scope of the Yukawa-vertex work in this file. Anyone
> using `C₂(16)` numerically should read both documents and pick one
> convention explicitly rather than combining a number from one with a
> `g` normalization from the other.

============================================================
## Layer 4 — Assembled beta system  —  ⚠️ RETRACTED, SEE NOTICE BELOW
============================================================

> **RETRACTION NOTICE (added post-hoc, repository-consistency pass).**
> The block immediately below is preserved verbatim **for the historical
> record only** (per Rule 4/8, "Phase M corrects Phase L" — corrections
> are filed, not silently edited out). **Do not use it.** It is wrong in
> three places:
> - `λ(126,126)=6` (the `2·6 Y_126 Y126†Y_126` term in β(Y_126)) is a
>   **basis artifact**, not a physical value — retracted in
>   `vertex_terms_resolved/RESULT_126_VERTEX_TERM_RESOLVED.md` §3, and
>   independently re-confirmed as a basis artifact (two inequivalent
>   representative choices for the same 126 CG tensor set give λ=+6 and
>   λ=−6 respectively for the *same* physical component) during a
>   later audit.
> - The two `(unavailable, R_b=126)` placeholders in β(Y_10), β(Y_120)
>   are resolved to **exactly 0** in
>   `vertex_126_external_completion/RESULT_YUKAWA_BETA_126_VERTEX_COMPLETION.md`.
>
> **Corrected values: `λ(126,10) = λ(126,120) = λ(126,126) = 0`,
> all exact, all L1.** The correct fully-assembled system is in
> `yukawa_rge_system_assembled/RESULT_YUKAWA_RGE_SYSTEM_ASSEMBLED.md`,
> reproduced here for convenience:
> ```
> 16π² β(Y_10)  = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_10}
>               + 16 Y_10 tr(Y_10†Y_10) − 16 Y_10Y10†Y10 + 96 Y_120Y10†Y_120
>               − 3 g² {C₂(16), Y_10}
>
> 16π² β(Y_120) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_120}
>               + 16 Y_120 tr(Y_120†Y_120) + 8 Y_10Y120†Y_10 + 16 Y_120Y120†Y_120
>               − 3 g² {C₂(16), Y_120}
>
> 16π² β(Y_126) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_126}
>               + 16 Y_126 tr(Y_126†Y_126)
>               − 3 g² {C₂(16), Y_126}
> ```
> Everything else on this page (Layers 0–3) is unaffected and still
> correct.

**[STALE — historical record only, see notice above]**

```
16π² β(Y_10)  = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_10}
              + 16 Y_10 tr(Y_10†Y_10)
              + 2[ −8 Y_10 Y10†Y10  +  48 Y_120 Y10†Y_120  +  (unavailable, R_b=126) ]
              − 3 g² {C₂(16), Y_10}

16π² β(Y_120) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_120}
              + 16 Y_120 tr(Y_120†Y_120)
              + 2[ 4 Y_10 Y120†Y_10  +  8 Y_120 Y120†Y_120  +  (unavailable, R_b=126) ]
              − 3 g² {C₂(16), Y_120}

16π² β(Y_126) = (1/2){[10 Y10†Y10 + 120 Y120†Y120 + 126 Y126†Y126], Y_126}
              + 16 Y_126 tr(Y_126†Y_126)
              + 2·6 Y_126 Y126†Y_126   ⚠️ RETRACTED — see notice above, this term does not exist
              − 3 g² {C₂(16), Y_126}
```

Every numerical coefficient above other than the three marked
"unavailable" is **(a) derived** in this session from the explicit
Cl(10) representation (Layers 0–2), to machine precision, with the
mechanism stated (Schur's lemma applied to an explicitly-checked
equivariant map) rather than merely observed — satisfying Rule 1. The
combinatorial prefactors `(1/2), 16, 2, −3` are **(b) externally
verified with citation** (Layer 3). The two `λ(126,10)`, `λ(126,120)`
vertex coefficients were **(c) marked formally unavailable in this
session** ⚠️ **— superseded, now resolved to exactly 0, see retraction
notice above** — with the exact obstruction identified as the
non-self-dual reality type of 126 under the tested bilinear invariant
(this diagnosis of *why the naive test fails* remains correct; only the
conclusion "therefore unavailable" is superseded — the correct
resolution turned out not to need the missing trilinear tensor at all,
since the whole vertex sum vanishes by a selection rule instead).

No coefficient in this document was estimated, fit, or imported without
the derivation shown above. (The λ=6 and "unavailable" entries were
genuine, reproducible outputs of the code as run — not typos — which is
why they are retracted explicitly rather than deleted; see
`vertex_terms_resolved/RESULT_126_VERTEX_TERM_RESOLVED.md` §3 for the
mechanism of the error.)
