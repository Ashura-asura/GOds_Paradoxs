"""
Phase O: Sorkin's Causal-Set Cosmological-Constant Prediction -- Checked
For Real [built directly on Sorkin's actual argument, cited above,
NOT the fabricated N=1e120-picked-to-match placeholder in tests.zip]
======================================================================
Real argument (Sorkin 1990s; Ahmed-Sorkin 2012; see citations pulled
directly from arXiv:1703.07556, hep-th/9911102, arXiv:1210.2589):
spacetime volume V, expressed as N = V / l_Planck^4 causal-set
elements, has a Poisson fluctuation delta-N ~ sqrt(N). Via the
V-Lambda uncertainty relation of unimodular gravity, this induces
Lambda ~ 1/sqrt(N) ~ 1/sqrt(V) in Planck units. Computed here with
the ACTUAL observable-universe volume, not a number picked to match
the answer in advance.
"""
import numpy as np

print('=' * 72)
print("Phase O: Sorkin's causal-set Lambda prediction, computed with real numbers")
print('=' * 72)

hbar = 1.0546e-34
c = 2.998e8
G = 6.674e-11

l_planck = np.sqrt(hbar * G / c**3)
t_planck = l_planck / c
print(f"Planck length: {l_planck:.4e} m")

# Observable universe: radius ~ 4.4e26 m (comoving, ~46.5 Gly), age ~13.8 Gyr
# Use a real 4-volume estimate: R_H (Hubble radius) as the natural scale
H0 = 67.4 * 1000 / 3.086e22   # 1/s
R_H = c / H0                   # Hubble radius, m
V4 = R_H**4                    # 4-volume estimate (order of magnitude), m^4
N = V4 / l_planck**4
print(f"Hubble radius R_H = c/H0 = {R_H:.4e} m")
print(f"4-volume estimate V ~ R_H^4 = {V4:.4e} m^4")
print(f"N = V / l_Planck^4 = {N:.4e}  (causal-set element count)")

Lambda_pred_natural = 1/np.sqrt(N)   # dimensionless, in Planck units
print(f"\nSorkin's predicted |Lambda| ~ 1/sqrt(N) (dimensionless, Planck units): "
      f"{Lambda_pred_natural:.3e}")
print(f"  (order of magnitude only, per the original heuristic argument)")

# Convert to physical Lambda (1/m^2) and compare with measured value
Lambda_pred_permsq = Lambda_pred_natural / l_planck**2
Lambda_measured = 3 * (0.685) * H0**2 / c**2    # Lambda = 3 Omega_L H0^2/c^2, in 1/m^2
print(f"\nPredicted Lambda (1/m^2): {Lambda_pred_permsq:.3e}")
print(f"Measured   Lambda (1/m^2): {Lambda_measured:.3e}")
print(f"Ratio (predicted/measured): {Lambda_pred_permsq/Lambda_measured:.3f}")
print(f"Same order of magnitude: "
      f"{0.01 < Lambda_pred_permsq/Lambda_measured < 100}")

print('=' * 72)
print('HONEST CONCLUSION')
print('=' * 72)
print("""
This is real: unlike the ~10^120 mismatch from naive QFT vacuum energy
(test_hypo2), Sorkin's causal-set argument, computed here with the
actual observable-universe volume (not reverse-engineered), lands
within an order of magnitude of the measured cosmological constant.
This is a genuinely well-known result in the causal-set literature --
described by its own proponents as "the only successful prediction-
in-advance from any quantum gravity theory" (Dowker et al, cited
above) -- and it is NOT the same claim as tests.zip's causal_and_
scale.py, which picked N=1e120 by hand specifically to reproduce
10^-120 rather than deriving N from an actual volume estimate as done
here.

IMPORTANT CAVEATS, stated honestly rather than left out:
  - This predicts ORDER OF MAGNITUDE only, and by construction (Lambda
    ~ 1/sqrt(V)) will ALWAYS roughly track the current horizon scale,
    at any epoch -- meaning it doesn't uniquely postdict today's value
    so much as predict "whatever epoch you're in, Lambda will look
    about horizon-scale," which is a real, honest limitation actively
    discussed in the causal-set literature itself (the "why now"
    problem is addressed, not avoided, by "everpresent Lambda").
  - This is causal set theory's own result, not Cl(10)xE8's. Nothing
    here connects it to the Standard Model parameter problem this
    project's core phases (A-M) address. Recorded as a real, honestly
    verified result on its own terms, same category as test_hypo*.py
    -- explicitly NOT merged into solution.md.
""")
