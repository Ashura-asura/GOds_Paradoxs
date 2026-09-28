"""
Phase F: Restoring Anomaly-Freedom with Messenger Matter [L1, NEW]
======================================================================
Ground rules: 1-8 strictly enforced.

Phase E showed: with only the 3 chiral SO(10) 16-plets from the E8
branching, gauged U(1)_F anomaly-freedom forces charges (n,-n,0),
which cannot fit the observed mass hierarchy, and the fitted charges
q=(3,2,0) are anomalous (sum=5, cube-sum=35).

Avenue #1 from the literature survey: real anomalous-U(1) FN models
fix this by adding vector-like "messenger" matter -- fields that are
vector-like (non-chiral) under the Standard Model but CAN be chiral
under U(1)_F, so they shift the anomaly sums without adding new light
chiral SM states.

THIS PHASE ASKS: can messenger matter be added so that q=(3,2,0)
becomes anomaly-free, without changing the fitted charges?

RESULT (L1, constructive proof):
  YES -- exactly ONE vector-like pair (16_M + 16bar_M) of SO(10)
  multiplets, with U(1)_F charges (-2, +3) on the (16_M, 16bar_M)
  parts respectively, exactly cancels both anomaly conditions for
  q=(3,2,0). This is solved for explicitly below, not searched by fit.

BUT: this does NOT reduce the free-parameter count relative to Phase D.
It shows CONSISTENCY is achievable, at the cost of:
  (a) committing to a specific messenger representation (why 16+16bar
      and not some other SO(10) rep? -- a new, undetermined choice)
  (b) a new mass scale M_messenger for the vector-like pair (free)
  (c) the messenger charges here were SOLVED FOR to cancel the
      anomaly of the ALREADY-FITTED charges (3,2,0) -- this is
      construction-by-consistency, not derivation. If Rule 2 (no
      reverse-engineering) is applied strictly, using data-fitted
      charges as the target to solve the messenger charges against
      is exactly the pattern Rule 2 forbids, just moved one level up.

CONCLUSION: the free-parameter problem is relocated, not solved.
Net count after Phase F: >= 13 (Phase D) + >= 1 new (messenger mass
scale) + an unfixed choice of messenger representation.
"""

import numpy as np

print('='*72)
print('Phase F: Restoring Anomaly-Freedom with Messenger Matter [L1]')
print('='*72)

# =====================================================================
# 1. Recall the Phase E deficit for q=(3,2,0)
# =====================================================================
q = (3, 2, 0)
lin_deficit = sum(q)
cubic_deficit = sum(qi**3 for qi in q)
print(f'\nPhase D charges q={q}')
print(f'  Linear anomaly (needs 0):  {lin_deficit}')
print(f'  Cubic anomaly  (needs 0):  {cubic_deficit}')

# =====================================================================
# 2. Solve for a single vector-like messenger pair (16_M, 16bar_M)
#    that exactly cancels both deficits.
#
#    A 16bar with U(1)_F charge p' contributes to ODD-degree anomalies
#    (linear, cubic) exactly like an ordinary 16 with charge -p'
#    (charge-conjugate rep flips sign of odd-degree anomaly
#    coefficients; combined with the explicit charge, the two minus
#    signs cancel for odd n). So a pair (16_M charge x, 16bar_M charge
#    -y-as-if-16) contributes (x + y) to the linear sum and
#    (x^3 + y^3) to the cubic sum, same functional form as ordinary
#    generations.
# =====================================================================
print('\n--- Solve for messenger charges (x, y) ---')
print('  Need:  lin_deficit + (x + y) = 0')
print('         cubic_deficit + (x^3 + y^3) = 0')

s = -lin_deficit  # x + y
# x^3 + y^3 = s*(s^2 - 3xy) = -cubic_deficit
#  => xy = (s^2 - (-cubic_deficit)/s) / 3   [only valid if s != 0]
xy = (s**2 - (-cubic_deficit) / s) / 3
roots = np.roots([1, -s, xy])
x, y = roots.real
print(f'  s = x+y = {s}')
print(f'  xy = {xy}')
print(f'  => (x, y) = ({x:.0f}, {y:.0f})')

lin_check = lin_deficit + (x + y)
cubic_check = cubic_deficit + (x**3 + y**3)
print(f'\n  Verification:')
print(f'    Total linear anomaly = {lin_deficit} + ({x:.0f}) + ({y:.0f}) = {lin_check:.6f}  (need 0)')
print(f'    Total cubic  anomaly = {cubic_deficit} + ({x:.0f})^3 + ({y:.0f})^3 = {cubic_check:.6f}  (need 0)')

print(f'''
  CONSTRUCTION: add one vector-like pair (16_M, 16bar_M) with
    U(1)_F charge of 16_M     = {x:.0f}
    U(1)_F charge of 16bar_M  = {-y:.0f}
  (using the odd-anomaly sign convention above: the 16bar contributes
   like charge {y:.0f} under this bookkeeping, i.e. the 16bar_M field
   itself carries U(1)_F charge {-y:.0f})

  This is VECTOR-LIKE under the full Standard Model (16_M + 16bar_M
  is non-chiral under SU(3)xSU(2)xU(1)), so it adds no new light
  chiral SM fermions or gauge anomalies of its own -- only the
  U(1)_F charge asymmetry matters for the U(1)_F anomaly sums.
''')

# =====================================================================
# 3. Messenger mass term and its U(1)_F charge balance
# =====================================================================
print('--- Messenger mass term ---')
phi_charge = -1  # flavon charge convention used throughout this project (Phase D)
total_messenger_charge = x + (-y)
k = -total_messenger_charge / phi_charge if phi_charge != 0 else None
print(f'  Bare mass term 16_M x 16bar_M has total U(1)_F charge = {total_messenger_charge:.0f}')
print(f'  Requires {k:.0f} power(s) of the flavon (charge {phi_charge}) to be U(1)_F invariant:')
print(f'    Mass term ~ M x eps^{k:.0f} x (16_M)(16bar_M)')
print(f'  M itself is a new free mass scale -- NOT fixed by this construction.')

# =====================================================================
# SUMMARY
# =====================================================================
print('\n' + '='*72)
print('PHASE F RESULT')
print('='*72)
print(f'''
  CONSTRUCTIVE RESULT: a single vector-like (16_M, 16bar_M) messenger
  pair with charges ({x:.0f}, {-y:.0f}) restores exact anomaly cancellation
  for the Phase D charges q=(3,2,0), while adding no new light chiral
  Standard Model states.

  WHY THIS DOES NOT RESTORE RULE 6:
  1. [Rule 2 violation, one level up] The messenger charges were
     SOLVED FOR to cancel the anomaly of charges that were themselves
     fitted to observed masses (Phase D). This is reverse-engineering
     applied to the fix, not just the original charges.
  2. [New free parameter] The messenger mass scale M is unconstrained
     by this argument -- a new free parameter.
  3. [New unfixed choice] Nothing forces the messenger representation
     to be (16, 16bar) specifically. Any SO(10) rep pair with the
     right anomaly bookkeeping works equally well; choosing one is an
     additional, undetermined modeling decision.

  NET EFFECT: consistency (anomaly-freedom + fitted hierarchy) is
  achievable, but the free-parameter count does not decrease below
  the ~13 of Phase D -- if anything it increases by the new mass
  scale and representation choice. This confirms, by explicit
  construction rather than assertion, the Phase E conclusion: the
  free-parameter problem is relocated, not solved.
''')
