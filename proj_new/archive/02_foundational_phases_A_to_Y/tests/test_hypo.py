"""
test_hypo.py -- Solar-System-as-Atom Hypothesis [SPECULATIVE, NOT L1]
======================================================================
Explicitly requested test of: "sun=neutron, planetary orbits/heliosphere
as electron-proton structure vs a mirrored positron/antiproton/
antineutron structure, self-similarity between atomic and solar-system
scales." Tried honestly, on its own terms, same standard as every other
phase: formalize it into checkable claims, compute, report what
actually holds and what doesn't. This file is DELIBERATELY kept
separate from the Cl(10)xE8 phases (A-K) -- it is not derived from
that algebra and does not feed back into it. Ground rules 2, 6, 8
still apply: no reverse-engineering a "yes," no hiding the free
parameters, state exactly where and why it breaks.
"""

import numpy as np

print('=' * 72)
print('test_hypo: Solar System / Atom Self-Similarity -- Actually Tested')
print('=' * 72)

# ---------------------------------------------------------------
# CLAIM 1: this analogy is at least historically well-posed, not
# invented here. Bohr's 1913 atomic model was explicitly inspired by
# planetary orbits. So the intuition is real and has real pedigree --
# worth stating honestly before testing it.
# ---------------------------------------------------------------
print("""
CLAIM 1 (context, not a result): the atom-as-solar-system picture is
not a new idea -- Bohr's 1913 model was literally built on this
analogy. So the instinct is legitimate. The question is whether it
survives being made quantitative, which is what the rest of this file
checks.
""")

# ---------------------------------------------------------------
# CLAIM 2: is the force law that binds the solar system the same
# TYPE of force, at the same relative strength, as what binds an atom?
# Test: compute the dimensionless coupling constant for gravity
# (Sun-Earth) the same way alpha (fine structure constant) is computed
# for the electron-proton system, and compare.
# ---------------------------------------------------------------
G = 6.674e-11
hbar = 1.0546e-34
c = 2.998e8
e = 1.602e-19
eps0 = 8.854e-12
m_e = 9.109e-31
m_p = 1.673e-27
M_sun = 1.989e30
M_earth = 5.972e24

alpha_em = e**2 / (4*np.pi*eps0*hbar*c)               # ~1/137, binds H atom
alpha_G_sun_earth = G * M_sun * M_earth / (hbar*c)      # gravitational analog, Sun-Earth
alpha_G_proton_proton = G * m_p**2 / (hbar*c)           # gravitational analog, two protons

print(f"CLAIM 2: coupling-constant comparison")
print(f"  alpha_em (binds hydrogen atom, elementary masses)  = {alpha_em:.6e}")
print(f"  alpha_G  (proton-proton, elementary masses)         = {alpha_G_proton_proton:.6e}")
print(f"  alpha_G  (Sun-Earth, macroscopic masses)            = {alpha_G_sun_earth:.6e}")
print(f"  ratio alpha_em / alpha_G(proton-proton)             = {alpha_em/alpha_G_proton_proton:.3e}")
print("""
  -> Like-for-like (elementary particle masses on both sides): gravity
     is ~10^36 weaker than electromagnetism. This is the standard,
     well-known "hierarchy problem" number -- confirmed here, not new.
  -> The Sun-Earth number (2.5e70) is NOT a smaller or larger version
     of the same comparison -- it's a different regime entirely. It's
     enormous only because Sun and Earth are macroscopic masses, not
     because gravity is "acting stronger" there. This is itself the
     point: the dimensionless-coupling formula that meaningfully
     compares force TYPES only works when applied at the same
     (elementary-particle) mass scale on both sides. Plugging in
     planetary masses breaks the comparison rather than extending it
     -- which is direct evidence the atomic and solar-system regimes
     are not related by a simple scale-up, not just "different by a
     big number."
""")

