# Phase S0 — Prior Art Lock

Status: DONE (based on searches actually performed in this session, 2026-08-03).
This is not exhaustive — a real S0 pass before any further investment should
redo this search independently and go deeper into each row — but it is real,
sourced, and not fabricated.

## Claim being checked
"A Dirac operator built from Cl(10)/octonion/E8 data forces N_g = 3 under
reality + first-order + orientability + Poincaré duality + KO-dim 6."

## Table

| Work | Author(s) / Year | Closest existing claim | Status re: our claim |
|---|---|---|---|
| "Why the Standard Model" | Chamseddine & Connes, 2007, arXiv:0706.3688 | Classifies finite spectral triples at K-theoretic dim 6; N=3 and quaternion-linearity both explicitly named as unresolved inputs, not derived | OPEN — authors' own words: "Three generations: We took the number N=3... as an input... it remains to find a convincing mathematical counterpart." |
| "Non-Associative Geometry and the Spectral Action Principle" | Farnsworth & Boyle, 2013/2015, arXiv:1303.1782, JHEP 07 (2015) 023 | Built spectral action directly from octonions (not the free finite algebra) | NEGATIVE DATA POINT — result was Einstein gravity + G2 gauge theory + 8 Dirac fermions (singlet + septuplet under G2). Not 3 SM generations. Direct octonion-first spectral triple did not reproduce the target. |
| "The Standard Model, The Exceptional Jordan Algebra, and Triality" | Boyle, 2020/2026, arXiv:2006.16265, J. Math. Phys. 67, 071701 (2026) | Relates existence of 3 generations to SO(8) triality via J3(O) | Explicitly framed as suggestive ("This suggests a geometric interpretation..."), not a forcing proof. Closest existing work to our claim; does not close it. |
| "Deducing the symmetry of the standard model from the automorphism and structure groups of the exceptional Jordan algebra" | Todorov & Dubois-Violette, 2018, Int. J. Mod. Phys. A33 | J3(O) automorphism/structure groups -> SM gauge group | Addresses gauge group derivation, not generation multiplicity forcing |
| "The standard model, the Pati-Salam model, and 'Jordan geometry'" | Boyle & Farnsworth, 2020, New J. Phys. 22, 073023 | Jordan-algebraic reformulation of Connes-Chamseddine | Does not resolve N=3 either, per own citations list |
| "There is no 'Theory of Everything' inside E8" | Distler & Garibaldi, 2009/2010, Comm. Math. Phys. 298, 419 | No-go for SL(2,C)+chiral-G subgroups of one E8 copy | NOT APPLICABLE to this project's E8 construction (E8 used as internal symmetry only, gravity never embedded — ToE1 hypothesis absent). Confirmed by direct code check against `phase_a2_e8_core.py` in archive. |
| SU(3) family symmetry literature (King, Ross, Appelquist-Bai-Piai, and many others, 1990s-present) | Multiple | Gauge family symmetry alone cannot generate Yukawa hierarchy; flavons required | Foundational premise of the subfield, not a discovery. Matches this project's own Z42 result (archived), which independently re-derives the same fact via Weyl's 1939 FFT for SU(3) invariants applied directly to E8's branching content. |

## Verdict
The specific claim (five spectral-triple axioms forcing N_g=3 from
Cl(10)/octonion/E8-sourced data, as opposed to the free finite algebra) is
**still open** as of this search. The nearest published attempt (Boyle
2020/2026) stops at "suggestive," and the one concrete prior attempt to build
the spectral triple directly from octonions (Farnsworth-Boyle 2013) did not
reach the Standard Model's generation count at all.

## Caveats, stated honestly
- This search was run across a handful of web searches in one session, not a
  systematic literature review. Before investing real time in S1/S2, redo
  this with actual database search (INSPIRE-HEP, arXiv full-text) and follow
  every citation chain from the papers above.
- "Still open" is the honest reading of what was found — it is not proof
  that no one has closed it; it means no closure was found.
