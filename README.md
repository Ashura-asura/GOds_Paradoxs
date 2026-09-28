# GOds_Paradoxs

A research program investigating whether the Standard Model can be derived from geometric and algebraic first principles, using non-commutative geometry, Clifford algebra, octonions, and exceptional structures.

This repository is not a polished physics theory package. It is a transparent, staged research project documenting a specific claim, the current state of evidence, and the honest failure modes encountered along the way.

Current status: 0/19 Standard Model parameters derived from the proposed construction so far; approximately 13 remain under active investigation or unresolved.

---

## Research Question

Can a Dirac operator built from Cl(10), octonion/E8-related data, together with the standard spectral-triple axioms, force the observed number of fermion generations and recover Standard Model parameters from first principles?

The motivating claim under investigation is:

> A Dirac operator built from Cl(10)/octonion/E8 data forces N_g = 3 under reality + first-order + orientability + Poincaré duality + KO-dimension 6.

This project tracks the evidence for and against that claim with explicit methodological rigor.

---

## Project Philosophy

This repository follows a strict, honest scientific workflow:

- Prior art is locked before major investment.
- Minimal constructions are tested before any complexity is added.
- Claims are checked against the literature and cross-validated independently.
- Negative results are treated as valid research outcomes, not failure to publish.
- Open questions and unresolved issues are documented in plain language.

The guiding principle is simple: if a minimal construction fails, that is the answer; we do not add ad hoc complexity to rescue a weak model.

---

## Repository Structure

```text
GOds_Paradoxs/
├── README.md
├── proj_new/
│   └── ACTIVE_phase_S/
│       ├── phase_S0_prior_art_lock/
│       │   └── README.md
│       ├── phase_S1_formulation/
│       ├── phase_S2_minimal_construction/
│       ├── phase_S3_cross_verification/
│       └── phase_S4_full_construction/
├── archive_pre_S/
│   ├── phases_below_Z_25/
│   └── session_new_files/
└── ...
```

The active work is organized by research phase.

---

## Phase Overview

### Phase S0 — Prior Art Lock

Status: Completed.

This phase checks the closest existing literature and the strongest precedent for the core claim before any substantial construction work proceeds.

Key findings from the current prior-art review:

- Chamseddine & Connes (2007) explicitly identify N = 3 and quaternion-linearity as unresolved in the finite spectral-triple classification.
- Boyle (2020/2026) connects three generations to SO(8) triality and exceptional Jordan algebra ideas, but the argument remains suggestive rather than definitive.
- Farnsworth & Boyle (2013/2015) built octonionic spectral-action ideas, but did not recover the Standard Model generation count.
- The specific claim that the five spectral-triple axioms alone force N_g = 3 from Cl(10)/octonion/E8 data remains open according to the reviewed prior art.

See: `proj_new/ACTIVE_phase_S/phase_S0_prior_art_lock/README.md`

### Phase S1 — Formulation

Status: In progress / gated.

This phase formalizes the construction and defines the exact axiom checks, selection strategy, and success criteria before code is written.

The goal is to choose the smallest viable route and specify precisely:

1. Which construction is being tested
2. Which axioms are imposed
3. How each axiom is checked
4. What constitutes a valid success or failure outcome

### Phase S2 — Minimal Construction

Status: Blocked until S1 is complete.

The objective is to build the smallest possible version of the chosen construction, and to test the five axioms in the cheapest-to-falsify order.

Valid outcomes are explicitly defined:

- Positive: all five axioms pass uniquely at N = 3
- Negative: a specific axiom fails or the selection is not unique
- Underdetermined: multiple N values pass or the axioms do not constrain N

The project refuses to add complexity as a rescue strategy when the minimal case fails.

### Phase S3 — Independent Cross-Verification

Status: Blocked until S2 produces a result.

Every claim produced in S2 is independently reproduced.

- Algebraic claims are checked with exact arithmetic.
- Cross-checks are performed with independent tools.
- Disagreements are not deferred; they must be resolved before moving on.

### Phase S4 — Full Construction

Status: Blocked until S3 passes.

Only after the minimal construction is validated and cross-checked does the project scale toward a larger E8-based construction.

---

## Current Scientific Position

The project is intentionally candid about the current state of the work:

- 0/19 parameters have been derived from the proposed route so far.
- Roughly 13 parameters remain unresolved or under investigation.
- The central hypothesis remains open and is not being presented as established fact.
- The repository makes a special effort to document failure modes, missing assumptions, and unresolved structural constraints.

This is not a polished success story. It is a serious attempt to test a difficult claim under explicit standards.

---

## Why This Repository Exists

This project exists to answer a specific research question with explicit intellectual honesty:

- Does the chosen algebraic and geometric construction actually recover Standard Model structure?
- Does a Dirac operator built from Cl(10)/octonion/E8 data constrain the generation count and parameters?
- If not, where exactly do the assumptions break down?

The repository therefore records both promising structures and failed attempts, because both are scientifically valuable.

---

## Technical Standards

The project emphasizes methodological discipline:

- Exact arithmetic for algebraic calculations where possible
- Independent verification of nontrivial claims
- Explicit reporting of numerical tolerances and sample sizes
- No vague hand-waving in place of proof
- No fabrication of evidence or overstatement of conclusions

This is especially important in a field where attractive but underdetermined constructions can easily obscure the actual logic of the argument.

---

## Key Literature and Prior Art

The repository draws from work in:

- non-commutative geometry
- spectral triples
- Clifford algebras and KO-theory
- exceptional Jordan algebras
- octonions and E8-related structures
- Standard Model reconstruction from algebraic geometry

Representative references include:

- Chamseddine & Connes, 2007 — Why the Standard Model
- Farnsworth & Boyle, 2013/2015 — Non-Associative Geometry and the Spectral Action Principle
- Todorov & Dubois-Violette, 2018 — Exceptional Jordan algebra and Standard Model symmetry
- Boyle, 2020/2026 — Standard Model, exceptional Jordan algebra, and triality
- Distler & Garibaldi, 2009/2010 — no-go results related to E8 embeddings

More complete discussion and the literature matrix are kept in the phase-specific README files.

---

## Repository Notes

This project is intentionally transparent about uncertainty. It is not a claim that the framework is complete, proven, or fully successful. It is a research archive of a difficult, incomplete, but disciplined attempt to derive structure from algebraic geometry and non-commutative spectral theory.

---

## License

Repository content is provided for research transparency and reproducibility. Please respect the rights of the original authors and cite the relevant source material when reusing any result, derivation, or discussion from this project.

---

## Status

Active research repository.

Last updated: 2026-09-28

Project direction: systematic testing of a geometric derivation of Standard Model structure, with strict gates, transparent reporting, and open documentation of failure modes.