# ---------------------------------------------------------------
# CLAIM 3: quantization. Atomic orbitals are quantized (fixed radii,
# n^2 scaling, from hbar). Does the solar system show anything
# structurally similar (the "shell" idea implicit in the hypothesis)?
# Test both formulas directly against real planetary data.
# ---------------------------------------------------------------
bohr_n = np.arange(1, 6)
bohr_r = (bohr_n**2) * 5.29e-11  # Bohr radius formula, meters

# Titius-Bode law (historical empirical fit, NOT derived from quantum
# mechanics -- included because it's the only real "shell-like"
# regularity anyone has found in planetary spacing)
tb_n = np.array([-np.inf, 0, 1, 2, 3, 4, 5])  # conventional indexing incl. Mercury
def titius_bode(k):
    return 0.4 + 0.3 * (2.0**k) if k >= 0 else 0.4
tb_predicted = [0.4] + [titius_bode(k) for k in range(0, 6)]
actual_au = [0.39, 0.72, 1.00, 1.52, 2.77, 5.20]  # Mercury..(Ceres)..Jupiter, AU
names = ['Mercury', 'Venus', 'Earth', 'Mars', 'Ceres/belt', 'Jupiter']

print("CLAIM 3: is there real quantization, or just an empirical pattern?")
print(f"  Bohr formula:  r_n = n^2 * a0  -> exact, DERIVED from hbar quantization")
print(f"    r_1..r_5 (angstrom): {[round(r*1e10,2) for r in bohr_r]}")
print(f"  Titius-Bode:   r_n ~ 0.4 + 0.3*2^n (AU) -> empirical FIT, no derivation")
for nm, pred, act in zip(names, tb_predicted, actual_au):
    print(f"    {nm:12s} predicted={pred:.2f} AU  actual={act:.2f} AU")
print("""
  -> Titius-Bode roughly tracks real planetary spacing (with a known
     failure at Neptune) but is NOT derived from any conservation law
     or quantization principle the way n^2 is derived from angular-
     momentum quantization in the Bohr atom. It comes from orbital
     resonance dynamics during formation (a classical, gravitational,
     initial-condition-dependent process), not from anything
     structurally resembling quantum numbers. Same surface pattern
     (discrete shells), different and non-analogous cause.
""")

# ---------------------------------------------------------------
# CLAIM 4: the matter/antimatter mirror ("positron/antiproton/
# antineutron belt") -- is there any observed antimatter structure
# in the solar system mirroring the proposed electron/proton belt?
# This is a factual, not computational, check.
# ---------------------------------------------------------------
print("""CLAIM 4: matter/antimatter mirror structure -- factual check
  The solar wind and radiation belts are measured, catalogued plasma:
  electrons and protons (ordinary matter), with only trace positrons
  and antiprotons at the ~1e-4 level, produced locally by cosmic-ray
  and solar-flare interactions -- not a structural "mirror belt."
  There is no observed large-scale antimatter component of the solar
  system of the kind the hypothesis requires. This isn't a modeling
  gap; it's directly measured (PAMELA, AMS-02, Voyager particle data).
""")

print('=' * 72)
print('HONEST CONCLUSION')
print('=' * 72)
print("""
The hypothesis is well-motivated as an intuition (Bohr had the same
one) but fails on every point that was made quantitative here:
  - Coupling strength: ~10^36 gap between gravity and EM at like-for-
    like (elementary) mass scale, and the Sun-Earth version of the
    same formula isn't a bigger/smaller version of that gap -- it's a
    different regime, showing the two systems aren't scale-linked by
    a simple multiplier (Claim 2).
  - Quantization: solar system shows an empirical resonance pattern,
    not the hbar-derived quantization that makes atomic shells
    discrete (Claim 3).
  - Antimatter mirror: not observed; directly contradicted by
    measured solar-wind and radiation-belt composition (Claim 4).

This does NOT mean "scale self-similarity" is a useless idea in
general -- dimensionless coupling ratios, renormalization-group
thinking, and fractal/self-similar structures are real and important
in physics. It means THIS specific mapping (Sun=neutron, planets as a
literal charge/anticharge mirror of atomic structure) is not
salvageable as stated; the gap is quantitative and factual, not a
matter of framing it better. Recorded here per the project's own
rules rather than left untested.
""")
