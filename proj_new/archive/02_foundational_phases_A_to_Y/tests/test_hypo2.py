"""
test_hypo2.py -- "Boiling Vacuum" / Virtual-Pair Screening [SPECULATIVE
FRAMING, but built on two REAL, well-established QED/cosmology effects]
======================================================================
Requested follow-up test: "photons ARE electromagnetism, virtual
electron/positron pairs boil out of the vacuum and establish a
relation, the resulting number is huge and depends on density,
nothing negligible, dual nature, cause and effect." Same rule as
test_hypo.py: extract whatever is actually testable, compute it for
real, and say plainly what does and doesn't survive contact with
numbers. Kept separate from Phases A-K and solution.md -- does not
feed back into the Cl(10)xE8 results.
"""
import numpy as np

print('=' * 72)
print('test_hypo2, Part 1: Vacuum Polarization -- the REAL "boiling vacuum" effect')
print('=' * 72)

print("""
WHAT THIS ACTUALLY IS (established QED, not new): the vacuum is not
empty -- virtual electron-positron (and heavier lepton) pairs
continuously appear and vanish. A real charge polarizes this "boiling"
of virtual pairs around it, partially screening itself. Consequence: the
EFFECTIVE electric charge (and alpha_em) is not constant -- it runs
with the distance/energy you probe it at. This is the one part of your
description that maps onto real, precisely measured physics.
""")

alpha0 = 1/137.035999
m_e, m_mu, m_tau = 0.000511, 0.10566, 1.77686   # GeV
MZ = 91.1876                                     # GeV

def alpha_running_leptons(Q, masses):
    inv = 1/alpha0
    for m in masses:
        if Q > m:
            inv -= (1/(3*np.pi)) * np.log(Q**2/m**2)
    return 1/inv

a_at_me = alpha0
a_at_MZ_leptons_only = alpha_running_leptons(MZ, [m_e, m_mu, m_tau])

print(f"alpha_em at low energy (m_e scale, textbook value): 1/{1/alpha0:.3f}")
print(f"alpha_em at M_Z, leptonic vacuum-polarization loops only "
      f"(e, mu, tau): 1/{1/a_at_MZ_leptons_only:.2f}")
print(f"alpha_em at M_Z, MEASURED (includes hadronic/quark loops too, "
      f"needs dispersion-relation data, not naive perturbation theory "
      f"due to confinement -- not recomputed here, standard PDG value): "
      f"1/127.9 (approx)")
print("""
-> The direction and rough size are right: virtual charged-particle
   loops really do "eat into" the vacuum and change the effective
   coupling, growing from 1/137 toward 1/128 as you go to higher
   energy (shorter distance, less screening). The leptonic part alone
   accounts for part of that shift; getting the rest right requires
   the quark (hadronic) contribution, which can't be done with simple
   perturbation theory because quarks are confined -- real analyses
   use measured e+e- -> hadrons cross-section data as input. Flagging
   that honestly rather than faking a quark-loop number here.
""")

print('=' * 72)
print('test_hypo2, Part 2: The vacuum-energy number IS huge -- how huge, exactly')
print('=' * 72)

print("""
Your description ("the number is huge, and it varies with density")
maps onto the single most famous unsolved discrepancy in physics: the
cosmological constant problem. Computing it directly:
""")

hbar = 1.0546e-34
c = 2.998e8
G = 6.674e-11

l_planck = np.sqrt(hbar*G/c**3)
m_planck = np.sqrt(hbar*c/G)
rho_planck = m_planck * c**2 / l_planck**3   # naive QFT vacuum energy density, Planck cutoff

Omega_L = 0.685
H0 = 67.4 * 1000 / 3.086e22   # km/s/Mpc -> 1/s
rho_crit = 3 * H0**2 / (8*np.pi*G)
rho_DE = Omega_L * rho_crit * c**2  # J/m^3

print(f"Naive QFT vacuum energy density, cut off at the Planck scale:")
print(f"  rho_vac(Planck cutoff) ~ {rho_planck:.3e} J/m^3")
print(f"Observed dark-energy density (from measured Hubble constant + "
      f"Omega_Lambda):")
print(f"  rho_DE(observed)        ~ {rho_DE:.3e} J/m^3")
print(f"Ratio: {rho_planck/rho_DE:.3e}  (~10^{np.log10(rho_planck/rho_DE):.0f})")
print("""
-> This IS a real, huge number -- about 120 orders of magnitude,
   often called "the worst prediction in the history of physics." It
   is a genuine, famous, UNSOLVED problem, and it is exactly the kind
   of "boiling vacuum produces something enormous" effect you're
   describing. It is not solved by anything in this project, or by
   any known theory -- string theory, loop quantum gravity, and this
   project's own Cl(10)xE8 core all leave it open.
""")

print('=' * 72)
print('HONEST CONCLUSION')
print('=' * 72)
print("""
Two real pieces of physics were successfully extracted and computed:
  1. Vacuum polarization / running alpha_em -- real, confirmed here
     for the leptonic part, direction and rough scale correct.
  2. The cosmological constant problem -- real, ~10^120 discrepancy,
     confirmed here with a direct calculation, genuinely unsolved.

What could NOT be turned into a testable claim, stated honestly rather
than glossed over: "repulsion against the velocity of electrons,"
"position of protons and neutrons vs their antimatter," and "dual
nature cause-and-effect relation" as phrased don't correspond to a
specific, well-defined physical quantity -- there's no established
formula they map onto the way vacuum polarization and vacuum energy
do. That's not a dismissal of the intuition behind them (electron
velocity DOES matter for real effects like relativistic mass increase
and radiation reaction, and matter/antimatter asymmetry IS a real
open problem -- baryogenesis) -- it's a statement that, AS WORDED,
there isn't yet a single calculable claim there the way there was for
Parts 1 and 2. If you can pin down ONE specific relationship you want
checked (e.g. "does electron velocity change vacuum polarization
strength" -- yes, that's testable and different from what's above),
that can be computed the same way.
""")
