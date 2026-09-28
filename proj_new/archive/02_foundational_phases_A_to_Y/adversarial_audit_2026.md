# ADVERSARIAL RE-AUDIT (2026-07-27)
## Cl(10) + E8 → Standard Model: Ground Rule Compliance & Scientific Status

---

## EXECUTIVE SUMMARY

The project has advanced from pure octonion algebra (Phases 1–19) to an SO(10) × SU(3)_f
model with Froggatt-Nielsen mechanism (Phases 20–34). This shift moved from rigorous
algebraic computation to parametric model-building. The result is a clear framework
for understanding CKM, PMNS, and Higgs mass, but **it does not derive any SM parameter
from Cl(10) or E8 algebra alone**.

**Verdict**: 4/8 ground rules violated. 0/19 SM parameters derived (19/19 are fitted
or approximately matched with free parameters). The structural core from Phases 1–19
(L1/L2) survives but is disconnected from the Phases 20–34 phenomenology.

---

## 1. 2026 SM EXPERIMENTAL DATA (Reference Values)

### Higgs Mass
| Source | m_H (GeV) | Year |
|--------|-----------|------|
| CMS (γγ) | 125.14 ± 0.15 | 2026 |
| CMS (γγ+4ℓ combined) | 125.07 ± 0.14 | 2026 |
| ATLAS (γγ+4ℓ combined) | 125.11 ± 0.11 | 2023 |
| **PDG average** | **125.10 ± 0.08** | 2026 |

### CKM Matrix (PDG 2026 global fit)
| Element | Value | Our best fit | Error |
|---------|-------|-------------|-------|
| λ (Wolfenstein) | 0.22501 ± 0.00068 | 0.225 (input) | 0% |
| |V_us| | 0.22431 ± 0.00085 | 0.169 | 25% |
| |V_cb| | 0.04183 +0.00079/-0.00069 | 0.039 | 7% |
| |V_ub| | 0.003732 +0.000090/-0.000085 | 0.00374 | 0.2% |
| δ (CP phase) | 1.147 ± 0.026 rad | 0 | 100% |

### PMNS (PDG 2024, still current 2026)
| Angle | Value | Our best fit | Error |
|-------|-------|-------------|-------|
| sin²θ₁₂ | 0.304 ± 0.012 | 0.59 (from |U_e2|=0.77) | 94% |
| sin²θ₂₃ | 0.573 ± 0.016 | 0.164 (from |U_μ3|=0.405) | 71% |
| sin²θ₁₃ | 0.02219 ± 0.00060 | 0.0071 (from |U_e3|=0.084) | 68% |

### Gauge couplings at M_Z (PDG 2024)
| Coupling | Value |
|----------|-------|
| α₃ | 0.1180 |
| α₂ | 0.03379 |
| α₁ (SM convention) | 0.01686 |

---

## 2. GROUND RULE COMPLIANCE

### Rule 1: No numerology
**STATUS: VIOLATED**

| Claim | Why it's numerology | Evidence |
|-------|---------------------|----------|
| FN charges (3,2,0) | Chosen to match CKM hierarchy. Any (n,n-1,0) pattern works. | Phase 19c "derivation" picks a specific Cartan direction; no algebraic constraint forces the actual values 3,2,0 vs 2,1,0 vs 5,4,0. |
| phi_10 = (ε³, ε, 1) | Chosen explicitly to match the CKM pattern. | `a10 = eps_obs**3` in phase33_solved.py:14. The exponent 3 is picked to match |V_ub| ~ ε³. |
| ε = 0.225 | Set equal to Wolfenstein λ. The "bare epsilon from E8 VEV ratio" is back-calculated to give 0.225 at M_Z. | `sol.root = 0.267` is the *solution* to `rge_eps_fast(eb) - eps_obs = 0`. The VEV ratio `v_10_3/Lambda_E8` is set to make this work. |
| SO(10) Clebsch ru=4, rd=-3 | Scanned over a range to fit CKM data, not derived. | Arrays `ru in [0.5,1,1.5,2,2.5,3,3.5,4]`, `rd in [-4.5,-4,-3.5,-3,-2.5,-2]` - grid search. |
| phi_126 VEV = (A, B, 1) | A and B are scanned to minimize CKM chi². | `A in np.linspace(0.6,1.8,13)`, `B in np.linspace(-0.8,0.2,11)`. |

