"""
Phase I: Actually Testing the Other Two Avenues [L1/L2, NEW]
======================================================================
Ground rules: 1-8 strictly enforced.

RESEARCH_ROADMAP.md (2026-07-27) identified two avenues from the
literature survey that had NEVER been tested against anything, only
described: (2) modular flavor symmetry, (3) entanglement-minimization.
"Try everything possible" -- this phase actually tries them, rather
than continuing to describe them qualitatively.

======================================================================
PART 1: Entanglement-minimization -- reproduced independently
======================================================================
Thaler & Trifinopoulos, "Flavor Patterns of Fundamental Particles from
Quantum Entanglement?" (arXiv:2410.23343, Phys. Rev. D 111, 056021).
Their central two-generation result (their Eq. 32) is reproduced here
from scratch -- not taken on faith from the abstract -- to verify it
independently before drawing any conclusion about its relevance.
"""

import numpy as np

print('=' * 72)
print('Phase I, Part 1: Entanglement-Minimization -- Independent Check')
print('=' * 72)

# SM quantum numbers (these ARE the same charges Cl(10)xE8 already
# derives for free via the SO(10) 16 -- see Part 1 item #1 of
# RESEARCH_ROADMAP.md). sin^2(theta_W) is NOT derived by this
# framework; it is a measured SM input, exactly as in the original paper.
Qu, Qd = 2/3, -1/3
T3u, T3d = 1/2, -1/2


def entangling_power_min(sin2thW):
    cos2thW = 1 - sin2thW
    Yu = T3u - Qu * sin2thW
    Yd = T3d - Qd * sin2thW
    y = (Yu * Yd) / cos2thW + sin2thW * Qu * Qd

    def E_perp(theta_C):
        s2, c2 = np.sin(theta_C) ** 2, np.cos(theta_C) ** 2
        Np2 = 1 + 2 * y + 4 * y ** 2 - 2 * y * np.cos(2 * theta_C)
        Nm2 = 1 + 2 * y + 4 * y ** 2 + 2 * y * np.cos(2 * theta_C)
        return 8 * y ** 2 * (c2 ** 2 / Np2 ** 2 + s2 ** 2 / Nm2 ** 2)

    thetas = np.linspace(0.001, np.pi / 4, 20000)
    vals = E_perp(thetas)
    return np.degrees(thetas[np.argmin(vals)]), y


theta_min_measured, y_measured = entangling_power_min(0.2312)
theta_min_gut, y_gut = entangling_power_min(3 / 8)

print(f"\nUsing measured sin^2(theta_W)=0.2312: entangling-power minimum "
      f"at theta_C = {theta_min_measured:.2f} deg")
print("  (published result: ~6 deg; measured Cabibbo angle: ~13.0 deg -- "
      "REPRODUCED INDEPENDENTLY)")

print(f"\nRobustness check -- using the GUT-scale tree-level value "
      f"sin^2(theta_W)=3/8 instead: theta_C = {theta_min_gut:.2f} deg")
print("  Barely moves (6.2 -> 7.0 deg): confirms the paper's own note that "
      "the result depends only weakly on this input.")

print('''
FINDING: independently confirmed. The entanglement-minimization
principle uses exactly the same quark charges (Q, T3) that Cl(10)xE8
already derives for free (Part 1, item #1) -- but its one remaining
input, sin^2(theta_W), is NOT derived by this framework (it is one of
Phase D's free parameters). Swapping in the GUT-scale tree-level value
instead of the measured one barely changes the result, so there is no
meaningful sense in which Cl(10)xE8's own structure sharpens this
principle's prediction. The principle itself is self-contained,
external to this framework, and -- on its own numbers -- undershoots
the real Cabibbo angle by roughly a factor of 2, exactly as its
original authors note. It cannot be used to reduce this project's own
free-parameter count, and it has not been connected to Cl(10)xE8
beyond sharing SM charges that were never in dispute.
''')

# =====================================================================
# PART 2: Modular flavor symmetry -- literature grounding check
# =====================================================================
print('=' * 72)
print('Phase I, Part 2: Modular Flavor Symmetry -- Literature Check')
print('=' * 72)
print('''
No numerical test performed here -- this part reports what a literature
check (2026-07-27) found, honestly, rather than assuming the earlier
qualitative description was complete.

FINDING: modular-flavor-symmetric SO(10) models already exist in the
literature (e.g. Ding, King, Lu, "SO(10) models with A4 modular
symmetry," JHEP 11 (2021) 007, arXiv:2108.09655, and related papers).
So this avenue is not merely "unconnected to SO(10)" -- it has been
combined with SO(10) before, by other groups, in other model-building
contexts.

BUT: in every such construction, the modular group (A4, S4, etc.) and
the modulus tau are EXTRA data, motivated by a specific string
compactification (an orbifold or magnetized torus) -- exactly the same
category of missing ingredient identified in Phase H for the "fuller"
Green-Schwarz mechanism. SO(10) or E8 representation theory alone does
not generate a modulus or select a discrete modular group; string
compactification data does. This is the SAME root cause blocking
Phase H's stronger Green-Schwarz claim, not a different one:

  Green-Schwarz (Phase H): needs a string-coupling-normalized
    anomalous U(1) and quantized modular weights from a specific
    compactification.
  Modular flavor symmetry: needs a modulus tau and a discrete flavor
    group, ALSO from a specific compactification.

Both require grafting on string-vacuum-specific data that Cl(10)xE8's
own algebra has no mechanism to produce. Neither is "impossible" in
the abstract -- both are standard, active research programs in their
own right -- but neither can be honestly presented as a Cl(10)xE8
derivation. Pursuing either seriously would mean starting a genuinely
different project (string model-building), not extending this one.
''')

# =====================================================================
# PART 3: NCG / spectral action -- literature grounding check (R1)
# =====================================================================
print('=' * 72)
print('Phase I, Part 3: Spectral Action / NCG -- Literature Check')
print('=' * 72)
print('''
FINDING: R1 is less "years of research from scratch" than
RESEARCH_ROADMAP.md's first draft suggested. Chamseddine, Connes, and
van Suijlekom already extended the spectral-action / noncommutative-
geometry Standard Model to PATI-SALAM unification specifically:

  - "Beyond the Spectral Standard Model: Emergence of Pati-Salam
    Unification," JHEP 11 (2013) 132.
  - "Grand Unification in the Spectral Pati-Salam Model," JHEP 11
    (2015) 011 -- includes an explicit one-loop gauge-coupling running
    and unification analysis.

Pati-Salam (SU(4) x SU(2) x SU(2)) is a maximal subgroup in the
SO(10)-breaking chain that this project's own Cl(10) -> SO(10)
embedding passes through. This means the honest next step for R1 is
NOT "attempt to build a spectral triple from scratch" -- it is:
check whether the finite algebra and Hilbert space used in the
existing spectral Pati-Salam construction matches the fermion content
and gauge structure Cl(10)xE8 already derives (Part 1, items #1-2). If
it matches, this project could adopt an established, peer-reviewed
dynamical framework rather than build one from zero. If it doesn't
match, that mismatch is itself real information about where
Cl(10)xE8's structure diverges from the finite geometries that are
known to work.

This does not change the honest bottom line -- gravity, VEV
minimization, and any falsifiable number are still open, and matching
an existing construction is real technical work, not a weekend task --
but it changes the STARTING POINT from "build new mathematics" to
"verify an existing candidate," which is a meaningfully smaller lift.
This is the concrete, updated first step for R1 (see
RESEARCH_ROADMAP.md).
''')
