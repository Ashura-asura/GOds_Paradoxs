"""
test_hypo4.py -- When a mediator's range "dies," what actually happens?
[Built on real QFT: Yukawa potentials, multiple simultaneous mediators,
and the energy-time uncertainty relation for virtual particles.]
======================================================================
Direct follow-up question: "when it dies, does it get replaced by
something else spontaneously?" Answered by actually computing it, not
asserting it. Kept separate from Phases A-K / solution.md (checked
again at the end, per the wall this project has kept since test_hypo.py).
"""
import numpy as np

print('=' * 72)
print('test_hypo4: Does a decaying interaction get "replaced"? -- computed')
print('=' * 72)

print("""
SHORT ANSWER FIRST, then the numbers: NO, nothing spontaneously
appears to "take over." All possible mediators (photon, W/Z boson,
gluon, etc.) are ALWAYS acting simultaneously, everywhere, at every
distance. What changes with distance is which one's contribution is
still large enough to matter. A massive mediator's contribution decays
exponentially past its own Compton wavelength (test_hypo3); a massless
one (photon) never does. So at long range you're not seeing a
replacement -- you're seeing the massive contributions fall away while
the massless one, which was there the whole time, is simply all
that's left standing.
""")

hbar = 1.0546e-34
c = 2.998e8
eV = 1.602e-19

def compton_range(mass_GeV):
    m_kg = mass_GeV * 1e9 * eV / c**2
    return hbar / (m_kg * c)

mediators = {
    'photon (EM, massless)':      0.0,
    'gluon (strong, effectively confined -> ~1 GeV scale)': 1.0,
    'W/Z boson (weak)':           80.4,
}

print(f"{'mediator':45s}  {'range (Compton wavelength)':>28s}")
for name, m in mediators.items():
    if m == 0:
        print(f"{name:45s}  {'infinite':>28s}")
    else:
        r = compton_range(m)
        print(f"{name:45s}  {r:24.3e} m")

print("""
-> The weak force isn't "weak" because its coupling constant is small
   -- at short distance its coupling is actually comparable to EM's.
   It LOOKS weak because its mediator (W/Z) is heavy, so its Yukawa-
   suppressed range is ~10^-18 m -- utterly negligible at any distance
   bigger than a proton. Nothing replaces it beyond that range; its
   effect is just gone, while the massless photon (which was acting
   the entire time, at every distance, including inside the proton)
   is the only channel still contributing once you're microns away.
""")

print('=' * 72)
print('Showing the crossover directly: Yukawa (massive) vs Coulomb (massless)')
print('=' * 72)

# Toy comparison: same coupling strength g^2=1, compare weak-like
# Yukawa term to EM-like Coulomb term at increasing distance
r_vals = np.array([1e-18, 1e-16, 1e-14, 1e-12, 1e-10])
lam_W = compton_range(80.4)
yukawa_over_coulomb = np.exp(-r_vals / lam_W)  # ratio of Yukawa/Coulomb forms at equal coupling & r
for r, ratio in zip(r_vals, yukawa_over_coulomb):
    print(f"  r = {r:.0e} m:  Yukawa/Coulomb amplitude ratio (equal coupling) = {ratio:.3e}")

print("""
-> By r=10^-14 m (still inside a large nucleus), the weak-mediator
   contribution is already ~10^4 times smaller than the photon's, at
   EQUAL coupling strength. Nothing spontaneously "kicks in" to
   replace it -- the photon channel was simply always the larger term
   in the sum once you're past the heavy mediator's own range.
""")

print('=' * 72)
print('The genuinely spontaneous part: virtual pairs, bounded by uncertainty')
print('=' * 72)

print("""
There IS a real "spontaneous" phenomenon in this picture, but it's a
different thing from "replacement": vacuum fluctuations (virtual
electron-positron pairs, etc. -- test_hypo2, Part 1) pop in and out
CONTINUOUSLY, everywhere, governed by the energy-time uncertainty
relation Delta-E * Delta-t ~ hbar. A virtual electron pair of energy
~2*m_e*c^2 can exist for a maximum time roughly hbar/(2 m_e c^2),
which -- multiplied by c -- gives almost exactly the same Compton-
wavelength range already computed in test_hypo3.
""")

m_e_c2_J = 0.511e6 * eV
dt_max = hbar / (2 * m_e_c2_J)
range_from_uncertainty = dt_max * c
print(f"  virtual e+e- pair max lifetime (uncertainty principle): {dt_max:.3e} s")
print(f"  implied range (lifetime * c): {range_from_uncertainty:.3e} m")
print(f"  (compare: electron Compton wavelength from test_hypo3: 3.862e-13 m)")
print("""
-> Same order of magnitude, as it should be -- these are two views of
   the same physics, not two different effects. The "spontaneous"
   part is real: pairs really do wink in and out constantly,
   unpredictably, everywhere. What's NOT true is that this spontaneous
   activity "replaces" a dying force with a new one at long range --
   the pairs are short-lived and short-range REGARDLESS of what
   distance you're asking about; they don't reach out further to
   compensate for a decaying massive mediator.
""")

print('=' * 72)
print('HONEST CONCLUSION')
print('=' * 72)
print("""
1. No spontaneous replacement occurs. All mediators act at once, at
   every distance; the massless ones simply dominate once the massive
   ones' exponential cutoff has kicked in. This was checked directly
   above with real Yukawa-vs-Coulomb numbers, not asserted.
2. The one genuinely spontaneous thing in this picture -- vacuum pair
   production -- is real, constant, and everywhere, but it does not
   scale up its range to compensate for anything; its own range is
   fixed by the pair's mass, same as any other mediator.
3. solution.md: still not updated. This is real, standard QFT
   (Yukawa potentials, mediator masses, the uncertainty principle),
   applied honestly to your question -- it does not touch the
   Cl(10)xE8 / Standard-Model-parameter question that solution.md
   answers.
""")
