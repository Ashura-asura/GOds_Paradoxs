"""
test_hypo3.py -- "Nothing Is Independent" as a Physics Claim, Tested
Per-Species [SPECULATIVE FRAMING, built on ONE real QFT fact]
======================================================================
Requested: formalize "cause and effect -- nothing is independent, even
massless photons, every small activity affects everything else,
like a neural network" into an actual relation, per particle type, and
report what happens. Kept separate from Phases A-K / solution.md
unless it genuinely changes something there (checked at the end).
"""
import numpy as np

print('=' * 72)
print('test_hypo3: Range of Influence, Per Particle Type -- Actually Computed')
print('=' * 72)

print("""
WHAT'S ACTUALLY TRUE HERE (real QFT, not new): in interacting quantum
field theory, connected correlation functions between two points are,
strictly, never EXACTLY zero at any finite separation -- this is a real
theorem (cluster decomposition / Reeh-Schlieder). In that narrow, formal
sense, "nothing is independent" is literally correct. What it does NOT
mean is "everything affects everything with comparable strength, like a
trained neural net's weighted connections." The strength of that
influence is a specific, computable, wildly different number for each
particle type -- that's the actual content of "establish the relation
for each kind." Computed directly below.
""")

hbar = 1.0546e-34
c = 2.998e8
eV = 1.602e-19

masses_MeV = {
    'electron/positron': 0.511,
    'proton/antiproton':  938.27,
    'neutron/antineutron': 939.57,
    'photon':             0.0,
}

print(f"{'particle':22s}  {'mass (MeV)':>12s}  {'Compton wavelength (range)':>28s}")
ranges = {}
for name, m_MeV in masses_MeV.items():
    if m_MeV == 0:
        print(f"{name:22s}  {m_MeV:12.3f}  {'infinite (massless -> long-range)':>28s}")
        ranges[name] = None
    else:
        m_kg = m_MeV * 1e6 * eV / c**2
        lam_C = hbar / (m_kg * c)   # reduced Compton wavelength = natural correlation range
        ranges[name] = lam_C
        print(f"{name:22s}  {m_MeV:12.3f}  {lam_C:24.3e} m")

print("""
-> This IS the real, quantitative version of "establish the relation
   for each kind": a massive particle's field correlations decay
   roughly as exp(-r / lambda_Compton) / r -- exponentially suppressed
   beyond its own Compton wavelength. A massless one (the photon) has
   no such cutoff -- power-law decay only, technically infinite range.
   This is also the actual, textbook reason electromagnetism "reaches
   everywhere" while the nuclear forces (mediated by effectively
   massive exchanges once confinement/screening is included) do not.
""")

print('=' * 72)
print('How "negligible" becomes actually negligible -- computed, not asserted')
print('=' * 72)

lam_e = ranges['electron/positron']
for r_name, r in [('1 nanometer', 1e-9), ('1 micrometer', 1e-6),
                   ('1 millimeter', 1e-3), ('1 meter', 1.0)]:
    suppression = np.exp(-r / lam_e)
    print(f"  electron-mediated correlation at r = {r_name:14s}: "
          f"exp(-r/lambda_C) = {suppression:.3e}")

print("""
-> At 1 meter, the electron's own correlation-range suppression factor
   is effectively zero to ~10^12 decimal places (exp(-1/3.86e-13) is a
   number with roughly 4x10^11 zeros after the decimal point -- far
   too small to print meaningfully). "Never exactly zero" is formally
   true and physically irrelevant at any distance you could measure or
   care about, for any massive particle. This is the precise, honest
   content behind "nothing is independent": true as a limiting
   statement, not true as "everything meaningfully influences
   everything," which is the version the neural-network analogy
   actually implies.
""")

print('=' * 72)
print('Is "particle interactions = neural network" itself a valid physical claim?')
print('=' * 72)
print("""
No, and this is worth being precise about rather than softening: a
neural network's connections are WEIGHTED and LEARNED (adjusted by an
optimization process to minimize a loss function) -- the strength
between two nodes is history-dependent and can be rewired. A quantum
field's correlation function is FIXED by the field's mass and coupling
constants, the same everywhere, unchanging, with no learning or
adaptation. Both are "everything is connected" systems in a loose
verbal sense, but they are not the same kind of connectedness, and
nothing here shows or suggests they are governed by the same
mathematics. The metaphor is evocative; it is not a derivation, and
this file does not treat it as one.
""")

print('=' * 72)
print('DOES THIS CHANGE solution.md?')
print('=' * 72)
print("""
No. Nothing computed here bears on whether the Standard Model's 19
parameters can be derived from Cl(10)xE8 -- that question, and its
answer in solution.md, is untouched. This file adds one more honestly-
tested speculative thread, correctly walled off, per the project's own
stated design (README, "Speculative, off-framework tests" section).
solution.md is NOT being updated as a result of this file.
""")