**Diagnosis**: The framework has ~10 free parameters pretending to be 0.

### Rule 2: No reverse-engineering
**STATUS: VIOLATED**

The code structure claims UV→IR running, but parameter choices are IR-informed:

1. ε = 0.225 is the *observed* Wolfenstein λ. The bare ε at Λ_E₈ is then computed by *solving* `f(eb)=rge_eps_fast(eb)-eps_obs=0`. This is reverse-engineering: the observed value determines the UV parameter.

2. CKM parameters (A, B, ru, rd) are chosen by grid-scanning to minimize chi² against observed CKM values. The parameter values are determined by the data they're supposed to predict.

3. M_R structure (M1, M2, off) is scanned to match PMNS angles.

4. The y_nu/y_t ratio is a free parameter adjusted to make m_H come closer to 125 GeV.

**Correct UV→IR approach would**: Fix all parameters from algebraic constraints at Λ_E₈, then run RGE and compare to data (not the other way around).

### Rule 3: Level labeling (L1=proved, L2=verified, L3=conjecture)
**STATUS: VIOLATED - Systematic over-labeling**

| Claim | Labeled As | Should Be | Reason |
|-------|-----------|-----------|--------|
| "m_H = 125 GeV" | L2 | L3 | RGE gives 142 GeV. 125 requires unspecified threshold corrections (δλ from 126 singlet, seesaw thresholds). The 126 threshold formula in Phase 34 is ad-hoc, not from E8 algebra. |
| "ε = 0.225 from E8 VEV ratio + RGE" | L2 | L3 | The bare ε value is solved from the observed value. The "E8 adjoint VEV ratio" claim (v_10_3/Λ_E8 = 0.267) is a post-hoc assignment, not a computation. |
| "CKM from phi_10 ≠ phi_126" | L2 | L2 (qualitative) | CKM ≠ I is verified (L2). Exact angles are L3. The 25% error on Vus is structural to the FN charge assignment. |
| "PMNS from 126 seesaw" | L2 | L3 | PMNS ≠ I is verified (L2). Exact angles are L3. Current errors: U_e2 94%, U_e3 68%, U_μ3 71%. |
| "All 19 SM parameters derived" | L2 (claimed) | FALSE | No SM parameter is *derived*. ~6 parameters are fitted with ~10 free inputs. 13 parameters are never computed (fermion masses). |
| "Rule 6 satisfied" | L2 | FALSE | 10+ free parameters. |
| "Rule 8: No structural impossibility" | L2 | FALSE | See Section 4. |

**Proper level assignment**:
- **L1 (proved)**: Octonion CAR algebra, SU(3) generators, charge quantization, 105 Witt bases, vacuum overlap = 1/(2√2). These are in DISTILLED_CORE.md. NOTHING beyond Phase 19 is L1.
- **L2 (verified)**: SO(10) gamma matrices (Phase 31), SU(3)_f ε_{ijk} Yukawa structure, 3875 contains (126,3), CKM ≠ I is possible, PMNS ≠ I is possible, 3-loop SM RGE runs correctly.
- **L3 (conjecture)**: Everything in Phases 27–34: ε = 0.225, exact CKM/PMNS angles, m_H = 125 GeV, gauge unification with E6 matter.
- **L0 (false)**: "19/19 SM parameters derived", "Rule 6 satisfied", "All four problems solved".

### Rule 4: Adversarial audit always on
**STATUS: HONORED on paper, but ignored in practice**

The previous audit (adversarial_audit_failures.md) correctly identified violations, but
Phases 27–34 proceeded without addressing them:

- Old audit Rule 6 violation: "ε, Y_ν (L3 struct), M_R (L3), O(1) coeffs (L3)" → Phase 33
  claims L2 solution with same free parameters
- Old audit finding: "FN charges not derived" → Phase 33 still uses (3,2,0) without derivation
- Old audit finding: "m_H = 172 GeV (L2), 126 as L3" → Phase 33 claims "125 GeV [L2 verified]"

### Rule 5: Document failures
**STATUS: HONORED**

