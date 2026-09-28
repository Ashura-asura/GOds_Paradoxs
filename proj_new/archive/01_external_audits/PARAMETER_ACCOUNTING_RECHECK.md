# PARAMETER_ACCOUNTING_RECHECK.md — Phase 5

Recomputed independently (not inherited from `phase_c_honest_accounting.py`'s
own numbers), then compared against Phase C at the end.

## What counts as "the 19 SM parameters" (minimal SM, massless neutrinos)

1. 6 quark masses (u,d,s,c,b,t)
2. 3 charged-lepton masses (e,μ,τ)
3. 3 gauge couplings (g1,g2,g3 / α1,α2,α3, equivalently e, sin²θ_W, g_s)
4. 2 Higgs-sector parameters (μ² and λ, equivalently m_H and v)
5. 3 CKM mixing angles + 1 CKM CP phase = 4
6. 1 QCD θ-parameter (strong CP angle)

**Total: 6+3+3+2+4+1 = 19.** This matches the conventional count and
matches the project's own "19" figure.

**Independent observation (not in Phase C's own writeup):** if neutrino
masses and PMNS mixing are included — as the repository's own Phase C
output table actually does, listing |U_e2|, |U_mu3|, |U_e3|, δ_PMNS
alongside the 19 — the honest total is larger than 19 (add ≥3 neutrino
masses + 3 PMNS angles + at least 1 Dirac phase, more if Majorana). The
repository is internally inconsistent on this point: it states "19" as
the target in prose but its own Phase C table lists 23 rows (19 + 4
PMNS entries), without flagging the mismatch. This doesn't change any
conclusion (0 of either 19 or 23 are derived from algebra alone), but
it's a real, checkable accounting slip, worth naming as such.

## A) Derived (zero free parameters, from algebra alone)

None of the 19 (or 23). Re-checked directly:
- No dimensionful quantity of any kind exists in Cl(10) or E8 as
  abstract algebraic structures (both are defined over a field/reals
  with no built-in energy scale) — this genuinely rules out **all 9**
  fermion masses, m_H, v, and any threshold-dependent coupling value
  from being derived by algebra alone, independent of any dynamics
  layered on top.
- **A = 0 / 19 (or 0/23).**

## B) Constrained (not fixed to a number, but algebra rules out
   large regions of parameter space or forces a discrete structure)

- CKM = I and PMNS = I are the **forced, structural** output of the
  minimal 248 (re-verified, Phase B). This is a real, nonzero
  constraint on 4 of the 19 (the CKM sector: 3 angles + 1 phase all
  forced to their trivial values in the minimal model) — but "forced
  to a specific wrong-looking value" is not "derived to match
  observation"; CKM is not exactly the identity in nature, so this
  constraint is falsified by minimal 248 and requires new structure
  (3875 rep) to even be viable, at which point the angles are no
  longer fixed at all (see C below).
- Charge quantization forces all electric charges into {0,±1/3,±2/3,±1}
  — this constrains, but doesn't reduce, any of the 19/23 numerical
  parameters (it's a structural/topological fact, not a numeric input).
- Anomaly-freedom (Phase E) constrains FN charge *shape* to (n,−n,0),
  a genuine discrete restriction on an infinite family, but n itself
  remains free (see D).
- Phase X: any Higgs representation outside {10,120,126} is provably
  forbidden — a real, nonzero constraint on model-building, but it
  constrains which fields can exist, not any of the 19/23 numbers
  directly.
- **B = 0 of the 19/23 numerically constrained to a value; several
  structural quantities (charge quantization, forced-identity mixing
  matrices, forbidden Higgs reps) are constrained but these are not
  among the 19/23 counted parameters themselves.**

## C) Fitted (a real number chosen/solved to match observation)

Re-checked against Phase D's explicit parametric (L3) model and Phase
C's own list:
- FN breaking parameter ε ≈ 0.225 — chosen to match the Cabibbo angle.
- 126 Higgs VEV direction (2 real parameters) — chosen to fit CKM/PMNS
  once the 3875/126 extension is added.
- SO(10) Clebsch-Gordan coefficients r_u, r_d (2 parameters) — chosen
  to fit up/down quark mass ratios.
- Majorana mass scale M_R (1 parameter) — chosen to fit light-neutrino
  masses via seesaw.
- ν Yukawa-to-top ratio y_ν/y_t (1 parameter) — chosen to fit neutrino
  Dirac mass scale.
- Higgs VEV v = 246 GeV — external input, not from algebra.
- **C ≈ 7 real numbers actively fitted** to reproduce known values in
  the explicit (Phase D, L3) extended model — all correctly labeled L3
  in the source.

## D) Completely free (no algebraic constraint at all, value never
   compared to data, or compared but with no mechanism forcing the
   comparison)

- FN charge integers themselves (the specific choice n giving
  q=(3,2,0)) — 2 free integers; anomaly-freedom (B above) restricts
  the *shape* but not the *value* of n.
- 3 gauge couplings g1,g2,g3 at M_Z — these come from QFT running, not
  algebra; Cl(10)×E8 supplies no coupling values, only which groups
  exist.
- **D ≈ 3–4 genuinely unconstrained real numbers** feeding directly
  into the 19/23-parameter target, plus the FN-charge integers (2,
  discrete but arbitrary within the constrained shape).

## Independent tally

Recounting item-by-item without reference to Phase C's own labels:
FN charges (2) + ε (1) + 126-VEV direction (2) + Clebsch r_u,r_d (2) +
M_R (1) + y_ν/y_t (1) + v (1) + g1,g2,g3 (3) = **13 free inputs**,
required to extend the algebraically-derived skeleton (gauge group,
charge quantization, generation count, forced-identity CKM/PMNS in the
minimal model) into anything that can be numerically compared to the
19 (or 23) SM parameters — and even with all 13 supplied, the match to
data is approximate (Phase D, L3), not exact.

**This independently reproduces Phase C's own "~13 free parameters"
and "0/19 derived" figures.** No correction to the numerical bottom
line is warranted. The one genuine finding from doing this recount
independently is the 19-vs-23 inconsistency noted above (the
repository states its target as 19 in prose while its own Phase C
table counts 23 rows), which should be resolved by either dropping the
PMNS rows from that table or updating the stated target to reflect
that neutrino parameters are included.
