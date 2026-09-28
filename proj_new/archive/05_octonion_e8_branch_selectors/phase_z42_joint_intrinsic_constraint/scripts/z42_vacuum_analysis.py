"""
Z42 Task 3 -- intrinsic Higgs/flavon selection test.

Rule: do NOT choose a flavon direction, vacuum alignment, or VEV ratio
by hand. Derive the invariant potential space from the invariants
Task 2 actually found to exist (delta, epsilon), and nothing else.

Single SU(3)_f triplet flavon phi (3 of SU(3)_f, whatever E6 content
it also carries is irrelevant here -- Task 1/2 showed the flavor part
factors cleanly regardless):

Available invariants of (phi, phi^dagger) at each degree:
  degree 2:  delta_ij phi^i phibar^j            = |phi|^2
  degree 3:  epsilon_ijk phi^i phi^j phi^k       = 0  identically
             (antisymmetric contracted into a totally symmetric
             product of three copies of the SAME vector -- always zero,
             confirmed below to machine precision, not asserted)
  degree 3 (mixed): epsilon_ijk needs 3 unbarred (or 3 barred) indices;
             cannot be built from 2 phi + 1 phibar or similar without
             leaving free indices. No invariant here.
  degree 4+: only powers of |phi|^2 (no new generator -- consequence
             of Task 2's FFT-of-invariant-theory finding).

Conclusion forced BEFORE choosing any potential coefficients: the most
general renormalizable SU(3)_f-invariant potential for a single triplet
flavon is

    V(phi) = -mu^2 |phi|^2 + lambda |phi|^4      (mu^2, lambda free)

which is a function of |phi|^2 ONLY. This is derived, not assumed.
"""

import numpy as np
import json

rng = np.random.default_rng(7)

EPS = np.zeros((3, 3, 3), dtype=complex)
EPS[0, 1, 2] = EPS[1, 2, 0] = EPS[2, 0, 1] = 1
EPS[0, 2, 1] = EPS[2, 1, 0] = EPS[1, 0, 2] = -1


def confirm_cubic_self_contraction_vanishes(n_trials=500, tol=1e-10):
    max_val = 0.0
    for _ in range(n_trials):
        phi = rng.normal(size=3) + 1j * rng.normal(size=3)
        val = np.einsum("ijk,i,j,k->", EPS, phi, phi, phi)
        max_val = max(max_val, abs(val))
    return max_val < tol, max_val


def minimize_potential(mu2, lam, n_directions=64):
    """
    Confirm: minimization of V(phi) = -mu2 |phi|^2 + lam |phi|^4 over
    the FULL complex 3-vector space fixes |phi| but leaves a continuous
    (flat) direction -- the SU(3)_f orbit of any minimum is itself a
    minimum, at fixed radius. This is checked, not assumed: sample many
    random directions at the analytically predicted radius and confirm
    V is constant along them, then confirm off-radius points score worse.
    """
    if lam <= 0 or mu2 <= 0:
        return None
    v_star = np.sqrt(mu2 / (2 * lam))  # |phi| at the minimum, from dV/d|phi|=0
    vals = []
    for _ in range(n_directions):
        direction = rng.normal(size=3) + 1j * rng.normal(size=3)
        direction = direction / np.linalg.norm(direction)
        phi = v_star * direction
        norm2 = np.vdot(phi, phi).real
        V = -mu2 * norm2 + lam * norm2 ** 2
        vals.append(V)
    vals = np.array(vals)
    flat = np.std(vals) < 1e-10
    # off-radius check
    off = []
    for scale in (0.5, 1.5, 2.0):
        phi = v_star * scale * (rng.normal(size=3) + 1j * rng.normal(size=3))
        phi = phi / np.linalg.norm(phi) * v_star * scale
        norm2 = np.vdot(phi, phi).real
        off.append(-mu2 * norm2 + lam * norm2 ** 2)
    higher_at_min = all(o > vals.mean() - 1e-9 for o in off)
    return {
        "v_star": float(v_star),
        "V_at_minimum": float(vals.mean()),
        "flat_along_SU3f_orbit_at_fixed_radius": bool(flat),
        "std_along_orbit": float(np.std(vals)),
        "min_is_lower_than_offradius_samples": bool(higher_at_min),
    }


if __name__ == "__main__":
    cubic_ok, cubic_val = confirm_cubic_self_contraction_vanishes()
    min_result = minimize_potential(mu2=1.0, lam=0.5)

    results = {
        "cubic_self_contraction_vanishes_confirmed": bool(cubic_ok),
        "cubic_self_contraction_max_value": float(cubic_val),
        "general_invariant_potential": "V(phi) = -mu^2 |phi|^2 + lambda |phi|^4 + O(|phi|^6) -- function of |phi|^2 only",
        "number_of_independent_quartic_invariants": 1,
        "vacuum_structure": "discrete_in_magnitude_continuous_in_direction",
        "minimization_check": min_result,
        "conclusion": (
            "The invariant potential is a function of |phi|^2 alone at every "
            "order (Task 2 result). Minimization therefore always fixes |phi| "
            "to a discrete value (or leaves it at 0, depending on the sign of "
            "mu^2) but never selects a direction in SU(3)_f space: the full "
            "SU(3)_f orbit of any minimum is degenerate. The 'missing "
            "information' Z39/Z40 already identified is exactly this: no "
            "SU(3)_f-invariant potential built from a single flavon can ever "
            "supply the missing directional information, at any order, "
            "because no such invariant exists to be minimized against."
        ),
    }
    with open("results_task3.json", "w") as f:
        json.dump(results, f, indent=2)
    print(json.dumps(results, indent=2))