Failures are documented in adversarial_audit_failures.md, DISTILLED_CORE.md (Section 6),
and reality_check.md. However, Phase 33 contradicts these documented failures without
explanation.

### Rule 6: Zero free parameters
**STATUS: VIOLATED**

| Free Parameter | Role | How Fixed | Source |
|---------------|------|-----------|--------|
| FN charges q₁, q₂ | CKM hierarchy | Chosen as (3,2,0) | phase33_solved.py:13 |
| φ₁₂₆ VEV A | CKM fit | Scanned [0.6, 1.8] | phase33_solved.py:152 |
| φ₁₂₆ VEV B | CKM fit | Scanned [-0.8, 0.2] | phase33_solved.py:153 |
| SO(10) Clebsch r_u | Up/down splitting | Scanned [0.5, 4.0] | phase33_solved.py:154 |
| SO(10) Clebsch r_d | Up/down splitting | Scanned [-4.5, -1.0] | phase33_solved.py:155 |
| M_R scale M1 | Seesaw | Scanned [10¹⁰, 10¹⁵] | phase33_solved.py:201 |
| M_R scale M2 | Seesaw | Scanned [10¹², 10¹⁶] | phase33_solved.py:202 |
| M_R off-diagonal | PMNS | Scanned [0, 0.3] | phase33_solved.py:205 |
| y_ν/y_t ratio r | Higgs mass | Scanned [0, 1] | phase33_solved.py:257 |
| 126 threshold M_S | Higgs mass | Set to 10¹⁵ (guess) | phase34_complete_solve.py |
| ε (bare) | Everything | Solved from obs. | phase33_solved.py:135 |
| **Total** | **~11 free params** | | |

**Countable SM parameters from the 19 that are "derived"**:
- ε = 0.225: INPUT from observation, not derived
- V_us, V_cb, V_ub: FITTED with ~5 free params (A, B, ru, rd + FN charges)
- PMNS angles: FITTED with ~4 free params (M1, M2, off + y_nu)
- m_H: FITTED with ~2 free params (y_nu/y_t + threshold scale M_S)
- 6 quark masses: NOT computed
- 3 lepton masses: NOT computed  
- 2 CP phases: NOT computed (predicted 0, observed ~1.1 rad and ~π rad)

**Actual count**: 0/19 SM parameters derived. 6 approximately fitted with 11 free parameters.

### Rule 7: One provable step at a time
**STATUS: HONORED**

Each phase builds on the previous. The code is well-structured.

### Rule 8: Structural failure = result
**STATUS: VIOLATED - Known structural failures are ignored/overwritten**

Documented L1 structural failures (from previous audits):
1. **CKM = I from pure SU(3)_f d-symbols** (Phase 23c, L1-proved) → Phase 33 bypasses this
   by introducing a second VEV direction (φ₁₂₆) that is NOT in the minimal E8 248.
2. **ε minimum at 0 from SU(3)_f + fermion loops** (Phase 31, L1-proved) → Phase 33 bypasses
   this by treating ε as an input, not a derived minimum.
3. **No dimensionful parameter in the algebra** (DISTILLED_CORE §8.1) → Phase 33 introduces
   arbitrary scales Λ_E₈, M_R, M_S without deriving them.

These are not addressed. They are bypassed by adding free parameters.

---

## 3. SPECIFIC FINDINGS

### 3.1 Claim: "19/19 SM parameters derived from Cl(10) × E8"
**STATUS: FALSE**

| SM Parameter | Computed? | Method | Error |
|-------------|-----------|--------|-------|
| m_u, m_c, m_t | ❌ | Not in any phase file | N/A |
| m_d, m_s, m_b | ❌ | Not computed | N/A |
| m_e, m_μ, m_τ | ❌ | Not computed | N/A |
| |V_us| | ⚠️ Approx. fit | 25% |
| |V_cb| | ⚠️ Approx. fit | 7% |
| |V_ub| | ⚠️ Approx. fit | 0.2% |
| CKM δ | ❌ | Predicted 0 (obs: 1.147 rad) | 100% |
| |U_e2| | ⚠️ Approx. fit | 94% |
| |U_e3| | ⚠️ Approx. fit | 68% |
| |U_μ3| | ⚠️ Approx. fit | 71% |
| PMNS δ | ❌ | Not computed | 100% |
| m_H | ⚠️ | 142 GeV (± 1 free param: 130 GeV) | 14% |
| ε | ⚠️ | Input = 0.225 | 0% |

