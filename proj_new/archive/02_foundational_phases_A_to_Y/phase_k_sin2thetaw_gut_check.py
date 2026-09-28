"""
Phase K: Does GUT-normalized sin^2(theta_W)=3/8 survive RG running down
to M_Z, closing (or reopening) the entanglement-minimization lead
flagged in Phase J? [L1, uses STANDARD, CITED textbook inputs -- not
re-derived from scratch, exactly as Phase A2 cites E8 branching tables
rather than re-deriving Lie theory from first principles.]
======================================================================
"""
import numpy as np

print('=' * 72)
print('Phase K: sin^2(theta_W)=3/8 GUT prediction vs measured value')
print('=' * 72)

print("""
NOTE ON WHAT THIS DOES AND DOES NOT SHOW:
sin^2(theta_W)=3/8 at the GUT scale is a THEOREM of any SO(10) or
SU(5) embedding with a correctly-normalized Cartan U(1)_Y generator --
guaranteed by the uniqueness (up to scale) of the Killing form on a
simple Lie algebra. It is NOT something Cl(10)xE8 could get "right" or
"wrong" differently from any other SO(10) model; testing it does not
distinguish this project's construction from textbook SO(10). What
CAN be tested is whether it survives standard 1-loop RG running down
to M_Z with only Standard Model particle content in between -- a
textbook calculation (see e.g. Peskin & Schroeder ch.20, or any GUT
review), not new physics, used here only to close this project's own
open question honestly.
""")

# Standard 1-loop SM beta coefficients (GUT-normalized alpha_1 = (5/3) alpha_Y)
b1, b2, b3 = 41/10, -19/6, -7

# Standard MSbar values at M_Z (textbook / PDG-derived, cited not fitted here)
a1_MZ_inv, a2_MZ_inv, a3_MZ_inv = 59.0, 29.6, 8.5

def run_inv(a_inv_MZ, b, t):
    # 1/alpha(mu) = 1/alpha(MZ) - b/(2pi) * ln(mu/MZ) ;  t = ln(mu/MZ)
    return a_inv_MZ - b / (2 * np.pi) * t

MZ = 91.1876
t = np.linspace(0, np.log(1e17 / MZ), 200000)
a1i = run_inv(a1_MZ_inv, b1, t)
a2i = run_inv(a2_MZ_inv, b2, t)
a3i = run_inv(a3_MZ_inv, b3, t)

# Find where alpha2 and alpha3 cross (defines an effective unification scale
# in the absence of exact 3-way meeting)
idx = np.argmin(np.abs(a2i - a3i))
M_X_eff = MZ * np.exp(t[idx])
a1_at_X, a2_at_X, a3_at_X = a1i[idx], a2i[idx], a3i[idx]

print(f"Where alpha2^-1 = alpha3^-1 (effective non-SUSY unification point):")
print(f"  M_X_eff ~ {M_X_eff:.2e} GeV")
print(f"  alpha2^-1 = alpha3^-1 = {a2_at_X:.2f}")
print(f"  alpha1^-1 at that same scale = {a1_at_X:.2f}  "
      f"(would need to equal the above for TRUE 3-way unification)")
mismatch = abs(a1_at_X - a2_at_X)
print(f"  mismatch: {mismatch:.2f} in inverse-alpha units "
      f"({'lines do NOT meet at a point' if mismatch > 1 else 'lines meet'})")

# Predicted sin^2(theta_W)(M_Z) if we insist on EXACT unification (alpha1=alpha2=alpha3
# at common M_X) and back-run using measured alpha_em, alpha_s only (drop alpha_2 input)
# -- standard 2-input GUT-prediction method
alpha_em_inv_MZ = 127.9
alpha_s_MZ = 0.118
a3_MZ_inv2 = 1 / alpha_s_MZ

# alpha_em^-1 = (3/5) a1^-1 ... + a2^-1 ... ; solve using running + unification constraint
# Standard closed-form result (Georgi-Quinn-Weinberg-style): with only SM content,
# unification forces:
def predict_sin2thw():
    # Solve for t_X such that a2(t_X) = a3(t_X) using ONLY alpha_s + alpha_em as inputs,
    # with alpha_2(MZ) eliminated via alpha_em and sin2thw as unknown.
    from scipy.optimize import brentq

    def sin2thw_residual(s2):
        c2 = 1 - s2
        a2_inv_MZ_guess = alpha_em_inv_MZ * s2 / 1.0  # alpha2 = alpha_em/sin2thw -> inv relation
        # alpha_em = alpha2 * sin2thw  => alpha2^-1 = sin2thw * alpha_em^-1
        a2_inv = alpha_em_inv_MZ * s2
        a1_inv = alpha_em_inv_MZ * (3/5) * c2  # alpha1=(5/3)alpha_Y, alpha_em relation, GUT norm
        a2r = run_inv(a2_inv, b2, t)
        a3r = run_inv(a3_MZ_inv2, b3, t)
        a1r = run_inv(a1_inv, b1, t)
        j = np.argmin(np.abs(a2r - a3r))
        return a1r[j] - a2r[j]

    return brentq(sin2thw_residual, 0.15, 0.30)

try:
    s2_pred = predict_sin2thw()
    print(f"\nPredicted sin^2(theta_W)(M_Z) demanding EXACT 3-way unification, "
          f"using only measured alpha_em and alpha_s as inputs:")
    print(f"  sin^2(theta_W)_predicted = {s2_pred:.4f}")
    print(f"  sin^2(theta_W)_measured  = 0.2312")
    print(f"  discrepancy = {abs(s2_pred-0.2312)/0.2312*100:.1f}%")
except Exception as e:
    print(f"solver note: {e}")

print("""
CONCLUSION:
This is the textbook result, not new physics: minimal, non-SUSY
grand-desert running (SM particle content, nothing new between M_Z and
the GUT scale) does NOT unify the three couplings at a single point,
and the sin^2(theta_W) it would predict misses the measured value by
roughly 10% -- the classic, decades-old motivation for either SUSY
GUTs or intermediate-scale matter, neither of which is available in
this framework's own algebra (Phases B/C already showed Cl(10)xE8 has
no free mass scale to place intermediate matter at, and no dynamics to
select SUSY).

This closes Phase J's flagged lead honestly: even setting aside
whether Cl(10)'s generator normalization matches SO(10)'s Killing form
(a separate, narrower check not needed given this result), the
GUT-scale value of sin^2(theta_W) does not survive down to the scale
where entanglement-minimization's Cabibbo-angle calculation is
evaluated, without new dynamics this project cannot supply. Combined
with Phase I's finding that even the raw 3/8 value barely moves the
predicted Cabibbo angle (6.2 -> 7.0 deg, vs measured 13 deg), this
lead is now closed on BOTH ends: value doesn't survive running, AND
even if it did, it wouldn't close the gap to the measured angle.
""")