The 6 quark masses and 3 charged lepton masses are never computed in any phase file.
They are completely absent.

### 3.2 Claim: "Spectral action gives m_H = 125 GeV"
**STATUS: FALSE - structural gap of ~13% remains**

The spectral action formula `λ(Λ) = π²/24 × Tr(Y⁴)/Tr(Y²)²` gives `λ(Λ) ≈ 0.196`
for the off-diagonal Yukawa structure. SM 3-loop RGE from Λ_E₈ → M_Z gives:

```
λ(Λ) = 0.196 → m_H = 142 GeV  (no thresholds)
λ(Λ) = 0.196 + δλ_thresholds → m_H ≈ 130 GeV (with 126 singlet threshold)
Target: m_H = 125.10 GeV
```

The gap of 5 GeV (3.9%) between the computed result and observation requires:
- Either additional unknown threshold corrections (~8% of λ)
- Or a different spectral triple structure (Big D operator)
- Or non-perturbative effects

**None of these are computed.** The claim "125 GeV" is aspirational, not computational.

### 3.3 Claim: "Epsilon = 0.225 from E8 VEV ratio + RGE"
**STATUS: REVERSE-ENGINEERED**

The "RGE for epsilon" is not a standard RGE. ε = 〈v₂〉/〈v₃〉 is a VEV ratio.
VEV ratios do not run like Yukawa couplings. The formula used:

```python
def rge_eps_fast(eps0):
    c = yt_avg**2 / (4*np.pi**2)
    eps2_new = eps2 * np.exp(-c * L_ratio)
    return sqrt(eps2_new / (1 + eps2 - eps2_new))
```

has no basis in perturbative QFT. The "bare epsilon" `eb = 0.267` is then
solved from `rge_eps_fast(eb) - 0.225 = 0`, which is circular.

Additionally, Phase 31 (L1) proved that the SU(3)_f + fermion loop potential
gives ε minimum at 0, not 0.225. The Phase 33 "RGE solution" does not resolve
this structural contradiction.

### 3.4 Claim: "CKM from phi_10 ≠ phi_126 with different SO(10) Clebsch"
**STATUS: QUALITATIVELY CORRECT (L2), QUANTITATIVELY UNPREDICTIVE (L3)**

The mechanism of misaligned VEV directions + different up/down SO(10) Clebsch
DOES produce CKM ≠ I. This is a valid mechanism.

However:
- Vus = 0.169 ± 25% from 0.224 — the Cabibbo angle is not predicted
- The FN charges (3,2,0) are chosen to produce |V_ub| ≈ ε³ but this gives Vus ≈ ε¹ = 0.225, which the actual model does NOT reproduce (Vus=0.169 in best fit)
- This is the same FN model used in hundreds of published papers — nothing novel
- The SO(10) × SU(3)_f combination is a known GUT+flavor approach (e.g., King, Ross, etc.)

### 3.5 Claim: "PMNS from 126 seesaw with M_R = M1*I + M2*Y_126"
**STATUS: QUALITATIVELY CORRECT (L2), QUANTITATIVELY UNPREDICTIVE (L3)**

The seesaw mechanism produces non-diagonal PMNS. But:
- |U_e2| = 0.77 (obs: 0.53, 45% error)
- |U_e3| = 0.084 (obs: 0.145, 42% error)  
- |U_μ3| = 0.405 (obs: 0.67, 40% error)
- Neutrino masses are 6-12 orders of magnitude too small (10⁻¹² eV vs 10⁻² eV)

The neutrino sector is structurally the weakest part of the model.

### 3.6 Claim: "Gauge unification with 126 matter"
**STATUS: MISLEADING**

SM 2-loop RGE already shows g₂ ≈ g₃ at ~3×10¹⁶ GeV (this is well-known).
Adding E6 matter worsens the fit: g₂/g₃ = 1.15 vs 1.02 without.
The g₁ mismatch is 10% in both cases.

The claim "gauge unification at Λ_E₈" is not supported by the computation.

---

## 4. STRUCTURAL FAILURES (Rule 8)

### L1-Proved (Mathematically Certain)

| Failure | Phase | Description |
|---------|-------|-------------|
| ε minimum at 0 | 31 | SU(3)_f + fermion loops give V_eff minimum at ε = 0. The -ε²/(1+ε²)³ form requires E8 structure not present in Cl(10) alone. |
| CKM = I from pure 248 | 23c | Minimal E8 adjoint 248 has no 126 rep. Up/down Yukawas are from same SU(3)_f structure → CKM = I. |
| PMNS = I from pure 248 | 30 | Same reason: Y_ν ∝ M_R in minimal 248. |
| No dimensionful parameter | Core | Charge spectrum, overlaps, weights are all dimensionless. Absolute masses, VEVs, and scales require external input. |
| 16-dim Witt degeneracy | 13 | a·a† = I/2 → every state has Q = 1/2. |

These are NOT addressed by Phases 27–34. The solution is to add new structures
(3875 rep, φ₁₂₆, M_R, FN charges) that are not derived from Cl(10) or E8.

### L2-Verified Limitations

| Limitation | Phase | Description |
|------------|-------|-------------|
| 3875 contains (126,3) | 30 | Verified, but (126,3) is not in the minimal 248. Requires non-adjoint E8 rep. |
| CKM ≠ I is possible | 30-33 | Verified with φ₁₀ ≠ φ₁₂₆ + diff Clebsch |
| PMNS ≠ I is possible | 30-33 | Verified with 126 seesaw |
| m_H ≥ 142 GeV from spectral action | 27,33 | Verified with 3-loop SM RGE |
| SO(10) gamma matrices | 31 | Verified in 16D Weyl rep |

### L3 Conjectures (Not Resolved, Some Probably Wrong)

| Conjecture | Status | Why Unresolved |
|------------|--------|----------------|
| ε = 0.225 from E8 potential | Contradicted by Phase 31 L1 | SU(3)_f alone gives ε minimum at 0. E8 cross terms needed but not computed. |
| Exact CKM angles from φ₁₂₆ | Unlikely without tuning | 25% error on Vus is structural — FN charges (3,2,0) give Vus ≈ 0.17, not 0.224. Fixing this requires changing the FN charges, which changes all other predictions. |
| m_H = 125 GeV via thresholds | Uncomputed | 5 GeV gap requires ~8% correction to λ. Threshold corrections of this magnitude need explicit 2-loop matching. |
| Gauge unification at Λ_E₈ | Not supported | g1 off by 10%. Adding E6 matter makes it worse (g1 overshoots). |
| PMNS large angles from 126 | Needs O(1) tuning | Current fit errors: 40-94% per angle. |

---

## 5. FRAMEWORK-SCIENCE MISMATCH

### What the framework actually does (vs what it claims)

**Actually does** (L1+L2, from Phases 1–19):
- Constructs CAR algebra from octonion L_i matrices → charge quantization
- Finds 105 valid Witt bases
- Identifies 3 "maximally distinct" vacuums with overlap 1/(2√2)
- Constructs SU(3) generators from ladder operators
- Shows SU(3) preserves the vacuum
- Computes color overlap matrices

**Claims but does not do** (Phases 20–34):
- Derive FN charges from E8 (makes up (3,2,0))
- Derive ε = 0.225 (solves from observation)
- Derive CKM angles (fits with 5 free params)
- Derive PMNS angles (fits with 4 free params)
- Derive m_H = 125 GeV (computes 142 GeV, waves hands at thresholds)
- Derive gauge unification (uses SM running, ignores that E6 matter breaks it)
- Derive 19/19 SM parameters (computes 0)

### Comparison with published literature

The SO(10) × SU(3)_f model with Froggatt-Nielsen mechanism in Phases 30–34 is
a **standard GUT flavor model**, similar to hundreds of published papers (King,
Ross, Varzielas, etc.). The Cl(10)/E8 algebraic framework from Phases 1–19
provides NO additional predictive power to this flavor model — the parameters
(charges, VEVs, Clebsch) are equally free.

**The spectral action approach to m_H** (Chamseddine-Connes-Devastato-Lizzi)
is a separate research program. The formula `λ(Λ) = π²/24 × Tr(Y⁴)/Tr(Y²)²`
is from the NCG literature, not from Cl(10) or E8.

---

## 6. RECOMMENDATIONS

### Necessary corrections:

1. **Phase 33 claims**: Downgrade to L3 with explicit error bars.
   - "19/19 SM parameters derived" → DELETE (0/19 derived, ~6 approximately fitted)
   - "All four problems solved" → DELETE (only qualitatively addressed)
   - "Rule 6 satisfied" → DELETE (10+ free parameters)
   - "m_H = 125 GeV [L2]" → "142 GeV [L2], 125 GeV requires uncomputed thresholds [L3]"
   - "ε = 0.225 [L2]" → "ε = 0.225 is input [L3]"
   - "CKM from φ₁₀ ≠ φ₁₂₆ [L2]" → "CKM ≠ I is possible [L2], exact angles are fitted [L3]"

2. **Phase 31 L1 result**: The ε-minimum-at-0 theorem must be explicitly addressed
   before claiming ε is solved. Phase 33 contradicts Phase 31 without explanation.

3. **Rule 6 audit**: Count free parameters honestly. List them all. Mark as
   CURRENTLY VIOLATED with path to resolution.

4. **New direction**: If the goal is a testable E8 GUT, the correct approach is:
   - Derive FN charges from E8 breaking pattern (specific U(1) ⊂ E6)
   - Derive φ₁₂₆ VEV from E8 potential minimization
   - Compute 126 threshold from E8 scalar masses
   - Compute CP phases from complex VEV phases (requires E8 potential)

### What would need to change for Rule 6 compliance:

| Parameter | Current Status | How to Derive from Cl(10)+E8 |
|-----------|---------------|------------------------------|
| FN charges | Chosen (3,2,0) | From E8→E6×SU(3)_F→SO(10)×U(1)_FN branching. Specific U(1)_FN charges from the E8 root system. |
| φ₁₂₆ VEV | Fitted (A,B) | From E8 potential minimization with (10,3) + (126,3) cross terms. |
| SO(10) Clebsch | Fitted (ru,rd) | From explicit 10 and 126 Yukawa coupling computation. |
| M_R | Scanned | From Higgs VEV in (126,3) × (126̄,3̄) contraction. |
| y_ν/y_t | Scanned | From D-term minimization in E8 potential. |
| ε = v₂/v₃ | Solved from obs | From E8 adjoint potential minimization with a₄ + a₆ terms. |

None of these are currently derived.

---

## 7. FINAL ACCOUNTING

```
L1 (proved): 8 results      (from Phases 1-19, DISTILLED_CORE.md)
L2 (verified): 6 results    (SO(10) gammas, ε_{ijk} Yukawa, 3875 cont., CKM≠I possibility, PMNS≠I possibility, SM RGE)
L3 (conjecture): ~12        (exact CKM/PMNS, ε=0.225, m_H=125, gauge unification, DM, proton decay)
L0 (false): ~5 claims        (19/19 params derived, Rule 6 satisfied, Phase 33 "solved")
```

| Ground Rule | Status | What Must Change |
|-------------|--------|------------------|
| 1. No numerology | ❌ VIOLATED | Derive FN charges, φ VEVs, and Clebsch from E8 algebra |
| 2. No reverse-engineering | ❌ VIOLATED | Fix all parameters at Λ_E₈, run RGE to M_Z, compare |
| 3. Level labeling | ❌ VIOLATED | Downgrade Phase 33 claims to honest L3 with error bars |
| 4. Audit always on | ⚠️ Partial | Previous audit findings are correct but ignored |
| 5. Document failures | ✅ HONORED | Existing docs are good |
| 6. Zero free parameters | ❌ VIOLATED | 10+ free params, 0/19 derived |
| 7. One step at a time | ✅ HONORED | Code is well-structured |
| 8. Structural failure = result | ❌ VIOLATED | L1 structural failures (ε min at 0, no 126 in 248) are bypassed |

**Recommendation**: Downgrade Phase 33 claims to L3, separate the L1 algebraic results
from the L3 parametric model, and pursue honest GUT model-building if the goal
is testable predictions.
